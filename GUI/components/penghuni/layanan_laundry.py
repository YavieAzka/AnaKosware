from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFileDialog, QLineEdit, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtCore import Qt

class BaseDialog(QDialog):
    """Helper class untuk style dialog konsisten"""
    def __init__(self, title, width=480, height=400):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; border: none; }
            QLineEdit { 
                border: 1px solid #CBD5E0; border-radius: 8px; padding: 8px; font-size: 14px; 
            }
            QPushButton#ActionBtn {
                background-color: #FF9966; color: white; border-radius: 10px; 
                padding: 10px; font-weight: bold; border: none;
            }
            QPushButton#ActionBtn:hover { background-color: #FF8C4D; }
            QFrame#Card {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;
            }
        """)

class LaundryInputDialog(BaseDialog):
    def __init__(self):
        super().__init__("Layanan Laundry", 450, 350)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        lbl_title = QLabel("⚖️ Input Berat Cucian")
        lbl_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Desc
        lbl_desc = QLabel("Silakan timbang cucian Anda di ruang tamu.")
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_desc.setStyleSheet("color: #666;")
        layout.addWidget(lbl_desc)

        # Info Harga
        card = QFrame(); card.setObjectName("Card")
        c_layout = QHBoxLayout(card); c_layout.setContentsMargins(20,15,20,15)
        c_layout.addWidget(QLabel("Harga per Kg:"))
        c_layout.addStretch()
        lbl_price = QLabel("Rp 5.000"); lbl_price.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        c_layout.addWidget(lbl_price)
        layout.addWidget(card)

        # Input Row
        row = QHBoxLayout()
        row.addWidget(QLabel("Total Berat (Kg):"))
        self.input_berat = QLineEdit()
        self.input_berat.setPlaceholderText("0")
        self.input_berat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_berat.setFixedWidth(100)
        row.addWidget(self.input_berat)
        layout.addLayout(row)

        layout.addStretch()

        # Button
        btn = QPushButton("Lanjut Pembayaran")
        btn.setObjectName("ActionBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.go_to_payment)
        layout.addWidget(btn)

    def go_to_payment(self):
        val = self.input_berat.text().strip()
        if not val.isdigit() or int(val) <= 0:
            QMessageBox.warning(self, "Input Salah", "Masukkan berat yang valid (angka > 0).")
            return
        self.close()
        dlg = LaundryPaymentDialog(int(val))
        dlg.exec()

class LaundryPaymentDialog(BaseDialog):
    def __init__(self, berat):
        super().__init__("Pembayaran Laundry", 450, 450)
        self.total = berat * 5000
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        lbl_title = QLabel("Rincian Pembayaran")
        lbl_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Rincian
        card = QFrame(); card.setObjectName("Card")
        c_layout = QVBoxLayout(card)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel(f"Laundry ({berat} Kg)"))
        row1.addStretch()
        row1.addWidget(QLabel(f"Rp {self.total:,}"))
        c_layout.addLayout(row1)
        
        layout.addWidget(card)

        # Rekening Info
        lbl_rek = QLabel("Transfer ke:\nBCA 790568301 / GOPAY 085235990976")
        lbl_rek.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_rek.setStyleSheet("color: #555; font-weight: bold; margin: 10px 0;")
        layout.addWidget(lbl_rek)

        layout.addStretch()

        btn = QPushButton("Unggah Bukti Bayar")
        btn.setObjectName("ActionBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.upload_bukti)
        layout.addWidget(btn)

    def upload_bukti(self):
        file, _ = QFileDialog.getOpenFileName(self, "Pilih Bukti", "", "Images (*.png *.jpg *.jpeg)")
        if file:
            QMessageBox.information(self, "Sukses", "Pesanan Laundry berhasil dibuat!")
            self.close()