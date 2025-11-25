import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QDialog, QLabel, QComboBox,
    QLineEdit, QFrame, QHeaderView, QAbstractItemView, QMessageBox,
    QSizePolicy, QGridLayout, QScrollArea
)
from PyQt6.QtGui import QFont, QCursor, QColor
from PyQt6.QtCore import Qt, QSize, QPoint


# --- Gaya Global (Stylesheet) ---
STYLE_SHEET = """
QWidget {
    /* Mengadopsi style dari Dashboard Penghuni */
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2D3142; /* Warna teks utama */
    background-color: white; 
}

/* Header dan Judul */
QLabel#PageTitle {
    font-size: 24px; /* Lebih besar dari sebelumnya (24px) */
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 25px; /* Tambahkan ruang di bawah judul */
    color: #2D3142;
}

/* Container Frame (Membungkus Search, Filter, dan Tabel) - mempertahankan border */
QFrame#ContentFrame {
    border: 1px solid #E0E0E0; /* Border abu-abu muda */
    border-radius: 10px; /* Sudut membulat */
    background-color: #FFFFFF;
}

/* Kotak Pencarian (Dibuat memanjang) */
QLineEdit {
    padding: 10px; /* Menyesuaikan padding dari contoh */
    border: 1px solid #E0E0E0; /* Menggunakan warna border dari contoh */
    border-radius: 8px;
    background-color: #F8F9FA; /* Background abu-abu muda */
    min-height: 35px;
    font-size: 14px;
}
QLineEdit:focus {
    border: 1px solid #4A90E2; /* Warna border focus dari contoh */
    background-color: white;
}

/* Tabel */
QTableWidget {
    background-color: white;
    border: none; /* Hapus border tabel karena sudah ada di QFrame#ContentFrame */
    gridline-color: #F0F0F0;
    selection-background-color: #E8F0FE; /* Warna selection yang lebih modern */
    selection-color: #2D3142;
    outline: 0; /* Hapus outline fokus */
}

QHeaderView::section {
    /* Mengadopsi warna header dari contoh */
    background-color: #E8D5A8; 
    color: #333333;
    padding: 12px; /* Padding yang lebih besar */
    border: none;
    font-weight: bold;
}

/* Tombol Action */
QPushButton.ActionBtn {
    /* Tombol Action di tabel (seperti ikon pensil) tidak berborder */
    padding: 0; 
    border: none;
    background: none;
    cursor: pointer;
    font-size: 12pt;
    font-family: Arial, sans-serif;
    color: #4A90E2; /* Warna ikon agar terlihat seperti link/action */
    width: 30px;
    height: 30px;
}

/* Tombol Filter */
QPushButton#FilterButton {
    padding: 8px 16px;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    background-color: white;
    font-weight: 600;
}
QPushButton#FilterButton:hover {
    background-color: #F0F0F0;
    border-color: #D0D0D0;
}

/* Status Labels */
QLabel.StatusLabel {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 9pt;
    font-weight: bold;
    min-width: 70px;
    text-align: center;
}
"""


class StatusLabel(QLabel):
    """Widget kustom untuk label status berwarna (Done, In Progress, Waiting)."""
    def __init__(self, status):
        super().__init__(status)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("StatusLabel")

        # Logika warna status
        if status == 'Done' or status == 'Completed':
            self.setStyleSheet("QLabel {background-color: #C6E2C6; color: #1E8449;}") # Hijau
        elif status == 'In Progress':
            self.setStyleSheet("QLabel {background-color: #FFECB3; color: #FFA500;}") # Kuning/Oranye
        elif status == 'Waiting' or status == 'Pending':
            self.setStyleSheet("QLabel {background-color: #E8D5A8; color: #505050;}") # Coklat Muda (Mirip warna header baru)
        
        self.setProperty("class", "StatusLabel")
        self.setFixedSize(QSize(90, 24))


