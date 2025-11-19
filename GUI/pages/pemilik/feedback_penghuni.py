# # import tkinter as tk
# # from tkinter import ttk, messagebox

# # class FeedbackPenghuni(tk.Frame):
# #     """Halaman untuk menampilkan feedback penghuni"""
    
# #     def __init__(self, parent, controller):
# #         super().__init__(parent, bg='white')
# #         self.controller = controller
# #         self.tree = None
# #         self.create_content()
    
# #     def create_content(self):
# #         """Membuat konten halaman Feedback Penghuni"""
# #         print("Membuat konten Feedback Penghuni...")
        
# #         # Judul Halaman
# #         title = tk.Label(
# #             self,
# #             text="Record Feedback Penghuni",
# #             font=('Arial', 18, 'bold'),
# #             bg='white',
# #             fg='#2D3142'
# #         )
# #         title.pack(pady=(30, 20), padx=40, anchor='w')
        
# #         # Frame pencarian dan filter
# #         self.create_search_filter()

# #         # Kontainer untuk tabel feedback penghuni
# #         table_outer_frame = tk.Frame(self, bg='#E0E0E0', padx=1, pady=1)
# #         table_outer_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 40))

# #         # Data feedback penghuni contoh
# #         self.data = [
# #             ["04/17/23", "A01\nLeslie Alexander", "Saya merasa sangat puas dengan pelayanan Kos Melati, pelayanan sangat lengkap dan rumahnya nyaman serta bersih", "★★★★★"],
# #             ["04/17/23", "A01\nLeslie Alexander", "Saya merasa sangat puas dengan pelayanan Kos Melati, pelayanan sangat lengkap dan rumahnya nyaman serta bersih", "★★★★★"],
# #             ["04/17/23", "A01\nLeslie Alexander", "Saya merasa sangat puas dengan pelayanan Kos Melati, pelayanan sangat lengkap dan rumahnya nyaman serta bersih", "★★★★★"],
# #             ["04/17/23", "A01\nLeslie Alexander", "Saya merasa sangat puas dengan pelayanan Kos Melati, pelayanan sangat lengkap dan rumahnya nyaman serta bersih", "★★★★★"],
# #             ["04/17/23", "A01\nLeslie Alexander", "Saya merasa sangat puas dengan pelayanan Kos Melati, pelayanan sangat lengkap dan rumahnya nyaman serta bersih", "★★★★★"],
# #         ]

# #         # Kolom tabel
# #         columns = ["Tanggal", "Penghuni", "Pesan Feedback", "Rating"]

# #         # Membuat Treeview untuk feedback penghuni
# #         self.create_table(table_outer_frame, columns, self.data)
    
# #     def create_search_filter(self):
# #         """Membuat bar pencarian dan tombol filter"""
# #         search_frame = tk.Frame(self, bg='white')
# #         search_frame.pack(fill=tk.X, padx=40, pady=(0, 10))

# #         # Kontainer untuk pencarian dengan border
# #         search_container = tk.Frame(search_frame, bg='#F0F0F0', relief='solid', borderwidth=1)
# #         search_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

# #         # Ikon pencarian (🔍)
# #         search_icon = tk.Label(
# #             search_container,
# #             text="🔍",
# #             font=('Arial', 12),
# #             bg='#F0F0F0',
# #             fg='#666666'
# #         )
# #         search_icon.pack(side=tk.LEFT, padx=(10, 5))

# #         # Kolom pencarian
# #         self.search_entry = tk.Entry(
# #             search_container,
# #             font=('Arial', 11),
# #             bg='#F0F0F0',
# #             fg='#333333',
# #             relief='flat',
# #             borderwidth=0
# #         )
# #         self.search_entry.insert(0, "Search feedback")
# #         self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=8)

# #         # Placeholder behavior
# #         self.search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in())
# #         self.search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out())
# #         self.search_entry.bind('<KeyRelease>', lambda e: self.on_search())

# #         # Tombol filter
# #         filter_btn = tk.Button(
# #             search_frame,
# #             text="Filter ☰",
# #             font=('Arial', 11),
# #             bg='white',
# #             fg='#333333',
# #             relief='solid',
# #             borderwidth=1,
# #             padx=20,
# #             pady=6,
# #             cursor='hand2',
# #             command=self.show_filter
# #         )
# #         filter_btn.pack(side=tk.RIGHT)

