from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class RefillGalonDialog(QDialog):
    def __init__(self, request_service, user_id):
        super().__init__()
        self.request_service = request_service
        self.user_id = user_id
        self.setWindowTitle("Refill Galon")
        self.setFixedSize(400, 350)
        self.setStyleSheet("QDialog { background: white; } QPushButton { background: #FF9966; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }")
        
        layout = QVBoxLayout(self); layout.setSpacing(15); layout.setContentsMargins(30,30,30,30)
        
        lbl = QLabel("💧 Refill Galon"); lbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold)); lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Jumlah Galon:"))
        self.qty = QLineEdit(); self.qty.setPlaceholderText("1")
        row.addWidget(self.qty)
        layout.addLayout(row)
        
        layout.addStretch()
        btn = QPushButton("Pesan"); btn.clicked.connect(self.submit)
        layout.addWidget(btn)

    def submit(self):
        qty = self.qty.text().strip()
        if not qty.isdigit(): return
        
        if self.request_service:
            res = self.request_service.create_request(
                user_id=self.user_id,
                nama_layanan="Refill Galon",
                catatan=f"Jumlah: {qty} Galon"
            )
            if res["status"] == "success":
                QMessageBox.information(self, "Sukses", "Galon dipesan!")
                self.close()
            else:
                QMessageBox.warning(self, "Gagal", res["message"])