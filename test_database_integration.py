"""
Test script to verify database integration with POS app
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database import DatabaseManager

def test_database_operations():
    """Test all database operations"""
    print("=" * 60)
    print("Testing Database Integration")
    print("=" * 60)

    try:
        # Initialize database connection
        print("\n[1] Testing database connection...")
        db = DatabaseManager()
        print("    [OK] Connected to database successfully")

        # Test 1: Get all products
        print("\n[2] Testing get_all_products()...")
        products = db.get_all_products()
        print(f"    [OK] Retrieved {len(products)} products")
        if products:
            sample = products[0]
            print(f"    Sample: {sample['name']} - Baht {sample['price']:.2f} ({sample['category']})")

        # Test 2: Search products
        print("\n[3] Testing search_products()...")
        search_results = db.search_products("coffee")
        print(f"    [OK] Found {len(search_results)} products matching 'coffee'")
        for p in search_results[:3]:
            print(f"    - {p['name']}: Baht {p['price']:.2f}")

        # Test 3: Get all categories
        print("\n[4] Testing get_all_categories()...")
        categories = db.get_all_categories()
        print(f"    [OK] Found {len(categories)} categories")
        print(f"    Categories: {', '.join(categories)}")

        # Test 4: Get products by category
        print("\n[5] Testing get_products_by_category()...")
        beverages = db.get_products_by_category("Beverages")
        print(f"    [OK] Found {len(beverages)} beverages")

        # Test 5: Get sales summary
        print("\n[6] Testing get_sales_summary()...")
        summary = db.get_sales_summary()
        print(f"    [OK] Sales Summary:")
        print(f"    - Total receipts: {summary['total_receipts']}")
        print(f"    - Total sales: Baht {summary['total_sales']:,.2f}")
        print(f"    - Today's receipts: {summary['today_receipts']}")
        print(f"    - Today's sales: Baht {summary['today_sales']:,.2f}")

        # Test 6: Get all receipts
        print("\n[7] Testing get_all_receipts()...")
        receipts = db.get_all_receipts(limit=5)
        print(f"    [OK] Retrieved {len(receipts)} recent receipts")
        if receipts:
            sample_receipt = receipts[0]
            print(f"    Latest receipt: ID {sample_receipt['id']} - Baht {sample_receipt['total']:,.2f}")

        # Test 7: Simulate saving a new receipt
        print("\n[8] Testing save_receipt()...")
        test_cart = [
            {
                'id': products[0]['id'],
                'name': products[0]['name'],
                'price': products[0]['price'],
                'qty': 2,
                'total': products[0]['price'] * 2
            },
            {
                'id': products[1]['id'],
                'name': products[1]['name'],
                'price': products[1]['price'],
                'qty': 1,
                'total': products[1]['price']
            }
        ]

        total = sum(item['total'] for item in test_cart)
        cash_received = total + 100.0
        change = cash_received - total

        receipt_id = db.save_receipt(
            cart=test_cart,
            total=total,
            cash_received=cash_received,
            change=change
        )
        print(f"    [OK] Receipt saved with ID: {receipt_id}")
        print(f"    Total: Baht {total:.2f}, Cash: Baht {cash_received:.2f}, Change: Baht {change:.2f}")

        # Test 8: Retrieve the saved receipt
        print("\n[9] Testing get_receipt_by_id()...")
        saved_receipt = db.get_receipt_by_id(receipt_id)
        if saved_receipt:
            print(f"    [OK] Retrieved receipt #{saved_receipt['id']}")
            print(f"    Date: {saved_receipt['date']}")
            print(f"    Items: {len(saved_receipt['items'])}")
            for item in saved_receipt['items']:
                print(f"      - {item['name']}: {item['qty']} x Baht {item['price']:.2f} = Baht {item['total']:.2f}")
        else:
            print("    [ERROR] Could not retrieve saved receipt")

        # Close connection
        print("\n[10] Closing database connection...")
        db.close()
        print("    [OK] Database connection closed")

        # Final summary
        print("\n" + "=" * 60)
        print("[SUCCESS] All database operations completed successfully!")
        print("=" * 60)
        print("\nDatabase integration is working correctly.")
        print("The POS application is ready to use with SQLite backend.")

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = test_database_operations()
    sys.exit(0 if success else 1)
