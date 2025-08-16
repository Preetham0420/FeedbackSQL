import sqlite3
import os
from tabulate import tabulate

def view_database():
    db_path = os.path.join('instance', 'feedback.db')

    if not os.path.exists(db_path):
        print("❌ Database file not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Show tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("📦 Tables in the database:")
    for table in tables:
        print(f" - {table[0]}")

    # Show contents of each table
    for table in tables:
        table_name = table[0]
        print(f"\n📄 Contents of table '{table_name}':")

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if rows:
            print(tabulate(rows, headers=columns, tablefmt="grid"))
        else:
            print("  (No records)")

    conn.close()

if __name__ == "__main__":
    view_database()
