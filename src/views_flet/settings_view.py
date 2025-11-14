# -*- coding: utf-8 -*-
"""
Settings View - Flet Version
Application settings and configuration
"""
import flet as ft


class SettingsView:
    def __init__(self, app):
        """Initialize Settings view"""
        self.app = app
        self.page = app.page
        self.db = app.db

    def create(self):
        """Create Settings view layout"""
        return ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Container(
                        content=ft.Text(
                            "⚙️ ตั้งค่าระบบ",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        bgcolor=ft.Colors.GREY_800,
                        padding=20,
                        border_radius=10
                    ),

                    # Settings sections
                    self.build_section("🏪 ข้อมูลร้าน", [
                        self.build_setting_row("ชื่อร้าน", "Chili POS Restaurant"),
                        self.build_setting_row("ที่อยู่", "123 Food Street, Bangkok"),
                        self.build_setting_row("เบอร์โทร", "02-123-4567"),
                        self.build_setting_row("อีเมล", "contact@chilipos.com"),
                    ]),

                    self.build_section("💰 การชำระเงิน", [
                        self.build_switch_row("เปิดใช้เงินสด", True),
                        self.build_switch_row("เปิดใช้บัตร", True),
                        self.build_switch_row("เปิดใช้ QR Code", True),
                        self.build_setting_row("ภาษี (%)", "7"),
                    ]),

                    self.build_section("🖨️ ใบเสร็จ", [
                        self.build_switch_row("พิมพ์อัตโนมัติ", False),
                        self.build_setting_row("ขนาดกระดาษ", "80mm"),
                        self.build_switch_row("แสดงโลโก้", True),
                    ]),

                    self.build_section("🎨 การแสดงผล", [
                        self.build_switch_row("โหมดมืด", False),
                        self.build_setting_row("ภาษา", "ไทย"),
                        self.build_setting_row("สกุลเงิน", "฿ (บาท)"),
                    ]),

                    # Save button
                    ft.Container(
                        content=ft.ElevatedButton(
                            "💾 บันทึกการตั้งค่า",
                            on_click=lambda e: self.save_settings(),
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                            width=200,
                            height=50
                        ),
                        alignment=ft.alignment.center,
                        padding=20
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20,
            expand=True
        )

    def build_section(self, title, settings):
        """Build settings section"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Divider(),
                        *settings
                    ],
                    spacing=15
                ),
                padding=20
            ),
            elevation=2
        )

    def build_setting_row(self, label, value):
        """Build setting row"""
        return ft.Row(
            [
                ft.Text(label, size=14, expand=True),
                ft.TextField(
                    value=value,
                    width=200,
                    text_size=14,
                    border_color=ft.Colors.GREY_400
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def build_switch_row(self, label, value):
        """Build switch row"""
        return ft.Row(
            [
                ft.Text(label, size=14, expand=True),
                ft.Switch(value=value, active_color=ft.Colors.GREEN_700)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def save_settings(self):
        """Save settings"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=24),
                    ft.Text("บันทึกการตั้งค่าสำเร็จ!", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ],
                spacing=10
            ),
            bgcolor=ft.Colors.GREEN_700,
            duration=3000,
            action="ปิด",
            action_color=ft.Colors.WHITE
        )
        self.page.snack_bar.open = True
        self.page.update()
