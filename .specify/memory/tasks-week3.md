# Spec Kit Tasks: Week 3 (Version 0.3) - Open Guardian Kids (OGK)
<!-- Deep Network Filtering: DNS Proxy F2, App SHA-256 & Transparency F3 -->

## Phase 1: Server Database Models & Schemas
- [ ] T3_001 Add DomainRule model in server/models.py
- [ ] T3_002 Add AppRule model in server/models.py
- [ ] T3_003 Add ActivityEvent model (F3 schema) in server/models.py
- [ ] T3_004 Add AccessRequest model (NT3 voice of child) in server/models.py
- [ ] T3_005 Add domain and app rule Pydantic schemas in server/schemas.py
- [ ] T3_006 Add event ingestion batch Pydantic schemas in server/schemas.py
- [ ] T3_007 Add access request and report summary Pydantic schemas in server/schemas.py

## Phase 2: Domain Rules Seeding & Core Filtering Services
- [ ] T3_008 Create seed data script for 200 categorized domains in server/seed_domains.py
- [ ] T3_009 Implement filtering management service in server/services/filtering_service.py
- [ ] T3_010 Implement batch event ingestion service with idempotency key in server/services/event_service.py
- [ ] T3_011 Implement report summary and timeline aggregation service in server/services/report_service.py
- [ ] T3_012 Implement access request handler with WebSocket dispatch in server/services/request_service.py

## Phase 3: Server Routes & API Endpoints
- [ ] T3_013 Implement GET /api/v1/filtering/rules endpoint in server/routes/filtering.py
- [ ] T3_014 Implement POST /api/v1/filtering/domain-rules and app-rules in server/routes/filtering.py
- [ ] T3_015 Implement POST /api/v1/events/batch endpoint in server/routes/events.py
- [ ] T3_016 Implement GET /api/v1/reports/summary endpoint in server/routes/reports.py
- [ ] T3_017 Implement POST /api/v1/requests endpoint in server/routes/requests.py
- [ ] T3_018 Implement GET /api/v1/requests and PUT /api/v1/requests/{id}/review in server/routes/requests.py
- [ ] T3_019 Register filtering, events, reports, and requests routers in server/main.py

## Phase 4: Parent Dashboard Reporting, Filtering & Child Requests UI
- [ ] T3_020 Integrate lightweight Chart.js library into dashboard/templates/base.html
- [ ] T3_021 Add usage reports section (timeline chart, top 10 apps/domains) in dashboard/templates/devices.html
- [ ] T3_022 Add 200-domain classification management table in dashboard/templates/devices.html
- [ ] T3_023 Add SHA-256 application control table in dashboard/templates/devices.html
- [ ] T3_024 Add child access requests inbox (NT3) in dashboard/templates/devices.html
- [ ] T3_025 Update dashboard view route with reports, rules, and requests in server/routes/dashboard.py
- [ ] T3_026 Add styles for charts, filtering tables, and request badges in dashboard/static/style.css

## Phase 5: Client Agent DNS Proxy & SafeSearch Enforcer
- [ ] T3_027 Add dnslib dependency in agent/requirements.txt
- [ ] T3_028 Add dns_rules_cache and app_rules_cache tables in agent/storage.py
- [ ] T3_029 Initialize UDP DNS proxy server on 127.0.0.1:53 in agent/dns_proxy.py
- [ ] T3_030 Implement domain and wildcard subdomain matching in agent/dns_proxy.py
- [ ] T3_031 Implement DNS sinkholing (0.0.0.0 loopback response) in agent/dns_proxy.py
- [ ] T3_032 Implement SafeSearch enforcement (Google, Bing, YouTube rewrite) in agent/dns_proxy.py
- [ ] T3_033 Implement DoH canary domain NXDOMAIN responder in agent/dns_proxy.py
- [ ] T3_034 Implement upstream DNS forwarding to 1.1.1.3/8.8.8.8 in agent/dns_proxy.py
- [ ] T3_035 Implement permanent whitelist bypass for schools and 111 hotline (NT6) in agent/dns_proxy.py
- [ ] T3_036 Implement Windows DNS adapter configurator (127.0.0.1 redirect) in agent/dns_configurator.py

## Phase 6: Client Agent Process SHA-256 App Controller
- [ ] T3_037 Add psutil dependency in agent/requirements.txt
- [ ] T3_038 Implement AppController with SHA-256 file hashing in agent/app_controller.py
- [ ] T3_039 Implement background process scan loop (3-5s interval) in agent/app_controller.py
- [ ] T3_040 Implement process termination and NT4 explanatory popup in agent/app_controller.py
- [ ] T3_041 Implement anti-rename bypass protection using SHA-256 matching in agent/app_controller.py

## Phase 7: Client Agent Offline Event Buffer & Child Transparency View
- [ ] T3_042 Add offline event buffer table (pending_events) in agent/storage.py
- [ ] T3_043 Implement event collector and batch sync loop in agent/event_collector.py
- [ ] T3_044 Implement child transparency dashboard window ("Today's Usage") in agent/child_view.py
- [ ] T3_045 Implement "Request More Time" and "Report Wrongly Blocked" actions in agent/child_view.py
- [ ] T3_046 Integrate child view in agent/tray.py and start DNS/App/Event threads in agent/main.py

## Phase 8: Network Technical Reports, Automated Tests & Verification
- [ ] T3_047 Create Network Technical Report Section M1 (DNS Packet Flow & Wireshark) in docs/M1_LUONG_GOI_TIN_DNS.md
- [ ] T3_048 Create Network Technical Report Section M2 (Comparison of 4 Blocking Methods) in docs/M2_SO_SANH_PHUONG_AN_CHAN.md
- [ ] T3_049 Create DNS proxy automated tests in tests/test_dns_proxy.py
- [ ] T3_050 Create app filtering and event ingestion tests in tests/test_app_filtering_and_events.py
- [ ] T3_051 Create Week 3 end-to-end verification checklist in docs/VERIFY_WEEK3.md
