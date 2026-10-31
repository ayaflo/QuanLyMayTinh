"""Parent dashboard web view routes for Open Guardian Kids.
Renders Jinja2 HTML templates for login, device management, and pairing code modals.
"""

import os
from typing import Optional
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, Request, Response, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


try:
    from ..database import get_db
    from ..models import Parent, Device, Policy, AuditLog, DomainRule, AppRule, AccessRequest, DEFAULT_SCHEDULE_MATRIX
    from ..security import (
        verify_password,
        hash_password,
        create_access_token,
        decode_access_token,
        check_ip_rate_limit,
        revoke_token
    )
    from ..services.policy_service import get_or_create_default_policy
    from ..services.report_service import get_device_report_summary, get_weekly_usage_stats
    from ..services.filtering_service import get_active_domain_rules, get_active_app_rules, get_domain_category_summaries
    from ..services.request_service import get_requests
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent, Device, Policy, AuditLog, DomainRule, AppRule, AccessRequest, DEFAULT_SCHEDULE_MATRIX
    from server.security import (
        verify_password,
        hash_password,
        create_access_token,
        decode_access_token,
        check_ip_rate_limit,
        revoke_token
    )
    from server.services.policy_service import get_or_create_default_policy
    from server.services.report_service import get_device_report_summary, get_weekly_usage_stats
    from server.services.filtering_service import get_active_domain_rules, get_active_app_rules, get_domain_category_summaries
    from server.services.request_service import get_requests

# Locate dashboard templates directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "dashboard", "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

VN_TZ = timezone(timedelta(hours=7))


def format_local_time(dt, fmt: str = "%H:%M:%S %d/%m/%Y") -> str:
    """Format a UTC datetime or ISO timestamp string into Vietnam Local Time (UTC+7 / ICT)."""
    if not dt:
        return "Chưa có" if "%H" in fmt and "%d" not in fmt else ""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except Exception:
            return dt
    if not isinstance(dt, datetime):
        return str(dt)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    local_dt = dt.astimezone(VN_TZ)
    return local_dt.strftime(fmt)


templates.env.filters["local_time"] = format_local_time
templates.env.filters["vn_time"] = format_local_time

router = APIRouter()


def get_current_parent_from_cookie(request: Request, db: Session) -> Optional[Parent]:
    """Extract authenticated parent object from HTTP cookie, or return None."""
    token = request.cookies.get("access_token")
    if not token:
        return None

    payload = decode_access_token(token)
    if not payload:
        return None

    parent_id = payload.get("parent_id")
    if not parent_id and "sub" in payload and payload["sub"].startswith("parent:"):
        try:
            parent_id = int(payload["sub"].split(":")[1])
        except (ValueError, IndexError):
            return None

    if not parent_id:
        return None

    return db.query(Parent).filter(Parent.id == parent_id).first()


@router.get("/login", response_class=HTMLResponse, summary="Hiển thị trang đăng nhập phụ huynh")
def login_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Render parent login page or redirect to /devices if already authenticated."""
    parent = get_current_parent_from_cookie(request, db)
    if parent:
        return RedirectResponse(url="/devices", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"parent": None, "error": None}
    )


@router.get("/register", response_class=HTMLResponse, summary="Hiển thị trang đăng ký phụ huynh")
def register_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Render parent registration page or redirect to /devices if already authenticated."""
    parent = get_current_parent_from_cookie(request, db)
    if parent:
        return RedirectResponse(url="/devices", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"parent": None, "error": None}
    )


