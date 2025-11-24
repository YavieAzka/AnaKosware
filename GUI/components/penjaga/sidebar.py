from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import os


class Sidebar(QWidget):
    """Reusable sidebar component with navigation menu"""

    def __init__(self, parent=None, on_menu_click=None, active_menu="dashboard"):
        super().__init__(parent)
        self.on_menu_click = on_menu_click
        self.active_menu = active_menu

        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #EFE5B7;")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 0, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.create_logo()
        self.create_navigation()
        self.create_logout()

    def create_logo(self):
        logo_container = QVBoxLayout()
        logo_container.setContentsMargins(0, 40, 0, 40)

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # load image
        logo_path = os.path.join("assets", "image", "AnaKosware Logo.png")
        pixmap = QPixmap(logo_path).scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)

        logo_container.addWidget(logo_label)
        self.layout.addLayout(logo_container)

    def create_navigation(self):
        menu_items = [
            ("🏠", "Dashboard", "dashboard"),
            ("🛒", "Layanan", "layanan"),
        ]

        for icon, text, menu_id in menu_items:
            self.create_menu_item(icon, text, menu_id)

    def create_menu_item(self, icon, text, menu_id):
        is_active = (menu_id == self.active_menu)

        bg_color = "#FFFFFF" if is_active else "#EFE5B7"
        font_weight = "bold" if is_active else "normal"

        item = QPushButton(f"{icon}  {text}")
        item.setCursor(Qt.CursorShape.PointingHandCursor)
        item.setFixedHeight(45)
        item.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border: none;
                text-align: left;
                padding-left: 18px;
                font-size: 14px;
                font-weight: {font_weight};
                color: #2D3142;
            }}
            QPushButton:hover {{
                background-color: #DCC9A0;
            }}
        """)

        if self.on_menu_click:
            item.clicked.connect(lambda _, m=menu_id: self.on_menu_click(m))

        self.layout.addWidget(item)

    def create_logout(self):
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(spacer)

        logout_btn = QPushButton("🚪  Logout")
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setFixedHeight(45)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #EFE5B7;
                border: none;
                text-align: left;
                padding-left: 18px;
                font-size: 14px;
                color: #2D3142;
            }
            QPushButton:hover {
                background-color: #DCC9A0;
            }
        """)

        if self.on_menu_click:
            logout_btn.clicked.connect(lambda: self.on_menu_click("logout"))

        self.layout.addWidget(logout_btn)
