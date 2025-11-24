from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QFrame, QMessageBox, QScrollArea, QWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class CateringInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layanan Catering")
        self.setFixedSize(600, 600)
        
        self.setStyleSheet("""
            QDialog { background: white; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; border: none; }
            QFrame#MenuCard {
                background-color: white; border: 1px solid #E2E8F0; border-radius: 12px;
            }
            QComboBox {
                border: 1px solid #CBD5E0; border-radius: 8px; padding: 8px; background: white;
            }
            QPushButton#ActionBtn {
                background-color: #FF9966; color: white; border-radius: 10px; 
                padding: 12px; font-weight: bold; border: none;
            }
            QPushButton#ActionBtn:hover { background-color: #FF8C4D; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        lbl_title = QLabel("🍱 Catering Nasi Bu Imas")
        lbl_title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Grid Menu (Scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        scroll_content = QWidget()
        grid_layout = QHBoxLayout(scroll_content)
        grid_layout.setSpacing(15)

        # Data Paket
        pakets = [
            ("Makan Siang", {"7 Hari": "100rb", "14 Hari": "180rb", "30 Hari": "375rb"}),
            ("Sarapan + Siang", {"7 Hari": "200rb", "14 Hari": "360rb", "30 Hari": "750rb"}),
            ("Full Day (3x)", {"7 Hari": "300rb", "14 Hari": "500rb", "30 Hari": "1jt"}),
        ]

        for judul, harga_dict in pakets:
            card = QFrame(); card.setObjectName("MenuCard")
            card.setFixedWidth(160)
            v = QVBoxLayout(card)
            
            l_jud = QLabel(judul)
            l_jud.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            l_jud.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v.addWidget(l_jud)
            v.addWidget(self._create_line())
            
            for dur, prc in harga_dict.items():
                row = QHBoxLayout()
                row.addWidget(QLabel(dur))
                row.addStretch()
                row.addWidget(QLabel(prc))
                v.addLayout(row)
            
            grid_layout.addWidget(card)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Dropdown
        layout.addWidget(QLabel("Pilih Paket Langganan:"))
        self.combo = QComboBox()
        self.combo.addItems([
            "Makan Siang - 7 Hari", "Makan Siang - 14 Hari", "Makan Siang - 30 Hari",
            "Sarapan + Siang - 7 Hari", "Sarapan + Siang - 14 Hari", "Sarapan + Siang - 30 Hari",
            "Full Day - 7 Hari", "Full Day - 14 Hari", "Full Day - 30 Hari"
        ])
        layout.addWidget(self.combo)

        # Button
        btn = QPushButton("Lanjut Pembayaran")
        btn.setObjectName("ActionBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.process)
        layout.addWidget(btn)

    def _create_line(self):
        line = QFrame(); line.setFixedHeight(1); line.setStyleSheet("background: #EEE;")
        return line

    def process(self):
        QMessageBox.information(self, "Info", f"Anda memilih: {self.combo.currentText()}\n(Fitur Bayar Catering Coming Soon)")
        self.close()