"""
Seed Database Script
Migrate data from JSON to SQLite
"""
import sqlite3
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

DB_PATH = os.path.join("database", "pos.db")
PRODUCTS_JSON = os.path.join("data", "products.json")
RECEIPTS_JSON = os.path.join("data", "receipts.json")
SCHEMA_SQL = os.path.join("database", "schema.sql")


def create_database():
    """Create database and tables from schema"""
    print("=" * 60)
    print("Creating Database...")
    print("=" * 60)

    # Create database directory if it doesn't exist
    os.makedirs("database", exist_ok=True)

    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute schema
    print(f"\n[OK] Reading schema from: {SCHEMA_SQL}")
    with open(SCHEMA_SQL, 'r', encoding='utf-8') as f:
        schema = f.read()

    # Execute schema using executescript (handles triggers and multiple statements)
    cursor.executescript(schema)

    conn.commit()
    print("[OK] Database schema created successfully")

    return conn


def seed_products(conn):
    """Seed products from JSON file"""
    print("\n" + "=" * 60)
    print("Seeding Products...")
    print("=" * 60)

    if not os.path.exists(PRODUCTS_JSON):
        print(f"[ERROR] Products file not found: {PRODUCTS_JSON}")
        return 0

    # Read products from JSON
    with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
        products = json.load(f)

    print(f"\n[OK] Found {len(products)} products in JSON")

    cursor = conn.cursor()

    # Clear existing products
    cursor.execute("DELETE FROM products")
    print("[OK] Cleared existing products")

    # Insert products
    inserted = 0
    for product in products:
        cursor.execute("""
            INSERT INTO products (name, price, category)
            VALUES (?, ?, ?)
        """, (product['name'], product['price'], product['category']))
        inserted += 1

    conn.commit()
    print(f"[OK] Inserted {inserted} products")

    # Display sample
    cursor.execute("SELECT * FROM products LIMIT 5")
    samples = cursor.fetchall()
    print("\nSample products:")
    for p in samples:
        print(f"  - {p[1]} (฿{p[2]:.2f}) - {p[3]}")

    return inserted


def seed_receipts(conn):
    """Seed receipts from JSON file"""
    print("\n" + "=" * 60)
    print("Seeding Receipts...")
    print("=" * 60)

    if not os.path.exists(RECEIPTS_JSON):
        print(f"[ERROR] Receipts file not found: {RECEIPTS_JSON}")
        print("  (This is normal if no transactions have been made yet)")
        return 0

    # Read receipts from JSON
    with open(RECEIPTS_JSON, 'r', encoding='utf-8') as f:
        receipts = json.load(f)

    print(f"\n[OK] Found {len(receipts)} receipts in JSON")

    cursor = conn.cursor()

    # Clear existing receipts (will cascade delete receipt_items)
    cursor.execute("DELETE FROM receipts")
    print("[OK] Cleared existing receipts")

    # Insert receipts
    inserted_receipts = 0
    inserted_items = 0

    for receipt in receipts:
        # Insert receipt
        cursor.execute("""
            INSERT INTO receipts (date, total, cash_received, change)
            VALUES (?, ?, ?, ?)
        """, (
            receipt['date'],
            receipt['total'],
            receipt.get('cash_received', receipt['total']),
            receipt.get('change', 0)
        ))

        receipt_id = cursor.lastrowid
        inserted_receipts += 1

        # Insert receipt items
        for item in receipt['items']:
            # Try to find matching product ID
            cursor.execute("SELECT id FROM products WHERE name = ?", (item['name'],))
            result = cursor.fetchone()
            product_id = result[0] if result else None

            cursor.execute("""
                INSERT INTO receipt_items (receipt_id, product_id, product_name, price, qty, total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                receipt_id,
                product_id,
                item['name'],
                item['price'],
                item['qty'],
                item['total']
            ))
            inserted_items += 1

    conn.commit()
    print(f"[OK] Inserted {inserted_receipts} receipts")
    print(f"[OK] Inserted {inserted_items} receipt items")

    # Display sample
    cursor.execute("""
        SELECT r.id, r.date, r.total, COUNT(ri.id) as items
        FROM receipts r
        LEFT JOIN receipt_items ri ON r.id = ri.receipt_id
        GROUP BY r.id
        ORDER BY r.date DESC
        LIMIT 5
    """)
    samples = cursor.fetchall()
    print("\nSample receipts:")
    for r in samples:
        print(f"  - Receipt #{r[0]}: {r[1]} - ฿{r[2]:.2f} ({r[3]} items)")

    return inserted_receipts


def show_statistics(conn):
    """Show database statistics"""
    print("\n" + "=" * 60)
    print("Database Statistics")
    print("=" * 60)

    cursor = conn.cursor()

    # Products count
    cursor.execute("SELECT COUNT(*) FROM products")
    products_count = cursor.fetchone()[0]

    # Products by category
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM products
        GROUP BY category
        ORDER BY count DESC
    """)
    categories = cursor.fetchall()

    print(f"\n[PRODUCTS] Total Products: {products_count}")
    print("   By Category:")
    for cat, count in categories:
        print(f"   - {cat}: {count}")

    # Receipts count
    cursor.execute("SELECT COUNT(*) FROM receipts")
    receipts_count = cursor.fetchone()[0]

    # Total sales
    cursor.execute("SELECT SUM(total) FROM receipts")
    total_sales = cursor.fetchone()[0] or 0

    print(f"\n[RECEIPTS] Total Receipts: {receipts_count}")
    print(f"[SALES] Total Sales: ฿{total_sales:,.2f}")

    # Database file size
    if os.path.exists(DB_PATH):
        size = os.path.getsize(DB_PATH)
        size_kb = size / 1024
        print(f"\n[DB] Database Size: {size_kb:.2f} KB")


def main():
    """Main seed function"""
    print("=" * 50)
    print("   POS System - Database Seeder")
    print("   Migrate from JSON to SQLite")
    print("=" * 50)

    try:
        # Create database and tables
        conn = create_database()

        # Seed products
        products_count = seed_products(conn)

        # Seed receipts
        receipts_count = seed_receipts(conn)

        # Show statistics
        show_statistics(conn)

        # Close connection
        conn.close()

        print("\n" + "=" * 60)
        print("[SUCCESS] Database seeding completed successfully!")
        print("=" * 60)
        print(f"\n[LOCATION] Database location: {os.path.abspath(DB_PATH)}")
        print(f"   Products: {products_count}")
        print(f"   Receipts: {receipts_count}")
        print("\nYou can now run the POS application with SQLite backend.")

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
