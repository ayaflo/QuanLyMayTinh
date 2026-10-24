# Spec Kit Tasks: Week 4 (Version 0.4 - Final Release) - Open Guardian Kids (OGK)
<!-- Security Hardening F5, Anti-Bypass Guard M3, Benchmarking M4, Fault Tolerance M5, Legal Compliance & Final Packaging -->

## Phase 1: Security Hardening F5 - Authentication, Brute-Force Protection & Session Management (ASVS Level 1)
- [x] T4_001 Add failed_login_attempts and locked_until fields to Parent model in server/models.py
- [x] T4_002 Enforce minimum 10-character password requirement in server/schemas.py (NIST SP 800-63B)
- [x] T4_003 Implement account lockout logic (15-minute lockout after 5 consecutive failed attempts) in server/routes/auth.py
- [x] T4_004 Integrate account lockout messaging and countdown in web login template and route server/routes/dashboard.py
- [x] T4_005 Implement in-memory IP-based rate limiting (10 requests/min per IP) in server/security.py
- [x] T4_006 Enforce secure session cookies (HttpOnly, SameSite=Lax) and explicit session revocation on logout in server/routes/dashboard.py

## Phase 2: Security Hardening F5 - Encryption at Rest & Anti-IDOR Authorization Controls
- [x] T4_007 Create symmetric AES-256-GCM encryption utility (12-byte Nonce, 16-byte Tag) in server/crypto_utils.py
- [x] T4_008 Enforce device ownership verification (anti-IDOR) on emergency commands in server/routes/commands.py
- [x] T4_009 Enforce device ownership verification (anti-IDOR) on policy queries and updates in server/routes/policy.py
- [x] T4_010 Enforce device ownership verification (anti-IDOR) on reports and child request review routes in server/routes/reports.py and server/routes/requests.py

## Phase 3: Legal & Ethical Compliance - 90-Day Data Retention & Right to Erasure (Decree 13/2023/ND-CP)
- [x] T4_011 Implement purge_expired_activity_data() (90-day retention cleanup) in server/services/retention_service.py
- [x] T4_012 Register 24-hour periodic retention cleanup background task in server/main.py lifespan
- [x] T4_013 Implement Right to Erasure business logic (synchronous wipe + agent buffer purge dispatch) in server/services/retention_service.py
- [x] T4_014 Create DELETE /api/v1/devices/{device_id}/data endpoint with parent password confirmation in server/routes/retention.py
- [x] T4_015 Implement purge_local_data() (clearing offline logs, cache, daily usage) in agent/storage.py
- [x] T4_016 Build "Delete All My Child's Data" UI button and password confirmation modal in dashboard/templates/devices.html

## Phase 4: Anti-Bypass Guard & Process/Network Defense M3 (Client Agent)
- [x] T4_017 Implement DNS Adapter Watchdog loop (checks if adapter DNS is 127.0.0.1 every 20s) in agent/dns_watchdog.py
- [x] T4_018 Implement auto-remediation (restore 127.0.0.1) and emit tamper_attempt activity event in agent/dns_watchdog.py
- [x] T4_019 Seed common VPN processes (WARP, ProtonVPN, Psiphon, UltraSurf) in server/seed_domains.py and agent rules cache
- [x] T4_020 Integrate dns_watchdog daemon thread into agent lifecycle in agent/main.py

## Phase 5: Empirical Performance Measurement M4 & Fault Tolerance Verification M5
- [x] T4_021 Create automated benchmark script (CPU, RAM, DNS p50/p95 over 50 queries vs 1.1.1.3, WS latency < 500ms) in scripts/benchmark_performance.py
- [x] T4_022 Implement automated fault tolerance test suite (network loss SQLite buffer, server down, reboot recovery) in tests/test_fault_tolerance.py

## Phase 6: Specialized Network Technical Reports (M3, M4, M5)
- [x] T4_023 Author Network Technical Report M3 (7 Bypass Techniques Analysis & Countermeasures) in docs/M3_PHAN_TICH_DOI_PHO_BYPASS.md
- [x] T4_024 Author Network Technical Report M4 (Empirical Performance Benchmark with >= 30 samples) in docs/M4_DO_LUONG_HIEU_NANG.md
- [x] T4_025 Author Network Technical Report M5 (Fault Tolerance, Offline Buffer Integrity & Sync Recovery) in docs/M5_KHA_NANG_CHIU_LOI.md

## Phase 7: Ethics, Legal Compliance & Threat Modeling Documentation
- [x] T4_026 Finalize Privacy & Ethics Documentation (4 minimal fields table + child-friendly pledge NT1/NT2) in docs/PRIVACY.md
- [x] T4_027 Author STRIDE Threat Model (8 threats) & OWASP ASVS v4 Level 1 Checklist (>= 20 controls) in docs/THREATMODEL.md
- [x] T4_028 Author AI Transparency Disclosure & Academic Integrity Pledge in docs/AI_USAGE.md

## Phase 8: Automated Security Test Suite, Clean Setup Guide & Final Verification
- [x] T4_029 Create automated security tests (Account lockout, >=10 char password, anti-IDOR, AES-256-GCM, 90-day purge, Right to Erasure) in tests/test_security_f5.py
- [x] T4_030 Update clean 15-minute setup and deployment guide in README.md
- [x] T4_031 Author Week 4 final release end-to-end verification checklist in docs/VERIFY_WEEK4.md
