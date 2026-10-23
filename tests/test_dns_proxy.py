"""Automated tests for Local DNS Proxy, Sinkholing, SafeSearch and NT6 Whitelist (T3_049)."""

import pytest
from dnslib import DNSRecord, DNSQuestion, QTYPE, RCODE, A, RR
from agent.dns_proxy import (
    DNSProxyServer,
    match_domain,
    normalize_domain,
    is_google_search_domain,
    is_bing_search_domain,
    SAFESEARCH_GOOGLE_IP,
    SAFESEARCH_BING_IP,
    DOH_CANARY_DOMAIN
)


def test_domain_matching_and_subdomain_wildcard():
    """Verify exact and wildcard subdomain matching logic (T3_030)."""
    blocklist = {"tiktok.com", "roblox.com", "badsite.example.com"}

    # Exact matches
    assert match_domain("tiktok.com", blocklist) is True
    assert match_domain("TIKTOK.COM", blocklist) is True
    assert match_domain("roblox.com.", blocklist) is True

    # Subdomain wildcard matches
    assert match_domain("m.tiktok.com", blocklist) is True
    assert match_domain("api.v2.tiktok.com", blocklist) is True
    assert match_domain("web.roblox.com", blocklist) is True
    assert match_domain("sub.badsite.example.com", blocklist) is True

    # Non-matches
    assert match_domain("google.com", blocklist) is False
    assert match_domain("notroblox.com", blocklist) is False
    assert match_domain("khanacademy.org", blocklist) is False


def test_safesearch_detection_helpers():
    """Verify Google and Bing search domain classification (T3_032)."""
    assert is_google_search_domain("google.com") is True
    assert is_google_search_domain("www.google.com") is True
    assert is_google_search_domain("www.google.com.vn") is True
    assert is_google_search_domain("mail.google.com") is False

    assert is_bing_search_domain("bing.com") is True
    assert is_bing_search_domain("www.bing.com") is True
    assert is_bing_search_domain("api.bing.com") is False


def test_dns_proxy_sinkhole_response():
    """Verify that blocked domains return 0.0.0.0 sinkhole response (T3_031)."""
    recorded_events = []

    def mock_event_cb(ev_type, domain):
        recorded_events.append((ev_type, domain))

    proxy = DNSProxyServer(on_event_callback=mock_event_cb)
    proxy.update_rules(blocked={"gambling.test", "social.test"})

    # 1. Query blocked domain
    query_packet = DNSRecord.question("gambling.test").pack()
    resp_bytes = proxy.process_dns_query(query_packet)
    resp = DNSRecord.parse(resp_bytes)

    assert resp.header.rcode == RCODE.NOERROR
    assert len(resp.rr) == 1
    assert str(resp.rr[0].rdata) == "0.0.0.0"

    # Verify event was emitted
    assert ("blocked_domain", "gambling.test") in recorded_events

    # 2. Query blocked subdomain
    sub_packet = DNSRecord.question("sub.social.test").pack()
    resp_sub = DNSRecord.parse(proxy.process_dns_query(sub_packet))
    assert str(resp_sub.rr[0].rdata) == "0.0.0.0"
    assert ("blocked_domain", "sub.social.test") in recorded_events


def test_dns_proxy_safesearch_rewrite():
    """Verify SafeSearch VIP address rewrite for Google and Bing (T3_032)."""
    proxy = DNSProxyServer()
    proxy.update_rules(blocked=set(), enforce_safesearch=True)

    # 1. Google SafeSearch Rewrite
    g_query = DNSRecord.question("www.google.com").pack()
    g_resp = DNSRecord.parse(proxy.process_dns_query(g_query))
    assert g_resp.header.rcode == RCODE.NOERROR
    assert len(g_resp.rr) == 1
    assert str(g_resp.rr[0].rdata) == SAFESEARCH_GOOGLE_IP

    # 2. Bing SafeSearch Rewrite
    b_query = DNSRecord.question("bing.com").pack()
    b_resp = DNSRecord.parse(proxy.process_dns_query(b_query))
    assert b_resp.header.rcode == RCODE.NOERROR
    assert len(b_resp.rr) == 1
    assert str(b_resp.rr[0].rdata) == SAFESEARCH_BING_IP


def test_dns_proxy_doh_canary_nxdomain():
    """Verify that Canary domain use-application-dns.net returns NXDOMAIN to disable browser DoH (T3_033)."""
    proxy = DNSProxyServer()
    canary_query = DNSRecord.question(DOH_CANARY_DOMAIN).pack()
    resp = DNSRecord.parse(proxy.process_dns_query(canary_query))

    assert resp.header.rcode == RCODE.NXDOMAIN
    assert len(resp.rr) == 0


def test_dns_proxy_permanent_whitelist_immunity(monkeypatch):
    """Verify NT6: Schools and 111 hotline cannot be blocked even if in blocklist (T3_035)."""
    proxy = DNSProxyServer()
    # Mock forward_upstream to avoid network dependency in tests
    mock_reply = DNSRecord.question("tongdai111.vn").reply()
    mock_reply.add_answer(RR("tongdai111.vn", QTYPE.A, rdata=A("103.1.2.3"), ttl=300))
    monkeypatch.setattr(proxy, "forward_upstream", lambda data: mock_reply.pack())

    # Attempt to block tongdai111.vn and hcmus.edu.vn
    proxy.update_rules(
        blocked={"tongdai111.vn", "hcmus.edu.vn", "malicious.test"},
        whitelist={"tongdai111.vn", "hcmus.edu.vn"}
    )

    # Malicious test is sinkholed to 0.0.0.0
    m_resp = DNSRecord.parse(proxy.process_dns_query(DNSRecord.question("malicious.test").pack()))
    assert str(m_resp.rr[0].rdata) == "0.0.0.0"

    # Whitelist domain is NOT sinkholed and returns authentic IP
    w_resp = DNSRecord.parse(proxy.process_dns_query(DNSRecord.question("tongdai111.vn").pack()))
    assert str(w_resp.rr[0].rdata) == "103.1.2.3"


def test_dns_proxy_youtube_safesearch_rewrite():
    """Verify YouTube SafeSearch rewrite to restrict.youtube.com (T3_032)."""
    proxy = DNSProxyServer()
    proxy.update_rules(blocked=set(), enforce_safesearch=True)

    y_query = DNSRecord.question("www.youtube.com").pack()
    y_resp = DNSRecord.parse(proxy.process_dns_query(y_query))
    assert y_resp.header.rcode == RCODE.NOERROR
    assert len(y_resp.rr) == 1
    assert str(y_resp.rr[0].rdata) == "216.239.38.120"


def test_dns_proxy_malformed_packet_handling():
    """Verify DNS proxy gracefully discards garbage or truncated packets without crashing."""
    proxy = DNSProxyServer()
    assert proxy.process_dns_query(b"") == b""
    assert proxy.process_dns_query(b"\x00\x01\x02") == b""
    assert proxy.process_dns_query(b"RANDOM_MALFORMED_GARBAGE_BYTES") == b""


