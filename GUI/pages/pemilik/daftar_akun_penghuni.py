import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QDateEdit, QMessageBox,
    QGraphicsDropShadowEffect, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QCursor, QColor

class DaftarAkunPenghuni(QWidget):
    """Page untuk daftarkan akun baru penghuni"""
    
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        # Setup properti dasar
        self.setObjectName("MainPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self._setup_ui()
        self._setup_styles()
    
    def _setup_ui(self):
        """Create page content"""
        # --- Layout Utama Halaman ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Hilangkan margin luar agar full
        main_layout.setSpacing(0)
        
        # --- 1. Header Title (Tetap diam di atas) ---
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(40, 30, 40, 20)
        
        title = QLabel("Daftar Akun Penghuni Baru")
        title.setObjectName("PageTitle")
        header_layout.addWidget(title)
        
        main_layout.addWidget(header_container)
        
        # --- 2. Scroll Area (Agar responsif di layar apapun) ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) # Penting! Agar konten bisa resize
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame) # Hilangkan border scroll area
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container untuk isi Scroll Area
        scroll_content = QWidget()
        scroll_content.setObjectName("ScrollContent")
        
        # Layout untuk memusatkan Form di tengah Scroll Area
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(40, 10, 40, 40) # Margin agar shadow tidak terpotong
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        # --- 3. Form Container (Kotak Putus-putus) ---
        self.form_container = QFrame()
        self.form_container.setObjectName("FormContainer")
        # Batasi lebar maksimum agar form tidak terlalu lebar saat full screen
        self.form_container.setMaximumWidth(900) 
        self.form_container.setMinimumWidth(600)
        
        # Efek Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.form_container.setGraphicsEffect(shadow)
        
        # Layout ISIAN Form
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(25)
        
        # --- Field Input ---
        
        # Nama
        self.nama_input = self.create_input_group(form_layout, "Nama Penghuni", "Masukkan Nama Penghuni")
        
        # Row: Tanggal & Telepon
        row_layout = QHBoxLayout()
        row_layout.setSpacing(30)
        
        # Tanggal
        date_container = self.create_date_picker()
        row_layout.addWidget(date_container, 1)
        
        # Telepon
        phone_container = self.create_phone_input()
        row_layout.addWidget(phone_container, 1)
        
        form_layout.addLayout(row_layout)
        
        # Sisanya
        self.kamar_input = self.create_input_group(form_layout, "Nomor Kamar Penghuni", "Masukkan Nomor Kamar")
        self.harga_input = self.create_input_group(form_layout, "Harga Kamar Penghuni", "Masukkan Harga (Rp.)")
        self.username_input = self.create_input_group(form_layout, "Username Akun Penghuni", "Masukkan Username")
        self.password_input = self.create_input_group(form_layout, "Password Penghuni", "Masukkan Password", is_password=True)
        
        form_layout.addSpacing(20)
        
        # Tombol Submit
        self.submit_btn = QPushButton("Daftarkan Akun Penghuni")
        self.submit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.submit_btn.clicked.connect(self.submit_form)
        self.submit_btn.setFixedHeight(55) # Height fix
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn, 3)
        btn_layout.addStretch()
        form_layout.addLayout(btn_layout)
        
        # Finishing Layout hierarchy
        scroll_layout.addWidget(self.form_container)
        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)

    # --- Helper Methods ---

    def create_input_group(self, parent_layout, label_text, placeholder, is_password=False):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        label = QLabel(label_text)
        label.setObjectName("FieldLabel")
        
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setMinimumHeight(50) # Pastikan tinggi cukup
        # Set Policy agar tidak bisa diperkecil paksa oleh layout
        inp.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        if is_password:
            inp.setEchoMode(QLineEdit.EchoMode.Password)
            
        layout.addWidget(label)
        layout.addWidget(inp)
        parent_layout.addWidget(container)
        return inp

    def create_date_picker(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        label = QLabel("Tanggal Masuk")
        label.setObjectName("FieldLabel")
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setMinimumHeight(50)
        self.date_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.date_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        layout.addWidget(label)
        layout.addWidget(self.date_input)
        return container

    def create_phone_input(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        label = QLabel("Nomor Telepon Penghuni")
        label.setObjectName("FieldLabel")
        
        input_group = QWidget()
        ig_layout = QHBoxLayout(input_group)
        ig_layout.setContentsMargins(0, 0, 0, 0)
        ig_layout.setSpacing(0)
        
        prefix = QLabel("+62")
        prefix.setObjectName("PrefixLabel")
        prefix.setFixedSize(60, 50) # Fixed size match input height
        prefix.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("8123456789")
        self.phone_input.setMinimumHeight(50)
        self.phone_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.phone_input.setStyleSheet("border-top-left-radius: 0; border-bottom-left-radius: 0; border-left: 0;")
        
        ig_layout.addWidget(prefix)
        ig_layout.addWidget(self.phone_input)
        
        layout.addWidget(label)
        layout.addWidget(input_group)
        return container

    def _setup_styles(self):
        self.setStyleSheet("""
            QWidget#MainPage, QWidget#ScrollContent {
                background-color: white;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            
            /* Typography */
            QLabel#PageTitle {
                font-family: 'Segoe UI', sans-serif;
                font-size: 26px;
                font-weight: 800;
                color: #2D3142;
            }
            QLabel#FieldLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 700;
                color: #4A5568;
            }
            
            /* Form Box */
            QFrame#FormContainer {
                background-color: white;
                border: 1px dashed #E2E8F0; /* Warna border lebih halus */
                border-radius: 20px;
            }
            
            /* Input Fields */
            QLineEdit, QDateEdit {
                background-color: #F8FAFC; /* Warna background input sedikit abu */
                border: 1px solid #CBD5E0;
                border-radius: 10px;
                padding: 0 15px;
                font-size: 15px;
                color: #2D3748;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit:focus, QDateEdit:focus {
                background-color: white;
                border: 2px solid #FF9966; /* Highlight orange */
            }
            
            /* Phone Prefix */
            QLabel#PrefixLabel {
                background-color: #EDF2F7;
                border: 1px solid #CBD5E0;
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
                font-weight: bold;
                color: #4A5568;
                font-size: 15px;
            }
            
            /* Button */
            QPushButton {
                background-color: #FF9966;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 27px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF8C4D;
                margin-top: 2px; /* Efek tekan halus */
            }
            QPushButton:pressed {
                background-color: #E67300;
            }
        """)

    def submit_form(self):
        # Logic validasi sama seperti sebelumnya
        data = {
            'nama': self.nama_input.text(),
            'tanggal_masuk': self.date_input.date().toString("dd/MM/yyyy"),
            'telepon': self.phone_input.text(),
            'kamar': self.kamar_input.text(),
            'harga': self.harga_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }
        print("Data Submitted:", data)
        QMessageBox.information(self, "Sukses", "Data berhasil disimpan!")
        self.clear_form()

    def clear_form(self):
        self.nama_input.clear()
        self.phone_input.clear()
        self.kamar_input.clear()
        self.harga_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.date_input.setDate(QDate.currentDate())

# --- Test Standalone ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = DaftarAkunPenghuni()
    window.resize(1200, 800) # Test ukuran besar
    window.show()
    
    sys.exit(app.exec())