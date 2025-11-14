# -*- coding: utf-8 -*-
"""
Menu View - Flet Version
Manage menu items and products
"""
import flet as ft


class MenuView:
    def __init__(self, app):
        """Initialize Menu view"""
        self.app = app
        self.page = app.page
        self.db = app.db
        self.products_list = None

    def create(self):
        """Create Menu view layout"""
        # Get all products
        products = self.app.products

        return ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    "📦 จัดการเมนู",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "+ เพิ่มเมนูใหม่",
                                    on_click=lambda e: self.add_product(),
                                    bgcolor=ft.Colors.ORANGE_700,
                                    color=ft.Colors.WHITE
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.ORANGE_700,
                        padding=20,
                        border_radius=10
                    ),

                    # Stats Cards
                    ft.Row(
                        [
                            self.build_stat_card("📦 สินค้าทั้งหมด", str(len(products)), ft.Colors.BLUE_600),
                            self.build_stat_card("🏷️ หมวดหมู่", str(len(self.app.categories)), ft.Colors.GREEN_600),
                        ],
                        spacing=20
                    ),

                    # Products Table
                    ft.Container(
                        content=self.build_products_table(products),
                        expand=True
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20,
            expand=True
        )

    def build_stat_card(self, title, value, color):
        """Build stat card"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(title, size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Text(value, size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                bgcolor=color,
                padding=20,
                border_radius=10
            ),
            elevation=4
        )

    def build_products_table(self, products):
        """Build products table"""
        if not products:
            return ft.Container(
                content=ft.Text("ยังไม่มีสินค้า", size=16, color=ft.Colors.GREY_600),
                alignment=ft.alignment.center,
                padding=40
            )

        rows = []
        for product in products:
            rows.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                # Product emoji
                                ft.Text(self.get_product_emoji(product), size=32),

                                # Product info
                                ft.Column(
                                    [
                                        ft.Text(product['name'], size=16, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"🏷️ {product['category']}", size=12, color=ft.Colors.GREY_600)
                                    ],
                                    spacing=2,
                                    expand=True
                                ),

                                # Price
                                ft.Text(
                                    f"฿{product['price']:.2f}",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREEN_700
                                ),

                                # Actions
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color=ft.Colors.BLUE_700,
                                            tooltip="แก้ไข",
                                            on_click=lambda e, p=product: self.edit_product(p)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED_700,
                                            tooltip="ลบ",
                                            on_click=lambda e, p=product: self.delete_product(p)
                                        )
                                    ],
                                    spacing=5
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

        return ft.Column(rows, spacing=10, scroll=ft.ScrollMode.AUTO)

    def get_product_emoji(self, product):
        """Get emoji for product"""
        name = product['name'].lower()
        emoji_map = {
            'coffee': '☕', 'tea': '🍵', 'latte': '☕', 'juice': '🧃',
            'sandwich': '🥪', 'croissant': '🥐', 'salad': '🥗', 'burger': '🍔',
            'pizza': '🍕', 'pasta': '🍝', 'rice': '🍚', 'wings': '🍗',
            'cake': '🍰', 'ice cream': '🍦', 'brownie': '🧁'
        }
        for keyword, emoji in emoji_map.items():
            if keyword in name:
                return emoji
        return '🍽️'

    def add_product(self):
        """Add new product - Show dialog"""
        name_field = ft.TextField(label="ชื่อสินค้า", width=300)
        price_field = ft.TextField(label="ราคา", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        category_dropdown = ft.Dropdown(
            label="หมวดหมู่",
            width=300,
            options=[ft.dropdown.Option(cat) for cat in self.app.categories]
        )

        def close_dlg(e):
            add_dlg.open = False
            self.page.update()

        def save_product(e):
            if not name_field.value or not price_field.value or not category_dropdown.value:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("กรุณากรอกข้อมูลให้ครบ"),
                    bgcolor=ft.Colors.RED_700
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

            add_dlg.open = False
            self.page.update()

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ เพิ่มสินค้า '{name_field.value}' สำเร็จ (Demo)"),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.snack_bar.open = True
            self.page.update()

        add_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("➕ เพิ่มสินค้าใหม่", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                name_field,
                price_field,
                category_dropdown
            ], spacing=15, tight=True),
            actions=[
                ft.TextButton("ยกเลิก", on_click=close_dlg),
                ft.ElevatedButton(
                    "บันทึก",
                    on_click=save_product,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE
                )
            ]
        )

        self.page.overlay.append(add_dlg)
        add_dlg.open = True
        self.page.update()

    def edit_product(self, product):
        """Edit product - Show dialog"""
        name_field = ft.TextField(label="ชื่อสินค้า", value=product['name'], width=300)
        price_field = ft.TextField(label="ราคา", value=str(product['price']), width=300, keyboard_type=ft.KeyboardType.NUMBER)
        category_dropdown = ft.Dropdown(
            label="หมวดหมู่",
            value=product['category'],
            width=300,
            options=[ft.dropdown.Option(cat) for cat in self.app.categories]
        )

        def close_dlg(e):
            edit_dlg.open = False
            self.page.update()

        def save_changes(e):
            edit_dlg.open = False
            self.page.update()

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ แก้ไข '{name_field.value}' สำเร็จ (Demo)"),
                bgcolor=ft.Colors.BLUE_700
            )
            self.page.snack_bar.open = True
            self.page.update()

        edit_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"✏️ แก้ไขสินค้า: {product['name']}", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                name_field,
                price_field,
                category_dropdown
            ], spacing=15, tight=True),
            actions=[
                ft.TextButton("ยกเลิก", on_click=close_dlg),
                ft.ElevatedButton(
                    "บันทึกการแก้ไข",
                    on_click=save_changes,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE
                )
            ]
        )

        self.page.overlay.append(edit_dlg)
        edit_dlg.open = True
        self.page.update()

    def delete_product(self, product):
        """Delete product - Show confirmation dialog"""
        def close_dlg(e):
            delete_dlg.open = False
            self.page.update()

        def confirm_delete(e):
            delete_dlg.open = False
            self.page.update()

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ ลบสินค้า '{product['name']}' สำเร็จ (Demo)"),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.snack_bar.open = True
            self.page.update()

        delete_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED_700, size=32),
                ft.Text("ยืนยันการลบ", size=20, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Text(f"คุณต้องการลบสินค้า '{product['name']}' หรือไม่?\nการกระทำนี้ไม่สามารถยกเลิกได้", size=14),
            actions=[
                ft.TextButton("ยกเลิก", on_click=close_dlg),
                ft.ElevatedButton(
                    "ลบ",
                    on_click=confirm_delete,
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE
                )
            ]
        )

        self.page.overlay.append(delete_dlg)
        delete_dlg.open = True
        self.page.update()
