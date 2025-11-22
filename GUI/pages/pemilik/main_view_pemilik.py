"""
Main application (Pemilik View) - Modern PyQt6 Version
Fixes: Table readability, Layout glitches (Yellow Box), Removed Tkinter dependency.
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


class MainViewPemilik(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- FIX 1: Hapus Tkinter sepenuhnya ---
        # Mencampur Tkinter & PyQt menyebabkan glitch visual (kotak kuning/artifact).
        
        # === Window Setup ===
        self.setWindowTitle("AnaKosware - Sistem Manajemen Kos")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)

        # --- FIX 2: Styling Global untuk Memperbaiki Tabel Dashboard ---
        # Kita set style global disini agar Table di Dashboard otomatis terkoreksi 
        # warnanya tanpa mengubah kode dashboard satu per satu.
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8FAFC; /* Background abu muda bersih */
            }
            QFrame#content_area {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
            /* FIX TABLE READABILITY */
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F9FAFB; /* Abu sangat muda (bukan biru tua) */
                gridline-color: #E2E8F0;
                selection-background-color: #E0F2FE; /* Biru muda saat dipilih */
                selection-color: #0F172A;
                color: #334155;
                border: none;
            }
            QHeaderView::section {
                background-color: #E2E8F0;
                color: #1E293B;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        # === User Info ===
        self.current_user_name = "Ibu Kos"
        self.current_user_role = "Pemilik Kos"

        # === Layout Utama ===
        # Gunakan widget pusat untuk menampung layout horizontal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout: [Sidebar] [Content Area]
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # === SIDEBAR (Kiri) ===
        # Kita simpan referensi container sidebar agar mudah diganti
        self.sidebar = Sidebar(
            parent=self,
            on_menu_click=self.handle_navigation,
            active_menu='dashboard'
        )
        # Fixed width penting agar sidebar tidak 'gepeng'
        self.sidebar.setFixedWidth(280) 
        self.main_layout.addWidget(self.sidebar)

        # === CONTENT AREA (Kanan) ===
        # Container putih besar di sebelah kanan
        self.content_area = QFrame()
        self.content_area.setObjectName("content_area")
        
        # Shadow effect untuk content area (Estetika Modern)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.content_area.setGraphicsEffect(shadow)

        # Layout vertikal di dalam content area (Header + Page)
        self.content_layout = QVBoxLayout(self.content_area)
        # Margin diset agar konten tidak menempel ke pinggir frame putih
        self.content_layout.setContentsMargins(0, 0, 0, 0) 
        self.content_layout.setSpacing(0)

        # 1. Header
        self.header = Header(
            parent=self.content_area,
            user_name=self.current_user_name,
            user_role=self.current_user_role
        )
        self.content_layout.addWidget(self.header)

        # 2. Page Container (Tempat ganti-ganti halaman)
        self.page_container = QFrame()
        self.page_container.setLayout(QVBoxLayout())
        # Padding di dalam halaman
        self.page_container.layout().setContentsMargins(40, 30, 40, 40)
        self.content_layout.addWidget(self.page_container, stretch=1)

        # Tambahkan content area ke layout utama
        # Stretch=1 memastikan area ini mengambil sisa ruang yang ada
        self.main_layout.addWidget(self.content_area, stretch=1)
        
        # Set margin layout utama untuk memberikan efek "floating" pada content area (Opsional)
        # Jika ingin sidebar menempel penuh ke kiri, set margin left 0.
        # Disini kita beri margin sedikit agar terlihat seperti dashboard modern.
        self.main_layout.setContentsMargins(0, 0, 20, 20) 

        # === Tampilkan halaman pertama ===
        self.show_dashboard()

    # =================================================================
    # LOGIC NAVIGATION
    # =================================================================

    def handle_navigation(self, menu_id):
        """Menangani perpindahan halaman"""
        if menu_id == 'logout':
            self.handle_logout()
            return

        # Pindah Halaman
        if menu_id == 'dashboard':
            self.show_dashboard()
        elif menu_id == 'register_tenant':
            self.show_register_tenant()
        elif menu_id == 'transaction':
            self.show_transaction()
        elif menu_id == 'feedback':
            self.show_feedback()

        # Update tampilan sidebar (Active State)
        self.update_sidebar(menu_id)

    def update_sidebar(self, active_menu):
        """
        Teknik replace widget sidebar.
        Menggunakan setUpdatesEnabled(False) untuk mencegah kedipan (flicker).
        """
        self.setUpdatesEnabled(False) # Matikan update visual sementara
        
        # Hapus sidebar lama
        self.main_layout.removeWidget(self.sidebar)
        self.sidebar.deleteLater()
        
        # Buat sidebar baru dengan state aktif yang baru
        self.sidebar = Sidebar(
            parent=self,
            on_menu_click=self.handle_navigation,
            active_menu=active_menu
        )
        self.sidebar.setFixedWidth(280)
        
        # Masukkan kembali ke posisi awal (index 0)
        self.main_layout.insertWidget(0, self.sidebar)
        
        self.setUpdatesEnabled(True) # Nyalakan kembali

    def clear_page(self):
        """Membersihkan halaman lama sebelum memuat halaman baru"""
        layout = self.page_container.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # --- Page Loaders ---

    def show_dashboard(self):
        self.clear_page()
        self.setWindowTitle("AnaKosware - Dashboard")
        page = DashboardPenghuni(self.page_container, self)
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
        reply = QMessageBox.question(
            self, "Logout", "Apakah Anda yakin ingin logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            print("Logging out...")
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Font Global
    app.setFont(QFont("Segoe UI", 10))

    window = MainViewPemilik()
    window.show()
    sys.exit(app.exec())