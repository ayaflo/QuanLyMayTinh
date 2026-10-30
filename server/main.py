"""Open Guardian Kids (OGK) - Central Server.
FastAPI application entrypoint configuring CORS, database tables, and API routers.
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from server.database import engine, Base, SessionLocal, run_migrations
    from server.routes.auth import router as auth_router
    from server.routes.enroll import router as enroll_router
    from server.routes.heartbeat import router as heartbeat_router
    from server.routes.dashboard import router as dashboard_router
    from server.routes.policy import router as policy_router
    from server.routes.commands import router as commands_router
    from server.routes.ws import router as ws_router
    from server.routes.audit import router as audit_router
    from server.routes.filtering import router as filtering_router
    from server.routes.events import router as events_router
    from server.routes.reports import router as reports_router
    from server.routes.requests import router as requests_router
    from server.routes.retention import router as retention_router
    from server.seed_domains import seed_domain_rules, seed_app_rules
    from server.seed import seed_data
    from server.services.retention_service import purge_expired_activity_data
except ModuleNotFoundError as e:
    if e.name == "server":
        from database import engine, Base, SessionLocal, run_migrations
        from routes.auth import router as auth_router
        from routes.enroll import router as enroll_router
        from routes.heartbeat import router as heartbeat_router
        from routes.dashboard import router as dashboard_router
        from routes.policy import router as policy_router
        from routes.commands import router as commands_router
        from routes.ws import router as ws_router
        from routes.audit import router as audit_router
        from routes.filtering import router as filtering_router
        from routes.events import router as events_router
        from routes.reports import router as reports_router
        from routes.requests import router as requests_router
        from routes.retention import router as retention_router
        from seed_domains import seed_domain_rules, seed_app_rules
        from seed import seed_data
        from services.retention_service import purge_expired_activity_data
    else:
        raise



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events: create tables, run migrations, seed data, and start 24h retention cleanup."""
    import asyncio
    Base.metadata.create_all(bind=engine)
    run_migrations(engine)
    db = SessionLocal()
    try:
        seed_data(db)
        seed_domain_rules(db)
        seed_app_rules(db)
        # Perform an initial startup retention sweep
        purge_expired_activity_data(db, days=90)
    finally:
        db.close()

    async def periodic_retention_task():
        while True:
            await asyncio.sleep(86400)  # 24 hours
            try:
                task_db = SessionLocal()
                try:
                    purge_expired_activity_data(task_db, days=90)
                finally:
                    task_db.close()
            except Exception:
                pass

    cleanup_task = asyncio.create_task(periodic_retention_task())
    try:
        yield
    finally:
        cleanup_task.cancel()


app = FastAPI(
    title="Open Guardian Kids (OGK) API",
    description="Hệ thống hỗ trợ phụ huynh quản lý và đồng hành việc sử dụng máy tính của trẻ em.",
    version="0.4.0",
    lifespan=lifespan
)

# Mount Static Files for Web Dashboard UI
STATIC_DIR = os.path.join(PROJECT_ROOT, "dashboard", "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers (Week 1, Week 2 & Week 3)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(enroll_router, prefix="/api/v1/enroll", tags=["Enrollment"])
app.include_router(enroll_router, prefix="/api/v1/enrollment", tags=["Enrollment Alias"])
app.include_router(heartbeat_router, prefix="/api/v1/heartbeat", tags=["Heartbeat"])
app.include_router(policy_router, prefix="/api/v1/policy", tags=["Policy & Time Governance"])
app.include_router(policy_router, prefix="/api/v1/policies", tags=["Policy Alias"])
app.include_router(commands_router, prefix="/api/v1/devices", tags=["Emergency Commands"])
app.include_router(ws_router, prefix="/ws", tags=["WebSocket Real-Time"])
app.include_router(audit_router, prefix="/api/v1/audit-logs", tags=["Audit Logs"])
app.include_router(filtering_router)  # includes prefix /api/v1/filtering
app.include_router(events_router)     # includes prefix /api/v1/events
app.include_router(reports_router)    # includes prefix /api/v1/reports
app.include_router(requests_router)   # includes prefix /api/v1/requests
app.include_router(retention_router)  # includes prefix /api/v1/devices

# Register Dashboard View Router (T030)
app.include_router(dashboard_router, tags=["Dashboard"])


@app.get("/", tags=["General"])
def root():
    """Redirect to dashboard devices page."""
    return RedirectResponse(url="/devices")


@app.get("/download/agent", tags=["General"])
@app.get("/download/OGK.zip", tags=["General"])
def download_agent():
    """Download the OGK Agent installer package (OGK.zip)."""
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


@app.get("/api/v1/health", tags=["General"])
def health():
    """Service health status check."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)
