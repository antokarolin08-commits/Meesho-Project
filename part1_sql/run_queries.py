import sqlite3
import csv
import os

DB_PATH = os.path.join("data", "meesho_reseller.db")
OUT_DIR = os.path.join("part1_sql", "output")
os.makedirs(OUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Monthly revenue by category (Direct feed for Part 2 & Part 4)
q1 = """
SELECT month, category, 
       ROUND(SUM(quantity * unit_price), 2) AS revenue, 
       COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END, category;
"""
cur.execute(q1)
rows1 = cur.fetchall()
with open(os.path.join(OUT_DIR, "monthly_category_revenue.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["month", "category", "revenue", "n_orders"])
    w.writerows(rows1)

# 2. Region-wise revenue and order count
q2 = """
SELECT r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue, COUNT(o.order_id) AS n_orders
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;
"""
cur.execute(q2)
with open(os.path.join(OUT_DIR, "region_revenue.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["region", "total_revenue", "n_orders"])
    w.writerows(cur.fetchall())

# 3. Top resellers with spend > 50,000 (LIMIT 5)
q3 = """
SELECT r.reseller_id, r.reseller_name, r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""
cur.execute(q3)
with open(os.path.join(OUT_DIR, "top_resellers.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["reseller_id", "reseller_name", "region", "total_spend"])
    w.writerows(cur.fetchall())

# 4a. Zero-order reseller identification
q4a = """
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""
cur.execute(q4a)
with open(os.path.join(OUT_DIR, "zero_order_reseller.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["reseller_id", "reseller_name", "region"])
    w.writerows(cur.fetchall())

# 4b. COUNT(*) vs COUNT(order_id) demonstration
q4b = """
SELECT r.reseller_id, r.reseller_name, COUNT(*) AS count_star, COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;
"""
cur.execute(q4b)
with open(os.path.join(OUT_DIR, "count_demonstration.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["reseller_id", "reseller_name", "count_star", "count_order_id"])
    w.writerows(cur.fetchall())

# 5. AOV for June, Delivered orders only
q5 = """
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov_june_delivered
FROM orders
WHERE month = 'June' AND status = 'Delivered';
"""
cur.execute(q5)
with open(os.path.join(OUT_DIR, "june_delivered_aov.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["aov_june_delivered"])
    w.writerows(cur.fetchall())

# Grand total verification
cur.execute("SELECT ROUND(SUM(quantity * unit_price), 2) FROM orders;")
grand_total = cur.fetchone()[0]

conn.close()

print(f"All queries executed successfully. Output files saved in {OUT_DIR}/")
print(f"Grand Total Revenue across all 900 orders: INR {grand_total}")