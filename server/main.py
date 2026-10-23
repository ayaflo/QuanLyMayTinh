"""Open Guardian Kids (OGK) - Central Server.
FastAPI application entrypoint configuring CORS, database tables, and API routers.
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from server.database import engine, Base, SessionLocal
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
    from server.seed_domains import seed_domain_rules
except ImportError:
    from database import engine, Base, SessionLocal
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
    from seed_domains import seed_domain_rules



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events: create database tables and seed domain classification dataset on startup."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_domain_rules(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Open Guardian Kids (OGK) API",
    description="Hệ thống hỗ trợ phụ huynh quản lý và đồng hành việc sử dụng máy tính của trẻ em.",
    version="0.3.0",
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
app.include_router(heartbeat_router, prefix="/api/v1/heartbeat", tags=["Heartbeat"])
app.include_router(policy_router, prefix="/api/v1/policy", tags=["Policy & Time Governance"])
app.include_router(commands_router, prefix="/api/v1/devices", tags=["Emergency Commands"])
app.include_router(ws_router, prefix="/ws", tags=["WebSocket Real-Time"])
app.include_router(audit_router, prefix="/api/v1/audit-logs", tags=["Audit Logs"])
app.include_router(filtering_router)  # includes prefix /api/v1/filtering
app.include_router(events_router)     # includes prefix /api/v1/events
app.include_router(reports_router)    # includes prefix /api/v1/reports
app.include_router(requests_router)   # includes prefix /api/v1/requests

# Register Dashboard View Router (T030)
app.include_router(dashboard_router, tags=["Dashboard"])


@app.get("/", tags=["General"])
def root():
    """Redirect to dashboard devices page."""
    return RedirectResponse(url="/devices")



@app.get("/api/v1/health", tags=["General"])
def health():
    """Service health status check."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)
