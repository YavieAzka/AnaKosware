"""
Riwayat Transaksi page for AnaKosware application - PyQt6 Version
Style: Modern, Minimalist, Consistent with Dashboard.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView, QFrame, QMessageBox, 
    QGraphicsDropShadowEffect, QMenu
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QCursor, QAction

class RiwayatTransaksi(QWidget):
    """Halaman untuk menampilkan riwayat transaksi"""
    
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        # Setup Basic Properties
        self.setObjectName("TransactionPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)
        
        self._setup_styles()
        self.create_content()

    def _setup_styles(self):
        """Definisi CSS Global untuk halaman ini"""
        self.setStyleSheet("""
            QWidget#TransactionPage {
                background-color: white;
            }
            QLabel#PageTitle {
                font-family: 'Segoe UI', sans-serif;
                font-size: 24px;
                font-weight: bold;
                color: #2D3142;
            }
            /* Search Bar Style */
            QLineEdit {
                padding: 10px 15px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: #F8F9FA;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
                background-color: white;
            }
            /* Filter Button */
            QPushButton {
                padding: 8px 20px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
                color: #333333;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
            /* Table Style */
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                gridline-color: #F0F0F0;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #E8D5A8; /* Warna Header Krem Konsisten */
                color: #333333;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
            QTableWidget::item {
                padding-left: 10px;
                padding-right: 10px;
            }
        """)

    def create_content(self):
        """Membuat konten halaman Riwayat Transaksi"""
        
        # 1. Judul Halaman
        title = QLabel("Riwayat Transaksi")
        title.setObjectName("PageTitle")
        self.main_layout.addWidget(title)
        
        # 2. Search & Filter Section
        self.create_search_filter()
        
        # 3. Table Section
        # Data dummy (Logic sama dengan Tkinter)
        self.data = [
            ["04/17/23", "Rp. 1.000.000", "A01", "1", "Accept"],
            ["04/17/23", "Rp. 1.000.000", "A01", "1", "Decline"],
            ["04/17/23", "Rp. 1.000.000", "A01", "1", "Accept"],
            ["04/17/23", "Rp. 1.000.000", "A01", "1", "Accept"],
            ["04/17/23", "Rp. 1.000.000", "A01", "1", "Decline"],
        ]
        
        columns = ["Tanggal", "Pemasukan", "Username Penghuni", "Bulan ke-", "Status Pembayaran", "Action"]
        self.create_table(columns, self.data)
        
        # Spacer di bawah agar rapi
        self.main_layout.addStretch()

    def create_search_filter(self):
        """Membuat bar pencarian dan tombol filter"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(15)
        
        # Search Input
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("🔍 Search transaksi...")
        self.search_entry.setMinimumWidth(300)
        self.search_entry.textChanged.connect(self.on_search) # Live search
        
        # Filter Button
        filter_btn = QPushButton("Filter ☰")
        filter_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        filter_btn.clicked.connect(self.show_filter)
        
        # Add to layout
        layout.addWidget(self.search_entry)
        layout.addStretch()
        layout.addWidget(filter_btn)
        
        self.main_layout.addWidget(container)

    def create_table(self, columns, data):
        """Membuat tabel transaksi"""
        self.table = QTableWidget()
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # Table Properties
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setMinimumHeight(400) 

        # Header Config
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Atur lebar kolom spesifik agar proporsional
        self.table.setColumnWidth(0, 120) # Tanggal
        self.table.setColumnWidth(3, 80)  # Bulan ke-
        self.table.setColumnWidth(5, 80)  # Action
        
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

        # Populate Data
        self.populate_table(data)
        
        # Connect Signals
        self.table.cellClicked.connect(self.on_cell_click)
        
        # Add shadow effect (Estetika)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.table.setGraphicsEffect(shadow)

        self.main_layout.addWidget(self.table)

    def populate_table(self, data):
        """Mengisi data ke tabel dengan styling modern"""
        self.table.setRowCount(len(data))
        for i, row_data in enumerate(data):
            # 0: Tanggal
            item_date = QTableWidgetItem(row_data[0])
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, item_date)
            
            # 1: Pemasukan
            item_price = QTableWidgetItem(row_data[1])
            item_price.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, item_price)

            # 2: Username
            item_user = QTableWidgetItem(row_data[2])
            item_user.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 2, item_user)

            # 3: Bulan
            item_month = QTableWidgetItem(str(row_data[3]))
            item_month.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, item_month)

            # 4: Status (Dengan pewarnaan teks)
            status_text = row_data[4]
            item_status = QTableWidgetItem(status_text)
            item_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            
            if status_text == "Accept":
                item_status.setForeground(QColor("#28A745")) # Hijau
            elif status_text == "Decline":
                item_status.setForeground(QColor("#DC3545")) # Merah
            
            self.table.setItem(i, 4, item_status)
            
            # 5: Action Icon
            item_action = QTableWidgetItem("📝")
            item_action.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setPointSize(12)
            item_action.setFont(font)
            self.table.setItem(i, 5, item_action)

    def on_search(self):
        """Logic pencarian"""
        search_text = self.search_entry.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            # Search di semua kolom
            for col in range(self.table.columnCount() - 1):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def show_filter(self):
        QMessageBox.information(self, "Filter", "Opsi filter akan datang segera!")

    def on_cell_click(self, row, col):
        """Handle klik pada tabel"""
        # Kolom 5 adalah Action
        if col == 5:
            # Tampilkan menu popup di posisi kursor mouse
            self.show_action_menu(QCursor.pos(), row)

    def show_action_menu(self, global_pos, row):
        """Menampilkan menu konteks (View, Edit, Delete)"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: white; border: 1px solid #E0E0E0; }
            QMenu::item { padding: 8px 24px; }
            QMenu::item:selected { background-color: #F5F5F5; color: black; }
        """)

        view_action = menu.addAction("👁️  Lihat Detail")
        edit_action = menu.addAction("✏️   Edit Status")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️  Hapus")

        action = menu.exec(global_pos)
        
        if action == view_action:
            self.view_selected(row)
        elif action == edit_action:
            self.edit_selected(row)
        elif action == delete_action:
            self.delete_selected(row)

    def get_row_data(self, row):
        """Helper untuk mengambil data baris"""
        data = []
        for col in range(5): # Ambil 5 kolom pertama (skip action)
            data.append(self.table.item(row, col).text())
        return data

    def view_selected(self, row):
        """Melihat detail transaksi"""
        values = self.get_row_data(row)
        details = f"""
        Detail Transaksi:
        
        Tanggal          : {values[0]}
        Pemasukan        : {values[1]}
        Username         : {values[2]}
        Bulan ke-        : {values[3]}
        Status Pembayaran: {values[4]}
        """
        QMessageBox.information(self, "Detail Transaksi", details)

    def edit_selected(self, row):
        """Edit transaksi"""
        values = self.get_row_data(row)
        QMessageBox.information(self, "Edit", f"Edit transaksi user: {values[2]}\n(Fitur coming soon)")

    def delete_selected(self, row):
        """Hapus transaksi"""
        values = self.get_row_data(row)
        response = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus transaksi dari:\n{values[2]}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if response == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)
            QMessageBox.information(self, "Sukses", "Transaksi berhasil dihapus!")

# --- Test Standalone ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = RiwayatTransaksi()
    window.resize(1000, 600)
    window.show()
    
    sys.exit(app.exec())