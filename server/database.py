"""Database configuration and session management for Open Guardian Kids (OGK).
Uses SQLite with Write-Ahead Logging (WAL) for high concurrency and performance.
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ogk.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def run_migrations(target_engine=None):
    """Run lightweight schema migrations for SQLite without requiring Alembic."""
    eng = target_engine or engine
    with eng.connect() as conn:
        try:
            result = conn.exec_driver_sql("PRAGMA table_info(parents)")
            columns = [row[1] for row in result.fetchall()]
            if columns:
                if "failed_login_attempts" not in columns:
                    conn.exec_driver_sql("ALTER TABLE parents ADD COLUMN failed_login_attempts INTEGER DEFAULT 0 NOT NULL")
                if "locked_until" not in columns:
                    conn.exec_driver_sql("ALTER TABLE parents ADD COLUMN locked_until DATETIME")
            conn.commit()
        except Exception:
            pass


def get_db():
    """Dependency provider yielding a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

