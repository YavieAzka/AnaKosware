"""
Layanan Page (Penghuni) - Modern PyQt6 Version
Style: Grid Cards, Clean UI, Dark Mode Proof.
"""
import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtCore import Qt

# --- IMPORT DIALOG KOMPONEN ---
try:
    from GUI.components.penghuni.layanan_laundry import LaundryInputDialog
    from GUI.components.penghuni.layanan_catering import CateringInputDialog
    from GUI.components.penghuni.layanan_refill import RefillGalonDialog
    from GUI.components.penghuni.layanan_belanja import BelanjaInputDialog
    from layanan_dan_request.layanan import Layanan
    from layanan_dan_request.request_service import RequestService
except ImportError:
    print("Warning: Komponen layanan tidak ditemukan. Pastikan file ada di folder components/penghuni/")
    LaundryInputDialog = None
    CateringInputDialog = None
    RefillGalonDialog = None
    BelanjaInputDialog = None

class PenghuniLayananPage(QWidget):
    def __init__(self, request_service, user_id):
        super().__init__()
        self.request_service = request_service
        self.user_id = user_id
        
        self.setObjectName("LayananPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self):
        self.setStyleSheet("""
            QWidget#LayananPage {
                background-color: white;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                color: #2D3142;
                border: none;
            }
            /* Card Style khusus ID ServiceCard */
            QFrame#ServiceCard {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
            QFrame#ServiceCard:hover {
                border: 1px solid #FF9966; /* Highlight orange saat hover */
                background-color: #FFFBF8;
            }
            QPushButton {
                background-color: #FF9966;
                color: white;
                border-radius: 10px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF8C4D;
            }
        """)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Title
        title = QLabel("Pesan Layanan")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Grid of Services
        grid = QGridLayout()
        grid.setSpacing(30)

        layanan_list = [
            ("Laundry", "👕"),
            ("Catering", "🍱"),
            ("Refill Galon", "💧"),
            ("Belanja Kebutuhan", "🛒"),
        ]

        row, col = 0, 0
        for nama, icon in layanan_list:
            card = self.create_layanan_card(nama, icon)
            grid.addWidget(card, row, col)
            
            col += 1
            if col > 2: # Max 3 kolom
                col = 0
                row += 1

        main_layout.addLayout(grid)
        main_layout.addStretch()

    def create_layanan_card(self, layanan_name, icon_char):
        card = QFrame()
        card.setObjectName("ServiceCard")
        card.setFixedSize(280, 200)
        
        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20); shadow.setXOffset(0); shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 10))
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Icon Besar
        lbl_icon = QLabel(icon_char)
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_icon.setStyleSheet("font-size: 48px; border: none; background: transparent;")
        
        # Nama Layanan
        lbl_name = QLabel(layanan_name)
        lbl_name.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_name.setStyleSheet("border: none; background: transparent;")

        # Tombol Pesan
        btn = QPushButton("Pesan Sekarang")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Routing logic
        if layanan_name == "Catering":
            btn.clicked.connect(self.show_catering_popup)
        elif layanan_name == "Laundry":
            btn.clicked.connect(self.show_laundry_popup)
        elif layanan_name == "Refill Galon":
            btn.clicked.connect(self.show_refill_popup)
        elif layanan_name == "Belanja Kebutuhan":
            btn.clicked.connect(self.show_belanja_popup)
        else:
            btn.clicked.connect(lambda: self.pesan_layanan(layanan_name))

        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_name)
        layout.addWidget(btn)

        return card

    # --- POPUP HANDLERS ---
    def show_laundry_popup(self):
        if LaundryInputDialog:
            # Kirim dependency ke Dialog
            dlg = LaundryInputDialog(self.request_service, self.user_id)
            dlg.exec()

    def show_catering_popup(self):
        if CateringInputDialog:
            dlg = CateringInputDialog(self.request_service, self.user_id)
            dlg.exec()

    def show_refill_popup(self):
        if RefillGalonDialog:
            dlg = RefillGalonDialog(self.request_service, self.user_id)
            dlg.exec()

    def show_belanja_popup(self):
        if BelanjaInputDialog:
            dlg = BelanjaInputDialog(self.request_service, self.user_id)
            dlg.exec()

    def pesan_layanan(self, layanan):
        QMessageBox.information(self, "Info", f"Layanan {layanan} belum tersedia.")