import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, 
    QLabel, QFrame, QSizePolicy, QMessageBox, QScrollArea
)
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

# FIX IMPORT: Pastikan path ini benar sesuai struktur folder Anda
# Jika generic_service_dialog.py ada di GUI/components/penjaga/
try:
    from GUI.components.penjaga.generic_service_dialog import GenericServiceDialog
except ImportError:
    # Fallback untuk testing jika path beda
    print("Error: Tidak bisa import GenericServiceDialog")
    GenericServiceDialog = None

# --- STYLE SHEET (Tidak Berubah) ---
STYLE_SHEET = """
QWidget { font-family: 'Segoe UI'; color: #2D3142; background-color: #F8F9FA; }
QLabel#PageTitle { font-size: 24px; font-weight: bold; margin: 10px 0 25px 0; }
QFrame#ServiceCard { border: 1px solid #E0E0E0; border-radius: 10px; background-color: #FFFFFF; min-width: 200px; min-height: 250px; padding: 15px; }
QLabel#ServiceTitle { font-size: 16pt; font-weight: bold; margin-bottom: 10px; }
QLabel#ServicePrice { font-size: 12pt; color: #FF9800; font-weight: bold; margin-bottom: 5px; }
QPushButton.CardActionBtn { background-color: #FF9800; color: white; font-weight: 600; padding: 8px; border-radius: 6px; min-height: 35px; }
QPushButton.CardActionBtn:hover { background-color: #E68900; }
QFrame#AddCard { border: 1px dashed #B0B0B0; border-radius: 10px; background-color: #FFFFFF; min-width: 200px; min-height: 250px; }
"""

# --- SERVICE CARD ---
class ServiceCard(QFrame):
    def __init__(self, layanan_obj, edit_callback, delete_callback, parent=None):
        super().__init__(parent)
        self.setObjectName("ServiceCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)

        # Judul
        lbl_name = QLabel(layanan_obj.nama)
        lbl_name.setObjectName("ServiceTitle")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_name.setWordWrap(True)
        
        # Harga
        lbl_price = QLabel(f"Rp {layanan_obj.harga:,.0f}")
        lbl_price.setObjectName("ServicePrice")
        lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Deskripsi
        desc_short = (layanan_obj.deskripsi[:50] + '...') if len(layanan_obj.deskripsi) > 50 else layanan_obj.deskripsi
        lbl_desc = QLabel(desc_short)
        lbl_desc.setStyleSheet("color: #666; font-size: 10pt;")
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_desc.setWordWrap(True)

        layout.addWidget(lbl_name)
        layout.addWidget(lbl_price)
        layout.addWidget(lbl_desc)
        layout.addStretch()

        # Tombol
        btn_edit = QPushButton("Edit")
        btn_edit.setProperty("class", "CardActionBtn")
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.clicked.connect(lambda: edit_callback(layanan_obj))
        layout.addWidget(btn_edit)

        btn_del = QPushButton("Hapus")
        btn_del.setProperty("class", "CardActionBtn")
        btn_del.setStyleSheet("background-color: #D32F2F; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.clicked.connect(lambda: delete_callback(layanan_obj))
        layout.addWidget(btn_del)

class AddServiceCard(QFrame):
    def __init__(self, add_callback, parent=None):
        super().__init__(parent)
        self.setObjectName("AddCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mousePressEvent = lambda e: add_callback() if e.button() == Qt.MouseButton.LeftButton else None
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_title = QLabel("Tambahkan Layanan")
        lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #888;")
        lbl_plus = QLabel("+")
        lbl_plus.setStyleSheet("font-size: 50pt; color: #B0B0B0; background: transparent;")
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_plus, alignment=Qt.AlignmentFlag.AlignCenter)

# --- MAIN PAGE ---
class EditLayanan(QWidget):
    def __init__(self, layanan_service):
        super().__init__()
        self.service = layanan_service
        self.setWindowTitle('Edit Layanan')
        self.setStyleSheet(STYLE_SHEET)

        main_l = QVBoxLayout(self)
        main_l.setContentsMargins(30, 30, 30, 30)
        
        main_l.addWidget(QLabel("Daftar Layanan Kos", objectName="PageTitle"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        
        self.content_widget = QWidget()
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        scroll.setWidget(self.content_widget)
        main_l.addWidget(scroll)

        self.refresh_grid()

    def refresh_grid(self):
        # Clear
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget: widget.deleteLater()

        # Fetch
        try:
            layanan_list = self.service.get_all_layanan()
        except Exception as e:
            print(f"DB Error: {e}")
            layanan_list = []

        # Render
        cols = 3
        for i, item in enumerate(layanan_list):
            card = ServiceCard(item, self.handle_edit, self.handle_delete)
            self.grid_layout.addWidget(card, i // cols, i % cols)

        # Add Button
        idx = len(layanan_list)
        add_card = AddServiceCard(self.handle_add)
        self.grid_layout.addWidget(add_card, idx // cols, idx % cols)

    def handle_add(self):
        if not GenericServiceDialog: return
        dlg = GenericServiceDialog(self, layanan=None)
        if dlg.exec():
            data = dlg.get_data()
            new_obj = self.service.create_layanan(
                nama=data['nama'], deskripsi=data['deskripsi'],
                harga=data['harga'], kebutuhan=data['kebutuhan']
            )
            if new_obj:
                QMessageBox.information(self, "Sukses", "Layanan berhasil dibuat!")
                self.refresh_grid()
            else:
                QMessageBox.warning(self, "Gagal", "Gagal membuat layanan (Cek nama duplikat?).")

    def handle_edit(self, layanan_obj):
        if not GenericServiceDialog: return
        dlg = GenericServiceDialog(self, layanan=layanan_obj)
        if dlg.exec():
            data = dlg.get_data()
            success = self.service.update_layanan(
                id=layanan_obj.id, nama=data['nama'],
                deskripsi=data['deskripsi'], harga=data['harga'],
                kebutuhan=data['kebutuhan']
            )
            if success:
                QMessageBox.information(self, "Sukses", "Layanan diperbarui.")
                self.refresh_grid()
            else:
                QMessageBox.warning(self, "Gagal", "Update gagal.")

    def handle_delete(self, layanan_obj):
        reply = QMessageBox.question(self, "Hapus", f"Hapus layanan '{layanan_obj.nama}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.service.delete_layanan(layanan_obj.id):
                self.refresh_grid()
            else:
                QMessageBox.warning(self, "Gagal", "Gagal menghapus.")