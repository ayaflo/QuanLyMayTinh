"""Database seeder script for Open Guardian Kids (OGK).
Initializes default parent account `parent_admin` / `Admin@123456`.
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from server.database import engine, Base, SessionLocal
    from server.models import Parent
    from server.security import hash_password
except ImportError:
    from database import engine, Base, SessionLocal
    from models import Parent
    from security import hash_password



def seed_data(db=None):
    """Seed initial data into database.
    Ensures default admin accounts 'admin' and 'parent_admin' exist.
    """
    Base.metadata.create_all(bind=engine)

    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        # 1. Seed parent_admin
        existing_parent = db.query(Parent).filter(Parent.username == "parent_admin").first()
        if not existing_parent:
            hashed_pwd = hash_password("Admin@123456")
            admin_parent = Parent(
                username="parent_admin",
                password_hash=hashed_pwd
            )
            db.add(admin_parent)
            print(" [+] Khởi tạo tài khoản phụ huynh: 'parent_admin' / 'Admin@123456'")
        else:
            admin_parent = existing_parent

        # 2. Seed admin
        existing_admin = db.query(Parent).filter(Parent.username == "admin").first()
        if not existing_admin:
            hashed_pwd_admin = hash_password("Admin@123456")
            admin_user = Parent(
                username="admin",
                password_hash=hashed_pwd_admin
            )
            db.add(admin_user)
            print(" [+] Khởi tạo tài khoản phụ huynh: 'admin' / 'Admin@123456'")

        db.commit()
        return admin_parent
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    seed_data()
