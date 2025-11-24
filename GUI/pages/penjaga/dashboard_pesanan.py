import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QDialog, QLabel, QComboBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class DashboardPenjaga(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dashboard Pesanan Penjaga')
        self.setGeometry(100, 100, 800, 600)

        # Layout utama
        layout = QVBoxLayout()

        # Tabel pesanan penghuni
        self.table = QTableWidget(self)
        self.table.setRowCount(5)  # Contoh data 5 pesanan
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Nomor Kamar', 'Nama Lengkap', 'Tanggal Masuk', 'Total Harga', 'Action'])

        # Isi tabel dengan data contoh
        data = [
            ['A01', 'Benjamin Franklin', '04/17/23', 'Rp20.000', ''],
            ['A02', 'Albert Einstein', '04/15/23', 'Rp30.000', ''],
            ['A03', 'Marie Curie', '04/10/23', 'Rp25.000', ''],
            ['A04', 'Isaac Newton', '04/20/23', 'Rp15.000', ''],
            ['A05', 'Charles Darwin', '04/18/23', 'Rp18.000', ''],
        ]

        for row, rowData in enumerate(data):
            for column, value in enumerate(rowData):
                self.table.setItem(row, column, QTableWidgetItem(value))

            # Menambahkan tombol Action di setiap baris
            action_button = QPushButton('Action', self)
            action_button.clicked.connect(lambda checked, row=row: self.open_popup(row))
            self.table.setCellWidget(row, 4, action_button)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def open_popup(self, row):
        # Membuka pop-up dengan rincian pesanan
        dialog = PopUpPesanan(row)
        dialog.exec()


class PopUpPesanan(QDialog):
    def __init__(self, row):
        super().__init__()

        self.setWindowTitle('Detail Pesanan')
        self.setGeometry(150, 150, 400, 300)

        # Layout pop-up
        layout = QVBoxLayout()

        # Detail pesanan
        self.nomor_kamar_label = QLabel(f"Nomor Kamar: A{row+1}")
        self.nama_label = QLabel(f"Nama Lengkap: Nama Penghuni {row+1}")
        self.tanggal_label = QLabel(f"Tanggal Masuk: 04/{17+row}/23")
        self.total_harga_label = QLabel(f"Total Harga: Rp{(20000 + (row * 5000)):,}")

        # Dropdown untuk status
        self.status_label = QLabel('Status:')
        self.status_combo = QComboBox(self)
        self.status_combo.addItems(['Pending', 'In Progress', 'Completed'])
        
        # Button untuk simpan status
        self.simpan_button = QPushButton('Simpan Status', self)
        self.simpan_button.clicked.connect(self.simpan_status)

        # Menambahkan elemen ke layout
        layout.addWidget(self.nomor_kamar_label)
        layout.addWidget(self.nama_label)
        layout.addWidget(self.tanggal_label)
        layout.addWidget(self.total_harga_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_combo)
        layout.addWidget(self.simpan_button)

        self.setLayout(layout)

    def simpan_status(self):
        # Menyimpan status yang dipilih
        status = self.status_combo.currentText()
        print(f"Status pesanan diubah menjadi: {status}")
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardPenjaga()
    window.show()
    sys.exit(app.exec())
