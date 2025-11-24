from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QFrame, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from components.penghuni.layanan_catering import CateringInputDialog 

class EditCateringDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Catering")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Label untuk Layanan Catering
        title = QLabel("Layanan Catering")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tombol untuk Edit Deskripsi, Edit Menu, dan Lihat Layanan
        self.edit_deskripsi_button = QPushButton("Edit Deskripsi", self)
        self.edit_menu_button = QPushButton("Edit Menu", self)
        self.lihat_layanan_button = QPushButton("Lihat Layanan", self)

        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(save_button)

        self.setLayout(layout)

        # Menambahkan tombol ke layout
        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_menu_button)
        layout.addWidget(self.lihat_layanan_button)
        layout.addWidget(self.simpan_button)

        # Connect actions
        self.edit_deskripsi_button.clicked.connect(self.edit_deskripsi)
        self.edit_menu_button.clicked.connect(self.edit_menu)
        self.lihat_layanan_button.clicked.connect(self.lihat_layanan)

        self.setLayout(layout)

    def edit_deskripsi(self):
        # Tampilkan pop-up untuk mengedit deskripsi
        deskripsi_dialog = EditDeskripsiCateringDialog()
        deskripsi_dialog.exec()

    def edit_menu(self):
        # Tampilkan pop-up untuk mengedit menu (input gambar)
        menu_dialog = EditMenuCateringDialog()
        menu_dialog.exec()

    def lihat_layanan(self):
        # Menampilkan pop-up dari folder penghuni
        dialog = CateringInputDialog ()  # Pop-up dari penghuni
        dialog.exec()  # Menjalankan pop-up


class EditDeskripsiCateringDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Deskripsi Layanan Catering")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.deskripsi_input = QLineEdit(self)
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi catering...")

        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)


class EditMenuCateringDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Menu Layanan Catering")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Pilih gambar menu catering
        self.menu_image_button = QPushButton("Pilih Gambar Menu", self)
        self.menu_image_button.clicked.connect(self.choose_image)

        self.image_label = QLabel("Tidak ada gambar yang dipilih", self)

        save_button = QPushButton("Simpan", self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(self.menu_image_button)
        layout.addWidget(self.image_label)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def choose_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar Menu", "", "Images (*.png *.jpg *.jpeg)")

        if file:
            self.image_label.setText(f"File yang dipilih: {file.split('/')[-1]}")
            self.selected_image = file
        else:
            self.image_label.setText("Tidak ada gambar yang dipilih")


class LaundryInputDialog(QDialog):
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

        self.simpan_button = QPushButton("Simpan", self)

        # Menambahkan tombol ke layout
        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_harga_button)
        layout.addWidget(self.lihat_layanan_button)
        layout.addWidget(self.simpan_button)

        self.setLayout(layout)
