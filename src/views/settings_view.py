# -*- coding: utf-8 -*-
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import os
import shutil
from datetime import datetime
import subprocess

class SettingsView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)

    def create(self):
        """Create Settings view for application settings"""
        # Header
        header = ttk.Label(
            self.frame,
            text="⚙️ ตั้งค่าโปรแกรม",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-dark"
        )
        header.pack(fill=X, pady=(0, 20))

        # Settings sections
        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill=BOTH, expand=YES)

        # General settings tab
        general_tab = ttk.Frame(notebook, padding=20)
        notebook.add(general_tab, text="ทั่วไป")

        ttk.Label(general_tab, text="ข้อมูลร้าน", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 10))

        # Store name
        ttk.Label(general_tab, text="ชื่อร้าน:").pack(anchor=W, pady=(10, 5))
        store_name = ttk.Entry(general_tab, font=("Helvetica", 11))
        store_name.insert(0, "ระบบขายหน้าร้าน")
        store_name.pack(fill=X, pady=(0, 15))

        # Store address
        ttk.Label(general_tab, text="ที่อยู่ร้าน:").pack(anchor=W, pady=(0, 5))
        store_address = ttk.Text(general_tab, height=3, font=("Helvetica", 11))
        store_address.insert("1.0", "123 Main Street\nCity, Country\nPostal Code")
        store_address.pack(fill=X, pady=(0, 15))

        # Theme settings tab
        theme_tab = ttk.Frame(notebook, padding=20)
        notebook.add(theme_tab, text="การแสดงผล")

        ttk.Label(theme_tab, text="ธีม", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 10))
        ttk.Label(theme_tab, text="เลือกธีมสำหรับแอปพลิเคชัน:").pack(anchor=W, pady=(10, 5))

        theme_var = ttk.StringVar(value="cosmo")
        themes = ["cosmo", "flatly", "litera", "minty", "lumen", "sandstone", "yeti", "pulse", "united", "morph", "journal", "darkly", "superhero", "solar", "cyborg", "vapor"]

        for theme in themes[:8]:  # Show first 8 themes
            ttk.Radiobutton(
                theme_tab,
                text=theme.capitalize(),
                variable=theme_var,
                value=theme,
                bootstyle="toolbutton"
            ).pack(anchor=W, pady=2)

        # Database settings tab
        database_tab = ttk.Frame(notebook, padding=20)
        notebook.add(database_tab, text="ฐานข้อมูล")

        ttk.Label(database_tab, text="ข้อมูลฐานข้อมูล", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 10))

        db_info = ttk.Frame(database_tab, bootstyle="light", relief="solid", borderwidth=1)
        db_info.pack(fill=X, pady=(10, 0))

        db_inner = ttk.Frame(db_info, padding=15)
        db_inner.pack(fill=X)

        ttk.Label(db_inner, text=f"Database Type: SQLite", font=("Helvetica", 11)).pack(anchor=W, pady=2)
        ttk.Label(db_inner, text=f"Database Location: database/pos.db", font=("Helvetica", 11)).pack(anchor=W, pady=2)
        ttk.Label(db_inner, text=f"Total Products: {len(self.app.products)}", font=("Helvetica", 11)).pack(anchor=W, pady=2)

        try:
            summary = self.app.db.get_sales_summary()
            ttk.Label(db_inner, text=f"Total Receipts: {summary['total_receipts']}", font=("Helvetica", 11)).pack(anchor=W, pady=2)
        except:
            pass

        # Backup button
        ttk.Button(
            database_tab,
            text="💾 สำรองฐานข้อมูล",
            bootstyle="info",
            command=self.backup_database
        ).pack(anchor=W, pady=(20, 5), ipady=10, ipadx=20)

        ttk.Button(
            database_tab,
            text="🔄 รีเซ็ตฐานข้อมูล",
            bootstyle="warning",
            command=self.reset_database
        ).pack(anchor=W, pady=(5, 0), ipady=10, ipadx=20)

        # About tab
        about_tab = ttk.Frame(notebook, padding=20)
        notebook.add(about_tab, text="เกี่ยวกับ")

        ttk.Label(about_tab, text="ระบบขายหน้าร้าน", font=("Helvetica", 20, "bold")).pack(pady=(20, 10))
        ttk.Label(about_tab, text="เวอร์ชัน 2.0", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(about_tab, text="SQLite Database Edition", font=("Helvetica", 11), bootstyle="secondary").pack(pady=5)

        ttk.Separator(about_tab).pack(fill=X, pady=20)

        ttk.Label(about_tab, text="คุณสมบัติ:", font=("Helvetica", 12, "bold")).pack(anchor=W, pady=(10, 5))
        features_text = """
        • Point of Sale with shopping cart
        • Product category filtering
        • Transaction history and reporting
        • SQLite database backend
        • Receipt printing
        • Modern responsive UI
        • Multi-view navigation
        """
        ttk.Label(about_tab, text=features_text, font=("Helvetica", 10), justify=LEFT).pack(anchor=W, padx=20)

        # Save button at bottom
        save_frame = ttk.Frame(self.frame)
        save_frame.pack(side=BOTTOM, fill=X, pady=(20, 0))

        ttk.Button(
            save_frame,
            text="💾 บันทึกการตั้งค่า",
            bootstyle="success",
            command=lambda: Messagebox.show_info("Settings", "Settings saved successfully!")
        ).pack(side=RIGHT, ipady=10, ipadx=30)

        return self.frame

    def backup_database(self):
        """Create a backup of the database"""
        try:
            # Create backups directory if it doesn't exist
            backup_dir = os.path.join("database", "backups")
            os.makedirs(backup_dir, exist_ok=True)

            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"pos_backup_{timestamp}.db")

            # Copy database file
            shutil.copy2("database/pos.db", backup_file)

            # Get file size
            size = os.path.getsize(backup_file) / 1024  # KB

            Messagebox.show_info(
                "Backup Successful",
                f"Database backed up successfully!\n\nLocation: {backup_file}\nSize: {size:.2f} KB"
            )

        except Exception as e:
            Messagebox.show_error("Backup Failed", f"Failed to backup database:\n{str(e)}")

    def reset_database(self):
        """Reset database to default state"""
        result = Messagebox.yesno(
            "Confirm Reset",
            "⚠️ WARNING: This will delete ALL data and reset the database!\n\n"
            "This includes:\n"
            "• All products\n"
            "• All transaction history\n"
            "• All receipts\n\n"
            "This action CANNOT be undone!\n\n"
            "Do you want to continue?",
            parent=self.app.root
        )

        if result == "Yes":
            # Double confirmation
            result2 = Messagebox.yesno(
                "Final Confirmation",
                "Are you ABSOLUTELY SURE you want to reset the database?\n\n"
                "All data will be permanently deleted!",
                parent=self.app.root
            )

            if result2 == "Yes":
                try:
                    # Close current database connection
                    self.app.db.close()

                    # Re-run seed script
                    result = subprocess.run(
                        ["python", "database/seed_db.py"],
                        capture_output=True,
                        text=True
                    )

                    if result.returncode == 0:
                        # Reconnect to database
                        from database import DatabaseManager
                        self.app.db = DatabaseManager()

                        # Reload data
                        self.app.products = self.app.load_products()
                        self.app.categories = self.app.load_categories()

                        # Refresh all views
                        if hasattr(self.app, 'pos_view'):
                            self.app.pos_view.display_products()
                        if hasattr(self.app, 'menu_view'):
                            self.app.menu_view.refresh_products_tree()

                        # Clear cart
                        self.app.cart = []
                        if hasattr(self.app, 'pos_view'):
                            self.app.pos_view.update_cart_display()

                        Messagebox.show_info(
                            "Reset Complete",
                            "Database has been reset successfully!\n\n"
                            "All data has been restored to default state."
                        )
                    else:
                        Messagebox.show_error(
                            "Reset Failed",
                            f"Failed to reset database:\n{result.stderr}"
                        )

                except Exception as e:
                    Messagebox.show_error("Reset Failed", f"Failed to reset database:\n{str(e)}")

                    # Try to reconnect anyway
                    try:
                        from database import DatabaseManager
                        self.app.db = DatabaseManager()
                    except:
                        pass
