# -*- coding: utf-8 -*-
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class HistoryView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)

    def create(self):
        """Create History view to show transaction history"""
        # Header
        header = ttk.Label(
            self.frame,
            text="📋 ประวัติการขาย",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-info"
        )
        header.pack(fill=X, pady=(0, 20))

        # Summary cards
        summary_frame = ttk.Frame(self.frame)
        summary_frame.pack(fill=X, pady=(0, 20))

        # Get sales summary
        try:
            summary = self.app.db.get_sales_summary()

            # Today's sales card
            today_card = ttk.Frame(summary_frame, bootstyle="info", relief="solid", borderwidth=2)
            today_card.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

            today_inner = ttk.Frame(today_card, padding=15)
            today_inner.pack(fill=BOTH, expand=YES)

            ttk.Label(today_inner, text="ยอดขายวันนี้", font=("Helvetica", 12), bootstyle="inverse-info").pack()
            ttk.Label(today_inner, text=f"฿{summary['today_sales']:,.2f}", font=("Helvetica", 24, "bold"), bootstyle="inverse-info").pack()
            ttk.Label(today_inner, text=f"{summary['today_receipts']} ใบเสร็จ", font=("Helvetica", 10), bootstyle="inverse-info").pack()

            # Total sales card
            total_card = ttk.Frame(summary_frame, bootstyle="success", relief="solid", borderwidth=2)
            total_card.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(10, 0))

            total_inner = ttk.Frame(total_card, padding=15)
            total_inner.pack(fill=BOTH, expand=YES)

            ttk.Label(total_inner, text="ยอดขายรวม", font=("Helvetica", 12), bootstyle="inverse-success").pack()
            ttk.Label(total_inner, text=f"฿{summary['total_sales']:,.2f}", font=("Helvetica", 24, "bold"), bootstyle="inverse-success").pack()
            ttk.Label(total_inner, text=f"{summary['total_receipts']} ใบเสร็จ", font=("Helvetica", 10), bootstyle="inverse-success").pack()

        except Exception as e:
            print(f"Error loading sales summary: {e}")

        # Receipts list
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(list_frame, text="รายการล่าสุด", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 10))

        # Create treeview for receipts
        columns = ("รหัส", "วันที่", "รายการ", "ยอดรวม", "รับเงิน", "เงินทอน")
        receipts_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            receipts_tree.heading(col, text=col)

        receipts_tree.column("รหัส", width=50)
        receipts_tree.column("วันที่", width=150)
        receipts_tree.column("รายการ", width=80)
        receipts_tree.column("ยอดรวม", width=100)
        receipts_tree.column("รับเงิน", width=100)
        receipts_tree.column("เงินทอน", width=100)

        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=receipts_tree.yview)
        receipts_tree.configure(yscrollcommand=scrollbar.set)

        receipts_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Load receipts
        try:
            receipts = self.app.db.get_all_receipts(limit=100)
            for receipt in receipts:
                receipts_tree.insert("", END, values=(
                    receipt['id'],
                    receipt['date'],
                    receipt['items_count'],
                    f"฿{receipt['total']:,.2f}",
                    f"฿{receipt['cash_received']:,.2f}",
                    f"฿{receipt['change']:,.2f}"
                ))
        except Exception as e:
            print(f"Error loading receipts: {e}")

        return self.frame
