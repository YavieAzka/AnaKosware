import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
    QWidget, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

# ====================================================
# IMPORT KOMPONEN (Sidebar + Header)
# ====================================================
from components.penghuni.sidebar import SidebarPenghuni
from components.penghuni.header import HeaderPenghuni

# ====================================================
# IMPORT HALAMAN (Pages)
# ====================================================
from pages.penghuni.homepage_penghuni import HomepagePenghuni
from pages.penghuni.layanan import PenghuniLayananPage
from pages.penghuni.berikan_feedback import FeedbackPenghuniPage


class MainViewPenghuni(QMainWindow):
    def __init__(self):
        super().__init__()

        # ======= WINDOW SETUP ========
        self.setWindowTitle("AnaKosware - Penghuni Kos")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)

        # ========= USER DATA (from login) =========
        self.current_user_name = "Nama Penghuni"
        self.current_user_role = "Penghuni Kos"

        # ========= GLOBAL STYLE =========
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8FAFC;
            }
            QFrame#content_area {
                background-color: white;
                border-radius: 20px;
            }
        """)

        # ========= MAIN LAYOUT =========
        central = QWidget()
        self.setCentralWidget(central)

        self.main_layout = QHBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 20, 20)
        self.main_layout.setSpacing(0)

        # =====================================
        # SIDEBAR (Penghuni)
        # =====================================
        self.sidebar = SidebarPenghuni(
            parent=self,
            on_menu_click=self.handle_navigation,
            active_menu="homepage"
        )
        self.sidebar.setFixedWidth(260)
        self.main_layout.addWidget(self.sidebar)

        # =====================================
        # CONTENT AREA (Right Panel)
        # =====================================
        self.content_area = QFrame()
        self.content_area.setObjectName("content_area")

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.content_area.setGraphicsEffect(shadow)

        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # ========= HEADER =========
        self.header = HeaderPenghuni(
            parent=self.content_area,
            user_name=self.current_user_name,
            user_role=self.current_user_role
        )
        self.content_layout.addWidget(self.header)

        # ========= PAGE CONTAINER =========
        self.page_container = QFrame()
        self.page_container.setLayout(QVBoxLayout())
        self.page_container.layout().setContentsMargins(40, 30, 40, 40)
        self.content_layout.addWidget(self.page_container, stretch=1)

        # Add to main layout
        self.main_layout.addWidget(self.content_area, stretch=1)

        # Load first page (Homepage)
        self.show_homepage()

    # ============================================================
    #       NAVIGATION HANDLER
    # ============================================================
    def handle_navigation(self, menu_id):
        if menu_id == "homepage":
            self.show_homepage()
        elif menu_id == "layanan":
            self.show_layanan()
        elif menu_id == "feedback":
            self.show_feedback()
        elif menu_id == "logout":
            self.handle_logout()

        # Update active highlight di sidebar
        self.update_sidebar(menu_id)

    def update_sidebar(self, active):
        self.setUpdatesEnabled(False)

        self.main_layout.removeWidget(self.sidebar)
        self.sidebar.deleteLater()

        self.sidebar = SidebarPenghuni(
            parent=self,
            on_menu_click=self.handle_navigation,
            active_menu=active
        )
        self.sidebar.setFixedWidth(260)
        self.main_layout.insertWidget(0, self.sidebar)

        self.setUpdatesEnabled(True)

    # ============================================================
    #       PAGE SWITCHING
    # ============================================================
    def clear_page(self):
        layout = self.page_container.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_homepage(self):
        self.clear_page()
        page = HomepagePenghuni(self.page_container, self)
        self.page_container.layout().addWidget(page)

    def show_layanan(self):
        self.clear_page()
        page = PenghuniLayananPage()
        self.page_container.layout().addWidget(page)

    def show_feedback(self):
        self.clear_page()
        page = FeedbackPenghuniPage()
        self.page_container.layout().addWidget(page)

    # ============================================================
    #       LOGOUT HANDLER
    # ============================================================
    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Logout",
            "Ingin logout dari akun penghuni?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            print("Logout Penghuni...")
            self.close()


# ============================================================
#       RUN FOR TESTING
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    win = MainViewPenghuni()
    win.show()

    sys.exit(app.exec())
