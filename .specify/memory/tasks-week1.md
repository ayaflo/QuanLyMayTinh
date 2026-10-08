# Spec Kit Tasks: Week 1 (Version 0.1) - Open Guardian Kids (OGK)

## Phase 1: Setup & Environment
- [ ] T001 Create server dependency declaration file in server/requirements.txt
- [ ] T002 Create agent dependency declaration file in agent/requirements.txt
- [ ] T003 Create environment configuration template in .env.example
- [ ] T004 Create environment setup script in scripts/setup_env.ps1

## Phase 2: Server Database Models & Schemas
- [ ] T005 Create database connection and SQLite WAL engine in server/database.py
- [ ] T006 Create Parent model in server/models.py
- [ ] T007 Add Device model in server/models.py
- [ ] T008 Add PairingCode model in server/models.py
- [ ] T009 Add HeartbeatLog model in server/models.py
- [ ] T010 Create authentication Pydantic schemas in server/schemas.py
- [ ] T011 Add enrollment Pydantic schemas in server/schemas.py
- [ ] T012 Add heartbeat Pydantic schemas in server/schemas.py

## Phase 3: Core Security & Enrollment Services
- [ ] T013 Implement hash_password function using Argon2id in server/security.py
- [ ] T014 Implement verify_password function in server/security.py
- [ ] T015 Implement create_access_token function with HMAC in server/security.py
- [ ] T016 Implement generate_pairing_code function in server/services/enrollment_service.py
- [ ] T017 Implement verify_and_claim_code function in server/services/enrollment_service.py

## Phase 4: Server Routes & Endpoints
- [ ] T018 Initialize FastAPI app and CORS middleware in server/main.py
- [ ] T019 Implement POST /api/v1/auth/login endpoint in server/routes/auth.py
- [ ] T020 Implement POST /api/v1/enroll/create-code endpoint in server/routes/enroll.py
- [ ] T021 Implement POST /api/v1/enroll/claim endpoint in server/routes/enroll.py
- [ ] T022 Implement POST /api/v1/heartbeat endpoint in server/routes/heartbeat.py
- [ ] T023 Register auth, enroll, and heartbeat routers in server/main.py
- [ ] T024 Create initial parent seed script in server/seed.py

## Phase 5: Parent Dashboard Web UI
- [ ] T025 Create base HTML layout in dashboard/templates/base.html
- [ ] T026 Create login page template in dashboard/templates/login.html
- [ ] T027 Create device management template in dashboard/templates/devices.html
- [ ] T028 Add pairing code generation modal to dashboard/templates/devices.html
- [ ] T029 Create responsive stylesheet in dashboard/static/style.css
- [ ] T030 Create dashboard view routes in server/routes/dashboard.py

## Phase 6: Client Agent
- [ ] T031 Create agent configuration file in agent/config.py
- [ ] T032 Implement get_device_fingerprint function in agent/fingerprint.py
- [ ] T033 Implement save_credentials function in agent/storage.py
- [ ] T034 Implement load_credentials function in agent/storage.py
- [ ] T035 Implement pair_with_server function in agent/enrollment_client.py
- [ ] T036 Implement send_heartbeat function in agent/heartbeat_client.py
- [ ] T037 Implement run_heartbeat_loop function in agent/heartbeat_client.py
- [ ] T038 Implement init_tray_icon function using pystray in agent/tray.py
- [ ] T039 Add startup notification popup in agent/tray.py
- [ ] T040 Implement agent entry point in agent/main.py

## Phase 7: Verification & Documentation
- [ ] T041 Create architecture documentation in docs/KienTrucHeThong.md
- [ ] T042 Create draft privacy table in docs/PRIVACY.md
- [ ] T043 Create authentication unit tests in tests/test_auth.py
- [ ] T044 Create enrollment unit tests in tests/test_enrollment.py
- [ ] T045 Create heartbeat unit tests in tests/test_heartbeat.py
- [ ] T046 Create end-to-end verification checklist in docs/VERIFY_WEEK1.md
