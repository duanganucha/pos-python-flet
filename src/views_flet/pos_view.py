# -*- coding: utf-8 -*-
"""
POS View - Flet Version
Main point of sale interface with products, cart, and checkout
"""
import flet as ft
import os
from datetime import datetime


class POSView:
    def __init__(self, app):
        """Initialize POS view"""
        self.app = app
        self.page = app.page
        self.db = app.db

        # UI Components refs
        self.cart_list = None
        self.subtotal_text = None
        self.tax_text = None
        self.total_text = None
        self.product_grid = None
        self.search_field = None

    def create(self):
        """Create POS view layout"""
        return ft.Row(
            [
                # Left: Products area
                ft.Container(
                    content=ft.Column(
                        [
                            self.build_search_bar(),
                            self.build_category_tabs(),
                            self.build_products_grid()
                        ],
                        spacing=15,
                        scroll=ft.ScrollMode.AUTO
                    ),
                    expand=True,
                    padding=20,
                    bgcolor=ft.Colors.WHITE
                ),

                # Right: Cart sidebar
                self.build_cart_sidebar()
            ],
            spacing=0,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

    def build_search_bar(self):
        """Build search bar"""
        self.search_field = ft.TextField(
            hint_text="ค้นหาสินค้า...",
            border=ft.InputBorder.NONE,
            expand=True,
            on_submit=self.search_products
        )

        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SEARCH, color=ft.Colors.GREY_600),
                    self.search_field,
                    ft.ElevatedButton(
                        "ค้นหา",
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        on_click=self.search_products
                    )
                ],
                spacing=10
            ),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
            bgcolor=ft.Colors.WHITE
        )

    def build_category_tabs(self):
        """Build category tabs"""
        category_buttons = [
            ft.ElevatedButton(
                f"ทั้งหมด ({len(self.app.products)})",
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                on_click=lambda e: self.filter_by_category("All")
            )
        ]

        category_emojis = {
            'Beverages': '🥤', 'Food': '🍽️', 'Desserts': '🍰',
            'Snacks': '🍿', 'Dairy': '🥛', 'Breakfast': '🍳',
            'Soups': '🍲', 'Pasta': '🍝', 'Burgers': '🍔'
        }

        for category in self.app.categories:
            emoji = category_emojis.get(category, '🏷️')
            btn = ft.OutlinedButton(
                f"{emoji} {category}",
                on_click=lambda e, c=category: self.filter_by_category(c),
                style=ft.ButtonStyle(
                    color=ft.Colors.GREY_700,
                    side=ft.BorderSide(1, ft.Colors.GREY_300)
                )
            )
            category_buttons.append(btn)

        return ft.Container(
            content=ft.Row(
                category_buttons,
                spacing=10,
                scroll=ft.ScrollMode.AUTO
            ),
            height=50
        )

    def build_products_grid(self):
        """Build products grid"""
        self.product_grid = ft.GridView(
            runs_count=3,
            max_extent=250,
            child_aspect_ratio=0.9,
            spacing=15,
            run_spacing=15,
            expand=True
        )

        self.display_products()

        return ft.Container(
            content=self.product_grid,
            expand=True
        )

    def display_products(self, products=None):
        """Display products in grid"""
        if products is None:
            if self.app.active_category == "All":
                products = self.app.products
            else:
                products = [p for p in self.app.products if p['category'] == self.app.active_category]

        self.product_grid.controls.clear()

        for product in products:
            self.product_grid.controls.append(
                self.create_product_card(product)
            )

        self.page.update()

    def create_product_card(self, product):
        """Create product card"""
        emoji = self.get_product_emoji(product)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        # Emoji icon
                        ft.Container(
                            content=ft.Text(emoji, size=60),
                            bgcolor=ft.Colors.GREEN_50,
                            border_radius=50,
                            padding=20,
                            alignment=ft.alignment.center
                        ),

                        # Product name
                        ft.Text(
                            product['name'],
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
 
                       

                        # Price
                        ft.Text(
                            f"฿{product['price']:.2f}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_700
                        ),

                        # Add to cart button
                        ft.ElevatedButton(
                            "🛒 เพิ่มลงตะกร้า",
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                            width=200,
                            on_click=lambda e, p=product: self.add_to_cart(p)
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8
                ),
                padding=15
            ),
            elevation=2
        )

    def build_cart_sidebar(self):
        """Build cart sidebar"""
        self.cart_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        self.subtotal_text = ft.Text("฿0.00", size=14)
        self.tax_text = ft.Text("฿0.00", size=14)
        self.total_text = ft.Text("฿0.00", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)

        return ft.Container(
            content=ft.Column(
                [
                    # Cart header
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    "🛒 ตะกร้าสินค้า",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Text(
                                    "โต๊ะ 4",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        bgcolor=ft.Colors.GREEN_700,
                        padding=15,
                        border_radius=ft.border_radius.only(top_left=0, top_right=0)
                    ),

                    # Cart items - Expanded scrollable area
                    ft.Container(
                        content=self.cart_list,
                        padding=15,
                        expand=True
                    ),

                    # Footer section - Always at bottom
                    ft.Container(
                        content=ft.Column(
                            [
                                # Pricing breakdown
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [ft.Text("ราคารวม:", size=14), self.subtotal_text],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            ft.Row(
                                                [ft.Text("ภาษี (7%):", size=14), self.tax_text],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            ft.Divider(),
                                            ft.Row(
                                                [
                                                    ft.Text("ยอดรวมทั้งหมด:", size=16, weight=ft.FontWeight.BOLD),
                                                    self.total_text
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                            )
                                        ],
                                        spacing=10
                                    ),
                                    border=ft.border.all(1, ft.Colors.GREY_300),
                                    border_radius=8,
                                    padding=15,
                                    margin=ft.margin.only(bottom=15)
                                ),

                                # Payment method selector
                                self.build_payment_selector(),

                                # Action buttons
                                ft.Column(
                                    [
                                        ft.OutlinedButton(
                                            "🗑️ ล้างตะกร้า",
                                            width=float('inf'),
                                            on_click=self.clear_cart
                                        ),
                                        ft.ElevatedButton(
                                            "✅ สั่งซื้อและชำระเงิน",
                                            width=float('inf'),
                                            bgcolor=ft.Colors.GREEN_700,
                                            color=ft.Colors.WHITE,
                                            height=50,
                                            on_click=self.checkout
                                        )
                                    ],
                                    spacing=10
                                )
                            ],
                            spacing=0
                        ),
                        padding=ft.padding.only(left=15, right=15, bottom=15)
                    )
                ],
                spacing=0
            ),
            width=450,
            bgcolor=ft.Colors.GREY_50
        )

    def build_payment_selector(self):
        """Build payment method selector"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "💳 วิธีการชำระเงิน:",
                        size=14,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.RadioGroup(
                        content=ft.Row(
                            [
                                ft.Radio(value="Cash", label="💵 เงินสด"),
                                ft.Radio(value="Card", label="💳 บัตร"),
                                ft.Radio(value="QR", label="📱 QR Code")
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        value="Cash",
                        on_change=self.on_payment_method_change
                    )
                ],
                spacing=10
            ),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=15,
            margin=ft.margin.only(bottom=15)
        )

    def get_product_emoji(self, product):
        """Get emoji for product"""
        name = product['name'].lower()
        category = product.get('category', '').lower()

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

    def filter_by_category(self, category):
        """Filter products by category"""
        self.app.active_category = category
        self.display_products()

    def search_products(self, e=None):
        """Search products"""
        query = self.search_field.value.lower()
        if query:
            products = [p for p in self.app.products if query in p['name'].lower()]
            self.display_products(products)
        else:
            self.display_products()

    def add_to_cart(self, product):
        """Add product to cart"""
        for item in self.app.cart:
            if item['id'] == product['id']:
                item['qty'] += 1
                item['total'] = item['price'] * item['qty']
                self.update_cart_display()
                return

        self.app.cart.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'category': product['category'],
            'qty': 1,
            'total': product['price']
        })

        self.update_cart_display()

    def update_cart_display(self):
        """Update cart display"""
        self.cart_list.controls.clear()

        self.app.subtotal = 0

        for item in self.app.cart:
            emoji = self.get_product_emoji(item)

            self.cart_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                # Large emoji icon
                                ft.Text(emoji, size=28),
                                # Item details
                                ft.Column(
                                    [
                                        ft.Text(item['name'], size=13, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"฿{item['price']:.2f} × {item['qty']}", size=11, color=ft.Colors.GREY_700)
                                    ],
                                    spacing=2,
                                    expand=True
                                ),
                                # Total price
                                ft.Text(f"฿{item['total']:.2f}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=12
                        ),
                        padding=12
                    )
                )
            )

            self.app.subtotal += item['total']

        # Calculate tax and total
        self.app.tax = self.app.subtotal * 0.07
        self.app.total = self.app.subtotal + self.app.tax

        # Update text displays
        self.subtotal_text.value = f"฿{self.app.subtotal:.2f}"
        self.tax_text.value = f"฿{self.app.tax:.2f}"
        self.total_text.value = f"฿{self.app.total:.2f}"

        self.page.update()

    def on_payment_method_change(self, e):
        """Handle payment method change"""
        self.app.payment_method = e.control.value

    def clear_cart(self, e):
        """Clear cart"""
        self.app.cart.clear()
        self.update_cart_display()

    def checkout(self, e):
        """Process checkout - Show payment dialog"""
        if not self.app.cart:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("กรุณาเพิ่มสินค้าในตะกร้า"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Show payment dialog with numpad
        self.show_payment_dialog()

    def show_payment_dialog(self):
        """Show payment dialog with numpad"""
        # Cash received input state
        self.cash_received = 0

        # Create refs for dynamic updates
        cash_display_ref = ft.Ref[ft.Text]()
        change_display_ref = ft.Ref[ft.Text]()
        confirm_btn_ref = ft.Ref[ft.ElevatedButton]()

        def update_cash_display():
            """Update cash and change displays"""
            cash_display_ref.current.value = f"฿{self.cash_received:.2f}"
            change_amount = self.cash_received - self.app.total

            if change_amount >= 0:
                change_display_ref.current.value = f"฿{change_amount:.2f}"
                change_display_ref.current.color = ft.Colors.GREEN_700
                confirm_btn_ref.current.disabled = False
            else:
                change_display_ref.current.value = f"฿{change_amount:.2f}"
                change_display_ref.current.color = ft.Colors.RED_700
                confirm_btn_ref.current.disabled = True

            self.page.update()

        def on_numpad_click(number):
            """Handle numpad button click"""
            if number == "clear":
                self.cash_received = 0
            elif number == "backspace":
                self.cash_received = int(self.cash_received / 10)
            else:
                self.cash_received = self.cash_received * 10 + number
            update_cash_display()

        def on_quick_amount(amount):
            """Handle quick amount button click"""
            if amount == "exact":
                self.cash_received = self.app.total
            else:
                self.cash_received = amount
            update_cash_display()

        def confirm_payment(e):
            """Confirm payment and save receipt"""
            payment_dialog.open = False
            self.page.update()

            # Save to database
            try:
                receipt_id = self.db.save_receipt(
                    cart=self.app.cart,
                    total=self.app.total,
                    cash_received=self.cash_received,
                    change=self.cash_received - self.app.total
                )

                # Show receipt dialog
                self.show_receipt_dialog(receipt_id, self.cash_received, self.cash_received - self.app.total)

                # Clear cart
                self.app.cart.clear()
                self.update_cart_display()

            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ เกิดข้อผิดพลาด: {str(ex)}"),
                    bgcolor=ft.Colors.RED_700
                )
                self.page.snack_bar.open = True
                self.page.update()

        # Build numpad buttons
        numpad_buttons = []
        for row in [[7, 8, 9], [4, 5, 6], [1, 2, 3], [0, "clear", "backspace"]]:
            row_buttons = []
            for num in row:
                if num == "clear":
                    btn = ft.ElevatedButton(
                        "C",
                        on_click=lambda e, n=num: on_numpad_click(n),
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                        height=60
                    )
                elif num == "backspace":
                    btn = ft.ElevatedButton(
                        "⌫",
                        on_click=lambda e, n=num: on_numpad_click(n),
                        bgcolor=ft.Colors.ORANGE_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                        height=60
                    )
                else:
                    btn = ft.ElevatedButton(
                        str(num),
                        on_click=lambda e, n=num: on_numpad_click(n),
                        bgcolor=ft.Colors.GREY_300,
                        color=ft.Colors.BLACK,
                        expand=True,
                        height=60
                    )
                row_buttons.append(btn)
            numpad_buttons.append(ft.Row(row_buttons, spacing=10))

        # Quick amount buttons
        quick_amounts = [
            ("฿20", 20),
            ("฿50", 50),
            ("฿100", 100),
            ("฿500", 500),
            ("฿1000", 1000),
            ("พอดี", "exact")
        ]

        quick_buttons = []
        for label, amount in quick_amounts:
            btn = ft.OutlinedButton(
                label,
                on_click=lambda e, a=amount: on_quick_amount(a),
                style=ft.ButtonStyle(
                    color=ft.Colors.GREEN_700,
                    side=ft.BorderSide(1, ft.Colors.GREEN_700)
                ),
                expand=True
            )
            quick_buttons.append(btn)

        # Payment dialog
        payment_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("💰 รับชำระเงิน", size=24, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    # Total amount
                    ft.Container(
                        content=ft.Column([
                            ft.Text("ยอดที่ต้องชำระ", size=14, color=ft.Colors.GREY_700),
                            ft.Text(f"฿{self.app.total:.2f}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREEN_50,
                        padding=15,
                        border_radius=10,
                        expand=True   
                    ),

                    # Cash received and Change
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("เงินที่รับ", size=14, color=ft.Colors.GREY_700),
                                    ft.Text("฿0.00", size=28, weight=ft.FontWeight.BOLD, ref=cash_display_ref)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                bgcolor=ft.Colors.BLUE_50,
                                padding=15,
                                border_radius=10,
                                expand=True  # Make this container expand to fill available space
                            ),

                            ft.Container(
                                content=ft.Column([
                                    ft.Text("เงินทอน", size=14, color=ft.Colors.GREY_700),
                                    ft.Text("฿0.00", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700, ref=change_display_ref)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                bgcolor=ft.Colors.GREY_100,
                                padding=15,
                                border_radius=10,
                                expand=True  # Make this container expand to fill available space
                            )
                        ],
                        spacing=10,
                        expand=True  # Make the row expand to fill available space
                    ),

                    # Quick amount buttons
                    ft.Text("จำนวนเงินด่วน", size=14, weight=ft.FontWeight.BOLD),
                    ft.Row(quick_buttons[:3], spacing=5),
                    ft.Row(quick_buttons[3:], spacing=5),

                    # Numpad
                    ft.Text("ป้อนจำนวนเงิน", size=14, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column(numpad_buttons, spacing=10),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10
                    )
                ], spacing=15, scroll=ft.ScrollMode.AUTO),
                width=450,
                height=700
            ),
            actions=[
                ft.TextButton("❌ ยกเลิก", on_click=lambda e: self.close_dialog(payment_dialog)),
                ft.ElevatedButton(
                    "✅ ยืนยันการชำระเงิน",
                    on_click=confirm_payment,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE,
                    disabled=True,
                    ref=confirm_btn_ref
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        # Store dialog as instance variable to prevent garbage collection
        self.payment_dialog = payment_dialog
        self.page.overlay.append(self.payment_dialog)
        self.payment_dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        """Close dialog"""
        dialog.open = False
        self.page.update()

    def show_receipt_dialog(self, receipt_id, cash_received, change):
        """Show receipt dialog with transaction details"""
        # Build items list
        items_list = []
        for item in self.app.cart:
            items_list.append(
                ft.Row([
                    ft.Text(f"{item['qty']}x", size=12, width=40),
                    ft.Text(item['name'], size=12, expand=True),
                    ft.Text(f"฿{item['total']:.2f}", size=12, weight=ft.FontWeight.BOLD)
                ])
            )

        # Receipt dialog
        receipt_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_700, size=32),
                ft.Text("ชำระเงินสำเร็จ!", size=24, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Container(
                content=ft.Column([
                    # Receipt ID
                    ft.Container(
                        content=ft.Column([
                            ft.Text("รหัสใบเสร็จ", size=12, color=ft.Colors.GREY_700),
                            ft.Text(f"#{receipt_id}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREEN_50,
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
                        ft.Text(f"฿{self.app.subtotal:.2f}", size=14, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text("ภาษี 7%", size=14),
                        ft.Text(f"฿{self.app.tax:.2f}", size=14, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text("ยอดชำระ", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"฿{self.app.total:.2f}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Divider(),

                    # Payment details
                    ft.Row([
                        ft.Text("เงินที่รับ", size=14),
                        ft.Text(f"฿{cash_received:.2f}", size=14, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text("เงินทอน", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"฿{change:.2f}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ], spacing=10, scroll=ft.ScrollMode.AUTO),
                width=400,
                height=500
            ),
            actions=[
                ft.TextButton("ปิด", on_click=lambda e: self.close_dialog(receipt_dialog)),
                ft.ElevatedButton(
                    "🖨️ พิมพ์ใบเสร็จ",
                    on_click=lambda e: self.print_receipt(receipt_id, cash_received, change, receipt_dialog),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        # Store dialog as instance variable
        self.receipt_dialog = receipt_dialog
        self.page.overlay.append(self.receipt_dialog)
        self.receipt_dialog.open = True
        self.page.update()

    def print_receipt(self, receipt_id, cash_received, change, dialog):
        """Print receipt to file"""
        # Create receipts directory if not exists
        os.makedirs("data/receipts", exist_ok=True)

        # Generate receipt filename
        filename = f"data/receipts/receipt_{receipt_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        # Build receipt content
        receipt_content = f"""
========================================
          🍽️ CHILI POS SYSTEM
========================================
Receipt ID: #{receipt_id}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Payment Method: {self.app.payment_method}
========================================

ITEMS:
----------------------------------------
"""

        for item in self.app.cart:
            receipt_content += f"{item['qty']}x {item['name']:<20} ฿{item['total']:>8.2f}\n"

        receipt_content += f"""
----------------------------------------
Subtotal:                  ฿{self.app.subtotal:>8.2f}
Tax (7%):                  ฿{self.app.tax:>8.2f}
----------------------------------------
TOTAL:                     ฿{self.app.total:>8.2f}
========================================

PAYMENT:
Cash Received:             ฿{cash_received:>8.2f}
Change:                    ฿{change:>8.2f}

========================================
        Thank you for your order!
           Please come again!
========================================
"""

        # Write to file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(receipt_content)

            # Show success message
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ บันทึกใบเสร็จที่: {filename}"),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.snack_bar.open = True

            # Close dialog
            dialog.open = False
            self.page.update()

        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ เกิดข้อผิดพลาด: {str(ex)}"),
                bgcolor=ft.Colors.RED_700
            )
            self.page.snack_bar.open = True
            self.page.update()
