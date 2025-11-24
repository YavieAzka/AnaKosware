from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QFrame, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class RefillGalonDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Refill Galon")
        self.setFixedSize(450, 400)
        self.setStyleSheet("""
            QDialog { background: white; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; border: none; }
            QFrame#ItemRow { 
                background: #F8FAFC; border-radius: 10px; border: 1px solid #E2E8F0; 
            }
            QLineEdit {
                border: 1px solid #CBD5E0; border-radius: 8px; padding: 5px; width: 50px; text-align: center;
            }
            QPushButton#ActionBtn {
                background-color: #FF9966; color: white; border-radius: 10px; 
                padding: 10px; font-weight: bold; border: none;
            }
            QPushButton#ActionBtn:hover { background-color: #FF8C4D; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        lbl = QLabel("💧 Pesan Refill Galon")
        lbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        self.produk = [("Le Minerale 15L", 20000), ("AQUA 19L", 25000)]
        self.inputs = []

        for nama, harga in self.produk:
            frame = QFrame(); frame.setObjectName("ItemRow")
            h = QHBoxLayout(frame); h.setContentsMargins(15,10,15,10)
            
            h.addWidget(QLabel(nama))
            h.addStretch()
            h.addWidget(QLabel(f"Rp {harga:,}"))
            
            qty = QLineEdit(); qty.setPlaceholderText("0")
            self.inputs.append(qty)
            h.addWidget(qty)
            
            layout.addWidget(frame)

        layout.addStretch()
        
        btn = QPushButton("Pesan & Bayar")
        btn.setObjectName("ActionBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.process)
        layout.addWidget(btn)

    def process(self):
        total = 0
        pesanan = []
        for i, inp in enumerate(self.inputs):
            val = inp.text().strip()
            if val.isdigit() and int(val) > 0:
                qty = int(val)
                harga = self.produk[i][1]
                total += qty * harga
                pesanan.append(f"{self.produk[i][0]} x{qty}")
        
        if total == 0:
            QMessageBox.warning(self, "Error", "Masukkan jumlah galon minimal 1.")
            return
            
        QMessageBox.information(self, "Tagihan", f"Pesanan: {', '.join(pesanan)}\nTotal: Rp {total:,}\n\n(Silakan transfer ke rekening Admin)")
        self.close()