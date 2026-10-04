import sys
from functools import partial
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QMessageBox, QGraphicsDropShadowEffect, QScrollArea,
    QSizePolicy
)
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

# --- IMPORT DIALOG KOMPONEN ---
LaundryInputDialog = None
CateringInputDialog = None
RefillGalonDialog = None
BelanjaInputDialog = None
GenericRequestDialog = None

try:
    from GUI.components.penghuni.layanan_laundry import LaundryInputDialog
    from GUI.components.penghuni.layanan_catering import CateringInputDialog
    from GUI.components.penghuni.layanan_refill import RefillGalonDialog
    from GUI.components.penghuni.layanan_belanja import BelanjaInputDialog
    from GUI.components.penghuni.layanan_generic import GenericRequestDialog
except ImportError:
    pass 

# ============================================================================
# CLASS SERVICE CARD
# ============================================================================
class ServiceCard(QFrame):
    def __init__(self, layanan_obj, parent_callback):
        super().__init__()
        self.layanan_obj = layanan_obj
        self.callback = parent_callback
        
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("ServiceCard")
        self.setFixedSize(280, 230)
        
        # --- STYLE ---
        self.default_style = """
            QFrame#ServiceCard {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 16px;
            }
        """
        self.hover_style = """
            QFrame#ServiceCard {
                background-color: #FFFFFF; border: 2px solid #FF9966; border-radius: 16px;
            }
        """
        self.setStyleSheet(self.default_style)

        # --- SHADOW ---
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20); self.shadow.setXOffset(0); self.shadow.setYOffset(5)
        self.shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(self.shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        # 1. Icon Mapping (Disesuaikan dengan Data Database)
        icon_map = {
            "laundry": "👕",   # Menangkap 'Laundry Kiloan'
            "catering": "🍱",  # Menangkap 'Catering Harian'
            "cleaning": "🧹",  # Menangkap 'Cleaning Service'
            "refill": "💧", "galon": "💧", 
            "belanja": "🛒", "jastip": "🛒",
            "waifu": "🌸"      # Spesial untuk data unik di DB Anda
        }
        
        nama_lower = self.layanan_obj.nama.lower()
        icon_char = "📦" # Default Icon
        
        for key, val in icon_map.items():
            if key in nama_lower:
                icon_char = val
                break

        # 2. Icon Label
        lbl_icon = QLabel(icon_char)
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_icon.setStyleSheet("font-size: 42px; background: transparent; border: none;")
        layout.addWidget(lbl_icon)

        # 3. Nama Layanan
        lbl_name = QLabel(self.layanan_obj.nama)
        lbl_name.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_name.setWordWrap(True)
        lbl_name.setStyleSheet("background: transparent; border: none; color: #2D3142;")
        layout.addWidget(lbl_name)

        # 4. Harga / Deskripsi Singkat
        # Jika harga 0 (seperti Laundry/Catering di data Anda), tampilkan teks 'Harga Bervariasi'
        harga_txt = f"Mulai Rp {self.layanan_obj.harga:,.0f}" if self.layanan_obj.harga > 0 else "Harga Bervariasi"
        
        lbl_price = QLabel(harga_txt)
        lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_price.setStyleSheet("color: #64748B; font-size: 12px; background: transparent; border: none;")
        layout.addWidget(lbl_price)

        layout.addStretch()

        # 5. Tombol Pesan
        self.btn = QPushButton("Pesan Sekarang")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setFixedHeight(38)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9966; color: white; border-radius: 10px;
                font-weight: bold; font-size: 13px; border: none;
            }
            QPushButton:hover { background-color: #FF8C4D; margin-top: 2px; }
        """)
        
        self.btn.clicked.connect(self.on_btn_click) 
        layout.addWidget(self.btn)

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        self.shadow.setBlurRadius(40); self.shadow.setYOffset(8)
        self.shadow.setColor(QColor(0, 0, 0, 30))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        self.shadow.setBlurRadius(20); self.shadow.setYOffset(5)
        self.shadow.setColor(QColor(0, 0, 0, 15))
        super().leaveEvent(event)

    def on_btn_click(self):
        if self.callback:
            self.callback(self.layanan_obj)


# ============================================================================
# PAGE UTAMA
# ============================================================================
class PenghuniLayananPage(QWidget):
    def __init__(self, request_service, user_id):
        super().__init__()
        self.request_service = request_service
        self.user_id = user_id
        self.layanan_service = getattr(request_service, 'layanan_service', None)

        self.setObjectName("LayananPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self):
        self.setStyleSheet("QWidget#LayananPage { background-color: white; }")

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        title = QLabel("Pesan Layanan")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2D3142; border: none;")
        main_layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(content_widget)
        self.grid.setSpacing(30)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.load_layanan_from_db()

    def load_layanan_from_db(self):
        # Bersihkan Grid
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        if not self.layanan_service:
            self.create_dummy_cards() # Fallback
            return

        try:
            layanan_list = self.layanan_service.get_all_layanan()
        except Exception:
            layanan_list = []

        if not layanan_list:
            self.create_dummy_cards()
            return

        row, col = 0, 0
        max_cols = 3

        for layanan in layanan_list:
            card = ServiceCard(layanan, self.handle_click)
            self.grid.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def create_dummy_cards(self):
        class Dummy:
            def __init__(self, n, h): self.nama=n; self.harga=h
        dummies = [Dummy("Laundry Kiloan", 0), Dummy("Catering Harian", 0)]
        for i, d in enumerate(dummies):
            self.grid.addWidget(ServiceCard(d, self.handle_click), 0, i)

    def handle_click(self, layanan_obj):
        # Normalisasi nama (lowercase & strip) untuk pencocokan
        nama = layanan_obj.nama.lower().strip()

        def open_dlg(DialogClass):
            if DialogClass:
                try:
                    dlg = DialogClass(self.request_service, self.user_id)
                    dlg.exec()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Crash: {e}")
            else:
                QMessageBox.warning(self, "Info", "Komponen dialog tidak ditemukan.")

        # --- ROUTING LOGIC ---
        # Menggunakan 'in' untuk mencocokkan sebagian kata (Partial Match)
        # Contoh: "Laundry" akan match dengan "Laundry Kiloan"
        
        if "laundry" in nama:
            open_dlg(LaundryInputDialog)
        
        elif "catering" in nama:
            open_dlg(CateringInputDialog)
        
        elif "refill" in nama or "galon" in nama:
            open_dlg(RefillGalonDialog)
        
        elif "belanja" in nama or "jastip" in nama:
            open_dlg(BelanjaInputDialog)
        
        else:
            # Untuk "Cleaning Service", "Jasa Waifu", dll -> Masuk ke Generic Dialog
            if GenericRequestDialog:
                try:
                    # Kirim object layanan lengkap agar Generic Dialog bisa baca deskripsi/harga
                    dlg = GenericRequestDialog(self.request_service, self.user_id, layanan_obj)
                    dlg.exec()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Generic Dialog Crash: {e}")
            else:
                QMessageBox.warning(self, "Maaf", f"Layanan '{layanan_obj.nama}' belum bisa dipesan.")