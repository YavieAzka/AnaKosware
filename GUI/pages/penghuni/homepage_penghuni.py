"""
Homepage Penghuni - Updated with Real Data & Bill Details
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFrame, QFileDialog, QMessageBox, QDialog, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

# --- POPUP PEMBAYARAN (Sama seperti sebelumnya) ---
class PembayaranDialog(QDialog):
    def __init__(self, nominal=0, rincian=[]):
        super().__init__()
        self.nominal = nominal
        self.rincian = rincian # List of dict {'item': '...', 'harga': ...}
        self.setWindowTitle("Pembayaran Kos")
        self.setModal(True)
        self.setFixedSize(500, 550) # Sedikit lebih tinggi untuk rincian
        self._setup_style()
        self._setup_ui()

    def _setup_style(self):
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel { font-family: 'Segoe UI', sans-serif; color: #2D3142; border: none; }
            QFrame#BankCard { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 15px; }
            QPushButton#UploadBtn {
                background-color: #FF9966; color: white; font-weight: bold;
                border-radius: 20px; padding: 12px; font-size: 14px; border: none;
            }
            QPushButton#UploadBtn:hover { background-color: #FF8C4D; }
            QTableWidget { border: 1px solid #EEE; gridline-color: #EEE; }
        """)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(15)

        # Header
        title = QLabel("Pembayaran Kos")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Rincian Tabel (Jika ada)
        if self.rincian:
            layout.addWidget(QLabel("Rincian Pembayaran:"))
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Item", "Harga"])
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            table.setRowCount(len(self.rincian))
            table.setFixedHeight(100) # Tinggi terbatas
            
            for i, item in enumerate(self.rincian):
                table.setItem(i, 0, QTableWidgetItem(item['item']))
                price_fmt = f"Rp {item['harga']:,}"
                table.setItem(i, 1, QTableWidgetItem(price_fmt))
            
            layout.addWidget(table)

        # Total Nominal
        lbl_nominal = QLabel(f"Total Transfer: Rp {self.nominal:,}")
        lbl_nominal.setStyleSheet("font-size: 22px; font-weight: bold; color: #E53E3E; margin-top: 5px;")
        lbl_nominal.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(lbl_nominal)

        # Bank Info
        bank_frame = QFrame(); bank_frame.setObjectName("BankCard")
        b_layout = QVBoxLayout(bank_frame)
        self._add_bank_row(b_layout, "BCA", "740411403")
        self._add_bank_row(b_layout, "MANDIRI", "159837200")
        layout.addWidget(bank_frame)

        # Upload Button
        self.upload_btn = QPushButton("📤  Unggah Bukti Bayar")
        self.upload_btn.setObjectName("UploadBtn")
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.clicked.connect(self.upload_bukti)
        layout.addWidget(self.upload_btn)

    def _add_bank_row(self, layout, bank, number):
        row = QHBoxLayout()
        row.addWidget(QLabel(f"<b>{bank}</b>"))
        row.addWidget(QLabel(number))
        row.addStretch()
        layout.addLayout(row)

    def upload_bukti(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih Bukti", "", "Images (*.png *.jpg)")
        if file_path:
            QMessageBox.information(self, "Sukses", "Bukti pembayaran berhasil diupload!\nAdmin akan memverifikasi.")
            self.accept()


# --- HOMEPAGE PENGHUNI ---
class PenghuniHomepage(QWidget):
    def __init__(self, penghuni_data=None):
        super().__init__()
        
        # Default Data
        default_data = {
            "nama": "Penghuni", "kamar": "-", "harga": 0, "masuk": "-",
            "bulan_ke": 0, 
            "bill_status": None, 
            "rincian_tagihan": [], # List rincian item tagihan
            "layanan": {}
        }
        
        if penghuni_data:
            self.data = {**default_data, **penghuni_data}
        else:
            self.data = default_data

        self.setObjectName("Homepage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self):
        self.setStyleSheet("""
            QWidget#Homepage { background-color: #FFFFFF; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; border: none; background: transparent; }
            
            QFrame#InfoCard, QFrame#BillCard, QFrame#ServicesCard {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 16px;
            }
            QFrame#Badge { background-color: #E8D5A8; border-radius: 60px; border: 4px solid white; }
            
            /* Status Styles */
            QFrame.StatusBox { border-radius: 10px; }
            QFrame.StatusDanger { background-color: #FFF5F5; border: 1px solid #FC8181; }
            QLabel.TextDanger { color: #C53030; font-weight: bold; font-size: 16px; }
            QFrame.StatusWarning { background-color: #FFFFF0; border: 1px solid #F6E05E; }
            QLabel.TextWarning { color: #B7791F; font-weight: bold; font-size: 16px; }
            QFrame.StatusSuccess { background-color: #F0FFF4; border: 1px solid #9AE6B4; }
            QLabel.TextSuccess { color: #2F855A; font-weight: bold; font-size: 16px; }
            
            /* Button */
            QPushButton.PayBtn {
                background-color: #E53E3E; color: white; border-radius: 8px;
                padding: 8px; font-weight: bold; border: none;
            }
            QPushButton.PayBtn:hover { background-color: #C53030; }
            
            /* Mini Table in Bill Card */
            QTableWidget {
                background-color: transparent; border: none; font-size: 12px; color: #555;
            }
            QTableWidget::item { padding: 2px; }
        """)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        lbl_welcome = QLabel(f"Halo, {self.data['nama']} 👋")
        lbl_welcome.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        header_layout.addWidget(lbl_welcome)
        header_layout.addWidget(QLabel("Selamat datang kembali. Berikut ringkasan status Anda."))
        main_layout.addLayout(header_layout)

        # Grid (Info & Bill)
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(25)
        grid_layout.addWidget(self._create_info_card(), 2) 
        grid_layout.addWidget(self._create_bill_card(), 1) # Updated Bill Card
        main_layout.addLayout(grid_layout)

        # Layanan
        lbl_layanan = QLabel("Status Layanan Aktif")
        lbl_layanan.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        main_layout.addWidget(lbl_layanan)
        main_layout.addWidget(self._create_services_card())
        
        main_layout.addStretch()

    def _create_shadow(self, target):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20); shadow.setYOffset(4); shadow.setColor(QColor(0,0,0,15))
        target.setGraphicsEffect(shadow)

    # --- INFO CARD ---
    def _create_info_card(self):
        card = QFrame(); card.setObjectName("InfoCard"); self._create_shadow(card)
        layout = QHBoxLayout(card); layout.setContentsMargins(25,25,25,25)
        
        left = QVBoxLayout(); left.setSpacing(15)
        
        harga_val = self.data.get('harga')
        harga_fmt = f"Rp. {harga_val:,}" if harga_val else "Rp. 0"

        left.addLayout(self._row_detail("🏠", "NOMOR KAMAR", self.data.get('kamar', '-')))
        left.addLayout(self._row_detail("📅", "TANGGAL MASUK", self.data.get('masuk', '-')))
        left.addLayout(self._row_detail("💵", "HARGA BULANAN", harga_fmt))
        
        layout.addLayout(left)
        
        badge = QFrame(); badge.setObjectName("Badge"); badge.setFixedSize(120, 120)
        bl = QVBoxLayout(badge); bl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_n = QLabel(str(self.data.get('bulan_ke', 0))); lbl_n.setStyleSheet("font-size: 42px; font-weight: bold;")
        bl.addWidget(lbl_n); bl.addWidget(QLabel("Bulan Ke"))
        
        r_layout = QVBoxLayout(); r_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
        layout.addLayout(r_layout)
        return card

    def _row_detail(self, icon, title, val):
        row = QHBoxLayout()
        lbl_i = QLabel(icon); lbl_i.setFixedSize(24,24)
        v = QVBoxLayout(); v.setSpacing(2)
        l_t = QLabel(title); l_t.setStyleSheet("color:#888; font-size:11px; font-weight:bold;")
        l_v = QLabel(str(val)); l_v.setStyleSheet("font-size:15px; font-weight:600;")
        v.addWidget(l_t); v.addWidget(l_v)
        row.addWidget(lbl_i); row.addLayout(v)
        return row

    # --- BILL CARD (UPDATED: Show Details) ---
    def _create_bill_card(self):
        card = QFrame()
        card.setObjectName("BillCard")
        card.setStyleSheet("QFrame#BillCard { background-color: white; }")
        self._create_shadow(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        lbl_title = QLabel("PENGINGAT TAGIHAN")
        lbl_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #A0AEC0; letter-spacing: 1px;")
        layout.addWidget(lbl_title)

        notif = self.data.get('bill_status')
        rincian = self.data.get('rincian_tagihan', [])

        status_box = QFrame()
        status_box.setProperty("class", "StatusBox")
        sb_layout = QHBoxLayout(status_box)
        sb_layout.setContentsMargins(15, 15, 15, 15)
        
        icon = QLabel()
        msg_title = QLabel()
        
        btn_action = None

        # 1. Aman / Lunas
        if not notif or (notif['type'] == 'info' and notif.get('nominal') == 0):
            status_box.setProperty("class", "StatusBox StatusSuccess")
            icon.setText("✅"); msg_title.setText("LUNAS / AMAN")
            msg_title.setProperty("class", "TextSuccess")
            desc = QLabel(notif['message'] if notif else "Tidak ada tagihan.")
            desc.setStyleSheet("color: #718096; margin-top: 5px;")
            layout.addWidget(status_box); sb_layout.addWidget(icon); sb_layout.addWidget(msg_title); sb_layout.addStretch()
            layout.addWidget(desc)

        # 2. Ada Tagihan (Warning/Danger)
        else:
            style_class = "StatusDanger" if notif['type'] == 'danger' else "StatusWarning"
            text_class = "TextDanger" if notif['type'] == 'danger' else "TextWarning"
            
            status_box.setProperty("class", f"StatusBox {style_class}")
            icon.setText("📢" if notif['type'] == 'danger' else "⚠️")
            msg_title.setText("BELUM DIBAYAR")
            msg_title.setProperty("class", text_class)
            
            sb_layout.addWidget(icon); sb_layout.addWidget(msg_title); sb_layout.addStretch()
            layout.addWidget(status_box)

            # --- TABLE RINCIAN ---
            if rincian:
                lbl_det = QLabel("Rincian:")
                lbl_det.setStyleSheet("font-size: 12px; color: #888; font-weight: bold; margin-top: 5px;")
                layout.addWidget(lbl_det)
                
                tbl = QTableWidget()
                tbl.setColumnCount(2)
                tbl.horizontalHeader().setVisible(False)
                tbl.verticalHeader().setVisible(False)
                tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
                tbl.setRowCount(len(rincian))
                tbl.setFixedHeight(min(100, len(rincian) * 25 + 10)) # Auto height
                tbl.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
                tbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                
                for i, item in enumerate(rincian):
                    tbl.setItem(i, 0, QTableWidgetItem(item['item']))
                    p = f"{item['harga']:,}"
                    it_p = QTableWidgetItem(p)
                    it_p.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                    tbl.setItem(i, 1, it_p)
                
                layout.addWidget(tbl)

            # Tombol Bayar
            nominal_val = notif.get('nominal', 0)
            btn_action = QPushButton(f"Bayar Rp {nominal_val:,}")
            btn_action.setProperty("class", "PayBtn")
            btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
            # Kirim data nominal dan rincian ke dialog
            btn_action.clicked.connect(lambda: self.show_pembayaran_dialog(nominal_val, rincian))
            
            layout.addSpacing(5)
            layout.addWidget(btn_action)

        layout.addStretch()
        return card

    # --- SERVICES CARD (Sama) ---
    def _create_services_card(self):
        card = QFrame(); card.setObjectName("ServicesCard"); self._create_shadow(card)
        layout = QVBoxLayout(card); layout.setContentsMargins(25,20,25,20)
        
        if not self.data.get("layanan"):
            layout.addWidget(QLabel("Tidak ada layanan aktif saat ini."))
            return card
            
        for nama, status in self.data['layanan'].items():
            row = QHBoxLayout()
            row.addWidget(QLabel(nama))
            
            # Status styling
            lbl_s = QLabel(status)
            lbl_s.setFixedSize(120, 28)
            lbl_s.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_s.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            
            st_lower = status.lower()
            if "done" in st_lower or "selesai" in st_lower:
                col, txt = "#C6F6D5", "#22543D"
            elif "progress" in st_lower:
                col, txt = "#FEFCBF", "#744210"
            else:
                col, txt = "#EDF2F7", "#4A5568"
            
            lbl_s.setStyleSheet(f"background-color: {col}; color: {txt}; border-radius: 14px;")
            
            row.addWidget(lbl_s, alignment=Qt.AlignmentFlag.AlignRight)
            layout.addLayout(row)
            line = QFrame(); line.setFixedHeight(1); line.setStyleSheet("background: #F0F0F0;")
            layout.addWidget(line)
            
        return card

    def show_pembayaran_dialog(self, nominal, rincian):
        dlg = PembayaranDialog(nominal, rincian)
        if dlg.exec():
            QMessageBox.information(self, "Info", "Pembayaran sedang diproses.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    # Test data
    d = {
        "nama": "Tes", "harga": 1500000, 
        "bill_status": {"type": "danger", "nominal": 1550000, "message": "Telat"},
        "rincian_tagihan": [{"item": "Sewa Kos", "harga": 1500000}, {"item": "Laundry", "harga": 50000}]
    }
    window = PenghuniHomepage(d)
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec())