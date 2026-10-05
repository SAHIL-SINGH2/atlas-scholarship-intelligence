# Test Report

## Automated
- Minimum records: PASS — 20
- Source diversity: PASS — 3 types
- Verified threshold: PASS — 18 records at ≥95%
- No blank official evidence: PASS
- Change detection: PASS
- Expired status: PASS
- Documented change fixtures: PASS

## Manual demo cases
1. Run the crawler.
2. Search `AICTE` and open a technical scholarship.
3. Open `National Means Cum Merit Scholarship` and inspect the official PIB evidence and 30-Sep → 31-Oct history.
4. Open the Beedi/Cine/IOMC/LSDM pre-matric record and inspect EXPIRED status and 31-Aug → 30-Sep history.
5. Search `Reliance` and confirm Corporate source type.
6. Search `IIT Bombay` and confirm University source type.
7. Run the crawler twice and confirm the repository remains deduplicated.
