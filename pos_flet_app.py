# -*- coding: utf-8 -*-
"""
Chili POS - Flet Version with Views Architecture
Main application file using modular views
"""
import flet as ft
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from database import DatabaseManager
from src.views_flet import (
    POSView,
    HistoryView,
    MenuView,
    CategoryView,
    UsersView,
    SettingsView
)


class ChiliPOSApp:
    """Main Chili POS Application"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Chili POS - Food Delivery System"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.spacing = 0

        # Custom theme with green colors (Chili Pos style)
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.GREEN,
            use_material3=True
        )

        # Initialize database
        self.db = DatabaseManager()

        # App state
        self.cart = []
        self.products = self.load_products()
        self.categories = self.load_categories()
        self.active_category = "All"
        self.payment_method = "Cash"
        self.total = 0.0
        self.subtotal = 0.0
        self.tax = 0.0

        # Current view
        self.current_view = "pos"

        # Views container
        self.views_container = ft.Container(expand=True)

        # Navigation buttons references
        self.nav_buttons = {}

        # Cache view instances
        self.view_instances = {}

        # Build UI
        self.build_ui()

    def load_products(self):
        """Load products from database"""
        try:
            return self.db.get_all_products()
        except Exception as e:
            print(f"Error loading products: {e}")
            return []

    def load_categories(self):
        """Load categories from database"""
        try:
            return self.db.get_all_categories()
        except Exception as e:
            print(f"Error loading categories: {e}")
            return []

    def build_ui(self):
        """Build the main UI"""
        # Main layout with sidebar navigation
        self.page.add(
            ft.Row(
                [
                    # Sidebar
                    self.build_sidebar(),
                    # Main content area
                    ft.Container(
                        content=ft.Column(
                            [
                                self.build_header(),
                                ft.Divider(height=1, color=ft.Colors.GREY_300),
                                self.views_container
                            ],
                            spacing=0,
                            expand=True
                        ),
                        expand=True
                    )
                ],
                spacing=0,
                expand=True
            )
        )

        # Load initial view (POS)
        self.switch_view("pos")

    def build_sidebar(self):
        """Build sidebar navigation"""
        return ft.Container(
            content=ft.Column(
                [
                    # Logo/Brand
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("🏪", size=40),
                                ft.Text(
                                    "Chili POS",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        ),
                        padding=ft.padding.only(top=30, bottom=30)
                    ),

                    # Navigation menu
                    ft.Container(
                        content=ft.Column(
                            [
                                self.create_nav_button("pos", "🛒 POS", ft.Colors.GREEN_700, is_active=True),
                                self.create_nav_button("history", "📋 History", ft.Colors.BLUE_700),
                                self.create_nav_button("menu", "📦 Menu", ft.Colors.ORANGE_700),
                                self.create_nav_button("category", "🏷️ Category", ft.Colors.PURPLE_700),
                                self.create_nav_button("users", "👥 Users", ft.Colors.GREY_700),
                                self.create_nav_button("settings", "⚙️ Settings", ft.Colors.GREY_800),
                            ],
                            spacing=10
                        ),
                        padding=10
                    ),

                    # Version info
                    ft.Container(
                        content=ft.Text(
                            "v2.0 Flet (Views)",
                            size=10,
                            color=ft.Colors.WHITE70,
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=20,
                        alignment=ft.alignment.center
                    )
                ],
                spacing=0,
                expand=True
            ),
            width=200,
            bgcolor=ft.Colors.GREY_900,
        )

    def create_nav_button(self, view_id, text, color, is_active=False):
        """Create navigation button"""
        btn = ft.Container(
            content=ft.Text(
            text,
            size=14,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
            ),
            bgcolor=color if is_active else ft.Colors.TRANSPARENT,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            ink=True,
            on_click=lambda e: self.switch_view(view_id),
            expand=True,
            alignment=ft.alignment.center_left
        )

        # Store reference
        self.nav_buttons[view_id] = btn

        return btn

    def build_header(self):
        """Build top header"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "🍽️ Chili POS System",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_700
                    ),
                    ft.Container(expand=True),
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=30, color=ft.Colors.GREY_700)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE
        )

    def switch_view(self, view_id):
        """Switch between views"""
        self.current_view = view_id

        # Update navigation button styles
        for vid, btn in self.nav_buttons.items():
            if vid == view_id:
                # Get color from button text
                if "POS" in btn.content.value:
                    btn.bgcolor = ft.Colors.GREEN_700
                elif "History" in btn.content.value:
                    btn.bgcolor = ft.Colors.BLUE_700
                elif "Menu" in btn.content.value:
                    btn.bgcolor = ft.Colors.ORANGE_700
                elif "Category" in btn.content.value:
                    btn.bgcolor = ft.Colors.PURPLE_700
                elif "Users" in btn.content.value:
                    btn.bgcolor = ft.Colors.GREY_700
                elif "Settings" in btn.content.value:
                    btn.bgcolor = ft.Colors.GREY_800
            else:
                btn.bgcolor = ft.Colors.TRANSPARENT

        # Load view
        view_map = {
            "pos": POSView,
            "history": HistoryView,
            "menu": MenuView,
            "category": CategoryView,
            "users": UsersView,
            "settings": SettingsView
        }

        if view_id in view_map:
            # Check if view instance already exists in cache
            if view_id not in self.view_instances:
                view_class = view_map[view_id]
                self.view_instances[view_id] = view_class(self)

            # Get cached view instance
            view_instance = self.view_instances[view_id]
            self.views_container.content = view_instance.create()
            self.page.update()


def main(page: ft.Page):
    """Main entry point"""
    app = ChiliPOSApp(page)


if __name__ == "__main__":
    # Run as desktop app (can also use ft.WEB_BROWSER for web view)
    ft.app(target=main)
