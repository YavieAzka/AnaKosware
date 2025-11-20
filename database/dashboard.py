# ui_dashboard.py
# Implementasi PyQt6 untuk Antarmuka I-02: Dashboard Penghuni
print("SCRIPT START")
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLineEdit, QComboBox, QTableWidget, 
    QTableWidgetItem, QHeaderView, QPushButton, QStackedWidget
)
from PyQt6.QtCore import Qt

from db_manager import DatabaseManager

# Impor controller logika kita
try:
    from .logic_controller import LogicController
except ImportError:
    from logic_controller import LogicController
print("IMPORTS COMPLETE")

class DashboardPenghuni(QMainWindow):
    """
    Kelas ini merepresentasikan Antarmuka I-02 (Dashboard Penghuni).
    """
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("AnaKosware App - Dashboard Pemilik")
        self.setGeometry(100, 100, 1000, 600)
        
        # --- Di sini kita bisa terapkan Navigasi Bar ---
        # Untuk saat ini, kita fokus pada konten dashboard
        # Kita akan menggunakan QStackedWidget nanti untuk menukar halaman
        
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 1. Bar Pencarian dan Filter 
        filter_bar_layout = QHBoxLayout()
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search penghuni (username, nama, nomor kamar)...")
        # Hubungkan sinyal textChanged ke slot self.load_data
        self.search_bar.textChanged.connect(self.load_data)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Semua Status", userData=None)
        self.filter_combo.addItem("Aktif", userData=True)
        self.filter_combo.addItem("Nonaktif", userData=False)
        # Hubungkan sinyal currentIndexChanged ke slot self.load_data
        self.filter_combo.currentIndexChanged.connect(self.load_data)
        
        filter_bar_layout.addWidget(self.search_bar, 3) # Search bar 3x lebih besar
        filter_bar_layout.addWidget(self.filter_combo, 1) # Filter 1x
        
        main_layout.addLayout(filter_bar_layout)
        
        # 2. Tabel Data Penghuni 
        self.table_widget = QTableWidget()
        
        # Tentukan kolom sesuai Antarmuka I-02
        self.column_names = [
            "Nomor Kamar", "Username", "Nama Lengkap", 
            "Tanggal Masuk", "Harga Kamar", "Status Akun", "Action"
        ]
        self.table_widget.setColumnCount(len(self.column_names))
        self.table_widget.setHorizontalHeaderLabels(self.column_names)
        
        # Atur agar tabel mengisi ruang
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        main_layout.addWidget(self.table_widget)
        
        self.setCentralWidget(main_widget)
        
        # Muat data saat pertama kali dibuka
        self.load_data()

    def load_data(self):
        """
        Slot ini dipanggil setiap kali search/filter berubah.
        Ini memanggil controller untuk data baru dan mempopulasi tabel.
        (Ref: UC08 Sequence Diagram [cite: 243])
        """
        # 1. Dapatkan nilai dari UI
        search_keyword = self.search_bar.text()
        status_filter = self.filter_combo.currentData() # Akan berisi None, True, atau False
        
        # 2. Panggil Logic Controller
        try:
            data = self.controller.get_dashboard_penghuni(search_keyword, status_filter)
        except Exception as e:
            print(f"Error saat memanggil controller: {e}")
            data = []
            
        # 3. Populasi Tabel
        self.populate_table(data)

    def populate_table(self, data):
        """Helper untuk mengisi QTableWidget dengan data."""
        self.table_widget.setRowCount(0) # Kosongkan tabel
        
        if not data:
            return

        self.table_widget.setRowCount(len(data))
        
        for row_index, row_data in enumerate(data):
            # ["Nomor Kamar", "Username", "Nama Lengkap", "Tanggal Masuk", "Harga Kamar", "Status Akun", "Action"]
            
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(row_data['nomor_kamar']))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(row_data['username']))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(row_data['nama_lengkap']))
            
            # Format tanggal dan harga
            tgl_masuk = str(row_data['tanggal_masuk']) if row_data['tanggal_masuk'] else "N/A"
            harga_kamar = f"Rp {row_data['harga_kamar']:,}" if row_data['harga_kamar'] else "N/A"
            
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(tgl_masuk))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(harga_kamar))
            
            # Status Akun (dari 'status_teks' yang kita buat di controller)
            status_item = QTableWidgetItem(row_data['status_teks'])
            if row_data['status_teks'] == "Aktif":
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.table_widget.setItem(row_index, 5, status_item)

            # 7. Action Buttons (Placeholder)
            # Di implementasi nyata, ini akan terhubung ke UC03 (Nonaktifkan)
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            btn_view = QPushButton("View")
            btn_edit = QPushButton("Edit") # (Ref: UC03)
            
            action_layout.addWidget(btn_view)
            action_layout.addWidget(btn_edit)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.table_widget.setCellWidget(row_index, 6, action_widget)

if __name__ == "__main__":
    print("MAIN: SCRIPT START")
    db_manager = DatabaseManager(password='kulintang8') # Ganti password

    if db_manager.connection:
        # Contoh SELECT
        print("\nTesting SELECT (User):")
        users = db_manager.execute_query("SELECT username, nama FROM user LIMIT 5")
        if users:
            for user in users:
                print(f"- Username: {user['username']}, Nama: {user['nama']}")
    app = QApplication(sys.argv)
    print("MAIN: QApplication dibuat.")
    

    main_controller = LogicController()
    print("MAIN: LogicController dibuat.")
    
    window = DashboardPenghuni(controller=main_controller)
    print("MAIN: Window DashboardPenghuni dibuat.")
    
    window.show()
    print("MAIN: window.show() dipanggil.")
    
    sys.exit(app.exec())

    print("MAIN: app.exec() selesai.")