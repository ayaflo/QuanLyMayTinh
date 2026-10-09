# Spec Kit Tasks: Week 1 (Version 0.1) - Open Guardian Kids (OGK)

## Phase 1: Setup & Environment
- [x] T001 Create server dependency declaration file in server/requirements.txt
- [x] T002 Create agent dependency declaration file in agent/requirements.txt
- [x] T003 Create environment configuration template in .env.example
- [x] T004 Create environment setup script in scripts/setup_env.ps1

## Phase 2: Server Database Models & Schemas
- [x] T005 Create database connection and SQLite WAL engine in server/database.py
- [x] T006 Create Parent model in server/models.py
- [x] T007 Add Device model in server/models.py
- [x] T008 Add PairingCode model in server/models.py
- [x] T009 Add HeartbeatLog model in server/models.py
- [x] T010 Create authentication Pydantic schemas in server/schemas.py
- [x] T011 Add enrollment Pydantic schemas in server/schemas.py
- [x] T012 Add heartbeat Pydantic schemas in server/schemas.py

## Phase 3: Core Security & Enrollment Services
- [x] T013 Implement hash_password function using Argon2id in server/security.py
- [x] T014 Implement verify_password function in server/security.py
- [x] T015 Implement create_access_token function with HMAC in server/security.py
- [x] T016 Implement generate_pairing_code function in server/services/enrollment_service.py
- [x] T017 Implement verify_and_claim_code function in server/services/enrollment_service.py

## Phase 4: Server Routes & Endpoints
- [x] T018 Initialize FastAPI app and CORS middleware in server/main.py
- [x] T019 Implement POST /api/v1/auth/login endpoint in server/routes/auth.py
- [x] T020 Implement POST /api/v1/enroll/create-code endpoint in server/routes/enroll.py
- [x] T021 Implement POST /api/v1/enroll/claim endpoint in server/routes/enroll.py
- [x] T022 Implement POST /api/v1/heartbeat endpoint in server/routes/heartbeat.py
- [x] T023 Register auth, enroll, and heartbeat routers in server/main.py
- [x] T024 Create initial parent seed script in server/seed.py


## Phase 5: Parent Dashboard Web UI
- [x] T025 Create base HTML layout in dashboard/templates/base.html
- [x] T026 Create login page template in dashboard/templates/login.html
- [x] T027 Create device management template in dashboard/templates/devices.html
- [x] T028 Add pairing code generation modal to dashboard/templates/devices.html
- [x] T029 Create responsive stylesheet in dashboard/static/style.css
- [x] T030 Create dashboard view routes in server/routes/dashboard.py


## Phase 6: Client Agent
- [x] T031 Create agent configuration file in agent/config.py
- [x] T032 Implement get_device_fingerprint function in agent/fingerprint.py
- [x] T033 Implement save_credentials function in agent/storage.py
- [x] T034 Implement load_credentials function in agent/storage.py
- [x] T035 Implement pair_with_server function in agent/enrollment_client.py
- [x] T036 Implement send_heartbeat function in agent/heartbeat_client.py
- [x] T037 Implement run_heartbeat_loop function in agent/heartbeat_client.py
- [x] T038 Implement init_tray_icon function using pystray in agent/tray.py
- [x] T039 Add startup notification popup in agent/tray.py
- [x] T040 Implement agent entry point in agent/main.py


## Phase 7: Verification & Documentation
- [x] T041 Create architecture documentation in docs/KienTrucHeThong.md
- [x] T042 Create draft privacy table in docs/PRIVACY.md
- [x] T043 Create authentication unit tests in tests/test_auth.py
- [x] T044 Create enrollment unit tests in tests/test_enrollment.py
- [x] T045 Create heartbeat unit tests in tests/test_heartbeat.py
- [x] T046 Create end-to-end verification checklist in docs/VERIFY_WEEK1.md
