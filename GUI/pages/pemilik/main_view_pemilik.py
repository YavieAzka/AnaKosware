"""
Main application (Pemilik View) - Modern PyQt6 Version
Updated: Auto-update Header when user data is set.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
    QWidget, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

# Import komponen & halaman
from GUI.components.pemilik.sidebar import Sidebar
from GUI.components.pemilik.header import Header
from GUI.pages.pemilik.dashboard_penghuni import DashboardPenghuni
from GUI.pages.pemilik.daftar_akun_penghuni import DaftarAkunPenghuni
from GUI.pages.pemilik.riwayat_transaksi import RiwayatTransaksi
from GUI.pages.pemilik.feedback_penghuni import FeedbackPenghuni
from GUI.pages.pemilik.manajemen_akun import ManajemenAkunPage


class MainViewPemilik(QMainWindow):
    def __init__(self):
        super().__init__()

        # Data User (Internal Variables)
        self._current_user_name = "Guest"
        self._current_user_role = "Pemilik Kos"

        # === Window Setup ===
        self.setWindowTitle("AnaKosware - Sistem Manajemen Kos")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)

        # Styling Global
        self.setStyleSheet("""
            QMainWindow { background-color: #F8FAFC; }
            QFrame#content_area { background-color: #FFFFFF; border-radius: 20px; }
            /* FIX TABLE READABILITY */
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F9FAFB;
                gridline-color: #E2E8F0;
                selection-background-color: #E0F2FE;
                selection-color: #0F172A;
                color: #334155;
                border: none;
            }
            QHeaderView::section {
                background-color: #E2E8F0; color: #1E293B;
                padding: 8px; border: none; font-weight: bold;
            }
        """)

        # === Layout Utama ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # === SIDEBAR ===
        self.sidebar = Sidebar(
            parent=self,
            on_menu_click=self.handle_navigation,
            active_menu='dashboard'
        )
        self.sidebar.setFixedWidth(280) 
        self.main_layout.addWidget(self.sidebar)

        # === CONTENT AREA ===
        self.content_area = QFrame()
        self.content_area.setObjectName("content_area")
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40); shadow.setXOffset(0); shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.content_area.setGraphicsEffect(shadow)

        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0) 
        self.content_layout.setSpacing(0)

        # 1. HEADER (Diinisialisasi dengan data default dulu)
        self.header = Header(
            parent=self.content_area,
            user_name=self._current_user_name,
            user_role=self._current_user_role
        )
        self.content_layout.addWidget(self.header)

        # 2. PAGE CONTAINER
        self.page_container = QFrame()
        self.page_container.setLayout(QVBoxLayout())
        self.page_container.layout().setContentsMargins(40, 30, 40, 40)
        self.content_layout.addWidget(self.page_container, stretch=1)

        self.main_layout.addWidget(self.content_area, stretch=1)
        self.main_layout.setContentsMargins(0, 0, 20, 20) 

        # Tampilkan Dashboard
        self.show_dashboard()

    # =================================================================
    # PROPERTY SETTERS (MAGIC FIX)
    # =================================================================
    # Ini memungkinkan kode LoginWindow Anda bekerja tanpa diubah.
    # Saat LoginWindow set 'current_user_name', Header otomatis update.

    @property
    def current_user_name(self):
        return self._current_user_name

    @current_user_name.setter
    def current_user_name(self, value):
        self._current_user_name = value
        # Update Header UI secara real-time
        if hasattr(self, 'header'):
            self.header.update_user_info(value, self._current_user_role)

    @property
    def current_user_role(self):
        return self._current_user_role

    @current_user_role.setter
    def current_user_role(self, value):
        self._current_user_role = value
        # Update Header UI secara real-time
        if hasattr(self, 'header'):
            self.header.update_user_info(self._current_user_name, value)

    # =================================================================
    # LOGIC NAVIGATION
    # =================================================================

    def handle_navigation(self, menu_id):
        if menu_id == 'logout':
            self.handle_logout()
            return

        if menu_id == 'dashboard': self.show_dashboard()
        elif menu_id == 'register_tenant': self.show_register_tenant()
        elif menu_id == 'transaction': self.show_transaction()
        elif menu_id == 'feedback': self.show_feedback()
        elif menu_id == 'manage_account': self.show_manajemen_akun()

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
        self.setWindowTitle("AnaKosware - Dashboard")
        page = DashboardPenghuni(self.page_container, self)
        self.page_container.layout().addWidget(page)
        
    def show_manajemen_akun(self):
        self.clear_page()
        self.setWindowTitle("AnaKosware - Manajemen Akun Penghuni")
        page = ManajemenAkunPage(self.page_container, self)
        self.page_container.layout().addWidget(page)

    def show_register_tenant(self):
        self.clear_page()
        self.setWindowTitle("AnaKosware - Daftar Akun Penghuni")
        page = DaftarAkunPenghuni(self.page_container, self)
        self.page_container.layout().addWidget(page)

    def show_transaction(self):
        self.clear_page()
        self.setWindowTitle("AnaKosware - Riwayat Transaksi")
        page = RiwayatTransaksi(self.page_container, self)
        self.page_container.layout().addWidget(page)

    def show_feedback(self):
        self.clear_page()
        self.setWindowTitle("AnaKosware - Feedback Penghuni")
        page = FeedbackPenghuni(self.page_container, self)
        self.page_container.layout().addWidget(page)

    def handle_logout(self):
        reply = QMessageBox.question(self, "Logout", "Apakah Anda yakin ingin logout?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print("Logging out...")
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    window = MainViewPemilik()
    window.show()
    sys.exit(app.exec())