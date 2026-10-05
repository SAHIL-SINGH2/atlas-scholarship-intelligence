# Technical Note — Atlas Scholarship Intelligence

## 1. Architecture
A lightweight pipeline implements **Discover → Crawl → Extract → Verify → Score → Store → Update**. A small number of authoritative seed pages are used to discover multiple opportunities rather than hard-coding one URL per scholarship.

## 2. Discovery and extraction
The crawler uses Requests and BeautifulSoup. The NSP hub is parsed for scholarship/fellowship cards; university and corporate landing pages are classified as separate source types. Records are normalized into a common schema covering provider, source URLs, benefit, eligibility, academic requirements, level, income/category/domicile/institution constraints, dates, documents, selection, renewal, status, confidence and evidence.

## 3. Verification
Aggregators are not authoritative. Each record retains an official source URL and evidence URL. Government, official university and official provider domains are accepted as primary sources. A verification timestamp is stored for every record.

## 4. Confidence methodology
The score is deterministic:
- 25 official primary domain
- 15 application route retained
- 10 name/provider extracted
- 15 evidence retained
- 10 verification timestamp
- 10 deadline supported
- 5 status classified
- 5 source type classified

`VERIFIED` requires **≥95%**. No LLM is asked to generate the number.

## 5. Anti-hallucination
The system never invents missing information. If an amount, age limit, income limit or document is not supported by the retained official evidence, the field is marked `Not specified` or points to the official specification/FAQ.

## 6. Change and stale detection
Repeated crawls compare important fields before upsert. Changes are written to `change_history` with old value, new value, timestamp, source and evidence. The demonstration retains two real 2026 official deadline extensions: NMMSS (30-Sep → 31-Oct) and the Beedi/Cine/IOMC/LSDM pre-matric scheme (31-Aug → 30-Sep). A deadline before the crawl date becomes `EXPIRED`; near deadlines can become `EXPIRING_SOON`; insufficient evidence becomes `REVIEW_REQUIRED`.

## 7. Database and UI
SQLite provides inspectable persistence with `scholarships`, `change_history` and `crawl_runs`. Streamlit provides a simple searchable interface with repository metrics, detailed evidence and change history.

## 8. Limitations
Official sites vary in structure and some detailed specifications require a linked document, login or application flow. The system prioritizes trustworthy omission over unsupported inference. A verification cache is packaged so the demo works when network access is temporarily unavailable; this cache is explicitly identified rather than being presented as a fresh live crawl.
