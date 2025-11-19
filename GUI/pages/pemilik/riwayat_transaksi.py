import tkinter as tk
from tkinter import ttk, messagebox

class RiwayatTransaksi(tk.Frame):
    """Halaman untuk menampilkan riwayat transaksi"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.tree = None
        self.create_content()

    def create_content(self):
        """Membuat konten halaman Riwayat Transaksi"""
        print("Membuat konten Riwayat Transaksi...")
        
        # Judul Halaman
        title = tk.Label(
            self,
            text="Riwayat Transaksi",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2D3142'
        )
        title.pack(pady=(30, 20), padx=40, anchor='w')
        
        # Frame pencarian dan filter
        self.create_search_filter()

        # Kontainer untuk tabel riwayat transaksi
        table_outer_frame = tk.Frame(self, bg='#E0E0E0', padx=1, pady=1)
        table_outer_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 40))

        # Data transaksi contoh
        self.data = [
            ["04/17/23", "Rp. 1.000.000", "A01", 1, "Accept"],
            ["04/17/23", "Rp. 1.000.000", "A01", 1, "Decline"],
            ["04/17/23", "Rp. 1.000.000", "A01", 1, "Accept"],
            ["04/17/23", "Rp. 1.000.000", "A01", 1, "Accept"],
            ["04/17/23", "Rp. 1.000.000", "A01", 1, "Decline"],
        ]

        # Kolom-kolom tabel
        columns = ["Tanggal", "Pemasukan", "Username Penghuni", "Bulan ke-", "Status Pembayaran", "Action"]

        # Membuat tabel untuk riwayat transaksi
        self.create_table(table_outer_frame, columns, self.data)

        print("Halaman Riwayat Transaksi berhasil dibuat!")

    def create_search_filter(self):
        """Membuat bar pencarian dan tombol filter"""
        search_frame = tk.Frame(self, bg='white')
        search_frame.pack(fill=tk.X, padx=40, pady=(0, 10))

        # Kontainer untuk pencarian dengan border
        search_container = tk.Frame(search_frame, bg='#F0F0F0', relief='solid', borderwidth=1)
        search_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Ikon pencarian (🔍)
        search_icon = tk.Label(
            search_container,
            text="🔍",
            font=('Arial', 12),
            bg='#F0F0F0',
            fg='#666666'
        )
        search_icon.pack(side=tk.LEFT, padx=(10, 5))

        # Kolom pencarian
        self.search_entry = tk.Entry(
            search_container,
            font=('Arial', 11),
            bg='#F0F0F0',
            fg='#333333',
            relief='flat',
            borderwidth=0
        )
        self.search_entry.insert(0, "Search transaksi")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=8)

        # Placeholder behavior
        self.search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in())
        self.search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out())
        self.search_entry.bind('<KeyRelease>', lambda e: self.on_search())

        # Tombol filter
        filter_btn = tk.Button(
            search_frame,
            text="Filter ☰",
            font=('Arial', 11),
            bg='white',
            fg='#333333',
            relief='solid',
            borderwidth=1,
            padx=20,
            pady=6,
            cursor='hand2',
            command=self.show_filter
        )
        filter_btn.pack(side=tk.RIGHT)

    def on_search_focus_in(self):
        """Menghapus placeholder saat fokus"""
        if self.search_entry.get() == "Search transaksi":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='#333333')

    def on_search_focus_out(self):
        """Menambahkan placeholder jika kosong"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search transaksi")
            self.search_entry.config(fg='#999999')

    def on_search(self):
        """Memfilter tabel berdasarkan pencarian"""
        search_text = self.search_entry.get().lower()
        if search_text == "search transaksi":
            return
        
        # Menghapus item yang ada
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Menyaring data yang sesuai
        for idx, row in enumerate(self.data):
            if any(search_text in str(field).lower() for field in row):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert('', tk.END, values=row, tags=(tag,))

    def show_filter(self):
        """Menampilkan filter"""
        messagebox.showinfo("Filter", "Opsi filter akan datang segera!")

    def create_table(self, parent, columns, data):
        """Membuat tabel untuk menampilkan data transaksi"""

        # Style konfigurasi
        style = ttk.Style()
        style.theme_use('clam')

        # Konfigurasi style untuk Treeview
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground="#333333",
            rowheight=40,
            fieldbackground="white",
            borderwidth=0,
            font=('Arial', 10)
        )

        # Konfigurasi header Treeview
        style.configure(
            "Custom.Treeview.Heading",
            background="#E8D5A8",  # Warna kuning krem seperti di desain
            foreground="#333333",
            borderwidth=1,
            relief="flat",
            font=('Arial', 12, 'bold')
        )

        style.map(
            "Custom.Treeview.Heading",
            background=[('active', '#D4C198')]
        )

        # Frame tabel
        table_frame = tk.Frame(parent, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview dengan style kustom
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            yscrollcommand=scrollbar.set,
            style="Custom.Treeview"
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.tree.yview)

        # Menyusun lebar kolom
        column_widths = {
            "Tanggal": 120,
            "Pemasukan": 120,
            "Username Penghuni": 150,
            "Bulan ke-": 90,
            "Status Pembayaran": 140,
            "Action": 90
        }

        for col in columns:
            self.tree.heading(col, text=col)
            width = column_widths.get(col, 150)
            self.tree.column(col, width=width, anchor='center')

        # Konfigurasi warna baris
        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#FAFAFA')

        # Memasukkan data ke dalam tabel
        for idx, row in enumerate(data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            # Menambahkan kolom aksi
            row_with_action = list(row) + ["📝"]
            self.tree.insert('', tk.END, values=row_with_action, tags=(tag,))

        # Menyusun event klik pada baris
        self.tree.bind('<Double-1>', lambda e: self.view_selected())
        self.tree.bind('<Button-1>', self.on_row_click)

    def on_row_click(self, event):
        """Menangani klik pada baris tabel"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            selected = self.tree.selection()

            if selected:
                # Mengecek apakah klik pada kolom Action
                col_index = int(column.replace('#', '')) - 1
                if col_index == 5:  # Kolom Action
                    # Menampilkan menu aksi
                    self.show_action_menu(event)

    def show_action_menu(self, event):
        """Menampilkan menu aksi ketika kolom Action diklik"""
        # Membuat menu popup
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="👁️ Lihat Detail", command=self.view_selected)
        menu.add_command(label="✏️     Edit", command=self.edit_selected)
        menu.add_separator()
        menu.add_command(label="🗑️ Hapus", command=self.delete_selected)

        # Menampilkan menu pada posisi kursor
        menu.post(event.x_root, event.y_root)

    def view_selected(self):
        """Melihat detail transaksi yang dipilih"""
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang ingin dilihat!")
            return

        item = self.tree.item(selected[0])
        values = item['values']

        # Menampilkan detail pada message box
        details = f"""
            Detail Transaksi:

            Tanggal        : {values[0]}
            Pemasukan      : {values[1]}
            Username       : {values[2]}
            Bulan ke-      : {values[3]}
            Status Pembayaran: {values[4]}
        """
        
        messagebox.showinfo("Detail Transaksi", details)

    def edit_selected(self):
        """Edit transaksi yang dipilih"""
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang ingin diedit!")
            return

        item = self.tree.item(selected[0])
        values = item['values']

        # TODO: Buka halaman edit
        # Edit status pembayaran saja
        messagebox.showinfo("Edit", f"Edit transaksi: {values[2]}\n(Fitur coming soon)")

    def delete_selected(self):
        """Hapus transaksi yang dipilih"""
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang ingin dihapus!")
            return

        item = self.tree.item(selected[0])
        values = item['values']

        # Konfirmasi penghapusan
        response = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus transaksi:\n{values[2]}?"
        )

        if response:
            self.tree.delete(selected[0])
            messagebox.showinfo("Sukses", "Transaksi berhasil dihapus!")

# Test standalone
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Riwayat Transaksi")

    app = RiwayatTransaksi(root, None)
    app.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
