from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFileDialog, QLineEdit, QFrame, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


# -------------------------------------------------------
# POPUP 1 — Input Berat
# -------------------------------------------------------
class LaundryInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Laundry")
        self.setModal(True)
        self.setFixedSize(480, 380)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
                border: 1px solid #DDDDDD;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        # CLOSE
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet("background:transparent; border:none; font-size:18px;")
        btn_close.clicked.connect(self.close)
        top = QHBoxLayout()
        top.addStretch()
        top.addWidget(btn_close)
        layout.addLayout(top)

        # TITLE
        title = QLabel("Layanan Laundry")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # DESC
        desc = QLabel(
            "Silakan timbang cucian terlebih dahulu\n"
            "menggunakan timbangan di ruang tamu kos"
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setFont(QFont("Segoe UI", 13))
        layout.addWidget(desc)

        # HARGA
        row_harga = QHBoxLayout()
        row_harga.addWidget(QLabel("Harga :"))
        row_harga.addWidget(QLabel("Rp5.000/kg"))
        row_harga.addStretch()
        layout.addLayout(row_harga)

        # INPUT BERAT
        row_berat = QHBoxLayout()
        row_berat.addWidget(QLabel("Total Berat :"))

        self.input_berat = QLineEdit()
        self.input_berat.setFixedWidth(80)
        self.input_berat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_berat.setStyleSheet("border:1px solid #CCC; border-radius:8px; padding:4px;")
        row_berat.addWidget(self.input_berat)
        row_berat.addWidget(QLabel("Kg"))

        row_berat.addStretch()
        layout.addLayout(row_berat)

        layout.addStretch()

        # BUTTON BAYAR
        btn = QPushButton("Bayar")
        btn.setStyleSheet("background:#E99670; color:white; padding:10px 25px; border-radius:12px;")
        btn.clicked.connect(self.go_to_payment)

        bx = QHBoxLayout()
        bx.addStretch()
        bx.addWidget(btn)
        bx.addStretch()
        layout.addLayout(bx)

        container = QVBoxLayout(self)
        container.addStretch()
        container.addWidget(frame)
        container.addStretch()

        self.setStyleSheet("QDialog { background:rgba(0,0,0,90); }")

    def go_to_payment(self):
        val = self.input_berat.text()
        if not val.isdigit():
            QMessageBox.warning(self, "Input Salah", "Masukkan berat dalam angka.")
            return

        berat = int(val)
        self.close()

        dlg = LaundryPaymentDialog(berat)
        dlg.exec()


# -------------------------------------------------------
# POPUP 2 — Pembayaran + Upload Bukti
# -------------------------------------------------------
class LaundryPaymentDialog(QDialog):
    def __init__(self, berat):
        super().__init__()
        self.berat = berat
        self.harga = 5000
        self.total = berat * self.harga

        self.setWindowTitle("Pembayaran Laundry")
        self.setFixedSize(520, 440)
        self.setModal(True)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 22px;
                border: 1px solid #DDDDDD;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(30, 25, 30, 25)

        # CLOSE
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet("background:transparent; border:none; font-size:18px;")
        btn_close.clicked.connect(self.close)

        top = QHBoxLayout()
        top.addStretch()
        top.addWidget(btn_close)
        layout.addLayout(top)

        # TITLE
        title = QLabel("Layanan Laundry")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # PAYMENT INFO
        info = QLabel(
            "Silakan bayar melalui rekening berikut\n\n"
            "BCA   : 790568301\n"
            "GOPAY : 085235990976"
        )
        info.setFont(QFont("Segoe UI", 13))
        layout.addWidget(info)

        # RINCIAN
        rincian = QFrame()
        rincian.setStyleSheet("""
            QFrame {
                background: #F8F4DE;
                border-radius: 10px;
                border: 1px solid #CFCFCF;
            }
            QLabel { font-size: 14px; }
        """)
        rin_lay = QVBoxLayout(rincian)
        rin_lay.setContentsMargins(20, 14, 20, 14)

        r1 = QHBoxLayout()
        r1.addWidget(QLabel("Laundry"))
        r1.addStretch()
        r1.addWidget(QLabel(f"{self.berat} kg"))
        rin_lay.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Total Harga"))
        r2.addStretch()
        r2.addWidget(QLabel(f"Rp{self.total:,}"))
        rin_lay.addLayout(r2)

        layout.addWidget(rincian)

        # UPLOAD BUTTON
        btn_upload = QPushButton("Unggah Bukti Bayar")
        btn_upload.setStyleSheet("""
            QPushButton {
                background:#E99670; color:white;
                padding:10px 25px; border-radius:12px;
            }
            QPushButton:hover { background:#F1A882; }
        """)
        btn_upload.clicked.connect(self.upload_bukti)

        bx = QHBoxLayout()
        bx.addStretch()
        bx.addWidget(btn_upload)
        bx.addStretch()
        layout.addLayout(bx)

        # BACKGROUND
        container = QVBoxLayout(self)
        container.addStretch()
        container.addWidget(card)
        container.addStretch()

        self.setStyleSheet("QDialog { background:rgba(0,0,0,90); }")

    def upload_bukti(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Unggah Bukti Pembayaran", "", "Images (*.png *.jpg *.jpeg)"
        )

        if file:
            QMessageBox.information(self, "Sukses", "Bukti pembayaran berhasil diupload!")

            # TODO: SIMPAN DATABASE
            # save_service_payment("Laundry", self.berat, self.total, file)

            self.close()
