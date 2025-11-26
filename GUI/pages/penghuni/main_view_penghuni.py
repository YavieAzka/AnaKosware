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
    from layanan_dan_request.request_service import RequestService
    from GUI.pages.penghuni.layanan import PenghuniLayananPage
except ImportError as e:
    print(f"Error Importing Components: {e}")
    Sidebar = None
    Header = None
    PenghuniHomepage = None
    BerikanFeedback = None
    PenghuniLayananPage = None

try:
    from database.db_manager import DatabaseManager
    from layanan_dan_request.layanan_service import LayananService
    from layanan_dan_request.request_service import RequestService
    # Jika ingin notifikasi tagihan juga (UC04), import NotificationService di sini
    from notification.notification_service import NotificationService 
except ImportError as e:
    print(f"Error Importing Backend Services: {e}")
    DatabaseManager = None
    LayananService = None
    RequestService = None
    NotificationService = None

class MainViewPenghuni(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Data User Session (Akan diisi saat login)
        self._current_user_name = "Ahmad Husein"
        self._current_user_role = "Penghuni Kos"
        self._current_user_id = 1

        self.db = None
        self.layanan_service = None
        self.request_service = None
        self.notification_service = None

        if DatabaseManager and LayananService and RequestService:
            try:
                # 1. Koneksi Database
                self.db = DatabaseManager()
                
                # 2. Init Service Layanan (Butuh DB)
                self.layanan_service = LayananService(self.db)
                
                # 3. Init Service Request (Butuh DB & LayananService)
                self.request_service = RequestService(self.db, self.layanan_service)
                
                # 4. Init Notification Service (Optional untuk Homepage)
                if NotificationService:
                    self.notification_service = NotificationService()
                    
                print("Backend Services Connected Successfully.")
            except Exception as e:
                print(f"Failed to initialize services: {e}")

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
        
        # --- 1. AMBIL DATA PENGHUNI DARI DB ---
        user_data = {
            "nama": self._current_user_name,
            "kamar": "-", "harga": 0, "masuk": "-", 
            "bulan_ke": 0, 
            "bill_status": None,
            "layanan": {}, # Riwayat status layanan
            "rincian_tagihan": [] # List baru untuk rincian
        }

        if self.db:
            try:
                # A. Info Kamar & Harga
                q_info = """
                    SELECT nomor_kamar, harga_kamar, tanggal_masuk 
                    FROM penghuni WHERE user_id = %s
                """
                res_info = self.db.execute_query(q_info, (self._current_user_id,))
                if res_info:
                    row = res_info[0]
                    user_data["kamar"] = row['nomor_kamar']
                    user_data["harga"] = row['harga_kamar']
                    # Hitung bulan ke- (sederhana)
                    if row['tanggal_masuk']:
                        import datetime
                        delta = datetime.date.today() - row['tanggal_masuk']
                        user_data["bulan_ke"] = (delta.days // 30) + 1
                        user_data["masuk"] = row['tanggal_masuk'].strftime("%d %b %Y")

                # B. Status Layanan (Request)
                # Mengambil request terakhir
                q_req = """
                    SELECT l.nama_layanan, r.status_request 
                    FROM request r
                    JOIN layanan l ON r.layanan_id = l.layanan_id
                    WHERE r.user_id = %s
                    ORDER BY r.request_id DESC LIMIT 3
                """
                res_req = self.db.execute_query(q_req, (self._current_user_id,))
                for r in res_req:
                    user_data["layanan"][r['nama_layanan']] = r['status_request']

                # C. Rincian Tagihan (Layanan Belum Dibayar)
                q_bill = """
                    SELECT l.nama_layanan, l.harga_layanan 
                    FROM request r
                    JOIN layanan l ON r.layanan_id = l.layanan_id
                    WHERE r.user_id = %s AND r.status_bayar = 'Belum Dibayar'
                """
                res_bill = self.db.execute_query(q_bill, (self._current_user_id,))
                for b in res_bill:
                    # Handle jika harga_layanan 0 (misal laundry kiloan yg harganya dihitung belakangan/input manual)
                    # Untuk simplifikasi, kita ambil harga dasar dulu
                    user_data["rincian_tagihan"].append({
                        "item": b['nama_layanan'],
                        "harga": b['harga_layanan']
                    })

            except Exception as e:
                print(f"Error fetching homepage data: {e}")

        # --- 2. LOGIKA BILL STATUS (Gabungan Tagihan Bulanan + Layanan) ---
        if self.notification_service:
            try:
                # Cek Tagihan Bulanan
                bill = self.notification_service.get_monthly_bill_notification(self._current_user_id)
                
                # Jika ada tagihan bulanan yang harus dibayar, masukkan ke rincian
                if bill and bill.get('is_due'):
                    user_data['rincian_tagihan'].insert(0, {
                        "item": "Sewa Kos Bulanan",
                        "harga": bill['nominal']
                    })
                
                # Hitung Total Tagihan Keseluruhan
                total_tagihan = sum(item['harga'] for item in user_data['rincian_tagihan'])
                
                # Update object bill_status agar UI homepage bisa menampilkan total yang benar
                if total_tagihan > 0:
                    user_data['bill_status'] = {
                        "type": "danger" if bill and bill.get('type') == 'danger' else "warning",
                        "message": "Anda memiliki tagihan belum dibayar.",
                        "nominal": total_tagihan,
                        "detail_tanggal": bill.get('detail_tanggal') if bill else "Segera",
                        "is_due": True
                    }
                else:
                    # Jika tidak ada tagihan sama sekali
                    user_data['bill_status'] = {
                        "type": "info", "message": "Tidak ada tagihan.", "nominal": 0, "is_due": False
                    }

            except Exception as e:
                print(f"Error fetching bill: {e}")

        if PenghuniHomepage:
            page = PenghuniHomepage(user_data)
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
        
        if PenghuniLayananPage:
            # Sekarang self.request_service SUDAH ADA nilainya
            page = PenghuniLayananPage(self.request_service, self._current_user_id)
            self.page_container.layout().addWidget(page)
        else:
            self.page_container.layout().addWidget(QLabel("Halaman Layanan tidak ditemukan."))

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