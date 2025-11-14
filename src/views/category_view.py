# -*- coding: utf-8 -*-
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class CategoryView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)

    def create(self):
        """Create Category view for category management"""
        # Header
        header = ttk.Label(
            self.frame,
            text="🏷️ จัดการหมวดหมู่",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-warning"
        )
        header.pack(fill=X, pady=(0, 20))

        # Action buttons
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            action_frame,
            text="หมายเหตุ: หมวดหมู่จะถูกจัดการอัตโนมัติผ่านสินค้า เพิ่มสินค้าเพื่อสร้างหมวดหมู่",
            font=("Helvetica", 10),
            bootstyle="secondary",
            wraplength=800
        ).pack(side=LEFT, padx=(0, 10))

        # Category list with product counts
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(list_frame, text="หมวดหมู่ทั้งหมด", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 10))

        # Create grid for categories
        grid_frame = ttk.Frame(list_frame)
        grid_frame.pack(fill=BOTH, expand=YES)

        # Count products by category
        category_counts = {}
        for product in self.app.products:
            cat = product['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Display category cards
        row = 0
        col = 0
        for category in self.app.categories:
            count = category_counts.get(category, 0)

            card = ttk.Frame(grid_frame, bootstyle="warning", relief="solid", borderwidth=2)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            inner = ttk.Frame(card, padding=20)
            inner.pack(fill=BOTH, expand=YES)

            ttk.Label(inner, text=category, font=("Helvetica", 16, "bold"), bootstyle="inverse-warning").pack()
            ttk.Label(inner, text=f"{count} products", font=("Helvetica", 12), bootstyle="inverse-warning").pack(pady=(5, 0))

            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Configure grid weights
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)

        return self.frame
