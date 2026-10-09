"""Authentication routes and parent session management.
Implements POST /api/v1/auth/login and current parent dependency.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..models import Parent
    from ..schemas import LoginRequest, TokenResponse
    from ..security import verify_password, create_access_token, decode_access_token
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent
    from server.schemas import LoginRequest, TokenResponse
    from server.security import verify_password, create_access_token, decode_access_token

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
    response: Response,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """Authenticate parent with username/password, sets session cookie and returns access token."""
    parent = db.query(Parent).filter(Parent.username == req.username).first()
    if not parent or not verify_password(req.password, parent.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
        )

    # 15 minutes validity
    access_token = create_access_token({
        "sub": f"parent:{parent.id}",
        "parent_id": parent.id,
        "username": parent.username,
        "role": "parent"
    })

    # Set HTTP-only cookie for web dashboard
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
