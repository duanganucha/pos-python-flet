# -*- coding: utf-8 -*-
"""
Category View - Flet Version
Manage product categories
"""
import flet as ft


class CategoryView:
    def __init__(self, app):
        """Initialize Category view"""
        self.app = app
        self.page = app.page
        self.db = app.db

    def create(self):
        """Create Category view layout"""
        categories = self.app.categories

        category_emojis = {
            'Beverages': '🥤', 'Food': '🍽️', 'Desserts': '🍰',
            'Snacks': '🍿', 'Dairy': '🥛', 'Breakfast': '🍳',
            'Soups': '🍲', 'Pasta': '🍝', 'Burgers': '🍔',
            'Main Course': '🍖', 'Drinks': '☕'
        }

        return ft.Container(
            content=ft.Column(
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
                        content=self.build_categories_grid(categories, category_emojis),
                        expand=True
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20,
            expand=True
        )

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
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("กรุณากรอกชื่อหมวดหมู่"),
                    bgcolor=ft.Colors.RED_700
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

            add_dlg.open = False
            self.page.update()

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ เพิ่มหมวดหมู่ '{name_field.value}' สำเร็จ (Demo)"),
                bgcolor=ft.Colors.PURPLE_700
            )
            self.page.snack_bar.open = True
            self.page.update()

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
            title=ft.Text(f"✏️ แก้ไขหมวดหมู่: {category}", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([name_field], tight=True),
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
        def close_dlg(e):
            delete_dlg.open = False
            self.page.update()

        def confirm_delete(e):
            delete_dlg.open = False
            self.page.update()

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ ลบหมวดหมู่ '{category}' สำเร็จ (Demo)"),
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
            content=ft.Text(f"คุณต้องการลบหมวดหมู่ '{category}' หรือไม่?\n\n⚠️ สินค้าในหมวดหมู่นี้จะถูกย้ายไป 'อื่นๆ'", size=14),
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
