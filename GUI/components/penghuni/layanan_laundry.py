from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFileDialog, QLineEdit, QFrame, QMessageBox
)
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt

class LaundryInputDialog(QDialog):
    def __init__(self, request_service, user_id):
        super().__init__()
        self.request_service = request_service
        self.user_id = user_id
        
        self.setWindowTitle("Layanan Laundry")
        self.setFixedSize(450, 350)
        self.setStyleSheet("""
            QDialog { background: white; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; border: none; }
            QLineEdit { border: 1px solid #CBD5E0; border-radius: 8px; padding: 8px; }
            QPushButton { background-color: #FF9966; color: white; border-radius: 10px; padding: 10px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #FF8C4D; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30,30,30,30); layout.setSpacing(20)
        
        lbl = QLabel("⚖️ Input Berat Cucian"); lbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
        
        layout.addWidget(QLabel("Harga: Rp 5.000 / Kg"))
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Berat (Kg):"))
        self.inp_berat = QLineEdit(); self.inp_berat.setPlaceholderText("0")
        row.addWidget(self.inp_berat)
        layout.addLayout(row)
        
        layout.addStretch()
        btn = QPushButton("Pesan"); btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.submit)
        layout.addWidget(btn)

    def submit(self):
        val = self.inp_berat.text().strip()
        if not val.isdigit() or int(val) <= 0:
            QMessageBox.warning(self, "Error", "Berat tidak valid")
            return
            
        total = int(val) * 5000
        
        if self.request_service:
            res = self.request_service.create_request(
                user_id=self.user_id,
                # --- PERBAIKAN DI SINI (Sesuaikan dengan Database) ---
                nama_layanan="Laundry Kiloan", 
                # -----------------------------------------------------
                catatan=f"Berat: {val} Kg. Estimasi: Rp {total:,}"
            )
            if res["status"] == "success":
                QMessageBox.information(self, "Sukses", f"Laundry berhasil dipesan!\nTotal: Rp {total:,}")
                self.close()
            else:
                QMessageBox.warning(self, "Gagal", res["message"])