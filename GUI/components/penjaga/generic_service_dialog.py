from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, 
    QDoubleSpinBox, QHBoxLayout, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class GenericServiceDialog(QDialog):
    def __init__(self, parent=None, layanan=None):
        super().__init__(parent)
        self.layanan = layanan  # Jika None = Mode Tambah, Jika Ada = Mode Edit
        
        mode = "Edit" if layanan else "Tambah"
        self.setWindowTitle(f"{mode} Layanan")
        self.setFixedSize(450, 550)
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel { font-weight: bold; color: #2D3142; font-size: 12px; }
            QLineEdit, QTextEdit, QDoubleSpinBox { 
                padding: 8px; border: 1px solid #ccc; border-radius: 6px; background: #F8F9FA;
            }
            QPushButton#Save { background-color: #FF9800; color: white; padding: 10px; border-radius: 6px; font-weight: bold;}
            QPushButton#Cancel { background-color: #E0E0E0; color: #333; padding: 10px; border-radius: 6px; font-weight: bold;}
        """)

        self.setup_ui()
        if self.layanan:
            self.populate_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Nama
        layout.addWidget(QLabel("Nama Layanan:"))
        self.inp_nama = QLineEdit()
        self.inp_nama.setPlaceholderText("Contoh: Laundry Kilat")
        layout.addWidget(self.inp_nama)

        # Deskripsi
        layout.addWidget(QLabel("Deskripsi:"))
        self.inp_desc = QTextEdit()
        self.inp_desc.setPlaceholderText("Jelaskan detail layanan...")
        self.inp_desc.setFixedHeight(80)
        layout.addWidget(self.inp_desc)

        # Harga
        layout.addWidget(QLabel("Harga (Rp):"))
        self.inp_harga = QDoubleSpinBox()
        self.inp_harga.setRange(0, 100000000)
        self.inp_harga.setSingleStep(1000)
        layout.addWidget(self.inp_harga)

        # Kebutuhan
        layout.addWidget(QLabel("Kebutuhan (Pisahkan dengan koma):"))
        self.inp_kebutuhan = QTextEdit()
        self.inp_kebutuhan.setPlaceholderText("Contoh: Detergen, Pewangi, Plastik")
        self.inp_kebutuhan.setFixedHeight(60)
        layout.addWidget(self.inp_kebutuhan)

        # Tombol
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Batal")
        btn_cancel.setObjectName("Cancel")
        btn_save = QPushButton("Simpan")
        btn_save.setObjectName("Save")

        btn_cancel.clicked.connect(self.reject)
        btn_save.clicked.connect(self.validate_and_accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addStretch()
        layout.addLayout(btn_layout)

    def populate_data(self):
        """Isi form jika mode edit"""
        self.inp_nama.setText(self.layanan.nama)
        self.inp_desc.setText(self.layanan.deskripsi)
        self.inp_harga.setValue(self.layanan.harga)
        # Join list kebutuhan menjadi string koma
        kebutuhan_str = ", ".join(self.layanan.kebutuhan)
        self.inp_kebutuhan.setText(kebutuhan_str)
        
        # Nama tidak boleh diedit agar konsistensi ID terjaga (opsional logic)
        # self.inp_nama.setReadOnly(True) 

    def validate_and_accept(self):
        nama = self.inp_nama.text().strip()
        if not nama:
            QMessageBox.warning(self, "Validasi", "Nama layanan tidak boleh kosong.")
            return
        self.accept()

    def get_data(self):
        """Mengembalikan data dictionary dari form"""
        # Parse kebutuhan string to list
        keb_raw = self.inp_kebutuhan.toPlainText()
        keb_list = [x.strip() for x in keb_raw.split(',') if x.strip()]

        return {
            "nama": self.inp_nama.text().strip(),
            "deskripsi": self.inp_desc.toPlainText().strip(),
            "harga": self.inp_harga.value(),
            "kebutuhan": keb_list
        }