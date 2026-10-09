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



def seed_data():
    """Seed initial data into database."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_parent = db.query(Parent).filter(Parent.username == "parent_admin").first()
        if existing_parent:
            print(" [i] Tài khoản phụ huynh 'parent_admin' đã tồn tại trong CSDL.")
            return existing_parent

        hashed_pwd = hash_password("Admin@123456")
        admin = Parent(
            username="parent_admin",
            password_hash=hashed_pwd
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(" [+] Khởi tạo thành công tài khoản phụ huynh mẫu:")
        print("     Username: parent_admin")
        print("     Password: Admin@123456")
        return admin
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
