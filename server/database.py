"""Database configuration and session management for Open Guardian Kids (OGK).
Uses SQLite with Write-Ahead Logging (WAL) for high concurrency and performance.
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ogk.db")

# Fix Render PostgreSQL URL: Render provides 'postgres://' which SQLAlchemy 1.4/2.0 requires as 'postgresql://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

is_sqlite = DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}
engine_kwargs = {"connect_args": connect_args}

if not is_sqlite:
    # Enable connection pooling and pre-ping checks for cloud PostgreSQL (Render, Neon, Supabase)
    engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_recycle": 300,
    })

engine = create_engine(DATABASE_URL, **engine_kwargs)

if is_sqlite:
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
    if eng.dialect.name == "sqlite":
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

