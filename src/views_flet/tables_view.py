# -*- coding: utf-8 -*-
"""
Tables View - Flet Version
Table management with CRUD operations
"""
import flet as ft
import json
import os


class TablesView:
    def __init__(self, app):
        """Initialize Tables view"""
        self.app = app
        self.page = app.page
        self.db = app.db

        # Table management state
        self.tables = []
        self.load_tables()
        self.tables_list = None

    def load_tables(self):
        """Load tables from file"""
        try:
            if os.path.exists("data/tables.json"):
                with open("data/tables.json", "r", encoding="utf-8") as f:
                    self.tables = json.load(f)
            else:
                # Default tables
                self.tables = [
                    {"id": i, "number": i, "seats": 4, "status": "available", "name": f"โต๊ะ {i}"}
                    for i in range(1, 11)
                ]
                self.save_tables()
        except Exception as e:
            print(f"Error loading tables: {e}")
            self.tables = []

    def save_tables(self):
        """Save tables to file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/tables.json", "w", encoding="utf-8") as f:
                json.dump(self.tables, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving tables: {e}")

    def create(self):
        """Create Tables view layout"""
        self.tables_list = ft.Column(spacing=10)
        self.display_tables()

        return ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    "🍽️ จัดการโต๊ะ",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.ElevatedButton(
                                    "➕ เพิ่มโต๊ะใหม่",
                                    on_click=self.show_add_table_dialog,
                                    bgcolor=ft.Colors.GREEN_700,
                                    color=ft.Colors.WHITE
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        bgcolor=ft.Colors.BLUE_700,
                        padding=20,
                        border_radius=10
                    ),

                    # Tables list
                    ft.Container(
                        content=self.tables_list,
                        expand=True,
                        padding=10
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                expand=True
            ),
            padding=20,
            expand=True
        )

    def display_tables(self):
        """Display all tables"""
        self.tables_list.controls.clear()

        if not self.tables:
            self.tables_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "ยังไม่มีโต๊ะ กรุณาเพิ่มโต๊ะใหม่",
                        size=16,
                        color=ft.Colors.GREY_700
                    ),
                    alignment=ft.alignment.center,
                    padding=50
                )
            )
        else:
            for table in self.tables:
                self.tables_list.controls.append(
                    self.create_table_card(table)
                )

        self.page.update()

    def create_table_card(self, table):
        """Create table card"""
        # Status color
        status_colors = {
            "available": ft.Colors.GREEN_700,
            "occupied": ft.Colors.RED_700,
            "reserved": ft.Colors.ORANGE_700
        }
        status_text = {
            "available": "ว่าง",
            "occupied": "ไม่ว่าง",
            "reserved": "จองแล้ว"
        }

        status_color = status_colors.get(table.get("status", "available"), ft.Colors.GREEN_700)
        status_label = status_text.get(table.get("status", "available"), "ว่าง")

        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        # Table icon and number
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("🍽️", size=40),
                                    ft.Text(
                                        f"โต๊ะ {table['number']}",
                                        size=18,
                                        weight=ft.FontWeight.BOLD
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5
                            ),
                            bgcolor=ft.Colors.BLUE_50,
                            border_radius=10,
                            padding=15,
                            width=120
                        ),

                        # Table details
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        table.get("name", f"โต๊ะ {table['number']}"),
                                        size=16,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.CHAIR, size=16, color=ft.Colors.GREY_700),
                                            ft.Text(
                                                f"{table.get('seats', 4)} ที่นั่ง",
                                                size=14,
                                                color=ft.Colors.GREY_700
                                            )
                                        ],
                                        spacing=5
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            status_label,
                                            size=12,
                                            color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        bgcolor=status_color,
                                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                        border_radius=15
                                    )
                                ],
                                spacing=8
                            ),
                            expand=True,
                            padding=10
                        ),

                        # Action buttons
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=ft.Colors.BLUE_700,
                                        tooltip="แก้ไข",
                                        on_click=lambda _, t=table: self.show_edit_table_dialog(t)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color=ft.Colors.RED_700,
                                        tooltip="ลบ",
                                        on_click=lambda _, t=table: self.delete_table(t)
                                    )
                                ],
                                spacing=5
                            ),
                            padding=10
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10
            ),
            elevation=2
        )

    def show_add_table_dialog(self, _=None):
        """Show add table dialog"""
        # Input fields
        table_number = ft.TextField(
            label="หมายเลขโต๊ะ",
            hint_text="ระบุหมายเลขโต๊ะ",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        table_name = ft.TextField(
            label="ชื่อโต๊ะ",
            hint_text="เช่น โต๊ะ VIP 1",
            width=200
        )
        table_seats = ft.TextField(
            label="จำนวนที่นั่ง",
            hint_text="ระบุจำนวนที่นั่ง",
            value="4",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        table_status = ft.Dropdown(
            label="สถานะ",
            width=200,
            options=[
                ft.dropdown.Option("available", "ว่าง"),
                ft.dropdown.Option("occupied", "ไม่ว่าง"),
                ft.dropdown.Option("reserved", "จองแล้ว")
            ],
            value="available"
        )

        def add_table(_):
            try:
                # Validate
                if not table_number.value:
                    self.show_error("กรุณาระบุหมายเลขโต๊ะ")
                    return

                number = int(table_number.value)

                # Check duplicate
                if any(t['number'] == number for t in self.tables):
                    self.show_error(f"มีโต๊ะหมายเลข {number} อยู่แล้ว")
                    return

                # Add new table
                new_table = {
                    "id": len(self.tables) + 1,
                    "number": number,
                    "name": table_name.value or f"โต๊ะ {number}",
                    "seats": int(table_seats.value) if table_seats.value else 4,
                    "status": table_status.value
                }

                self.tables.append(new_table)
                self.tables.sort(key=lambda x: x['number'])
                self.save_tables()
                self.display_tables()

                # Close dialog
                add_dialog.open = False
                self.page.update()

                # Show success
                self.show_success(f"เพิ่มโต๊ะ {number} สำเร็จ")

            except ValueError:
                self.show_error("กรุณาระบุตัวเลขที่ถูกต้อง")

        # Create dialog
        add_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("➕ เพิ่มโต๊ะใหม่", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    [
                        table_number,
                        table_name,
                        table_seats,
                        table_status
                    ],
                    spacing=15,
                    tight=True
                ),
                width=300
            ),
            actions=[
                ft.TextButton("ยกเลิก", on_click=lambda _: self.close_dialog(add_dialog)),
                ft.ElevatedButton(
                    "เพิ่มโต๊ะ",
                    on_click=add_table,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.add_dialog = add_dialog
        self.page.overlay.append(self.add_dialog)
        self.add_dialog.open = True
        self.page.update()

    def show_edit_table_dialog(self, table):
        """Show edit table dialog"""
        # Input fields
        table_number = ft.TextField(
            label="หมายเลขโต๊ะ",
            value=str(table['number']),
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        table_name = ft.TextField(
            label="ชื่อโต๊ะ",
            value=table.get('name', f"โต๊ะ {table['number']}"),
            width=200
        )
        table_seats = ft.TextField(
            label="จำนวนที่นั่ง",
            value=str(table.get('seats', 4)),
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        table_status = ft.Dropdown(
            label="สถานะ",
            width=200,
            options=[
                ft.dropdown.Option("available", "ว่าง"),
                ft.dropdown.Option("occupied", "ไม่ว่าง"),
                ft.dropdown.Option("reserved", "จองแล้ว")
            ],
            value=table.get('status', 'available')
        )

        def update_table(_):
            try:
                # Validate
                if not table_number.value:
                    self.show_error("กรุณาระบุหมายเลขโต๊ะ")
                    return

                number = int(table_number.value)

                # Check duplicate (except current table)
                if any(t['number'] == number and t['id'] != table['id'] for t in self.tables):
                    self.show_error(f"มีโต๊ะหมายเลข {number} อยู่แล้ว")
                    return

                # Update table
                table['number'] = number
                table['name'] = table_name.value or f"โต๊ะ {number}"
                table['seats'] = int(table_seats.value) if table_seats.value else 4
                table['status'] = table_status.value

                self.tables.sort(key=lambda x: x['number'])
                self.save_tables()
                self.display_tables()

                # Close dialog
                edit_dialog.open = False
                self.page.update()

                # Show success
                self.show_success(f"อัปเดตโต๊ะ {number} สำเร็จ")

            except ValueError:
                self.show_error("กรุณาระบุตัวเลขที่ถูกต้อง")

        # Create dialog
        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("✏️ แก้ไขโต๊ะ", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    [
                        table_number,
                        table_name,
                        table_seats,
                        table_status
                    ],
                    spacing=15,
                    tight=True
                ),
                width=300
            ),
            actions=[
                ft.TextButton("ยกเลิก", on_click=lambda _: self.close_dialog(edit_dialog)),
                ft.ElevatedButton(
                    "บันทึก",
                    on_click=update_table,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.edit_dialog = edit_dialog
        self.page.overlay.append(self.edit_dialog)
        self.edit_dialog.open = True
        self.page.update()

    def delete_table(self, table):
        """Delete table with confirmation"""
        def confirm_delete(_):
            self.tables = [t for t in self.tables if t['id'] != table['id']]
            self.save_tables()
            self.display_tables()

            # Close dialog
            delete_dialog.open = False
            self.page.update()

            # Show success
            self.show_success(f"ลบโต๊ะ {table['number']} สำเร็จ")

        # Confirmation dialog
        delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED_700, size=32),
                ft.Text("ยืนยันการลบ", size=20, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Text(
                f"คุณต้องการลบโต๊ะ {table['number']} ({table.get('name', '')}) ใช่หรือไม่?",
                size=14
            ),
            actions=[
                ft.TextButton("ยกเลิก", on_click=lambda _: self.close_dialog(delete_dialog)),
                ft.ElevatedButton(
                    "ลบ",
                    on_click=confirm_delete,
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.delete_dialog = delete_dialog
        self.page.overlay.append(self.delete_dialog)
        self.delete_dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        """Close dialog"""
        dialog.open = False
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
            duration=2000
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
