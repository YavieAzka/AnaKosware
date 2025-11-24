"""
Homepage Penghuni - Modern PyQt6 Version
Fixes: 
1. Force Dark Text (Fix Invisible Text on Dark Mode OS)
2. Remove unwanted borders from Labels (Fix Boxy UI)
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFrame, QFileDialog, QMessageBox, QDialog, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtCore import Qt

# --- POPUP PEMBAYARAN ---
class PembayaranDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pembayaran Kos")
        self.setModal(True)
        self.setFixedSize(500, 450)
        
        # Style Dialog yang diperbaiki
        self.setStyleSheet("""
            QDialog { background-color: white; }
            
            /* Reset Label Style */
            QLabel { 
                font-family: 'Segoe UI', sans-serif; 
                color: #2D3142; 
                border: none; 
            }
            
            QFrame#BankCard {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 15px;
            }
            QPushButton#UploadBtn {
                background-color: #FF9966; color: white; font-weight: bold;
                border-radius: 20px; padding: 12px; font-size: 14px; border: none;
            }
            QPushButton#UploadBtn:hover { background-color: #FF8C4D; }
            QPushButton#CloseBtn {
                background: transparent; border: none; font-size: 18px; color: #888;
            }
            QPushButton#CloseBtn:hover { color: #DC3545; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Pembayaran Kos")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        close_btn = QPushButton("✕")
        close_btn.setObjectName("CloseBtn")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        layout.addLayout(header_layout)

        # Instruksi
        instr = QLabel("Silakan transfer sesuai nominal tagihan ke salah satu rekening di bawah ini:")
        instr.setWordWrap(True)
        instr.setStyleSheet("color: #666; font-size: 13px;")
        layout.addWidget(instr)

        # Bank Info Card
        bank_frame = QFrame()
        bank_frame.setObjectName("BankCard")
        bank_layout = QVBoxLayout(bank_frame)
        bank_layout.setSpacing(15)
        bank_layout.setContentsMargins(20, 20, 20, 20)

        self._add_bank_row(bank_layout, "BCA", "740411403", "A.n AnaKosware")
        self._add_bank_row(bank_layout, "BNI", "159837200", "A.n AnaKosware")
        self._add_bank_row(bank_layout, "MANDIRI", "209388782984", "A.n AnaKosware")

        layout.addWidget(bank_frame)
        layout.addStretch()

        # Upload Button
        self.upload_btn = QPushButton("📤  Unggah Bukti Bayar")
        self.upload_btn.setObjectName("UploadBtn")
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.clicked.connect(self.upload_bukti)
        layout.addWidget(self.upload_btn)

    def _add_bank_row(self, layout, bank_name, acc_number, acc_name):
        row = QHBoxLayout()
        
        lbl_bank = QLabel(bank_name)
        lbl_bank.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lbl_bank.setFixedWidth(80)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        lbl_num = QLabel(acc_number)
        lbl_num.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        
        lbl_name = QLabel(acc_name)
        lbl_name.setStyleSheet("color: #888; font-size: 11px;")
        
        info_layout.addWidget(lbl_num)
        info_layout.addWidget(lbl_name)
        
        btn_copy = QPushButton("Salin")
        btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copy.setStyleSheet("""
            color: #4A90E2; border: 1px solid #4A90E2; 
            border-radius: 5px; padding: 4px 10px; font-size: 11px; background: white;
        """)
        
        row.addWidget(lbl_bank)
        row.addLayout(info_layout)
        row.addStretch()
        row.addWidget(btn_copy)
        
        layout.addLayout(row)
        
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #EEE; border: none;")
        layout.addWidget(line)

    def upload_bukti(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Bukti Pembayaran", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            QMessageBox.information(self, "Upload Sukses", "Bukti pembayaran berhasil diupload!")
            self.close()


# --- HOMEPAGE PENGHUNI ---
class PenghuniHomepage(QWidget):
    def __init__(self, penghuni_data=None):
        super().__init__()
        
        if not penghuni_data:
            self.data = {
                "nama": "Penghuni", "kamar": "-", "harga": 0, "masuk": "-",
                "bulan_ke": 0, "pembayaran_lunas": False, "layanan": {}
            }
        else:
            self.data = penghuni_data

        self.setObjectName("Homepage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self):
        # --- CSS PERBAIKAN ---
        self.setStyleSheet("""
            QWidget#Homepage {
                background-color: #FFFFFF; 
            }
            
            /* PERBAIKAN 1: Paksa semua Label tidak punya border dan warnanya gelap */
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                color: #2D3142;
                border: none;
                background: transparent;
            }
            
            /* PERBAIKAN 2: Hanya QFrame dengan ID tertentu yang punya border */
            QFrame#InfoCard, QFrame#BillCard, QFrame#ServicesCard {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
            
            /* Badge Bulan */
            QFrame#Badge {
                background-color: #E8D5A8;
                border-radius: 60px;
                border: 4px solid white;
            }
            
            /* Tombol */
            QPushButton.ActionBtn {
                background-color: #FF9966; color: white;
                border-radius: 10px; padding: 8px 16px;
                font-weight: bold; border: none;
            }
            QPushButton.ActionBtn:hover { background-color: #FF8C4D; }
        """)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # 1. Welcome Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        lbl_welcome = QLabel(f"Halo, {self.data['nama']} 👋")
        lbl_welcome.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        
        lbl_sub = QLabel("Selamat datang kembali di Kos Melati. Berikut ringkasan status Anda.")
        lbl_sub.setStyleSheet("color: #888; font-size: 16px;")
        
        header_layout.addWidget(lbl_welcome)
        header_layout.addWidget(lbl_sub)
        main_layout.addLayout(header_layout)

        # 2. Top Section (Grid Layout)
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(25)

        # --- CARD 1: INFO KAMAR ---
        card_info = self._create_info_card()
        grid_layout.addWidget(card_info, 2)

        # --- CARD 2: TAGIHAN ---
        card_bill = self._create_bill_card()
        grid_layout.addWidget(card_bill, 1)

        main_layout.addLayout(grid_layout)

        # 3. Bottom Section (Layanan)
        lbl_layanan = QLabel("Status Layanan Aktif")
        lbl_layanan.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        main_layout.addWidget(lbl_layanan)

        card_layanan = self._create_services_card()
        main_layout.addWidget(card_layanan)

        main_layout.addStretch()

    def _create_shadow(self, target_widget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20); shadow.setXOffset(0); shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        target_widget.setGraphicsEffect(shadow)

    # --- CARD BUILDERS ---

    def _create_info_card(self):
        card = QFrame()
        card.setObjectName("InfoCard") # ID Selector digunakan di CSS
        self._create_shadow(card)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Left Side
        details_layout = QVBoxLayout()
        details_layout.setSpacing(15)

        def add_detail_row(icon, label, value):
            row = QHBoxLayout()
            row.setSpacing(10)
            lbl_icon = QLabel(icon)
            lbl_icon.setFixedSize(24, 24)
            lbl_icon.setStyleSheet("font-size: 16px;")
            
            v_layout = QVBoxLayout()
            v_layout.setSpacing(2)
            lbl_title = QLabel(label)
            lbl_title.setStyleSheet("font-size: 12px; color: #888; font-weight: bold;")
            lbl_val = QLabel(value)
            lbl_val.setStyleSheet("font-size: 16px; font-weight: 600;")
            
            v_layout.addWidget(lbl_title)
            v_layout.addWidget(lbl_val)
            
            row.addWidget(lbl_icon)
            row.addLayout(v_layout)
            return row

        details_layout.addLayout(add_detail_row("🏠", "NOMOR KAMAR", self.data['kamar']))
        details_layout.addLayout(add_detail_row("📅", "TANGGAL MASUK", self.data['masuk']))
        details_layout.addLayout(add_detail_row("💵", "HARGA BULANAN", f"Rp. {self.data['harga']:,}"))
        details_layout.addStretch()

        layout.addLayout(details_layout)

        # Right Side (Badge)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        badge = QFrame()
        badge.setObjectName("Badge")
        badge.setFixedSize(120, 120)
        
        badge_shadow = QGraphicsDropShadowEffect(self)
        badge_shadow.setBlurRadius(10); badge_shadow.setColor(QColor(0,0,0,20))
        badge.setGraphicsEffect(badge_shadow)

        badge_layout = QVBoxLayout(badge)
        badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_layout.setSpacing(0)
        
        lbl_angka = QLabel(str(self.data['bulan_ke']))
        lbl_angka.setStyleSheet("font-size: 42px; font-weight: bold;")
        lbl_angka.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_text = QLabel("Bulan Ke")
        lbl_text.setStyleSheet("font-size: 12px; color: #555; font-weight: 600;")
        lbl_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        badge_layout.addWidget(lbl_angka)
        badge_layout.addWidget(lbl_text)
        
        right_layout.addWidget(badge)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(right_layout)
        return card

    def _create_bill_card(self):
        card = QFrame()
        card.setObjectName("BillCard") # ID Selector
        
        # Background card putih agar menonjol dari background abu halus homepage
        card.setStyleSheet("QFrame#BillCard { background-color: white; }")
        self._create_shadow(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        lbl_title = QLabel("Status Tagihan Bulan Ini")
        lbl_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #888; text-transform: uppercase;")
        layout.addWidget(lbl_title)

        is_lunas = self.data["pembayaran_lunas"]

        if is_lunas:
            status_frame = QFrame()
            status_frame.setObjectName("StatusLunas")
            status_frame.setStyleSheet("#StatusLunas { background-color: #E6FFFA; border-radius: 10px; border: 1px solid #B2F5EA; }")
            sf_layout = QHBoxLayout(status_frame)
            
            lbl_icon = QLabel("✅")
            lbl_text = QLabel("LUNAS")
            lbl_text.setStyleSheet("color: #285E61; font-weight: bold; font-size: 18px;")
            
            sf_layout.addWidget(lbl_icon)
            sf_layout.addWidget(lbl_text)
            sf_layout.addStretch()
            
            layout.addWidget(status_frame)
            
            desc = QLabel("Terima kasih sudah membayar tepat waktu.")
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #718096; font-size: 13px;")
            layout.addWidget(desc)
            
        else:
            status_frame = QFrame()
            status_frame.setObjectName("StatusBelum")
            status_frame.setStyleSheet("#StatusBelum { background-color: #FFF5F5; border-radius: 10px; border: 1px solid #FEB2B2; }")
            sf_layout = QHBoxLayout(status_frame)
            
            lbl_icon = QLabel("⚠️")
            lbl_text = QLabel("BELUM LUNAS")
            lbl_text.setStyleSheet("color: #C53030; font-weight: bold; font-size: 18px;")
            
            sf_layout.addWidget(lbl_icon)
            sf_layout.addWidget(lbl_text)
            sf_layout.addStretch()
            
            layout.addWidget(status_frame)
            
            btn_bayar = QPushButton("Bayar Sekarang")
            btn_bayar.setProperty("class", "ActionBtn")
            btn_bayar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_bayar.clicked.connect(self.show_pembayaran_dialog)
            
            layout.addSpacing(10)
            layout.addWidget(btn_bayar)

        layout.addStretch()
        return card

    def _create_services_card(self):
        card = QFrame()
        card.setObjectName("ServicesCard")
        card.setStyleSheet("QFrame#ServicesCard { background-color: white; }")
        self._create_shadow(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(0)

        # Header Row
        header = QHBoxLayout()
        header.setSpacing(10)
        lbl_h1 = QLabel("NAMA LAYANAN"); lbl_h1.setStyleSheet("font-weight: bold; color: #888; font-size: 12px;")
        lbl_h2 = QLabel("STATUS PENGERJAAN"); lbl_h2.setStyleSheet("font-weight: bold; color: #888; font-size: 12px;")
        
        header.addWidget(lbl_h1, stretch=2)
        header.addWidget(lbl_h2, stretch=1)
        header.setAlignment(lbl_h2, Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(header)
        
        line = QFrame(); line.setFixedHeight(1); line.setStyleSheet("background: #EEE; margin-top: 10px; margin-bottom: 10px; border: none;")
        layout.addWidget(line)

        layanan_data = self.data.get("layanan", {})
        if not layanan_data:
            layout.addWidget(QLabel("Tidak ada layanan aktif saat ini."))
        
        for nama, status in layanan_data.items():
            row = QHBoxLayout()
            
            lbl_nama = QLabel(nama)
            lbl_nama.setFont(QFont("Segoe UI", 14))
            
            lbl_status = QLabel(status)
            lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_status.setFixedSize(120, 30)
            lbl_status.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            
            if status == "Done":
                lbl_status.setText("Selesai")
                lbl_status.setStyleSheet("background-color: #C6F6D5; color: #22543D; border-radius: 15px;")
            elif status == "OnProgress":
                lbl_status.setText("Diproses")
                lbl_status.setStyleSheet("background-color: #FEFCBF; color: #744210; border-radius: 15px;")
            else: 
                lbl_status.setText("Menunggu")
                lbl_status.setStyleSheet("background-color: #EDF2F7; color: #4A5568; border-radius: 15px;")
            
            row.addWidget(lbl_nama, stretch=2)
            row.addWidget(lbl_status, stretch=1)
            row.setAlignment(lbl_status, Qt.AlignmentFlag.AlignCenter)
            
            layout.addLayout(row)
            
            sep = QFrame()
            sep.setFixedHeight(1)
            sep.setStyleSheet("background: #FAFAFA; border: none;")
            layout.addWidget(sep)
            
        layout.addStretch()
        return card

    def show_pembayaran_dialog(self):
        dlg = PembayaranDialog()
        dlg.exec()

# --- TEST STANDALONE ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    dummy_data = {
        "nama": "Ahmad Husein",
        "kamar": "A01",
        "harga": 2000000,
        "masuk": "10 Januari 2023",
        "bulan_ke": 7,
        "pembayaran_lunas": False,
        "layanan": {
            "Laundry Kilat": "Waiting",
            "Catering Harian": "Done",
            "Pembersihan Kamar": "OnProgress",
        }
    }
    
    window = PenghuniHomepage(dummy_data)
    window.resize(1000, 700)
    window.show()
    
    sys.exit(app.exec())