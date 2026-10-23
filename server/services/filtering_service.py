"""Filtering management service for Open Guardian Kids (F2 & NT6).
Manages Domain filtering rules and Executable SHA-256 application control rules.
"""

from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone

try:
    from ..models import DomainRule, AppRule
    from ..schemas import DomainRuleCreate, AppRuleCreate, DomainCategorySummary, FilteringRulesSyncResponse
except (ImportError, ValueError):
    from server.models import DomainRule, AppRule
    from server.schemas import DomainRuleCreate, AppRuleCreate, DomainCategorySummary, FilteringRulesSyncResponse


def utc_now():
    return datetime.now(timezone.utc)


def get_active_domain_rules(db: Session) -> List[DomainRule]:
    """Retrieve all configured domain filtering rules."""
    return db.query(DomainRule).order_by(DomainRule.category, DomainRule.domain).all()


def get_active_app_rules(db: Session, device_id: Optional[int] = None) -> List[AppRule]:
    """Retrieve application rules applicable to a specific device or globally."""
    query = db.query(AppRule)
    if device_id is not None:
        query = query.filter((AppRule.device_id == device_id) | (AppRule.device_id.is_(None)))
    return query.order_by(AppRule.app_name).all()


def get_consolidated_filtering_rules(db: Session, device_id: Optional[int] = None) -> Dict[str, Any]:
    """Compile rules for Client Agent sync and offline local SQLite caching (F2 & NT6)."""
    domains = db.query(DomainRule).all()
    app_rules = get_active_app_rules(db, device_id=device_id)

    blocked_domains = []
    allowed_domains = []
    permanent_whitelist = []

    for d in domains:
        if d.is_permanent_whitelist:
            permanent_whitelist.append(d.domain)
            allowed_domains.append(d.domain)
        elif d.action == "block":
            blocked_domains.append(d.domain)
        else:
            allowed_domains.append(d.domain)

    app_blocklist = [
        {
            "name": r.app_name,
            "sha256": r.sha256_hash.lower(),
            "description": r.description or ""
        }
        for r in app_rules if r.action == "block"
    ]

    return {
        "version": 1,
        "blocked_domains": blocked_domains,
        "allowed_domains": allowed_domains,
        "permanent_whitelist": permanent_whitelist,
        "app_blocklist": app_blocklist
    }


def create_domain_rule(db: Session, rule_in: DomainRuleCreate) -> DomainRule:
    """Create or update a domain rule.
    Enforces NT6: Permanent whitelist domains can NEVER be blocked.
    """
    clean_domain = rule_in.domain.strip().lower()
    existing = db.query(DomainRule).filter(DomainRule.domain == clean_domain).first()

    if existing:
        if existing.is_permanent_whitelist and rule_in.action == "block":
            raise ValueError(f"Tên miền '{clean_domain}' nằm trong danh sách trắng vĩnh viễn (NT6), không thể chặn.")
        existing.category = rule_in.category
        existing.action = rule_in.action
        db.commit()
        db.refresh(existing)
        return existing

    if rule_in.is_permanent_whitelist and rule_in.action == "block":
        raise ValueError("Danh sách trắng vĩnh viễn (NT6) không thể mang hành động chặn.")

    new_rule = DomainRule(
        category=rule_in.category,
        domain=clean_domain,
        action=rule_in.action,
        is_permanent_whitelist=rule_in.is_permanent_whitelist,
        created_at=utc_now()
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule


def delete_domain_rule(db: Session, rule_id: int) -> bool:
    """Delete a domain rule by ID.
    Enforces NT6: Permanent whitelist entries cannot be deleted.
    """
    rule = db.query(DomainRule).filter(DomainRule.id == rule_id).first()
    if not rule:
        return False
    if rule.is_permanent_whitelist:
        raise ValueError("Không thể xóa tên miền thuộc danh sách trắng vĩnh viễn (NT6).")

    db.delete(rule)
    db.commit()
    return True


def create_app_rule(db: Session, rule_in: AppRuleCreate) -> AppRule:
    """Create a new executable SHA-256 control rule (F2)."""
    clean_hash = rule_in.sha256_hash.strip().lower()
    existing = db.query(AppRule).filter(
        AppRule.sha256_hash == clean_hash,
        AppRule.device_id == rule_in.device_id
    ).first()

    if existing:
        existing.app_name = rule_in.app_name
        existing.action = rule_in.action
        existing.description = rule_in.description
        db.commit()
        db.refresh(existing)
        return existing

    new_rule = AppRule(
        device_id=rule_in.device_id,
        app_name=rule_in.app_name,
        sha256_hash=clean_hash,
        action=rule_in.action,
        description=rule_in.description,
        created_at=utc_now()
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule


def delete_app_rule(db: Session, rule_id: int) -> bool:
    """Delete an app control rule by ID."""
    rule = db.query(AppRule).filter(AppRule.id == rule_id).first()
    if not rule:
        return False
    db.delete(rule)
    db.commit()
    return True


def get_domain_category_summaries(db: Session) -> List[DomainCategorySummary]:
    """Summarize counts of domains per category for Parent Dashboard."""
    categories = db.query(DomainRule.category).distinct().all()
    summaries = []
    for (cat,) in categories:
        total = db.query(DomainRule).filter(DomainRule.category == cat).count()
        blocked = db.query(DomainRule).filter(DomainRule.category == cat, DomainRule.action == "block").count()
        allowed = db.query(DomainRule).filter(DomainRule.category == cat, DomainRule.action == "allow").count()
        summaries.append(DomainCategorySummary(
            category=cat,
            total_domains=total,
            blocked_domains=blocked,
            allowed_domains=allowed
        ))
    return summaries