# #     def on_search_focus_in(self):
# #         """Menghapus placeholder saat fokus"""
# #         if self.search_entry.get() == "Search feedback":
# #             self.search_entry.delete(0, tk.END)
# #             self.search_entry.config(fg='#333333')

# #     def on_search_focus_out(self):
# #         """Menambahkan placeholder jika kosong"""
# #         if not self.search_entry.get():
# #             self.search_entry.insert(0, "Search feedback")
# #             self.search_entry.config(fg='#999999')

# #     def on_search(self):
# #         """Memfilter tabel berdasarkan pencarian"""
# #         search_text = self.search_entry.get().lower()
# #         if search_text == "search feedback":
# #             return
        
# #         # Menghapus item yang ada
# #         for item in self.tree.get_children():
# #             self.tree.delete(item)

# #         # Menyaring data yang sesuai
# #         for idx, row in enumerate(self.data):
# #             if any(search_text in str(field).lower() for field in row):
# #                 tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
# #                 self.tree.insert('', tk.END, values=row, tags=(tag,))

# #     def show_filter(self):
# #         """Menampilkan filter"""
# #         messagebox.showinfo("Filter", "Opsi filter akan datang segera!")

# #     def create_table(self, parent, columns, data):
# #         """Membuat tabel untuk menampilkan feedback penghuni"""

# #         # Style konfigurasi
# #         style = ttk.Style()
# #         style.theme_use('clam')

# #         # Konfigurasi style untuk Treeview
# #         style.configure(
# #             "Custom.Treeview",
# #             background="white",
# #             foreground="#333333",
# #             rowheight=40,
# #             fieldbackground="white",
# #             borderwidth=0,
# #             font=('Arial', 10)
# #         )

# #         # Konfigurasi header Treeview
# #         style.configure(
# #             "Custom.Treeview.Heading",
# #             background="#E8D5A8",  # Warna kuning krem seperti di desain
# #             foreground="#333333",
# #             borderwidth=1,
# #             relief="flat",
# #             font=('Arial', 10, 'bold')
# #         )

# #         style.map(
# #             "Custom.Treeview.Heading",
# #             background=[('active', '#D4C198')]
# #         )

# #         # Frame tabel
# #         table_frame = tk.Frame(parent, bg='white')
# #         table_frame.pack(fill=tk.BOTH, expand=True)

# #         # Scrollbar
# #         scrollbar = ttk.Scrollbar(table_frame)
# #         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# #         # Treeview dengan style kustom
# #         self.tree = ttk.Treeview(
# #             table_frame, 
# #             columns=columns, 
# #             show="headings",
# #             yscrollcommand=scrollbar.set,
# #             style="Custom.Treeview"
# #         )
# #         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# #         scrollbar.config(command=self.tree.yview)

# #         # Menyusun lebar kolom
# #         column_widths = {
# #             "Tanggal": 100,
# #             "Penghuni": 170,
# #             "Pesan Feedback": 350,
# #             "Rating": 100,
# #         }

# #         for col in columns:
# #             self.tree.heading(col, text=col)
# #             width = column_widths.get(col, 150)
# #             self.tree.column(col, width=width, anchor='center')

# #         # Menyusun tag warna untuk baris
# #         self.tree.tag_configure('evenrow', background='#FFFFFF')
# #         self.tree.tag_configure('oddrow', background='#FAFAFA')

# #         # Menambahkan data ke dalam tabel
# #         for idx, row in enumerate(data):
# #             tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
# #             # Menambahkan kolom aksi
# #             row_with_action = list(row) + ["📝"]
# #             self.tree.insert('', tk.END, values=row_with_action, tags=(tag,))

# # # Menjalankan aplikasi
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     root.geometry("1200x800")
# #     root.title("Feedback Penghuni")

# #     app = FeedbackPenghuni(root, None)
# #     app.pack(fill=tk.BOTH, expand=True)

# #     root.mainloop()

# import tkinter as tk
# from tkinter import ttk, messagebox

# class FeedbackPenghuni(tk.Frame):
#     """Halaman untuk menampilkan feedback penghuni"""
    
