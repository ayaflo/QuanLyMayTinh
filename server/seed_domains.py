"""Predefined seed dataset of 200 categorized domains for Open Guardian Kids (F2).
Categories:
1. Giáo dục (Education) - Permanent whitelist NT6 protected
2. Giải trí (Entertainment)
3. Mạng xã hội (Social Media)
4. Game (Gaming)
5. Không phù hợp (Unsuitable / Inappropriate - safe neutral test domains)
6. DoH (DNS over HTTPS resolvers)
"""

import sys
from sqlalchemy.orm import Session
from datetime import datetime, timezone

try:
    from .database import SessionLocal, engine, Base
    from .models import DomainRule
except (ImportError, ValueError):
    from server.database import SessionLocal, engine, Base
    from server.models import DomainRule


def utc_now():
    return datetime.now(timezone.utc)


SEED_DOMAINS_DATA = [
    # -------------------------------------------------------------------------
    # 1. Giáo dục (>= 40 domains, NT6 Whitelist protected)
    # -------------------------------------------------------------------------
    {"category": "Giáo dục", "domain": "tongdai111.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "moet.gov.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "hcmus.edu.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "vnuhcm.edu.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "khanacademy.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "wikipedia.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "vi.wikipedia.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "en.wikipedia.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "coursera.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "edx.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "duolingo.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "quizlet.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "scratch.mit.edu", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "vietjack.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "loigiaihay.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "hoc247.net", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "olm.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "vuihoc.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "hocmai.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "sachmem.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "codecademy.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "w3schools.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "geeksforgeeks.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "stackoverflow.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "github.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "gitlab.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "python.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "developer.mozilla.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "hust.edu.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "vnu.edu.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "uit.edu.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "uet.vnu.edu.vn", "action": "allow", "is_permanent_whitelist": True},
    {"category": "Giáo dục", "domain": "báchkhoa.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "vndoc.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "cunghoc.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "tuyensinh247.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "violet.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "onluyen.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "tienganh123.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "topica.edu.vn", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "freecodecamp.org", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "leetcode.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "hackerrank.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "codewars.com", "action": "allow", "is_permanent_whitelist": False},
    {"category": "Giáo dục", "domain": "ted.com", "action": "allow", "is_permanent_whitelist": False},

    # -------------------------------------------------------------------------
    # 2. Mạng xã hội (Social Media - >= 30 domains, Default: block)
    # -------------------------------------------------------------------------
    {"category": "Mạng xã hội", "domain": "facebook.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "m.facebook.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "fb.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "tiktok.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "instagram.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "twitter.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "x.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "threads.net", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "reddit.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "discord.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "discord.gg", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "telegram.org", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "t.me", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "snapchat.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "pinterest.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "tumblr.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "vk.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "weibo.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "line.me", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "viber.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "wechat.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "kakaotalk.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "ask.fm", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "badoo.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "tinder.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "omegle.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "chatroulette.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "clubhouse.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "mastodon.social", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "blueskyweb.xyz", "action": "block", "is_permanent_whitelist": False},
    {"category": "Mạng xã hội", "domain": "bsky.app", "action": "block", "is_permanent_whitelist": False},

    # -------------------------------------------------------------------------
    # 3. Game (Gaming - >= 30 domains, Default: block)
    # -------------------------------------------------------------------------
    {"category": "Game", "domain": "roblox.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "steampowered.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "steamcommunity.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "epicgames.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "riotgames.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "garena.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "garena.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "minecraft.net", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "ea.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "ubisoft.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "battle.net", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "blizzard.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "origin.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "playstation.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "xbox.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "nintendo.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "leagueoflegends.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "valorant.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "genshin.hoyoverse.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "hoyoverse.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "pubg.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "freefiremobile.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "vnggames.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "zingplay.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "gameloft.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "miniclip.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "poki.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "y8.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "crazygames.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "krunker.io", "action": "block", "is_permanent_whitelist": False},
    {"category": "Game", "domain": "slither.io", "action": "block", "is_permanent_whitelist": False},

    # -------------------------------------------------------------------------
    # 4. Giải trí (Entertainment - >= 30 domains, Default: block)
    # -------------------------------------------------------------------------
    {"category": "Giải trí", "domain": "youtube.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "youtu.be", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "netflix.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "spotify.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "zingmp3.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "nhaccuatui.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "bilibili.tv", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "iq.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "fptplay.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "vieon.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "twitch.tv", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "soundcloud.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "disneyplus.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "primevideo.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "hulu.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "appletv.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "tv360.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "galaxycine.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "cgv.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "lottecinemavn.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "dailymotion.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "vimeo.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "9gag.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "webtoons.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "manga-plus.org", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "nettruyen.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "truyenfull.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "popsworldwide.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "kplus.vn", "action": "block", "is_permanent_whitelist": False},
    {"category": "Giải trí", "domain": "vtvgiaitri.vn", "action": "block", "is_permanent_whitelist": False},

    # -------------------------------------------------------------------------
    # 5. DoH (DNS over HTTPS resolvers - >= 15 domains, Default: block to prevent bypass)
    # -------------------------------------------------------------------------
    {"category": "DoH", "domain": "cloudflare-dns.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "1dot1dot1dot1.cloudflare-dns.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "dns.google", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "dns.google.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "dns.quad9.net", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "doh.opendns.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "dns.adguard.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "dns.nextdns.io", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "doh.cleanbrowsing.org", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "doh.tiar.app", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "dns.alidns.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "doh.mullvad.net", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "dns.controld.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "ordns.he.net", "action": "block", "is_permanent_whitelist": False},
    {"category": "DoH", "domain": "doh.applied-privacy.net", "action": "block", "is_permanent_whitelist": False},

    # -------------------------------------------------------------------------
    # 6. Không phù hợp (Unsuitable - >= 50 safe neutral test domains, Default: block)
    # Using safe synthetic test domains (NT2 & Karpathy Governance rule 3)
    # -------------------------------------------------------------------------
    {"category": "Không phù hợp", "domain": "adult-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "gambling-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "betting-demo.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "casino-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "malware-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "phishing-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "violence-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "weapons-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "drugs-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "hate-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "proxy-bypass-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "vpn-free-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "tor-exit-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "anonymizer-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "piracy-warez-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "torrent-seed-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "scam-alert-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "crypto-drainer-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "exploit-payload-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "spyware-beacon-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "trojan-dropper-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "ransomware-c2-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "illegal-substance-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "darkweb-portal-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "unregulated-crypto-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "ponzi-scheme-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "lottery-scam-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "fake-giveaway-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "credential-harvest-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "botnet-controller-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "ddos-stress-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "keylogger-upload-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "unauthorized-remote-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "web-miner-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "coinhive-mock-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "clickjack-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "malvertising-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "popunder-network-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "trackers-invasive-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "typosquatting-target-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "fake-bank-auth-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "vishing-portal-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "smishing-link-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "identity-theft-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "data-leak-repo-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "zero-day-market-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "carding-forum-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "counterfeit-goods-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "stolen-accounts-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "rootkit-distribution-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "bypass-firewall-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "evasion-payload-test.example.com", "action": "block", "is_permanent_whitelist": False},
    {"category": "Không phù hợp", "domain": "c2-domain-flux-test.example.com", "action": "block", "is_permanent_whitelist": False},
]


def seed_domain_rules(db: Session) -> int:
    """Seed the 200 predefined categorized domain rules into the database.
    Returns the count of new rules inserted.
    """
    inserted = 0
    for item in SEED_DOMAINS_DATA:
        existing = db.query(DomainRule).filter(DomainRule.domain == item["domain"]).first()
        if not existing:
            rule = DomainRule(
                category=item["category"],
                domain=item["domain"],
                action=item["action"],
                is_permanent_whitelist=item.get("is_permanent_whitelist", False),
                created_at=utc_now()
            )
            db.add(rule)
            inserted += 1
    if inserted > 0:
        db.commit()
    return inserted


if __name__ == "__main__":
    db = SessionLocal()
    try:
        # Create tables if not existing
        Base.metadata.create_all(bind=engine)
        count = seed_domain_rules(db)
        total = db.query(DomainRule).count()
        print(f"[*] Seeded {count} new domains. Total domain rules in DB: {total}")
    finally:
        db.close()
