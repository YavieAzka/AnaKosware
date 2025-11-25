import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, 
    QLabel, QDialog, QHBoxLayout, QFrame, QSizePolicy, QMessageBox, QLineEdit
)
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QSize

# ==============================================================================
# IMPORT DARI FOLDER COMPONENTS
# ==============================================================================
from GUI.components.penjaga.edit_laundry import EditLaundryDialog 
from GUI.components.penjaga.edit_refil import EditRefillDialog 
from GUI.components.penjaga.edit_catering import EditCateringDialog 
from GUI.components.penjaga.edit_belanja import EditBelanjaDialog

# ==============================================================================


# --- Gaya Global (Stylesheet) ---
STYLE_SHEET = """
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2D3142; 
    background-color: #F8F9FA; /* Background abu-abu muda untuk keseluruhan widget */
}

/* Judul Halaman */
QLabel#PageTitle {
    font-size: 24px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 25px;
    color: #2D3142;
    background-color: transparent;
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

/* Tombol Aksi di dalam Kartu (Orange) */
QPushButton.CardActionBtn {
    background-color: #FF9800; /* Orange */
    color: white; 
    font-weight: 600; 
    padding: 8px 15px; 
    border-radius: 6px;
    border: none;
    min-height: 35px;
    min-width: 150px; 
    font-size: 12pt;
    margin-top: 5px;
}
QPushButton.CardActionBtn:hover {
    background-color: #E68900;
}

/* --- Gaya Khusus untuk Dialog Baru (Diperlukan oleh dialog di file components) --- */

/* Gaya untuk QDialog (Pop-up) */
QDialog {
    background-color: #FFFFFF; 
    border-radius: 12px;
}

/* Judul di dalam Dialog */
QLabel#DialogTitle {
    font-size: 18pt;
    font-weight: bold;
    color: #2D3142;
    margin-bottom: 20px;
}

/* Input Field (QLineEdit) */
QLineEdit {
    padding: 10px;
    border: 1px solid #B0B0B0;
    border-radius: 8px;
    font-size: 10pt;
    min-height: 40px;
    background-color: #F8F9FA;
}

/* Input Field Multi-line (QTextEdit) */
QTextEdit {
    padding: 10px;
    border: 1px solid #B0B0B0;
    border-radius: 8px;
    font-size: 10pt;
    min-height: 100px; /* Lebih tinggi untuk deskripsi */
    background-color: #F8F9FA;
}

/* Tombol Primer di Dialog (Simpan) */
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

/* Tombol Sekunder di Dialog (Edit Deskripsi/Harga/Lihat) */
QPushButton#SecondaryDialogBtn {
    background-color: #E0E0E0; /* Abu-abu muda */
    color: #2D3142;
    font-weight: 600; 
    padding: 15px; 
    border-radius: 8px;
    border: none;
    font-size: 12pt;
    min-height: 50px;
}
QPushButton#SecondaryDialogBtn:hover {
    background-color: #D5D5D5;
}


/* Kartu Tambah Layanan (dengan ikon +) */
QFrame#AddCard {
    border: 1px dashed #B0B0B0; /* Border putus-putus */
    border-radius: 10px;
    background-color: #FFFFFF;
    min-width: 200px;
    min-height: 250px;
}
"""

class AddLayananDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Tambahkan Layanan Baru')
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        label = QLabel("Nama Layanan Baru:")
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Masukkan nama layanan (mis: Isi Ulang Pulsa)")

        button_layout = QHBoxLayout()
        ok_button = QPushButton('Tambahkan')
        cancel_button = QPushButton('Batal')
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)

        layout.addWidget(label)
        layout.addWidget(self.input_field)
        layout.addLayout(button_layout)
        
    def get_layanan(self):
        return self.input_field.text().strip()
        
