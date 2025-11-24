"""
Riwayat Transaksi page for AnaKosware application - PyQt6 Version
Layout: Tabs (Separated Tables for Bills & Services)
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView, QFrame, QMessageBox, 
    QGraphicsDropShadowEffect, QMenu, QTabWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QCursor, QAction

# --- IMPORT BACKEND ---
try:
    from history.bill_history import BillHistory
    from history.service_history import ServiceHistory
except ImportError:
    print("Warning: Backend History Services not found.")
    BillHistory = None
    ServiceHistory = None

class RiwayatTransaksi(QWidget):
    """Halaman untuk menampilkan riwayat transaksi dengan Tab"""
    
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        # --- INISIALISASI BACKEND ---
        if BillHistory and ServiceHistory:
            self.bill_service = BillHistory()
            self.service_history = ServiceHistory()
        else:
            self.bill_service = None
            self.service_history = None
            
        self.setObjectName("TransactionPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)
        
        self._setup_styles()
        self.create_content()

    def _setup_styles(self):
        self.setStyleSheet("""
            QWidget#TransactionPage { background-color: white; }
            QLabel#PageTitle {
                font-family: 'Segoe UI'; font-size: 24px; font-weight: bold; color: #2D3142;
            }
            QLineEdit {
                padding: 10px 15px; border: 1px solid #E0E0E0; border-radius: 8px;
                background-color: #F8F9FA; font-size: 14px; color: #333333;
            }
            QLineEdit:focus { border: 1px solid #4A90E2; background-color: white; }
            QPushButton {
                padding: 8px 20px; border: 1px solid #E0E0E0; border-radius: 8px;
                background-color: white; color: #333333; font-weight: 600;
            }
            QPushButton:hover { background-color: #F5F5F5; }
            
            /* TAB WIDGET STYLING */
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                background: white;
                top: -1px; 
            }
            QTabBar::tab {
                background: #F8F9FA;
                border: 1px solid #E0E0E0;
                padding: 12px 25px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #666;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: #E8D5A8; /* Warna Aksen */
                color: #2D3142;
                border-bottom-color: #E8D5A8; /* Blend with pane */
            }
            
            /* TABLE STYLING */
            QTableWidget {
                background-color: white; border: none; gridline-color: #F0F0F0; font-size: 14px;
            }
            QHeaderView::section {
                background-color: #F1F1F1; color: #333333; padding: 12px;
                border: none; font-weight: bold; font-family: 'Segoe UI';
            }
        """)

    def create_content(self):
        """Membuat layout halaman"""
        # 1. Judul
        title = QLabel("Riwayat Transaksi")
        title.setObjectName("PageTitle")
        self.main_layout.addWidget(title)
        
        # 2. Search Bar Global
        self.create_search_filter()
        
        # 3. Tabs Container
        self.tabs = QTabWidget()
        self.tabs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # --- TAB 1: TAGIHAN BULANAN ---
        self.tab_tagihan = QWidget()
        self.layout_tagihan = QVBoxLayout(self.tab_tagihan)
        self.layout_tagihan.setContentsMargins(10, 20, 10, 10)
        
        cols_tagihan = ["Tanggal Bayar", "Penghuni", "Kamar", "Periode", "Nominal", "Status", "Action"]
        self.table_tagihan = self.create_table_structure(cols_tagihan)
        self.layout_tagihan.addWidget(self.table_tagihan)
        
        # --- TAB 2: RIWAYAT LAYANAN ---
        self.tab_layanan = QWidget()
        self.layout_layanan = QVBoxLayout(self.tab_layanan)
        self.layout_layanan.setContentsMargins(10, 20, 10, 10)
        
        cols_layanan = ["Tanggal Request", "Penghuni", "Kamar", "Jenis Layanan", "Total Harga", "Status Pengerjaan", "Action"]
        self.table_layanan = self.create_table_structure(cols_layanan)
        self.layout_layanan.addWidget(self.table_layanan)
        
        # Add Tabs to Widget
        self.tabs.addTab(self.tab_tagihan, "💰  Tagihan Bulanan")
        self.tabs.addTab(self.tab_layanan, "🛠️  Riwayat Layanan")
        
        # Shadow Effect untuk Tab
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.tabs.setGraphicsEffect(shadow)
        
        self.main_layout.addWidget(self.tabs)
        
        # 4. Load Data
        self.load_data_tagihan()
        self.load_data_layanan()

        # Event saat tab berubah (opsional, utk refresh search)
        self.tabs.currentChanged.connect(self.on_search)

    def create_search_filter(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(15)
        
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("🔍 Cari transaksi (berdasarkan tab yang aktif)...")
        self.search_entry.setMinimumWidth(350)
        self.search_entry.textChanged.connect(self.on_search) 
        
        filter_btn = QPushButton("Refresh ↻")
        filter_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        filter_btn.clicked.connect(self.refresh_data)
        
        layout.addWidget(self.search_entry)
        layout.addStretch()
        layout.addWidget(filter_btn)
        self.main_layout.addWidget(container)

    def create_table_structure(self, columns):
        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Lebar kolom Action fix
        idx_action = len(columns) - 1
        header.setSectionResizeMode(idx_action, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(idx_action, 80)
        
        # Connect signal
        table.cellClicked.connect(lambda r, c, t=table: self.on_cell_click(r, c, t))
        
        return table

    # --- DATA LOADING ---

    def refresh_data(self):
        self.load_data_tagihan()
        self.load_data_layanan()
        QMessageBox.information(self, "Info", "Data berhasil diperbarui.")

    def load_data_tagihan(self):
        if not self.bill_service: return
        try:
            data = self.bill_service.get_riwayat_tagihan()
            self.populate_tagihan(data)
        except Exception as e:
            print(f"Error Tagihan: {e}")

    def load_data_layanan(self):
        if not self.service_history: return
        try:
            data = self.service_history.get_riwayat_layanan()
            self.populate_layanan(data)
        except Exception as e:
            print(f"Error Layanan: {e}")

    def populate_tagihan(self, data_list):
        table = self.table_tagihan
        table.setRowCount(0)
        table.setRowCount(len(data_list))
        
        self.tagihan_map = {} # Simpan data asli untuk popup

        for i, item in enumerate(data_list):
            self.tagihan_map[i] = item
            
            # Kolom: Tanggal, Penghuni, Kamar, Periode, Nominal, Status, Action
            self.set_cell(table, i, 0, item['tanggal'])
            self.set_cell(table, i, 1, f"{item['nama_penghuni']}\n({item['username']})")
            self.set_cell(table, i, 2, item['kamar'])
            self.set_cell(table, i, 3, item['periode'])
            
            nominal = f"Rp. {item['nominal']:,.0f}".replace(",", ".")
            self.set_cell(table, i, 4, nominal)
            
            self.set_status_cell(table, i, 5, item['status'])
            self.set_action_cell(table, i, 6)
            
            table.setRowHeight(i, 55)

    def populate_layanan(self, data_list):
        table = self.table_layanan
        table.setRowCount(0)
        table.setRowCount(len(data_list))
        
        self.layanan_map = {}

        for i, item in enumerate(data_list):
            self.layanan_map[i] = item
            
            # Kolom: Tanggal, Penghuni, Kamar, Jenis Layanan, Harga, Status, Action
            self.set_cell(table, i, 0, item['tanggal'])
            self.set_cell(table, i, 1, f"{item['nama_penghuni']}\n({item['username']})")
            self.set_cell(table, i, 2, item['nomor_kamar'])
            self.set_cell(table, i, 3, item['layanan'])
            
            harga = f"Rp. {item['total_harga']:,.0f}".replace(",", ".")
            self.set_cell(table, i, 4, harga)
            
            self.set_status_cell(table, i, 5, item['status'])
            self.set_action_cell(table, i, 6)
            
            table.setRowHeight(i, 55)

    # --- HELPER UNTUK ISI TABEL ---
    
    def set_cell(self, table, row, col, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setItem(row, col, item)

    def set_status_cell(self, table, row, col, status_text):
        item = QTableWidgetItem(status_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        item.setFont(font)
        
        # Coloring logic
        if status_text in ['Diterima', 'Selesai']:
            item.setForeground(QColor("#28A745")) # Hijau
        elif status_text in ['Ditolak']:
            item.setForeground(QColor("#DC3545")) # Merah
        else:
            item.setForeground(QColor("#FFC107")) # Kuning/Oranye
            
        table.setItem(row, col, item)

    def set_action_cell(self, table, row, col):
        item = QTableWidgetItem("📝")
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont(); font.setPointSize(12)
        item.setFont(font)
        table.setItem(row, col, item)

    # --- INTERACTION LOGIC ---

    def on_search(self):
        """Filter tabel berdasarkan tab yang sedang aktif"""
        search_text = self.search_entry.text().lower()
        current_idx = self.tabs.currentIndex()
        
        # Tentukan tabel mana yang mau difilter
        target_table = self.table_tagihan if current_idx == 0 else self.table_layanan
        
        for row in range(target_table.rowCount()):
            match = False
            for col in range(target_table.columnCount() - 1): # Skip action
                item = target_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            target_table.setRowHidden(row, not match)

    def on_cell_click(self, row, col, table):
        # Cek apakah kolom terakhir (Action) yang diklik
        action_col_idx = table.columnCount() - 1
        if col == action_col_idx:
            # Tentukan jenis data berdasarkan tabel mana yang dikirim
            data_type = "tagihan" if table == self.table_tagihan else "layanan"
            self.show_action_menu(QCursor.pos(), row, data_type)

    def show_action_menu(self, global_pos, row, data_type):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background: white; border: 1px solid #DDD; padding: 5px; }")
        view_action = menu.addAction("👁️  Lihat Detail")
        
        action = menu.exec(global_pos)
        if action == view_action:
            self.view_detail(row, data_type)

    def view_detail(self, row, data_type):
        # Ambil data asli dari map
        if data_type == "tagihan":
            data = self.tagihan_map.get(row)
            title = "Detail Tagihan Bulanan"
            content = f"""
            <table>
                <tr><td><b>Periode</b></td><td>: {data['periode']}</td></tr>
                <tr><td><b>Penghuni</b></td><td>: {data['nama_penghuni']}</td></tr>
                <tr><td><b>Kamar</b></td><td>: {data['kamar']}</td></tr>
                <tr><td><b>Tanggal Bayar</b></td><td>: {data['tanggal']}</td></tr>
                <tr><td><b>Nominal</b></td><td>: Rp. {data['nominal']:,}</td></tr>
                <tr><td><b>Status</b></td><td>: {data['status']}</td></tr>
            </table>
            <br>
            <b>Bukti Pembayaran:</b><br>
            {data.get('bukti_upload', '(Tidak ada file)')}
            """
        else:
            data = self.layanan_map.get(row)
            title = "Detail Request Layanan"
            content = f"""
            <table>
                <tr><td><b>Layanan</b></td><td>: {data['layanan']}</td></tr>
                <tr><td><b>Penghuni</b></td><td>: {data['nama_penghuni']}</td></tr>
                <tr><td><b>Kamar</b></td><td>: {data['nomor_kamar']}</td></tr>
                <tr><td><b>Tanggal Request</b></td><td>: {data['tanggal']}</td></tr>
                <tr><td><b>Total Biaya</b></td><td>: Rp. {data['total_harga']:,}</td></tr>
                <tr><td><b>Status</b></td><td>: {data['status']}</td></tr>
            </table>
            <br>
            <b>Rincian Kebutuhan:</b><br>
            {data['rincian_barang']}
            <br><br>
            <b>Bukti Pembayaran:</b><br>
            {data.get('bukti_upload', '(Bayar Cash/Belum Upload)')}
            """

        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(content)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

# --- Test Standalone ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = RiwayatTransaksi()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec())