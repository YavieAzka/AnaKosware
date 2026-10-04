"""
Dashboard Penghuni untuk AnaKosware application (PyQt6 Refactor).
Fitur: Menampilkan daftar penghuni REAL dari database.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView, QFrame, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QColor, QCursor

# --- IMPORT SERVICE ---
try:
    from auth.auth_service import AuthService
except ImportError:
    print("Warning: AuthService not found. Using dummy data.")
    AuthService = None

class DashboardPenghuni(QWidget):
    """Dashboard untuk menampilkan daftar penghuni"""
    
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.auth_service = AuthService() if AuthService else None
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)
        
        # Stylesheet
        self.setStyleSheet("""
            QWidget { background-color: white; font-family: 'Segoe UI', Arial, sans-serif; color: #2D3142; }
            QLabel#PageTitle { font-size: 24px; font-weight: bold; color: #2D3142; }
            QLineEdit { padding: 10px; border: 1px solid #E0E0E0; border-radius: 8px; background-color: #F8F9FA; font-size: 14px; }
            QLineEdit:focus { border: 1px solid #4A90E2; background-color: white; }
            QPushButton { padding: 8px 16px; border: 1px solid #E0E0E0; border-radius: 6px; background-color: white; font-weight: 600; }
            QPushButton:hover { background-color: #F0F0F0; border-color: #D0D0D0; }
            QTableWidget { border: 1px solid #E0E0E0; gridline-color: #F0F0F0; selection-background-color: #E8F0FE; selection-color: #2D3142; outline: 0; }
            QHeaderView::section { background-color: #E8D5A8; padding: 12px; border: none; font-weight: bold; color: #333333; }
        """)

        self.create_content()

    def create_content(self):
        # 1. Page Title
        title_label = QLabel("Dashboard Penghuni")
        title_label.setObjectName("PageTitle")
        self.main_layout.addWidget(title_label)

        # 2. Search and Filter
        self.create_search_filter()

        # 3. Table
        # Kolom: No Kamar, Username, Nama Lengkap, Tgl Masuk, Harga, Status, Action
        columns = ["Nomor Kamar", "Username", "Nama Lengkap", "Harga Kamar", "Status Akun", "Action"]
        self.create_table_structure(columns)

    def create_search_filter(self):
        search_layout = QHBoxLayout()
        
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("🔍 Search penghuni...")
        self.search_entry.textChanged.connect(self.on_search)
        
        filter_btn = QPushButton("Refresh ↻")
        filter_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        filter_btn.clicked.connect(self.load_data)
        
        search_layout.addWidget(self.search_entry, stretch=4)
        search_layout.addSpacing(10)
        search_layout.addWidget(filter_btn, stretch=0)
        
        self.main_layout.addLayout(search_layout)

    def create_table_structure(self, columns):
        self.table = QTableWidget()
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 80) # Action column width
        
        self.table.cellClicked.connect(self.on_cell_click)
        self.main_layout.addWidget(self.table)

    def load_data(self):
        """Mengambil data real dari database via AuthService"""
        self.table.setRowCount(0) # Bersihkan tabel
        self.full_data = []

        if not self.auth_service:
            return # Atau tampilkan dummy jika backend mati

        try:
            # Menggunakan method yang sudah ada di auth_service (get_all_penghuni)
            data_penghuni = self.auth_service.get_all_penghuni()
            self.full_data = data_penghuni # Simpan untuk referensi
            
            self.table.setRowCount(len(data_penghuni))
            
            for row, item in enumerate(data_penghuni):
                # 1. Nomor Kamar
                kamar = item.get('nomor_kamar') if item.get('nomor_kamar') else "-"
                self._set_item(row, 0, kamar)
                
                # 2. Username
                self._set_item(row, 1, item['username'])
                
                # 3. Nama Lengkap
                self._set_item(row, 2, item['nama'])
                
                # 4. Harga Kamar
                harga = item.get('harga_kamar', 0)
                harga_fmt = f"Rp. {harga:,}".replace(",", ".") if harga else "-"
                self._set_item(row, 3, harga_fmt)
                
                # 5. Status Akun
                status_raw = item.get('statusAkun') # Bisa statusAkun atau status_akun tergantung DB
                if status_raw is None: status_raw = item.get('status_akun')
                
                status_text = "Aktif"
                try:
                    if str(status_raw) in ['0', 'False', 'Non-Aktif']:
                        status_text = "Nonaktif"
                except: pass
                
                self._set_item(row, 4, status_text)
                
                # 6. Action Icon
                action_item = QTableWidgetItem("📝")
                action_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                action_item.setFont(QFont("Segoe UI", 12))
                self.table.setItem(row, 5, action_item)

        except Exception as e:
            print(f"Error Loading Dashboard: {e}")

    def _set_item(self, row, col, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, col, item)

    def on_search(self):
        search_text = self.search_entry.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount() - 1):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def on_cell_click(self, row, column):
        if column == 5: # Kolom Action
            self.show_action_menu(QCursor.pos(), row)

    def show_action_menu(self, global_pos, row):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: white; border: 1px solid #E0E0E0; } QMenu::item { padding: 8px 24px; }")
        
        view_action = menu.addAction("👁️  Lihat Detail")
        # edit_action = menu.addAction("✏️  Edit")
        
        action = menu.exec(global_pos)
        
        if action == view_action:
            self.view_selected(row)

    def view_selected(self, row):
        if row >= len(self.full_data): return
        data = self.full_data[row]
        
        status = "Aktif" if str(data.get('statusAkun', 1)) == '1' else "Nonaktif"
        
        details = f"""
        <b>Detail Penghuni:</b><br><br>
        <table>
        <tr><td>Nomor Kamar</td><td>: {data.get('nomor_kamar', '-')}</td></tr>
        <tr><td>Nama Lengkap</td><td>: {data['nama']}</td></tr>
        <tr><td>Username</td><td>: {data['username']}</td></tr>
        <tr><td>No. Telepon</td><td>: {data.get('nomor_telepon', '-')}</td></tr>
        <tr><td>Harga Kamar</td><td>: Rp {data.get('harga_kamar', 0):,}</td></tr>
        <tr><td>Status Akun</td><td>: {status}</td></tr>
        </table>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Detail Penghuni")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(details)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

# Test standalone
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = DashboardPenghuni()
    window.show()
    sys.exit(app.exec())