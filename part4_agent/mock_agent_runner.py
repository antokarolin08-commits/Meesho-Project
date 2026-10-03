import csv
import json
import os
import sys

# Ensure Python can import from part2_engine
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART2_DIR = os.path.join(ROOT_DIR, "part2_engine")
if PART2_DIR not in sys.path:
    sys.path.insert(0, PART2_DIR)

from growth_engine import is_flagged, mom_growth, validate_feed


def load_category_data(csv_path: str) -> dict:
    data = {}
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["category"].strip()
            data[cat] = {
                "month": row["month"].strip(),
                "revenue": float(row["revenue"].strip()),
                "n_orders": int(row["n_orders"].strip()),
            }
    return data


def format_narrative_message(category, month, prev_month, prev_rev, curr_rev, mom_pct):
    sign = "+" if mom_pct > 0 else ""
    return (
        f"Context: {category} performance monitoring for {month} vs. {prev_month}. "
        f"Insight [Fact]: Revenue recorded a {sign}{mom_pct}% MoM change, moving from "
        f"INR {prev_rev:.2f} to INR {curr_rev:.2f}. "
        f"Implication [Hypothesis]: Significant category variance requires ops review on supply SLAs and catalog inventory."
    )


def run(current_month: str, previous_month_csv: str, current_month_csv: str, threshold: float = 8.0) -> dict:
    # 1 & 2: Input Guardrail
    is_valid, validation_errors = validate_feed(current_month_csv)
    if not is_valid:
        return {
            "run_month": current_month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    prev_data = load_category_data(previous_month_csv)
    curr_data = load_category_data(current_month_csv)

    flagged_pool = []
    escalated_categories = []

    # 3 & 4: Compute MoM and check threshold
    for category, curr_info in curr_data.items():
        if category not in prev_data:
            continue

        prev_info = prev_data[category]
        prev_rev = prev_info["revenue"]
        curr_rev = curr_info["revenue"]
        prev_month = prev_info["month"]

        pct = mom_growth(prev_rev, curr_rev)
        flag_status = is_flagged(pct, threshold=threshold)

        if flag_status == "flagged":
            flagged_pool.append({
                "category": category,
                "mom_pct": pct,
                "previous_revenue": prev_rev,
                "current_revenue": curr_rev,
                "month": current_month,
                "prev_month": prev_month,
                "abs_magnitude": abs(pct),
            })
        elif flag_status == "escalate_exact_boundary":
            escalated_categories.append(category)

    # 5: Sort flagged by abs(mom_pct) descending
    flagged_pool.sort(key=lambda x: x["abs_magnitude"], reverse=True)

    # 6 & 7: Top 3 cap & suppression
    flagged_categories = []
    suppressed_categories = []

    for idx, item in enumerate(flagged_pool):
        if idx < 3:
            msg = format_narrative_message(
                item["category"], item["month"], item["prev_month"],
                item["previous_revenue"], item["current_revenue"], item["mom_pct"]
            )
            flagged_categories.append({
                "category": item["category"],
                "mom_pct": item["mom_pct"],
                "previous_revenue": item["previous_revenue"],
                "current_revenue": item["current_revenue"],
                "drafted": True,
                "message": msg,
            })
        else:
            suppressed_categories.append(item["category"])

    # 8: Emit JSON
    return {
        "run_month": current_month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval",
    }


if __name__ == "__main__":
    fixtures = os.path.join(ROOT_DIR, "part2_engine", "fixtures")
    p4 = os.path.join(ROOT_DIR, "part4_agent")

    # Use the monthly files already in part4_agent
    april_feed = os.path.join(p4, "april_revenue.csv")
    may_feed = os.path.join(p4, "may_revenue.csv")
    june_feed = os.path.join(p4, "june_revenue.csv")
    corrupt_feed = os.path.join(fixtures, "corrupted_feed.csv")

    print("\n================== MAY RUN (April -> May) ==================")
    res_may = run("May", april_feed, may_feed)
    print(json.dumps(res_may, indent=2))

    print("\n================== JUNE RUN (May -> June) ==================")
    res_june = run("June", may_feed, june_feed)
    print(json.dumps(res_june, indent=2))

    print("\n============== CORRUPTED FEED RUN (Hard Stop) ==============")
    res_corrupt = run("July", june_feed, corrupt_feed)
    print(json.dumps(res_corrupt, indent=2))