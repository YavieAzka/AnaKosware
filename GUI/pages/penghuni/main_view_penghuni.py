"""
Main Application (Penghuni View)
Integrates: Sidebar, Header, Homepage, Feedback, Layanan
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
    QWidget, QFrame, QMessageBox, QGraphicsDropShadowEffect, QLabel
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

# --- IMPORT KOMPONEN ---
try:
    from GUI.components.penghuni.sidebar import Sidebar
    from GUI.components.pemilik.header import Header
    from GUI.pages.penghuni.homepage_penghuni import PenghuniHomepage
    from GUI.pages.penghuni.berikan_feedback import BerikanFeedback
    # Import Halaman Layanan yang baru dibuat
    from GUI.pages.penghuni.layanan import PenghuniLayananPage
except ImportError as e:
    print(f"Error Importing Components: {e}")
    Sidebar = None
    Header = None
    PenghuniHomepage = None
    BerikanFeedback = None
    PenghuniLayananPage = None

class MainViewPenghuni(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Data User Session (Akan diisi saat login)
        self._current_user_name = "Ahmad Husein"
        self._current_user_role = "Penghuni Kos"
        self._current_user_id = 1

        self.setWindowTitle("AnaKosware - Panel Penghuni")
        self.setGeometry(100, 100, 1280, 800)
        self.setMinimumSize(1100, 650)

        # Global Style
        self.setStyleSheet("""
            QMainWindow { background-color: #F8FAFC; }
            QFrame#content_area { background-color: #FFFFFF; border-radius: 20px; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. SIDEBAR
        if Sidebar:
            self.sidebar = Sidebar(
                parent=self,
                on_menu_click=self.handle_navigation,
                active_menu='homepage'
            )
            self.main_layout.addWidget(self.sidebar)

        # 2. CONTENT AREA
        self.content_area = QFrame()
        self.content_area.setObjectName("content_area")
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30); shadow.setXOffset(0); shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.content_area.setGraphicsEffect(shadow)

        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        if Header:
            self.header = Header(
                parent=self.content_area,
                user_name=self._current_user_name,
                user_role=self._current_user_role
            )
            self.content_layout.addWidget(self.header)

        self.page_container = QFrame()
        self.page_container.setLayout(QVBoxLayout())
        self.page_container.layout().setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.page_container, stretch=1)

        self.main_layout.addWidget(self.content_area, stretch=1)
        self.main_layout.setContentsMargins(0, 0, 20, 20)

        self.show_homepage()

    # --- NAVIGATION LOGIC ---
    def handle_navigation(self, menu_id):
        if menu_id == 'logout':
            self.handle_logout()
            return

        if menu_id == 'homepage': self.show_homepage()
        elif menu_id == 'layanan': self.show_layanan()
        elif menu_id == 'berikan_feedback': self.show_feedback()
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

    def show_homepage(self):
        self.clear_page()
        self.setWindowTitle("AnaKosware - Homepage")
        data = {
            "nama": self._current_user_name,
            "kamar": "A01", "harga": 1500000, "masuk": "15 Jan 2023",
            "bulan_ke": 12, "pembayaran_lunas": False,
            "layanan": {"Laundry": "Done", "Cleaning": "Waiting"}
        }
        if PenghuniHomepage:
            page = PenghuniHomepage(data)
            self.page_container.layout().addWidget(page)

    def show_feedback(self):
        self.clear_page()
        self.setWindowTitle("AnaKosware - Berikan Feedback")
        if BerikanFeedback:
            page = BerikanFeedback(current_user_id=self._current_user_id)
            self.page_container.layout().addWidget(page)

    def show_layanan(self):
        self.clear_page()
        self.setWindowTitle("AnaKosware - Layanan")
        
        # Load Halaman Layanan
        if PenghuniLayananPage:
            page = PenghuniLayananPage()
            self.page_container.layout().addWidget(page)
        else:
            self.page_container.layout().addWidget(QLabel("Halaman Layanan tidak dapat dimuat."))

    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Apakah Anda yakin ingin logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainViewPenghuni()
    window.show()
    sys.exit(app.exec())