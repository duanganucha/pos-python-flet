# -*- coding: utf-8 -*-
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime
import os

class POSView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)

        # UI elements that need to be accessed
        self.products_canvas = None
        self.products_frame = None
        self.canvas_window = None
        self.search_var = None
        self.cart_tree = None
        self.total_label = None
        self.subtotal_label = None
        self.tax_label = None
        self.payment_method = ttk.StringVar(value="Cash")

    def create(self):
        """Create POS view (original main view)"""
        # Left Panel - Products
        left_panel = ttk.Frame(self.frame)
        left_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 5))

        # Products header with modern design
        header_frame = ttk.Frame(left_panel)
        header_frame.pack(fill=X, pady=(0, 15))

        products_header = ttk.Label(
            header_frame,
            text="🍽️ เมนูอาหาร",
            font=("Helvetica", 22, "bold"),
            bootstyle="success"
        )
        products_header.pack(side=LEFT)

        # Enhanced search bar with icon
        search_frame = ttk.Frame(left_panel, bootstyle="light", relief="solid", borderwidth=1)
        search_frame.pack(fill=X, pady=(0, 15))

        search_inner = ttk.Frame(search_frame, padding=5)
        search_inner.pack(fill=X)

        ttk.Label(
            search_inner,
            text="🔍",
            font=("Segoe UI Emoji", 16)
        ).pack(side=LEFT, padx=(5, 5))

        self.search_var = ttk.StringVar()
        search_entry = ttk.Entry(
            search_inner,
            textvariable=self.search_var,
            font=("Helvetica", 13)
        )
        search_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 8))

        # Bind Enter key to search
        search_entry.bind('<Return>', lambda e: self.search_products())

        search_btn = ttk.Button(
            search_inner,
            text="ค้นหา",
            bootstyle="success",
            command=self.search_products
        )
        search_btn.pack(side=RIGHT, ipady=5, ipadx=15)

        # Category tabs
        category_tabs_frame = ttk.Frame(left_panel)
        category_tabs_frame.pack(fill=X, pady=(0, 10))

        # Create scrollable frame for category tabs
        canvas_tabs = ttk.Canvas(category_tabs_frame, height=50)
        scrollbar_tabs = ttk.Scrollbar(category_tabs_frame, orient=HORIZONTAL, command=canvas_tabs.xview)
        tabs_inner_frame = ttk.Frame(canvas_tabs)

        tabs_inner_frame.bind(
            "<Configure>",
            lambda e: canvas_tabs.configure(scrollregion=canvas_tabs.bbox("all"))
        )

        canvas_tabs.create_window((0, 0), window=tabs_inner_frame, anchor="nw")
        canvas_tabs.configure(xscrollcommand=scrollbar_tabs.set)

        canvas_tabs.pack(side=TOP, fill=X)
        scrollbar_tabs.pack(side=BOTTOM, fill=X)

        # Add "All" category button with count
        all_count = len(self.app.products)
        all_btn = ttk.Button(
            tabs_inner_frame,
            text=f"ทั้งหมด ({all_count})",
            bootstyle="success",
            command=lambda: self.filter_by_category("All")
        )
        all_btn.pack(side=LEFT, padx=4, ipady=10, ipadx=18)
        self.app.category_buttons["All"] = all_btn

        # Add category buttons with emoji icons
        category_emojis = {
            'Beverages': '🥤',
            'Food': '🍽️',
            'Desserts': '🍰',
            'Snacks': '🍿',
            'Dairy': '🥛',
            'Breakfast': '🍳',
            'Soups': '🍲',
            'Pasta': '🍝',
            'Main Course': '🍖',
            'Burgers': '🍔',
            'Drinks': '☕'
        }

        for category in self.app.categories:
            emoji = category_emojis.get(category, '🏷️')
            cat_btn = ttk.Button(
                tabs_inner_frame,
                text=f"{emoji} {category}",
                bootstyle="light-outline",
                command=lambda c=category: self.filter_by_category(c)
            )
            cat_btn.pack(side=LEFT, padx=4, ipady=10, ipadx=18)
            self.app.category_buttons[category] = cat_btn

        # Products grid
        products_container = ttk.Frame(left_panel)
        products_container.pack(fill=BOTH, expand=YES)

        # Scrollable frame for products
        self.products_canvas = ttk.Canvas(products_container)
        scrollbar = ttk.Scrollbar(products_container, orient=VERTICAL, command=self.products_canvas.yview)
        self.products_frame = ttk.Frame(self.products_canvas)

        self.products_frame.bind(
            "<Configure>",
            lambda e: self.products_canvas.configure(scrollregion=self.products_canvas.bbox("all"))
        )

        self.canvas_window = self.products_canvas.create_window((0, 0), window=self.products_frame, anchor="nw")
        self.products_canvas.configure(yscrollcommand=scrollbar.set)

        # Bind canvas resize to update width and redraw products
        self.products_canvas.bind("<Configure>", self.on_products_canvas_configure)

        self.products_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.display_products()

        # Right Panel - Cart and Checkout (Chili Pos style)
        right_panel = ttk.Frame(self.frame, width=480, bootstyle="light")
        right_panel.pack(side=RIGHT, fill=BOTH, padx=(8, 0))
        right_panel.pack_propagate(False)

        # Cart header with table number
        cart_header_frame = ttk.Frame(right_panel, bootstyle="success", padding=12)
        cart_header_frame.pack(fill=X, pady=(0, 10))

        ttk.Label(
            cart_header_frame,
            text="🛒 ตะกร้าสินค้า",
            font=("Helvetica", 20, "bold"),
            bootstyle="inverse-success"
        ).pack(side=LEFT)

        ttk.Label(
            cart_header_frame,
            text="โต๊ะ 4",
            font=("Helvetica", 16, "bold"),
            bootstyle="inverse-success"
        ).pack(side=RIGHT)

        # Cart items
        cart_frame = ttk.Frame(right_panel)
        cart_frame.pack(fill=BOTH, expand=YES, pady=(0, 10))

        # Cart treeview
        columns = ("รายการ", "ราคา", "จำนวน", "รวม")

        # Configure custom treeview style before creating the widget
        cart_style = ttk.Style()
        cart_style.configure("Cart.Treeview",
                           font=("Segoe UI Emoji", 11),
                           rowheight=40)
        cart_style.configure("Cart.Treeview.Heading",
                           font=("Helvetica", 12, "bold"))

        self.cart_tree = ttk.Treeview(
            cart_frame,
            columns=columns,
            show="headings",
            height=8,
            bootstyle="info",
            style="Cart.Treeview"
        )

        for col in columns:
            self.cart_tree.heading(col, text=col)

        self.cart_tree.column("รายการ", width=190)
        self.cart_tree.column("ราคา", width=80)
        self.cart_tree.column("จำนวน", width=60)
        self.cart_tree.column("รวม", width=90)

        cart_scrollbar = ttk.Scrollbar(
            cart_frame,
            orient=VERTICAL,
            command=self.cart_tree.yview
        )
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)

        self.cart_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        cart_scrollbar.pack(side=RIGHT, fill=Y)

        # Remove button
        remove_btn = ttk.Button(
            right_panel,
            text="🗑️ ลบรายการที่เลือก",
            bootstyle="danger-outline",
            command=self.remove_from_cart
        )
        remove_btn.pack(fill=X, pady=(0, 12), ipady=8)

        # Pricing breakdown (Chili Pos style)
        pricing_frame = ttk.Frame(right_panel, bootstyle="light", relief="solid", borderwidth=1, padding=15)
        pricing_frame.pack(fill=X, pady=(0, 12))

        # Subtotal
        subtotal_row = ttk.Frame(pricing_frame)
        subtotal_row.pack(fill=X, pady=3)

        ttk.Label(
            subtotal_row,
            text="ราคารวม:",
            font=("Helvetica", 12)
        ).pack(side=LEFT)

        self.subtotal_label = ttk.Label(
            subtotal_row,
            text="฿0.00",
            font=("Helvetica", 12)
        )
        self.subtotal_label.pack(side=RIGHT)

        # Tax
        tax_row = ttk.Frame(pricing_frame)
        tax_row.pack(fill=X, pady=3)

        ttk.Label(
            tax_row,
            text="ภาษี (7%):",
            font=("Helvetica", 12)
        ).pack(side=LEFT)

        self.tax_label = ttk.Label(
            tax_row,
            text="฿0.00",
            font=("Helvetica", 12)
        )
        self.tax_label.pack(side=RIGHT)

        # Separator
        ttk.Separator(pricing_frame, orient=HORIZONTAL).pack(fill=X, pady=8)

        # Total Amount
        total_row = ttk.Frame(pricing_frame)
        total_row.pack(fill=X, pady=3)

        ttk.Label(
            total_row,
            text="ยอดรวมทั้งหมด:",
            font=("Helvetica", 16, "bold")
        ).pack(side=LEFT)

        self.total_label = ttk.Label(
            total_row,
            text="฿0.00",
            font=("Helvetica", 16, "bold"),
            bootstyle="success"
        )
        self.total_label.pack(side=RIGHT)

        # Payment method selector (Chili Pos style) - Expanded height
        payment_frame = ttk.Frame(right_panel, bootstyle="light", relief="solid", borderwidth=1, padding=15)
        payment_frame.pack(fill=X, pady=(0, 15))

        ttk.Label(
            payment_frame,
            text="💳 วิธีการชำระเงิน:",
            font=("Helvetica", 13, "bold")
        ).pack(anchor=W, pady=(0, 12))

        payment_methods_frame = ttk.Frame(payment_frame)
        payment_methods_frame.pack(fill=X)

        # Configure payment button style for larger buttons
        payment_style = ttk.Style()
        payment_style.configure("Payment.TButton", font=("Helvetica", 12, "bold"))

        # Cash button - Expanded height
        cash_btn = ttk.Radiobutton(
            payment_methods_frame,
            text="💵\nเงินสด",
            variable=self.payment_method,
            value="Cash",
            bootstyle="success-outline-toolbutton"
        )
        cash_btn.pack(side=LEFT, fill=X, expand=YES, padx=(0, 6), ipady=20)

        # Credit/Debit Card button - Expanded height
        card_btn = ttk.Radiobutton(
            payment_methods_frame,
            text="💳\nบัตร",
            variable=self.payment_method,
            value="Card",
            bootstyle="success-outline-toolbutton"
        )
        card_btn.pack(side=LEFT, fill=X, expand=YES, padx=3, ipady=20)

        # QR Code button - Expanded height
        qr_btn = ttk.Radiobutton(
            payment_methods_frame,
            text="📱\nQR Code",
            variable=self.payment_method,
            value="QR",
            bootstyle="success-outline-toolbutton"
        )
        qr_btn.pack(side=LEFT, fill=X, expand=YES, padx=(6, 0), ipady=20)

        # Action buttons
        btn_frame = ttk.Frame(right_panel)
        btn_frame.pack(fill=X)

        # Clear cart button
        clear_btn = ttk.Button(
            btn_frame,
            text="🗑️ ล้างตะกร้า",
            bootstyle="warning-outline",
            command=self.clear_cart
        )
        clear_btn.pack(fill=X, pady=(0, 10), ipady=12)

        # Place Order button (green - primary action like Chili Pos)
        checkout_btn = ttk.Button(
            btn_frame,
            text="✅ สั่งซื้อและชำระเงิน",
            bootstyle="success",
            command=self.checkout
        )
        checkout_btn.pack(fill=X, ipady=16)

        # Configure larger font for checkout button
        checkout_style = ttk.Style()
        checkout_style.configure("Checkout.TButton", font=("Helvetica", 14, "bold"))

        # Store references in app for access from other methods
        self.app.products_canvas = self.products_canvas
        self.app.products_frame = self.products_frame
        self.app.canvas_window = self.canvas_window
        self.app.search_var = self.search_var
        self.app.cart_tree = self.cart_tree
        self.app.total_label = self.total_label

        return self.frame

    def calculate_columns(self):
        """Calculate number of columns based on canvas width"""
        canvas_width = self.products_canvas.winfo_width()
        if canvas_width <= 1:
            return 3  # Default for initial display

        # Minimum card width: 220px (increased for larger content)
        min_card_width = 220
        cols = max(1, canvas_width // min_card_width)
        return min(cols, 6)  # Max 6 columns

    def on_products_canvas_configure(self, event):
        """Handle canvas resize event - update width and redraw products"""
        # Update the frame width to match canvas width
        canvas_width = event.width
        self.products_canvas.itemconfig(self.canvas_window, width=canvas_width)

        # Redraw products with new column calculation
        if self.app.current_products is not None:
            self.display_products(self.app.current_products)

    def get_product_emoji(self, product):
        """Get emoji icon for product based on name or category"""
        name = product['name'].lower()
        category = product['category'].lower()

        # Specific product emojis
        emoji_map = {
            'coffee': '☕', 'tea': '🍵', 'latte': '☕', 'cappuccino': '☕',
            'espresso': '☕', 'juice': '🧃', 'smoothie': '🥤', 'chocolate': '🍫',
            'water': '💧', 'soda': '🥤', 'lemonade': '🍋', 'energy': '⚡',
            'sandwich': '🥪', 'croissant': '🥐', 'salad': '🥗', 'burger': '🍔',
            'pizza': '🍕', 'pasta': '🍝', 'spaghetti': '🍝', 'rice': '🍚',
            'thai': '🍜', 'wings': '🍗', 'chicken': '🍗', 'fries': '🍟',
            'onion': '🧅', 'steak': '🥩', 'fish': '🐟', 'taco': '🌮',
            'burrito': '🌯', 'quesadilla': '🫔', 'cake': '🍰', 'cheesecake': '🍰',
            'ice cream': '🍦', 'brownie': '🧁', 'tiramisu': '🍰', 'pie': '🥧',
            'donut': '🍩', 'muffin': '🧁', 'chips': '🍟', 'cookie': '🍪',
            'pretzels': '🥨', 'popcorn': '🍿', 'nachos': '🌮', 'granola': '🥜',
            'candy': '🍬', 'trail': '🥜', 'protein': '🍫', 'yogurt': '🥛',
            'milk': '🥛', 'cheese': '🧀', 'butter': '🧈'
        }

        # Check for specific keywords in product name
        for keyword, emoji in emoji_map.items():
            if keyword in name:
                return emoji

        # Category-based fallback
        category_emoji = {
            'beverages': '🥤',
            'food': '🍽️',
            'desserts': '🍰',
            'snacks': '🍿',
            'dairy': '🥛'
        }

        return category_emoji.get(category, '🛒')

    def display_products(self, products=None):
        """Display products in responsive grid layout"""
        # Clear existing products
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        if products is None:
            products = self.app.products

        # Store current products for resize
        self.app.current_products = products

        # Calculate responsive columns
        cols = self.calculate_columns()

        # Display products in a grid
        for idx, product in enumerate(products):
            row = idx // cols
            col = idx % cols

            product_card = ttk.Frame(
                self.products_frame,
                bootstyle="light",
                relief="raised",
                borderwidth=1
            )
            product_card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            # Inner container with padding
            card_inner = ttk.Frame(product_card, padding=12)
            card_inner.pack(fill=BOTH, expand=YES)

            # Product emoji icon with circular background
            icon_frame = ttk.Frame(card_inner, bootstyle="success", relief="flat")
            icon_frame.pack(pady=(0, 10))

            emoji = self.get_product_emoji(product)
            emoji_label = ttk.Label(
                icon_frame,
                text=emoji,
                font=("Segoe UI Emoji", 52),
                padding=15
            )
            emoji_label.pack()

            # Product name
            name_label = ttk.Label(
                card_inner,
                text=product["name"],
                font=("Helvetica", 13, "bold"),
                wraplength=180
            )
            name_label.pack(pady=(0, 5))

            # Category badge
            category_frame = ttk.Frame(card_inner)
            category_frame.pack(pady=(0, 8))

            category_label = ttk.Label(
                category_frame,
                text=f"🏷️ {product['category']}",
                font=("Helvetica", 9),
                bootstyle="secondary"
            )
            category_label.pack()

            # Rating stars (simulated - you can make this dynamic later)
            rating_frame = ttk.Frame(card_inner)
            rating_frame.pack(pady=(0, 8))

            rating_label = ttk.Label(
                rating_frame,
                text="⭐⭐⭐⭐⭐",
                font=("Segoe UI Emoji", 9)
            )
            rating_label.pack()

            # Product price - prominent
            price_label = ttk.Label(
                card_inner,
                text=f"฿{product['price']:.2f}",
                font=("Helvetica", 18, "bold"),
                bootstyle="success"
            )
            price_label.pack(pady=(0, 12))

            # Add to Cart button - green like Chili Pos
            add_btn = ttk.Button(
                card_inner,
                text="🛒 เพิ่มลงตะกร้า",
                bootstyle="success",
                command=lambda p=product: self.add_to_cart(p)
            )
            add_btn.pack(fill=X, ipady=10)

        # Configure grid weights to distribute space evenly
        for i in range(cols):
            self.products_frame.columnconfigure(i, weight=1, uniform="cols")

        # Configure row weights
        num_rows = (len(products) + cols - 1) // cols
        for i in range(num_rows):
            self.products_frame.rowconfigure(i, weight=0)

    def filter_by_category(self, category):
        """Filter products by category with Chili Pos styling"""
        self.app.active_category = category

        # Update button styles to highlight active category (green theme)
        for cat_name, btn in self.app.category_buttons.items():
            if cat_name == category:
                btn.configure(bootstyle="success")  # Green for active (Chili Pos style)
            else:
                btn.configure(bootstyle="light-outline")  # Light outline for inactive

        # Clear search box when switching categories
        self.search_var.set("")

        # Get filtered products
        if category == "All":
            products = self.app.products
        else:
            try:
                products = self.app.db.get_products_by_category(category)
            except Exception as e:
                print(f"Error filtering by category: {e}")
                products = []

        self.display_products(products)

    def search_products(self):
        """Search products by name using database"""
        search_term = self.search_var.get()
        if search_term:
            try:
                # Search all products
                filtered = self.app.db.search_products(search_term)

                # If a category is active, further filter by category
                if self.app.active_category != "All":
                    filtered = [p for p in filtered if p['category'] == self.app.active_category]

                self.display_products(filtered)
            except Exception as e:
                print(f"Error searching products: {e}")
                self.display_products([])
        else:
            # If search is empty, show products based on active category
            self.filter_by_category(self.app.active_category)

    def add_to_cart(self, product):
        """Add product to cart"""
        # Check if item already in cart
        for item in self.app.cart:
            if item["id"] == product["id"]:
                item["qty"] += 1
                item["total"] = item["qty"] * item["price"]
                self.update_cart_display()
                return

        # Add new item to cart (store full product info for emoji)
        cart_item = {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "category": product["category"],
            "qty": 1,
            "total": product["price"]
        }
        self.app.cart.append(cart_item)
        self.update_cart_display()

    def remove_from_cart(self):
        """Remove selected item from cart"""
        selection = self.cart_tree.selection()
        if selection:
            # Get the index of selected item in treeview
            tree_item_id = selection[0]
            item_index = self.cart_tree.index(tree_item_id)

            # Remove from cart by index
            if 0 <= item_index < len(self.app.cart):
                self.app.cart.pop(item_index)
                self.update_cart_display()

    def update_cart_display(self):
        """Update cart treeview and total with tax calculation (Chili Pos style)"""
        # Clear cart display
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        # Calculate subtotal
        subtotal = 0
        for item in self.app.cart:
            # Get emoji for the product
            emoji = self.get_product_emoji(item)
            item_name_with_emoji = f"{emoji} {item['name']}"

            self.cart_tree.insert("", END, values=(
                item_name_with_emoji,
                f"฿{item['price']:.2f}",
                item["qty"],
                f"฿{item['total']:.2f}"
            ))
            subtotal += item["total"]

        # Calculate tax (7% like in Chili Pos example)
        tax = subtotal * 0.07

        # Calculate total
        self.app.total = subtotal + tax

        # Update labels
        self.subtotal_label.config(text=f"฿{subtotal:.2f}")
        self.tax_label.config(text=f"฿{tax:.2f}")
        self.total_label.config(text=f"฿{self.app.total:.2f}")

    def clear_cart(self):
        """Clear all items from cart"""
        if self.app.cart:
            result = Messagebox.yesno(
                "Clear Cart",
                "Are you sure you want to clear the cart?",
                parent=self.app.root
            )
            if result == "Yes":
                self.app.cart = []
                self.update_cart_display()

    def checkout(self):
        """Process checkout - show payment dialog"""
        if not self.app.cart:
            Messagebox.show_warning(
                "Empty Cart",
                "Please add items to cart before checkout.",
                parent=self.app.root
            )
            return

        # Show payment dialog
        self.show_payment_dialog()

    def show_payment_dialog(self):
        """Show payment dialog with modern design"""
        dialog = ttk.Toplevel(self.app.root)
        dialog.title("ชำระเงิน - Payment")
        dialog.geometry("800x850")
        dialog.resizable(True, True)

        # Center the window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Make dialog modal
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Cash amount variable
        cash_amount = ttk.StringVar(value="0")

        # Main container with gradient-like sections
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Header section with modern design
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 15))

        ttk.Label(
            header_frame,
            text="ชำระเงิน",
            font=("Helvetica", 32, "bold"),
            bootstyle="inverse-primary"
        ).pack(fill=X, pady=10)

        # Total amount - Large and prominent
        total_display = ttk.Frame(main_frame, bootstyle="success")
        total_display.pack(fill=X, pady=(0, 15))

        total_inner = ttk.Frame(total_display, padding=20)
        total_inner.pack(fill=X)

        ttk.Label(
            total_inner,
            text="ยอดรวม",
            font=("Helvetica", 14, "bold"),
            bootstyle="inverse-success"
        ).pack()

        ttk.Label(
            total_inner,
            text=f"฿{self.app.total:,.2f}",
            font=("Helvetica", 48, "bold"),
            bootstyle="inverse-success"
        ).pack(pady=(5, 0))

        # Cash input with modern card design
        input_card = ttk.Frame(main_frame, relief="flat")
        input_card.pack(fill=X, pady=(0, 12))

        ttk.Label(
            input_card,
            text="💵 รับเงินมา",
            font=("Helvetica", 13, "bold")
        ).pack(anchor=W, pady=(0, 5))

        cash_display_frame = ttk.Frame(input_card, bootstyle="info", relief="solid", borderwidth=2)
        cash_display_frame.pack(fill=X)

        cash_display = ttk.Label(
            cash_display_frame,
            textvariable=cash_amount,
            font=("Helvetica", 36, "bold"),
            bootstyle="inverse-info",
            anchor=CENTER,
            padding=15
        )
        cash_display.pack(fill=X)

        # Content area - Compact layout
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=YES, pady=(0, 12))

        # Left side - Numpad (compact)
        numpad_card = ttk.Frame(content_frame)
        numpad_card.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 8))

        numpad_frame = ttk.Frame(numpad_card)
        numpad_frame.pack(fill=BOTH, expand=YES)

        # Numpad functions
        def add_digit(digit):
            current = cash_amount.get()
            if current == "0":
                cash_amount.set(digit)
            else:
                cash_amount.set(current + digit)
            update_change()

        def clear_amount():
            cash_amount.set("0")
            update_change()

        def backspace():
            current = cash_amount.get()
            if len(current) > 1:
                cash_amount.set(current[:-1])
            else:
                cash_amount.set("0")
            update_change()

        def add_double_zero():
            current = cash_amount.get()
            if current == "0":
                cash_amount.set("00")
            else:
                cash_amount.set(current + "00")
            update_change()

        # Numpad buttons (3x4 grid) - Compact
        numpad_buttons = [
            ('7', '8', '9'),
            ('4', '5', '6'),
            ('1', '2', '3'),
            ('C', '0', '⌫')
        ]

        # Configure numpad button style for larger text
        numpad_style = ttk.Style()
        numpad_style.configure("Numpad.TButton", font=("Helvetica", 18, "bold"))

        for row_idx, row in enumerate(numpad_buttons):
            for col_idx, btn_text in enumerate(row):
                if btn_text == 'C':
                    cmd = clear_amount
                    style = "danger"
                elif btn_text == '⌫':
                    cmd = backspace
                    style = "warning"
                else:
                    cmd = lambda d=btn_text: add_digit(d)
                    style = "secondary"

                btn = ttk.Button(
                    numpad_frame,
                    text=btn_text,
                    bootstyle=style,
                    command=cmd
                )
                btn.configure(style="Numpad.TButton")
                btn.grid(row=row_idx, column=col_idx, padx=3, pady=3, sticky="nsew", ipady=18)

        # 00 button
        btn_00 = ttk.Button(
            numpad_frame,
            text="00",
            bootstyle="secondary",
            command=add_double_zero
        )
        btn_00.configure(style="Numpad.TButton")
        btn_00.grid(row=4, column=0, columnspan=3, padx=3, pady=3, sticky="ew", ipady=18)

        # Configure numpad grid weights
        for i in range(3):
            numpad_frame.columnconfigure(i, weight=1)

        # Right side - Quick buttons (compact)
        quick_card = ttk.Frame(content_frame)
        quick_card.pack(side=RIGHT, fill=BOTH)

        quick_frame = ttk.Frame(quick_card)
        quick_frame.pack(fill=BOTH, expand=YES)

        # Quick amount buttons - 2 columns for compact layout
        quick_amounts = [
            (20, 50),
            (100, 500),
            (1000, None)
        ]

        # Configure quick button style
        quick_style = ttk.Style()
        quick_style.configure("Quick.TButton", font=("Helvetica", 14, "bold"))

        for row_idx, (amt1, amt2) in enumerate(quick_amounts):
            row_frame = ttk.Frame(quick_frame)
            row_frame.pack(fill=X, pady=3)

            btn1 = ttk.Button(
                row_frame,
                text=f"฿{amt1}",
                bootstyle="success-outline",
                command=lambda a=amt1: (cash_amount.set(str(a)), update_change())
            )
            btn1.configure(style="Quick.TButton")
            btn1.pack(side=LEFT, fill=X, expand=YES, padx=(0, 3), ipady=12)

            if amt2:
                btn2 = ttk.Button(
                    row_frame,
                    text=f"฿{amt2}",
                    bootstyle="success-outline",
                    command=lambda a=amt2: (cash_amount.set(str(a)), update_change())
                )
                btn2.configure(style="Quick.TButton")
                btn2.pack(side=RIGHT, fill=X, expand=YES, padx=(3, 0), ipady=12)

        # Exact amount button
        exact_btn = ttk.Button(
            quick_frame,
            text=f"จำนวนเต็ม\n฿{self.app.total:,.2f}",
            bootstyle="info",
            command=lambda: (cash_amount.set(str(self.app.total)), update_change())
        )
        exact_btn.configure(style="Quick.TButton")
        exact_btn.pack(fill=X, pady=(8, 0), ipady=15)

        # Save payment button - will be configured later
        save_payment_btn = ttk.Button(
            quick_frame,
            text="✓ บันทึกชำระเงิน",
            bootstyle="success"
        )
        save_payment_btn.configure(style="Quick.TButton")
        save_payment_btn.pack(fill=X, pady=(8, 0), ipady=15)

        # Change display - Prominent
        change_card = ttk.Frame(main_frame, bootstyle="warning", relief="solid", borderwidth=2)
        change_card.pack(fill=X, pady=(0, 12))

        change_inner = ttk.Frame(change_card, padding=15)
        change_inner.pack(fill=X)

        ttk.Label(
            change_inner,
            text="💰 เงินทอน",
            font=("Helvetica", 14, "bold"),
            bootstyle="inverse-warning"
        ).pack()

        change_label = ttk.Label(
            change_inner,
            text="฿0.00",
            font=("Helvetica", 36, "bold"),
            bootstyle="inverse-warning"
        )
        change_label.pack(pady=(5, 0))

        # Update change function
        def update_change():
            try:
                received = float(cash_amount.get())
                change = received - self.app.total

                if change >= 0:
                    change_label.config(text=f"฿{change:,.2f}")
                    change_card.config(bootstyle="success")
                    change_label.config(bootstyle="inverse-success")
                else:
                    change_label.config(text=f"฿{change:,.2f}")
                    change_card.config(bootstyle="danger")
                    change_label.config(bootstyle="inverse-danger")
            except ValueError:
                change_label.config(text="฿0.00")
                change_card.config(bootstyle="warning")
                change_label.config(bootstyle="inverse-warning")

        # Confirm payment function
        def confirm_payment():
            try:
                total_received = float(cash_amount.get())
            except ValueError:
                total_received = 0

            if total_received < self.app.total:
                Messagebox.show_error(
                    "จำนวนเงินไม่พอ",
                    f"รับเงินมา ฿{total_received:,.2f}\nยอดรวม ฿{self.app.total:,.2f}\nยังขาดอีก ฿{self.app.total - total_received:,.2f}",
                    parent=dialog
                )
                return

            change = total_received - self.app.total

            # Create receipt
            receipt = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "items": self.app.cart.copy(),
                "total": self.app.total,
                "cash_received": total_received,
                "change": change
            }

            # Save receipt
            self.save_receipt(receipt)

            # Close payment dialog
            dialog.destroy()

            # Show receipt dialog
            self.show_receipt_dialog(receipt)

            # Clear cart
            self.app.cart = []
            self.update_cart_display()

        # Configure save payment button command now that confirm_payment is defined
        save_payment_btn.configure(command=confirm_payment)

        # Action buttons - Large and prominent
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=X, pady=(0, 0))

        # Configure action button style
        action_style = ttk.Style()
        action_style.configure("Action.TButton", font=("Helvetica", 16, "bold"))

        # Confirm button - Extra large and eye-catching
        confirm_btn = ttk.Button(
            action_frame,
            text="✓ ยืนยันการชำระเงิน",
            bootstyle="success",
            command=confirm_payment
        )
        confirm_btn.configure(style="Action.TButton")
        confirm_btn.pack(fill=X, pady=(0, 8), ipady=22)

        # Cancel button - Smaller, less prominent
        cancel_btn = ttk.Button(
            action_frame,
            text="✕ ยกเลิก",
            bootstyle="secondary-outline",
            command=dialog.destroy
        )
        cancel_btn.pack(fill=X, ipady=12)

        # Initialize display
        update_change()

    def show_receipt_dialog(self, receipt):
        """Show receipt dialog with print option"""
        dialog = ttk.Toplevel(self.app.root)
        dialog.title("ใบเสร็จ - Receipt")
        dialog.geometry("350x700")
        dialog.resizable(False, False)

        # Center the window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Make dialog modal
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Main container with scrollbar
        main_canvas = ttk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient=VERTICAL, command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Main container
        main_frame = ttk.Frame(scrollable_frame, padding=12)
        main_frame.pack(fill=BOTH, expand=YES)

        # Success icon with background
        success_header = ttk.Frame(main_frame, bootstyle="success")
        success_header.pack(fill=X, pady=(0, 15))

        success_inner = ttk.Frame(success_header, padding=10)
        success_inner.pack(fill=X)

        ttk.Label(
            success_inner,
            text="✓",
            font=("Helvetica", 32, "bold"),
            bootstyle="inverse-success"
        ).pack()

        ttk.Label(
            success_inner,
            text="ชำระเงินสำเร็จ!",
            font=("Helvetica", 14, "bold"),
            bootstyle="inverse-success"
        ).pack()

        # Receipt details frame
        receipt_frame = ttk.Frame(main_frame, relief="solid", borderwidth=2)
        receipt_frame.pack(fill=BOTH, expand=YES, pady=(0, 15))

        receipt_inner = ttk.Frame(receipt_frame, padding=10)
        receipt_inner.pack(fill=BOTH, expand=YES)

        # Store name
        ttk.Label(
            receipt_inner,
            text="ระบบขายหน้าร้าน",
            font=("Helvetica", 13, "bold")
        ).pack()

        # Date
        ttk.Label(
            receipt_inner,
            text=receipt["date"],
            font=("Helvetica", 10),
            bootstyle="secondary"
        ).pack(pady=(5, 10))

        # Separator
        ttk.Separator(receipt_inner).pack(fill=X, pady=8)

        # Items
        items_text = ttk.Text(receipt_inner, height=8, font=("Courier", 10), wrap=WORD)
        items_text.pack(fill=BOTH, expand=YES, pady=(0, 8))

        for item in receipt["items"]:
            emoji = self.get_product_emoji(item)
            items_text.insert(END, f"{emoji} {item['name']}\n")
            items_text.insert(END, f"  ฿{item['price']:.2f} x {item['qty']} = ฿{item['total']:.2f}\n")

        items_text.config(state=DISABLED)

        # Separator
        ttk.Separator(receipt_inner).pack(fill=X, pady=8)

        # Summary section with background
        summary_frame = ttk.Frame(receipt_inner, bootstyle="light", relief="solid", borderwidth=1)
        summary_frame.pack(fill=X, pady=(5, 0))

        summary_inner = ttk.Frame(summary_frame, padding=8)
        summary_inner.pack(fill=X)

        # Total
        total_frame = ttk.Frame(summary_inner)
        total_frame.pack(fill=X, pady=2)
        ttk.Label(total_frame, text="ยอดรวม:", font=("Helvetica", 11, "bold")).pack(side=LEFT)
        ttk.Label(total_frame, text=f"฿{receipt['total']:,.2f}", font=("Helvetica", 11, "bold")).pack(side=RIGHT)

        # Cash received
        cash_frame = ttk.Frame(summary_inner)
        cash_frame.pack(fill=X, pady=2)
        ttk.Label(cash_frame, text="รับเงินมา:", font=("Helvetica", 10)).pack(side=LEFT)
        ttk.Label(cash_frame, text=f"฿{receipt['cash_received']:,.2f}", font=("Helvetica", 10)).pack(side=RIGHT)

        # Separator for visual break
        ttk.Separator(summary_inner).pack(fill=X, pady=8)

        # Change and Print button section - Side by side
        change_print_frame = ttk.Frame(summary_inner)
        change_print_frame.pack(fill=X, pady=(5, 5))

        # Left side - Change amount with prominent display
        change_section = ttk.Frame(change_print_frame)
        change_section.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 5))

        ttk.Label(
            change_section,
            text="💰 เงินทอน",
            font=("Helvetica", 9, "bold")
        ).pack(anchor=W)

        change_display = ttk.Frame(change_section, bootstyle="success", relief="solid", borderwidth=2)
        change_display.pack(fill=X, pady=(3, 0))

        ttk.Label(
            change_display,
            text=f"฿{receipt['change']:,.2f}",
            font=("Helvetica", 16, "bold"),
            bootstyle="inverse-success",
            padding=6
        ).pack(fill=X)

        # Right side - Print button
        print_section = ttk.Frame(change_print_frame)
        print_section.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(5, 0))

        ttk.Label(
            print_section,
            text="",
            font=("Helvetica", 9)
        ).pack(anchor=W)  # Empty label for alignment

        print_btn = ttk.Button(
            print_section,
            text="🖨️\nพิมพ์",
            bootstyle="primary",
            command=lambda: self.print_receipt(receipt, dialog)
        )
        print_btn.pack(fill=BOTH, expand=YES, pady=(3, 0), ipady=8)

        # Thank you message
        ttk.Label(
            receipt_inner,
            text="ขอบคุณที่ใช้บริการ",
            font=("Helvetica", 9),
            bootstyle="secondary"
        ).pack(pady=(8, 0))

        # Close button at bottom
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=X, pady=(0, 0))

        close_btn = ttk.Button(
            action_frame,
            text="✕ ปิด",
            bootstyle="secondary",
            command=dialog.destroy
        )
        close_btn.pack(fill=X, ipady=12)

    def print_receipt(self, receipt, parent_dialog=None):
        """Print receipt to printer"""
        try:
            # Create receipts directory if it doesn't exist
            receipts_dir = os.path.join("data", "printed_receipts")
            os.makedirs(receipts_dir, exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(receipts_dir, f"receipt_{timestamp}.txt")

            # Create receipt text (narrower format - 32 chars)
            width = 32
            receipt_text = []
            receipt_text.append("=" * width)
            receipt_text.append("ระบบขายหน้าร้าน".center(width))
            receipt_text.append("=" * width)
            receipt_text.append(f"วันที่: {receipt['date']}")
            receipt_text.append("=" * width)
            receipt_text.append("")

            for item in receipt["items"]:
                # Remove emoji for better printing compatibility
                name = item['name']
                if len(name) > width - 2:
                    name = name[:width - 5] + "..."
                receipt_text.append(name)
                receipt_text.append(f"  {item['price']:.2f}฿ x {item['qty']} = {item['total']:.2f}฿")
                receipt_text.append("")

            receipt_text.append("=" * width)
            receipt_text.append(f"ยอดรวม:      {receipt['total']:>8.2f}฿")
            receipt_text.append(f"รับเงิน:      {receipt['cash_received']:>8.2f}฿")
            receipt_text.append(f"เงินทอน:      {receipt['change']:>8.2f}฿")
            receipt_text.append("=" * width)
            receipt_text.append("")
            receipt_text.append("ขอบคุณค่ะ".center(width))
            receipt_text.append("=" * width)

            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(receipt_text))

            # Send to printer using Windows default printer
            try:
                os.startfile(filename, "print")

                Messagebox.show_info(
                    "กำลังพิมพ์",
                    f"ส่งใบเสร็จไปยังเครื่องพิมพ์แล้ว\n\nบันทึกที่: {filename}",
                    parent=parent_dialog or self.app.root
                )
            except Exception as print_error:
                # Fallback: If printing fails, just save the file
                Messagebox.show_warning(
                    "บันทึกไฟล์แล้ว",
                    f"ไม่สามารถเชื่อมต่อเครื่องพิมพ์ได้\n\nบันทึกใบเสร็จที่:\n{filename}\n\nกรุณาเปิดไฟล์และพิมพ์ด้วยตนเอง",
                    parent=parent_dialog or self.app.root
                )

        except Exception as e:
            Messagebox.show_error(
                "เกิดข้อผิดพลาด",
                f"ไม่สามารถพิมพ์ใบเสร็จได้:\n{str(e)}",
                parent=parent_dialog or self.app.root
            )

    def save_receipt(self, receipt):
        """Save receipt to SQLite database"""
        try:
            receipt_id = self.app.db.save_receipt(
                cart=receipt['items'],
                total=receipt['total'],
                cash_received=receipt['cash_received'],
                change=receipt['change']
            )
            print(f"Receipt saved successfully with ID: {receipt_id}")
        except Exception as e:
            print(f"Error saving receipt to database: {e}")
            Messagebox.show_error(
                "Database Error",
                f"Failed to save receipt:\n{str(e)}",
                parent=self.app.root
            )
