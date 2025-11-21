import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame, 
                             QHBoxLayout, QDateEdit, QScrollArea)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIntValidator

from .register_logic import AuthService
# Import Backend Class (Pastikan kode backend di atas sudah ada)
# from backend import AuthService 

class RegisterPenghuniWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService() # Inisialisasi backend
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AnaKosware - Daftar Penghuni")
        self.setGeometry(100, 100, 600, 750) # Ukuran window portrait
        self.setStyleSheet("background-color: #FFFFFF;")

        # --- Main Layout dengan Scroll Area (agar responsif di layar kecil) ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)

        # 1. Header Title
        lbl_title = QLabel("Daftar Akun Penghuni Baru")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2D3142; margin-bottom: 10px;")
        content_layout.addWidget(lbl_title)

        # 2. Form Container (Dashed Border Frame)
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 2px dashed #D8BFD8; /* Border putus-putus ungu muda sesuai request */
                border-radius: 10px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(15)

        # --- Form Fields Helper ---
        # Kita buat style global untuk input agar rapi
        self.input_style = """
            QLineEdit, QDateEdit {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333;
            }
            QDateEdit::drop-down {
                border: 0px;
            }
        """

        # -- Field: Nama Penghuni --
        form_layout.addWidget(self.create_label("Nama Penghuni"))
        self.txt_nama = QLineEdit()
        self.txt_nama.setPlaceholderText("Masukkan Nama Lengkap")
        self.txt_nama.setStyleSheet(self.input_style)
        form_layout.addWidget(self.txt_nama)

        # -- Field Row: Tanggal Masuk & Telepon --
        row_layout = QHBoxLayout()
        
        # Tanggal Masuk
        date_container = QVBoxLayout()
        date_container.addWidget(self.create_label("Tanggal Masuk"))
        self.date_masuk = QDateEdit()
        self.date_masuk.setCalendarPopup(True) # Modern calendar popup
        self.date_masuk.setDate(QDate.currentDate())
        self.date_masuk.setDisplayFormat("dd/MM/yyyy")
        self.date_masuk.setStyleSheet(self.input_style + "color: #333;") 
        date_container.addWidget(self.date_masuk)
        row_layout.addLayout(date_container, 1) # Stretch factor 1

        row_layout.addSpacing(20)

        # Telepon (+62 Prefix)
        phone_container = QVBoxLayout()
        phone_container.addWidget(self.create_label("Nomor Telepon"))
        
        phone_input_layout = QHBoxLayout()
        lbl_prefix = QLabel("+62")
        lbl_prefix.setStyleSheet("background-color: #F5F5F5; border: 1px solid #E0E0E0; border-radius: 8px; padding: 10px; font-weight: bold; color: #666;")
        phone_input_layout.addWidget(lbl_prefix)
        
        self.txt_telepon = QLineEdit()
        self.txt_telepon.setPlaceholderText("81234567890")
        self.txt_telepon.setValidator(QIntValidator()) # Hanya angka
        self.txt_telepon.setStyleSheet(self.input_style)
        phone_input_layout.addWidget(self.txt_telepon)
        
        phone_container.addLayout(phone_input_layout)
        row_layout.addLayout(phone_container, 1)

        form_layout.addLayout(row_layout)

        # -- Field: Nomor Kamar --
        form_layout.addWidget(self.create_label("Nomor Kamar"))
        self.txt_kamar = QLineEdit()
        self.txt_kamar.setPlaceholderText("Contoh: A-101")
        self.txt_kamar.setStyleSheet(self.input_style)
        form_layout.addWidget(self.txt_kamar)

        # -- Field: Harga Kamar --
        form_layout.addWidget(self.create_label("Harga Kamar (Per Bulan)"))
        self.txt_harga = QLineEdit()
        self.txt_harga.setPlaceholderText("Contoh: 1000000")
        self.txt_harga.setValidator(QIntValidator())
        self.txt_harga.setStyleSheet(self.input_style)
        form_layout.addWidget(self.txt_harga)

        # -- Field: Username --
        form_layout.addWidget(self.create_label("Username Akun"))
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Buat username unik")
        self.txt_username.setStyleSheet(self.input_style)
        form_layout.addWidget(self.txt_username)

        # -- Field: Password --
        form_layout.addWidget(self.create_label("Password"))
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Minimal 6 karakter")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setStyleSheet(self.input_style)
        form_layout.addWidget(self.txt_password)

        # -- Submit Button --
        btn_submit = QPushButton("Daftarkan Akun Penghuni")
        btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_submit.clicked.connect(self.submit_form)
        btn_submit.setStyleSheet("""
            QPushButton {
                background-color: #EE8B60;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #D97A50;
            }
            QPushButton:pressed {
                background-color: #C06940;
            }
        """)
        form_layout.addWidget(btn_submit)

        # Masukkan frame form ke layout utama
        content_layout.addWidget(form_frame)
        content_layout.addStretch()

        # Set Scroll Area widget
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; color: #2D3142; font-size: 13px; border: none;")
        return label

    def show_popup(self, title, message, is_error=False):
        """Custom Popup Style konsisten dengan Login Page"""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        
        if is_error:
            msg.setIcon(QMessageBox.Icon.Warning)
        else:
            msg.setIcon(QMessageBox.Icon.Information)
            
        msg.setStyleSheet("""
            QMessageBox { background-color: #FFFFFF; }
            QLabel { color: #000000; font-size: 13px; }
            QPushButton {
                background-color: #EE8B60; color: white;
                border-radius: 5px; padding: 6px 20px;
                font-weight: bold; min-width: 60px;
            }
            QPushButton:hover { background-color: #D97A50; }
        """)
        msg.exec()

    def submit_form(self):
        # 1. Ambil Data
        data = {
            'nama': self.txt_nama.text().strip(),
            'tanggal_masuk': self.date_masuk.date().toString("yyyy-MM-dd"), # Format SQL
            'telepon': "0" + self.txt_telepon.text().strip(), # Tambah 0 di depan +62 logic bisa disesuaikan
            'nomor_kamar': self.txt_kamar.text().strip(),
            'harga': self.txt_harga.text().strip(),
            'username': self.txt_username.text().strip(),
            'password': self.txt_password.text().strip()
        }

        # 2. Validasi Form (Porting dari Tkinter logic)
        for key, val in data.items():
            if not val:
                self.show_popup("Error Validasi", f"Field {key.replace('_', ' ').title()} harus diisi!", True)
                return

        if not self.txt_telepon.text().isdigit():
             self.show_popup("Error Validasi", "Nomor telepon harus berupa angka!", True)
             return
        
        # Cek panjang telepon (di UI user input misal 812..., ditambah 0 jadi min 10 digit total)
        if len(self.txt_telepon.text()) < 9:
             self.show_popup("Error Validasi", "Nomor telepon minimal 9 digit!", True)
             return

        if ' ' in data['username']:
             self.show_popup("Error Validasi", "Username tidak boleh mengandung spasi!", True)
             return

        if len(data['password']) < 6:
             self.show_popup("Error Validasi", "Password minimal 6 karakter!", True)
             return

        # 3. Kirim ke Backend
        # Sesuaikan no telepon untuk database (misal format 08...)
        # Logic: User input 8123 -> kita simpan 08123
        
        result = self.auth_service.register_penghuni_complete(data)

        if result["status"] == "success":
            self.show_popup("Sukses", result["message"])
            self.clear_form()
        else:
            self.show_popup("Gagal", result["message"], True)

    def clear_form(self):
        self.txt_nama.clear()
        self.txt_telepon.clear()
        self.txt_kamar.clear()
        self.txt_harga.clear()
        self.txt_username.clear()
        self.txt_password.clear()
        self.date_masuk.setDate(QDate.currentDate())

# --- Main Execution untuk Testing ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = RegisterPenghuniWindow()
    window.show()
    sys.exit(app.exec())