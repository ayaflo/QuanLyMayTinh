"""Parent dashboard web view routes for Open Guardian Kids.
Renders Jinja2 HTML templates for login, device management, and pairing code modals.
"""

import os
from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request, Response, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


try:
    from ..database import get_db
    from ..models import Parent, Device, Policy, AuditLog
    from ..security import verify_password, create_access_token, decode_access_token
    from ..services.policy_service import get_or_create_default_policy
except (ImportError, ValueError):
    from server.database import get_db
    from server.models import Parent, Device, Policy, AuditLog
    from server.security import verify_password, create_access_token, decode_access_token
    from server.services.policy_service import get_or_create_default_policy

# Locate dashboard templates directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "dashboard", "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

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


@router.post("/login", response_class=HTMLResponse, summary="Xử lý đăng nhập từ Form HTML")
def handle_login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Process login form submission, set HTTP-only session cookie, redirect to /devices."""
    parent = db.query(Parent).filter(Parent.username == username.strip()).first()
    if not parent or not verify_password(password, parent.password_hash):
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

    # 15-minute access token
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
        max_age=900,
        samesite="lax"
    )
    return redirect


@router.get("/logout", summary="Đăng xuất tài khoản phụ huynh")
def logout():
    """Clear session cookie and redirect to login page."""
    redirect = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie("access_token")
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

    return templates.TemplateResponse(
        request=request,
        name="devices.html",
        context={
            "parent": parent,
            "devices": devices,
            "policies_map": policies_map,
            "audit_logs": audit_logs,
            "online_count": online_count,
            "offline_count": offline_count
        }
    )


