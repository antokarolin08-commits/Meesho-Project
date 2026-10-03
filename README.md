# Meesho Reseller Growth & Alert Intelligence Pipeline

A deterministic, offline intelligence pipeline for monitoring month-on-month category revenue fluctuations, suppressing notification flooding, enforcing data privacy, and alerting regional category managers with zero hallucinated figures.

---

## 1. Zero Paid or Account-Gated Services
- This entire repository runs offline with standard Python 3 (Python 3.9+).
- **Zero API keys required**: All narrative generation uses deterministic offline template filling.
- **Zero media uploaded**: No images, plots, or PDF files are used or required.

---

## 2. Python Standard Libraries Consulted
- `sqlite3`: In-memory and file-based SQL business query processing.
- `csv`: Reading, writing, and parsing feeds and fixtures.
- `unittest`: Executing Given-When-Then test specifications.
- `json`: Emitting structured JSON agent contracts.
- `os` & `sys`: Path resolution and modular script execution.

---

## 3. Order of Operations / Reproduction Steps

Run each script from the project root in the following sequence:

```bash
# 1. Regenerate raw dataset and database (April, May, June 2026)
python data/generate_dataset.py

# 2. Run Part 1 SQL business queries and export CSV results
python part1_sql/run_queries.py

# 3. Run Part 2 growth engine test suite
python part2_engine/test_growth_engine.py

# 4. Run Part 3 privacy masking test suite
python part3_narrative/test_masking.py

# 5. Execute Part 4 Mock Agent Runner
python part4_agent/mock_agent_runner.py