from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QFileDialog, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt6.QtCore import Qt
import os

# Pop up kalau mau membayar
class PembayaranDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pembayaran Kos")
        self.setModal(True)
        self.setFixedSize(480, 380)

        # styling frame (agar tampak seperti card pop-up)
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
                border: 1px solid #DDDDDD;
            }
        """)

        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(30, 25, 30, 25)
        frame_layout.setSpacing(18)

        # =====================
        # CLOSE BUTTON (X)
        # =====================
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 18px;
                background-color: transparent;
            }
            QPushButton:hover {
                color: #B00000;
            }
        """)
        close_btn.clicked.connect(self.close)

        top_row = QHBoxLayout()
        top_row.addStretch()
        top_row.addWidget(close_btn)
        frame_layout.addLayout(top_row)

        # =====================
        # TITLE
        # =====================
        title = QLabel("Pembayaran Kos")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame_layout.addWidget(title)
        frame_layout.addSpacing(10)

        # =====================
        # TEXT REKENING
        # =====================
        info = QLabel(
            "Silakan transfer melalui rekening berikut\n\n"
            "BCA        : 740411403\n"
            "BNI        : 159837200\n"
            "MANDIRI : 209388782984"
        )
        info.setFont(QFont("Segoe UI", 13))
        info.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info.setStyleSheet("line-height: 1.4;")

        frame_layout.addWidget(info)

        frame_layout.addStretch()

        # =====================
        # UPLOAD BUTTON
        # =====================
        upload_btn = QPushButton("Unggah Bukti Bayar")
        upload_btn.setStyleSheet("""
            QPushButton {
                background: #E99670;
                padding: 10px 18px;
                border-radius: 12px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #F1A882;
            }
        """)
        upload_btn.clicked.connect(self.upload_bukti)

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        bottom_row.addWidget(upload_btn)
        bottom_row.addStretch()

        frame_layout.addLayout(bottom_row)

        # =====================
        # MAIN LAYOUT
        # =====================
        main_layout = QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(frame)
        main_layout.addStretch()

        # semi-transparent backdrop effect
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(0, 0, 0, 90);
            }
        """)

# Untuk tampilan homepage
class PenghuniHomepage(QWidget):
    def __init__(self, penghuni_data):
        """
        penghuni_data = {
            "nama": "Ahmad Husein",
            "kamar": "A01",
            "harga": 2000000,
            "masuk": "10 Januari 2025",
            "bulan_ke": 7,
            "pembayaran_lunas": False,
            "layanan": {
                "Laundry": "Waiting",
                "Catering": "Done",
                "Refill Galon": "OnProgress",
            }
        }
        """
        super().__init__()
        self.data = penghuni_data

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(25)

        # =======================
        # Judul Halo Penghuni
        # =======================
        title = QLabel(f"Halo, {self.data['nama']}…")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))

        subtitle = QLabel("Selamat datang di Kos Melati")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: gray;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # =======================
        # Row 1: Info Penghuni + Notifikasi Pembayaran
        # =======================
        row1 = QHBoxLayout()
        row1.setSpacing(20)

        # CARD 1 — Informasi Penghuni
        card_info = self.make_card_info()
        row1.addWidget(card_info, 2)

        # CARD 2 — Status Pembayaran
        card_noti = self.make_card_notifikasi()
        row1.addWidget(card_noti, 1)

        main_layout.addLayout(row1)

        # =======================
        # Row 2 — Status Layanan
        # =======================
        card_layanan = self.make_card_layanan()
        main_layout.addWidget(card_layanan)

        self.setLayout(main_layout)

    # =================================================================
    # CARD INFORMASI PENGHUNI
    # =================================================================
    def make_card_info(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #F8F4DE;
                border-radius: 18px;
                border: 1px solid #E0DBBF;
            }
            QLabel {
                font-size: 15px;
            }
        """)
        card.setMinimumWidth(350)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        # isi data
        lbl_kamar = QLabel(f"Kamar {self.data['kamar']}")
        lbl_harga = QLabel(f"Kos perbulan\nRp. {self.data['harga']:,}")
        lbl_masuk = QLabel(f"Masuk\n{self.data['masuk']}")

        # BULAN KE box
        bulan_frame = QFrame()
        bulan_frame.setStyleSheet("""
            QFrame {
                background: #F0E3B1;
                border-radius: 14px;
                border: 1px solid #D0C38F;
            }
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
        """)
        bulan_layout = QHBoxLayout(bulan_frame)
        bulan_layout.setContentsMargins(16, 10, 16, 10)
        bulan_label = QLabel(str(self.data["bulan_ke"]))
        bulan_text = QLabel("BULAN KE")
        bulan_text.setFont(QFont("Segoe UI", 13))
        bulan_layout.addWidget(bulan_text)
        bulan_layout.addWidget(bulan_label)

        layout.addWidget(lbl_kamar)
        layout.addWidget(lbl_harga)
        layout.addWidget(lbl_masuk)
        layout.addWidget(bulan_frame)

        return card

    # =================================================================
    # CARD NOTIFIKASI PEMBAYARAN
    # =================================================================
    def make_card_notifikasi(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #F8F4DE;
                border-radius: 18px;
                border: 1px solid #E0DBBF;
            }
            QLabel {
                font-size: 15px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        title = QLabel("Notifikasi Tagihan")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        if not self.data["pembayaran_lunas"]:
            # belum bayar
            btn = QPushButton("Bayar Sekarang")
            btn.setStyleSheet("""
                QPushButton {
                    background: #E6DDA7;
                    padding: 10px 20px;
                    border-radius: 12px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #F3E9B8;
                }
            """)
            btn.clicked.connect(self.show_pembayaran_dialog)
            layout.addWidget(btn)
        else:
            # sudah bayar
            btn = QLabel("Pembayaran Lunas")
            btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn.setStyleSheet("""
                QLabel {
                    background: #E4EBCB;
                    border-radius: 12px;
                    padding: 12px;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            layout.addWidget(btn)

        return card

    # =================================================================
    # CARD STATUS LAYANAN
    # =================================================================
    def make_card_layanan(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #F8F4DE;
                border-radius: 18px;
                border: 1px solid #E0DBBF;
            }
            QLabel {
                font-size: 15px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)

        title = QLabel("Status Layanan")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        for layanan, status in self.data["layanan"].items():
            row = QHBoxLayout()
            label = QLabel(layanan)
            label.setMinimumWidth(120)

            badge = QLabel(status)
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setFixedWidth(90)

            if status == "Waiting":
                badge.setStyleSheet("background:#E0E0E0; padding:6px; border-radius:10px;")
            elif status == "Done":
                badge.setStyleSheet("background:#C9E4FF; padding:6px; border-radius:10px;")
            else:  # OnProgress
                badge.setStyleSheet("background:#F7E6A6; padding:6px; border-radius:10px;")

            row.addWidget(label)
            row.addWidget(badge)
            row.addStretch()
            layout.addLayout(row)

        return card

    def upload_bukti(self):
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Pilih Bukti Pembayaran",
                "",
                "Images (*.png *.jpg *.jpeg)"
            )

            if file_path:
                QMessageBox.information(
                    self,
                    "Upload Sukses",
                    "Bukti pembayaran berhasil diupload!"
                )

                # TODO: Simpan ke database:
                # save_payment_proof(file_path)

                self.close()
            
    def show_pembayaran_dialog(self):
        dlg = PembayaranDialog()
        dlg.exec()



