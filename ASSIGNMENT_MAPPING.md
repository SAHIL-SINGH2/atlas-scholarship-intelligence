# Assignment 2 Mapping

| Assignment requirement | Implementation |
|---|---|
| Discover → Crawl → Extract → Verify → Score → Store → Update | `src/crawler.py`, `src/verification.py`, `src/database.py` |
| Authentic primary source | `official_source_url`, `evidence_url`, official-domain policy |
| Structured schema | `data/scholarships_verified.json` + SQLite |
| Confidence score methodology | deterministic rules in `src/verification.py` |
| VERIFIED ≥95 | threshold enforced by verification logic/data |
| Anti-hallucination | `Not specified` for unsupported facts |
| Repeated crawler | `run_crawler.py` + SQLite upsert |
| Change detection | `src/change_detection.py` + `change_history` |
| Retain old/new/date/source/evidence | `change_history` table |
| Stale/expired | deadline-based classification + current statuses |
| Free database | SQLite |
| Working interface | Streamlit `app.py` |
| 20+ records | 20 records |
| 15+ verified | 18 verified |
| 10+ at ≥95 | 18 at ≥95 |
| 3 source types | Government, University, Corporate |
| 2 change examples | NMMSS + Beedi/Cine/IOMC/LSDM official PIB extensions |
| 2 stale/expired | Beedi pre-matric + a closed application window represented in repository |
| Not a fixed URL-per-record scraper | source-hub discovery + structured extraction |
| Free/open source only | Python, Requests, BeautifulSoup, SQLite, Streamlit |
