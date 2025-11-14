# 🗄️ POS System - SQLite Database

## การเปลี่ยนจาก JSON เป็น SQLite

โปรเจคนี้ได้อัปเกรดจาก JSON files เป็น SQLite database เพื่อประสิทธิภาพและความยืดหยุ่นที่ดีกว่า

---

## 🚀 Quick Start

### วิธีที่ 1: ใช้ Batch File (แนะนำ)
```cmd
setup_database.bat
```

### วิธีที่ 2: ใช้ Python Script
```cmd
python database/seed_db.py
```

---

## 📂 โครงสร้าง Database

### Tables:

#### **1. products**
```sql
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- price (REAL)
- category (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

#### **2. receipts**
```sql
- id (INTEGER PRIMARY KEY)
- date (TEXT)
- total (REAL)
- cash_received (REAL)
- change (REAL)
- created_at (TIMESTAMP)
```

#### **3. receipt_items**
```sql
- id (INTEGER PRIMARY KEY)
- receipt_id (INTEGER FK)
- product_id (INTEGER FK)
- product_name (TEXT)
- price (REAL)
- qty (INTEGER)
- total (REAL)
```

---

## 🔄 Migration Process

### ขั้นตอนการ Migrate:

1. **อ่านข้อมูลจาก JSON**
   - `data/products.json` → products table
   - `data/receipts.json` → receipts + receipt_items tables

2. **สร้าง Database**
   - สร้างไฟล์ `database/pos.db`
   - รัน schema.sql

3. **Import ข้อมูล**
   - Insert products
   - Insert receipts และ items

---

## 💻 การใช้งาน Database Manager

### Basic Usage:

```python
from database import DatabaseManager

# Connect to database
db = DatabaseManager()

# Get all products
products = db.get_all_products()
for product in products:
    print(f"{product['name']}: ฿{product['price']}")

# Search products
results = db.search_products("coffee")

# Save receipt
receipt_id = db.save_receipt(
    cart=[...],
    total=100.00,
    cash_received=200.00,
    change=100.00
)

# Close connection
db.close()
```

### Using Context Manager:

```python
from database import DatabaseManager

with DatabaseManager() as db:
    products = db.get_all_products()
    # Database will auto-close
```

---

## 📊 Database Operations

### Products:
- `get_all_products()` - ดึงสินค้าทั้งหมด
- `get_product_by_id(id)` - ดึงสินค้าตาม ID
- `search_products(query)` - ค้นหาสินค้า
- `add_product(name, price, category)` - เพิ่มสินค้า
- `update_product(id, name, price, category)` - แก้ไขสินค้า
- `delete_product(id)` - ลบสินค้า

### Receipts:
- `save_receipt(cart, total, cash, change)` - บันทึกใบเสร็จ
- `get_receipt_by_id(id)` - ดึงใบเสร็จตาม ID
- `get_all_receipts(limit)` - ดึงใบเสร็จทั้งหมด
- `get_sales_summary()` - สรุปยอดขาย

### Categories:
- `get_all_categories()` - ดึงหมวดหมู่ทั้งหมด
- `get_products_by_category(category)` - ดึงสินค้าตามหมวดหมู่

---

## 🛠️ Database Tools

### ดู Database ด้วย SQLite Browser:
1. ดาวน์โหลด [DB Browser for SQLite](https://sqlitebrowser.org/)
2. เปิดไฟล์ `database/pos.db`
3. ดูและแก้ไขข้อมูลได้

### Query ด้วย Command Line:
```cmd
sqlite3 database/pos.db
```

```sql
-- ดูสินค้าทั้งหมด
SELECT * FROM products;

-- ดูยอดขายวันนี้
SELECT * FROM receipts WHERE date LIKE '2025-01-13%';

-- สินค้าขายดี Top 5
SELECT p.name, SUM(ri.qty) as total_sold
FROM receipt_items ri
JOIN products p ON ri.product_id = p.id
GROUP BY p.id
ORDER BY total_sold DESC
LIMIT 5;
```

---

## 🔐 Backup & Restore

### Backup Database:
```cmd
copy database\pos.db database\pos_backup.db
```

### Restore Database:
```cmd
copy database\pos_backup.db database\pos.db
```

### Export to SQL:
```cmd
sqlite3 database/pos.db .dump > backup.sql
```

### Import from SQL:
```cmd
sqlite3 database/pos.db < backup.sql
```

---

## 📈 Performance

### ข้อดีของ SQLite:
✅ **เร็วกว่า JSON** - Query และ filter ได้เร็วกว่ามาก
✅ **ประหยัดพื้นที่** - ข้อมูลถูกบีบอัดอัตโนมัติ
✅ **Transaction Support** - รองรับ ACID compliance
✅ **Indexes** - ค้นหาเร็วด้วย index
✅ **Concurrent Access** - หลาย process อ่านพร้อมกันได้

### เปรียบเทียบ:
| ฟีเจอร์ | JSON | SQLite |
|---------|------|--------|
| ความเร็ว | 🟡 ปานกลาง | 🟢 เร็วมาก |
| Query | ❌ ไม่ได้ | ✅ SQL |
| ขนาดไฟล์ | 🟡 ใหญ่ | 🟢 เล็ก |
| Transactions | ❌ | ✅ |
| Relations | ❌ | ✅ |

---

## 🔧 Troubleshooting

### ❌ ปัญหา: "database is locked"
**วิธีแก้:**
- ปิดแอปพลิเคชันที่เปิด database อยู่
- รอ 2-3 วินาทีแล้วลองใหม่

### ❌ ปัญหา: "no such table"
**วิธีแก้:**
```cmd
python database/seed_db.py
```

### ❌ ปัญหา: ข้อมูลหายหลัง migrate
**วิธีแก้:**
- ตรวจสอบว่าไฟล์ JSON ยังอยู่
- รัน seed_db.py อีกครั้ง

---

## 📝 Migration Checklist

- [x] สร้าง schema.sql
- [x] สร้าง seed_db.py
- [x] สร้าง DatabaseManager class
- [x] ทดสอบ migration
- [x] อัปเดต pos_app.py ให้ใช้ SQLite
- [x] ทดสอบแอปพลิเคชัน
- [x] สำรอง JSON files (เก็บไว้เผื่อ rollback)

---

## 📞 Support

หากมีปัญหา:
1. ตรวจสอบว่ารัน `setup_database.bat` แล้ว
2. ดูว่าไฟล์ `database/pos.db` ถูกสร้างหรือไม่
3. ลองลบ `database/pos.db` และรัน setup ใหม่

---

**Version:** 2.0
**Database:** SQLite 3
**Last Updated:** 2025-01-13