#     def __init__(self, parent, controller):
#         super().__init__(parent, bg='white')
#         self.controller = controller
#         self.tree = None
#         self.create_content()
    
#     def create_content(self):
#         """Membuat konten halaman Feedback Penghuni"""
#         print("Membuat konten Feedback Penghuni...")
        
#         # Judul Halaman
#         title = tk.Label(
#             self,
#             text="Record Feedback Penghuni",
#             font=('Arial', 18, 'bold'),
#             bg='white',
#             fg='#2D3142'
#         )
#         title.pack(pady=(30, 20), padx=40, anchor='w')
        
#         # Frame pencarian dan filter
#         self.create_search_filter()

#         # Kontainer untuk tabel feedback penghuni
#         table_outer_frame = tk.Frame(self, bg='#E0E0E0', padx=1, pady=1)
#         table_outer_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 40))

#         # Data feedback penghuni contoh
#         self.data = [
#             ["04/17/23", "A01", "Leslie Alexander", "Saya merasa sangat puas dengan pelayanan Kos Melati, pelayanan sangat lengkap dan rumahnya nyaman serta bersih.", "★★★★★"],
#             ["04/17/23", "A01", "Benjamin Franklin", "Pelayanan Kos ini cukup baik, namun ada beberapa area yang bisa diperbaiki, terutama kebersihan di sekitar.", "★★★★"],
#             ["04/17/23", "A02", "John Doe", "Kamar sangat nyaman dan fasilitas lengkap, saya merasa sangat nyaman tinggal di sini selama beberapa minggu.", "★★★★★"],
#             ["04/17/23", "A03", "Alice Johnson", "Kos ini cukup nyaman, tetapi harga sedikit lebih mahal dibandingkan dengan kos lainnya di daerah ini.", "★★★"],
#         ]

#         # Kolom tabel
#         columns = ["Tanggal", "Penghuni", "Pesan Feedback", "Rating", "Action"]

#         # Membuat Treeview untuk feedback penghuni
#         self.create_table(table_outer_frame, columns, self.data)
    
#     def create_search_filter(self):
#         """Membuat bar pencarian dan tombol filter"""
#         search_frame = tk.Frame(self, bg='white')
#         search_frame.pack(fill=tk.X, padx=40, pady=(0, 10))

#         # Kontainer untuk pencarian dengan border
#         search_container = tk.Frame(search_frame, bg='#F0F0F0', relief='solid', borderwidth=1)
#         search_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

#         # Ikon pencarian (🔍)
#         search_icon = tk.Label(
#             search_container,
#             text="🔍",
#             font=('Arial', 12),
#             bg='#F0F0F0',
#             fg='#666666'
#         )
#         search_icon.pack(side=tk.LEFT, padx=(10, 5))

#         # Kolom pencarian
#         self.search_entry = tk.Entry(
#             search_container,
#             font=('Arial', 11),
#             bg='#F0F0F0',
#             fg='#333333',
#             relief='flat',
#             borderwidth=0
#         )
#         self.search_entry.insert(0, "Search feedback")
#         self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=8)

#         # Placeholder behavior
#         self.search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in())
#         self.search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out())
#         self.search_entry.bind('<KeyRelease>', lambda e: self.on_search())

#         # Tombol filter
#         filter_btn = tk.Button(
#             search_frame,
#             text="Filter ☰",
#             font=('Arial', 11),
#             bg='white',
#             fg='#333333',
#             relief='solid',
#             borderwidth=1,
#             padx=20,
#             pady=6,
#             cursor='hand2',
#             command=self.show_filter
#         )
#         filter_btn.pack(side=tk.RIGHT)

#     def on_search_focus_in(self):
#         """Menghapus placeholder saat fokus"""
#         if self.search_entry.get() == "Search feedback":
#             self.search_entry.delete(0, tk.END)
#             self.search_entry.config(fg='#333333')

#     def on_search_focus_out(self):
#         """Menambahkan placeholder jika kosong"""
#         if not self.search_entry.get():
#             self.search_entry.insert(0, "Search feedback")
#             self.search_entry.config(fg='#999999')

#     def on_search(self):
#         """Memfilter tabel berdasarkan pencarian"""
#         search_text = self.search_entry.get().lower()
#         if search_text == "search feedback":
#             return
        