class DashboardPenjaga(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dashboard Pesanan Penghuni')
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(STYLE_SHEET)

        # Layout utama (Vertikal)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40) # Margins lebih besar (diadopsi dari contoh)
        main_layout.setSpacing(20) 

        # --- Judul Halaman ---
        page_title = QLabel("Dashboard Pesanan Penghuni")
        page_title.setObjectName("PageTitle")
        main_layout.addWidget(page_title)

        # --- Container Frame untuk semua elemen Dashboard (kecuali judul) ---
        content_frame = QFrame(self)
        content_frame.setObjectName("ContentFrame")
        
        # Layout di dalam frame
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # 1. Search & Filter
        search_filter_layout = QHBoxLayout()
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Search pesanan...")
        search_input.textChanged.connect(self.on_search) # Tambahkan fungsi search
        search_filter_layout.addWidget(search_input, stretch=4) # Search memanjang

        # Tombol Filter
        filter_button = QPushButton("Filter ☰")
        filter_button.setObjectName("FilterButton")
        filter_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        filter_button.clicked.connect(self.show_filter)
        
        search_filter_layout.addSpacing(10)
        search_filter_layout.addWidget(filter_button, stretch=0)

        content_layout.addLayout(search_filter_layout)

        # 2. Tabel Pesanan
        self.data = self._get_dummy_data()
        self.table = self._create_table()
        content_layout.addWidget(self.table)
        
        # Menambahkan frame ke layout utama
        main_layout.addWidget(content_frame)
        
        self.setLayout(main_layout)

    def _get_dummy_data(self):
        """Mendapatkan data contoh pesanan."""
        return [
            ['A01', 'A01', 'Benjamin Franklin', '04/17/23', 'Rp20.000', 'In Progress'],
            ['A01', 'A01', 'Benjamin Franklin', '04/17/23', 'Rp5.000', 'Done'],
            ['A01', 'A01', 'Benjamin Franklin', '04/17/23', 'Rp20.000', 'In Progress'],
            ['A02', 'A02', 'Albert Einstein', '04/15/23', 'Rp30.000', 'Done'],
            ['A03', 'A03', 'Marie Curie', '04/10/23', 'Rp25.000', 'Waiting'],
            ['A04', 'A04', 'Isaac Newton', '04/20/23', 'Rp15.000', 'Done'],
            ['A05', 'A05', 'Charles Darwin', '04/18/23', 'Rp18.000', 'Done'],
            ['A06', 'A06', 'Nikola Tesla', '04/16/23', 'Rp10.000', 'Waiting'], # Ganti 'Pending' jadi 'Waiting'
            ['A07', 'A07', 'Galileo Galilei', '04/19/23', 'Rp22.000', 'Done'],
            ['A08', 'A08', 'Ada Lovelace', '04/21/23', 'Rp16.000', 'Waiting'],
        ]

    def _create_table(self):
        """Membuat dan mengisi QTableWidget dengan gaya baru."""
        table = QTableWidget(self)
        
        # Mengatur kolom
        headers = ['Nomor Kamar', 'Username', 'Nama Lengkap', 'Tanggal Pesan', 'Total Harga', 'Status', 'Action']
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        table.setRowCount(len(self.data))
        table.verticalHeader().setVisible(False) # Sembunyikan header vertikal
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # Read only
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Atur lebar kolom
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Kolom Kamar
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Kolom Harga
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Kolom Status
        
        # Set lebar kolom Action menjadi Fixed 80px
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed) 
        table.setColumnWidth(6, 80) 

        for row, rowData in enumerate(self.data):
            for column, value in enumerate(rowData):
                if column == 5: # Kolom Status (indeks 5)
                    status_widget = StatusLabel(value)
                    
                    container = QWidget()
                    h_layout = QHBoxLayout(container)
                    h_layout.addWidget(status_widget)
                    h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    h_layout.setContentsMargins(0, 0, 0, 0)
                    table.setCellWidget(row, column, container)
                else:
                    item = QTableWidgetItem(value)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable) 
                    
                    # Rata tengah untuk Nomor Kamar dan Total Harga
                    if column in [0, 4]:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    table.setItem(row, column, item)

            # Menambahkan tombol Action di setiap baris (sebagai widget)
            action_btn = QPushButton('📝')
            action_btn.setProperty("class", "ActionBtn")
            action_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # Menghubungkan tombol ke metode open_popup dengan lambda
            action_btn.clicked.connect(lambda _, r=row: self.open_popup(r)) 
            
            # Memastikan tombol rata tengah di sel
            container = QWidget()
            h_layout = QHBoxLayout(container)
            h_layout.addWidget(action_btn)
            h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h_layout.setContentsMargins(0, 0, 0, 0)

            table.setCellWidget(row, 6, container) 
            
        return table
    
    def on_search(self):
        """Filter table based on search input."""
        search_entry = self.findChild(QLineEdit)
        if not search_entry: return
        
        search_text = search_entry.text().lower()
        
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount() - 1): # Skip Action col
                item = self.table.item(row, col)
                # Check status label text instead of item for column 5
                if col == 5:
                    status_widget = self.table.cellWidget(row, col)
                    status_label = status_widget.findChild(QLabel) if status_widget else None
                    if status_label and search_text in status_label.text().lower():
                        match = True
                        break
                elif item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def show_filter(self):
        """Show filter options."""
        QMessageBox.information(self, "Filter", "Fitur filter pesanan akan ditambahkan di sini.")
        
    def get_row_data(self, row):
        """Helper to get data list from a specific row."""
        if row < 0 or row >= self.table.rowCount():
            return None
        
        row_data = []
        # Collect data only (exclude action column)
        for col in range(self.table.columnCount() - 1):
            if col == 5: # Status column
                 widget = self.table.cellWidget(row, col)
                 text = widget.findChild(QLabel).text() if widget and widget.findChild(QLabel) else ''
            else:
                item = self.table.item(row, col)
                text = item.text() if item else ''
            row_data.append(text)
            
        return row_data

    def open_popup(self, row):
        """Membuka pop-up rincian pesanan."""
        rowData = self.get_row_data(row)
        if not rowData: 
            print(f"Error: Data baris ke-{row} tidak ditemukan.")
            return

        # Menggunakan Tanggal Pesan (indeks 3)
        nomor_kamar = rowData[0]
        nama_lengkap = rowData[2]
        tanggal_pesan = rowData[3] 
        total_harga = rowData[4]
        status_saat_ini = rowData[5]

        # Data mock untuk rincian item (karena tidak ada di data tabel)
        mock_items = [
            {"item": "Le Minerale", "quantity": "1 galon"},
            {"item": "Indomie Ayam Bawang", "quantity": "2 pcs"},
            {"item": "Air Mineral Gelas", "quantity": "1 kotak"},
            {"item": "Sabun Mandi", "quantity": "1 buah"},
            {"item": "Shampo", "quantity": "1 botol"},
            {"item": "Kopi Sachet", "quantity": "10 sachet"},
            {"item": "Teh Celup", "quantity": "5 sachet"},
        ]
        
        dialog = PopUpPesanan(
            nomor_kamar, 
            nama_lengkap, 
            tanggal_pesan, 
            total_harga, 
            status_saat_ini, 
            mock_items
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Jika user memilih status baru, perbarui di tabel
            new_status = dialog.get_new_status()
            
            # Hapus widget lama
            self.table.removeCellWidget(row, 5)
            
            # Buat dan set widget status baru
            new_status_widget = StatusLabel(new_status)
            container = QWidget()
            h_layout = QHBoxLayout(container)
            h_layout.addWidget(new_status_widget)
            h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 5, container)
            
            QMessageBox.information(self, "Status Diperbarui", f"Status pesanan {nomor_kamar} ({nama_lengkap}) berhasil diperbarui menjadi: {new_status}")


