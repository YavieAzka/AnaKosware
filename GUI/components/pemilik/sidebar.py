"""
Sidebar component for AnaKosware application - PyQt6 Version
Style: Modern, Minimalist, Flat Design.
Updated: Added 'Manajemen Akun' menu item.
"""
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, 
    QSpacerItem, QSizePolicy, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont, QCursor

class Sidebar(QWidget):
    """Reusable sidebar with navigation menu"""
    
    def __init__(self, parent=None, on_menu_click=None, active_menu='dashboard'):
        super().__init__(parent)
        self.on_menu_click = on_menu_click
        self.active_menu = active_menu
        
        # PENTING: Force styled background
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setFixedWidth(260)
        self.setObjectName("SidebarContainer")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 40, 20, 40)
        self.main_layout.setSpacing(10)

        self._setup_style()
        
        self.create_logo()
        self.main_layout.addSpacing(20)
        self.create_navigation()
        
        self.main_layout.addStretch()
        self.create_logout()

    def _setup_style(self):
        self.setStyleSheet("""
            QWidget#SidebarContainer {
                background-color: #EFE5B7;
            }
            QLabel, QPushButton {
                color: #2D3142;
            }
            QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-radius: 12px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                background-color: transparent;
                color: #2D3142;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.6);
                color: #2D3142;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.8);
                color: #2D3142;
            }
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
            scaled_pixmap = pixmap.scaled(
                150, 150, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            logo_container.setPixmap(scaled_pixmap)
        else:
            logo_container.setText("AnaKosware")
            logo_container.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
            logo_container.setStyleSheet("color: #2D3142;")
            
        self.main_layout.addWidget(logo_container)

    def create_navigation(self):
        # Update Menu List di sini
        menu_items = [
            ("📊", "Dashboard", "dashboard"),
            ("📝", "Daftar Penghuni Baru", "register_tenant"),
            ("⚙️", "Manajemen Akun", "manage_account"), # Menu Baru Ditambahkan
            ("💰", "Riwayat Transaksi", "transaction"),
            ("💬", "Feedback Record", "feedback")
        ]
        
        self.buttons = {}
        
        for icon, text, menu_id in menu_items:
            btn = QPushButton(f"  {icon}   {text}")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setCheckable(True)
            
            if menu_id == self.active_menu:
                btn.setChecked(True)
            
            btn.clicked.connect(lambda checked, mid=menu_id: self.handle_click(mid))
            
            self.main_layout.addWidget(btn)
            self.buttons[menu_id] = btn

    def create_logout(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #DCC9A0; border: none; max-height: 1px;")
        self.main_layout.addWidget(line)
        
        self.main_layout.addSpacing(10)

        logout_btn = QPushButton("  🚪   Logout")
        logout_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        logout_btn.setStyleSheet("""
            QPushButton {
                text-align: left; padding: 12px 20px; border: none;
                border-radius: 12px; font-family: 'Segoe UI'; font-size: 14px;
                background-color: transparent; color: #2D3142;
            }
            QPushButton:hover {
                background-color: #FFEBEE; color: #D32F2F;
            }
        """)
        
        logout_btn.clicked.connect(lambda: self.handle_click('logout'))
        self.main_layout.addWidget(logout_btn)

    def handle_click(self, menu_id):
        if menu_id == 'logout':
            if self.on_menu_click:
                self.on_menu_click(menu_id)
            return

        self.active_menu = menu_id
        for key, btn in self.buttons.items():
            btn.setChecked(False)
        if menu_id in self.buttons:
            self.buttons[menu_id].setChecked(True)
        if self.on_menu_click:
            self.on_menu_click(menu_id)