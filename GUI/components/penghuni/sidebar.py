"""
Sidebar component for Penghuni - PyQt6 Version
Refactored: Uses QPushButton for robust state management (Hover/Checked).
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QCursor

class Sidebar(QWidget):
    """Reusable sidebar navigation for role Penghuni"""
    
    def __init__(self, parent=None, on_menu_click=None, active_menu='homepage'):
        super().__init__(parent)
        self.on_menu_click = on_menu_click
        self.active_menu = active_menu
        
        # Setup Widget
        self.setFixedWidth(260)
        self.setObjectName("SidebarContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 40, 20, 40)
        self.main_layout.setSpacing(10)

        self._setup_style()
        
        # Components
        self.create_logo()
        self.main_layout.addSpacing(20)
        self.create_navigation()
        self.main_layout.addStretch()
        self.create_logout()

    def _setup_style(self):
        self.setStyleSheet("""
            QWidget#SidebarContainer {
                background-color: #EFE5B7; /* Warna Dasar Krem */
            }
            /* Button Style */
            QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-radius: 12px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #2D3142; /* Teks Selalu Gelap */
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.4);
            }
            /* Active State */
            QPushButton[checked="true"] {
                background-color: #FFFFFF;
                color: #000000;
                font-weight: bold;
                border-left: 4px solid #2D3142;
            }
        """)

    def create_logo(self):
        logo_container = QLabel()
        logo_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_path = os.path.join("assets", "image", "AnaKosware Logo.png")
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_container.setPixmap(scaled_pixmap)
        else:
            logo_container.setText("AnaKosware")
            logo_container.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
            logo_container.setStyleSheet("color: #2D3142;")
            
        self.main_layout.addWidget(logo_container)

    def create_navigation(self):
        menu_items = [
            ("🏠", "Homepage", "homepage"),
            ("🛒", "Layanan", "layanan"),
            ("👍", "Berikan Feedback", "berikan_feedback"),
        ]
        
        self.buttons = {}
        
        for icon, text, menu_id in menu_items:
            btn = QPushButton(f"  {icon}   {text}")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setCheckable(True)
            
            if menu_id == self.active_menu:
                btn.setChecked(True)
            
            # Gunakan lambda dengan checked=False untuk handle click
            btn.clicked.connect(lambda checked, mid=menu_id: self.handle_click(mid))
            
            self.main_layout.addWidget(btn)
            self.buttons[menu_id] = btn

    def create_logout(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #DCC9A0; max-height: 1px;")
        self.main_layout.addWidget(line)
        self.main_layout.addSpacing(10)

        logout_btn = QPushButton("  🚪   Logout")
        logout_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_btn.clicked.connect(lambda: self.handle_click('logout'))
        
        # Style khusus logout (hover merah)
        logout_btn.setStyleSheet("""
            QPushButton {
                text-align: left; padding: 12px 20px; border-radius: 12px;
                font-family: 'Segoe UI'; font-size: 14px; color: #2D3142; background: transparent;
            }
            QPushButton:hover { background-color: #FFEBEE; color: #D32F2F; }
        """)
        self.main_layout.addWidget(logout_btn)

    def handle_click(self, menu_id):
        if menu_id == 'logout':
            if self.on_menu_click: self.on_menu_click(menu_id)
            return

        # Visual update
        for btn in self.buttons.values():
            btn.setChecked(False)
        
        if menu_id in self.buttons:
            self.buttons[menu_id].setChecked(True)
            
        if self.on_menu_click:
            self.on_menu_click(menu_id)