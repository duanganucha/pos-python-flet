# -*- coding: utf-8 -*-
"""
Users View - Flet Version
Manage users and permissions
"""
import flet as ft


class UsersView:
    def __init__(self, app):
        """Initialize Users view"""
        self.app = app
        self.page = app.page
        self.db = app.db

    def create(self):
        """Create Users view layout"""
        # Mock users data
        users = [
            {'id': 1, 'name': 'Admin', 'email': 'admin@chilipos.com', 'role': 'Administrator', 'status': 'Active'},
            {'id': 2, 'name': 'Cashier 1', 'email': 'cashier1@chilipos.com', 'role': 'Cashier', 'status': 'Active'},
            {'id': 3, 'name': 'Cashier 2', 'email': 'cashier2@chilipos.com', 'role': 'Cashier', 'status': 'Inactive'},
        ]

        return ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    "👥 จัดการผู้ใช้",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "+ เพิ่มผู้ใช้ใหม่",
                                    on_click=lambda e: self.add_user(),
                                    bgcolor=ft.Colors.GREY_700,
                                    color=ft.Colors.WHITE
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.GREY_700,
                        padding=20,
                        border_radius=10
                    ),

                    # Stats
                    ft.Row(
                        [
                            self.build_stat_card("👥 ผู้ใช้ทั้งหมด", str(len(users)), ft.Colors.BLUE_600),
                            self.build_stat_card("✅ ใช้งานอยู่", str(len([u for u in users if u['status'] == 'Active'])), ft.Colors.GREEN_600),
                            self.build_stat_card("❌ ไม่ใช้งาน", str(len([u for u in users if u['status'] == 'Inactive'])), ft.Colors.RED_600),
                        ],
                        spacing=15
                    ),

                    # Users List
                    ft.Container(
                        content=self.build_users_list(users),
                        expand=True
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20,
            expand=True
        )

    def build_stat_card(self, title, value, color):
        """Build stat card"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(title, size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                bgcolor=color,
                padding=15,
                border_radius=10
            ),
            elevation=4
        )

    def build_users_list(self, users):
        """Build users list"""
        user_cards = []
        for user in users:
            status_color = ft.Colors.GREEN_700 if user['status'] == 'Active' else ft.Colors.RED_700

            user_cards.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                # Avatar
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.PERSON,
                                        color=ft.Colors.WHITE,
                                        size=30
                                    ),
                                    bgcolor=ft.Colors.GREY_700,
                                    border_radius=50,
                                    padding=15
                                ),

                                # User info
                                ft.Column(
                                    [
                                        ft.Text(user['name'], size=16, weight=ft.FontWeight.BOLD),
                                        ft.Text(user['email'], size=12, color=ft.Colors.GREY_600),
                                        ft.Text(user['role'], size=11, color=ft.Colors.BLUE_700)
                                    ],
                                    spacing=2,
                                    expand=True
                                ),

                                # Status
                                ft.Container(
                                    content=ft.Text(
                                        user['status'],
                                        size=12,
                                        color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    bgcolor=status_color,
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
                                            on_click=lambda e, u=user: self.edit_user(u)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED_700,
                                            tooltip="ลบ",
                                            on_click=lambda e, u=user: self.delete_user(u)
                                        )
                                    ],
                                    spacing=5
                                )
                            ],
                            spacing=15,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=15
                    ),
                    elevation=2
                )
            )

        return ft.Column(user_cards, spacing=10, scroll=ft.ScrollMode.AUTO)

    def add_user(self):
        """Add new user - Show dialog"""
        name_field = ft.TextField(label="ชื่อ", width=300)
        email_field = ft.TextField(label="อีเมล", width=300, keyboard_type=ft.KeyboardType.EMAIL)
        role_dropdown = ft.Dropdown(
            label="สิทธิ์",
            width=300,
            options=[
                ft.dropdown.Option("Administrator"),
                ft.dropdown.Option("Cashier"),
                ft.dropdown.Option("Manager")
            ],
            value="Cashier"
        )

        def close_dlg(e):
            add_dlg.open = False
            self.page.update()

        def save_user(e):
            if not name_field.value or not email_field.value:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("กรุณากรอกข้อมูลให้ครบ"),
                    bgcolor=ft.Colors.RED_700
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

            add_dlg.open = False
            self.page.update()

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ เพิ่มผู้ใช้ '{name_field.value}' สำเร็จ (Demo)"),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.snack_bar.open = True
            self.page.update()

        add_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("➕ เพิ่มผู้ใช้ใหม่", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                name_field,
                email_field,
                role_dropdown
            ], spacing=15, tight=True),
            actions=[
                ft.TextButton("ยกเลิก", on_click=close_dlg),
                ft.ElevatedButton(
                    "บันทึก",
                    on_click=save_user,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE
                )
            ]
        )

        self.page.overlay.append(add_dlg)
        add_dlg.open = True
        self.page.update()

    def edit_user(self, user):
        """Edit user - Show dialog"""
        name_field = ft.TextField(label="ชื่อ", value=user['name'], width=300)
        email_field = ft.TextField(label="อีเมล", value=user['email'], width=300, keyboard_type=ft.KeyboardType.EMAIL)
        role_dropdown = ft.Dropdown(
            label="สิทธิ์",
            value=user['role'],
            width=300,
            options=[
                ft.dropdown.Option("Administrator"),
                ft.dropdown.Option("Cashier"),
                ft.dropdown.Option("Manager")
            ]
        )
        status_switch = ft.Switch(label="เปิดใช้งาน", value=(user['status'] == 'Active'))

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
            title=ft.Text(f"✏️ แก้ไขผู้ใช้: {user['name']}", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                name_field,
                email_field,
                role_dropdown,
                status_switch
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

    def delete_user(self, user):
        """Delete user - Show confirmation dialog"""
        def close_dlg(e):
            delete_dlg.open = False
            self.page.update()

        def confirm_delete(e):
            delete_dlg.open = False
            self.page.update()

            # Show success
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ ลบผู้ใช้ '{user['name']}' สำเร็จ (Demo)"),
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
            content=ft.Column([
                ft.Text(f"คุณต้องการลบผู้ใช้ '{user['name']}' หรือไม่?", size=14),
                ft.Text("การกระทำนี้ไม่สามารถยกเลิกได้", size=12, color=ft.Colors.GREY_700)
            ], tight=True, spacing=10),
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
