import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
    QWidget, QFrame, QMessageBox, QGraphicsDropShadowEffect, QLabel
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

# --- IMPORT DATABASE & SERVICES ---
try:
    from database.db_manager import DatabaseManager
    from layanan_dan_request.layanan_service import LayananService
    from layanan_dan_request.request_service import RequestService
except ImportError as e:
    print(f"Database Error: {e}")
    DatabaseManager = None
    LayananService = None
    RequestService = None

# --- IMPORT KOMPONEN UI ---
from GUI.components.penjaga.sidebar import Sidebar 
from GUI.components.penjaga.header import Header 
from GUI.pages.penjaga.dashboard_pesanan import DashboardPenjaga 
from GUI.pages.penjaga.edit_layanan import EditLayanan 

class MainViewPenjaga(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. SETUP DATABASE & SERVICE
        self.db_manager = None
        self.layanan_service = None
        self.request_service = None
        
        if DatabaseManager and LayananService:
            try:
                self.db_manager = DatabaseManager()
                self.layanan_service = LayananService(self.db_manager)
                self.request_service = RequestService(self.db_manager, self.layanan_service)
                print("Services Connected.")
                print("Database & Service Connected Successfully.")
            except Exception as e:
                print(f"Connection Failed: {e}")

        # 2. WINDOW SETUP
        self.setWindowTitle("AnaKosware - Penjaga Kos")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)
        self.current_user_name = "Asep"
        self.current_user_role = "Penjaga Kos"

        self.setStyleSheet("""
            QMainWindow { background-color: #F8FAFC; }
            QFrame#content_area { background-color: white; border-radius: 20px; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QHBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 20, 20)
        self.main_layout.setSpacing(0)

        # 3. SIDEBAR
        self.sidebar = Sidebar(parent=self, on_menu_click=self.handle_navigation, active_menu="dashboard")
        self.sidebar.setFixedWidth(260)
        self.main_layout.addWidget(self.sidebar)

        # 4. CONTENT AREA
        self.content_area = QFrame()
        self.content_area.setObjectName("content_area")
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40); shadow.setColor(QColor(0, 0, 0, 20))
        self.content_area.setGraphicsEffect(shadow)

        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.header = Header(parent=self.content_area, user_name=self.current_user_name, user_role=self.current_user_role)
        self.content_layout.addWidget(self.header)

        self.page_container = QFrame()
        self.page_container.setLayout(QVBoxLayout())
        self.page_container.layout().setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.page_container, stretch=1)

        self.main_layout.addWidget(self.content_area, stretch=1)

        self.show_dashboard()

    def handle_navigation(self, menu_id):
        if menu_id == "dashboard": self.show_dashboard()
        elif menu_id == "edit_layanan": self.show_edit_layanan()
        elif menu_id == "logout": self.handle_logout()
        self.update_sidebar(menu_id)

    def update_sidebar(self, active_menu):
        self.setUpdatesEnabled(False)
        self.main_layout.removeWidget(self.sidebar)
        self.sidebar.deleteLater()
        self.sidebar = Sidebar(parent=self, on_menu_click=self.handle_navigation, active_menu=active_menu)
        self.sidebar.setFixedWidth(280)
        self.main_layout.insertWidget(0, self.sidebar)
        self.setUpdatesEnabled(True)

    def clear_page(self):
        layout = self.page_container.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

    def show_dashboard(self):
        self.clear_page()
        # Inject RequestService ke Dashboard
        if DashboardPenjaga and self.request_service:
            page = DashboardPenjaga(self.request_service) # Kirim Service
            self.page_container.layout().addWidget(page)
        elif DashboardPenjaga: # Fallback jika service mati (tampil dummy/kosong)
             page = DashboardPenjaga(None)
             self.page_container.layout().addWidget(page)
        else:
            self.page_container.layout().addWidget(QLabel("Dashboard Not Found"))

    def show_edit_layanan(self):
        self.clear_page()
        if self.layanan_service:
            # Inject Service ke Halaman
            page = EditLayanan(self.layanan_service)
            self.page_container.layout().addWidget(page)
        else:
            self.page_container.layout().addWidget(QLabel("Error: Layanan Service (Database) tidak terhubung."))

    def handle_logout(self):
        reply = QMessageBox.question(self, "Logout", "Ingin logout?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    win = MainViewPenjaga()
    win.show()
    sys.exit(app.exec())