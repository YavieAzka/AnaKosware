"""
Main Application (Penghuni View)
Integrates: Sidebar, Header, Homepage, Feedback, Layanan
Updated: Includes user_id in homepage data for payment processing.
"""
import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
    QWidget, QFrame, QMessageBox, QGraphicsDropShadowEffect, QLabel
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

# --- IMPORT KOMPONEN UI ---
try:
    from GUI.components.penghuni.sidebar import Sidebar
    from GUI.components.pemilik.header import Header
    from GUI.pages.penghuni.homepage_penghuni import PenghuniHomepage
    from GUI.pages.penghuni.berikan_feedback import BerikanFeedback
    from GUI.pages.penghuni.layanan import PenghuniLayananPage
except ImportError as e:
    print(f"Error Importing UI Components: {e}")
    Sidebar = None
    Header = None
    PenghuniHomepage = None
    BerikanFeedback = None
    PenghuniLayananPage = None

# --- IMPORT SERVICE (BACKEND) ---
try:
    from database.db_manager import DatabaseManager
    from layanan_dan_request.layanan_service import LayananService
    from layanan_dan_request.request_service import RequestService
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
        
        # Data User Session
        self._current_user_name = "Ahmad Husein"
        self._current_user_role = "Penghuni Kos"
        self._current_user_id = 1 

        # --- INISIALISASI SERVICE ---
        self.db = None
        self.layanan_service = None
        self.request_service = None
        self.notification_service = None

        if DatabaseManager and LayananService and RequestService:
            try:
                self.db = DatabaseManager()
                self.layanan_service = LayananService(self.db)
                self.request_service = RequestService(self.db, self.layanan_service)
                
                if NotificationService:
                    self.notification_service = NotificationService()
                    
                print("Backend Services Connected Successfully.")
            except Exception as e:
                print(f"Failed to initialize services: {e}")

        self.setWindowTitle("AnaKosware - Panel Penghuni")
        self.setGeometry(100, 100, 1280, 800)
        self.setMinimumSize(1100, 650)

        self.setStyleSheet("""
            QMainWindow { background-color: #F8FAFC; }
            QFrame#content_area { background-color: #FFFFFF; border-radius: 20px; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        if Sidebar:
            self.sidebar = Sidebar(parent=self, on_menu_click=self.handle_navigation, active_menu='homepage')
            self.main_layout.addWidget(self.sidebar)

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
            self.header = Header(parent=self.content_area, user_name=self._current_user_name, user_role=self._current_user_role)
            self.content_layout.addWidget(self.header)

        self.page_container = QFrame()
        self.page_container.setLayout(QVBoxLayout())
        self.page_container.layout().setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.page_container, stretch=1)

        self.main_layout.addWidget(self.content_area, stretch=1)
        self.main_layout.setContentsMargins(0, 0, 20, 20)

        self.show_homepage()

    def handle_navigation(self, menu_id):
        if menu_id == 'logout': self.handle_logout()
        elif menu_id == 'homepage': self.show_homepage()
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
        
        user_data = {
            "user_id": self._current_user_id,  # PENTING: KIRIM ID KE HOMEPAGE
            "nama": self._current_user_name,
            "kamar": "-", "harga": 0, "masuk": "-",
            "bulan_ke": 0,
            "bill_status": None,
            "layanan": [],
            "rincian_tagihan": []
        }

        if self.db:
            try:
                q_info = "SELECT nomor_kamar, harga_kamar, tanggal_masuk FROM penghuni WHERE user_id = %s"
                res_info = self.db.execute_query(q_info, (self._current_user_id,))
                if res_info:
                    row = res_info[0]
                    user_data["kamar"] = row.get('nomor_kamar', '-')
                    user_data["harga"] = row.get('harga_kamar', 0)
                    if row.get('tanggal_masuk'):
                        import datetime
                        delta = datetime.date.today() - row['tanggal_masuk']
                        user_data["bulan_ke"] = (delta.days // 30) + 1
                        user_data["masuk"] = row['tanggal_masuk'].strftime("%d %b %Y")

                q_req = """
                    SELECT 
                        r.request_id,
                        l.nama_layanan,
                        l.harga_layanan,
                        r.status_request,
                        r.status_bayar
                    FROM request r
                    JOIN layanan l ON r.layanan_id = l.layanan_id
                    WHERE r.user_id = %s
                    ORDER BY r.request_id DESC
                    LIMIT 5
                """
                res_req = self.db.execute_query(q_req, (self._current_user_id,))

                user_data["layanan"] = []

                for r in res_req:
                    harga = r.get("harga_layanan", 0) or 0
                    try:
                        harga = int(harga)
                    except:
                        harga = 0

                    status_request = (r.get("status_request") or "").strip()        # Pending / In Progress / Done
                    status_bayar   = (r.get("status_bayar") or "").strip()          # Belum Dibayar / Sudah Dibayar

                    # Untuk tampilan & logika tombol "Bayar", kita utamakan status_bayar
                    status_text = status_bayar if status_bayar else status_request

                    user_data["layanan"].append({
                        "nama": r["nama_layanan"],
                        "status_layanan": status_request or "-",
                        "status_bayar": status_bayar or "-",
                        "harga": harga,                 # dipakai untuk nominal bayar layanan
                        "request_id": r["request_id"],  # dipakai saat pembayaran layanan
                    })

                q_bill = """
                    SELECT 
                        r.request_id,
                        l.nama_layanan,
                        l.harga_layanan,
                        r.catatan
                    FROM request r
                    JOIN layanan l ON r.layanan_id = l.layanan_id
                    WHERE r.user_id = %s
                    AND r.status_bayar = 'Belum Dibayar'
                """
                res_bill = self.db.execute_query(q_bill, (self._current_user_id,))
                if res_bill:
                    for b in res_bill:
                        harga_db = float(b.get('harga_layanan', 0))
                        catatan = b.get('catatan', '')
                        final_price = 0

                        if harga_db > 0:
                            final_price = int(harga_db)
                        else:
                            match = re.search(r'Rp\s*([\d,.]+)', catatan)
                            if match:
                                clean_str = match.group(1).replace(',', '').replace('.', '')
                                if clean_str.isdigit():
                                    final_price = int(clean_str)

                        if final_price > 0:
                            user_data["rincian_tagihan"].append({
                                "item": b['nama_layanan'],
                                "harga": final_price,
                                "jenis": "LAYANAN",
                                "request_id": b["request_id"],
                            })

            except Exception as e: print(f"Error Homepage Data: {e}")

        total_service = sum(item['harga'] for item in user_data['rincian_tagihan'])
        rent_nominal = 0; rent_msg = "Segera"; is_rent_due = False
        
        if self.notification_service:
            try:
                bill = self.notification_service.get_monthly_bill_notification(self._current_user_id)
                if bill and bill.get('is_due'):
                    is_rent_due = True
                    rent_nominal = bill['nominal']
                    rent_msg = bill.get('detail_tanggal', 'Segera')
                    user_data['rincian_tagihan'].insert(0, {
                        "item": "Sewa Kos Bulanan",
                        "harga": int(rent_nominal),
                        "jenis": "TAGIHAN",
                        "request_id": None,
                    })
            except Exception as e: print(f"Notif Error: {e}")

        total_final = total_service + rent_nominal
        if total_final > 0:
            user_data['bill_status'] = {
                "type": "danger" if is_rent_due else "warning", "message": "Anda memiliki tagihan belum dibayar.",
                "nominal": total_final, "detail_tanggal": rent_msg, "is_due": True 
            }
        else:
            user_data['bill_status'] = {"type": "info", "message": "Tidak ada tagihan saat ini.", "nominal": 0, "is_due": False}

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
            page = PenghuniLayananPage(self.request_service, self._current_user_id)
            self.page_container.layout().addWidget(page)
        else:
            self.page_container.layout().addWidget(QLabel("Halaman Layanan tidak ditemukan."))

    def handle_logout(self):
        reply = QMessageBox.question(self, "Logout", "Apakah Anda yakin ingin logout?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes: self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainViewPenghuni()
    window.show()
    sys.exit(app.exec())