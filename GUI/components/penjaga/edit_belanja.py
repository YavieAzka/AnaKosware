from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt

# ======================================================
#                 GLOBAL STYLE SHEET
# ======================================================
STYLE_SHEET = """
QDialog {
    background-color: #FFFFFF;
    border-radius: 12px;
    font-family: 'Segoe UI', Arial;
}

/* Title */
QLabel#DialogTitle {
    font-size: 20pt;
    font-weight: bold;
    color: #2D3142;
    margin-bottom: 20px;
}

/* Input */
QLineEdit {
    padding: 10px;
    border: 1px solid #B0B0B0;
    border-radius: 8px;
    background-color: #F8F9FA;
    min-height: 40px;
}

/* Button Utama */
QPushButton#PrimaryDialogBtn {
    background-color: #FF9800;
    color: white;
    font-weight: bold;
    padding: 12px;
    border-radius: 8px;
    border: none;
    font-size: 12pt;
}
QPushButton#PrimaryDialogBtn:hover {
    background-color: #E68900;
}

/* Button Sekunder */
QPushButton#SecondaryDialogBtn {
    background-color: #FF9800;
    color: white;
    font-weight: 600;
    padding: 12px;
    border-radius: 8px;
    border: none;
    font-size: 12pt;
    min-height: 45px;
}
QPushButton#SecondaryDialogBtn:hover {
    background-color: #E68900;
}

/* Button Tambah */
QPushButton#AddItemBtn {
    background-color: #FFFFFF;
    border: 2px solid #FF9800;
    color: #FF9800;
    padding: 8px 12px;
    border-radius: 8px;
    font-weight: bold;
}
QPushButton#AddItemBtn:hover {
    background-color: #FFF3E0;
}
"""


# ======================================================
#                  DIALOG UTAMA BELANJA
# ======================================================
class EditBelanjaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Layanan Belanja Kebutuhan")
        self.resize(500, 350)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Judul
        title = QLabel("Layanan Belanja Kebutuhan")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tombol-tombol utama (Sekunder)
        self.edit_deskripsi_button = QPushButton("Edit Deskripsi")
        self.edit_deskripsi_button.setObjectName("PrimaryDialogBtn")

        self.edit_daftar_button = QPushButton("Edit Daftar")
        self.edit_daftar_button.setObjectName("PrimaryDialogBtn")

        self.lihat_layanan_button = QPushButton("Lihat Layanan")
        self.lihat_layanan_button.setObjectName("PrimaryDialogBtn")

        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_daftar_button)
        layout.addWidget(self.lihat_layanan_button)

        # Tombol simpan (Primer)
        self.simpan_button = QPushButton("Simpan")
        self.simpan_button.setObjectName("PrimaryDialogBtn")
        layout.addWidget(self.simpan_button)

        # Connect
        self.edit_deskripsi_button.clicked.connect(self.edit_deskripsi)
        self.edit_daftar_button.clicked.connect(self.edit_daftar)
        self.lihat_layanan_button.clicked.connect(self.lihat_layanan)


    def edit_deskripsi(self):
        dlg = EditDeskripsiBelanjaDialog(self)
        dlg.exec()

    def edit_daftar(self):
        dlg = EditDaftarBelanjaDialog(self)
        dlg.exec()

    def lihat_layanan(self):
        from GUI.components.penghuni.layanan_belanja import BelanjaInputDialog
        dialog = BelanjaInputDialog()
        dialog.exec()


# ======================================================
#                 DIALOG EDIT DESKRIPSI
# ======================================================
class EditDeskripsiBelanjaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Deskripsi Layanan Belanja")
        self.setMinimumWidth(400)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        title = QLabel("Deskripsi Belanja Kebutuhan")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.deskripsi_input = QLineEdit()
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi belanja...")

        save_button = QPushButton("Simpan")
        save_button.setObjectName("PrimaryDialogBtn")
        save_button.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)


# ======================================================
#               DIALOG EDIT DAFTAR BELANJA
# ======================================================
class EditDaftarBelanjaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Daftar Layanan Belanja")
        self.setMinimumWidth(500)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        title = QLabel("Daftar Barang Belanja")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Nama Barang", "Harga"])
        self.table.setColumnWidth(0, 230)
        self.table.setColumnWidth(1, 150)

        # Data awal
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

        # Add item
        add_button = QPushButton("Tambahkan Barang")
        add_button.setObjectName("AddItemBtn")
        add_button.clicked.connect(self.add_item)
        layout.addWidget(add_button)

        # Save
        save_button = QPushButton("Simpan")
        save_button.setObjectName("PrimaryDialogBtn")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def add_item(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
