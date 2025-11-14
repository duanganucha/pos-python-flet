# -*- coding: utf-8 -*-
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class UsersView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)

    def create(self):
        """Create Users view for user management"""
        # Header
        header = ttk.Label(
            self.frame,
            text="👥 จัดการผู้ใช้",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-secondary"
        )
        header.pack(fill=X, pady=(0, 20))

        # Info message
        info_frame = ttk.Frame(self.frame, bootstyle="info", relief="solid", borderwidth=2)
        info_frame.pack(fill=X, pady=(0, 20))

        info_inner = ttk.Frame(info_frame, padding=20)
        info_inner.pack(fill=X)

        ttk.Label(
            info_inner,
            text="ℹ️ ระบบจัดการผู้ใช้",
            font=("Helvetica", 14, "bold"),
            bootstyle="inverse-info"
        ).pack(anchor=W)

        ttk.Label(
            info_inner,
            text="ระบบนี้ช่วยให้คุณจัดการบัญชีผู้ใช้ สิทธิ์การเข้าถึง และบทบาท\nเร็ว ๆ นี้ในการอัปเดตถัดไป!",
            font=("Helvetica", 11),
            bootstyle="inverse-info",
            wraplength=800
        ).pack(anchor=W, pady=(10, 0))

        # Placeholder features list
        features_frame = ttk.Frame(self.frame)
        features_frame.pack(fill=BOTH, expand=YES, pady=(20, 0))

        ttk.Label(features_frame, text="คุณสมบัติที่วางแผนไว้:", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 15))

        features = [
            "👤 Add/Edit/Delete user accounts",
            "🔒 Role-based access control (Admin, Cashier, Manager)",
            "🔑 Password management and reset",
            "📊 User activity logging",
            "⏰ Work shift tracking",
            "📧 Email notifications for new users",
            "🔐 Two-factor authentication (2FA)"
        ]

        for feature in features:
            feature_item = ttk.Frame(features_frame)
            feature_item.pack(fill=X, pady=5)

            ttk.Label(
                feature_item,
                text=feature,
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(anchor=W, padx=20)

        return self.frame
