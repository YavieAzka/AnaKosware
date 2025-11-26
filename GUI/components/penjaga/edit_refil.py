from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

STYLE_SHEET = """
QDialog {
    background-color: #FFFFFF;
    border-radius: 12px;
    font-family: 'Segoe UI', Arial;
}

QLabel#DialogTitle {
    font-size: 20pt;
    font-weight: bold;
    color: #2D3142;
    margin-bottom: 20px;
}

QLineEdit {
    padding: 10px;
    border: 1px solid #B0B0B0;
    border-radius: 8px;
    background-color: #F8F9FA;
    min-height: 40px;
}

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

/* Tombol Tambahkan Barang */
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
#                   DIALOG UTAMA REFILL
# ======================================================
class EditRefillDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Layanan Refill Galon")
        self.setMinimumWidth(400)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        title = QLabel("Layanan Refill Galon")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tombol
        self.edit_deskripsi_button = QPushButton("Edit Deskripsi")
        self.edit_deskripsi_button.setObjectName("SecondaryDialogBtn")

        self.edit_daftar_button = QPushButton("Edit Daftar")
        self.edit_daftar_button.setObjectName("SecondaryDialogBtn")

        self.lihat_layanan_button = QPushButton("Lihat Layanan")
        self.lihat_layanan_button.setObjectName("SecondaryDialogBtn")

        self.simpan_button = QPushButton("Simpan")
        self.simpan_button.setObjectName("PrimaryDialogBtn")
        self.simpan_button.clicked.connect(self.accept)

        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_daftar_button)
        layout.addWidget(self.lihat_layanan_button)
        layout.addStretch()
        layout.addWidget(self.simpan_button)

        self.edit_deskripsi_button.clicked.connect(self.edit_deskripsi)
        self.edit_daftar_button.clicked.connect(self.edit_daftar)
        self.lihat_layanan_button.clicked.connect(self.lihat_layanan)

        self.setLayout(layout)

    def edit_deskripsi(self):
        dlg = EditDeskripsiRefillDialog(self)
        dlg.exec()

    def edit_daftar(self):
        dlg = EditDaftarRefillDialog(self)
        dlg.exec()

    def lihat_layanan(self):
        from components.penghuni.layanan_refill import RefillGalonDialog
        dialog = RefillGalonDialog()
        dialog.exec()


# ======================================================
#                  DIALOG EDIT DESKRIPSI
# ======================================================
class EditDeskripsiRefillDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Deskripsi Layanan Refill")
        self.setMinimumWidth(400)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        title = QLabel("Deskripsi Refill Galon")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.deskripsi_input = QLineEdit()
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi refill...")

        save_button = QPushButton("Simpan")
        save_button.setObjectName("PrimaryDialogBtn")
        save_button.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)


# ======================================================
#                  DIALOG EDIT DAFTAR HARGA
# ======================================================
class EditDaftarRefillDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Daftar Layanan Refill")
        self.setMinimumWidth(500)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        title = QLabel("Daftar Barang Refill")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Table
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

        # Tambah item
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
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(""))
        self.table.setItem(row_position, 1, QTableWidgetItem(""))
