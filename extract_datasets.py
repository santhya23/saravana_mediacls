import sqlite3
import csv

DB_PATH = 'database/pharmacy.db'

def extract_and_export(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"\n📋 ===== DATA FROM {table_name.upper()} =====\n")

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Column names
    headers = [desc[0] for desc in cursor.description]

    # ---- PRINT TO TERMINAL ----
    print(" | ".join(headers))
    print("-" * 120)

    for row in rows:
        print(row)

    # ---- EXPORT TO CSV ----
    csv_file = f"{table_name}_dataset.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"\n✅ Exported to {csv_file}")

    conn.close()


if __name__ == "__main__":
    extract_and_export("suppliers")
    extract_and_export("medicines")
    extract_and_export("sales")
    extract_and_export("sale_items")