@router.post("/register", response_class=HTMLResponse, summary="Xử lý đăng ký tài khoản phụ huynh từ Form HTML")
def handle_register(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Process parent self-registration, validate password and duplicates, log in and redirect."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not check_ip_rate_limit(client_ip, limit=10, window_seconds=60):
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "parent": None,
                "username": username,
                "error": "Quá nhiều yêu cầu từ IP này. Vui lòng thử lại sau 1 phút."
            },
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    clean_user = username.strip()
    if len(clean_user) < 3 or len(clean_user) > 50:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "parent": None,
                "username": username,
                "error": "Tên đăng nhập phải có độ dài từ 3 đến 50 ký tự."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if len(password) < 10:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "parent": None,
                "username": username,
                "error": "Mật khẩu phải có tối thiểu 10 ký tự (theo khuyến nghị bảo mật NIST SP 800-63B)."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "parent": None,
                "username": username,
                "error": "Mật khẩu xác nhận không khớp với mật khẩu đã nhập."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    existing = db.query(Parent).filter(Parent.username == clean_user).first()
    if existing:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "parent": None,
                "username": username,
                "error": f"Tên đăng nhập '{clean_user}' đã tồn tại trong hệ thống. Vui lòng chọn tên khác."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Create new parent record
    hashed_pwd = hash_password(password)
    new_parent = Parent(
        username=clean_user,
        password_hash=hashed_pwd
    )
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)

    # Issue access token and redirect straight into /devices
    access_token = create_access_token({
        "sub": f"parent:{new_parent.id}",
        "parent_id": new_parent.id,
        "username": new_parent.username,
        "role": "parent"
    })

    redirect = RedirectResponse(url="/devices", status_code=status.HTTP_302_FOUND)
    redirect.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=86400,  # 1 ngày liên tục (24 giờ = 86400 giây)
        samesite="lax"
    )
    return redirect


