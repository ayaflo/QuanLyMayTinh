"""Tests for authentication logic and endpoints (T043).
Verifies Argon2id password hashing, token creation/verification, and login endpoint.
"""

from datetime import timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database import Base, get_db
from server.models import Parent
from server.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    reset_ip_rate_limits,
    clear_revoked_tokens
)
from server.main import app

# Setup isolated in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Create fresh tables for every test, reset rate limits/tokens, and tear down after."""
    reset_ip_rate_limits()
    clear_revoked_tokens()
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        # Seed test parent
        test_parent = Parent(
            username="test_parent",
            password_hash=hash_password("ValidPassword123")
        )
        db.add(test_parent)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        reset_ip_rate_limits()
        clear_revoked_tokens()


@pytest.fixture
def client(setup_test_db):
    """FastAPI test client with get_db dependency overridden."""
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_argon2_hash_and_verify():
    """Test Argon2id password hashing and comparison."""
    password = "SuperSecretPassword#2026"
    hashed = hash_password(password)

    # Hash should use Argon2id
    assert hashed.startswith("$argon2id$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword#2026", hashed) is False


def test_jwt_token_creation_and_tampering():
    """Test HMAC token creation, claims verification, and tampering rejection."""
    payload = {"sub": "parent:1", "username": "test_parent"}
    token = create_access_token(payload, expires_delta=timedelta(minutes=15))

    # Token structure header.payload.signature
    parts = token.split(".")
    assert len(parts) == 3

    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "parent:1"
    assert decoded["username"] == "test_parent"

    # Tampered signature should be rejected
    tampered_token = f"{parts[0]}.{parts[1]}.invalidsignature"
    assert decode_access_token(tampered_token) is None

    # Expired token should be rejected
    expired_token = create_access_token(payload, expires_delta=timedelta(seconds=-1))
    assert decode_access_token(expired_token) is None


def test_login_success(client):
    """Test POST /api/v1/auth/login with valid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test_parent", "password": "ValidPassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 900

    # Verify session cookie was set
    assert "access_token" in response.cookies


def test_login_wrong_password(client):
    """Test POST /api/v1/auth/login with incorrect password returns 401."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test_parent", "password": "IncorrectPassword"}
    )
    assert response.status_code == 401
    assert "Tên đăng nhập hoặc mật khẩu không chính xác" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test POST /api/v1/auth/login with unknown username returns 401."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "unknown_user", "password": "ValidPassword123"}
    )
    assert response.status_code == 401
    assert "Tên đăng nhập hoặc mật khẩu không chính xác" in response.json()["detail"]


