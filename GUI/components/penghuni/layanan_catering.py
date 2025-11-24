from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class CateringInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Catering")
        self.setFixedSize(550, 500)

        self.setStyleSheet("""
            QDialog {
                background: white;
                border-radius: 20px;
            }
            QLabel {
                font-family: Segoe UI;
                color: #333;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # =====================================
        # TITLE
        # =====================================
        title = QLabel("Layanan Catering")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("Catering Nasi Bu Imas")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        # =====================================
        # MENU PAKET
        # =====================================
        grid_frame = QFrame()
        grid_frame.setStyleSheet("""
            QFrame {
                background: #F8F4DE;
                border-radius: 12px;
                border: 1px solid #E0DBBF;
            }
            QLabel {
                font-size: 14px;
            }
        """)
        grid_layout = QHBoxLayout(grid_frame)

        # Card Template
        def create_card(title, prices):
            card = QFrame()
            card.setFixedSize(150, 180)
            card.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 12px;
                    border: 1px solid #CDC9B5;
                }
            """)

            v = QVBoxLayout(card)
            v.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

            lbl = QLabel(title)
            lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v.addWidget(lbl)

            for dur, price in prices.items():
                item = QLabel(f"{dur}    Rp{price}")
                item.setAlignment(Qt.AlignmentFlag.AlignLeft)
                v.addWidget(item)

            return card

        # Paket 1
        card1 = create_card("Makan Siang", {
            "7 Hari": "100.000",
            "14 Hari": "180.000",
            "30 Hari": "375.000"
        })

        # Paket 2
        card2 = create_card("Sarapan + Makan Siang", {
            "7 Hari": "200.000",
            "14 Hari": "360.000",
            "30 Hari": "750.000"
        })

        # Paket 3
        card3 = create_card("Sarapan + Siang + Malam", {
            "7 Hari": "300.000",
            "14 Hari": "500.000",
            "30 Hari": "1.000.000"
        })

        grid_layout.addWidget(card1)
        grid_layout.addWidget(card2)
        grid_layout.addWidget(card3)
        main_layout.addWidget(grid_frame)

        # =====================================
        # DROPDOWN
        # =====================================
        dropdown_label = QLabel("Pilihan Langganan :")
        dropdown_label.setFont(QFont("Segoe UI", 12))
        main_layout.addWidget(dropdown_label)

        self.combo = QComboBox()
        self.combo.setFixedHeight(35)
        self.combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border-radius: 8px;
                border: 1px solid #BDB8A3;
            }
        """)

        pilihan = [
            "Makan Siang - 7 Hari",
            "Makan Siang - 14 Hari",
            "Makan Siang - 30 Hari",
            "Sarapan + Makan Siang - 7 Hari",
            "Sarapan + Makan Siang - 14 Hari",
            "Sarapan + Makan Siang - 30 Hari",
            "Sarapan + Siang + Malam - 7 Hari",
            "Sarapan + Siang + Malam - 14 Hari",
            "Sarapan + Siang + Malam - 30 Hari"
        ]

        self.combo.addItems(pilihannya := pilihan)
        main_layout.addWidget(self.combo)

        # =====================================
        # BUTTON BAYAR
        # =====================================
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
        btn_bayar.clicked.connect(self.show_payment_popup)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_bayar)
        btn_row.addStretch()
        main_layout.addLayout(btn_row)

    # =====================================
    # POPUP PEMBAYARAN
    # =====================================
    def show_payment_popup(self):
        pilihan = self.combo.currentText()
        self.close()

        dlg = CateringPaymentDialog(pilihan)
        dlg.exec()


# ==========================================
# POPUP PEMBAYARAN
# ==========================================
class CateringPaymentDialog(QDialog):
    def __init__(self, pesanan):
        super().__init__()
        self.setWindowTitle("Pembayaran Catering")
        self.setFixedSize(480, 400)

        self.setStyleSheet("""
            QDialog { background: white; border-radius: 20px; }
            QLabel { font-family: Segoe UI; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Layanan Catering")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        # Informasi rekening
        info = QLabel("Silakan bayar melalui rekening berikut")
        info.setFont(QFont("Segoe UI", 13))
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        rekening = QLabel("BCA     : 790568301\nGOPAY : 085235990976")
        rekening.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        rekening.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(rekening)

        # Rincian Pesanan
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

        lbl_pesanan = QLabel(pesanan)
        lbl_pesanan.setFont(QFont("Segoe UI", 13))
        lbl_pesanan.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Hitung harga otomatis
        harga_map = {
            "7 Hari": "300.000",
            "14 Hari": "500.000",
            "30 Hari": "1.000.000"
        }

        durasi = pesanan.split("-")[-1].strip()
        harga = harga_map.get(durasi, "?")

        lbl_total = QLabel(f"Total Harga: Rp{harga}")
        lbl_total.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        lbl_total.setAlignment(Qt.AlignmentFlag.AlignCenter)

        f_layout.addWidget(lbl_pesanan)
        f_layout.addWidget(lbl_total)

        layout.addWidget(frame)

        # Tombol unggah bukti
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

        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(btn_upload)
        row.addStretch()
        layout.addLayout(row)
