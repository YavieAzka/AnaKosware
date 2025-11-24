from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class BelanjaInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jastip Belanja")
        self.setFixedSize(500, 500)
        self.setStyleSheet("""
            QDialog { background: white; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; border: none; }
            QLineEdit {
                border: 1px solid #CBD5E0; border-radius: 8px; padding: 10px; font-size: 14px;
            }
            QTableWidget {
                background-color: white; border: 1px solid #E2E8F0; gridline-color: #F0F0F0;
            }
            QPushButton#ActionBtn {
                background-color: #FF9966; color: white; border-radius: 10px; 
                padding: 10px; font-weight: bold; border: none;
            }
            QPushButton#ActionBtn:hover { background-color: #FF8C4D; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        lbl = QLabel("🛒 Titip Belanja Kebutuhan")
        lbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        # Table Referensi Harga
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Barang Umum", "Estimasi Harga"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        items = [("Sabun Mandi", "Rp 5.000"), ("Shampoo Sachet", "Rp 1.000"), ("Mie Instan", "Rp 3.500"), ("Telur (Butir)", "Rp 2.500")]
        self.table.setRowCount(len(items))
        for i, (n, p) in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(n))
            self.table.setItem(i, 1, QTableWidgetItem(p))
            
        layout.addWidget(QLabel("Referensi Harga:"))
        layout.addWidget(self.table)

        # Input Manual
        layout.addWidget(QLabel("Tulis pesanan (Format: Barang Jumlah Estimasi)"))
        self.input_barang = QLineEdit()
        self.input_barang.setPlaceholderText("Contoh: Telur 5 12500")
        layout.addWidget(self.input_barang)

        layout.addStretch()

        btn = QPushButton("Ajukan Request")
        btn.setObjectName("ActionBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.submit)
        layout.addWidget(btn)

    def submit(self):
        text = self.input_barang.text().strip()
        if not text:
            QMessageBox.warning(self, "Error", "Pesanan tidak boleh kosong.")
            return
        
        QMessageBox.information(self, "Sukses", "Request belanja dikirim ke penjaga!\nTotal biaya akan dikonfirmasi nanti.")
        self.close()