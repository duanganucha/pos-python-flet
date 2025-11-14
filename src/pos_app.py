# -*- coding: utf-8 -*-
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for database import
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import DatabaseManager
from views import POSView, HistoryView, MenuView, CategoryView, UsersView, SettingsView

class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point of Sale System")
        self.root.geometry("1300x750")

        # Initialize database connection
        self.db = DatabaseManager()

        # Data storage
        self.cart = []
        self.products = self.load_products()
        self.categories = self.load_categories()
        self.total = 0.0
        self.current_products = None  # Track currently displayed products
        self.active_category = "All"  # Track active category filter
        self.category_buttons = {}  # Store category button references

        # View management
        self.current_view = None
        self.views = {}  # Store view frames
        self.active_menu_btn = None  # Track active menu button

        # Configure button style for larger text
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11))
        style.configure("Outline.TButton", font=("Helvetica", 11))

        # Configure sidebar button style
        style.configure("Sidebar.TButton", font=("Helvetica", 12, "bold"))

        # Create UI
        self.create_ui()

        # Register cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_products(self):
        """Load products from SQLite database"""
        try:
            return self.db.get_all_products()
        except Exception as e:
            print(f"Error loading products from database: {e}")
            # Return empty list if database error
            return []

    def load_categories(self):
        """Load categories from SQLite database"""
        try:
            return self.db.get_all_categories()
        except Exception as e:
            print(f"Error loading categories from database: {e}")
            return []

    def create_ui(self):
        """Create the main UI layout with sidebar navigation"""

        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=BOTH, expand=YES)

        # Sidebar
        self.create_sidebar(main_container)

        # Content area
        self.content_area = ttk.Frame(main_container, padding=10)
        self.content_area.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Create all views
        self.create_views()

        # Show POS view by default
        self.show_view("pos")

    def create_sidebar(self, parent):
        """Create sidebar navigation menu"""
        sidebar = ttk.Frame(parent, bootstyle="dark", width=200)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)

        # App title/logo
        title_frame = ttk.Frame(sidebar, bootstyle="dark")
        title_frame.pack(fill=X, pady=(20, 30), padx=10)

        ttk.Label(
            title_frame,
            text="🏪",
            font=("Segoe UI Emoji", 32),
            bootstyle="inverse-dark"
        ).pack()

        ttk.Label(
            title_frame,
            text="ระบบขายหน้าร้าน",
            font=("Helvetica", 16, "bold"),
            bootstyle="inverse-dark"
        ).pack()

        # Navigation buttons
        self.menu_buttons = {}
        self.menu_styles = {}  # Store original styles

        menu_items = [
            ("pos", "🛒 POS", "primary"),
            ("history", "📋 History", "info"),
            ("menu", "📦 Menu", "success"),
            ("category", "🏷️ Category", "warning"),
            ("users", "👥 Users", "secondary"),
            ("settings", "⚙️ Settings", "dark")
        ]

        for view_id, text, style in menu_items:
            btn = ttk.Button(
                sidebar,
                text=text,
                bootstyle=f"{style}-outline",
                command=lambda v=view_id: self.show_view(v)
            )
            btn.pack(fill=X, padx=10, pady=5, ipady=12)
            self.menu_buttons[view_id] = btn
            self.menu_styles[view_id] = style

        # Footer info
        footer = ttk.Frame(sidebar, bootstyle="dark")
        footer.pack(side=BOTTOM, fill=X, pady=20)

        ttk.Label(
            footer,
            text="v2.0 SQLite",
            font=("Helvetica", 9),
            bootstyle="inverse-dark"
        ).pack()

    def create_views(self):
        """Create all view frames"""
        # Create POS view
        self.pos_view = POSView(self.content_area, self)
        self.views["pos"] = self.pos_view.create()

        # Create History view
        self.history_view = HistoryView(self.content_area, self)
        self.views["history"] = self.history_view.create()

        # Create Menu view
        self.menu_view = MenuView(self.content_area, self)
        self.views["menu"] = self.menu_view.create()

        # Create Category view
        self.category_view = CategoryView(self.content_area, self)
        self.views["category"] = self.category_view.create()

        # Create Users view
        self.users_view = UsersView(self.content_area, self)
        self.views["users"] = self.users_view.create()

        # Create Settings view
        self.settings_view = SettingsView(self.content_area, self)
        self.views["settings"] = self.settings_view.create()

    def show_view(self, view_id):
        """Switch to a different view"""
        # Hide current view
        if self.current_view:
            self.views[self.current_view].pack_forget()

        # Show new view
        self.views[view_id].pack(fill=BOTH, expand=YES)
        self.current_view = view_id

        # Update menu button styles
        for vid, btn in self.menu_buttons.items():
            style = self.menu_styles[vid]
            if vid == view_id:
                # Active button - solid color
                btn.configure(bootstyle=style)
            else:
                # Inactive button - outline
                btn.configure(bootstyle=f"{style}-outline")

    def on_closing(self):
        """Clean up resources and close application"""
        try:
            # Close database connection
            self.db.close()
            print("Database connection closed")
        except Exception as e:
            print(f"Error closing database: {e}")
        finally:
            # Destroy the window
            self.root.destroy()


def main():
    # Create the main window with a theme (green theme for food/fresh vibe like Chili Pos)
    root = ttk.Window(themename="flatly")  # Flatly has nice green tones

    # Maximize window on startup
    root.state('zoomed')

    app = POSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
