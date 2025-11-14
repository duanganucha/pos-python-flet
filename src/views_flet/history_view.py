# -*- coding: utf-8 -*-
"""
History View - Flet Version
Show transaction history and sales summary
"""
import flet as ft
from datetime import datetime


class HistoryView:
    def __init__(self, app):
        """Initialize History view"""
        self.app = app
        self.page = app.page
        self.db = app.db
        self.receipts_list = None

    def create(self):
        """Create History view layout"""
        # Get sales summary
        try:
            summary = self.db.get_sales_summary()
        except:
            summary = {
                'today_sales': 0,
                'today_receipts': 0,
                'total_sales': 0,
                'total_receipts': 0
            }

        # Get receipts
        try:
            receipts = self.db.get_all_receipts(limit=50)
        except:
            receipts = []

        self.receipts_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        return ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Container(
                        content=ft.Text(
                            "📋 ประวัติการขาย",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        bgcolor=ft.Colors.BLUE_700,
                        padding=20,
                        border_radius=10
                    ),

                    # Summary Cards
                    ft.Row(
                        [
                            # Today's Sales Card
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "ยอดขายวันนี้",
                                                size=14,
                                                color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Text(
                                                f"฿{summary['today_sales']:,.2f}",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.WHITE
                                            ),
                                            ft.Text(
                                                f"{summary['today_receipts']} ใบเสร็จ",
                                                size=12,
                                                color=ft.Colors.WHITE70
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5
                                    ),
                                    bgcolor=ft.Colors.BLUE_600,
                                    padding=20,
                                    border_radius=10
                                ),
                                elevation=4
                            ),

                            # Total Sales Card
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "ยอดขายรวม",
                                                size=14,
                                                color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Text(
                                                f"฿{summary['total_sales']:,.2f}",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.WHITE
                                            ),
                                            ft.Text(
                                                f"{summary['total_receipts']} ใบเสร็จ",
                                                size=12,
                                                color=ft.Colors.WHITE70
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5
                                    ),
                                    bgcolor=ft.Colors.GREEN_600,
                                    padding=20,
                                    border_radius=10
                                ),
                                elevation=4
                            )
                        ],
                        spacing=20
                    ),

                    # Receipts List Header
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("รายการขายล่าสุด", size=20, weight=ft.FontWeight.BOLD),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "🔍 ค้นหา",
                                    on_click=lambda e: self.show_search_dialog(),
                                    bgcolor=ft.Colors.PURPLE_700,
                                    color=ft.Colors.WHITE
                                ),
                                ft.ElevatedButton(
                                    "📊 รายงาน",
                                    on_click=lambda e: self.show_report_dialog(),
                                    bgcolor=ft.Colors.ORANGE_700,
                                    color=ft.Colors.WHITE
                                ),
                                ft.ElevatedButton(
                                    "🔄 รีเฟรช",
                                    on_click=lambda e: self.refresh_data(),
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE
                                )
                            ],
                            spacing=10
                        ),
                        padding=ft.padding.only(top=20, bottom=10)
                    ),

                    # Receipts List
                    ft.Container(
                        content=self.build_receipts_list(receipts),
                        expand=True
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20,
            expand=True
        )

    def build_receipts_list(self, receipts):
        """Build receipts list"""
        if not receipts:
            return ft.Container(
                content=ft.Text(
                    "ยังไม่มีรายการขาย",
                    size=16,
                    color=ft.Colors.GREY_600
                ),
                alignment=ft.alignment.center,
                padding=40
            )

        receipt_cards = []
        for receipt in receipts:
            receipt_cards.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                # Receipt Icon
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.RECEIPT_LONG,
                                        color=ft.Colors.WHITE,
                                        size=30
                                    ),
                                    bgcolor=ft.Colors.BLUE_700,
                                    border_radius=50,
                                    padding=15
                                ),

                                # Receipt Info
                                ft.Column(
                                    [
                                        ft.Text(
                                            f"ใบเสร็จ #{receipt['id']}",
                                            size=16,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            f"{receipt['date']}",
                                            size=12,
                                            color=ft.Colors.GREY_600
                                        ),
                                        ft.Text(
                                            f"{receipt['items_count']} รายการ",
                                            size=12,
                                            color=ft.Colors.GREY_700
                                        )
                                    ],
                                    spacing=2,
                                    expand=True
                                ),

                                # Amount
                                ft.Column(
                                    [
                                        ft.Text(
                                            f"฿{receipt['total']:,.2f}",
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.GREEN_700
                                        ),
                                        ft.Text(
                                            f"เงินทอน ฿{receipt['change']:,.2f}",
                                            size=11,
                                            color=ft.Colors.GREY_600
                                        )
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                    spacing=2
                                ),

                                # View Button
                                ft.IconButton(
                                    icon=ft.Icons.VISIBILITY,
                                    icon_color=ft.Colors.BLUE_700,
                                    tooltip="ดูรายละเอียด",
                                    on_click=lambda e, r=receipt: self.view_receipt_details(r)
                                )
                            ],
                            spacing=15,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=15
                    ),
                    elevation=2
                )
            )

        return ft.Column(receipt_cards, spacing=10, scroll=ft.ScrollMode.AUTO)

    def view_receipt_details(self, receipt_summary):
        """View receipt details"""
        # Get full receipt details
        try:
            receipt = self.db.get_receipt(receipt_summary['id'])
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ ไม่สามารถโหลดข้อมูลได้: {str(e)}"),
                bgcolor=ft.Colors.RED_700
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Build items list
        items_list = []
        for item in receipt['items']:
            items_list.append(
                ft.Row([
                    ft.Text(f"{item['qty']}x", size=12, width=40),
                    ft.Text(item['name'], size=12, expand=True),
                    ft.Text(f"฿{item['total']:.2f}", size=12, weight=ft.FontWeight.BOLD)
                ])
            )

        # Calculate subtotal and tax
        subtotal = sum(item['total'] for item in receipt['items'])
        tax = subtotal * 0.07

        # Receipt details dialog
        details_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.RECEIPT_LONG, color=ft.Colors.BLUE_700, size=32),
                ft.Text(f"ใบเสร็จ #{receipt['id']}", size=24, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Container(
                content=ft.Column([
                    # Date
                    ft.Container(
                        content=ft.Column([
                            ft.Text("วันที่", size=12, color=ft.Colors.GREY_700),
                            ft.Text(receipt['date'], size=16, weight=ft.FontWeight.BOLD)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=10,
                        border_radius=10
                    ),

                    ft.Divider(),

                    # Items
                    ft.Text("รายการสินค้า", size=14, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column(items_list, spacing=5),
                        bgcolor=ft.Colors.GREY_50,
                        padding=10,
                        border_radius=10
                    ),

                    ft.Divider(),

                    # Pricing
                    ft.Row([
                        ft.Text("ยอดรวม", size=14),
                        ft.Text(f"฿{subtotal:.2f}", size=14, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text("ภาษี 7%", size=14),
                        ft.Text(f"฿{tax:.2f}", size=14, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text("ยอดชำระ", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"฿{receipt['total']:.2f}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Divider(),

                    # Payment details
                    ft.Row([
                        ft.Text("เงินที่รับ", size=14),
                        ft.Text(f"฿{receipt['cash_received']:.2f}", size=14, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text("เงินทอน", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"฿{receipt['change']:.2f}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ], spacing=10, scroll=ft.ScrollMode.AUTO),
                width=400,
                height=500
            ),
            actions=[
                ft.TextButton("ปิด", on_click=lambda e: self.close_dialog(details_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        # Store dialog as instance variable
        self.details_dialog = details_dialog
        self.page.overlay.append(self.details_dialog)
        self.details_dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        """Close dialog"""
        dialog.open = False
        self.page.update()

    def show_search_dialog(self):
        """Show search dialog"""
        receipt_id_field = ft.TextField(label="รหัสใบเสร็จ", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        date_from_field = ft.TextField(label="ตั้งแต่วันที่ (YYYY-MM-DD)", width=300, hint_text="2024-01-01")
        date_to_field = ft.TextField(label="ถึงวันที่ (YYYY-MM-DD)", width=300, hint_text="2024-12-31")
        min_amount_field = ft.TextField(label="ยอดขั้นต่ำ", width=300, keyboard_type=ft.KeyboardType.NUMBER, hint_text="0")
        max_amount_field = ft.TextField(label="ยอดสูงสุด", width=300, keyboard_type=ft.KeyboardType.NUMBER, hint_text="10000")

        def close_dlg(e):
            search_dlg.open = False
            self.page.update()

        def do_search(e):
            search_dlg.open = False
            self.page.update()

            # Build search criteria message
            criteria = []
            if receipt_id_field.value:
                criteria.append(f"รหัส: {receipt_id_field.value}")
            if date_from_field.value:
                criteria.append(f"จาก: {date_from_field.value}")
            if date_to_field.value:
                criteria.append(f"ถึง: {date_to_field.value}")
            if min_amount_field.value:
                criteria.append(f"ขั้นต่ำ: ฿{min_amount_field.value}")
            if max_amount_field.value:
                criteria.append(f"สูงสุด: ฿{max_amount_field.value}")

            criteria_text = ", ".join(criteria) if criteria else "ทั้งหมด"

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"🔍 ค้นหา: {criteria_text} (Demo)"),
                bgcolor=ft.Colors.PURPLE_700
            )
            self.page.snack_bar.open = True
            self.page.update()

        search_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("🔍 ค้นหาใบเสร็จ", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("กรอกเงื่อนไขการค้นหา (ไม่บังคับทั้งหมด)", size=12, color=ft.Colors.GREY_700),
                    receipt_id_field,
                    ft.Divider(),
                    ft.Text("ช่วงวันที่", size=14, weight=ft.FontWeight.BOLD),
                    date_from_field,
                    date_to_field,
                    ft.Divider(),
                    ft.Text("ช่วงยอดเงิน", size=14, weight=ft.FontWeight.BOLD),
                    min_amount_field,
                    max_amount_field
                ], spacing=15, tight=True, scroll=ft.ScrollMode.AUTO),
                width=400,
                height=500
            ),
            actions=[
                ft.TextButton("ยกเลิก", on_click=close_dlg),
                ft.ElevatedButton(
                    "ค้นหา",
                    on_click=do_search,
                    bgcolor=ft.Colors.PURPLE_700,
                    color=ft.Colors.WHITE
                )
            ]
        )

        self.page.overlay.append(search_dlg)
        search_dlg.open = True
        self.page.update()

    def show_report_dialog(self):
        """Show report dialog"""
        report_type = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="daily", label="รายงานรายวัน"),
                ft.Radio(value="weekly", label="รายงานรายสัปดาห์"),
                ft.Radio(value="monthly", label="รายงานรายเดือน"),
                ft.Radio(value="yearly", label="รายงานรายปี"),
                ft.Radio(value="custom", label="กำหนดเอง")
            ]),
            value="daily"
        )

        date_from_field = ft.TextField(label="ตั้งแต่วันที่", width=300, hint_text="2024-01-01")
        date_to_field = ft.TextField(label="ถึงวันที่", width=300, hint_text="2024-12-31")

        def close_dlg(e):
            report_dlg.open = False
            self.page.update()

        def generate_report(e):
            report_dlg.open = False
            self.page.update()

            report_names = {
                "daily": "รายวัน",
                "weekly": "รายสัปดาห์",
                "monthly": "รายเดือน",
                "yearly": "รายปี",
                "custom": "กำหนดเอง"
            }

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"📊 สร้างรายงาน{report_names.get(report_type.value, 'รายวัน')} (Demo)"),
                bgcolor=ft.Colors.ORANGE_700
            )
            self.page.snack_bar.open = True
            self.page.update()

        report_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("📊 สร้างรายงาน", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("เลือกประเภทรายงาน", size=14, weight=ft.FontWeight.BOLD),
                    report_type,
                    ft.Divider(),
                    ft.Text("ช่วงวันที่ (สำหรับกำหนดเอง)", size=14, weight=ft.FontWeight.BOLD),
                    date_from_field,
                    date_to_field
                ], spacing=15, tight=True, scroll=ft.ScrollMode.AUTO),
                width=400,
                height=450
            ),
            actions=[
                ft.TextButton("ยกเลิก", on_click=close_dlg),
                ft.ElevatedButton(
                    "สร้างรายงาน",
                    on_click=generate_report,
                    bgcolor=ft.Colors.ORANGE_700,
                    color=ft.Colors.WHITE
                )
            ]
        )

        self.page.overlay.append(report_dlg)
        report_dlg.open = True
        self.page.update()

    def refresh_data(self):
        """Refresh data"""
        # Rebuild the view
        new_view = self.create()
        # Update parent container
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("✅ รีเฟรชข้อมูลแล้ว"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()
