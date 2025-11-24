"""
Sidebar component for AnaKosware application - PyQt6 Version
Style: Modern, Minimalist, Flat Design.
Fix: Force light background and dark text for visibility in dark mode OS.
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
        
        # PENTING: Atribut ini memaksa widget untuk menggunakan style background-color 
        # yang didefinisikan di QSS, mengatasi masalah transparansi di dark mode.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Setup properti dasar Sidebar
        self.setFixedWidth(260)
        self.setObjectName("SidebarContainer")
        
        # Layout Utama
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 40, 20, 40)
        self.main_layout.setSpacing(10)

        # Setup Style
        self._setup_style()
        
        # Komponen
        self.create_logo()
        self.main_layout.addSpacing(20)
        self.create_navigation()
        
        self.main_layout.addStretch()
        self.create_logout()

    def _setup_style(self):
        """Define CSS styles"""
        # Warna background (#EFE5B7) dan teks (#2D3142) didefinisikan secara eksplisit.
        # Warna teks dipaksa gelap di semua state agar selalu kontras.
        self.setStyleSheet("""
            QWidget#SidebarContainer {
                background-color: #EFE5B7;
            }
            
            /* Tegaskan warna teks gelap untuk semua label dan button di sidebar */
            QLabel, QPushButton {
                color: #2D3142;
            }

            /* Style untuk Menu Button */
            QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-radius: 12px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                background-color: transparent;
                /* Pastikan warna teks selalu gelap */
                color: #2D3142;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.6); /* Lebih solid saat hover */
                color: #2D3142; /* Teks tetap gelap */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.8);
                color: #2D3142;
            }
            
            /* State ketika menu Aktif (Checked) */
            QPushButton[checked="true"] {
                background-color: #FFFFFF;
                color: #000000; /* Hitam pekat saat aktif */
                font-weight: bold;
                border-left: 4px solid #2D3142;
            }
        """)

    def create_logo(self):
        """Create logo section"""
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
            # Fallback: Teks AnaKosware dengan warna gelap eksplisit
            logo_container.setText("AnaKosware")
            logo_container.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
            # Tambahan penegasan warna teks
            logo_container.setStyleSheet("color: #2D3142;")
            
        self.main_layout.addWidget(logo_container)

    def create_navigation(self):
        """Create navigation menu buttons"""
        menu_items = [
            ("🏠", "Dashboard", "dashboard"),
            ("👤", "Daftar Penghuni", "register_tenant"),
            ("📊", "Riwayat Transaksi", "transaction"),
            ("👍", "Feedback Record", "feedback")
        ]
        
        self.buttons = {}
        
        for icon, text, menu_id in menu_items:
            # Catatan: Ikon emoji mungkin masih terlihat terang di beberapa OS dark mode.
            # Solusi terbaik adalah menggunakan QIcon dengan file gambar berwarna hitam.
            btn = QPushButton(f"  {icon}   {text}")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setCheckable(True)
            
            if menu_id == self.active_menu:
                btn.setChecked(True)
            
            btn.clicked.connect(lambda checked, mid=menu_id: self.handle_click(mid))
            
            self.main_layout.addWidget(btn)
            self.buttons[menu_id] = btn

    def create_logout(self):
        """Create logout button"""
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
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-radius: 12px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                background-color: transparent; 
                /* Paksa warna teks gelap */
                color: #2D3142;
            }
            QPushButton:hover {
                background-color: #FFEBEE;
                color: #D32F2F; /* Merah saat hover */
            }
        """)
        
        logout_btn.clicked.connect(lambda: self.handle_click('logout'))
        self.main_layout.addWidget(logout_btn)

    def handle_click(self, menu_id):
        """Handle menu selection logic"""
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

# --- Block Test Standalone ---
if __name__ == "__main__":
    def dummy_callback(menu_id):
        print(f"Menu diklik: {menu_id}")

    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("Sidebar Test - Dark Mode Fix")
    window.resize(900, 600)
    
    # Set background window utama jadi gelap untuk simulasi
    window.setStyleSheet("background-color: #222222;")
    
    layout = QHBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    
    sidebar = Sidebar(window, on_menu_click=dummy_callback, active_menu='dashboard')
    layout.addWidget(sidebar)
    
    content = QLabel("Konten Halaman Disini")
    content.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # Konten area tetap terang
    content.setStyleSheet("background-color: white; font-size: 24px; color: #AAA;")
    layout.addWidget(content, 1)
    
    window.show()
    sys.exit(app.exec())