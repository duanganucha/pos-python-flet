import win32print
import win32api
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io


class ReceiptPrinterV2:
    def __init__(self, printer_name=None):
        """
        Initialize printer
        printer_name: ชื่อ printer (ถ้า None จะใช้ default printer)
        """
        if printer_name is None:
            self.printer_name = win32print.GetDefaultPrinter()
        else:
            self.printer_name = printer_name
        
        print(f"Using printer: {self.printer_name}")
    
    @staticmethod
    def get_available_printers():
        """ดึงรายชื่อ printers ทั้งหมด"""
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
        printer_list = [printer[2] for printer in printers]
        return printer_list
    
    def format_receipt(self, data):
        """จัดรูปแบบข้อมูลใบเสร็จ"""
        lines = []
        
        # Header
        lines.append("=" * 40)
        if 'shop_name' in data:
            lines.append(self.center_text(data['shop_name'], 40))
        if 'address' in data:
            lines.append(self.center_text(data['address'], 40))
        lines.append("=" * 40)
        
        # Date and time
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        lines.append(f"วันที่: {now}")
        if 'receipt_no' in data:
            lines.append(f"เลขที่ใบเสร็จ: {data['receipt_no']}")
        lines.append("-" * 40)
        
        # Items header
        lines.append(f"{'รายการ':<20} {'จำนวน':>6} {'ราคา':>10}")
        lines.append("-" * 40)
        
        # Items
        total = 0
        if 'items' in data:
            for item in data['items']:
                name = item['name'][:18]
                qty = item['qty']
                price = item['price']
                amount = qty * price
                total += amount
                
                lines.append(f"{name:<20} {qty:>6} {amount:>10}")
                if len(item['name']) > 18:
                    lines.append(f"  {item['name'][18:]}")
        
        lines.append("-" * 40)
        
        # Totals
        subtotal = total
        if 'discount' in data:
            discount = data['discount']
            lines.append(f"{'รวมเบื้องต้น':<28} {subtotal:>10}")
            lines.append(f"{'ส่วนลด':<28} {discount:>10}")
            total = subtotal - discount
        
        lines.append(f"{'รวมทั้งสิ้น':<28} {total:>10}")
        
        if 'tax' in data:
            lines.append(f"{'ภาษีมูลค่าเพิ่ม':<28} {data['tax']:>10}")
        
        lines.append("=" * 40)
        
        # Payment method
        if 'payment_method' in data:
            lines.append(f"วิธีชำระเงิน: {data['payment_method']}")
        
        # Footer message
        if 'message' in data:
            lines.append("")
            lines.append(self.center_text(data['message'], 40))
        
        lines.append("")
        lines.append(self.center_text("ขอบคุณที่ซื้อสินค้า", 40))
        lines.append("")
        lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def center_text(text, width):
        """จัดกึ่งกลาง text"""
        return text.center(width)
    
    def print_receipt_simple(self, receipt_data):
        """
        วิธี 1: พิมพ์โดยบันทึกเป็น text file แล้วเปิดด้วย Notepad
        (วิธีนี้ง่ายที่สุด ใช้งานได้กับ printer ทั่วไป)
        """
        try:
            import subprocess
            import os
            import tempfile
            
            receipt_text = self.format_receipt(receipt_data)
            
            # บันทึกเป็น temp file
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as f:
                f.write(receipt_text)
                temp_file = f.name
            
            # เปิด Notepad และพิมพ์
            subprocess.Popen(f'notepad.exe /p "{temp_file}"')
            
            print("✓ ส่งไปพิมพ์แล้ว (Notepad)")
            return True
            
        except Exception as e:
            print(f"✗ เกิดข้อผิดพลาด: {e}")
            return False
    
    def print_receipt_raw(self, receipt_data):
        """
        วิธี 2: ส่งไป printer โดยตรง (สำหรับ thermal printer)
        """
        try:
            receipt_text = self.format_receipt(receipt_data)
            
            # เปิด connection กับ printer
            hprinter = win32print.OpenPrinter(self.printer_name)
            
            # แปลง text เป็น bytes
            text_bytes = receipt_text.encode('utf-8')
            
            # ส่งไป printer
            win32print.StartDocPrinter(hprinter, 1, ("Receipt", None, "RAW"))
            win32print.StartPagePrinter(hprinter)
            win32print.WritePrinter(hprinter, text_bytes)
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
            win32print.ClosePrinter(hprinter)
            
            print("✓ พิมพ์สำเร็จ")
            return True
            
        except Exception as e:
            print(f"✗ เกิดข้อผิดพลาด: {e}")
            return False
    
    def print_to_file(self, receipt_data, filename="receipt.txt"):
        """บันทึกใบเสร็จเป็นไฟล์ (สำหรับ test)"""
        receipt_text = self.format_receipt(receipt_data)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(receipt_text)
        print(f"✓ บันทึกไฟล์: {filename}")


# ตัวอย่างการใช้
if __name__ == "__main__":
    # 1. ดูรายชื่อ printers ทั้งหมด
    print("รายชื่อ Printers ที่มี:")
    printers = ReceiptPrinterV2.get_available_printers()
    for i, printer in enumerate(printers, 1):
        print(f"{i}. {printer}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. สร้าง receipt data
    receipt_data = {
        'shop_name': 'ร้านค้า ABC',
        'address': '123 ถนนประชาธิปัตย์ กรุงเทพ',
        'receipt_no': '001234',
        'items': [
            {'name': 'สินค้า A', 'qty': 2, 'price': 150},
            {'name': 'สินค้า B', 'qty': 1, 'price': 250},
            {'name': 'สินค้า C ชื่อยาว', 'qty': 3, 'price': 100},
        ],
        'discount': 50,
        'tax': 35.50,
        'payment_method': 'เงินสด',
        'message': 'ขอให้อากาศร่มเย็น'
    }
    
    # 3. สร้าง printer object
    printer = ReceiptPrinterV2()
    
    # 4. บันทึกเป็นไฟล์ก่อน (สำหรับ preview)
    printer.print_to_file(receipt_data, "receipt_preview.txt")
    
    # 5. วิธีที่ 1: พิมพ์ผ่าน Notepad (ง่ายที่สุด)
    #printer.print_receipt_simple(receipt_data)
    
    # 6. วิธีที่ 2: ส่งไป printer โดยตรง (สำหรับ thermal printer)
    printer.print_receipt_raw(receipt_data)