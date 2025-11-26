from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QFrame, QMessageBox, QScrollArea, QWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class CateringInputDialog(QDialog):
    def __init__(self, request_service, user_id):
        super().__init__()
        self.request_service = request_service
        self.user_id = user_id
        self.setWindowTitle("Layanan Catering")
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog { background: white; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; }
            QComboBox { border: 1px solid #ccc; padding: 5px; border-radius: 6px; }
            QPushButton { background-color: #FF9966; color: white; border-radius: 10px; padding: 10px; font-weight: bold; border: none; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30,30,30,30); layout.setSpacing(20)

        lbl = QLabel("🍱 Catering Bu Imas"); lbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        layout.addWidget(QLabel("Pilih Paket:"))
        self.combo = QComboBox()
        self.combo.addItems(["Makan Siang (7 Hari) - 100rb", "Makan Siang (30 Hari) - 375rb", "Full Day (7 Hari) - 300rb"])
        layout.addWidget(self.combo)

        layout.addStretch()
        btn = QPushButton("Pesan"); btn.clicked.connect(self.process)
        layout.addWidget(btn)

    def process(self):
        pilihan = self.combo.currentText()
        if self.request_service:
            res = self.request_service.create_request(
                user_id=self.user_id,
                # --- PERBAIKAN DI SINI (Sesuaikan dengan Database) ---
                nama_layanan="Catering Harian",
                # -----------------------------------------------------
                catatan=f"Paket: {pilihan}"
            )
            if res["status"] == "success":
                QMessageBox.information(self, "Sukses", "Catering berhasil dipesan!")
                self.close()
            else:
                QMessageBox.warning(self, "Gagal", res["message"])