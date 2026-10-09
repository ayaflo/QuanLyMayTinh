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
    decode_access_token
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
    """Create fresh tables for every test and tear down after."""
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
