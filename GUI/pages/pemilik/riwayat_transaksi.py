import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView, 
    QFrame, QMessageBox, QDialog, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QFont, QColor, QCursor, QPixmap
from PyQt6.QtCore import Qt

# --- IMPORT SERVICE ---
try:
    from verification.verification_service import VerificationService
except ImportError:
    VerificationService = None

class RiwayatTransaksi(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.service = VerificationService() if VerificationService else None
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        lbl_title = QLabel("Riwayat Transaksi Masuk")
        lbl_title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #2D3142;")
        layout.addWidget(lbl_title)

        # Tabel
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tanggal", "Penghuni", "Tipe", "Nominal", "Status", "Aksi"
        ])
        
        # Table Properties
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setShowGrid(False) # Hilangkan grid agar lebih bersih
        
        # Header Resize Modes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # ID
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed) # Status Fixed Width
        self.table.setColumnWidth(5, 130)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed) # Aksi Fixed Width
        self.table.setColumnWidth(6, 100)

        # Style Table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white; 
                border: 1px solid #E2E8F0; 
                border-radius: 10px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #F1F5F9;
            }
            QHeaderView::section {
                background-color: #F8FAFC; 
                padding: 12px; 
                border: none; 
                font-weight: bold; 
                color: #475569;
            }
        """)
        
        layout.addWidget(self.table)
        
        # Refresh Button
        btn_refresh = QPushButton("🔄 Refresh Data")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFixedSize(140, 45)
        btn_refresh.setStyleSheet("""
            QPushButton { background-color: #3B82F6; color: white; border-radius: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #2563EB; }
        """)
        btn_refresh.clicked.connect(self.load_data)
        layout.addWidget(btn_refresh, alignment=Qt.AlignmentFlag.AlignRight)

    def load_data(self):
        if not self.service:
            return
        
        # Bersihkan tabel
        self.table.setRowCount(0)
        
        try:
            data = self.service.get_all_transactions()
        except Exception as e:
            print(f"Error Fetching Data: {e}")
            data = []
        
        self.table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            # Set Height Row agar Widget tidak gepeng
            self.table.setRowHeight(row, 50)

            # 1. ID
            self._set_text_item(row, 0, str(item.get('pembayaran_id', '-')))
            
            # 2. Tanggal
            tgl = item['tanggal_bayar'].strftime("%d/%m/%Y") if item.get('tanggal_bayar') else "-"
            self._set_text_item(row, 1, tgl)
            
            # 3. Penghuni
            nama = item.get('nama_penghuni', 'Unknown')
            kamar = item.get('nomor_kamar', '-')
            self._set_text_item(row, 2, f"{nama} ({kamar})")
            
            # 4. Tipe
            tipe = "Sewa Bulanan" if item.get('jenis_pembayaran') == 'TAGIHAN' else f"Layanan: {item.get('nama_layanan', '-')}"
            self._set_text_item(row, 3, tipe)
            
            # 5. Nominal
            nom = item.get('nominal_pembayaran', 0)
            self._set_text_item(row, 4, f"Rp {int(nom):,}")
            
            # 6. Status (Widget Badge)
            status_txt = item.get('status_pembayaran', 'Unknown')
            self._set_status_widget(row, 5, status_txt)
            
            # 7. Aksi (Widget Button)
            self._set_action_widget(row, 6, item)

    def _set_text_item(self, row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, col, item)

    def _set_status_widget(self, row, col, status_txt):
        # Container
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Label Badge
        lbl = QLabel(status_txt)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        lbl.setFixedSize(120, 26) # Ukuran fix agar rapi
        
        if status_txt == "Sudah diverifikasi":
            style = "color: #065F46; background-color: #D1FAE5; border-radius: 13px;"
        elif status_txt == "Ditolak":
            style = "color: #991B1B; background-color: #FEE2E2; border-radius: 13px;"
        else: # Belum diverifikasi
            style = "color: #92400E; background-color: #FEF3C7; border-radius: 13px;"
            
        lbl.setStyleSheet(style)
        layout.addWidget(lbl)
        self.table.setCellWidget(row, col, container)

    def _set_action_widget(self, row, col, item_data):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn = QPushButton("Lihat Bukti")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(90, 30)
        btn.setStyleSheet("""
            QPushButton { 
                background-color: white;
                border: 1px solid #CBD5E0; 
                border-radius: 6px; 
                color: #475569; 
                font-weight: 600; 
                font-size: 12px;
            }
            QPushButton:hover { background-color: #F1F5F9; border-color: #94A3B8; }
        """)
        
        # Gunakan default argument pada lambda untuk mengunci nilai item_data
        btn.clicked.connect(lambda checked, d=item_data: self.open_detail_dialog(d))
        
        layout.addWidget(btn)
        self.table.setCellWidget(row, col, container)

    def open_detail_dialog(self, data):
        dlg = TransactionDetailDialog(data, self.service, self)
        dlg.exec()
        self.load_data() # Refresh setelah dialog tutup


class TransactionDetailDialog(QDialog):
    def __init__(self, data, service, parent=None):
        super().__init__(parent)
        self.data = data
        self.service = service
        self.setWindowTitle("Verifikasi Pembayaran")
        self.setFixedSize(500, 700)
        self.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Judul
        layout.addWidget(QLabel(f"Detail Transaksi #{self.data['pembayaran_id']}", styleSheet="font-size: 18px; font-weight: bold; color: #2D3142;"))
        
        # Info Grid Frame
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #F8FAFC; border-radius: 10px; border: 1px solid #E2E8F0;")
        gl = QVBoxLayout(info_frame)
        gl.setSpacing(8)
        
        self.add_row(gl, "Penghuni:", self.data.get('nama_penghuni', '-'))
        self.add_row(gl, "Nominal:", f"Rp {int(self.data.get('nominal_pembayaran', 0)):,}")
        self.add_row(gl, "Tanggal:", str(self.data.get('tanggal_bayar', '-')))
        self.add_row(gl, "Status:", self.data.get('status_pembayaran', '-'))
        
        layout.addWidget(info_frame)
        
        # Bukti Gambar Section
        layout.addWidget(QLabel("Bukti Transfer:", styleSheet="font-weight: bold; margin-top: 10px; color: #2D3142;"))
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: 1px dashed #CBD5E0; border-radius: 8px; background-color: #FAFAFA;")
        
        img_container = QLabel()
        img_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Load Gambar
        img_path = self.data.get('bukti_pembayaran')
        if img_path:
            abs_path = os.path.abspath(img_path)
            if os.path.exists(abs_path):
                pixmap = QPixmap(abs_path)
                # Scale tapi tetap pertahankan rasio
                if not pixmap.isNull():
                    scaled = pixmap.scaled(420, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    img_container.setPixmap(scaled)
                else:
                    img_container.setText("Gagal memuat gambar (Format salah).")
            else:
                img_container.setText(f"File tidak ditemukan:\n{abs_path}")
                img_container.setStyleSheet("color: red; padding: 20px;")
        else:
            img_container.setText("Tidak ada bukti upload.")
            
        scroll.setWidget(img_container)
        layout.addWidget(scroll)
        
        # Tombol Aksi (Hanya jika status Belum diverifikasi)
        if self.data.get('status_pembayaran') == 'Belum diverifikasi':
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(15)
            
            btn_tolak = QPushButton("Tolak")
            btn_tolak.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_tolak.setFixedHeight(40)
            btn_tolak.setStyleSheet("""
                QPushButton { background-color: #EF4444; color: white; border-radius: 8px; font-weight: bold; border: none;}
                QPushButton:hover { background-color: #DC2626; }
            """)
            btn_tolak.clicked.connect(lambda: self.process_verif(False))
            
            btn_terima = QPushButton("Terima / Verifikasi")
            btn_terima.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_terima.setFixedHeight(40)
            btn_terima.setStyleSheet("""
                QPushButton { background-color: #10B981; color: white; border-radius: 8px; font-weight: bold; border: none;}
                QPushButton:hover { background-color: #059669; }
            """)
            btn_terima.clicked.connect(lambda: self.process_verif(True))
            
            btn_layout.addWidget(btn_tolak)
            btn_layout.addWidget(btn_terima)
            layout.addLayout(btn_layout)
        else:
            # Jika sudah selesai
            lbl_done = QLabel("Transaksi Selesai")
            lbl_done.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_done.setStyleSheet("color: #64748B; font-weight: bold; margin-top: 10px; font-size: 14px;")
            layout.addWidget(lbl_done)

    def add_row(self, layout, label, val):
        row = QHBoxLayout()
        row.addWidget(QLabel(label, styleSheet="color: #64748B; font-weight: 500;"))
        val_lbl = QLabel(str(val), styleSheet="font-weight: 600; color: #334155;")
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        row.addWidget(val_lbl)
        layout.addLayout(row)

    def process_verif(self, is_valid):
        if self.service.verify_payment(self.data['pembayaran_id'], is_valid):
            msg = "Pembayaran Diterima" if is_valid else "Pembayaran Ditolak"

            # === Pakai QMessageBox dengan style khusus ===
            box = QMessageBox(self)
            box.setIcon(QMessageBox.Icon.Information)
            box.setWindowTitle("Sukses")
            box.setText(msg)
            box.setStandardButtons(QMessageBox.StandardButton.Ok)

            # Biar teks & tombol kelihatan
            box.setStyleSheet("""
                QLabel { 
                    color: #000000; 
                    font-family: 'Segoe UI'; 
                    font-size: 12pt;
                }
                QPushButton {
                    color: #000000;
                    background-color: #E5E7EB;
                    padding: 6px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #CBD5E1;
                }
            """)

            box.exec()
            self.accept()
        else:
            box = QMessageBox(self)
            box.setIcon(QMessageBox.Icon.Warning)
            box.setWindowTitle("Gagal")
            box.setText("Terjadi kesalahan database.")
            box.setStandardButtons(QMessageBox.StandardButton.Ok)
            box.setStyleSheet("""
                QLabel { color: #000000; font-family: 'Segoe UI'; font-size: 12pt; }
                QPushButton { color: #000000; background-color: #FECACA; border-radius: 6px; padding: 6px 16px; }
                QPushButton:hover { background-color: #FCA5A5; }
            """)
            box.exec()