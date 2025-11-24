from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class PenghuniLayananPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        # =====================================
        # TITLE
        # =====================================
        title = QLabel("Pemesan Layanan")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))

        main_layout.addWidget(title)
        main_layout.addSpacing(10)

        # =====================================
        # GRID OF CARDS (Layanan)
        # =====================================
        grid = QGridLayout()
        grid.setSpacing(30)

        layanan_list = [
            "Laundry",
            "Catering",
            "Refill Galon",
            "Belanja Kebutuhan",
        ]

        row = 0
        col = 0

        for layanan in layanan_list:
            card = self.create_layanan_card(layanan)
            grid.addWidget(card, row, col)

            col += 1
            if col > 2:  # max 3 per row
                col = 0
                row += 1

        main_layout.addLayout(grid)
        main_layout.addStretch()

        self.setLayout(main_layout)

    # =====================================
    # CARD: LAYANAN INDIVIDUAL
    # =====================================
    def create_layanan_card(self, layanan_name):
        card = QFrame()
        card.setFixedSize(260, 220)

        card.setStyleSheet("""
            QFrame {
                background: #F8F4DE;
                border-radius: 16px;
                border: 1px solid #E0DBBF;
            }
            QLabel {
                font-size: 22px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(25)

        # Nama layanan
        lbl = QLabel(layanan_name)
        lbl.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Tombol pesan
        btn = QPushButton("Pesan")
        btn.setFixedWidth(90)
        btn.setStyleSheet("""
            QPushButton {
                background: #E99670;
                color: white;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #F7A784;
            }
        """)
        if layanan_name == "Catering":
            btn.clicked.connect(self.show_catering_popup)
        elif layanan_name == "Laundry":
            btn.clicked.connect(self.show_laundry_popup)
        elif layanan_name == "Refill Galon":
            btn.clicked.connect(self.show_refill_popup)
        elif layanan_name == "Belanja Kebutuhan":
            belanja_btn.clicked.connect(self.show_belanja_popup)
        else:
            btn.clicked.connect(lambda: self.pesan_layanan(layanan_name))


        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn)
        btn_row.addStretch()

        layout.addWidget(lbl)
        layout.addLayout(btn_row)

        return card

    # =====================================
    # FUNGSI PESAN
    # =====================================
    def pesan_layanan(self, layanan):
        QMessageBox.information(
            self,
            "Layanan Dipesan",
            f"Layanan '{layanan}' berhasil dipesan!"
        )

        # TODO: Simpan ke database:
        # insert_layanan(penghuni_id, layanan)
    
    def show_laundry_popup(self):
    dlg = LaundryInputDialog()
    dlg.exec()

    def show_catering_popup(self):
    from components.layanan_catering import CateringInputDialog
    dlg = CateringInputDialog()
    dlg.exec()

    def show_refill_popup(self):
    from components.layanan_refill_galon import RefillGalonDialog
    dlg = RefillGalonDialog()
    dlg.exec()

    def show_belanja_popup(self):
    from components.layanan_belanja import BelanjaInputDialog
    dialog = BelanjaInputDialog()
    dialog.exec()

    

