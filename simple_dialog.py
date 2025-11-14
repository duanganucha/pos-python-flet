#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Dialog Test - Flet
ทดสอบ Dialog แบบง่าย ๆ เพื่อตรวจสอบว่า Dialog แสดงได้
"""
import flet as ft


def main(page: ft.Page):
    """Main app"""
    page.title = "Simple Dialog Test"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Counter
    counter = {"value": 0}

    # Text display
    counter_text = ft.Text(f"Counter: {counter['value']}", size=24, weight=ft.FontWeight.BOLD)

    def show_simple_dialog(e):
        """Show simple dialog"""
        print("show_simple_dialog called")

        def close_dlg(e):
            simple_dlg.open = False
            page.update()

        def increment_dlg(e):
            counter["value"] += 1
            counter_text.value = f"Counter: {counter['value']}"
            simple_dlg.open = False
            page.update()

        simple_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Simple Dialog"),
            content=ft.Text("This is a simple test dialog!"),
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.ElevatedButton(
                    "Increment Counter",
                    on_click=increment_dlg,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE
                )
            ]
        )

        page.dialog = simple_dlg
        simple_dlg.open = True
        page.update()
        print("Dialog should be visible now")

    def show_payment_dialog(e):
        """Show payment dialog with numpad"""
        print("show_payment_dialog called")

        cash_received = {"value": 0}
        total = 123.50

        # Refs
        cash_display_ref = ft.Ref[ft.Text]()
        change_display_ref = ft.Ref[ft.Text]()
        confirm_btn_ref = ft.Ref[ft.ElevatedButton]()

        def update_display():
            """Update displays"""
            cash_display_ref.current.value = f"฿{cash_received['value']:.2f}"
            change = cash_received['value'] - total

            if change >= 0:
                change_display_ref.current.value = f"฿{change:.2f}"
                change_display_ref.current.color = ft.Colors.GREEN_700
                confirm_btn_ref.current.disabled = False
            else:
                change_display_ref.current.value = f"฿{change:.2f}"
                change_display_ref.current.color = ft.Colors.RED_700
                confirm_btn_ref.current.disabled = True

            page.update()

        def on_numpad_click(num):
            """Handle numpad click"""
            if num == "clear":
                cash_received["value"] = 0
            elif num == "backspace":
                cash_received["value"] = int(cash_received["value"] / 10)
            else:
                cash_received["value"] = cash_received["value"] * 10 + num
            update_display()

        def on_quick_amount(amount):
            """Handle quick amount"""
            if amount == "exact":
                cash_received["value"] = total
            else:
                cash_received["value"] = amount
            update_display()

        def close_dlg(e):
            payment_dlg.open = False
            page.update()

        def confirm_payment(e):
            payment_dlg.open = False
            page.update()

            # Show success
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ ชำระเงินสำเร็จ! รับเงิน ฿{cash_received['value']:.2f} ทอน ฿{cash_received['value'] - total:.2f}"),
                bgcolor=ft.Colors.GREEN_700
            )
            page.snack_bar.open = True
            page.update()

        # Build numpad
        numpad_buttons = []
        for row in [[7, 8, 9], [4, 5, 6], [1, 2, 3], [0, "clear", "backspace"]]:
            row_buttons = []
            for num in row:
                if num == "clear":
                    btn = ft.ElevatedButton(
                        "C",
                        on_click=lambda e, n=num: on_numpad_click(n),
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                        height=60
                    )
                elif num == "backspace":
                    btn = ft.ElevatedButton(
                        "⌫",
                        on_click=lambda e, n=num: on_numpad_click(n),
                        bgcolor=ft.Colors.ORANGE_400,
                        color=ft.Colors.WHITE,
                        expand=True,
                        height=60
                    )
                else:
                    btn = ft.ElevatedButton(
                        str(num),
                        on_click=lambda e, n=num: on_numpad_click(n),
                        bgcolor=ft.Colors.GREY_300,
                        color=ft.Colors.BLACK,
                        expand=True,
                        height=60
                    )
                row_buttons.append(btn)
            numpad_buttons.append(ft.Row(row_buttons, spacing=10))

        # Quick amounts
        quick_buttons = []
        for label, amount in [("฿20", 20), ("฿50", 50), ("฿100", 100), ("฿500", 500), ("฿1000", 1000), ("พอดี", "exact")]:
            btn = ft.OutlinedButton(
                label,
                on_click=lambda e, a=amount: on_quick_amount(a),
                expand=True
            )
            quick_buttons.append(btn)

        payment_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("💰 รับชำระเงิน", size=24, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    # Total
                    ft.Container(
                        content=ft.Column([
                            ft.Text("ยอดที่ต้องชำระ", size=14, color=ft.Colors.GREY_700),
                            ft.Text(f"฿{total:.2f}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREEN_50,
                        padding=15,
                        border_radius=10
                    ),

                    # Cash received
                    ft.Container(
                        content=ft.Column([
                            ft.Text("เงินที่รับ", size=14, color=ft.Colors.GREY_700),
                            ft.Text("฿0.00", size=28, weight=ft.FontWeight.BOLD, ref=cash_display_ref)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=15,
                        border_radius=10
                    ),

                    # Change
                    ft.Container(
                        content=ft.Column([
                            ft.Text("เงินทอน", size=14, color=ft.Colors.GREY_700),
                            ft.Text("฿0.00", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700, ref=change_display_ref)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREY_100,
                        padding=15,
                        border_radius=10
                    ),

                    # Quick amounts
                    ft.Text("จำนวนเงินด่วน", size=14, weight=ft.FontWeight.BOLD),
                    ft.Row(quick_buttons[:3], spacing=5),
                    ft.Row(quick_buttons[3:], spacing=5),

                    # Numpad
                    ft.Text("ป้อนจำนวนเงิน", size=14, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column(numpad_buttons, spacing=10),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10
                    )
                ], spacing=15, scroll=ft.ScrollMode.AUTO),
                width=450,
                height=700
            ),
            actions=[
                ft.TextButton("❌ ยกเลิก", on_click=close_dlg),
                ft.ElevatedButton(
                    "✅ ยืนยันการชำระเงิน",
                    on_click=confirm_payment,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE,
                    disabled=True,
                    ref=confirm_btn_ref
                )
            ]
        )

        page.dialog = payment_dlg
        payment_dlg.open = True
        page.update()
        print("Payment dialog should be visible now")

    # UI
    page.add(
        ft.Column(
            [
                ft.Text("Simple Dialog Test", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                counter_text,
                ft.Divider(),
                ft.ElevatedButton(
                    "Show Simple Dialog",
                    on_click=show_simple_dialog,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    height=50,
                    width=300
                ),
                ft.ElevatedButton(
                    "Show Payment Dialog (with Numpad)",
                    on_click=show_payment_dialog,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE,
                    height=50,
                    width=300
                )
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
