# -*- coding: utf-8 -*-
"""
Translation script to convert all English text to Thai in POS app
"""

# Dictionary of translations
TRANSLATIONS = {
    # Category View
    '"🏷️ Category Management"': '"🏷️ จัดการหมวดหมู่"',
    '"Note: Categories are automatically managed through products. Add products to create categories."': '"หมายเหตุ: หมวดหมู่จะถูกจัดการอัตโนมัติผ่านสินค้า เพิ่มสินค้าเพื่อสร้างหมวดหมู่"',
    '"All Categories"': '"หมวดหมู่ทั้งหมด"',

    # User View
    '"👥 User Management"': '"👥 จัดการผู้ใช้"',
    '"ℹ️ User Management Feature"': '"ℹ️ ระบบจัดการผู้ใช้"',
    '"This feature allows you to manage user accounts, roles, and permissions.\\nComing soon in the next update!"': '"ระบบนี้ช่วยให้คุณจัดการบัญชีผู้ใช้ สิทธิ์การเข้าถึง และบทบาท\\nเร็ว ๆ นี้ในการอัปเดตถัดไป!"',
    '"Planned Features:"': '"คุณสมบัติที่วางแผนไว้:"',

    # Settings View
    '"⚙️ Application Settings"': '"⚙️ ตั้งค่าโปรแกรม"',
    '"General"': '"ทั่วไป"',
    '"Store Information"': '"ข้อมูลร้าน"',
    '"Store Name:"': '"ชื่อร้าน:"',
    '"Store Address:"': '"ที่อยู่ร้าน:"',
    '"Appearance"': '"การแสดงผล"',
    '"Theme"': '"ธีม"',
    '"Select a theme for the application:"': '"เลือกธีมสำหรับแอปพลิเคชัน:"',
    '"Database"': '"ฐานข้อมูล"',
    '"Database Information"': '"ข้อมูลฐานข้อมูล"',
    '"💾 Backup Database"': '"💾 สำรองฐานข้อมูล"',
    '"🔄 Reset Database"': '"🔄 รีเซ็ตฐานข้อมูล"',
    '"About"': '"เกี่ยวกับ"',
    '"POS System"': '"ระบบขายหน้าร้าน"',
    '"Version 2.0"': '"เวอร์ชัน 2.0"',
    '"SQLite Database Edition"': '"SQLite Database Edition"',
    '"Features:"': '"คุณสมบัติ:"',
    '"💾 Save Settings"': '"💾 บันทึกการตั้งค่า"',

    # Dialogs
    '"Add to Cart"': '"เพิ่มลงตะกร้า"',
    '"➕ Add New Product"': '"➕ เพิ่มสินค้า"',
    '"Product Name:"': '"ชื่อสินค้า:"',
    '"Price (฿):"': '"ราคา (฿):"',
    '"Category:"': '"หมวดหมู่:"',
    '"✓ Save Product"': '"✓ บันทึกสินค้า"',
    '"✕ Cancel"': '"✕ ยกเลิก"',
    '"✏️ Edit Product"': '"✏️ แก้ไขสินค้า"',
    '"✓ Update Product"': '"✓ อัปเดตสินค้า"',

    # Logo and version
    '"v2.0 SQLite"': '"v2.0 SQLite"',
}

# Read the file
with open('src/pos_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Apply translations
for english, thai in TRANSLATIONS.items():
    content = content.replace(english, thai)

# Write back
with open('src/pos_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Translation complete!")
print(f"[OK] Translated {len(TRANSLATIONS)} text strings")
