"""
Feedback Penghuni page for AnaKosware application - PyQt6 Version
Style: Modern, Minimalist, Consistent with Dashboard.
Integration: Connected to FeedbackService (Backend).
"""
import html
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView, QFrame, QMessageBox, 
    QGraphicsDropShadowEffect, QDialog, QDateEdit, QDialogButtonBox, QCheckBox
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

from datetime import datetime, date

class FilterDialog(QDialog):
    """Dialog sederhana untuk filter feedback berdasarkan nama & rentang tanggal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filter Feedback")
        self.setFixedSize(400, 260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Filter nama penghuni
        lbl_nama = QLabel("Nama penghuni (opsional):")
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("mis. 'halo'")

        layout.addWidget(lbl_nama)
        layout.addWidget(self.nama_input)

        # Checkbox untuk mengaktifkan filter tanggal
        self.chk_tanggal = QCheckBox("Filter berdasarkan rentang tanggal")
        self.chk_tanggal.setChecked(False)
        layout.addWidget(self.chk_tanggal)

        # Rentang tanggal
        row_tgl = QHBoxLayout()
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(self.date_from.date().currentDate())

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(self.date_to.date().currentDate())

        row_tgl.addWidget(QLabel("Dari:"))
        row_tgl.addWidget(self.date_from)
        row_tgl.addWidget(QLabel("Sampai:"))
        row_tgl.addWidget(self.date_to)
        layout.addLayout(row_tgl)

        # Tombol OK / Reset / Cancel
        btn_box = QDialogButtonBox()
        btn_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Reset
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        btn_box.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(self.reset_fields)

        layout.addWidget(btn_box)

    def reset_fields(self):
        self.nama_input.clear()
        self.chk_tanggal.setChecked(False)

    def get_values(self):
        """Return dict kriteria filter."""
        nama = self.nama_input.text().strip()
        use_date = self.chk_tanggal.isChecked()
        if use_date:
            d_from = self.date_from.date().toPyDate()
            d_to = self.date_to.date().toPyDate()
        else:
            d_from = None
            d_to = None
        return {
            "nama": nama,
            "use_date": use_date,
            "date_from": d_from,
            "date_to": d_to,
        }

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
        columns = ["Tanggal", "Penghuni", "Pesan Feedback", "Action"]
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
        filter_btn.clicked.connect(self.open_filter_dialog)
        
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
        self.table.setColumnWidth(3, 80)  # Action

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
            # format: [Tanggal, Penghuni, Pesan, ActionPlaceholder]
            self.data = [
                ["04/17/23", "Dummy User", "Backend tidak terhubung.", ""],
            ]
            self.all_data = list(self.data)
            self.populate_table(self.data)
            return

        try:
            response = self.feedback_service.get_all_feedbacks()
            
            if response["status"] == "success":
                db_data = response["data"]
                self.data = []
                
                # Transform data dari Dict (Backend) ke List (Frontend)
                for item in db_data:
                    row = [
                        item['tanggal'],   # Tanggal sudah diformat di backend
                        item['penghuni'],  # Nama penghuni
                        item['isi'],       # Isi Feedback
                        ""                 # Placeholder action
                    ]
                    self.data.append(row)
                
                # simpan full data untuk kebutuhan filter
                self.all_data = list(self.data)
                self.populate_table(self.data)
            else:
                QMessageBox.warning(self, "Info", response["message"])
                
        except Exception as e:
            print(f"Error loading data: {e}")
            QMessageBox.critical(self, "Error", "Gagal memuat data feedback.")

    def populate_table(self, data):
        """Mengisi data ke tabel"""
        self.table.setRowCount(0) 
        self.table.setRowCount(len(data))
        
        for i, row_data in enumerate(data):
            # Tanggal (col 0)
            item_date = QTableWidgetItem(str(row_data[0]))
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, item_date)
            
            # Penghuni (col 1)
            self.table.setItem(i, 1, QTableWidgetItem(str(row_data[1])))
            
            # Pesan (col 2)
            self.table.setItem(i, 2, QTableWidgetItem(str(row_data[2])))
            
            # Action (col 3)
            item_action = QTableWidgetItem("📝")
            item_action.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            action_font = QFont()
            action_font.setPointSize(12)
            item_action.setFont(action_font)
            self.table.setItem(i, 3, item_action)
            
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
        # Kolom 3 adalah kolom Action
        if col == 3:
            self.view_feedback(row)

    def view_feedback(self, row):
        """Menampilkan detail feedback"""
        try:
            tanggal = self.table.item(row, 0).text()
            penghuni = self.table.item(row, 1).text()
            pesan = self.table.item(row, 2).text()

            # Escape supaya tanda < > dll tidak bikin HTML rusak
            safe_pesan = html.escape(pesan)

            details = f"""
            <b>Detail Feedback</b><br><br>
            <table>
            <tr><td><b>Tanggal</b></td><td>: {tanggal}</td></tr>
            <tr><td><b>Penghuni</b></td><td>: {penghuni}</td></tr>
            </table>
            <br>
            <b>Pesan:</b><br>
            <div style='background-color:#F5F5F5;
                        color:#111111;
                        padding:10px;
                        border-radius:5px;
                        white-space:pre-wrap;'>
                {safe_pesan}
            </div>
            """

            msg = QMessageBox(self)
            msg.setWindowTitle("View Feedback")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(details)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
        except Exception:
            pass

    def open_filter_dialog(self):
        """Buka dialog filter dan terapkan hasilnya."""
        self.load_data()
        if not hasattr(self, "all_data"):
            self.all_data = list(self.data) if hasattr(self, "data") else []

        dlg = FilterDialog(self)
        if dlg.exec():  # OK ditekan
            criteria = dlg.get_values()
            self.apply_filter(criteria)

    def apply_filter(self, criteria: dict):
        """Terapkan filter ke self.all_data lalu tampilkan di tabel."""
        if not hasattr(self, "all_data"):
            self.all_data = list(self.data)

        nama_key = criteria.get("nama", "").lower()
        use_date = criteria.get("use_date", False)
        d_from: date | None = criteria.get("date_from")
        d_to: date | None = criteria.get("date_to")

        filtered = []

        for row in self.all_data:
            tgl_str, penghuni, pesan, _ = row

            # 1. Filter nama penghuni (contains)
            if nama_key and nama_key not in str(penghuni).lower():
                continue

            # 2. Filter rentang tanggal (kalau diaktifkan)
            if use_date:
                tgl_obj = self._parse_date_safely(tgl_str)
                if tgl_obj is None:
                    # Kalau gagal parse, anggap tidak lolos
                    continue
                if d_from and tgl_obj < d_from:
                    continue
                if d_to and tgl_obj > d_to:
                    continue

            filtered.append(row)

        # Simpan & tampilkan
        self.data = filtered
        self.populate_table(self.data)

    def _parse_date_safely(self, date_str: str):
        """Coba parse string tanggal ke date() dengan beberapa format umum."""
        if not date_str:
            return None
        for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None

# --- Test Standalone ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = FeedbackPenghuni()
    window.resize(1000, 600)
    window.show()
    
    sys.exit(app.exec())