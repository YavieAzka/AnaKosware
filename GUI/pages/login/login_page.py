import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

# --- IMPORT BACKEND ---
try:
    from auth.auth_service import AuthService 
except ImportError:
    print("Warning: AuthService not found. Database features disabled.")
    AuthService = None

# --- IMPORT MAIN VIEWS ---
try:
    # Import View Pemilik
    from GUI.pages.pemilik.main_view_pemilik import MainViewPemilik
except ImportError:
    print("Warning: MainViewPemilik not found.")
    MainViewPemilik = None

try:
    # Import View Penghuni
    from GUI.pages.penghuni.main_view_penghuni import MainViewPenghuni
except ImportError:
    print("Warning: MainViewPenghuni not found.")
    MainViewPenghuni = None


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

        image_path = r"assets/image/login_pic.jpg" 
        
        pixmap = QPixmap(image_path)
        
        if pixmap.isNull():
            # Fallback UI
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

        # Scale & Crop Image
        scaled_pixmap = pixmap.scaled(
            container_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        cropped = scaled_pixmap.copy(
            (scaled_pixmap.width() - container_size.width()) // 2,
            (scaled_pixmap.height() - container_size.height()) // 2,
            container_size.width(),
            container_size.height()
        )

        self.lbl_background.setPixmap(cropped)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.load_background_image)
        if hasattr(self, 'overlay_widget'):
            self.overlay_widget.resize(self.right_container.size())

    def init_ui(self):
        self.setWindowTitle("AnaKosware - Login")
        self.setGeometry(100, 100, 1200, 700)
        
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #FFFFFF, stop: 0.3 #FFF7E0,
                    stop: 0.6 #FFEBB8, stop: 1 #FFD44D
                );
            }
        """)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # --- LEFT SIDE ---
        left_container = QFrame()
        left_container.setStyleSheet("background-color: transparent;")
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(80, 60, 80, 60)
        left_container.setLayout(left_layout)

        # Logo Area
        logo_title_layout = QHBoxLayout()
        logo_title_layout.setSpacing(15)
        logo_title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        lbl_icon = QLabel()
        logo_path = r"assets/image/AnaKosware_Logo.png"
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            scaled_logo = pixmap.scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            lbl_icon.setPixmap(scaled_logo)
        else:
            lbl_icon.setText("AK")
            lbl_icon.setStyleSheet("background-color: #FFD166; color: #2C2C2C; font-weight: bold; font-size: 20px; border-radius: 12px;")
            lbl_icon.setFixedSize(56, 56)
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_icon.setFixedSize(56, 56)

        lbl_logo_text = QLabel("AnaKosware")
        lbl_logo_text.setStyleSheet("color: #2C2C2C; font-size: 32px; font-weight: bold; font-family: 'Segoe UI', Arial;")

        logo_title_layout.addWidget(lbl_icon)
        logo_title_layout.addWidget(lbl_logo_text)
        logo_title_layout.addStretch()
        left_layout.addLayout(logo_title_layout)

        # Title
        lbl_title = QLabel("Login")
        lbl_title.setStyleSheet("color: #2C2C2C; font-size: 32px; font-weight: 600; margin-top: 60px; margin-bottom: 5px;")

        # Styles
        input_style = """
            QLineEdit, QComboBox {
                background-color: #FFFFFF; border: none; border-radius: 12px;
                padding: 16px 20px; font-size: 14px; color: #2C2C2C; min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus { background-color: #FFFFFF; outline: none; }
            QComboBox::drop-down { border: none; padding-right: 10px; }
            QComboBox::down-arrow {
                image: none; border-left: 5px solid transparent;
                border-right: 5px solid transparent; border-top: 5px solid #666666; margin-right: 10px;
            }
        """

        # Fields
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
        
        pass_container = QFrame()
        pass_container.setStyleSheet("background-color: #FFFFFF; border-radius: 12px;")
        pass_layout = QHBoxLayout(pass_container)
        pass_layout.setContentsMargins(20, 0, 10, 0)
        
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Enter your password")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setStyleSheet("background: transparent; border: none; padding: 16px 0; font-size: 14px; color: #2C2C2C;")
        
        btn_eye = QPushButton("👁")
        btn_eye.setFixedSize(30, 30)
        btn_eye.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_eye.setStyleSheet("background: transparent; border: none; font-size: 16px;")
        btn_eye.clicked.connect(self.toggle_password_visibility)
        
        pass_layout.addWidget(self.txt_password)
        pass_layout.addWidget(btn_eye)

        btn_submit = QPushButton("Submit")
        btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_submit.clicked.connect(self.handle_login)
        btn_submit.setStyleSheet("""
            QPushButton {
                background-color: #FFD166; color: #2C2C2C; font-weight: 600;
                border: none; border-radius: 12px; padding: 16px; font-size: 15px; margin-top: 25px;
            }
            QPushButton:hover { background-color: #FFC850; }
            QPushButton:pressed { background-color: #F0B840; }
        """)

        lbl_terms = QLabel('<a href="#" style="color: #666666; text-decoration: none;">Terms & Conditions</a>')
        lbl_terms.setStyleSheet("font-size: 12px; margin-top: 10px;")

        left_layout.addWidget(lbl_title)
        left_layout.addWidget(lbl_role)
        left_layout.addWidget(self.combo_role)
        left_layout.addWidget(lbl_username)
        left_layout.addWidget(self.txt_username)
        left_layout.addWidget(lbl_password)
        left_layout.addWidget(pass_container)
        left_layout.addWidget(btn_submit)
        left_layout.addStretch()
        left_layout.addWidget(lbl_terms)

        # --- RIGHT SIDE ---
        self.right_container = QFrame()
        self.right_container.setStyleSheet("background-color: #F8F8F8; border-top-left-radius: 40px; border-bottom-left-radius: 40px;")
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.lbl_background = QLabel()
        self.lbl_background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_background.setStyleSheet("border-top-left-radius: 40px; border-bottom-left-radius: 40px;")
        right_layout.addWidget(self.lbl_background)

        # Close Overlay
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
                background-color: rgba(255, 255, 255, 180); color: #444;
                border: none; border-radius: 20px; font-size: 18px; font-weight: bold;
            }
            QPushButton:hover { background-color: #FFD166; color: #2C2C2C; }
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
        msg.setIcon(QMessageBox.Icon.Warning if is_error else QMessageBox.Icon.Information)
        msg.setStyleSheet("""
            QMessageBox { background-color: #FFFFFF; }
            QLabel { color: #2C2C2C; font-size: 13px; padding: 10px; }
            QPushButton {
                background-color: #FFD166; color: #2C2C2C; border: none;
                border-radius: 8px; padding: 8px 24px; font-weight: 600; min-width: 70px;
            }
            QPushButton:hover { background-color: #FFC850; }
        """)
        msg.exec()

    def handle_login(self):
        """Logic Login & Redirect"""
        if not self.auth_service:
            self.show_popup("Error", "Koneksi database tidak tersedia.", True)
            return

        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()
        role_text = self.combo_role.currentText()

        if not username or not password:
            self.show_popup("Validasi Error", "Username dan password tidak boleh kosong!", True)
            return

        role_map = {"Penghuni": "P", "Pemilik": "O", "Penjaga": "S"}
        jenis_akun = role_map.get(role_text)

        try:
            # 1. Cek Login ke Database
            result = self.auth_service.login(jenis_akun, username, password)

            if result["status"] == "success":
                user_data = result["user"]
                
                # 2. Redirect Berdasarkan Role
                
                # --- PEMILIK (Owner) ---
                if jenis_akun == "O": 
                    if MainViewPemilik:
                        self.main_window = MainViewPemilik()
                        # Trigger Property Setter di MainViewPemilik
                        self.main_window.current_user_name = user_data["nama"]
                        self.main_window.current_user_role = role_text
                        self.main_window.show()
                        self.close()
                    else:
                        self.show_popup("Error", "File MainViewPemilik tidak ditemukan.", True)

                # --- PENGHUNI (Tenant) ---
                elif jenis_akun == "P": 
                    if MainViewPenghuni:
                        self.main_window = MainViewPenghuni()
                        
                        # Inject Data ke Variable Internal Penghuni
                        self.main_window._current_user_name = user_data["nama"]
                        self.main_window._current_user_role = "Penghuni Kos"
                        self.main_window._current_user_id = user_data["user_id"]
                        
                        # Update Header (Jika ada method update_user_info)
                        if hasattr(self.main_window, 'header') and self.main_window.header:
                            self.main_window.header.update_user_info(user_data["nama"], "Penghuni Kos")
                        
                        # Refresh Homepage agar nama berubah ("Halo, [Nama]")
                        self.main_window.show_homepage()
                        
                        self.main_window.show()
                        self.close()
                    else:
                        self.show_popup("Error", "File MainViewPenghuni tidak ditemukan.", True)
                
                # --- PENJAGA (Security) ---
                elif jenis_akun == "S": 
                    self.show_popup("Info", f"Login Penjaga: {user_data['nama']}\n(View Penjaga belum tersedia)", False)

            else:
                self.show_popup("Login Gagal", result["message"], True)

        except Exception as e:
            self.show_popup("System Error", f"Terjadi kesalahan: {str(e)}", True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())