from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTextEdit, QMessageBox, QFrame
)
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtCore import Qt

class GenericRequestDialog(QDialog):
    def __init__(self, request_service, user_id, layanan_data):
        super().__init__()
        self.request_service = request_service
        self.user_id = user_id
        self.layanan = layanan_data # Object Layanan dari Database
        
        self.setWindowTitle(f"Pesan {self.layanan.nama}")
        self.setFixedSize(400, 450)
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; border: none; }
            QTextEdit {
                border: 1px solid #CBD5E0; border-radius: 8px; padding: 10px; font-size: 14px; background: #F8FAFC;
            }
            QPushButton#ActionBtn {
                background-color: #FF9966; color: white; border-radius: 10px; 
                padding: 10px; font-weight: bold; border: none;
            }
            QPushButton#ActionBtn:hover { background-color: #FF8C4D; }
            QFrame#Card {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Header
        lbl_title = QLabel(f"📦 {self.layanan.nama}")
        lbl_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Info Harga & Deskripsi
        info_card = QFrame(); info_card.setObjectName("Card")
        v_card = QVBoxLayout(info_card)
        
        lbl_desc = QLabel(self.layanan.deskripsi)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #64748B; font-size: 13px;")
        
        lbl_price = QLabel(f"Harga: Rp {self.layanan.harga:,.0f}")
        lbl_price.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        lbl_price.setStyleSheet("color: #FF9966;")
        
        v_card.addWidget(lbl_desc)
        v_card.addWidget(lbl_price)
        layout.addWidget(info_card)

        # Input Catatan
        layout.addWidget(QLabel("Catatan Tambahan (Opsional):"))
        self.input_catatan = QTextEdit()
        self.input_catatan.setPlaceholderText("Contoh: Tolong dikerjakan jam 10 pagi...")
        layout.addWidget(self.input_catatan)

        layout.addStretch()

        # Tombol Submit
        btn = QPushButton("Ajukan Request")
        btn.setObjectName("ActionBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.submit)
        layout.addWidget(btn)

    def submit(self):
        catatan = self.input_catatan.toPlainText().strip()
        
        # Panggil Backend
        if self.request_service:
            result = self.request_service.create_request(
                user_id=self.user_id,
                nama_layanan=self.layanan.nama,
                catatan=catatan if catatan else "Tanpa Catatan"
            )
            
            if result["status"] == "success":
                QMessageBox.information(self, "Sukses", "Request berhasil dikirim!")
                self.close()
            else:
                QMessageBox.warning(self, "Gagal", result["message"])