# --- Widget Kartu Layanan (Hanya Tampilan) ---
class ServiceCard(QFrame):
    """
    Widget kustom yang merepresentasikan satu kartu layanan. 
    Tombol di dalamnya dihubungkan oleh parent widget (EditLayanan).
    """
    def __init__(self, layanan_name, edit_button, hapus_button, parent=None):
        super().__init__(parent)
        self.setObjectName("ServiceCard")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter) 
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        # Judul Layanan
        title_label = QLabel(layanan_name)
        title_label.setObjectName("ServiceTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addStretch(1) 

        # Tambahkan tombol yang sudah dibuat di EditLayanan
        layout.addWidget(edit_button)
        layout.addWidget(hapus_button)


class AddServiceCard(QFrame):
    """
    Widget kustom untuk kartu Tambahkan Layanan dengan ikon '+'.
    Kartu ini berfungsi sebagai tombol.
    """
    def __init__(self, add_callback, parent=None):
        super().__init__(parent)
        self.setObjectName("AddCard")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.clicked = add_callback

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Judul "Tambahkan Layanan"
        title_label = QLabel("Tambahkan Layanan")
        title_label.setObjectName("ServiceTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Ikon Plus besar (+)
        plus_label = QLabel("+")
        # PERBAIKAN: Tambahkan background-color: transparent; di sini.
        plus_label.setStyleSheet("font-size: 50pt; color: #B0B0B0; background-color: transparent;")
        plus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(plus_label)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked()


# --- Kelas Utama ---
class EditLayanan(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Edit Layanan')
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(STYLE_SHEET)

        # Layout utama
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Judul Halaman
        page_title = QLabel("Edit Layanan")
        page_title.setObjectName("PageTitle")
        main_layout.addWidget(page_title)
        
        # Grid untuk menampilkan layanan
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(25) # Spasi antar kartu

        self.layanan_list = ['Laundry', 'Catering', 'Refill Galon', 'Belanja Kebutuhan']
        
        main_layout.addLayout(self.grid_layout)
        main_layout.addStretch(1) 
        
        # Inisialisasi grid
        self.update_layanan_grid()
        self.setLayout(main_layout)

    def update_layanan_grid(self):
        """Membuat ulang Grid Layout dengan kartu-kartu layanan."""
        
        # 1. Hapus semua widget lama
        for i in reversed(range(self.grid_layout.count())):
              widget = self.grid_layout.itemAt(i).widget()
              if widget:
                  widget.deleteLater()

        # 2. Tambahkan kartu untuk setiap layanan
        max_cols = 3 
        
        for i, layanan in enumerate(self.layanan_list):
            row = i // max_cols
            col = i % max_cols
            
            # --- Pembuatan Tombol Edit dan Hapus ---
            edit_button = QPushButton('Edit')
            edit_button.setProperty("class", "CardActionBtn")
            edit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            edit_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum) # Memastikan lebar penuh

            hapus_button = QPushButton('Hapus')
            hapus_button.setProperty("class", "CardActionBtn")
            hapus_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            hapus_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum) # Memastikan lebar penuh
            
            hapus_button.clicked.connect(lambda checked, layanan=layanan: self.show_confirmation_popup(layanan))
            
            # --- Logika Koneksi Tombol Edit ---
            # Menggunakan EditDialog yang diimpor dari modul components
            if layanan == "Laundry":
                edit_button.clicked.connect(self.open_laundry_dialog) 
            elif layanan == "Catering":
                edit_button.clicked.connect(self.open_catering_dialog)
            elif layanan == "Refill Galon": 
                edit_button.clicked.connect(self.open_refill_dialog)
            elif layanan == "Belanja Kebutuhan": 
                edit_button.clicked.connect(self.open_belanja_dialog)
            else:
                 edit_button.clicked.connect(lambda: QMessageBox.information(self, "Edit", f"Fungsi edit untuk {layanan} belum tersedia."))

            # Buat kartu layanan
            card = ServiceCard(
                layanan_name=layanan,
                edit_button=edit_button,
                hapus_button=hapus_button
            )
            self.grid_layout.addWidget(card, row, col)

        # 3. Tambahkan Kartu "Tambahkan Layanan"
        add_index = len(self.layanan_list)
        add_row = add_index // max_cols
        add_col = add_index % max_cols
        
        add_card = AddServiceCard(add_callback=self.add_layanan)
        self.grid_layout.addWidget(add_card, add_row, add_col)
        
        # 4. Tambahkan stretch ke semua kolom (0, 1, 2) agar lebar seragam
        for col in range(max_cols):
            self.grid_layout.setColumnStretch(col, 1)


    # --- Fungsi Pembuka Dialog Edit ---
    def open_laundry_dialog(self):
        # Memanggil EditLaundryDialog yang diimpor dari components.edit_laundry
        dialog = EditLaundryDialog(self)
        dialog.exec()
    
    def open_catering_dialog(self):
        # Memanggil EditCateringDialog yang diimpor dari components.edit_catering
        dialog = EditCateringDialog(self)
        dialog.exec()
    
    def open_refill_dialog(self):
        # Memanggil EditRefillDialog yang diimpor dari components.edit_refill
        dialog = EditRefillDialog(self)
        dialog.exec()

    def open_belanja_dialog(self):
        self.resize(450, 300)
        self.setMinimumWidth(400)
        # Memanggil EditBelanjaDialog yang diimpor dari components.edit_belanja
        dialog = EditBelanjaDialog(self)
        dialog.exec()

    # --- Fungsi Tambah Layanan ---
    def add_layanan(self):
        """Membuka dialog Tambah Layanan."""
        dialog = AddLayananDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_layanan = dialog.get_layanan()
            if new_layanan:
                if new_layanan not in self.layanan_list:
                    self.layanan_list.append(new_layanan)
                    self.update_layanan_grid() 
                    QMessageBox.information(self, "Berhasil", f"Layanan '{new_layanan}' berhasil ditambahkan.")
                else:
                    QMessageBox.warning(self, "Gagal", f"Layanan '{new_layanan}' sudah ada dalam daftar.")

    # --- Fungsi Hapus Layanan ---
    def show_confirmation_popup(self, layanan):
        """Membuka pop-up konfirmasi hapus."""
        dialog = ConfirmationDialog(layanan, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.layanan_list.remove(layanan)
                self.update_layanan_grid()
                QMessageBox.information(self, "Berhasil", f"Layanan '{layanan}' berhasil dihapus.")
            except ValueError:
                QMessageBox.warning(self, "Gagal Hapus", f"Layanan '{layanan}' tidak ditemukan.")

class ConfirmationDialog(QDialog):
    """Dialog Kustom untuk Konfirmasi Hapus."""
    def __init__(self, layanan, parent=None):
        super().__init__(parent)
        self.layanan = layanan
        self.setWindowTitle('Konfirmasi Hapus')
        self.setFixedSize(380, 180) 
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        confirmation_label = QLabel(f"Apakah Anda yakin untuk menghapus layanan <br><b>{self.layanan}</b>?", self)
        confirmation_label.setObjectName("ConfirmationLabel")
        confirmation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        yes_button = QPushButton('Ya, Hapus', self)
        yes_button.setObjectName("YesButton")
        no_button = QPushButton('Batal', self)
        no_button.setObjectName("NoButton")
        
        yes_button.clicked.connect(self.accept) 
        no_button.clicked.connect(self.reject) 

        button_layout.addWidget(no_button)
        button_layout.addWidget(yes_button)

        layout.addWidget(confirmation_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)