class PopUpPesanan(QDialog):
    def __init__(self, nomor_kamar, nama_lengkap, tanggal_pesan, total_harga, status_saat_ini, rincian_pesanan):
        super().__init__()

        self.setWindowTitle('Pesanan Penghuni')
        # Ukuran diperbesar (dari 450x550 menjadi 550x650)
        self.setFixedSize(550, 650) 
        self.setModal(True)
        self.rincian_pesanan = rincian_pesanan
        self._new_status = status_saat_ini

        # Styling untuk seluruh Dialog
        self.setStyleSheet("""
            QDialog {
                background-color: white; 
                border: 1px solid #E0E0E0; 
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
            QLabel {
                color: #2D3142;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13pt; /* Ukuran font umum dinaikkan */
            }
            QLabel#CloseButton { /* Pastikan CloseButton styling tidak mengganggu label lain */
                font-size: 18pt;
            }
            QPushButton#CloseButton {
                border: none;
                background: none;
                font-size: 18pt;
                color: #333;
                font-weight: bold;
                margin-top: -5px; 
            }
            /* Styling untuk ComboBox Ubah Status */
            QComboBox {
                padding: 10px 12px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                min-height: 40px;
                background-color: white;
                font-weight: 500;
                color: #2D3142;
                font-size: 13pt; /* Ukuran font dinaikkan */
            }
            QComboBox::drop-down {
                border-left: 1px solid #E0E0E0;
                width: 25px;
            }
            QComboBox QAbstractItemView {
                selection-background-color: #E8F0FE;
                selection-color: #2D3142;
                border-radius: 6px;
                outline: 0;
            }
            /* Styling untuk Rincian Frame */
            QFrame#RincianFrame {
                border: 1px solid #E0E0E0; 
                border-radius: 8px; 
                background-color: white;
            }
            QLabel#RincianTitle {
                font-weight: bold;
                color: #555;
                font-size: 13pt; /* Ukuran font dipertahankan */
            }
        """)
        
        # Layout utama pop-up
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # 1. Header (Judul dan Tombol Close)
        header_layout = QHBoxLayout()
        title_label = QLabel("Pesanan Penghuni")
        title_label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #2D3142;") # Judul lebih besar
        
        close_button = QPushButton("X")
        close_button.setObjectName("CloseButton")
        close_button.setFixedSize(30, 30)
        close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_button.clicked.connect(self.accept) 
        
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(close_button)
        main_layout.addLayout(header_layout)
        
        # 2. Detail Pesanan (Menggunakan QVBoxLayout biasa)
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        detail_layout.setSpacing(8) # Spasi antar baris detail
        
        # Helper function untuk membuat baris detail
        def create_detail_row(label_text, value_text):
            row_layout = QHBoxLayout()
            label_widget = QLabel(f"<span style='font-weight: 600;'>{label_text}</span>")
            separator_widget = QLabel(":")
            value_widget = QLabel(value_text)
            
            label_widget.setFixedWidth(140) # Lebar label diperlebar
            
            row_layout.addWidget(label_widget)
            row_layout.addWidget(separator_widget)
            row_layout.addWidget(value_widget)
            row_layout.addStretch(1)
            return row_layout

        detail_layout.addLayout(create_detail_row("Nomor Kamar", nomor_kamar))
        detail_layout.addLayout(create_detail_row("Nama Lengkap", nama_lengkap))
        detail_layout.addLayout(create_detail_row("Tanggal Pesan", tanggal_pesan))
            
        main_layout.addWidget(detail_widget)
        
        # 3. Rincian Pesanan Box
        rincian_frame = QFrame()
        rincian_frame.setObjectName("RincianFrame")
        rincian_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Scroll Area untuk rincian
        rincian_scroll_area = QScrollArea()
        rincian_scroll_area.setWidgetResizable(True)
        rincian_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        rincian_scroll_area.setWidget(rincian_frame)
        
        rincian_layout = QVBoxLayout(rincian_frame)
        rincian_layout.setContentsMargins(15, 10, 15, 15)
        
        rincian_title = QLabel("RINCIAN PESANAN")
        rincian_title.setObjectName("RincianTitle")
        rincian_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rincian_layout.addWidget(rincian_title)
        rincian_layout.addSpacing(10)
        
        # Grid Layout untuk item agar item dan kuantitas sejajar rapi
        item_grid = QGridLayout()
        item_grid.setSpacing(8)
        
        # Header Item Grid
        header_item = QLabel("Item")
        header_item.setStyleSheet("font-weight: bold; color: #555;")
        header_item.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        header_qty = QLabel("Kuantitas")
        header_qty.setStyleSheet("font-weight: bold; color: #555;")
        header_qty.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        item_grid.addWidget(header_item, 0, 0, Qt.AlignmentFlag.AlignLeft)
        item_grid.addWidget(header_qty, 0, 1, Qt.AlignmentFlag.AlignRight)
        
        # Tampilkan item pesanan
        for idx, item_data in enumerate(self.rincian_pesanan):
            item_label = QLabel(item_data["item"])
            qty_label = QLabel(item_data["quantity"])
            qty_label.setAlignment(Qt.AlignmentFlag.AlignRight)

            item_grid.addWidget(item_label, idx + 1, 0, Qt.AlignmentFlag.AlignLeft)
            item_grid.addWidget(qty_label, idx + 1, 1, Qt.AlignmentFlag.AlignRight)

        rincian_layout.addLayout(item_grid)
        rincian_layout.addStretch(1) # Agar total harga selalu di bawah

        # Total Harga Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        rincian_layout.addWidget(separator)

        # Total Harga
        total_row = QHBoxLayout()
        total_label = QLabel("<span style='font-weight: bold;'>Total Harga</span>")
        total_value = QLabel(f"<span style='font-weight: bold; font-size: 14pt;'>{total_harga}</span>") # Total Harga lebih menonjol
        total_row.addWidget(total_label)
        total_row.addStretch(1)
        total_row.addWidget(total_value)
        rincian_layout.addLayout(total_row)
        
        main_layout.addWidget(rincian_scroll_area) # Tambahkan Scroll Area

        # 4. Action Buttons (Bukti Bayar & Ubah Status)
        action_button_layout = QHBoxLayout()
        action_button_layout.setSpacing(20)
        
        # Tombol Lihat Bukti Bayar (Orange)
        bukti_bayar_btn = QPushButton("Lihat Bukti Bayar")
        bukti_bayar_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        bukti_bayar_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800; /* Warna Oranye */
                color: white; 
                font-weight: bold; 
                padding: 10px; 
                border-radius: 8px;
                border: none;
                min-height: 40px;
                font-size: 13pt;
            }
            QPushButton:hover {
                background-color: #E68900;
            }
        """)
        bukti_bayar_btn.clicked.connect(lambda: QMessageBox.information(self, "Bukti Bayar", "Fitur melihat bukti bayar akan ditambahkan."))
        
        # ComboBox Ubah Status
        self.status_combo = QComboBox(self)
        self.status_combo.addItems(['Waiting', 'In Progress', 'Done']) 
        self.status_combo.setCurrentText(status_saat_ini)
        self.status_combo.setMinimumWidth(160)
        self.status_combo.currentIndexChanged.connect(self._update_new_status)
        
        # Label 'Ubah Status'
        status_container = QVBoxLayout()
        status_container.setSpacing(2)
        
        ubah_status_label = QLabel("Ubah Status")
        ubah_status_label.setStyleSheet("font-weight: 500; font-size: 10pt; color: #555;")
        ubah_status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        status_container.addWidget(ubah_status_label)
        status_container.addWidget(self.status_combo)
        
        action_button_layout.addWidget(bukti_bayar_btn)
        action_button_layout.addStretch(1)
        action_button_layout.addLayout(status_container)
        
        main_layout.addLayout(action_button_layout)
        
        self.setLayout(main_layout)

    def _update_new_status(self, index):
        """Memperbarui status internal saat ComboBox diubah."""
        self._new_status = self.status_combo.currentText()
        
    def get_new_status(self):
        """Mengembalikan status baru yang dipilih."""
        return self._new_status


