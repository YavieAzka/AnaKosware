from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt
from components.penghuni.layanan_belanja import LaundryInputDialog  # Import LaundryInputDialog dari folder penghuni

class EditLaundryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Laundry")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Label untuk Layanan Laundry
        title = QLabel("Layanan Laundry")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tombol untuk Edit Deskripsi, Edit Harga, dan Lihat Layanan
        self.edit_deskripsi_button = QPushButton("Edit Deskripsi", self)
        self.edit_harga_button = QPushButton("Edit Harga", self)
        self.lihat_layanan_button = QPushButton("Lihat Layanan", self)

        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(save_button)

        self.setLayout(layout)

        # Menambahkan tombol ke layout
        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_harga_button)
        layout.addWidget(self.lihat_layanan_button)
        layout.addWidget(self.simpan_button)

        # Connect actions
        self.edit_deskripsi_button.clicked.connect(self.edit_deskripsi)
        self.edit_harga_button.clicked.connect(self.edit_harga)
        self.lihat_layanan_button.clicked.connect(self.lihat_layanan)

        self.setLayout(layout)

    def edit_deskripsi(self):
        # Tampilkan pop-up untuk mengedit deskripsi
        deskripsi_dialog = EditDeskripsiDialog()
        deskripsi_dialog.exec()

    def edit_harga(self):
        # Tampilkan pop-up untuk mengedit harga
        harga_dialog = EditHargaDialog()
        harga_dialog.exec()

    def lihat_layanan(self):
        # Menampilkan pop-up dari folder penghuni
        dialog = LaundryInputDialog()  # Membuka pop-up LaundryInputDialog dari folder penghuni
        dialog.exec()  # Menjalankan pop-up

class EditDeskripsiDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Deskripsi Laundry")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.deskripsi_input = QLineEdit(self)
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi laundry...")

        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)

class EditHargaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Harga Laundry")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.harga_input = QLineEdit(self)
        self.harga_input.setPlaceholderText("Masukkan harga laundry...")

        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(self.harga_input)
        layout.addWidget(save_button)

        self.setLayout(layout)