@router.post("/login", response_class=HTMLResponse, summary="Xử lý đăng nhập từ Form HTML")
def handle_login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Process login form submission, enforce rate limits and lockout, set HTTP-only cookie."""
    # 1. IP Rate Limiting Check
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not check_ip_rate_limit(client_ip, limit=10, window_seconds=60):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "parent": None,
                "username": username,
                "error": "Quá nhiều yêu cầu đăng nhập từ IP này. Vui lòng thử lại sau 1 phút."
            },
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    parent = db.query(Parent).filter(Parent.username == username.strip()).first()

    # 2. Lockout Check
    now = datetime.now(timezone.utc)
    if parent and parent.locked_until:
        locked_until = parent.locked_until
        if locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=timezone.utc)
        if locked_until > now:
            remaining_secs = int((locked_until - now).total_seconds())
            remaining_mins = max(1, (remaining_secs + 59) // 60)
            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "parent": None,
                    "username": username,
                    "error": f"Tài khoản đã bị tạm khóa do nhập sai mật khẩu quá 5 lần. Vui lòng thử lại sau {remaining_mins} phút."
                },
                status_code=status.HTTP_423_LOCKED
            )
        else:
            parent.locked_until = None
            parent.failed_login_attempts = 0
            db.commit()

    # 3. Password Verification
    if not parent or not verify_password(password, parent.password_hash):
        if parent:
            parent.failed_login_attempts = (parent.failed_login_attempts or 0) + 1
            if parent.failed_login_attempts >= 5:
                parent.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
                db.commit()
                return templates.TemplateResponse(
                    request=request,
                    name="login.html",
                    context={
                        "parent": None,
                        "username": username,
                        "error": "Tài khoản đã bị tạm khóa 15 phút do nhập sai mật khẩu quá 5 lần liên tiếp."
                    },
                    status_code=status.HTTP_423_LOCKED
                )
            db.commit()

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "parent": None,
                "username": username,
                "error": "Tên đăng nhập hoặc mật khẩu không chính xác."
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # 4. Successful Login: Reset failed counters
    if parent.failed_login_attempts != 0 or parent.locked_until is not None:
        parent.failed_login_attempts = 0
        parent.locked_until = None
        db.commit()

    # 5. 15-minute access token
    access_token = create_access_token({
        "sub": f"parent:{parent.id}",
        "parent_id": parent.id,
        "username": parent.username,
        "role": "parent"
    })

    redirect = RedirectResponse(url="/devices", status_code=status.HTTP_302_FOUND)
    redirect.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=86400,  # 1 ngày liên tục (24 giờ = 86400 giây)
        samesite="lax"
    )
    return redirect


@router.get("/logout", summary="Đăng xuất tài khoản phụ huynh")
def logout(request: Request):
    """Clear session cookie, revoke token server-side, and redirect to login page."""
    token = request.cookies.get("access_token")
    if token:
        revoke_token(token)

    redirect = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax"
    )
    return redirect


@router.get("/devices", response_class=HTMLResponse, summary="Trang quản lý thiết bị phụ huynh")
def devices_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Render device management page with live device status and pairing code modal."""
    parent = get_current_parent_from_cookie(request, db)
    if not parent:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    devices = db.query(Device).filter(Device.parent_id == parent.id).order_by(Device.id.desc()).all()

    # Dynamic Online/Offline calculation:
    # A device is considered Online if it sent a heartbeat within the last 120 seconds (2 x 60s cycle)
    now = datetime.now(timezone.utc)
    ONLINE_TIMEOUT_SECONDS = 120

    has_status_changed = False
    for dev in devices:
        if dev.last_seen:
            last = dev.last_seen if dev.last_seen.tzinfo else dev.last_seen.replace(tzinfo=timezone.utc)
            is_active = (now - last).total_seconds() <= ONLINE_TIMEOUT_SECONDS
            new_status = "online" if is_active else "offline"
        else:
            new_status = "offline"

        if dev.status != new_status:
            dev.status = new_status
            has_status_changed = True

    if has_status_changed:
        db.commit()

    online_count = sum(1 for d in devices if d.status == "online")
    offline_count = len(devices) - online_count

    # Week 2: Load policies and recent audit logs for parent's devices
    policies_map = {dev.id: get_or_create_default_policy(db, dev.id) for dev in devices}
    dev_ids = [d.id for d in devices]
    audit_logs = (
        db.query(AuditLog)
        .filter(AuditLog.device_id.in_(dev_ids))
        .order_by(AuditLog.id.desc())
        .limit(20)
        .all()
        if dev_ids else []
    )

    # Week 3 (v0.3): Load usage summaries, weekly stats, filtering rules and child requests
    reports_map = {dev.id: get_device_report_summary(db, dev.id) for dev in devices}
    weekly_stats_map = {dev.id: get_weekly_usage_stats(db, dev.id) for dev in devices}
    domain_rules = get_active_domain_rules(db)
    category_summaries = get_domain_category_summaries(db)
    app_rules = get_active_app_rules(db)
    all_requests = [r for r in get_requests(db) if r.device_id in dev_ids] if dev_ids else []
    pending_requests = [r for r in all_requests if r.status == "pending"]

    return templates.TemplateResponse(
        request=request,
        name="devices.html",
        context={
            "parent": parent,
            "devices": devices,
            "policies_map": policies_map,
            "audit_logs": audit_logs,
            "online_count": online_count,
            "offline_count": offline_count,
            "reports_map": reports_map,
            "weekly_stats_map": weekly_stats_map,
            "domain_rules": domain_rules,
            "total_domain_rules": len(domain_rules),
            "category_summaries": category_summaries,
            "app_rules": app_rules,
            "all_requests": all_requests,
            "pending_requests": pending_requests,
            "DEFAULT_SCHEDULE_MATRIX": DEFAULT_SCHEDULE_MATRIX
        }
    )


@router.get("/download/agent", tags=["Download"])
@router.get("/download/OGK.zip", tags=["Download"])
def download_ogk_agent_zip():
    """Download the production OGK Agent installer package (OGK.zip)."""
    candidates = [
        os.path.join(PROJECT_ROOT, "server", "OGK.zip"),
        os.path.join(PROJECT_ROOT, "OGK.zip"),
    ]
    for zip_path in candidates:
        if os.path.isfile(zip_path):
            return FileResponse(
                path=zip_path,
                filename="OGK.zip",
                media_type="application/zip"
            )
    raise HTTPException(status_code=404, detail="File OGK.zip không tồn tại trên máy chủ.")



