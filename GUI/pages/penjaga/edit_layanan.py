from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QDialog, QHBoxLayout


class EditLayanan(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Edit Layanan')
        self.setGeometry(100, 100, 800, 600)

        # Layout utama
        layout = QVBoxLayout()

        # Grid untuk menampilkan layanan
        self.grid_layout = QGridLayout()

        # Daftar layanan yang ada
        self.layanan_list = ['Laundry', 'Catering', 'Refill Galon', 'Belanja Kebutuhan']

        # Menambahkan tombol untuk setiap layanan
        self.update_layanan_grid()

        # Tombol Tambah Layanan
        tambah_layanan_button = QPushButton('Tambahkan Layanan', self)
        tambah_layanan_button.clicked.connect(self.add_layanan)
        layout.addWidget(tambah_layanan_button)

        # Menambahkan grid ke layout utama
        layout.addLayout(self.grid_layout)

        self.setLayout(layout)

    def update_layanan_grid(self):
        # Menghapus elemen lama sebelum menambahkan yang baru
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Menambahkan tombol untuk setiap layanan yang ada
        for i, layanan in enumerate(self.layanan_list):
            layanan_label = QLabel(layanan, self)
            edit_button = QPushButton('Edit', self)
            hapus_button = QPushButton('Hapus', self)
            
            # Menghubungkan tombol hapus dengan fungsi konfirmasi hapus
            hapus_button.clicked.connect(lambda checked, layanan=layanan: self.show_confirmation_popup(layanan))
            
            # Menghubungkan tombol edit untuk membuka pop-up EditLaundryDialog
            if layanan == "Laundry":
                edit_button.clicked.connect(self.open_laundry_dialog)
            elif layanan == "Catering":
                edit_button.clicked.connect(self.open_catering_dialog)
            elif layanan == "Refill":
                edit_button.clicked.connect(self.open_refill_dialog)
            elif layanan == "Belanja":
                edit_button.clicked.connect(self.open_belanja_dialog)

            # Menambahkan elemen ke dalam grid
            self.grid_layout.addWidget(layanan_label, i//2, (i%2)*2)
            self.grid_layout.addWidget(edit_button, i//2, (i%2)*2 + 1)
            self.grid_layout.addWidget(hapus_button, (i//2) + 1, (i%2)*2 + 1)

    def open_laundry_dialog(self):
        from components.edit_laundry import EditLaundryDialog
        # Menampilkan pop-up untuk edit laundry
        dialog = EditLaundryDialog()
        dialog.exec()
    
    def open_catering_dialog(self):
        from components.edit_catering import EditCateringDialog
        dialog = EditCateringDialog()
        dialog.exec()
    
    def open_refill_dialog(self):
        from components.edit_refill import EditRefillDialog  # Import EditRefillDialog dari components
        dialog = EditRefillDialog()
        dialog.exec()

    def open_belanja_dialog(self):
        from components.edit_belanja import EditBelanjaDialog  # Import EditBelanjaDialog dari components
        dialog = EditBelanjaDialog()
        dialog.exec()


    def add_layanan(self):
        # Menambahkan layanan baru
        dialog = AddLayananDialog()
        if dialog.exec():
            new_layanan = dialog.get_layanan()
            if new_layanan:
                self.layanan_list.append(new_layanan)
                self.update_layanan_grid()  # Perbarui grid dengan layanan baru

    def show_confirmation_popup(self, layanan):
        # Membuka pop-up konfirmasi hapus
        dialog = ConfirmationDialog(layanan)
        dialog.exec()

class ConfirmationDialog(QDialog):
    def __init__(self, layanan):
        super().__init__()

        self.layanan = layanan
        self.setWindowTitle('Konfirmasi Hapus')
        self.setGeometry(150, 150, 300, 150)

        # Layout pop-up
        layout = QVBoxLayout()

        # Label konfirmasi
        confirmation_label = QLabel(f"Apakah Anda yakin untuk menghapus layanan {self.layanan}?", self)

        # Tombol Yes dan No
        button_layout = QHBoxLayout()
        yes_button = QPushButton('Yes', self)
        no_button = QPushButton('No', self)
        
        # Menghubungkan tombol
        yes_button.clicked.connect(self.confirm_delete)
        no_button.clicked.connect(self.reject)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        # Menambahkan elemen ke layout
        layout.addWidget(confirmation_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def confirm_delete(self):
        print(f"Layanan {self.layanan} telah dihapus.")
        self.accept()  # Menutup pop-up setelah konfirmasi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditLayanan()
    window.show()
    sys.exit(app.exec())
