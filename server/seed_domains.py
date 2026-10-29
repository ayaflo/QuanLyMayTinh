"""Predefined seed dataset of categorized domains and application rules for Open Guardian Kids (F2).
Categories:
1. Giáo dục (Education) - Permanent whitelist NT6 protected
2. Mạng xã hội (Social Media)
3. Giải trí (Entertainment)
4. Game (Gaming)
5. Không phù hợp (Unsuitable / Inappropriate)
6. DoH (DNS over HTTPS resolvers)
"""

import sys
from sqlalchemy.orm import Session
from datetime import datetime, timezone

try:
    from .database import SessionLocal, engine, Base
    from .models import DomainRule, AppRule
except (ImportError, ValueError):
    from server.database import SessionLocal, engine, Base
    from server.models import DomainRule, AppRule


def utc_now():
    return datetime.now(timezone.utc)


# Clean, concise list of 10 representative domains across 6 categories
SEED_DOMAINS_DATA = [
    # 1. Giáo dục (NT6 Whitelist protected: Tổng đài 111 & Bộ GD&ĐT)
    {"category": "Giáo dục", "domain": "tongdai111.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "moet.gov.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "khanacademy.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "wikipedia.org", "action": "allow", "is_permanent_whitelist": False},

    # 2. Mạng xã hội (Default: block)
    {"category": "Mạng xã hội", "domain": "facebook.com", "action": "block", "is_permanent_whitelist": False},

    # 3. Giải trí (Default: allow)
    {"category": "Giải trí", "domain": "youtube.com", "action": "allow", "is_permanent_whitelist": False},

    # 4. Game (Default: block)
    {"category": "Game", "domain": "roblox.com", "action": "block", "is_permanent_whitelist": False},

    # 5. Không phù hợp (Default: block)
    {"category": "Không phù hợp", "domain": "gambling-test.example.com", "action": "block", "is_permanent_whitelist": False},

    # 6. DoH (Default: block)
    {"category": "DoH", "domain": "cloudflare-dns.com", "action": "block", "is_permanent_whitelist": False},
]


def seed_domain_rules(db: Session) -> int:
    """Seed the predefined categorized domain rules into the database.
    Returns the count of new rules inserted.
    """
    inserted = 0
    for item in SEED_DOMAINS_DATA:
        existing = db.query(DomainRule).filter(DomainRule.domain == item["domain"]).first()
        if not existing:
            rule = DomainRule(
                category=item["category"],
                domain=item["domain"],
                action=item["action"],
                is_permanent_whitelist=item.get("is_permanent_whitelist", False),
                created_at=utc_now()
            )
            db.add(rule)
            inserted += 1
    if inserted > 0:
        db.commit()
    return inserted


def reset_domain_rules_to_seed(db: Session) -> int:
    """Clear domain rules and reset to the clean 10-domain seed list."""
    db.query(DomainRule).delete()
    db.commit()
    return seed_domain_rules(db)


SEED_APP_RULES_DATA = [
    {
        "app_name": "notepad.exe",
        "sha256_hash": "468ffe129c395abf6b21a09efdf261910a95fb98aa982ead73caa7b2b684577e",
        "action": "block",
        "description": "Ứng dụng Notepad (Dùng thử nghiệm chặn ứng dụng)"
    },
    {
        "app_name": "Cloudflare WARP.exe",
        "sha256_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
        "action": "block",
        "description": "Ứng dụng VPN Cloudflare WARP - Ngăn chặn vượt rào DNS"
    },
    {
        "app_name": "warp-svc.exe",
        "sha256_hash": "5a8dd3ad0756a93ded72b823b19dd877a602b783a0c4415e30715e6138426172",
        "action": "block",
        "description": "Dịch vụ VPN ngầm Cloudflare WARP"
    },
    {
        "app_name": "ProtonVPN.exe",
        "sha256_hash": "4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce",
        "action": "block",
        "description": "Ứng dụng ProtonVPN - Ngăn chặn đường hầm mã hóa vượt rào"
    },
    {
        "app_name": "ProtonVPN.Launcher.exe",
        "sha256_hash": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
        "action": "block",
        "description": "Trình khởi chạy ứng dụng ProtonVPN"
    },
    {
        "app_name": "psiphon3.exe",
        "sha256_hash": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
        "action": "block",
        "description": "Công cụ vượt tường lửa Psiphon 3"
    },
    {
        "app_name": "u.exe",
        "sha256_hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
        "action": "block",
        "description": "Công cụ proxy UltraSurf (u.exe)"
    },
    {
        "app_name": "ultrasurf.exe",
        "sha256_hash": "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb",
        "action": "block",
        "description": "Ứng dụng proxy vượt rào UltraSurf"
    },
    {
        "app_name": "tor.exe",
        "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "action": "block",
        "description": "Dịch vụ mạng ẩn danh Tor (tor.exe) - Ngăn chặn vượt rào"
    },
    {
        "app_name": "tor-browser.exe",
        "sha256_hash": "3a01044298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b801",
        "action": "block",
        "description": "Trình duyệt Tor Browser - Ngăn chặn vượt rào mạng ẩn danh"
    },
    {
        "app_name": "opera.exe",
        "sha256_hash": "3a02044298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b802",
        "action": "block",
        "description": "Trình duyệt Opera (Tích hợp VPN miễn phí vượt rào)"
    },
    {
        "app_name": "opera_gx.exe",
        "sha256_hash": "3a03044298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b803",
        "action": "block",
        "description": "Trình duyệt Opera GX (Tích hợp VPN vượt rào)"
    },
    {
        "app_name": "epic.exe",
        "sha256_hash": "3a04044298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b804",
        "action": "block",
        "description": "Trình duyệt Epic Privacy (Tích hợp proxy VPN vượt rào)"
    },
    {
        "app_name": "ur.exe",
        "sha256_hash": "3a05044298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b805",
        "action": "block",
        "description": "Trình duyệt UR Browser (Tích hợp VPN vượt rào)"
    }
]


def seed_app_rules(db: Session) -> int:
    """Seed predefined VPN and demo application rules into the database (T4_019).
    Returns the count of new app rules inserted.
    """
    inserted = 0
    for item in SEED_APP_RULES_DATA:
        existing = db.query(AppRule).filter(
            (AppRule.app_name == item["app_name"]) | (AppRule.sha256_hash == item["sha256_hash"])
        ).first()
        if not existing:
            rule = AppRule(
                device_id=None,  # Global rule applying to all devices
                app_name=item["app_name"],
                sha256_hash=item["sha256_hash"],
                action=item["action"],
                description=item["description"],
                created_at=utc_now()
            )
            db.add(rule)
            inserted += 1
    if inserted > 0:
        db.commit()
    return inserted


if __name__ == "__main__":
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        count_domains = reset_domain_rules_to_seed(db)
        count_apps = seed_app_rules(db)
        total_domains = db.query(DomainRule).count()
        total_apps = db.query(AppRule).count()
        print(f"[*] Reset and seeded {count_domains} clean domains (Total: {total_domains}).")
        print(f"[*] Seeded {count_apps} new app rules (Total: {total_apps}).")
    finally:
        db.close()
