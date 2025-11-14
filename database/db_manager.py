"""
Database Manager for POS System
SQLite operations wrapper
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """Database Manager Class"""

    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        if db_path is None:
            db_path = os.path.join("database", "pos.db")

        self.db_path = db_path
        self.conn = None
        self.connect()

    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Access columns by name
        # Enable foreign keys
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    # ============================================================
    # PRODUCTS
    # ============================================================

    def get_all_products(self) -> List[Dict]:
        """Get all products"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, price, category
            FROM products
            ORDER BY category, name
        """)

        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'category': row['category']
            })

        return products

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Get product by ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, price, category
            FROM products
            WHERE id = ?
        """, (product_id,))

        row = cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'category': row['category']
            }
        return None

    def search_products(self, query: str) -> List[Dict]:
        """Search products by name"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, price, category
            FROM products
            WHERE name LIKE ?
            ORDER BY name
        """, (f"%{query}%",))

        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'category': row['category']
            })

        return products

    def add_product(self, name: str, price: float, category: str) -> int:
        """Add new product"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, price, category)
            VALUES (?, ?, ?)
        """, (name, price, category))

        self.conn.commit()
        return cursor.lastrowid

    def update_product(self, product_id: int, name: str, price: float, category: str) -> bool:
        """Update product"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE products
            SET name = ?, price = ?, category = ?
            WHERE id = ?
        """, (name, price, category, product_id))

        self.conn.commit()
        return cursor.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        """Delete product"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

        self.conn.commit()
        return cursor.rowcount > 0

    # ============================================================
    # RECEIPTS
    # ============================================================

    def save_receipt(self, cart: List[Dict], total: float, cash_received: float, change: float) -> int:
        """Save receipt with items"""
        cursor = self.conn.cursor()

        # Insert receipt
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO receipts (date, total, cash_received, change)
            VALUES (?, ?, ?, ?)
        """, (date_str, total, cash_received, change))

        receipt_id = cursor.lastrowid

        # Insert receipt items
        for item in cart:
            cursor.execute("""
                INSERT INTO receipt_items (receipt_id, product_id, product_name, price, qty, total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                receipt_id,
                item['id'],
                item['name'],
                item['price'],
                item['qty'],
                item['total']
            ))

        self.conn.commit()
        return receipt_id

    def get_receipt_by_id(self, receipt_id: int) -> Optional[Dict]:
        """Get receipt with items by ID"""
        cursor = self.conn.cursor()

        # Get receipt
        cursor.execute("""
            SELECT id, date, total, cash_received, change
            FROM receipts
            WHERE id = ?
        """, (receipt_id,))

        row = cursor.fetchone()
        if not row:
            return None

        receipt = {
            'id': row['id'],
            'date': row['date'],
            'total': row['total'],
            'cash_received': row['cash_received'],
            'change': row['change'],
            'items': []
        }

        # Get receipt items
        cursor.execute("""
            SELECT product_id, product_name, price, qty, total
            FROM receipt_items
            WHERE receipt_id = ?
        """, (receipt_id,))

        for item_row in cursor.fetchall():
            receipt['items'].append({
                'id': item_row['product_id'],
                'name': item_row['product_name'],
                'price': item_row['price'],
                'qty': item_row['qty'],
                'total': item_row['total']
            })

        return receipt

    def get_all_receipts(self, limit: int = 100) -> List[Dict]:
        """Get all receipts (summary only)"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT r.id, r.date, r.total, r.cash_received, r.change,
                   COUNT(ri.id) as items_count
            FROM receipts r
            LEFT JOIN receipt_items ri ON r.id = ri.receipt_id
            GROUP BY r.id
            ORDER BY r.date DESC
            LIMIT ?
        """, (limit,))

        receipts = []
        for row in cursor.fetchall():
            receipts.append({
                'id': row['id'],
                'date': row['date'],
                'total': row['total'],
                'cash_received': row['cash_received'],
                'change': row['change'],
                'items_count': row['items_count']
            })

        return receipts

    def get_sales_summary(self) -> Dict:
        """Get sales summary statistics"""
        cursor = self.conn.cursor()

        # Total sales
        cursor.execute("SELECT COUNT(*), SUM(total) FROM receipts")
        count, total = cursor.fetchone()

        # Today's sales
        cursor.execute("""
            SELECT COUNT(*), SUM(total)
            FROM receipts
            WHERE date LIKE ?
        """, (datetime.now().strftime("%Y-%m-%d") + "%",))
        today_count, today_total = cursor.fetchone()

        return {
            'total_receipts': count or 0,
            'total_sales': total or 0.0,
            'today_receipts': today_count or 0,
            'today_sales': today_total or 0.0
        }

    # ============================================================
    # CATEGORIES
    # ============================================================

    def get_all_categories(self) -> List[str]:
        """Get all unique categories"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT category
            FROM products
            ORDER BY category
        """)

        return [row[0] for row in cursor.fetchall()]

    def get_products_by_category(self, category: str) -> List[Dict]:
        """Get products by category"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, price, category
            FROM products
            WHERE category = ?
            ORDER BY name
        """, (category,))

        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'category': row['category']
            })

        return products
