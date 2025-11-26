import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QPushButton, QHeaderView, QFrame, QMessageBox,
    QAbstractItemView
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

# Pastikan path import sesuai struktur project Anda
try:
    from auth.auth_service import AuthService
except ImportError:
    AuthService = None

class ManajemenAkunPage(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.auth_service = AuthService() if AuthService else None
        
        self.setup_ui()
        # Load data awal tanpa notifikasi popup
        self.load_data(show_notification=False)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # --- 1. HEADER SECTION (PERBAIKAN: Hapus Kotak/Border) ---
        header_frame = QFrame()
        # Ubah style menjadi transparan agar menyatu dengan background utama
        header_frame.setStyleSheet("background-color: transparent; border: none;")
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10) # Kurangi margin sedikit
        header_layout.setSpacing(5)

        lbl_title = QLabel("Manajemen Status Penghuni")
        lbl_title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold)) # Font diperbesar sedikit
        lbl_title.setStyleSheet("color: #1E293B;")

        lbl_subtitle = QLabel("Kelola akses masuk penghuni kos. Akun non-aktif tidak akan bisa login.")
        lbl_subtitle.setStyleSheet("color: #64748B; font-size: 14px;")

        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_subtitle)
        layout.addWidget(header_frame)

        # --- 2. TABLE SECTION (PERBAIKAN: Button Terpotong) ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nama Penghuni", "Username", "Status", "Aksi"])
        
        # Style Table Modern
        self.table.verticalHeader().setVisible(False)
        
        # PENTING: Perbesar tinggi baris agar tombol tidak terpotong
        self.table.verticalHeader().setDefaultSectionSize(60) 
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # ID kecil aja
        
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Styling Tabel
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white; border: 1px solid #E2E8F0; border-radius: 10px;
                gridline-color: #F1F5F9; padding: 10px; font-family: 'Segoe UI';
            }
            QTableWidget::item { 
                padding-left: 10px; 
                border-bottom: 1px solid #F1F5F9; 
                color: #334155;
            }
            QHeaderView::section {
                background-color: #F8FAFC; color: #475569; font-weight: bold;
                border: none; padding: 12px; font-size: 13px;
            }
        """)

        layout.addWidget(self.table)
        
        # --- 3. REFRESH BUTTON (PERBAIKAN: Notifikasi) ---
        btn_refresh = QPushButton("🔄 Refresh Data")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFixedSize(140, 45)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6; color: white; border-radius: 8px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #2563EB; }
        """)
        # Panggil load_data dengan show_notification=True saat diklik
        btn_refresh.clicked.connect(lambda: self.load_data(show_notification=True))
        layout.addWidget(btn_refresh, alignment=Qt.AlignmentFlag.AlignRight)

    def load_data(self, show_notification=False):
        """
        Mengambil data dari database dan merender tabel.
        Param show_notification: Jika True, tampilkan popup sukses/gagal.
        """
        if not self.auth_service:
            if show_notification:
                QMessageBox.critical(self, "Error", "Database Service tidak terhubung!")
            return

        try:
            data_penghuni = self.auth_service.get_all_penghuni()
            
            # Reset Tabel
            self.table.setRowCount(0)

            if not data_penghuni:
                if show_notification:
                    QMessageBox.information(self, "Info", "Tidak ada data penghuni ditemukan.")
                return

            for row_idx, row_data in enumerate(data_penghuni):
                self.table.insertRow(row_idx)

                # 1. ID
                item_id = QTableWidgetItem(str(row_data.get('user_id', '')))
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, 0, item_id)
                
                # 2. Nama
                self.table.setItem(row_idx, 1, QTableWidgetItem(row_data.get('nama', '')))
                
                # 3. Username
                self.table.setItem(row_idx, 2, QTableWidgetItem(row_data.get('username', '')))

                # --- STATUS CHECK ---
                raw_status = row_data.get('statusAkun')
                if raw_status is None: raw_status = row_data.get('status_akun')
                
                is_active = False
                try:
                    if str(raw_status) in ['1', 'True', 'true', 'AKTIF']:
                        is_active = True
                except:
                    is_active = False

                # 4. KOLOM STATUS (Badge)
                status_text = "  AKTIF  " if is_active else "  NON-AKTIF  "
                lbl_status = QLabel(status_text)
                lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_status.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                lbl_status.setFixedSize(100, 25) # Ukuran Badge
                
                if is_active:
                    lbl_status.setStyleSheet("color: #065F46; background-color: #D1FAE5; border-radius: 12px;")
                else:
                    lbl_status.setStyleSheet("color: #64748B; background-color: #F1F5F9; border-radius: 12px;")
                
                # Container Layout untuk Status (Agar Center)
                status_container = QWidget()
                s_layout = QHBoxLayout(status_container)
                s_layout.setContentsMargins(0, 0, 0, 0)
                s_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                s_layout.addWidget(lbl_status)
                self.table.setCellWidget(row_idx, 3, status_container)

                # 5. KOLOM AKSI (Tombol)
                # Container Layout untuk Tombol (PENTING AGAR TIDAK TERPOTONG)
                btn_container = QWidget()
                b_layout = QHBoxLayout(btn_container)
                b_layout.setContentsMargins(5, 5, 5, 5)
                b_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                if is_active:
                    btn_aksi = QPushButton("Nonaktifkan")
                    btn_aksi.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn_aksi.setFixedSize(100, 30) # Set ukuran pasti tombol
                    btn_aksi.setStyleSheet("""
                        QPushButton {
                            background-color: #EF4444; color: white; border-radius: 5px; 
                            font-weight: bold; font-size: 12px; border: none;
                        }
                        QPushButton:hover { background-color: #DC2626; }
                    """)
                    
                    u_val = row_data.get('username')
                    btn_aksi.clicked.connect(lambda _, u=u_val: self.handle_nonaktifkan(u))
                    
                    b_layout.addWidget(btn_aksi)
                else:
                    lbl_strip = QLabel("-")
                    lbl_strip.setStyleSheet("color: #CBD5E1; font-weight: bold; font-size: 18px;")
                    b_layout.addWidget(lbl_strip)
                
                self.table.setCellWidget(row_idx, 4, btn_container)

            # Notifikasi Sukses Refresh (Hanya jika tombol diklik)
            if show_notification:
                QMessageBox.information(self, "Sukses", "Data berhasil diperbarui!")

        except Exception as e:
            print(f"Error loading data: {e}")
            if show_notification:
                QMessageBox.warning(self, "Gagal", f"Gagal memuat data: {str(e)}")

    def handle_nonaktifkan(self, username):
        """Memanggil backend untuk mematikan akun"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Konfirmasi Nonaktifkan")
        msg.setText(f"Apakah Anda yakin ingin menonaktifkan akun '{username}'?\nPenghuni tidak akan bisa login lagi.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        # Styling QMessageBox agar sesuai tema
        msg.setStyleSheet("""
            QMessageBox { background-color: white; }
            QLabel { color: #334155; font-size: 13px; }
            QPushButton {
                background-color: #3B82F6; color: white; border-radius: 5px; padding: 6px 15px;
            }
        """)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            result = self.auth_service.nonaktifkan_akun_penghuni(username)
            
            if result['status'] == 'success':
                QMessageBox.information(self, "Berhasil", result['message'])
                # Reload data otomatis tanpa notifikasi popup refresh
                self.load_data(show_notification=False) 
            else:
                QMessageBox.warning(self, "Gagal", result['message'])