#         # Menghapus item yang ada
#         for item in self.tree.get_children():
#             self.tree.delete(item)

#         # Menyaring data yang sesuai
#         for idx, row in enumerate(self.data):
#             if any(search_text in str(field).lower() for field in row):
#                 tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
#                 self.tree.insert('', tk.END, values=row, tags=(tag,))

#     def show_filter(self):
#         """Menampilkan filter"""
#         messagebox.showinfo("Filter", "Opsi filter akan datang segera!")

#     def create_table(self, parent, columns, data):
#         """Membuat tabel untuk menampilkan feedback penghuni"""

#         # Style konfigurasi
#         style = ttk.Style()
#         style.theme_use('clam')

#         # Konfigurasi style untuk Treeview
#         style.configure(
#             "Custom.Treeview",
#             background="white",
#             foreground="#333333",
#             rowheight=40,
#             fieldbackground="white",
#             borderwidth=0,
#             font=('Arial', 10)
#         )

#         # Konfigurasi header Treeview
#         style.configure(
#             "Custom.Treeview.Heading",
#             background="#E8D5A8",  # Warna kuning krem seperti di desain
#             foreground="#333333",
#             borderwidth=1,
#             relief="flat",
#             font=('Arial', 10, 'bold')
#         )

#         style.map(
#             "Custom.Treeview.Heading",
#             background=[('active', '#D4C198')]
#         )

#         # Frame tabel
#         table_frame = tk.Frame(parent, bg='white')
#         table_frame.pack(fill=tk.BOTH, expand=True)

#         # Scrollbar
#         scrollbar = ttk.Scrollbar(table_frame)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         # Treeview dengan style kustom
#         self.tree = ttk.Treeview(
#             table_frame, 
#             columns=columns, 
#             show="headings",
#             yscrollcommand=scrollbar.set,
#             style="Custom.Treeview"
#         )
#         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         scrollbar.config(command=self.tree.yview)

#         # Menyusun lebar kolom
#         column_widths = {
#             "Tanggal": 120,
#             "Penghuni": 150,
#             "Pesan Feedback": 250,
#             "Rating": 100,
#             "Action": 100
#         }

#         for col in columns:
#             self.tree.heading(col, text=col)
#             width = column_widths.get(col, 150)
#             self.tree.column(col, width=width, anchor='w')  # Rata kiri untuk "Penghuni" dan "Pesan Feedback"

#         # Menyusun tag warna untuk baris
#         self.tree.tag_configure('evenrow', background='#FFFFFF')
#         self.tree.tag_configure('oddrow', background='#FAFAFA')

#         # Menambahkan data ke dalam tabel
#         for idx, row in enumerate(data):
#             tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
#             # Menambahkan kolom aksi
#             row_with_action = list(row) + ["📝"]
#             item = self.tree.insert('', tk.END, values=row_with_action, tags=(tag,))
#             # Menambahkan event klik pada "📝" untuk melihat detail feedback
#             self.tree.bind('<ButtonRelease-1>', lambda event, item=item: self.view_feedback(event, item))
    
#     def view_feedback(self, event, item):
#         """Menampilkan feedback lengkap dalam jendela baru"""
#         # Ambil seluruh nilai data dari baris yang dipilih
#         values = self.tree.item(item)["values"]
#         feedback = values[2]  # Kolom Pesan Feedback

#         # Membuka jendela pop-up untuk menampilkan feedback lengkap
#         view_window = tk.Toplevel(self)
#         view_window.title("View Feedback")
#         view_window.geometry("500x350")

#         feedback_text = f"""
#         Tanggal         : {values[0]}
#         Penghuni        : {values[1]}
#         Pesan Feedback  : {feedback}
#         Rating          : {values[3]}
#         """

#         label = tk.Label(
#             view_window,
#             text=feedback_text,
#             font=("Arial", 12),
#             wraplength=480,  # Membungkus teks jika terlalu panjang
#             justify="left"
#         )
#         label.pack(padx=10, pady=10)

# # Menjalankan aplikasi
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.geometry("1200x800")
#     root.title("Feedback Penghuni")

#     app = FeedbackPenghuni(root, None)
#     app.pack(fill=tk.BOTH, expand=True)

#     root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox

