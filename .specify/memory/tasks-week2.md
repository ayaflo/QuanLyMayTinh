# Spec Kit Tasks: Week 2 (Version 0.2) - Open Guardian Kids (OGK)
<!-- Time Governance & Policy Synchronization (F1 & Lõi F4) -->

## Phase 1: Server Database Models & Schemas
- [x] T2_001 Add Policy model in server/models.py
- [x] T2_002 Add AuditLog model in server/models.py
- [x] T2_003 Add DeviceCommand model in server/models.py
- [x] T2_004 Add policy Pydantic schemas in server/schemas.py
- [x] T2_005 Add audit log Pydantic schemas in server/schemas.py
- [x] T2_006 Add emergency command Pydantic schemas in server/schemas.py

## Phase 2: Core Policy, HMAC & WebSocket Services
- [x] T2_007 Implement calculate_policy_hmac and verify_policy_hmac in server/security.py
- [x] T2_008 Implement ConnectionManager for WebSockets in server/services/connection_manager.py
- [x] T2_009 Implement get_or_create_default_policy in server/services/policy_service.py
- [x] T2_010 Implement update_policy_and_log_audit in server/services/policy_service.py
- [x] T2_011 Implement dispatch_command in server/services/command_service.py

## Phase 3: Server Routes & WebSocket Endpoints
- [x] T2_012 Implement GET /api/v1/policy endpoint in server/routes/policy.py
- [x] T2_013 Implement POST /api/v1/policy endpoint in server/routes/policy.py
- [x] T2_014 Implement POST /api/v1/devices/{device_id}/command endpoint in server/routes/commands.py
- [x] T2_015 Implement WebSocket /ws/device/{device_id} endpoint in server/routes/ws.py
- [x] T2_016 Implement GET /api/v1/audit-logs endpoint in server/routes/audit.py
- [x] T2_017 Update POST /api/v1/heartbeat endpoint to return dynamic policy version in server/routes/heartbeat.py
- [x] T2_018 Register policy, commands, ws, and audit routers in server/main.py

## Phase 4: Parent Dashboard Time & Policy UI
- [x] T2_019 Add styling for schedule matrix and emergency controls in dashboard/static/style.css
- [x] T2_020 Add quota configuration modal in dashboard/templates/devices.html
- [x] T2_021 Add 7x48 weekly schedule grid component in dashboard/templates/devices.html
- [x] T2_022 Add emergency command action buttons (lock, unlock, +15m) in dashboard/templates/devices.html
- [x] T2_023 Add audit log history table in dashboard/templates/devices.html
- [x] T2_024 Update dashboard view route with policy and audit log data in server/routes/dashboard.py

## Phase 5: Client Agent Time Tracker & Anti-Time Drift
- [x] T2_025 Add policy cache and time usage tables in agent/storage.py
- [x] T2_026 Implement idle detection using GetLastInputInfo in agent/idle_detector.py
- [x] T2_027 Implement 7x48 weekly schedule evaluator in agent/schedule_evaluator.py
- [x] T2_028 Implement monotonic clock time tracking loop in agent/screen_time_tracker.py
- [x] T2_029 Implement warning popups (10m, 5m, 1m) and 60s grace period in agent/screen_time_tracker.py
- [x] T2_030 Implement server_time drift verification in agent/screen_time_tracker.py

## Phase 6: Client Agent System Locker & WebSocket Listener
- [x] T2_031 Implement LockWorkStation system locker in agent/system_locker.py
- [x] T2_032 Implement re-lock enforcement loop in agent/system_locker.py
- [x] T2_033 Implement policy syncer with HMAC validation in agent/policy_syncer.py
- [x] T2_034 Implement WebSocket client connection in agent/ws_listener.py
- [x] T2_035 Implement WebSocket emergency command handler in agent/ws_listener.py
- [x] T2_036 Add remaining screen time indicator in agent/tray.py
- [x] T2_037 Integrate time tracker, ws listener, and locker into agent/main.py

## Phase 7: Verification, Technical Reports & Tests
- [x] T2_038 Create policy and HMAC automated tests in tests/test_policy.py
- [x] T2_039 Create monotonic time tracker and schedule evaluator tests in tests/test_time_tracker.py
- [x] T2_040 Create WebSocket emergency command tests in tests/test_websocket_command.py
- [x] T2_041 Create Network Technical Report Section M6 in docs/M6_DONG_BO_THOI_GIAN.md
- [x] T2_042 Create Week 2 end-to-end verification checklist in docs/VERIFY_WEEK2.md
