from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QPushButton, QLineEdit,
    QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
# Asumsi: CateringInputDialog adalah kelas yang dapat diimpor
# from GUI.components.penghuni.layanan_catering import CateringInputDialog

# Dummy class untuk simulasi import CateringInputDialog
class CateringInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Lihat Layanan Catering (Simulasi)')
        self.setFixedSize(500, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Ini adalah pop-up 'Lihat Layanan' dari sisi Penghuni."))

STYLE_SHEET = """
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2D3142; 
    background-color: #F8F9FA; /* DIUBAH: Background abu-abu muda untuk keseluruhan widget */
}

/* Judul Halaman */
QLabel#PageTitle {
    font-size: 24px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 25px;
    color: #2D3142;
}

/* Kartu Layanan (Card) */
QFrame#ServiceCard {
    border: 1px solid #E0E0E0;
    border-radius: 10px;
    background-color: #FFFFFF;
    min-width: 200px; 
    min-height: 250px; 
    padding: 15px;
}

/* Judul Layanan di dalam Kartu */
QLabel#ServiceTitle {
    font-size: 16pt;
    font-weight: bold;
    color: #2D3142;
    margin-bottom: 20px;
    background-color: transparent;
}

/* Tombol Edit/Hapus (Orange) */
QPushButton.CardActionBtn {
    background-color: #FF9800; /* Orange */
    color: white; 
    font-weight: 600; 
    padding: 8px 15px; 
    border-radius: 6px;
    border: none;
    min-height: 35px;
    font-size: 12pt;
    margin-top: 5px;
}

QPushButton.CardActionBtn:hover {
    background-color: #E68900;
}

/* Kartu Tambah Layanan (dengan ikon +) */
QFrame#AddCard {
    border: 1px dashed #B0B0B0; /* Border putus-putus */
    border-radius: 10px;
    background-color: #FFFFFF;
    min-width: 200px;
    min-height: 250px;
}

/* --- Gaya Khusus untuk Dialog (BARU: Disinkronkan dengan Edit Laundry) --- */
QDialog {
    background-color: #FFFFFF; 
    border-radius: 12px;
}
QLabel#DialogTitle {
    font-size: 18pt;
    font-weight: bold;
    color: #2D3142;
    margin-bottom: 20px;
}
QLineEdit {
    padding: 10px;
    border: 1px solid #B0B0B0;
    border-radius: 8px;
    font-size: 10pt;
    min-height: 40px;
    background-color: #F8F9FA;
}
QPushButton#PrimaryDialogBtn {
    background-color: #FF9800; /* Orange Primer */
    color: white; 
    font-weight: 600; 
    padding: 10px; 
    border-radius: 8px;
    border: none;
    font-size: 11pt;
    min-height: 45px;
}
QPushButton#PrimaryDialogBtn:hover {
    background-color: #E68900;
}
/* Tombol Sekunder di Dialog (Orange) */
QPushButton#SecondaryDialogBtn {
    background-color: #FF9800; 
    color: white;
    font-weight: 600; 
    padding: 15px; 
    border-radius: 8px;
    border: none;
    font-size: 12pt;
    min-height: 50px;
}
QPushButton#SecondaryDialogBtn:hover {
    background-color: #E68900;
}
/* Tombol Tambahkan Layanan (di luar grid) - Dihapus karena tombol Tambah sekarang adalah kartu */
"""


# =============================================================
#           ----    POP-UP EDIT DESKRIPSI ----
# =============================================================

class EditDeskripsiCateringDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Deskripsi Catering")
        self.setMinimumWidth(400)
        # Ambil style sheet dari parent (EditCateringDialog)
        if parent and hasattr(parent, 'styleSheet'): self.setStyleSheet(parent.styleSheet())
        else: self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Title
        title = QLabel("Layanan Catering")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.deskripsi_input = QLineEdit(self)
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi catering...")

        save_button = QPushButton("Simpan")
        save_button.setObjectName("PrimaryDialogBtn")
        save_button.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)


# =============================================================
#           ----    POP-UP EDIT MENU (GAMBAR) ----
# =============================================================

class EditMenuCateringDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Menu Catering")
        self.setMinimumWidth(400)
        # Ambil style sheet dari parent (EditCateringDialog)
        if parent and hasattr(parent, 'styleSheet'): self.setStyleSheet(parent.styleSheet())
        else: self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Layanan Catering")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.menu_image_button = QPushButton("Pilih Gambar Menu")
        self.menu_image_button.setObjectName("SecondaryDialogBtn")
        self.menu_image_button.clicked.connect(self.choose_image)

        self.image_label = QLabel("Tidak ada gambar dipilih")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("font-size: 10pt; color: #555555; margin-top: 5px;") # Gaya tambahan untuk label

        save_button = QPushButton("Simpan")
        save_button.setObjectName("PrimaryDialogBtn")
        save_button.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(self.menu_image_button)
        layout.addWidget(self.image_label)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def choose_image(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Pilih Gambar Menu", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file:
            self.image_label.setText(f"File dipilih: {file.split('/')[-1]}")
            self.selected_image = file
        else:
            self.image_label.setText("Tidak ada gambar dipilih")


# =============================================================
#           ----    POP-UP UTAMA EDIT CATERING  ----
# =============================================================

class EditCateringDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Layanan Catering")
        self.setMinimumWidth(400)

        # Menggunakan STYLE_SHEET yang sudah diperbarui
        self.setStyleSheet(STYLE_SHEET) 

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Title
        title = QLabel("Layanan Catering")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Buttons
        self.edit_deskripsi_button = QPushButton("Edit Deskripsi")
        self.edit_deskripsi_button.setObjectName("SecondaryDialogBtn")

        self.edit_menu_button = QPushButton("Edit Menu")
        self.edit_menu_button.setObjectName("SecondaryDialogBtn")

        self.lihat_layanan_button = QPushButton("Lihat Layanan")
        self.lihat_layanan_button.setObjectName("SecondaryDialogBtn")

        self.simpan_button = QPushButton("Simpan")
        self.simpan_button.setObjectName("PrimaryDialogBtn")
        self.simpan_button.clicked.connect(self.accept)

        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_menu_button)
        layout.addWidget(self.lihat_layanan_button)
        layout.addStretch(1)
        layout.addWidget(self.simpan_button)

        # Connect actions
        self.edit_deskripsi_button.clicked.connect(self.edit_deskripsi)
        self.edit_menu_button.clicked.connect(self.edit_menu)
        self.lihat_layanan_button.clicked.connect(self.lihat_layanan)

        self.setLayout(layout)

    def edit_deskripsi(self):
        dlg = EditDeskripsiCateringDialog(self)
        dlg.exec()

    def edit_menu(self):
        dlg = EditMenuCateringDialog(self)
        dlg.exec()

    def lihat_layanan(self):
        dlg = CateringInputDialog(self)
        dlg.exec()