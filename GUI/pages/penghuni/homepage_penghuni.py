"""
Homepage Penghuni - Final Version
Features: Real Payment Integration, Clean Bill Layout, See More Details.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFrame, QFileDialog, QMessageBox, QDialog, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy
)
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtCore import Qt

# --- IMPORT SERVICE ---
try:
    from payment.payment_service import PaymentService
except ImportError:
    PaymentService = None

# --- DIALOG RINCIAN LENGKAP ---
class BillDetailDialog(QDialog):
    def __init__(self, rincian):
        super().__init__()
        self.setWindowTitle("Rincian Tagihan Lengkap")
        self.setModal(True)
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel { font-family: 'Segoe UI'; color: #2D3142; }
            QTableWidget { border: 1px solid #E2E8F0; gridline-color: #F1F5F9; }
            QHeaderView::section { background-color: #F8FAFC; padding: 8px; border: none; font-weight: bold; color: #475569; }
            QPushButton { background-color: #CBD5E0; border: none; border-radius: 8px; padding: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #A0AEC0; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25); layout.setSpacing(15)
        
        lbl = QLabel("Daftar Tagihan Belum Dibayar")
        lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(lbl)
        
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Nama Layanan/Item", "Nominal"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.setRowCount(len(rincian))
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        total = 0
        for i, item in enumerate(rincian):
            table.setItem(i, 0, QTableWidgetItem(item['item']))
            price = item['harga']
            total += price
            p_item = QTableWidgetItem(f"Rp {price:,}")
            p_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            table.setItem(i, 1, p_item)
            
        layout.addWidget(table)
        
        lbl_total = QLabel(f"Total Keseluruhan: Rp {total:,}")
        lbl_total.setStyleSheet("font-size: 14px; font-weight: bold; color: #E53E3E; margin-top: 10px;")
        lbl_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(lbl_total)
        
        btn_close = QPushButton("Tutup")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)


# --- DIALOG PEMBAYARAN ---
class PembayaranDialog(QDialog):
    def __init__(self, nominal=0, rincian=[], user_id=None, is_layanan=False, request_id=None):
        super().__init__()
        self.nominal = nominal
        self.rincian = rincian
        self.user_id = user_id  # PENTING: Menyimpan User ID untuk proses upload
        self.is_layanan = is_layanan
        self.request_id = request_id

        self.setWindowTitle("Pembayaran Kos")
        self.setModal(True)
        self.setFixedSize(500, 550)
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

        title = QLabel("Pembayaran Kos")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        if self.rincian:
            layout.addWidget(QLabel("Ringkasan Item:"))
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Item", "Harga"])
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            
            display_limit = min(len(self.rincian), 3)
            table.setRowCount(display_limit)
            table.setFixedHeight(100) 
            
            for i in range(display_limit):
                item = self.rincian[i]
                table.setItem(i, 0, QTableWidgetItem(item['item']))
                table.setItem(i, 1, QTableWidgetItem(f"Rp {item['harga']:,}"))
            
            layout.addWidget(table)
            if len(self.rincian) > 3:
                layout.addWidget(QLabel(f"...dan {len(self.rincian)-3} item lainnya."))

        lbl_nominal = QLabel(f"Total Transfer: Rp {self.nominal:,}")
        lbl_nominal.setStyleSheet("font-size: 22px; font-weight: bold; color: #E53E3E; margin-top: 5px;")
        lbl_nominal.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(lbl_nominal)

        bank_frame = QFrame(); bank_frame.setObjectName("BankCard")
        b_layout = QVBoxLayout(bank_frame)
        self._add_bank_row(b_layout, "BCA", "740411403")
        self._add_bank_row(b_layout, "MANDIRI", "159837200")
        layout.addWidget(bank_frame)

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
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Bukti", "", "Images (*.png *.jpg *.jpeg)"
        )

        if not file_path:
            return

        if not PaymentService or not self.user_id:
            QMessageBox.critical(self, "Error", "Service Pembayaran tidak tersedia.")
            return

        service = PaymentService()

        if self.is_layanan:
            result = service.process_layanan_payment(
                user_id=self.user_id,
                request_id=self.request_id,
                nominal=self.nominal,
                file_path_asal=file_path
            )
        else:
            result = service.process_monthly_payment(
                self.user_id,
                self.nominal,
                file_path
            )

        if result["status"] == "success":
            QMessageBox.information(self, "Sukses", result["message"])
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", result["message"])


# --- HOMEPAGE PENGHUNI ---
class PenghuniHomepage(QWidget):
    def __init__(self, penghuni_data=None):
        super().__init__()
        
        default_data = {
            "user_id": None,
            "nama": "Penghuni", "kamar": "-", "harga": 0, "masuk": "-",
            "bulan_ke": 0,
            "bill_status": None,
            "rincian_tagihan": [],
            "layanan": [] 
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
            QFrame.StatusBox { border-radius: 10px; }
            QFrame.StatusDanger { background-color: #FFF5F5; border: 1px solid #FC8181; }
            QLabel.TextDanger { color: #C53030; font-weight: bold; font-size: 16px; }
            QFrame.StatusWarning { background-color: #FFFFF0; border: 1px solid #F6E05E; }
            QLabel.TextWarning { color: #B7791F; font-weight: bold; font-size: 16px; }
            QFrame.StatusSuccess { background-color: #F0FFF4; border: 1px solid #9AE6B4; }
            QLabel.TextSuccess { color: #2F855A; font-weight: bold; font-size: 16px; }
            QPushButton.PayBtn {
                background-color: #E53E3E; color: white; border-radius: 8px;
                padding: 8px; font-weight: bold; border: none;
            }
            QPushButton.PayBtn:hover { background-color: #C53030; }
            QPushButton.LinkBtn {
                background-color: transparent; color: #4A90E2; font-size: 12px; border: none;
                text-align: left;
            }
            QPushButton.LinkBtn:hover { text-decoration: underline; color: #2B6CB0; }
            QTableWidget { background-color: transparent; border: none; font-size: 13px; color: #4A5568; }
            QTableWidget::item { padding-top: 5px; padding-bottom: 5px; border-bottom: 1px solid #F0F0F0; }
        """)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40); main_layout.setSpacing(30)

        header_layout = QVBoxLayout(); header_layout.setSpacing(5)
        lbl_welcome = QLabel(f"Halo, {self.data['nama']} 👋")
        lbl_welcome.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        header_layout.addWidget(lbl_welcome)
        header_layout.addWidget(QLabel("Selamat datang kembali. Berikut ringkasan status Anda."))
        main_layout.addLayout(header_layout)

        grid_layout = QHBoxLayout(); grid_layout.setSpacing(25)
        grid_layout.addWidget(self._create_info_card(), 2) 
        grid_layout.addWidget(self._create_bill_card(), 1)
        main_layout.addLayout(grid_layout)

        lbl_layanan = QLabel("Status Layanan Aktif")
        lbl_layanan.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        main_layout.addWidget(lbl_layanan)
        main_layout.addWidget(self._create_services_card())
        main_layout.addStretch()

    def _create_shadow(self, target):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20); shadow.setYOffset(4); shadow.setColor(QColor(0,0,0,15))
        target.setGraphicsEffect(shadow)

    def _create_info_card(self):
        card = QFrame(); card.setObjectName("InfoCard"); self._create_shadow(card)
        layout = QHBoxLayout(card); layout.setContentsMargins(25,25,25,25)
        
        left = QVBoxLayout(); left.setSpacing(15)
        harga_val = self.data.get('harga'); harga_fmt = f"Rp. {harga_val:,}" if harga_val else "Rp. 0"
        left.addLayout(self._row_detail("🏠", "NOMOR KAMAR", self.data.get('kamar', '-')))
        left.addLayout(self._row_detail("📅", "TANGGAL MASUK", self.data.get('masuk', '-')))
        left.addLayout(self._row_detail("💵", "HARGA BULANAN", harga_fmt))
        layout.addLayout(left)
        
        badge = QFrame(); badge.setObjectName("Badge"); badge.setFixedSize(120, 120)
        badge_layout = QVBoxLayout(badge); badge_layout.setContentsMargins(0, 0, 0, 0); badge_layout.setSpacing(0); badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_n = QLabel(str(self.data.get('bulan_ke', 0)))
        lbl_n.setStyleSheet("font-size: 48px; font-weight: bold; color: #2D3142; margin-top: 10px;")
        lbl_n.setAlignment(Qt.AlignmentFlag.AlignCenter); lbl_n.setFixedHeight(50)
        lbl_txt = QLabel("Bulan Ke"); lbl_txt.setStyleSheet("font-size: 12px; color: #555; font-weight: 600; margin-bottom: 10px;")
        lbl_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_layout.addWidget(lbl_n); badge_layout.addWidget(lbl_txt)
        r_layout = QVBoxLayout(); r_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
        layout.addLayout(r_layout)
        return card

    def _row_detail(self, icon, title, val):
        row = QHBoxLayout(); lbl_i = QLabel(icon); lbl_i.setFixedSize(24,24)
        v = QVBoxLayout(); v.setSpacing(2)
        l_t = QLabel(title); l_t.setStyleSheet("color:#888; font-size:11px; font-weight:bold;")
        l_v = QLabel(str(val)); l_v.setStyleSheet("font-size:15px; font-weight:600;")
        v.addWidget(l_t); v.addWidget(l_v)
        row.addWidget(lbl_i); row.addLayout(v)
        return row

    def _create_bill_card(self):
        card = QFrame()
        card.setObjectName("BillCard")
        card.setStyleSheet("QFrame#BillCard { background-color: white; }")
        self._create_shadow(card)

        # >>> tambahkan tinggi minimum supaya isi tidak ke-clip
        card.setMinimumHeight(280)  # boleh disesuaikan, 280–320 juga oke
        card.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Fixed)
        # <<<

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

        # --- LUNAS / AMAN ---
        if not notif or (notif['type'] == 'info' and notif.get('nominal') == 0):
            status_box.setProperty("class", "StatusBox StatusSuccess")
            icon.setText("✅")
            msg_title.setText("LUNAS / AMAN")
            msg_title.setProperty("class", "TextSuccess")

            sb_layout.addWidget(icon)
            sb_layout.addWidget(msg_title)
            sb_layout.addStretch()
            layout.addWidget(status_box)

            desc = QLabel(notif['message'] if notif else "Tidak ada tagihan.")
            desc.setStyleSheet("color: #718096; margin-top: 5px;")
            layout.addWidget(desc)

        # --- MASIH ADA TAGIHAN ---
        else:
            style = "StatusDanger" if notif['type'] == 'danger' else "StatusWarning"
            text_class = "TextDanger" if notif['type'] == 'danger' else "TextWarning"

            status_box.setProperty("class", f"StatusBox {style}")
            icon.setText("📢" if notif['type'] == 'danger' else "⚠️")
            msg_title.setText("BELUM DIBAYAR")
            msg_title.setProperty("class", text_class)

            sb_layout.addWidget(icon)
            sb_layout.addWidget(msg_title)
            sb_layout.addStretch()
            layout.addWidget(status_box)

            # --- Rincian tagihan ---
            if rincian:
                layout.addSpacing(10)

                lbl_det = QLabel("Rincian:")
                lbl_det.setStyleSheet(
                    "font-size: 12px; color: #888; font-weight: bold;"
                )
                layout.addWidget(lbl_det)

                MAX_DISPLAY = 3
                display_data = rincian[:MAX_DISPLAY]

                tbl = QTableWidget()
                tbl.setColumnCount(2)
                tbl.horizontalHeader().setVisible(False)
                tbl.verticalHeader().setVisible(False)
                tbl.setShowGrid(False)
                tbl.horizontalHeader().setSectionResizeMode(
                    0, QHeaderView.ResizeMode.Stretch
                )
                tbl.horizontalHeader().setSectionResizeMode(
                    1, QHeaderView.ResizeMode.ResizeToContents
                )
                tbl.setRowCount(len(display_data))
                tbl.setFixedHeight(len(display_data) * 30 + 5)
                tbl.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
                tbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)

                for i, item in enumerate(display_data):
                    tbl.setItem(i, 0, QTableWidgetItem(item['item']))
                    it_p = QTableWidgetItem(f"{item['harga']:,}")
                    it_p.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    it_p.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                    tbl.setItem(i, 1, it_p)

                layout.addWidget(tbl)

                if len(rincian) > MAX_DISPLAY:
                    sisa = len(rincian) - MAX_DISPLAY
                    btn_more = QPushButton(f"Lihat {sisa} item lainnya...")
                    btn_more.setProperty("class", "LinkBtn")
                    btn_more.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn_more.clicked.connect(
                        lambda: self.show_detail_dialog(rincian)
                    )
                    layout.addWidget(btn_more)

            # --- Tombol Bayar ---
            nominal_val = notif.get('nominal', 0)
            btn_action = QPushButton(f"Bayar Rp {nominal_val:,}")
            btn_action.setProperty("class", "PayBtn")
            btn_action.setCursor(Qt.CursorShape.PointingHandCursor)

            btn_action.setMinimumHeight(42)
            btn_action.setSizePolicy(QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Fixed)

            user_id_val = self.data.get('user_id')
            btn_action.clicked.connect(
                lambda: self.show_pembayaran_dialog(nominal_val, rincian, user_id_val)
            )

            layout.addSpacing(10)
            layout.addWidget(btn_action)

        layout.addStretch()
        return card

    def _create_services_card(self):
        card = QFrame(); card.setObjectName("ServicesCard"); self._create_shadow(card)
        layout = QVBoxLayout(card); layout.setContentsMargins(25,20,25,20)

        layanan_list = self.data.get("layanan") or []
        if not layanan_list:
            layout.addWidget(QLabel("Tidak ada layanan aktif saat ini."))
            return card

        for layanan in layanan_list:
            row = QHBoxLayout()

            # Nama layanan
            row.addWidget(QLabel(layanan["nama"]))

            # STATUS LAYANAN (pending / in progress / done / dst)
            status_layanan = (layanan.get("status_layanan") or "-")
            status_layanan_lower = status_layanan.lower()

            lbl_s = QLabel(status_layanan)
            lbl_s.setFixedSize(120, 28)
            lbl_s.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_s.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

            # warna badge berdasarkan status_layanan
            if "done" in status_layanan_lower or "selesai" in status_layanan_lower:
                bg, fg = "#C6F6D5", "#22543D"
            elif "progress" in status_layanan_lower or "proses" in status_layanan_lower or "pending" in status_layanan_lower:
                bg, fg = "#FEFCBF", "#744210"
            else:
                bg, fg = "#EDF2F7", "#4A5568"

            lbl_s.setStyleSheet(f"background-color: {bg}; color: {fg}; border-radius: 14px;")
            row.addWidget(lbl_s, alignment=Qt.AlignmentFlag.AlignRight)

            layout.addLayout(row)

        return card

    def show_pembayaran_dialog(self, nominal, rincian, user_id):
        # default: anggap tagihan sewa
        is_layanan = False
        request_id = None

        # Kalau hanya ada 1 item dan jenisnya LAYANAN → anggap pembayaran layanan
        if rincian and len(rincian) == 1:
            jenis = rincian[0].get("jenis")
            if jenis == "LAYANAN":
                is_layanan = True
                request_id = rincian[0].get("request_id")

        dlg = PembayaranDialog(
            nominal=nominal,
            rincian=rincian,
            user_id=user_id,
            is_layanan=is_layanan,
            request_id=request_id
        )
        if dlg.exec():
            msg = QMessageBox(self)
            msg.setWindowTitle("Info")
            msg.setText("Pembayaran sedang diproses.")
            msg.setIcon(QMessageBox.Icon.Information)

            # Paksa warna background & teks supaya kontras, tidak ikut tema hitam
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #FFFFFF;
                }
                QMessageBox QLabel {
                    color: #1F2933;
                    font-family: 'Segoe UI';
                    font-size: 12pt;
                }
                QMessageBox QPushButton {
                    min-width: 70px;
                    padding: 6px 14px;
                }
            """)

            msg.exec()


    def show_detail_dialog(self, rincian):
        dlg = BillDetailDialog(rincian)
        dlg.exec()
    def show_layanan_payment_dialog(self, layanan):
        dlg = PembayaranDialog(
            nominal=layanan["harga"],
            rincian=[{
                "item": layanan["nama"],
                "harga": layanan["harga"]
            }],
            user_id=self.data["user_id"],
            is_layanan=True,
            request_id=layanan["request_id"]
        )

        if dlg.exec():
            msg = QMessageBox(self)
            msg.setWindowTitle("Info")
            msg.setText("Pembayaran sedang diproses.")
            msg.setIcon(QMessageBox.Icon.Information)

            # Paksa warna background & teks supaya kontras, tidak ikut tema hitam
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #FFFFFF;
                }
                QMessageBox QLabel {
                    color: #1F2933;
                    font-family: 'Segoe UI';
                    font-size: 12pt;
                }
                QMessageBox QPushButton {
                    min-width: 70px;
                    padding: 6px 14px;
                }
            """)

            msg.exec()