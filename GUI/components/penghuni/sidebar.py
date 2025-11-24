from PyQt6.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QFont, QCursor
from PyQt6.QtCore import Qt, QSize
import os


class Sidebar(QFrame):
    """Reusable sidebar navigation for role Penghuni"""

    def __init__(self, parent=None, on_menu_click=None, active_menu="homepage"):
        super().__init__(parent)

        self.setStyleSheet("background-color: #EFE5B7;")
        self.setFixedWidth(250)

        self.on_menu_click = on_menu_click
        self.active_menu = active_menu

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.create_logo()
        self.create_navigation()
        self.layout.addStretch()   # push logout to bottom
        self.create_logout()

    # ---------------- LOGO ---------------- #
    def create_logo(self):
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        logo_label = QLabel()
        logo_path = os.path.join("assets", "image", "AnaKosware Logo.png")

        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            pix = pix.scaled(QSize(180, 180), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pix)

        logo_label.setStyleSheet("padding: 25px; background-color: #EFE5B7;")

        logo_layout.addWidget(logo_label)
        self.layout.addLayout(logo_layout)

    # ---------------- MENU SECTION ---------------- #
    def create_navigation(self):
        menu_items = [
            ("🏠", "Homepage", "homepage"),
            ("🛒", "Layanan", "layanan"),
            ("👍", "Berikan Feedback", "berikan_feedback"),
        ]

        for icon, text, menu_id in menu_items:
            self.create_menu_item(icon, text, menu_id)

    def create_menu_item(self, icon, text, menu_id):
        is_active = (menu_id == self.active_menu)

        item = QFrame()
        item.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        bg_color = "white" if is_active else "#EFE5B7"

        item.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 6px;
            }}
            QLabel {{
                color: #2D3142;
            }}
        """)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(15, 10, 15, 10)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 16))
        layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 10, QFont.Weight.Bold if is_active else QFont.Weight.Normal))
        layout.addWidget(text_label)

        layout.addStretch()
        self.layout.addWidget(item)

        # ----- CLICK HANDLER -----
        if self.on_menu_click:
            def handler(_):
                self.on_menu_click(menu_id)
            item.mousePressEvent = handler  # override click event

        # ----- HOVER EFFECT -----
        if not is_active:
            def enter(_):
                item.setStyleSheet("""
                    QFrame { background-color: #DCC9A0; border-radius:6px; }
                    QLabel { color: #2D3142; }
                """)
            def leave(_):
                item.setStyleSheet("""
                    QFrame { background-color: #EFE5B7; border-radius:6px; }
                    QLabel { color: #2D3142; }
                """)
            item.enterEvent = enter
            item.leaveEvent = leave

    # ---------------- LOGOUT ---------------- #
    def create_logout(self):
        container = QFrame()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)

        icon_label = QLabel("🚪")
        icon_label.setFont(QFont("Arial", 16))
        layout.addWidget(icon_label)

        text_label = QLabel("Logout")
        text_label.setFont(QFont("Arial", 10))
        layout.addWidget(text_label)
        layout.addStretch()

        container.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        container.setStyleSheet("background-color: #EFE5B7;")

        self.layout.addWidget(container)

        if self.on_menu_click:
            def logout_click(_):
                self.on_menu_click("logout")
            container.mousePressEvent = logout_click

        # Hover logout
        def enter(_):
            container.setStyleSheet("background-color: #DCC9A0;")
        def leave(_):
            container.setStyleSheet("background-color: #EFE5B7;")

        container.enterEvent = enter
        container.leaveEvent = leave
