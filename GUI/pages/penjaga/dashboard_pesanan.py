import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QDialog, QLabel, QComboBox,
    QLineEdit, QFrame, QHeaderView, QAbstractItemView, QMessageBox,
    QSizePolicy, QGridLayout, QScrollArea
)
from PyQt6.QtGui import QFont, QCursor, QColor
from PyQt6.QtCore import Qt, QSize

# --- GAYA GLOBAL ---
STYLE_SHEET = """
QWidget { font-family: 'Segoe UI'; color: #2D3142; background-color: white; }

QLabel#PageTitle { 
    font-size: 24px; 
    font-weight: bold; 
    margin: 10px 0 25px 0; 
    color: #2D3142; 
}

QFrame#ContentFrame { 
    border: 1px solid #E0E0E0; 
    border-radius: 10px; 
    background-color: #FFFFFF; 
}

QLineEdit { 
    padding: 10px; 
    border: 1px solid #E0E0E0; 
    border-radius: 8px; 
    background: #F8F9FA; 
    min-height: 35px; 
}
QLineEdit:focus { 
    border: 1px solid #4A90E2; 
    background: white; 
}

QTableWidget { 
    border: none; 
    gridline-color: #F0F0F0; 
    selection-background-color: #E8F0FE; 
    selection-color: #2D3142; 
    outline: 0; 
}

QHeaderView::section { 
    background-color: #E8D5A8; 
    color: #333; 
    padding: 12px; 
    border: none; 
    font-weight: bold; 
}

QPushButton.ActionBtn { 
    border: none; 
    background: none; 
    color: #4A90E2; 
    font-weight: bold; 
    font-size: 13px; 
}
QPushButton.ActionBtn:hover {
    color: #357ABD;
    text-decoration: underline;
}
"""

class StatusLabel(QLabel):
    """Widget status dengan ukuran yang lebih proporsional"""
    def __init__(self, status):
        super().__init__(status)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Style dasar: Font lebih kecil, radius lebih halus
        base_style = "border-radius: 12px; padding: 2px 5px; font-weight: bold; font-size: 11px;"
        
        if status in ['Done', 'Completed']:
            # Hijau Soft
            self.setStyleSheet(f"background-color: #D1E7DD; color: #0F5132; {base_style}")
        elif status == 'In Progress':
            # Kuning Soft
            self.setStyleSheet(f"background-color: #FFF3CD; color: #856404; {base_style}")
        else: # Waiting/Pending
            # Abu Soft (Lebih netral daripada coklat sebelumnya)
            self.setStyleSheet(f"background-color: #F8F9FA; color: #6C757D; border: 1px solid #DEE2E6; {base_style}")
            
        # FIX: Ukuran diperkecil agar tidak memenuhi tabel
        self.setFixedSize(QSize(90, 24))

