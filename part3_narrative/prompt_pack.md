# Reusable Prompt Pack: Reseller Growth Narrative Generator

This prompt pack establishes a deterministic, privacy-guarded pattern for converting verified numerical changes into executive updates for regional category managers.

---

## 1. Trigger
This prompt is triggered whenever an individual category's month-on-month revenue variance test (`is_flagged(mom_pct)`) returns `"flagged"` (absolute growth strictly greater than 8.0%).

---

## 2. Input List
The prompt requires the following six parameters, sourced directly from verified SQL and engine outputs:
- `{category}`: Name of the product category (e.g., "Ethnic Wear").
- `{month}`: Current evaluation month (e.g., "May").
- `{prev_month}`: Baseline prior month (e.g., "April").
- `{previous_revenue}`: Verified revenue of the prior month rounded to 2 decimals.
- `{current_revenue}`: Verified revenue of the current month rounded to 2 decimals.
- `{mom_pct}`: Calculated Month-on-Month growth percentage rounded to 2 decimals.

---

## 3. Prompt

```text
You are an executive category operations analyst at Meesho. Generate a structured, 3-part update for regional category managers using the exact data provided below. Do not infer, estimate, or introduce any numeric value not explicitly supplied.

Data Inputs:
- Category: {category}
- Comparison: {month} vs. {prev_month}
- Previous Revenue: INR {previous_revenue}
- Current Revenue: INR {current_revenue}
- MoM Variance: {mom_pct}%

Required Output Structure:
1. Context: State the category being evaluated and the exact comparison timeframe ({month} vs. {prev_month}).
2. Insight (Fact): State the exact baseline revenue (INR {previous_revenue}), the current revenue (INR {current_revenue}), and the verified MoM growth rate ({mom_pct}%). Explicitly label this observation as [Fact].
3. Implication: Propose operational hypotheses explaining the variance and provide concrete next steps for category managers regarding catalog depth, seller dispatch rates, and regional allocation. Explicitly label hypotheses as [Hypothesis].