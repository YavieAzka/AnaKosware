"""
Feedback Penghuni page for AnaKosware application - PyQt6 Version
Style: Modern, Minimalist, Consistent with Dashboard.
Integration: Connected to FeedbackService (Backend).
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView, QFrame, QMessageBox, 
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QCursor

# --- IMPORT BACKEND ---
try:
    # Asumsi file backend disimpan di database/feedback.py
    from feedback.feedback import FeedbackService
except ImportError:
    print("Warning: Backend FeedbackService not found. Using Dummy Data.")
    FeedbackService = None

class FeedbackPenghuni(QWidget):
    """Halaman untuk menampilkan feedback penghuni"""
    
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        # --- INISIALISASI SERVICE ---
        if FeedbackService:
            self.feedback_service = FeedbackService()
        else:
            self.feedback_service = None

        # Setup Basic Properties
        self.setObjectName("FeedbackPage")
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
            QWidget#FeedbackPage {
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
                background-color: #E8D5A8; /* Kuning Krem */
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
        """Membuat konten halaman Feedback Penghuni"""
        
        # 1. Judul Halaman
        title = QLabel("Record Feedback Penghuni")
        title.setObjectName("PageTitle")
        self.main_layout.addWidget(title)
        
        # 2. Search & Filter Section
        self.create_search_filter()
        
        # 3. Table Section
        columns = ["Tanggal", "Penghuni", "Pesan Feedback", "Rating", "Action"]
        self.create_table(columns)
        
        # 4. LOAD DATA DARI BACKEND
        self.load_data()
        
        # Spacer di bawah agar rapi
        self.main_layout.addStretch()

    def create_search_filter(self):
        """Membuat bar pencarian dan tombol filter"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 10) # Margin bawah
        layout.setSpacing(15)
        
        # Search Input
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("🔍 Search feedback...")
        self.search_entry.setMinimumWidth(300)
        self.search_entry.textChanged.connect(self.on_search) # Live search logic
        
        # Filter Button
        filter_btn = QPushButton("Filter ☰")
        filter_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        filter_btn.clicked.connect(self.show_filter)
        
        # Add to layout
        layout.addWidget(self.search_entry)
        layout.addStretch() # Spacer tengah
        layout.addWidget(filter_btn)
        
        self.main_layout.addWidget(container)

    def create_table(self, columns):
        """Membuat struktur tabel feedback"""
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
        self.table.setMinimumHeight(400) # Tinggi minimum tabel

        # Header Config
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Kolom Pesan stretch
        
        # Set Initial Column Widths
        self.table.setColumnWidth(0, 150) # Tanggal
        self.table.setColumnWidth(1, 200) # Penghuni
        self.table.setColumnWidth(3, 80)  # Rating
        self.table.setColumnWidth(4, 80)  # Action

        # Connect Signals
        self.table.cellClicked.connect(self.on_cell_click)
        
        # Add shadow to table container effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.table.setGraphicsEffect(shadow)

        self.main_layout.addWidget(self.table)

    def load_data(self):
        """Mengambil data dari database menggunakan FeedbackService"""
        if not self.feedback_service:
            # Fallback jika backend belum siap (Dummy Data)
            self.data = [
                ["04/17/23", "Dummy User", "Backend tidak terhubung.", "★", ""],
            ]
            self.populate_table(self.data)
            return

        try:
            response = self.feedback_service.get_all_feedbacks()
            
            if response["status"] == "success":
                db_data = response["data"]
                self.data = []
                
                # Transform data dari Dict (Backend) ke List (Frontend)
                for item in db_data:
                    # Format baris: [Tanggal, Penghuni, Isi, Rating, ActionPlaceholder]
                    row = [
                        item['tanggal'],   # Tanggal sudah diformat di backend
                        item['penghuni'],  # Nama penghuni
                        item['isi'],       # Isi Feedback
                        "-",               # Rating (Default '-' karena tidak ada di DB)
                        ""                 # Placeholder action
                    ]
                    self.data.append(row)
                
                self.populate_table(self.data)
            else:
                QMessageBox.warning(self, "Info", response["message"])
                
        except Exception as e:
            print(f"Error loading data: {e}")
            QMessageBox.critical(self, "Error", "Gagal memuat data feedback.")

    def populate_table(self, data):
        """Mengisi data ke tabel"""
        self.table.setRowCount(0) # Reset tabel
        self.table.setRowCount(len(data))
        
        for i, row_data in enumerate(data):
            # Tanggal
            item_date = QTableWidgetItem(str(row_data[0]))
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, item_date)
            
            # Penghuni
            self.table.setItem(i, 1, QTableWidgetItem(str(row_data[1])))
            
            # Pesan
            self.table.setItem(i, 2, QTableWidgetItem(str(row_data[2])))
            
            # Rating
            # Karena DB tidak punya rating, kita tampilkan '-' atau bintang jika dummy
            rating_text = str(row_data[3])
            item_rating = QTableWidgetItem(rating_text)
            item_rating.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            if "★" in rating_text:
                item_rating.setForeground(QColor("#FFB400")) # Warna Emas
                font = QFont()
                font.setPointSize(14)
                item_rating.setFont(font)
            
            self.table.setItem(i, 3, item_rating)
            
            # Action Icon
            item_action = QTableWidgetItem("📝")
            item_action.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            action_font = QFont()
            action_font.setPointSize(12)
            item_action.setFont(action_font)
            self.table.setItem(i, 4, item_action)
            
            # Set row height
            self.table.setRowHeight(i, 50)

    def on_search(self):
        """Logic pencarian"""
        search_text = self.search_entry.text().lower()
        
        for row in range(self.table.rowCount()):
            match = False
            # Cek kolom Penghuni (1) dan Pesan (2)
            item_penghuni = self.table.item(row, 1)
            item_pesan = self.table.item(row, 2)
            
            if (item_penghuni and search_text in item_penghuni.text().lower()) or \
               (item_pesan and search_text in item_pesan.text().lower()):
                match = True
            
            self.table.setRowHidden(row, not match)

    def show_filter(self):
        # Refresh data saat tombol filter diklik (sebagai pengganti filter kompleks sementara)
        self.load_data() 
        QMessageBox.information(self, "Reload", "Data feedback diperbarui dari database.")

    def on_cell_click(self, row, col):
        """Handle klik pada tabel (khususnya kolom Action)"""
        # Kolom 4 adalah kolom Action
        if col == 4:
            self.view_feedback(row)

    def view_feedback(self, row):
        """Menampilkan detail feedback"""
        # Ambil data dari baris tersebut
        try:
            tanggal = self.table.item(row, 0).text()
            penghuni = self.table.item(row, 1).text()
            pesan = self.table.item(row, 2).text()
            
            details = f"""
            <b>Detail Feedback</b><br><br>
            <table>
            <tr><td><b>Tanggal</b></td><td>: {tanggal}</td></tr>
            <tr><td><b>Penghuni</b></td><td>: {penghuni}</td></tr>
            </table>
            <br>
            <b>Pesan:</b><br>
            <p style='background-color:#F5F5F5; padding:10px; border-radius:5px;'>{pesan}</p>
            """
            
            msg = QMessageBox(self)
            msg.setWindowTitle("View Feedback")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(details)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
        except Exception:
            pass

# --- Test Standalone ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = FeedbackPenghuni()
    window.resize(1000, 600)
    window.show()
    
    sys.exit(app.exec())