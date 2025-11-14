# -*- coding: utf-8 -*-
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

class MenuView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        self.products_tree = None

    def create(self):
        """Create Menu view for product management"""
        # Header
        header = ttk.Label(
            self.frame,
            text="📦 จัดการสินค้า",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-success"
        )
        header.pack(fill=X, pady=(0, 20))

        # Action buttons
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill=X, pady=(0, 20))

        ttk.Button(
            action_frame,
            text="➕ เพิ่มสินค้า",
            bootstyle="success",
            command=self.show_add_product_dialog
        ).pack(side=LEFT, padx=(0, 10), ipady=10, ipadx=20)

        ttk.Button(
            action_frame,
            text="✏️ แก้ไขสินค้า",
            bootstyle="primary",
            command=self.show_edit_product_dialog
        ).pack(side=LEFT, padx=(0, 10), ipady=10, ipadx=20)

        ttk.Button(
            action_frame,
            text="🗑️ ลบสินค้า",
            bootstyle="danger",
            command=self.delete_product
        ).pack(side=LEFT, ipady=10, ipadx=20)

        # Product list
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(list_frame, text="สินค้าทั้งหมด", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 10))

        # Create treeview for products
        columns = ("รหัส", "ชื่อสินค้า", "ราคา", "หมวดหมู่")
        self.products_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.products_tree.heading(col, text=col)

        self.products_tree.column("รหัส", width=50)
        self.products_tree.column("ชื่อสินค้า", width=300)
        self.products_tree.column("ราคา", width=100)
        self.products_tree.column("หมวดหมู่", width=150)

        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)

        self.products_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Store reference in app for access from other methods
        self.app.products_tree = self.products_tree

        # Load products
        self.refresh_products_tree()

        return self.frame

    def refresh_products_tree(self):
        """Refresh products tree view"""
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        # Reload products from database
        self.app.products = self.app.load_products()

        # Insert products
        for product in self.app.products:
            self.products_tree.insert("", END, values=(
                product['id'],
                product['name'],
                f"฿{product['price']:.2f}",
                product['category']
            ))

    def show_add_product_dialog(self):
        """Show dialog to add new product"""
        dialog = ttk.Toplevel(self.app.root)
        dialog.title("Add New Product")
        dialog.geometry("500x400")
        dialog.resizable(False, False)

        # Center the window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Make dialog modal
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Main container
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Header
        ttk.Label(
            main_frame,
            text="➕ เพิ่มสินค้า",
            font=("Helvetica", 18, "bold"),
            bootstyle="success"
        ).pack(pady=(0, 20))

        # Form fields
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=X, pady=(0, 20))

        # Product name
        ttk.Label(form_frame, text="ชื่อสินค้า:", font=("Helvetica", 11, "bold")).pack(anchor=W, pady=(10, 5))
        name_entry = ttk.Entry(form_frame, font=("Helvetica", 11))
        name_entry.pack(fill=X, pady=(0, 10))

        # Product price
        ttk.Label(form_frame, text="ราคา (฿):", font=("Helvetica", 11, "bold")).pack(anchor=W, pady=(10, 5))
        price_entry = ttk.Entry(form_frame, font=("Helvetica", 11))
        price_entry.pack(fill=X, pady=(0, 10))

        # Product category
        ttk.Label(form_frame, text="หมวดหมู่:", font=("Helvetica", 11, "bold")).pack(anchor=W, pady=(10, 5))
        category_var = ttk.StringVar()
        category_combo = ttk.Combobox(
            form_frame,
            textvariable=category_var,
            values=self.app.categories,
            font=("Helvetica", 11),
            state="readonly"
        )
        category_combo.pack(fill=X, pady=(0, 10))
        if self.app.categories:
            category_combo.current(0)

        def save_product():
            # Validate inputs
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            category = category_var.get()

            if not name:
                Messagebox.show_error("Validation Error", "Product name is required.", parent=dialog)
                return

            if not price_str:
                Messagebox.show_error("Validation Error", "Price is required.", parent=dialog)
                return

            try:
                price = float(price_str)
                if price <= 0:
                    raise ValueError()
            except ValueError:
                Messagebox.show_error("Validation Error", "Price must be a positive number.", parent=dialog)
                return

            if not category:
                Messagebox.show_error("Validation Error", "Please select a category.", parent=dialog)
                return

            # Add product to database
            try:
                product_id = self.app.db.add_product(name, price, category)
                Messagebox.show_info("Success", f"Product '{name}' added successfully!", parent=dialog)

                # Refresh products tree
                self.refresh_products_tree()

                # Also reload products for POS view
                self.app.products = self.app.load_products()
                if hasattr(self.app, 'pos_view'):
                    self.app.pos_view.display_products()

                # Close dialog
                dialog.destroy()

            except Exception as e:
                Messagebox.show_error("Database Error", f"Failed to add product:\n{str(e)}", parent=dialog)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, side=BOTTOM)

        ttk.Button(
            button_frame,
            text="✓ บันทึกสินค้า",
            bootstyle="success",
            command=save_product
        ).pack(side=RIGHT, padx=(10, 0), ipady=10, ipadx=30)

        ttk.Button(
            button_frame,
            text="✕ ยกเลิก",
            bootstyle="secondary",
            command=dialog.destroy
        ).pack(side=RIGHT, ipady=10, ipadx=30)

        # Focus on name entry
        name_entry.focus()

    def show_edit_product_dialog(self):
        """Show dialog to edit selected product"""
        selection = self.products_tree.selection()
        if not selection:
            Messagebox.show_warning("No Selection", "Please select a product to edit.")
            return

        # Get selected product data
        item = self.products_tree.item(selection[0])
        values = item['values']
        product_id = values[0]
        current_name = values[1]
        current_price = float(values[2].replace('฿', '').replace(',', ''))
        current_category = values[3]

        dialog = ttk.Toplevel(self.app.root)
        dialog.title("Edit Product")
        dialog.geometry("500x400")
        dialog.resizable(False, False)

        # Center the window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Make dialog modal
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Main container
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Header
        ttk.Label(
            main_frame,
            text="✏️ แก้ไขสินค้า",
            font=("Helvetica", 18, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 20))

        # Form fields
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=X, pady=(0, 20))

        # Product ID (read-only)
        ttk.Label(form_frame, text=f"Product ID: {product_id}", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W, pady=(0, 10))

        # Product name
        ttk.Label(form_frame, text="ชื่อสินค้า:", font=("Helvetica", 11, "bold")).pack(anchor=W, pady=(10, 5))
        name_entry = ttk.Entry(form_frame, font=("Helvetica", 11))
        name_entry.insert(0, current_name)
        name_entry.pack(fill=X, pady=(0, 10))

        # Product price
        ttk.Label(form_frame, text="ราคา (฿):", font=("Helvetica", 11, "bold")).pack(anchor=W, pady=(10, 5))
        price_entry = ttk.Entry(form_frame, font=("Helvetica", 11))
        price_entry.insert(0, str(current_price))
        price_entry.pack(fill=X, pady=(0, 10))

        # Product category
        ttk.Label(form_frame, text="หมวดหมู่:", font=("Helvetica", 11, "bold")).pack(anchor=W, pady=(10, 5))
        category_var = ttk.StringVar(value=current_category)
        category_combo = ttk.Combobox(
            form_frame,
            textvariable=category_var,
            values=self.app.categories,
            font=("Helvetica", 11),
            state="readonly"
        )
        category_combo.pack(fill=X, pady=(0, 10))

        def update_product():
            # Validate inputs
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            category = category_var.get()

            if not name:
                Messagebox.show_error("Validation Error", "Product name is required.", parent=dialog)
                return

            if not price_str:
                Messagebox.show_error("Validation Error", "Price is required.", parent=dialog)
                return

            try:
                price = float(price_str)
                if price <= 0:
                    raise ValueError()
            except ValueError:
                Messagebox.show_error("Validation Error", "Price must be a positive number.", parent=dialog)
                return

            if not category:
                Messagebox.show_error("Validation Error", "Please select a category.", parent=dialog)
                return

            # Update product in database
            try:
                success = self.app.db.update_product(product_id, name, price, category)
                if success:
                    Messagebox.show_info("Success", f"Product '{name}' updated successfully!", parent=dialog)

                    # Refresh products tree
                    self.refresh_products_tree()

                    # Also reload products for POS view
                    self.app.products = self.app.load_products()
                    if hasattr(self.app, 'pos_view'):
                        self.app.pos_view.display_products()

                    # Close dialog
                    dialog.destroy()
                else:
                    Messagebox.show_error("Error", "Failed to update product.", parent=dialog)

            except Exception as e:
                Messagebox.show_error("Database Error", f"Failed to update product:\n{str(e)}", parent=dialog)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, side=BOTTOM)

        ttk.Button(
            button_frame,
            text="✓ อัปเดตสินค้า",
            bootstyle="primary",
            command=update_product
        ).pack(side=RIGHT, padx=(10, 0), ipady=10, ipadx=30)

        ttk.Button(
            button_frame,
            text="✕ ยกเลิก",
            bootstyle="secondary",
            command=dialog.destroy
        ).pack(side=RIGHT, ipady=10, ipadx=30)

        # Focus on name entry
        name_entry.focus()
        name_entry.select_range(0, END)

    def delete_product(self):
        """Delete selected product"""
        selection = self.products_tree.selection()
        if not selection:
            Messagebox.show_warning("No Selection", "Please select a product to delete.")
            return

        # Get selected product data
        item = self.products_tree.item(selection[0])
        values = item['values']
        product_id = values[0]
        product_name = values[1]

        # Confirm deletion
        result = Messagebox.yesno(
            "Confirm Deletion",
            f"Are you sure you want to delete '{product_name}'?\n\nThis action cannot be undone.",
            parent=self.app.root
        )

        if result == "Yes":
            try:
                success = self.app.db.delete_product(product_id)
                if success:
                    Messagebox.show_info("Success", f"Product '{product_name}' deleted successfully!")

                    # Refresh products tree
                    self.refresh_products_tree()

                    # Also reload products for POS view
                    self.app.products = self.app.load_products()
                    if hasattr(self.app, 'pos_view'):
                        self.app.pos_view.display_products()
                else:
                    Messagebox.show_error("Error", "Failed to delete product.")

            except Exception as e:
                Messagebox.show_error("Database Error", f"Failed to delete product:\n{str(e)}")