class FeedbackPenghuni(tk.Frame):
    """Halaman untuk menampilkan feedback penghuni"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.tree = None
        self.create_content()
    
    def create_content(self):
        """Membuat konten halaman Feedback Penghuni"""
        print("Membuat konten Feedback Penghuni...")
        
        # Judul Halaman
        title = tk.Label(
            self,
            text="Record Feedback Penghuni",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2D3142'
        )
        title.pack(pady=(30, 20), padx=40, anchor='w')
        
        # Frame pencarian dan filter
        self.create_search_filter()

        # Kontainer untuk tabel feedback penghuni
        table_outer_frame = tk.Frame(self, bg='#E0E0E0', padx=1, pady=1)
        table_outer_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 40))

        # Data feedback penghuni contoh
        self.data = [
            ["04/17/23", "A01\nLeslie Alexander", "Saya merasa sangat puas dengan pelayanan Kos Melati, pelayanan sangat lengkap dan rumahnya nyaman serta bersih.", "★★★★★"],
            ["04/17/23", "A01\nBenjamin Franklin", "Pelayanan Kos ini cukup baik, namun ada beberapa area yang bisa diperbaiki, terutama kebersihan di sekitar.", "★★★★"],
            ["04/17/23", "A02\nJohn Doe", "Kamar sangat nyaman dan fasilitas lengkap, saya merasa sangat nyaman tinggal di sini selama beberapa minggu.", "★★★★★"],
            ["04/17/23", "A03\nAlice Johnson", "Kos ini cukup nyaman, tetapi harga sedikit lebih mahal dibandingkan dengan kos lainnya di daerah ini.", "★★★"],
        ]

        # Kolom tabel
        columns = ["Tanggal", "Penghuni", "Pesan Feedback", "Rating"]

        # Membuat Treeview untuk feedback penghuni
        self.create_table(table_outer_frame, columns, self.data)
    
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
        self.search_entry.insert(0, "Search feedback")
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
        if self.search_entry.get() == "Search feedback":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='#333333')

    def on_search_focus_out(self):
        """Menambahkan placeholder jika kosong"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search feedback")
            self.search_entry.config(fg='#999999')

    def on_search(self):
        """Memfilter tabel berdasarkan pencarian"""
        search_text = self.search_entry.get().lower()
        if search_text == "search feedback":
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
        """Membuat tabel untuk menampilkan feedback penghuni"""

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
            font=('Arial', 10, 'bold')
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
            "Penghuni": 150,
            "Pesan Feedback": 350,
            "Rating": 100
        }

        for col in columns:
            self.tree.heading(col, text=col)
            width = column_widths.get(col, 150)
            # Hanya kolom "Penghuni" dan "Pesan Feedback" yang rata kiri
            anchor = 'w' if col in ["Penghuni", "Pesan Feedback"] else 'center'
            self.tree.column(col, width=width, anchor=anchor)

        # Menyusun tag warna untuk baris
        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#FAFAFA')

        # Menambahkan data ke dalam tabel
        for idx, row in enumerate(data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            # Menambahkan kolom aksi
            row_with_action = list(row) + ["📝"]
            item = self.tree.insert('', tk.END, values=row_with_action, tags=(tag,))
            # Menambahkan event klik pada "📝" untuk melihat detail feedback
            self.tree.bind('<ButtonRelease-1>', lambda event, item=item: self.view_feedback(event, item))
    
    def view_feedback(self, event, item):
        """Menampilkan feedback lengkap dalam jendela baru"""
        # Ambil seluruh nilai data dari baris yang dipilih
        values = self.tree.item(item)["values"]
        feedback = values[2]  # Kolom Pesan Feedback

        # Membuka jendela pop-up untuk menampilkan feedback lengkap
        view_window = tk.Toplevel(self)
        view_window.title("View Feedback")
        view_window.geometry("500x350")

        feedback_text = f"""
        Tanggal         : {values[0]}
        Penghuni        : {values[1]}
        Pesan Feedback  : {feedback}
        Rating          : {values[3]}
        """

        label = tk.Label(
            view_window,
            text=feedback_text,
            font=("Arial", 12),
            wraplength=480,  # Membungkus teks jika terlalu panjang
            justify="left"
        )
        label.pack(padx=10, pady=10)

# Menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Feedback Penghuni")

    app = FeedbackPenghuni(root, None)
    app.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
