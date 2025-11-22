import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

# --- IMPORT BACKEND & MAIN VIEW ---
# Pastikan path import ini sesuai dengan struktur folder Anda
try:
    from auth.auth_service import AuthService
except ImportError:
    print("Warning: AuthService not found. Database features disabled.")
    AuthService = None

try:
    # Asumsi file MainViewPemilik disimpan di GUI/main_view_pemilik.py
    # Sesuaikan path ini dengan lokasi file MainViewPemilik Anda!
    from GUI.pages.pemilik.main_view_pemilik import MainViewPemilik
except ImportError:
    print("Warning: MainViewPemilik not found. Redirection disabled.")
    MainViewPemilik = None


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Inisialisasi Service
        if AuthService:
            self.auth_service = AuthService()
        else:
            self.auth_service = None
            
        self.init_ui()
        
        # Load background image after window is shown
        QTimer.singleShot(100, self.load_background_image)

    def load_background_image(self):
        if not hasattr(self, 'lbl_background'):
            return

        # Pastikan path image ini BENAR di komputer Anda
        image_path = r"assets/image/login_pic.jpg" 
        
        pixmap = QPixmap(image_path)
        
        if pixmap.isNull():
            # Fallback UI jika gambar tidak ketemu
            self.lbl_background.setText("🏢")
            self.lbl_background.setStyleSheet("""
                QLabel {
                    background-color: #F5F5F5;
                    border-top-left-radius: 40px;
                    border-bottom-left-radius: 40px;
                    font-size: 180px;
                    color: #DDDDDD;
                }
            """)
            return

        # Ambil ukuran container
        container_size = self.right_container.size()
        if container_size.width() <= 0 or container_size.height() <= 0:
            return

        # Scale dengan aspect ratio, tapi boleh melebihi container (untuk crop)
        scaled_pixmap = pixmap.scaled(
            container_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # Crop tengah jika terlalu besar
        cropped = scaled_pixmap.copy(
            (scaled_pixmap.width() - container_size.width()) // 2,
            (scaled_pixmap.height() - container_size.height()) // 2,
            container_size.width(),
            container_size.height()
        )

        self.lbl_background.setPixmap(cropped)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update background saat resize
        QTimer.singleShot(0, self.load_background_image)
        # Update ukuran overlay
        if hasattr(self, 'overlay_widget'):
            self.overlay_widget.resize(self.right_container.size())

    def init_ui(self):
        self.setWindowTitle("AnaKosware - Login")
        self.setGeometry(100, 100, 1200, 700)
        
        # Gradient background style
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #FFFFFF,
                    stop: 0.3 #FFF7E0,
                    stop: 0.6 #FFEBB8,
                    stop: 1 #FFD44D
                );
            }
        """)

        # Main Layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # --- LEFT SIDE: Form Container ---
        left_container = QFrame()
        left_container.setStyleSheet("background-color: transparent;")
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(80, 60, 80, 60)
        left_container.setLayout(left_layout)

        # Logo + Title Container (horizontal)
        logo_title_layout = QHBoxLayout()
        logo_title_layout.setSpacing(15)
        logo_title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Logo AnaKosware
        lbl_icon = QLabel()
        # Pastikan path logo benar
        logo_path = r"assets/image/AnaKosware_Logo.png"
        
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            scaled_logo = pixmap.scaled(
                56, 56,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            lbl_icon.setPixmap(scaled_logo)
        else:
            # Fallback
            lbl_icon.setText("AK")
            lbl_icon.setStyleSheet("""
                QLabel {
                    background-color: #FFD166;
                    color: #2C2C2C;
                    font-weight: bold;
                    font-size: 20px;
                    border-radius: 12px;
                }
            """)
            lbl_icon.setFixedSize(56, 56)
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_icon.setFixedSize(56, 56)

        # Title AnaKosware (besar)
        lbl_logo_text = QLabel("AnaKosware")
        lbl_logo_text.setStyleSheet("""
            QLabel {
                color: #2C2C2C;
                font-size: 32px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial;
            }
        """)

        # Tambahkan ke layout horizontal
        logo_title_layout.addWidget(lbl_icon)
        logo_title_layout.addWidget(lbl_logo_text)
        logo_title_layout.addStretch()

        # Tambahkan layout logo + title
        left_layout.addLayout(logo_title_layout)

        # Title Page
        lbl_title = QLabel("Login")
        lbl_title.setStyleSheet("""
            QLabel {
                color: #2C2C2C;
                font-size: 32px;
                font-weight: 600;
                margin-top: 60px;
                margin-bottom: 5px;
                margin-left: 0px;
            }
        """)

        # Modern Input Style
        input_style = """
            QLineEdit, QComboBox {
                background-color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 16px 20px;
                font-size: 14px;
                color: #2C2C2C;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #FFFFFF;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 10px;
            }
        """

        # Form Fields
        lbl_role = QLabel("Role")
        lbl_role.setStyleSheet("color: #2C2C2C; font-size: 13px; margin-top: 10px; margin-bottom: 5px;")
        
        self.combo_role = QComboBox()
        self.combo_role.addItems(["Penghuni", "Pemilik", "Penjaga"])
        self.combo_role.setStyleSheet(input_style)
        self.combo_role.setCursor(Qt.CursorShape.PointingHandCursor)

        lbl_username = QLabel("Username")
        lbl_username.setStyleSheet("color: #2C2C2C; font-size: 13px; margin-top: 15px; margin-bottom: 5px;")
        
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Enter your username")
        self.txt_username.setStyleSheet(input_style)

        lbl_password = QLabel("Password")
        lbl_password.setStyleSheet("color: #2C2C2C; font-size: 13px; margin-top: 15px; margin-bottom: 5px;")
        
        # Password container
        password_container = QFrame()
        password_container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)
        password_layout = QHBoxLayout()
        password_layout.setContentsMargins(20, 0, 10, 0)
        password_layout.setSpacing(5)
        password_container.setLayout(password_layout)
        
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Enter your password")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                padding: 16px 0px;
                font-size: 14px;
                color: #2C2C2C;
            }
        """)
        
        btn_toggle_password = QPushButton("👁")
        btn_toggle_password.setFixedSize(30, 30)
        btn_toggle_password.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_toggle_password.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
                border-radius: 5px;
            }
        """)
        btn_toggle_password.clicked.connect(self.toggle_password_visibility)
        
        password_layout.addWidget(self.txt_password)
        password_layout.addWidget(btn_toggle_password)

        # Submit Button
        btn_submit = QPushButton("Submit")
        btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_submit.clicked.connect(self.handle_login)
        btn_submit.setStyleSheet("""
            QPushButton {
                background-color: #FFD166;
                color: #2C2C2C;
                font-weight: 600;
                border: none;
                border-radius: 12px;
                padding: 16px;
                font-size: 15px;
                margin-top: 25px;
            }
            QPushButton:hover {
                background-color: #FFC850;
            }
            QPushButton:pressed {
                background-color: #F0B840;
            }
        """)

        # Terms link
        lbl_terms = QLabel('<a href="#" style="color: #666666; text-decoration: none;">Terms & Conditions</a>')
        lbl_terms.setOpenExternalLinks(False)
        lbl_terms.setStyleSheet("font-size: 12px; margin-top: 10px;")

        # Add all widgets to left layout
        left_layout.addWidget(lbl_title)
        left_layout.addWidget(lbl_role)
        left_layout.addWidget(self.combo_role)
        left_layout.addWidget(lbl_username)
        left_layout.addWidget(self.txt_username)
        left_layout.addWidget(lbl_password)
        left_layout.addWidget(password_container)
        left_layout.addWidget(btn_submit)
        left_layout.addStretch()
        left_layout.addWidget(lbl_terms)

        # --- RIGHT SIDE: Image/Visual Container ---
        self.right_container = QFrame()
        self.right_container.setStyleSheet("""
            QFrame {
                background-color: #F8F8F8;
                border-top-left-radius: 40px;
                border-bottom-left-radius: 40px;
            }
        """)
        
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Background label
        self.lbl_background = QLabel()
        self.lbl_background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_background.setStyleSheet("""
            QLabel {
                border-top-left-radius: 40px;
                border-bottom-left-radius: 40px;
            }
        """)
        self.lbl_background.setScaledContents(False)

        right_layout.addWidget(self.lbl_background)

        # Overlay untuk tombol close
        self.overlay_widget = QWidget(self.right_container)
        self.overlay_widget.setStyleSheet("background: transparent;")
        overlay_layout = QVBoxLayout(self.overlay_widget)
        overlay_layout.setContentsMargins(20, 20, 20, 20)

        close_layout = QHBoxLayout()
        close_layout.addStretch()

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(40, 40)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.close)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 180);
                color: #444444;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFD166;
                color: #2C2C2C;
            }
        """)
        close_layout.addWidget(btn_close)
        overlay_layout.addLayout(close_layout)
        overlay_layout.addStretch()

        self.overlay_widget.raise_()

        main_layout.addWidget(left_container, 45)
        main_layout.addWidget(self.right_container, 55)

    def toggle_password_visibility(self):
        if self.txt_password.echoMode() == QLineEdit.EchoMode.Password:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)

    def show_popup(self, title, message, is_error=False):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        
        if is_error:
            msg.setIcon(QMessageBox.Icon.Warning)
        else:
            msg.setIcon(QMessageBox.Icon.Information)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
            }
            QLabel {
                color: #2C2C2C;
                font-size: 13px;
                padding: 10px;
            }
            QPushButton {
                background-color: #FFD166;
                color: #2C2C2C;
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                font-weight: 600;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #FFC850;
            }
        """)
        msg.exec()

    def handle_login(self):
        """Menangani logika login"""
        # 1. Cek apakah service tersedia
        if not self.auth_service:
            self.show_popup("Error", "Koneksi database tidak tersedia.", is_error=True)
            return

        # 2. Ambil data input
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()
        role_text = self.combo_role.currentText()

        # 3. Validasi sederhana
        if not username or not password:
            self.show_popup("Validasi Error", "Username dan password tidak boleh kosong!", is_error=True)
            return

        # 4. Mapping Role (UI Text -> Database Code)
        role_map = {
            "Penghuni": "P",
            "Pemilik":  "O",
            "Penjaga":  "S"
        }
        jenis_akun = role_map.get(role_text)

        try:
            # 5. Panggil Backend
            result = self.auth_service.login(jenis_akun, username, password)

            if result["status"] == "success":
                user_data = result["user"]
                
                # --- LOGIC REDIRECT BERDASARKAN ROLE ---
                
                if jenis_akun == "O": # Jika Pemilik
                    if MainViewPemilik:
                        # Buat window utama Pemilik
                        self.main_window = MainViewPemilik()
                        # (Opsional) Oper data user ke window utama jika perlu
                        self.main_window.current_user_name = user_data["nama"]
                        self.main_window.current_user_role = role_text
                        
                        self.main_window.show()
                        self.close() # Tutup login
                    else:
                        self.show_popup("Error", "File MainViewPemilik tidak ditemukan.", is_error=True)

                elif jenis_akun == "P": # Jika Penghuni
                    # Placeholder untuk View Penghuni
                    self.show_popup("Login Berhasil", f"Selamat datang Penghuni: {user_data['nama']}\n(Halaman Penghuni Coming Soon)", is_error=False)
                
                elif jenis_akun == "S": # Jika Penjaga
                    # Placeholder untuk View Penjaga
                    self.show_popup("Login Berhasil", f"Selamat datang Penjaga: {user_data['nama']}\n(Halaman Penjaga Coming Soon)", is_error=False)

            else:
                # Login Gagal
                self.show_popup("Login Gagal", result["message"], is_error=True)

        except Exception as e:
            self.show_popup("System Error", f"Terjadi kesalahan: {str(e)}", is_error=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set modern font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())