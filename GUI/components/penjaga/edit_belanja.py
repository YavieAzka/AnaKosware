from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

class EditBelanjaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Belanja Kebutuhan")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Label untuk Layanan Belanja Kebutuhan
        title = QLabel("Layanan Belanja Kebutuhan")
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
        deskripsi_dialog = EditDeskripsiBelanjaDialog()
        deskripsi_dialog.exec()

    def edit_daftar(self):
        # Tampilkan pop-up untuk mengedit daftar barang (nama dan harga)
        daftar_dialog = EditDaftarBelanjaDialog()
        daftar_dialog.exec()

    def lihat_layanan(self):
        from components.penghuni.layanan_belanja import BelanjaInputDialog # Menampilkan pop-up dari folder penghuni
        dialog = BelanjaInputDialog()  # Pop-up LaundryInputDialog dari penghuni
        dialog.exec()  # Menjalankan pop-up


class EditDeskripsiBelanjaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Deskripsi Layanan Belanja")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.deskripsi_input = QLineEdit(self)
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi belanja kebutuhan...")

        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)


class EditDaftarBelanjaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Daftar Layanan Belanja")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        # Daftar barang
        self.table = QTableWidget()
        self.table.setRowCount(5)  # Menyesuaikan jumlah baris dengan barang yang ada
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Nama Barang", "Harga"])
        self.table.setColumnWidth(0, 230)
        self.table.setColumnWidth(1, 150)

        # Isi daftar barang
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
