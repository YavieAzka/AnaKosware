"""
Dashboard Penghuni untuk AnaKosware application (PyQt6 Refactor).
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView, QFrame, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QColor, QCursor

class DashboardPenghuni(QWidget):
    """Dashboard untuk menampilkan daftar penghuni"""
    
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.table = None
        
        # Setup Basic Window Properties untuk standalone test
        if parent is None:
            self.setWindowTitle("Dashboard Penghuni")
            self.resize(1200, 800)
            
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)
        
        # Stylesheet (CSS) untuk tampilan Modern Minimalis
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #2D3142;
            }
            QLabel#PageTitle {
                font-size: 24px;
                font-weight: bold;
                color: #2D3142;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: #F8F9FA;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
                background-color: white;
            }
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
                border-color: #D0D0D0;
            }
            QTableWidget {
                border: 1px solid #E0E0E0;
                gridline-color: #F0F0F0;
                selection-background-color: #E8F0FE;
                selection-color: #2D3142;
                outline: 0;
            }
            QHeaderView::section {
                background-color: #E8D5A8;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #333333;
            }
        """)

        self.create_content()

    def create_content(self):
        """Create page content"""
        print("Membuat konten Dashboard (PyQt6)...")

        # 1. Page Title
        title_label = QLabel("Dashboard Penghuni")
        title_label.setObjectName("PageTitle")
        self.main_layout.addWidget(title_label)

        # 2. Search and Filter Frame
        self.create_search_filter()

        print("Membuat tabel penghuni...")
        
        # 3. Table
        # Example data consistent with original
        self.data = [
            ["A01", "user_ben", "Benjamin Franklin", "04/17/23", "Rp. 1.000.000", "Aktif"],
            ["A01", "user_john", "John Doe", "04/18/23", "Rp. 950.000", "Aktif"],
            ["A02", "user_alice", "Alice Johnson", "04/15/23", "Rp. 1.050.000", "Nonaktif"],
            ["A03", "user_bob", "Bob Smith", "04/10/23", "Rp. 1.100.000", "Aktif"],
            ["A04", "user_carol", "Carol White", "04/12/23", "Rp. 980.000", "Nonaktif"],
        ]
        
        columns = ["Nomor Kamar", "Username", "Nama Lengkap", "Tanggal Masuk", "Harga Kamar", "Status Akun", "Action"]
        self.create_table(columns, self.data)
        
        print("Dashboard berhasil dibuat!")

    def create_search_filter(self):
        """Create search bar and filter button"""
        search_layout = QHBoxLayout()
        
        # Search Container (Search Bar)
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("🔍 Search penghuni...")
        self.search_entry.textChanged.connect(self.on_search) # Live search
        
        # Filter Button
        filter_btn = QPushButton("Filter ☰")
        filter_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        filter_btn.clicked.connect(self.show_filter)
        
        # Add to layout
        search_layout.addWidget(self.search_entry, stretch=4) # Entry takes more space
        search_layout.addSpacing(10)
        search_layout.addWidget(filter_btn, stretch=0)
        
        self.main_layout.addLayout(search_layout)

    def on_search(self):
        """Filter table based on search"""
        search_text = self.search_entry.text().lower()
        
        # PyQt logic: Iterate rows and hide/show based on match
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount() - 1): # Skip Action col
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def show_filter(self):
        """Show filter options"""
        QMessageBox.information(self, "Filter", "Filter options coming soon!")

    def create_table(self, columns, data):
        """Create table to show tenant data with proper styling"""
        self.table = QTableWidget()
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # Table Properties
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False) # Hide row numbers
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # Read only
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # Select full row
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus) # Remove dotted line on focus

        # Header Properties
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Room no
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed) # Action column fixed width
        self.table.setColumnWidth(6, 80)
        
        # Populate Data
        self.populate_table(data)

        # Signals
        self.table.cellClicked.connect(self.on_cell_click)
        self.table.doubleClicked.connect(self.view_selected)

        self.main_layout.addWidget(self.table)

    def populate_table(self, data):
        """Helper to insert data"""
        self.table.setRowCount(len(data))
        for i, row_data in enumerate(data):
            # Insert data columns
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, j, item)
            
            # Insert Action icon
            action_item = QTableWidgetItem("📝")
            action_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Make it distinct font/color if needed
            font = QFont()
            font.setPointSize(12)
            action_item.setFont(font)
            self.table.setItem(i, 6, action_item)

    def on_cell_click(self, row, column):
        """Handle click on table row"""
        # Check if clicked on Action column (last column, index 6)
        if column == 6:
            # Get global cursor position for popup
            cursor_pos = QCursor.pos()
            self.show_action_menu(cursor_pos)

    def show_action_menu(self, global_pos):
        """Show action menu"""
        menu = QMenu(self)
        
        # Style the menu to match
        menu.setStyleSheet("""
            QMenu { background-color: white; border: 1px solid #E0E0E0; }
            QMenu::item { padding: 8px 24px; }
            QMenu::item:selected { background-color: #F5F5F5; color: black; }
        """)

        view_action = menu.addAction("👁️  View Detail")
        edit_action = menu.addAction("✏️   Edit")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️  Delete")

        # Execute menu and handle selection
        action = menu.exec(global_pos)
        
        if action == view_action:
            self.view_selected()
        elif action == edit_action:
            self.edit_selected()
        elif action == delete_action:
            self.delete_selected()

    def get_selected_row_data(self):
        """Helper to get data list from selected row"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None
        
        current_row = self.table.currentRow()
        row_data = []
        # Collect data only (exclude action column)
        for col in range(self.table.columnCount() - 1):
            item = self.table.item(current_row, col)
            row_data.append(item.text())
        return row_data

    def view_selected(self):
        """View selected tenant details"""
        values = self.get_selected_row_data()
        if not values:
            QMessageBox.warning(self, "Peringatan", "Pilih penghuni yang ingin dilihat!")
            return

        details = f"""
        Detail Penghuni:

        Nomor Kamar    : {values[0]}
        Username       : {values[1]}
        Nama Lengkap   : {values[2]}
        Tanggal Masuk  : {values[3]}
        Harga Kamar    : {values[4]}
        Status Akun    : {values[5]}
        """
        QMessageBox.information(self, "Detail Penghuni", details)

    def edit_selected(self):
        """Edit selected tenant"""
        values = self.get_selected_row_data()
        if not values:
            QMessageBox.warning(self, "Peringatan", "Pilih penghuni yang ingin diedit!")
            return

        QMessageBox.information(self, "Edit", f"Edit penghuni: {values[2]}\n(Fitur coming soon)")

    def delete_selected(self):
        """Delete selected tenant"""
        values = self.get_selected_row_data()
        if not values:
            QMessageBox.warning(self, "Peringatan", "Pilih penghuni yang ingin dihapus!")
            return

        response = QMessageBox.question(
            self, 
            "Konfirmasi Hapus", 
            f"Apakah Anda yakin ingin menghapus penghuni:\n{values[2]}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if response == QMessageBox.StandardButton.Yes:
            current_row = self.table.currentRow()
            self.table.removeRow(current_row)
            QMessageBox.information(self, "Sukses", "Penghuni berhasil dihapus!")

# Test standalone
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set default font for application
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = DashboardPenghuni()
    window.show()
    
    sys.exit(app.exec())