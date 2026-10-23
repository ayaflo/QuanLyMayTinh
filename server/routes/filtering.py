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
        create_app_rule,
        delete_app_rule,
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
        create_app_rule,
        delete_app_rule,
        get_domain_category_summaries
    )

router = APIRouter(prefix="/api/v1/filtering", tags=["Filtering"])


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
def add_domain_rule(
    rule_in: DomainRuleCreate,
    db: Session = Depends(get_db)
) -> DomainRuleResponse:
    """Create or update domain rule. Enforces NT6 permanent whitelist protection."""
    try:
        rule = create_domain_rule(db, rule_in)
        return DomainRuleResponse.model_validate(rule)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/domain-rules/{rule_id}", status_code=status.HTTP_200_OK, summary="Xóa quy tắc lọc tên miền")
def remove_domain_rule(rule_id: int, db: Session = Depends(get_db)):
    """Delete a domain rule. Permanent whitelist items are protected from deletion (NT6)."""
    try:
        success = delete_domain_rule(db, rule_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy quy tắc tên miền.")
        return {"status": "success", "message": f"Đã xóa quy tắc #{rule_id}"}
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
def add_app_rule(
    rule_in: AppRuleCreate,
    db: Session = Depends(get_db)
) -> AppRuleResponse:
    """Create or update executable SHA-256 application control rule."""
    rule = create_app_rule(db, rule_in)
    return AppRuleResponse.model_validate(rule)


@router.delete("/app-rules/{rule_id}", status_code=status.HTTP_200_OK, summary="Xóa quy tắc ứng dụng")
def remove_app_rule(rule_id: int, db: Session = Depends(get_db)):
    """Delete an application control rule."""
    success = delete_app_rule(db, rule_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy quy tắc ứng dụng.")
    return {"status": "success", "message": f"Đã xóa quy tắc #{rule_id}"}


@router.get("/categories", response_model=List[DomainCategorySummary], summary="Thống kê số lượng tên miền theo nhóm")
def list_category_summaries(db: Session = Depends(get_db)) -> List[DomainCategorySummary]:
    """Return counts of total, blocked, and allowed domains per category."""
    return get_domain_category_summaries(db)
