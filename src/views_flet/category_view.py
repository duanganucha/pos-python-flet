# -*- coding: utf-8 -*-
"""
Category View - Flet Version
Manage product categories
"""
import flet as ft
import json
import os


class CategoryView:
    def __init__(self, app):
        """Initialize Category view"""
        self.app = app
        self.page = app.page
        self.db = app.db

        # Category emojis mapping
        self.category_emojis = {}
        self.load_category_emojis()

        # Reference to main content for refreshing
        self.main_content = None

    def load_category_emojis(self):
        """Load category emojis from file"""
        try:
            if os.path.exists("data/category_emojis.json"):
                with open("data/category_emojis.json", "r", encoding="utf-8") as f:
                    self.category_emojis = json.load(f)
            else:
                # Default emojis
                self.category_emojis = {
                    'Beverages': '🥤', 'Food': '🍽️', 'Desserts': '🍰',
                    'Snacks': '🍿', 'Dairy': '🥛', 'Breakfast': '🍳',
                    'Soups': '🍲', 'Pasta': '🍝', 'Burgers': '🍔',
                    'Main Course': '🍖', 'Drinks': '☕'
                }
                self.save_category_emojis()
        except Exception as e:
            print(f"Error loading category emojis: {e}")
            self.category_emojis = {}

    def save_category_emojis(self):
        """Save category emojis to file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/category_emojis.json", "w", encoding="utf-8") as f:
                json.dump(self.category_emojis, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving category emojis: {e}")

    def create(self):
        """Create Category view layout"""
        categories = self.app.categories

        self.main_content = ft.Column(
            [
                # Header
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                "🏷️ จัดการหมวดหมู่",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            ),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "+ เพิ่มหมวดหมู่ใหม่",
                                on_click=lambda e: self.add_category(),
                                bgcolor=ft.Colors.PURPLE_700,
                                color=ft.Colors.WHITE
                            )
                        ]
                    ),
                    bgcolor=ft.Colors.PURPLE_700,
                    padding=20,
                    border_radius=10
                ),

                # Total categories card
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("หมวดหมู่ทั้งหมด", size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                ft.Text(str(len(categories)), size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        ),
                        bgcolor=ft.Colors.PURPLE_600,
                        padding=30,
                        border_radius=10
                    ),
                    elevation=4
                ),

                # Categories Grid
                ft.Container(
                    content=self.build_categories_grid(categories, self.category_emojis),
                    expand=True
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )

        return ft.Container(
            content=self.main_content,
            padding=20,
            expand=True
        )

    def refresh_view(self):
        """Refresh the entire view"""
        # Reload data from database
        self.app.categories = self.app.load_categories()
        self.load_category_emojis()

        # Rebuild the view
        categories = self.app.categories

        # Update total count
        self.main_content.controls[1].content.content.controls[1].value = str(len(categories))

        # Rebuild grid
        self.main_content.controls[2].content = self.build_categories_grid(categories, self.category_emojis)

        self.page.update()

    def build_categories_grid(self, categories, emojis):
        """Build categories grid"""
        if not categories:
            return ft.Container(
                content=ft.Text("ยังไม่มีหมวดหมู่", size=16, color=ft.Colors.GREY_600),
                alignment=ft.alignment.center,
                padding=40
            )

        # Count products per category
        category_counts = {}
        for product in self.app.products:
            cat = product['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        cards = []
        for category in categories:
            emoji = emojis.get(category, '🏷️')
            count = category_counts.get(category, 0)

            cards.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                # Emoji
                                ft.Container(
                                    content=ft.Text(emoji, size=60),
                                    bgcolor=ft.Colors.PURPLE_50,
                                    border_radius=50,
                                    padding=20,
                                    alignment=ft.alignment.center
                                ),

                                # Category name
                                ft.Text(
                                    category,
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER
                                ),

                                # Product count
                                ft.Container(
                                    content=ft.Text(
                                        f"{count} สินค้า",
                                        size=12,
                                        color=ft.Colors.WHITE
                                    ),
                                    bgcolor=ft.Colors.PURPLE_700,
                                    border_radius=15,
                                    padding=ft.padding.symmetric(horizontal=15, vertical=5)
                                ),

                                # Actions
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color=ft.Colors.BLUE_700,
                                            tooltip="แก้ไข",
                                            on_click=lambda e, c=category: self.edit_category(c)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED_700,
                                            tooltip="ลบ",
                                            on_click=lambda e, c=category: self.delete_category(c)
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=5
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        padding=20
                    ),
                    elevation=2
                )
            )

        return ft.GridView(
            runs_count=4,
            max_extent=200,
            child_aspect_ratio=0.85,
            spacing=15,
            run_spacing=15,
            controls=cards,
            expand=True
        )

    def add_category(self):
        """Add new category - Show dialog"""
        name_field = ft.TextField(label="ชื่อหมวดหมู่", width=300)
        emoji_field = ft.TextField(label="Emoji (ไม่บังคับ)", width=300, hint_text="🍕")

        def close_dlg(e):
            add_dlg.open = False
            self.page.update()

        def save_category(e):
            if not name_field.value:
                self.show_error("กรุณากรอกชื่อหมวดหมู่")
                return

            category_name = name_field.value.strip()

            # Check if category already exists
            if category_name in self.app.categories:
                self.show_error(f"มีหมวดหมู่ '{category_name}' อยู่แล้ว")
                return

            try:
                # Add category to database
                self.db.add_category(category_name)

                # Save emoji if provided
                if emoji_field.value and emoji_field.value.strip():
                    self.category_emojis[category_name] = emoji_field.value.strip()
                    self.save_category_emojis()

                # Close dialog
                add_dlg.open = False
                self.page.update()

                # Refresh view
                self.refresh_view()

                # Show success
                self.show_success(f"เพิ่มหมวดหมู่ '{category_name}' สำเร็จ")

            except Exception as ex:
                self.show_error(f"เกิดข้อผิดพลาด: {str(ex)}")

        add_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("➕ เพิ่มหมวดหมู่ใหม่", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                name_field,
                emoji_field
            ], spacing=15, tight=True),
            actions=[
                ft.TextButton("ยกเลิก", on_click=close_dlg),
                ft.ElevatedButton(
                    "บันทึก",
                    on_click=save_category,
                    bgcolor=ft.Colors.PURPLE_700,
                    color=ft.Colors.WHITE
                )
            ]
        )

        self.page.overlay.append(add_dlg)
        add_dlg.open = True
        self.page.update()

    def edit_category(self, category):
        """Edit category - Show dialog"""
        name_field = ft.TextField(label="ชื่อหมวดหมู่", value=category, width=300)
        emoji_field = ft.TextField(
            label="Emoji (ไม่บังคับ)",
            value=self.category_emojis.get(category, ""),
            width=300,
            hint_text="🍕"
        )

        def close_dlg(e):
            edit_dlg.open = False
            self.page.update()

        def save_changes(e):
            if not name_field.value:
                self.show_error("กรุณากรอกชื่อหมวดหมู่")
                return

            new_category_name = name_field.value.strip()

            # Check if new name already exists (except current category)
            if new_category_name != category and new_category_name in self.app.categories:
                self.show_error(f"มีหมวดหมู่ '{new_category_name}' อยู่แล้ว")
                return

            try:
                # Update category in database (update all products with this category)
                self.db.update_category(category, new_category_name)

                # Update emoji
                if category in self.category_emojis:
                    del self.category_emojis[category]

                if emoji_field.value and emoji_field.value.strip():
                    self.category_emojis[new_category_name] = emoji_field.value.strip()

                self.save_category_emojis()

                # Close dialog
                edit_dlg.open = False
                self.page.update()

                # Refresh view
                self.refresh_view()

                # Show success
                self.show_success(f"แก้ไขหมวดหมู่เป็น '{new_category_name}' สำเร็จ")

            except Exception as ex:
                self.show_error(f"เกิดข้อผิดพลาด: {str(ex)}")

        edit_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"✏️ แก้ไขหมวดหมู่: {category}", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                name_field,
                emoji_field
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

    def delete_category(self, category):
        """Delete category - Show confirmation dialog"""
        # Count products in this category
        product_count = sum(1 for p in self.app.products if p['category'] == category)

        def close_dlg(e):
            delete_dlg.open = False
            self.page.update()

        def confirm_delete(e):
            try:
                # Delete category from database
                # This should move products to 'อื่นๆ' or 'Uncategorized'
                self.db.delete_category(category)

                # Remove emoji
                if category in self.category_emojis:
                    del self.category_emojis[category]
                    self.save_category_emojis()

                # Close dialog
                delete_dlg.open = False
                self.page.update()

                # Refresh view
                self.refresh_view()

                # Show success
                if product_count > 0:
                    self.show_success(f"ลบหมวดหมู่ '{category}' สำเร็จ\nย้าย {product_count} สินค้าไป 'อื่นๆ'")
                else:
                    self.show_success(f"ลบหมวดหมู่ '{category}' สำเร็จ")

            except Exception as ex:
                self.show_error(f"เกิดข้อผิดพลาด: {str(ex)}")

        delete_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED_700, size=32),
                ft.Text("ยืนยันการลบ", size=20, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Text(
                f"คุณต้องการลบหมวดหมู่ '{category}' หรือไม่?\n\n"
                f"⚠️ มีสินค้า {product_count} รายการในหมวดหมู่นี้\n"
                f"สินค้าทั้งหมดจะถูกย้ายไป 'อื่นๆ'",
                size=14
            ),
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

    def show_success(self, message):
        """Show success message"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=20),
                    ft.Text(message, size=14, color=ft.Colors.WHITE)
                ],
                spacing=10
            ),
            bgcolor=ft.Colors.GREEN_700,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()

    def show_error(self, message):
        """Show error message"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE, size=20),
                    ft.Text(message, size=14, color=ft.Colors.WHITE)
                ],
                spacing=10
            ),
            bgcolor=ft.Colors.RED_700,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()
