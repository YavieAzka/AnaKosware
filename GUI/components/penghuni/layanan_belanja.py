from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class BelanjaInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Belanja Kebutuhan")
        self.setMinimumWidth(500)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                font-size: 16px;
            }
            QPushButton {
                background-color: #FF8E72;
                padding: 8px 15px;
                border-radius: 10px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffa98e;
            }
            QLineEdit {
                border: 1px solid #c9c9c9;
                border-radius: 8px;
                padding: 6px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Layanan Belanja Kebutuhan")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # =======================
        # TABEL DAFTAR BARANG
        # =======================
        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Nama Barang", "Harga"])
        self.table.setColumnWidth(0, 230)
        self.table.setColumnWidth(1, 150)

        barang_list = [
            ("Sabun Batang", "Rp5.000"),
            ("Shampoo", "Rp17.000"),
            ("Tomat", "Rp1.000"),
            ("Telur", "Rp2.000"),
            ("Sikat gigi", "Rp5.000"),
        ]

        for i, (nama, harga) in enumerate(barang_list):
            self.table.setItem(i, 0, QTableWidgetItem(nama))
            self.table.setItem(i, 1, QTableWidgetItem(harga))

        layout.addWidget(self.table)

        # =======================
        # INPUT USER
        # =======================
        self.input_barang = QLineEdit()
        self.input_barang.setPlaceholderText(
            "Tuliskan barang yang ingin dibeli\nContoh:\nSabun 2 5000"
        )
        layout.addWidget(self.input_barang)

        # =======================
        # TOMBOL BAYAR
        # =======================
        pay_btn = QPushButton("Bayar")
        pay_btn.clicked.connect(self.open_payment_dialog)
        layout.addWidget(pay_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    # =========================
    # POP UP PEMBAYARAN
    # =========================
    def open_payment_dialog(self):
        text = self.input_barang.text().strip()

        if text == "":
            QMessageBox.warning(self, "Peringatan", "Input tidak boleh kosong!")
            return

        # Format input: "Sabun 2 5000"
        try:
            nama, jumlah, harga = text.split()
            jumlah = int(jumlah)
            harga = int(harga)
        except:
            QMessageBox.warning(self, "Format Salah",
                                "Gunakan format: NamaBarang Jumlah HargaSatuan\nContoh: Sabun 2 5000")
            return

        total = jumlah * harga

        dialog = PembayaranBelanjaDialog(nama, jumlah, harga, total)
        dialog.exec()


class PembayaranBelanjaDialog(QDialog):
    def __init__(self, nama, qty, harga, total):
        super().__init__()
        self.setWindowTitle("Rincian Pembayaran")
        self.setMinimumWidth(450)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
            QLabel {
                font-size: 15px;
            }
            QPushButton {
                background-color: #FF8E72;
                padding: 8px 15px;
                border-radius: 10px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffa98e;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Rincian Pembayaran")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # ==========================
        # TABEL RINCIAN PESANAN
        # ==========================
        table = QTableWidget()
        table.setRowCount(1)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Pesanan", "Jumlah", "Harga"])
        table.setColumnWidth(0, 180)
        table.setColumnWidth(1, 80)
        table.setColumnWidth(2, 120)

        table.setItem(0, 0, QTableWidgetItem(nama))
        table.setItem(0, 1, QTableWidgetItem(str(qty)))
        table.setItem(0, 2, QTableWidgetItem(f"Rp{harga:,}".replace(",", ".")))

        layout.addWidget(table)

        # ==========================
        # TOTAL HARGA
        # ==========================
        total_label = QLabel(f"Total: Rp{total:,}".replace(",", "."))
        total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(total_label)

        # ==========================
        # TOMBOL KONFIRMASI
        # ==========================
        pay_btn = QPushButton("Konfirmasi Pembayaran")
        layout.addWidget(pay_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
