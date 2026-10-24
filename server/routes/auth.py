"""Authentication routes and parent session management.
Implements POST /api/v1/auth/login and current parent dependency.
"""

from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent
    from ..schemas import LoginRequest, TokenResponse
    from ..security import (
        verify_password,
        create_access_token,
        decode_access_token,
        check_ip_rate_limit,
        revoke_token
    )
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent
    from server.schemas import LoginRequest, TokenResponse
    from server.security import (
        verify_password,
        create_access_token,
        decode_access_token,
        check_ip_rate_limit,
        revoke_token
    )

router = APIRouter()
security_scheme = HTTPBearer(auto_error=False)


def get_current_parent(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Parent:
    """Dependency to retrieve the authenticated parent from Bearer token or session cookie."""
    token: Optional[str] = None

    if credentials and credentials.credentials:
        token = credentials.credentials
    else:
        # Fallback to session cookie
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yêu cầu xác thực tài khoản phụ huynh",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

    parent_id = payload.get("parent_id")
    if not parent_id and "sub" in payload and payload["sub"].startswith("parent:"):
        try:
            parent_id = int(payload["sub"].split(":")[1])
        except (ValueError, IndexError):
            parent_id = None

    if not parent_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin định danh trong token không hợp lệ",
        )

    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản phụ huynh không tồn tại",
        )

    return parent


@router.post("/login", response_model=TokenResponse, summary="Đăng nhập tài khoản phụ huynh")
def login(
    req: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """Authenticate parent with username/password, enforce brute-force lockout and rate limits."""
    # 1. Rate Limiting Check (10 requests/min per IP)
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not check_ip_rate_limit(client_ip, limit=10, window_seconds=60):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Quá nhiều yêu cầu đăng nhập từ địa chỉ IP này. Vui lòng thử lại sau 1 phút."
        )

    parent = db.query(Parent).filter(Parent.username == req.username).first()

    # 2. Account Lockout Check (15 minutes after 5 consecutive failures)
    now = datetime.now(timezone.utc)
    if parent and parent.locked_until:
        locked_until = parent.locked_until
        if locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=timezone.utc)
        if locked_until > now:
            remaining_secs = int((locked_until - now).total_seconds())
            remaining_mins = max(1, (remaining_secs + 59) // 60)
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Tài khoản đã bị tạm khóa do nhập sai mật khẩu quá 5 lần. Vui lòng thử lại sau {remaining_mins} phút."
            )
        else:
            # Lockout expired, reset counters
            parent.locked_until = None
            parent.failed_login_attempts = 0
            db.commit()

    # 3. Verify Password
    if not parent or not verify_password(req.password, parent.password_hash):
        if parent:
            parent.failed_login_attempts = (parent.failed_login_attempts or 0) + 1
            if parent.failed_login_attempts >= 5:
                parent.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Tài khoản đã bị tạm khóa 15 phút do nhập sai mật khẩu quá 5 lần liên tiếp."
                )
            db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
        )

    # 4. Successful Login: Reset failed attempts
    if parent.failed_login_attempts != 0 or parent.locked_until is not None:
        parent.failed_login_attempts = 0
        parent.locked_until = None
        db.commit()

    # 5. Issue Access Token (15 minutes validity)
    access_token = create_access_token({
        "sub": f"parent:{parent.id}",
        "parent_id": parent.id,
        "username": parent.username,
        "role": "parent"
    })

    # 6. Set Secure HTTP-only Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=900,
        samesite="lax"
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=900
    )


@router.post("/logout", summary="Đăng xuất và hủy phiên làm việc")
def logout(
    request: Request,
    response: Response,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)
):
    """Explicitly revoke token and clear session cookie upon logout."""
    token = credentials.credentials if credentials and credentials.credentials else request.cookies.get("access_token")
    if token:
        revoke_token(token)

    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax"
    )
    return {"message": "Đăng xuất thành công, phiên làm việc đã bị thu hồi."}

