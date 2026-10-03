import csv
from typing import List, Tuple


def mom_growth(previous: float, current: float) -> float:
    if previous == 0:
        return 0.0
    return round(((current - previous) / previous) * 100.0, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    abs_pct = round(abs(mom_pct), 4)
    thresh = round(abs(threshold), 4)

    if abs_pct > thresh:
        return "flagged"
    elif abs_pct < thresh:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            _ = next(reader)
        except StopIteration:
            return (False, ["Empty feed file"])

        line_num = 1
        for row in reader:
            line_num += 1
            if not row or all(c.strip() == "" for c in row):
                continue

            month = row[0].strip() if len(row) > 0 else ""
            category = row[1].strip() if len(row) > 1 else ""
            revenue_raw = row[2].strip() if len(row) > 2 else ""

            if revenue_raw != "":
                try:
                    val = float(revenue_raw)
                    if val < 0:
                        errors.append(
                            f"line {line_num}: negative revenue ({val}) for category={category}"
                        )
                except ValueError:
                    errors.append(f"line {line_num}: revenue not numeric: {revenue_raw!r}")

            if not category:
                errors.append(f"line {line_num}: missing category (month={month})")

            if not revenue_raw:
                errors.append(f"line {line_num}: missing revenue (category={category})")

    return (len(errors) == 0, errors)