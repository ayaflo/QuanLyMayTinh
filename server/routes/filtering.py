"""Filtering API routes for Open Guardian Kids (F2 & NT6).
Exposes endpoints for domain filtering and executable SHA-256 application control.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..schemas import (
        DomainRuleCreate,
        DomainRuleResponse,
        AppRuleCreate,
        AppRuleResponse,
        DomainCategorySummary,
        FilteringRulesSyncResponse
    )
    from ..services.filtering_service import (
        get_active_domain_rules,
        get_active_app_rules,
        get_consolidated_filtering_rules,
        create_domain_rule,
        delete_domain_rule,
        toggle_domain_rule,
        create_app_rule,
        delete_app_rule,
        toggle_app_rule,
        get_domain_category_summaries
    )
except (ImportError, ValueError):
    from server.database import get_db
    from server.schemas import (
        DomainRuleCreate,
        DomainRuleResponse,
        AppRuleCreate,
        AppRuleResponse,
        DomainCategorySummary,
        FilteringRulesSyncResponse
    )
    from server.services.filtering_service import (
        get_active_domain_rules,
        get_active_app_rules,
        get_consolidated_filtering_rules,
        create_domain_rule,
        delete_domain_rule,
        toggle_domain_rule,
        create_app_rule,
        delete_app_rule,
        toggle_app_rule,
        get_domain_category_summaries
    )
try:
    from ..services.connection_manager import ws_manager
except (ImportError, ValueError):
    from server.services.connection_manager import ws_manager

router = APIRouter(prefix="/api/v1/filtering", tags=["Filtering"])


async def _notify_devices_rules_updated():
    """Notify all connected devices in real-time via WebSocket to re-sync rules."""
    for dev_id in list(ws_manager.active_connections.keys()):
        try:
            await ws_manager.send_command(dev_id, {"action": "policy_updated"})
        except Exception:
            pass


@router.get("/rules", response_model=FilteringRulesSyncResponse, summary="Đồng bộ toàn bộ quy tắc lọc cho Agent hoặc Dashboard")
def get_filtering_rules(
    device_id: Optional[int] = Query(None, description="ID thiết bị (tùy chọn)"),
    db: Session = Depends(get_db)
) -> FilteringRulesSyncResponse:
    """Return consolidated domain blocklist, allowlist, permanent whitelist, and app SHA-256 blocklist."""
    data = get_consolidated_filtering_rules(db, device_id=device_id)
    return FilteringRulesSyncResponse(**data)


@router.get("/domain-rules", response_model=List[DomainRuleResponse], summary="Lấy danh sách tất cả quy tắc tên miền")
def list_domain_rules(db: Session = Depends(get_db)) -> List[DomainRuleResponse]:
    """Retrieve all domain filtering rules."""
    return get_active_domain_rules(db)


@router.post("/domain-rules", response_model=DomainRuleResponse, status_code=status.HTTP_201_CREATED, summary="Thêm hoặc cập nhật quy tắc lọc tên miền")
async def add_domain_rule(
    rule_in: DomainRuleCreate,
    db: Session = Depends(get_db)
) -> DomainRuleResponse:
    """Create or update domain rule. Enforces NT6 permanent whitelist protection."""
    try:
        rule = create_domain_rule(db, rule_in)
        await _notify_devices_rules_updated()
        return DomainRuleResponse.model_validate(rule)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/domain-rules/{rule_id}", status_code=status.HTTP_200_OK, summary="Xóa quy tắc lọc tên miền")
async def remove_domain_rule(rule_id: int, force: bool = Query(False), db: Session = Depends(get_db)):
    """Delete a domain rule. Permanent whitelist items are protected from deletion unless force=True."""
    try:
        success = delete_domain_rule(db, rule_id, force=force)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy quy tắc tên miền.")
        await _notify_devices_rules_updated()
        return {"status": "success", "message": f"Đã xóa quy tắc #{rule_id}"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/domain-rules/{rule_id}/toggle", response_model=DomainRuleResponse, summary="Đảo trạng thái Chặn / Mở khóa tên miền")
async def toggle_domain_rule_action(rule_id: int, db: Session = Depends(get_db)) -> DomainRuleResponse:
    """Toggle a domain rule action between 'block' and 'allow'."""
    try:
        rule = toggle_domain_rule(db, rule_id)
        if not rule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy quy tắc tên miền.")
        await _notify_devices_rules_updated()
        return DomainRuleResponse.model_validate(rule)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/app-rules", response_model=List[AppRuleResponse], summary="Lấy danh sách quy tắc kiểm soát ứng dụng theo SHA-256")
def list_app_rules(
    device_id: Optional[int] = Query(None, description="Lọc theo thiết bị"),
    db: Session = Depends(get_db)
) -> List[AppRuleResponse]:
    """Retrieve app rules filtered by device ID or global."""
    return get_active_app_rules(db, device_id=device_id)


@router.post("/app-rules", response_model=AppRuleResponse, status_code=status.HTTP_201_CREATED, summary="Thêm quy tắc chặn ứng dụng theo SHA-256")
async def add_app_rule(
    rule_in: AppRuleCreate,
    db: Session = Depends(get_db)
) -> AppRuleResponse:
    """Create or update executable SHA-256 application control rule."""
    rule = create_app_rule(db, rule_in)
    await _notify_devices_rules_updated()
    return AppRuleResponse.model_validate(rule)


@router.post("/app-rules/{rule_id}/toggle", response_model=AppRuleResponse, summary="Đảo trạng thái Chặn / Mở khóa ứng dụng")
async def toggle_app_rule_action(rule_id: int, db: Session = Depends(get_db)) -> AppRuleResponse:
    """Toggle an application control rule between 'block' and 'allow'."""
    rule = toggle_app_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy quy tắc ứng dụng.")
    await _notify_devices_rules_updated()
    return AppRuleResponse.model_validate(rule)


@router.delete("/app-rules/{rule_id}", status_code=status.HTTP_200_OK, summary="Xóa quy tắc ứng dụng")
async def remove_app_rule(rule_id: int, db: Session = Depends(get_db)):
    """Delete an application control rule."""
    success = delete_app_rule(db, rule_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy quy tắc ứng dụng.")
    await _notify_devices_rules_updated()
    return {"status": "success", "message": f"Đã xóa quy tắc #{rule_id}"}


@router.get("/categories", response_model=List[DomainCategorySummary], summary="Thống kê số lượng tên miền theo nhóm")
def list_category_summaries(db: Session = Depends(get_db)) -> List[DomainCategorySummary]:
    """Return counts of total, blocked, and allowed domains per category."""
    return get_domain_category_summaries(db)