class DashboardPenjaga(QWidget):
    def __init__(self, request_service=None):
        super().__init__()
        self.request_service = request_service 
        self.setWindowTitle('Dashboard Pesanan Penghuni')
        self.setStyleSheet(STYLE_SHEET)

        main_l = QVBoxLayout(self)
        main_l.setContentsMargins(40, 40, 40, 40); main_l.setSpacing(20)

        main_l.addWidget(QLabel("Dashboard Pesanan Penghuni", objectName="PageTitle"))

        frame = QFrame(self); frame.setObjectName("ContentFrame")
        content_l = QVBoxLayout(frame); content_l.setContentsMargins(20, 20, 20, 20); content_l.setSpacing(15)

        search_l = QHBoxLayout()
        self.search_inp = QLineEdit(); self.search_inp.setPlaceholderText("🔍 Search pesanan...")
        self.search_inp.textChanged.connect(self.on_search)
        search_l.addWidget(self.search_inp)
        content_l.addLayout(search_l)

        self.table = self._create_table()
        content_l.addWidget(self.table)
        
        main_l.addWidget(frame)
        
        self.refresh_data()

    def refresh_data(self):
        self.table.setRowCount(0) 
        if not self.request_service: return

        try:
            requests = self.request_service.get_all_requests_with_details()
        except Exception as e:
            print(f"DB Error: {e}")
            requests = []

        self.full_data = requests
        self.table.setRowCount(len(requests))
        
        for row, data in enumerate(requests):
            kamar = data.get('nomor_kamar') if data.get('nomor_kamar') else "-"
            self._set_item(row, 0, kamar)
            self._set_item(row, 1, data['nama_lengkap'])
            self._set_item(row, 2, data['nama_layanan'])
            
            tgl = data['tanggal_request'].strftime("%d/%m/%Y") if data['tanggal_request'] else "-"
            self._set_item(row, 3, tgl)
            
            # Status Widget
            status_txt = data['status_request']
            if status_txt == 'Pending': status_txt = 'Waiting'
            
            st_widget = StatusLabel(status_txt)
            
            # Container layout agar widget status rapi di tengah sel
            container = QWidget()
            lh = QHBoxLayout(container)
            lh.addWidget(st_widget)
            lh.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lh.setContentsMargins(0, 4, 0, 4) # Tambah margin atas-bawah agar tidak sesak
            self.table.setCellWidget(row, 4, container)
            
            # Tombol Detail
            btn = QPushButton('📝 Detail')
            btn.setProperty("class", "ActionBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, r=row: self.open_popup(r))
            
            btn_con = QWidget(); bh = QHBoxLayout(btn_con); bh.addWidget(btn); bh.setAlignment(Qt.AlignmentFlag.AlignCenter); bh.setContentsMargins(0,0,0,0)
            self.table.setCellWidget(row, 5, btn_con)

    def _set_item(self, row, col, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, col, item)

    def _create_table(self):
        t = QTableWidget()
        headers = ['Kamar', 'Nama', 'Layanan', 'Tanggal', 'Status', 'Aksi']
        t.setColumnCount(len(headers))
        t.setHorizontalHeaderLabels(headers)
        
        t.verticalHeader().setVisible(False)
        t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        t.setShowGrid(False) # Tampilan lebih bersih tanpa grid vertikal tajam
        
        h = t.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed); t.setColumnWidth(4, 120) # Lebar Status pas
        h.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed); t.setColumnWidth(5, 100)
        
        # Set tinggi baris agar badge punya ruang napas
        t.verticalHeader().setDefaultSectionSize(45)
        
        return t

    def open_popup(self, row):
        if row >= len(self.full_data): return
        data = self.full_data[row]
        req_id = data['request_id']
        status_ui = data['status_request']
        if status_ui == 'Pending': status_ui = 'Waiting'

        dialog = PopUpPesanan(data, status_ui)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_status_ui = dialog.get_new_status()
            new_status_db = new_status_ui
            if new_status_ui == 'Waiting': new_status_db = 'Pending'
            
            if self.request_service:
                if self.request_service.update_status_request(req_id, new_status_db):
                    QMessageBox.information(self, "Sukses", "Status berhasil diperbarui!")
                    self.refresh_data()
                else:
                    QMessageBox.warning(self, "Gagal", "Gagal update status.")

    def on_search(self):
        txt = self.search_inp.text().lower()
        for r in range(self.table.rowCount()):
            match = False
            item_nama = self.table.item(r, 1)
            item_layanan = self.table.item(r, 2)
            if (item_nama and txt in item_nama.text().lower()) or \
               (item_layanan and txt in item_layanan.text().lower()):
                match = True
            self.table.setRowHidden(r, not match)


class PopUpPesanan(QDialog):
    def __init__(self, data, current_status):
        super().__init__()
        self.data = data
        self._new_status = current_status
        
        self.setWindowTitle("Detail Pesanan")
        self.setFixedSize(500, 550)
        self.setStyleSheet("""
            QDialog { background: white; border-radius: 10px; }
            QLabel { color: #2D3142; font-family: 'Segoe UI'; font-size: 12pt; }
            QComboBox { padding: 5px; border: 1px solid #ccc; border-radius: 5px; font-size: 12pt;}
            QPushButton#SaveBtn { background: #4CAF50; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30); layout.setSpacing(20)
        
        header = QLabel(f"Pesanan #{data['request_id']}")
        header.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(header)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        self.add_row(form_layout, "Nama Pemesan:", data['nama_lengkap'])
        self.add_row(form_layout, "Nomor Kamar:", data.get('nomor_kamar') or "-")
        self.add_row(form_layout, "Layanan:", data['nama_layanan'])
        self.add_row(form_layout, "Harga:", f"Rp {data['harga_layanan']:,}")
        
        layout.addLayout(form_layout)
        
        layout.addWidget(QLabel("<b>Catatan / Rincian:</b>"))
        catatan_box = QFrame()
        catatan_box.setStyleSheet("background: #F8F9FA; border: 1px solid #EEE; border-radius: 8px;")
        c_layout = QVBoxLayout(catatan_box)
        
        catatan_text = data.get('catatan') if data.get('catatan') else "Tidak ada catatan tambahan."
        lbl_catatan = QLabel(catatan_text)
        lbl_catatan.setWordWrap(True)
        c_layout.addWidget(lbl_catatan)
        
        layout.addWidget(catatan_box)
        layout.addStretch()
        
        layout.addWidget(QLabel("<b>Update Status Pengerjaan:</b>"))
        self.combo = QComboBox()
        self.combo.addItems(['Waiting', 'In Progress', 'Done'])
        self.combo.setCurrentText(current_status)
        self.combo.currentIndexChanged.connect(self.update_status_var)
        layout.addWidget(self.combo)
        
        btn_save = QPushButton("Simpan Perubahan")
        btn_save.setObjectName("SaveBtn")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

    def add_row(self, layout, label, value):
        row = QHBoxLayout()
        l = QLabel(label); l.setStyleSheet("font-weight: bold; color: #666;")
        v = QLabel(str(value)); v.setAlignment(Qt.AlignmentFlag.AlignRight)
        row.addWidget(l); row.addStretch(); row.addWidget(v)
        layout.addLayout(row)
        
    def update_status_var(self):
        self._new_status = self.combo.currentText()
        
    def get_new_status(self):
        return self._new_status