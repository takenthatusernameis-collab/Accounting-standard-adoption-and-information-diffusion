"""Fetch the P1 (EU member-state carve-out) governing sources and record them in the
campaign manifest, with SHA-256 over the raw bytes as received.

Run from the repository root.  Raw payloads are cached OUTSIDE the repository
per D-015; only the manifest record is committed.
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path("scripts").resolve()))
from data_manifest import ManifestWriter, sha256_bytes  # noqa: E402

UA = "ACCTCLOCK research (public-source verification; contact: research@example.org)"
CACHE = Path("/home/runner/work/_temp/kilo-tmp/kilo/cache/p1_carveout")
CACHE.mkdir(parents=True, exist_ok=True)

SOURCES = [
    (
        "S-100",
        "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02002R1606-20250101",
        "IAS Regulation (EC) No 1606/2002, consolidated version. The governing statutory text for "
        "the EU member-state IFRS obligation and the Article 4 / Article 5 options. Read for the "
        "P1 carve-out check (decision D-038).",
    ),
    (
        "S-101",
        "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32026R0338",
        "Commission Regulation (EU) 2026/338 of 13 February 2026 endorsing IFRS 18, amending "
        "Regulation (EU) 2023/1803. Article 2: application from the first financial year beginning "
        "on or after 1 January 2027. Article 3: 'binding in its entirety and directly applicable "
        "in all Member States' - the operative clause for the P1 carve-out check.",
    ),
    (
        "S-102",
        "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R1803",
        "Commission Regulation (EU) 2023/1803 - the codifying regulation whose Annex 2026/338 "
        "amends. Establishes that the EU adopts IFRS Accounting Standards in full, in bulk, as a "
        "single annex; there is no mechanism in it for a member state to opt out of an individual "
        "endorsed standard for its listed consolidated reporters.",
    ),
    (
        "S-103",
        "https://www.ifrs.org/use-around-the-world/use-of-ifrs-standards-by-jurisdiction/view-jurisdiction/european-union/",
        "IFRS Foundation jurisdiction profile for the European Union, re-read for the P1 check. "
        "Confirms the mandatory consolidated-IFRS rule and enumerates the Member State Option "
        "(Article 5 of the IAS Regulation) as the ONLY discretion left to member states.",
    ),
    (
        "S-104",
        "https://www.ifac.org/about-ifac/membership/profile/poland",
        "IFAC Country Profile - Poland, read for the P1 check as the known derogation case. "
        "Confirms Poland requires EU-endorsed IFRS for consolidated statements of all domestic "
        "publicly accountable entities, and that the only discretion exercised is the Article 5 "
        "option over WHICH ENTITIES may apply IFRS, not over WHICH STANDARDS.",
    ),
]


def main() -> int:
    writer = ManifestWriter(Path("research/manifests/p1_carveout_check.jsonl"))
    for sid, url, notes in SOURCES:
        out = CACHE / f"{sid}.html"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = resp.read()
                status = resp.status
                ctype = resp.headers.get("Content-Type")
            out.write_bytes(payload)
            writer.record_success(
                source_id=sid,
                url=url,
                http_status=status,
                payload=payload,
                local_path=str(out),
                user_agent=UA,
                content_type=ctype,
                notes=notes,
            )
            print(f"OK    {sid} {status} {len(payload)}B sha256={sha256_bytes(payload)[:16]}...")
        except Exception as exc:  # noqa: BLE001
            writer.record_failure(
                source_id=sid,
                url=url,
                http_status=None,
                error=str(exc),
                user_agent=UA,
                notes=notes,
            )
            print(f"FAIL  {sid} {type(exc).__name__}: {str(exc)[:120]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())