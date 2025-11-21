from .db_manager import DatabaseManager
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QMessageBox, 
                             QFrame, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon
from .temp_login_logic import AuthService

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AnaKosware - Login")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #FFFFFF;")  # Background Putih Bersih

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Container Tengah (Card) ---
        # Kita buat container agar elemen tidak melebar seisi layar
        container = QFrame()
        container.setFixedWidth(400) # Lebar fix agar mirip desain
        container.setStyleSheet("background-color: transparent;")
        
        # Layout untuk container
        container_layout = QVBoxLayout()
        container_layout.setSpacing(15)
        container.setLayout(container_layout)

        # 1. Logo & Judul
        # Karena saya tidak punya file gambar logo, saya buat placeholder text bergaya logo
        lbl_logo = QLabel("AnaKosware")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Arial';
                margin-bottom: 5px;
            }
        """)
        
        # Ikon Orang (Simulasi Logo Merah di Gambar)
        lbl_icon = QLabel("♟") # Placeholder icon
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_icon.setStyleSheet("font-size: 60px; color: #D9304F; margin-bottom: -10px;")

        lbl_title = QLabel("Login")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-size: 18px; color: #333333; margin-bottom: 20px;")

        # 2. Form Input
        # Style untuk Input Field (Beige background, rounded)
        input_style = """
            QLineEdit, QComboBox {
                background-color: #FAF8F0; 
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #555;
            }
            QComboBox::drop-down {
                border: 0px;
            }
        """

        # Dropdown Role
        self.combo_role = QComboBox()
        self.combo_role.addItems(["Penghuni", "Pemilik", "Penjaga"])
        self.combo_role.setStyleSheet(input_style)
        self.combo_role.setCursor(Qt.CursorShape.PointingHandCursor)

        # Username
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Username")
        self.txt_username.setStyleSheet(input_style)

        # Password
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Password")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setStyleSheet(input_style)

        # 3. Button Login
        btn_login = QPushButton("LOGIN")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self.handle_login)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #EE8B60; 
                color: white;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                margin-top: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #D97A50;
            }
            QPushButton:pressed {
                background-color: #C06940;
            }
        """)
        
        # Wrapper button agar tidak stretch penuh
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn_login)
        btn_container.addStretch()

        # --- Menyusun Widget ke Container ---
        container_layout.addWidget(lbl_icon)
        container_layout.addWidget(lbl_logo)
        container_layout.addWidget(lbl_title)
        container_layout.addWidget(self.combo_role)
        container_layout.addWidget(self.txt_username)
        container_layout.addWidget(self.txt_password)
        container_layout.addLayout(btn_container)

        # --- Menyusun Container ke Window Utama ---
        # Menggunakan Spacer agar container berada tepat di tengah (Center)
        main_layout.addStretch()
        
        center_h_layout = QHBoxLayout()
        center_h_layout.addStretch()
        center_h_layout.addWidget(container)
        center_h_layout.addStretch()
        
        main_layout.addLayout(center_h_layout)
        main_layout.addStretch()
    
    def show_popup(self, title, message, is_error=False):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        
        # Atur Icon
        if is_error:
            msg.setIcon(QMessageBox.Icon.Warning)
        else:
            msg.setIcon(QMessageBox.Icon.Information)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
            }
            QLabel {
                color: #000000; /* Paksa text hitam */
                font-size: 13px;
            }
            QPushButton {
                background-color: #EE8B60;
                color: white;
                border-radius: 5px;
                padding: 6px 20px;
                font-weight: bold;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #D97A50;
            }
        """)
        
        msg.exec()

    def handle_login(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()
        role_text = self.combo_role.currentText()

        # Mapping dari Teks UI ke Kode Database CHAR(1)
        role_map = {
            "Penghuni": "P",
            "Pemilik":  "O",  # Owner
            "Penjaga":  "S"   # Security/Staff
        }
        jenis_akun = role_map.get(role_text)

        # Panggil Backend
        result = self.auth_service.login(jenis_akun, username, password)

        if result["status"] == "success":
            self.show_popup("Berhasil", f"Selamat datang, {result['user']['nama']}!", is_error=False)
            print(f"User Data: {result['user']}")
        else:
            self.show_popup("Login Gagal", result["message"], is_error=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set font global aplikasi agar lebih estetik
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())