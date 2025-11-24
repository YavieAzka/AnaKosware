from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class RefillGalonDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Refill Galon")
        self.setFixedSize(550, 450)

        self.setStyleSheet("""
            QDialog { background: white; border-radius: 20px; }
            QLabel { font-family: Segoe UI; }
            QLineEdit {
                border: 1px solid #BDBDBD;
                border-radius: 8px;
                padding: 4px;
                font-size: 14px;
                width: 60px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # ==========================================
        # TITLE
        # ==========================================
        title = QLabel("Layanan Refill Galon")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # ==========================================
        # PRODUK
        # ==========================================
        produk_frame = QFrame()
        produk_frame.setStyleSheet("""
            QFrame {
                background: #F8F4DE;
                border-radius: 12px;
                border: 1px solid #D6D1B9;
            }
        """)
        p_layout = QVBoxLayout(produk_frame)
        p_layout.setContentsMargins(20, 20, 20, 20)
        p_layout.setSpacing(20)

        # Data produk
        self.produk = [
            ("Le Minerale 15L", 20000),
            ("AQUA 19L", 25000)
        ]

        self.qty_inputs = []

        for nama, harga in self.produk:
            row = QHBoxLayout()
            row.setSpacing(30)

            lbl_nama = QLabel(nama)
            lbl_nama.setFont(QFont("Segoe UI", 13))

            lbl_harga = QLabel(f"Rp{harga:,}".replace(",", "."))
            lbl_harga.setFont(QFont("Segoe UI", 13))

            qty = QLineEdit()
            qty.setFixedWidth(50)
            qty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qty.setPlaceholderText("0")

            self.qty_inputs.append(qty)

            row.addWidget(lbl_nama)
            row.addStretch()
            row.addWidget(lbl_harga)
            row.addWidget(qty)

            p_layout.addLayout(row)

        layout.addWidget(produk_frame)

        # ==========================================
        # BUTTON BAYAR
        # ==========================================
        btn_bayar = QPushButton("Bayar")
        btn_bayar.setFixedSize(120, 40)
        btn_bayar.setStyleSheet("""
            QPushButton {
                background: #E99670;
                color: white;
                border-radius: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #F7A784;
            }
        """)
        btn_bayar.clicked.connect(self.open_payment_popup)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_bayar)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    # ==========================================
    # POPUP PEMBAYARAN
    # ==========================================
    def open_payment_popup(self):
        pesanan = []
        total = 0

        for (nama, harga), input_qty in zip(self.produk, self.qty_inputs):
            try:
                qty = int(input_qty.text())
            except ValueError:
                qty = 0

            if qty > 0:
                pesanan.append((nama, qty, harga * qty))
                total += harga * qty

        if len(pesanan) == 0:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Masukkan minimal 1 galon.")
            return

        self.close()

        dlg = RefillGalonPaymentDialog(pesanan, total)
        dlg.exec()



# ==========================================
# POPUP PEMBAYARAN
# ==========================================
class RefillGalonPaymentDialog(QDialog):
    def __init__(self, pesanan, total_harga):
        super().__init__()
        self.setWindowTitle("Pembayaran Refill Galon")
        self.setFixedSize(500, 430)

        self.setStyleSheet("""
            QDialog { background: white; border-radius: 20px; }
            QLabel { font-family: Segoe UI; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Layanan Refill Galon")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        info = QLabel("Silakan bayar melalui rekening berikut")
        info.setFont(QFont("Segoe UI", 13))
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        rekening = QLabel("BCA     : 790568301\nGOPAY : 085235990976")
        rekening.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        rekening.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(rekening)

        # Rincian Pesanan Frame
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #F8F4DE;
                border-radius: 12px;
                border: 1px solid #D6D1B9;
            }
        """)
        f_layout = QVBoxLayout(frame)
        f_layout.setContentsMargins(20, 20, 20, 20)

        for nama, qty, subtotal in pesanan:
            row = QLabel(f"{nama}     {qty} galon")
            row.setFont(QFont("Segoe UI", 13))
            row.setAlignment(Qt.AlignmentFlag.AlignCenter)
            f_layout.addWidget(row)

        lbl_total = QLabel(f"Total Harga     Rp{total_harga:,}".replace(",", "."))
        lbl_total.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        lbl_total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(lbl_total)

        layout.addWidget(frame)

        # Upload tombol
        btn_upload = QPushButton("Unggah Bukti Bayar")
        btn_upload.setFixedSize(200, 40)
        btn_upload.setStyleSheet("""
            QPushButton {
                background: #E99670;
                color: white;
                border-radius: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #F7A784;
            }
        """)

        row2 = QHBoxLayout()
        row2.addStretch()
        row2.addWidget(btn_upload)
        row2.addStretch()
        layout.addLayout(row2)
