# Agent Specification: Monthly Reseller Growth & Alert Intelligence

## 1. Goal
Keep Meesho category managers continuously informed of significant month-on-month category revenue movements exceeding an 8.0% variance threshold, while holding every drafted message at a mandatory human-approval checkpoint prior to release.

---

## 2. Core Agentic Architecture

### 2.1 Tools
- `validate_feed(csv_path: str) -> tuple[bool, list[str]]`: Input verification tool that checks row format, missing categories, missing revenues, and non-negative values.
- `mom_growth(previous: float, current: float) -> float`: Deterministic Month-on-Month mathematical percentage growth calculator.
- `is_flagged(mom_pct: float, threshold: float = 8.0) -> str`: Three-state decision evaluator returning `"flagged"`, `"not_flagged"`, or `"escalate_exact_boundary"`.
- `prompt_pack_fill(category, month, prev_month, prev_rev, curr_rev, mom_pct)`: Deterministic template engine formatting factual numbers into Context → Insight → Implication drafts.

### 2.2 Memory / State
- Persistent state stores the prior month's category-level revenue and order counts loaded from SQLite/CSV feeds.
- Runtime state maintains:
  - Validated current-cycle feeds
  - Candidate variances sorted by magnitude
  - Top 3 drafted queue
  - Suppressed category names
  - Escalated category names

### 2.3 Planner (Ordered Subtasks 1–8)
1. **Intake & Validation**: Ingest `current_month_csv` and run `validate_feed`.
2. **Hard Stop Gate**: If validation fails, halt execution immediately with `action_taken: "hard_stop"`, returning the exact error list. Do not attempt MoM calculations.
3. **MoM Calculation**: For valid feeds, compute `mom_growth` against the corresponding category in `previous_month_csv`.
4. **Significance Evaluation**: Run `is_flagged` on every category at threshold = 8.0%.
5. **Magnitude Prioritization**: Sort all categories returning `"flagged"` descending by `abs(mom_pct)`.
6. **Top 3 Draft Capping**: Draft executive alert updates for at most the top 3 flagged categories to prevent notification fatigue.
7. **Suppression Logging**: Any flagged category ranked 4th or lower is logged in `suppressed_categories` with `drafted: False`.
7b. **Exact-Boundary Escalation**: Any category returning `"escalate_exact_boundary"` is routed to `escalated_categories` without auto-drafting.
8. **Structured JSON Serialization**: Emit one final structured JSON payload per run.

### 2.4 Feedback Loop
- The agent holds all drafts in a pending review state (`action_taken: "drafted_and_held_for_approval"`).
- A category operations manager signs off on the generated text before dispatch to stakeholders.

---

## 3. Guardrails

- **Input Guardrail**: The feed must pass `validate_feed` with zero schema, type, or range errors before any computation executes.
- **Action Guardrail**: The agent never sends external emails or messages directly; it drafts and stages updates for human verification.
- **Output Guardrail**: Every numeric metric in the generated message traces directly to verified Part 1 SQL and Part 2 engine numbers (zero hallucinated figures).

---

## 4. Stopping Conditions

- **Success Stopping Condition**: All rows pass validation, MoM variance is evaluated, top 3 flagged categories are drafted, remaining flagged items are recorded as suppressed, exact boundaries are escalated, and a structured JSON payload is produced with `action_taken: "drafted_and_held_for_approval"`.
- **Error Stopping Condition (Hard Stop)**: If `validate_feed` detects missing categories, missing revenues, unparseable strings, or negative values, the agent halts immediately with `validation_status: "invalid"`, outputs the ordered error list, and leaves calculation lists empty.

---

## 5. Agent-Level Behavioral Specs (Given-When-Then)

- **Spec 1 (Significant Surge)**:
  * **GIVEN** April→May Ethnic Wear revenue moves from 104520.77 to 185107.61,
  * **WHEN** the agent processes the feed,
  * **THEN** it calculates `mom_pct` = 77.1%, identifies status as `"flagged"`, and drafts an alert message inside the top 3 cap.

- **Spec 2 (Sub-Threshold Movement)**:
  * **GIVEN** May→June Beauty & Personal Care revenue moves from 35542.11 to 37559.07,
  * **WHEN** the agent processes the feed,
  * **THEN** it calculates `mom_pct` = 5.67%, identifies status as `"not_flagged"`, and excludes the category from both flagged and suppressed outputs.

- **Spec 3 (Exact Boundary Escalation)**:
  * **GIVEN** a category with prior revenue = 100000.0 and current revenue = 108000.0 (exact 8.0% variance),
  * **WHEN** the agent processes the feed,
  * **THEN** it calculates `mom_pct` = 8.0%, marks it as `"escalate_exact_boundary"`, and places it in `escalated_categories` without auto-drafting.

- **Spec 4 (Corrupted Input Hard Stop)**:
  * **GIVEN** an input feed containing negative values or missing fields (such as `corrupted_feed.csv`),
  * **WHEN** the agent executes validation,
  * **THEN** it halts immediately, returns `action_taken: "hard_stop"`, and populates `validation_errors` with the 3 ordered diagnostic messages.