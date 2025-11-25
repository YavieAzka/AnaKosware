import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, 
    QLabel, QDialog, QHBoxLayout, QFrame, QSizePolicy, QMessageBox, QLineEdit
)
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QSize
from GUI.components.penghuni.layanan_laundry import LaundryInputDialog

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


# --- Kelas Dialog Edit yang Diperbarui (Sesuai kode dan gambar) ---

class EditDeskripsiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Deskripsi Laundry")
        self.setMinimumWidth(400)
        self.setStyleSheet(self.parent().styleSheet()) # Warisi style dari parent

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Judul Pop-up (Meniru tampilan gambar)
        title = QLabel("Layanan Laundry")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Input Deskripsi (Menggunakan QLineEdit sesuai gambar 1, tapi QLineEdit kurang tepat untuk deskripsi panjang)
        # Mengganti ke QLineEdit sederhana sesuai permintaan, tetapi QLineEdit lebih cocok untuk input pendek.
        self.deskripsi_input = QLineEdit(self)
        self.deskripsi_input.setPlaceholderText("Tuliskan deskripsi laundry...")

        save_button = QPushButton("Simpan", self)
        save_button.setObjectName("PrimaryDialogBtn")
        save_button.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(self.deskripsi_input)
        layout.addWidget(save_button)

        self.setLayout(layout)

class EditHargaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Harga Laundry")
        self.setMinimumWidth(400)
        self.setStyleSheet(self.parent().styleSheet()) # Warisi style dari parent

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Judul Pop-up (Meniru tampilan gambar)
        title = QLabel("Layanan Laundry")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.harga_input = QLineEdit(self)
        self.harga_input.setPlaceholderText("Masukkan harga")
        self.harga_input.setAlignment(Qt.AlignmentFlag.AlignCenter) # Tengah sesuai gambar 2

        save_button = QPushButton("Simpan", self)
        save_button.setObjectName("PrimaryDialogBtn")
        save_button.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(self.harga_input)
        layout.addWidget(save_button)

        self.setLayout(layout)

class EditLaundryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE_SHEET)
        self.setWindowTitle("Layanan Laundry")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30) # Padding yang lebih baik

        # Label untuk Layanan Laundry
        title = QLabel("Layanan Laundry")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tombol untuk Edit Deskripsi, Edit Harga, dan Lihat Layanan
        self.edit_deskripsi_button = QPushButton("Edit Deskripsi", self)
        self.edit_deskripsi_button.setObjectName("SecondaryDialogBtn")
        self.edit_harga_button = QPushButton("Edit Harga", self)
        self.edit_harga_button.setObjectName("SecondaryDialogBtn")
        self.lihat_layanan_button = QPushButton("Lihat Layanan", self)
        self.lihat_layanan_button.setObjectName("SecondaryDialogBtn")

        self.simpan_button = QPushButton("Simpan", self)
        self.simpan_button.setObjectName("PrimaryDialogBtn")
        self.simpan_button.clicked.connect(self.accept)

        # Menambahkan tombol ke layout
        layout.addWidget(self.edit_deskripsi_button)
        layout.addWidget(self.edit_harga_button)
        layout.addWidget(self.lihat_layanan_button)
        layout.addStretch(1) # Stretch di tengah
        layout.addWidget(self.simpan_button)

        # Connect actions
        self.edit_deskripsi_button.clicked.connect(self.edit_deskripsi)
        self.edit_harga_button.clicked.connect(self.edit_harga)
        self.lihat_layanan_button.clicked.connect(self.lihat_layanan)

        self.setLayout(layout)

    def edit_deskripsi(self):
        # Tampilkan pop-up untuk mengedit deskripsi
        deskripsi_dialog = EditDeskripsiDialog(self)
        deskripsi_dialog.exec()

    def edit_harga(self):
        # Tampilkan pop-up untuk mengedit harga
        harga_dialog = EditHargaDialog(self)
        harga_dialog.exec()

    def lihat_layanan(self):
        # Menampilkan pop-up dari folder penghuni (Menggunakan dummy di sini)
        dialog = LaundryInputDialog(self) 
        dialog.exec() 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET) 
    
    window = EditLaundryDialog()
    window.show()
    sys.exit(app.exec())
