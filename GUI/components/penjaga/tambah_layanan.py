from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel

class AddLayananDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Tambah Layanan')
        self.setGeometry(150, 150, 400, 250)

        # Layout pop-up
        layout = QVBoxLayout()

        # Label dan input untuk nama layanan
        self.nama_label = QLabel('Masukkan Nama Layanan:', self)
        self.nama_input = QLineEdit(self)

        # Tombol untuk edit deskripsi dan harga
        self.edit_deskripsi_button = QPushButton('Edit Deskripsi', self)
        self.edit_harga_button = QPushButton('Edit Harga', self)
        self.simpan_button = QPushButton('Simpan', self)

        # Menambahkan elemen ke layout
        layout.addWidget(self.nama_label)
        layout.addWidget(self.nama_input)
        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_harga_button)
        layout.addWidget(self.simpan_button)

        self.setLayout(layout)

        # Connect button actions
        self.simpan_button.clicked.connect(self.accept)
        self.edit_deskripsi_button.clicked.connect(self.edit_deskripsi)
        self.edit_harga_button.clicked.connect(self.edit_harga)

    def edit_deskripsi(self):
        # Dialog untuk mengedit deskripsi
        deskripsi_dialog = EditDeskripsiDialog()
        deskripsi_dialog.exec()

    def edit_harga(self):
        # Dialog untuk mengedit harga
        harga_dialog = EditHargaDialog()
        harga_dialog.exec()

    def get_layanan(self):
        return self.nama_input.text()


class EditDeskripsiDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Edit Deskripsi')
        self.setGeometry(150, 150, 400, 200)

        layout = QVBoxLayout()

        self.deskripsi_input = QLineEdit(self)
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi")

        save_button = QPushButton('Simpan', self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)


class EditHargaDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Edit Harga')
        self.setGeometry(150, 150, 400, 200)

        layout = QVBoxLayout()

        self.harga_input = QLineEdit(self)
        self.harga_input.setPlaceholderText("Masukkan harga")

        save_button = QPushButton('Simpan', self)
        save_button.clicked.connect(self.accept)

        layout.addWidget(self.harga_input)
        layout.addWidget(save_button)

        self.setLayout(layout)
