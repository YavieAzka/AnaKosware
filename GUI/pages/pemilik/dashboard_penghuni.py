"""
Dashboard Penghuni untuk AnaKosware application.
"""
import tkinter as tk
from tkinter import ttk, messagebox


class DashboardPenghuni(tk.Frame):
    """Dashboard untuk menampilkan daftar penghuni"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.tree = None
        self.create_content()
    
    def create_content(self):
        """Create page content"""
        print("Membuat konten Dashboard...")
        
        # Page title
        title = tk.Label(
            self,
            text="Dashboard Penghuni",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2D3142'
        )
        title.pack(pady=(30, 20), padx=40, anchor='w')
        
        # Search and Filter Frame
        self.create_search_filter()
        
        print("Membuat tabel penghuni...")
        
        # Table container with border
        table_outer_frame = tk.Frame(self, bg='#E0E0E0', padx=1, pady=1)
        table_outer_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 40))
        
        # Example data for the table
        self.data = [
            ["A01", "user_ben", "Benjamin Franklin", "04/17/23", "Rp. 1.000.000", "Aktif"],
            ["A01", "user_john", "John Doe", "04/18/23", "Rp. 950.000", "Aktif"],
            ["A02", "user_alice", "Alice Johnson", "04/15/23", "Rp. 1.050.000", "Nonaktif"],
            ["A03", "user_bob", "Bob Smith", "04/10/23", "Rp. 1.100.000", "Aktif"],
            ["A04", "user_carol", "Carol White", "04/12/23", "Rp. 980.000", "Nonaktif"],
        ]
        
        columns = ["Nomor Kamar", "Username", "Nama Lengkap", "Tanggal Masuk", "Harga Kamar", "Status Akun", "Action"]
        
        self.create_table(table_outer_frame, columns, self.data)
        
        print("Dashboard berhasil dibuat!")
    
    def create_search_filter(self):
        """Create search bar and filter button"""
        search_frame = tk.Frame(self, bg='white')
        search_frame.pack(fill=tk.X, padx=40, pady=(0, 10))
        
        # Search container with border
        search_container = tk.Frame(search_frame, bg='#F0F0F0', relief='solid', borderwidth=1)
        search_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Search icon (🔍)
        search_icon = tk.Label(
            search_container,
            text="🔍",
            font=('Arial', 12),
            bg='#F0F0F0',
            fg='#666666'
        )
        search_icon.pack(side=tk.LEFT, padx=(10, 5))
        
        # Search entry
        self.search_entry = tk.Entry(
            search_container,
            font=('Arial', 11),
            bg='#F0F0F0',
            fg='#333333',
            relief='flat',
            borderwidth=0
        )
        self.search_entry.insert(0, "Search penghuni")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=8)
        
        # Placeholder behavior
        self.search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in())
        self.search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out())
        self.search_entry.bind('<KeyRelease>', lambda e: self.on_search())
        
        # Filter button
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
        """Clear placeholder on focus"""
        if self.search_entry.get() == "Search penghuni":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='#333333')
    
    def on_search_focus_out(self):
        """Add placeholder if empty"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search penghuni")
            self.search_entry.config(fg='#999999')
    
    def on_search(self):
        """Filter table based on search"""
        search_text = self.search_entry.get().lower()
        if search_text == "search penghuni":
            return
        
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Re-insert filtered data
        for idx, row in enumerate(self.data):
            # Search in all fields
            if any(search_text in str(field).lower() for field in row):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert('', tk.END, values=row, tags=(tag,))
    
    def show_filter(self):
        """Show filter options"""
        messagebox.showinfo("Filter", "Filter options coming soon!")
    
    def create_table(self, parent, columns, data):
        """Create table to show tenant data with proper styling"""
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Treeview style
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground="#333333",
            rowheight=40,
            fieldbackground="white",
            borderwidth=0,
            font=('Arial', 10)
        )
        
        # Configure Treeview heading (header) style
        style.configure(
            "Custom.Treeview.Heading",
            background="#E8D5A8",  # Kuning krem seperti di desain
            foreground="#333333",
            borderwidth=1,
            relief="flat",
            font=('Arial', 10, 'bold')
        )
        
        style.map(
            "Custom.Treeview.Heading",
            background=[('active', '#D4C198')]
        )
        
        # Table frame
        table_frame = tk.Frame(parent, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview with custom style
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            yscrollcommand=scrollbar.set,
            style="Custom.Treeview"
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.tree.yview)
        
        # Set column headers and widths
        column_widths = {
            "Nomor Kamar": 120,
            "Username": 120,
            "Nama Lengkap": 180,
            "Tanggal Masuk": 120,
            "Harga Kamar": 130,
            "Status Akun": 120,
            "Action": 100
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            width = column_widths.get(col, 150)
            self.tree.column(col, width=width, anchor='center')
        
        # Configure row colors
        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#FAFAFA')
        
        # Insert data into the table
        for idx, row in enumerate(data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            # Add action placeholder
            row_with_action = list(row) + ["📝"]
            self.tree.insert('', tk.END, values=row_with_action, tags=(tag,))
        
        # Bind click events
        self.tree.bind('<Double-1>', lambda e: self.view_selected())
        self.tree.bind('<Button-1>', self.on_row_click)
    
    def on_row_click(self, event):
        """Handle click on table row"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            selected = self.tree.selection()
            
            if selected:
                # Check if clicked on Action column (last column)
                col_index = int(column.replace('#', '')) - 1
                if col_index == 6:  # Action column
                    # Show action menu
                    self.show_action_menu(event)
    
    def show_action_menu(self, event):
        """Show action menu on Action column click"""
        # Create popup menu
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="👁️ View Detail", command=self.view_selected)
        menu.add_command(label="✏️     Edit", command=self.edit_selected)
        menu.add_separator()
        menu.add_command(label="🗑️ Delete", command=self.delete_selected)
        
        # Show menu at cursor position
        menu.post(event.x_root, event.y_root)
    
    def view_selected(self):
        """View selected tenant details"""
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih penghuni yang ingin dilihat!")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        # Show details in message box
        details = f"""
            Detail Penghuni:

            Nomor Kamar    : {values[0]}
            Username       : {values[1]}
            Nama Lengkap   : {values[2]}
            Tanggal Masuk  : {values[3]}
            Harga Kamar    : {values[4]}
            Status Akun    : {values[5]}
                    """
        
        messagebox.showinfo("Detail Penghuni", details)
    
    def edit_selected(self):
        """Edit selected tenant"""
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih penghuni yang ingin diedit!")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        # TODO: Buka halaman edit
        messagebox.showinfo("Edit", f"Edit penghuni: {values[2]}\n(Fitur coming soon)")
    
    def delete_selected(self):
        """Delete selected tenant"""
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih penghuni yang ingin dihapus!")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        # Confirm deletion
        response = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus penghuni:\n{values[2]}?"
        )
        
        if response:
            self.tree.delete(selected[0])
            messagebox.showinfo("Sukses", "Penghuni berhasil dihapus!")


# Test standalone
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Dashboard Penghuni")
    
    app = DashboardPenghuni(root, None)
    app.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()
