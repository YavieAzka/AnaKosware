from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class BelanjaInputDialog(QDialog):
    def __init__(self, request_service, user_id):
        super().__init__()
        self.request_service = request_service
        self.user_id = user_id
        self.setWindowTitle("Jastip Belanja")
        self.setFixedSize(450, 400)
        self.setStyleSheet("QDialog { background: white; } QPushButton { background: #FF9966; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        
        layout = QVBoxLayout(self); layout.setContentsMargins(30,30,30,30); layout.setSpacing(15)
        
        lbl = QLabel("🛒 Titip Belanja"); lbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold)); lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
        
        layout.addWidget(QLabel("Daftar Barang:"))
        self.inp = QLineEdit(); self.inp.setPlaceholderText("Telur 1kg, Minyak 1L...")
        layout.addWidget(self.inp)
        
        layout.addStretch()
        btn = QPushButton("Request"); btn.clicked.connect(self.submit)
        layout.addWidget(btn)

    def submit(self):
        barang = self.inp.text().strip()
        if not barang: return
        
        if self.request_service:
            res = self.request_service.create_request(
                user_id=self.user_id,
                nama_layanan="Belanja Kebutuhan",
                catatan=f"Barang: {barang}"
            )
            if res["status"] == "success":
                QMessageBox.information(self, "Sukses", "Request belanja terkirim!")
                self.close()
            else:
                QMessageBox.warning(self, "Gagal", res["message"])