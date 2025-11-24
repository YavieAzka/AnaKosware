from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

class EditRefillDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Refill Galon")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Label untuk Layanan Refill Galon
        title = QLabel("Layanan Refill Galon")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tombol untuk Edit Deskripsi, Edit Daftar, dan Lihat Layanan
        self.edit_deskripsi_button = QPushButton("Edit Deskripsi", self)
        self.edit_daftar_button = QPushButton("Edit Daftar", self)
        self.lihat_layanan_button = QPushButton("Lihat Layanan", self)

        self.simpan_button = QPushButton("Simpan", self)

        # Menambahkan tombol ke layout
        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_daftar_button)
        layout.addWidget(self.lihat_layanan_button)
        layout.addWidget(self.simpan_button)

        # Connect actions
        self.edit_deskripsi_button.clicked.connect(self.edit_deskripsi)
        self.edit_daftar_button.clicked.connect(self.edit_daftar)
        self.lihat_layanan_button.clicked.connect(self.lihat_layanan)

        self.setLayout(layout)

    def edit_deskripsi(self):
        # Tampilkan pop-up untuk mengedit deskripsi
        deskripsi_dialog = EditDeskripsiRefillDialog()
        deskripsi_dialog.exec()

    def edit_daftar(self):
        # Tampilkan pop-up untuk mengedit daftar barang (nama dan harga)
        daftar_dialog = EditDaftarRefillDialog()
        daftar_dialog.exec()

    def lihat_layanan(self):
        from components.penghuni.layanan_refill import RefillGalonDialog  # Menampilkan pop-up dari folder penghuni
        dialog = RefillGalonDialog()  # Pop-up LaundryInputDialog dari penghuni
        dialog.exec()  # Menjalankan pop-up


class EditDeskripsiRefillDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Deskripsi Layanan Refill")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.deskripsi_input = QLineEdit(self)
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi refill galon...")

        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)


class EditDaftarRefillDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Daftar Layanan Refill")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        # Daftar barang
        self.table = QTableWidget()
        self.table.setRowCount(2)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Nama Barang", "Harga"])
        self.table.setColumnWidth(0, 230)
        self.table.setColumnWidth(1, 150)

        self.table.setItem(0, 0, QTableWidgetItem("Le Minerale"))
        self.table.setItem(0, 1, QTableWidgetItem("Rp20.000"))
        self.table.setItem(1, 0, QTableWidgetItem("Aqua"))
        self.table.setItem(1, 1, QTableWidgetItem("Rp25.000"))

        layout.addWidget(self.table)

        # Tambahkan Barang
        add_button = QPushButton("Tambahkan Barang", self)
        add_button.clicked.connect(self.add_item)

        layout.addWidget(add_button)

        # Tombol Simpan
        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(save_button)

        self.setLayout(layout)

    def add_item(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)  # Menambahkan baris baru
        self.table.setItem(row_position, 0, QTableWidgetItem(""))  # Kolom Nama Barang kosong
        self.table.setItem(row_position, 1, QTableWidgetItem(""))  # Kolom Harga kosong