def test_login_password_minimum_10_chars(client):
    """Test NIST SP 800-63B password length policy: rejects < 10 chars with 422."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test_parent", "password": "Short123"}  # 8 chars
    )
    assert response.status_code == 422


def test_account_lockout_after_5_failed_attempts(client):
    """Test brute-force lockout: 5 consecutive failed attempts lock account for 15 minutes."""
    # Attempts 1 to 4 should return 401
    for i in range(4):
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": "test_parent", "password": "WrongPassword#1"}
        )
        assert resp.status_code == 401, f"Attempt {i+1} should return 401"

    # Attempt 5 should trigger account lockout (HTTP 423)
    resp5 = client.post(
        "/api/v1/auth/login",
        json={"username": "test_parent", "password": "WrongPassword#1"}
    )
    assert resp5.status_code == 423
    assert "tạm khóa 15 phút" in resp5.json()["detail"]

    # Even with correct password, account must remain locked
    resp_locked = client.post(
        "/api/v1/auth/login",
        json={"username": "test_parent", "password": "ValidPassword123"}
    )
    assert resp_locked.status_code == 423
    assert "tạm khóa" in resp_locked.json()["detail"]


def test_successful_login_resets_failed_counter(client, setup_test_db):
    """Test that a valid login resets the failed login attempt counter."""
    # 2 failed attempts
    for _ in range(2):
        client.post(
            "/api/v1/auth/login",
            json={"username": "test_parent", "password": "WrongPassword#1"}
        )

    # 3rd attempt is successful
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "test_parent", "password": "ValidPassword123"}
    )
    assert resp.status_code == 200

    # Query DB to verify counter was reset to 0
    parent = setup_test_db.query(Parent).filter(Parent.username == "test_parent").first()
    assert parent.failed_login_attempts == 0
    assert parent.locked_until is None


def test_ip_rate_limiting(client):
    """Test sliding window IP rate limiting: 10 requests allowed, 11th triggers 429."""
    reset_ip_rate_limits()
    # 10 allowed requests
    for i in range(10):
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": "unknown_user", "password": "ValidPassword123"}
        )
        assert resp.status_code == 401, f"Request {i+1} should be evaluated"

    # 11th request triggers 429 Too Many Requests
    resp11 = client.post(
        "/api/v1/auth/login",
        json={"username": "unknown_user", "password": "ValidPassword123"}
    )
    assert resp11.status_code == 429
    assert "Quá nhiều yêu cầu đăng nhập" in resp11.json()["detail"]


def test_explicit_session_revocation_on_logout(client):
    """Test that logging out explicitly revokes the session token server-side."""
    # 1. Login to get token
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": "test_parent", "password": "ValidPassword123"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Verify token is valid
    assert decode_access_token(token) is not None

    # 2. Call logout API
    logout_resp = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert logout_resp.status_code == 200

    # 3. Verify token is now revoked and cannot be decoded
    assert decode_access_token(token) is None


def test_parent_self_registration_api(client, setup_test_db):
    """Test successful self-registration via /api/v1/auth/register."""
    reset_ip_rate_limits()
    resp = client.post(
        "/api/v1/auth/register",
        json={"username": "new_parent_user", "password": "SecurePassword2026!"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify parent is created in DB
    created = setup_test_db.query(Parent).filter(Parent.username == "new_parent_user").first()
    assert created is not None
    assert created.failed_login_attempts == 0

    # Verify can decode token
    payload = decode_access_token(data["access_token"])
    assert payload["username"] == "new_parent_user"
    assert payload["parent_id"] == created.id


def test_parent_registration_duplicate_username(client):
    """Test that registering an already existing username returns 400."""
    reset_ip_rate_limits()
    resp = client.post(
        "/api/v1/auth/register",
        json={"username": "test_parent", "password": "AnotherPassword123"}
    )
    assert resp.status_code == 400
    assert "đã được sử dụng" in resp.json()["detail"]


def test_parent_registration_weak_password(client):
    """Test NIST SP 800-63B password length enforcement (<10 characters)."""
    reset_ip_rate_limits()
    resp = client.post(
        "/api/v1/auth/register",
        json={"username": "short_pwd_user", "password": "short"}
    )
    assert resp.status_code == 422 or resp.status_code == 400


def test_dashboard_registration_flow(client, setup_test_db):
    """Test web dashboard GET /register and POST /register form submission."""
    reset_ip_rate_limits()
    # 1. GET /register returns HTML page
    get_resp = client.get("/register")
    assert get_resp.status_code == 200
    assert "Đăng Ký Tài Khoản Phụ Huynh" in get_resp.text

    # 2. POST /register with mismatching passwords fails
    fail_resp = client.post(
        "/register",
        data={
            "username": "form_parent",
            "password": "ValidPassword123",
            "confirm_password": "DifferentPassword123"
        }
    )
    assert fail_resp.status_code == 400
    assert "không khớp" in fail_resp.text

    # 3. POST /register with valid form data succeeds and redirects
    success_resp = client.post(
        "/register",
        data={
            "username": "form_parent",
            "password": "ValidPassword123",
            "confirm_password": "ValidPassword123"
        },
        follow_redirects=False
    )
    assert success_resp.status_code == 302
    assert success_resp.headers["location"] == "/devices"
    assert "access_token" in success_resp.cookies


def test_seed_data_creates_both_admin_and_parent_admin(setup_test_db):
    """Verify seed_data creates both 'admin' and 'parent_admin' accounts."""
    from server.seed import seed_data
    seed_data(setup_test_db)

    admin = setup_test_db.query(Parent).filter(Parent.username == "admin").first()
    assert admin is not None
    assert verify_password("Admin@123456", admin.password_hash)

    p_admin = setup_test_db.query(Parent).filter(Parent.username == "parent_admin").first()
    assert p_admin is not None
    assert verify_password("Admin@123456", p_admin.password_hash)

