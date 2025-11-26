import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QDateEdit, QMessageBox,
    QGraphicsDropShadowEffect, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QCursor, QColor

# --- IMPORT BACKEND ---
try:
    from auth.auth_service import AuthService
except ImportError:
    print("Warning: Backend not found.")
    AuthService = None

class DaftarAkunPenghuni(QWidget):
    """Page untuk daftarkan akun baru penghuni"""
    
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        # --- INISIALISASI SERVICE BACKEND ---
        self.auth_service = AuthService() if AuthService else None
        
        self.setObjectName("MainPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self._setup_ui()
        self._setup_styles()
    
    def _setup_ui(self):
        """Create page content"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- 1. Header ---
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(40, 30, 40, 20)
        
        title = QLabel("Daftar Akun Penghuni Baru")
        title.setObjectName("PageTitle")
        header_layout.addWidget(title)
        main_layout.addWidget(header_container)
        
        # --- 2. Scroll Area ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_content.setObjectName("ScrollContent")
        
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(40, 10, 40, 40)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        # --- 3. Form Container ---
        self.form_container = QFrame()
        self.form_container.setObjectName("FormContainer")
        self.form_container.setMaximumWidth(900) 
        self.form_container.setMinimumWidth(600)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25); shadow.setYOffset(5); shadow.setColor(QColor(0, 0, 0, 20))
        self.form_container.setGraphicsEffect(shadow)
        
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(20)
        
        # --- FORM INPUTS ---
        
        # 1. Nama
        self.nama_input = self.create_input_group(form_layout, "Nama Penghuni", "Masukkan Nama Lengkap")
        
        # 2. Row (Tanggal & Telepon)
        row_layout = QHBoxLayout()
        row_layout.setSpacing(30)
        date_container = self.create_date_picker()
        phone_container = self.create_phone_input()
        row_layout.addWidget(date_container, 1)
        row_layout.addWidget(phone_container, 1)
        form_layout.addLayout(row_layout)
        
        # 3. Kamar & Harga
        self.kamar_input = self.create_input_group(form_layout, "Nomor Kamar", "Contoh: A-101")
        self.harga_input = self.create_input_group(form_layout, "Harga Sewa (Rp)", "Contoh: 1500000")
        
        # 4. Alamat Asal (BARU: Ditambahkan agar sesuai backend)
        self.alamat_input = self.create_input_group(form_layout, "Alamat Asal", "Kota atau alamat lengkap asal penghuni")

        # 5. Akun Login
        self.username_input = self.create_input_group(form_layout, "Username Login", "Buat username unik")
        self.password_input = self.create_input_group(form_layout, "Password", "Buat password", is_password=True)
        
        form_layout.addSpacing(20)
        
        # Submit Button
        self.submit_btn = QPushButton("Daftarkan Penghuni")
        self.submit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.submit_btn.clicked.connect(self.submit_form)
        self.submit_btn.setFixedHeight(50)
        
        form_layout.addWidget(self.submit_btn)
        
        scroll_layout.addWidget(self.form_container)
        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)

    # --- Helper Widget Creators ---
    def create_input_group(self, parent_layout, label_text, placeholder, is_password=False):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        label = QLabel(label_text)
        label.setObjectName("FieldLabel")
        
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setMinimumHeight(45)
        if is_password: inp.setEchoMode(QLineEdit.EchoMode.Password)
            
        layout.addWidget(label)
        layout.addWidget(inp)
        parent_layout.addWidget(container)
        return inp

    def create_date_picker(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        label = QLabel("Tanggal Masuk")
        label.setObjectName("FieldLabel")
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd") # Format SQL friendly
        self.date_input.setMinimumHeight(45)
        
        layout.addWidget(label)
        layout.addWidget(self.date_input)
        return container

    def create_phone_input(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        label = QLabel("No. Telepon (WA)")
        label.setObjectName("FieldLabel")
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("08xxxxxxxxxx")
        self.phone_input.setMinimumHeight(45)
        
        layout.addWidget(label)
        layout.addWidget(self.phone_input)
        return container

    def _setup_styles(self):
        self.setStyleSheet("""
            QWidget#MainPage, QWidget#ScrollContent { background-color: white; }
            QLabel#PageTitle { font-family: 'Segoe UI'; font-size: 24px; font-weight: bold; color: #2D3142; }
            QLabel#FieldLabel { font-family: 'Segoe UI'; font-size: 13px; font-weight: 600; color: #64748B; }
            QFrame#FormContainer { background-color: white; border: 1px solid #E2E8F0; border-radius: 16px; }
            QLineEdit, QDateEdit {
                background-color: #F8FAFC; border: 1px solid #CBD5E0; border-radius: 8px;
                padding: 0 12px; font-size: 14px; color: #334155;
            }
            QLineEdit:focus { border: 2px solid #3B82F6; background-color: white; }
            QPushButton {
                background-color: #3B82F6; color: white; font-weight: bold; font-size: 15px;
                border-radius: 8px; border: none;
            }
            QPushButton:hover { background-color: #2563EB; }
        """)

    # --- LOGIC SUBMIT (YANG DIPERBAIKI) ---
    def submit_form(self):
        if not self.auth_service:
            QMessageBox.critical(self, "Error", "Backend Service tidak terhubung.")
            return

        # 1. Ambil Data
        nama = self.nama_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        kamar = self.kamar_input.text().strip()
        telepon = self.phone_input.text().strip()
        alamat = self.alamat_input.text().strip()
        
        # Harga (Handle error jika bukan angka)
        harga_str = self.harga_input.text().strip()
        if not harga_str.isdigit():
            QMessageBox.warning(self, "Validasi", "Harga sewa harus berupa angka (tanpa titik/koma).")
            return
        harga = int(harga_str)

        # Tanggal
        tgl_masuk = self.date_input.date().toString("yyyy-MM-dd")
        # Asumsi: Tanggal jatuh tempo adalah tanggal yang sama bulan depan/bulan ini.
        # Untuk simplifikasi registrasi awal, kita samakan dulu.
        tgl_jatuh_tempo = tgl_masuk 

        # 2. Validasi Dasar
        if not all([nama, username, password, kamar, telepon]):
            QMessageBox.warning(self, "Validasi", "Semua field wajib diisi!")
            return

        # 3. Kirim ke Backend (PENTING: Kirim SEMUA argumen)
        try:
            result = self.auth_service.register_penghuni(
                username=username,
                nama=nama,
                password=password,
                nomor_kamar=kamar,
                harga_kamar=harga,
                tanggal_masuk=tgl_masuk,
                tanggal_jatuh_tempo=tgl_jatuh_tempo,
                nomor_telepon=telepon,
                alamat_asal=alamat
            )

            if result["status"] == "success":
                QMessageBox.information(self, "Berhasil", result["message"])
                self.clear_form()
            else:
                QMessageBox.warning(self, "Gagal", result["message"])

        except Exception as e:
            print(f"Error Submit: {e}")
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan sistem: {e}")

    def clear_form(self):
        self.nama_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.kamar_input.clear()
        self.harga_input.clear()
        self.phone_input.clear()
        self.alamat_input.clear()
        self.date_input.setDate(QDate.currentDate())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    win = DaftarAkunPenghuni()
    win.resize(1000, 800)
    win.show()
    sys.exit(app.exec())