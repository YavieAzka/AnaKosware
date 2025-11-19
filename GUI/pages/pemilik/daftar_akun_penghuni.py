"""
Daftar Akun Penghuni page for AnaKosware application.
"""
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sys
import os

from components.custom_widgets import PlaceholderEntry, StyledButton

class DaftarAkunPenghuni(tk.Frame):
    """Page untuk daftarkan akun baru penghuni"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        
        self.create_content()
    
    def create_content(self):
        """Create page content"""
        # Page title
        title = tk.Label(
            self,
            text="Daftar Akun Penghuni Baru",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#2D3142'
        )
        title.pack(pady=(30, 20), padx=40, anchor='w')
        
        # Form container with dashed border
        self.create_form_container()
    
    def create_form_container(self):
        """Create form container with dashed border"""
        # Outer frame for dashed border effect
        border_frame = tk.Frame(self, bg='white')
        border_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 40))
        
        # Canvas for dashed border
        canvas = tk.Canvas(border_frame, bg='white', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Inner form frame
        form_frame = tk.Frame(canvas, bg='white')
        form_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.96, relheight=0.94)
        
        # Draw dashed rectangle
        canvas.update()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        self.draw_dashed_rectangle(canvas, 10, 10, width-10, height-10, '#D8BFD8', 3, 10)
        
        # Create form fields
        self.create_form_fields(form_frame)
    
    def draw_dashed_rectangle(self, canvas, x1, y1, x2, y2, color, width, dash_length):
        """Draw a dashed rectangle on canvas"""
        # Top
        for x in range(x1, x2, dash_length * 2):
            canvas.create_line(x, y1, min(x + dash_length, x2), y1, fill=color, width=width)
        # Bottom
        for x in range(x1, x2, dash_length * 2):
            canvas.create_line(x, y2, min(x + dash_length, x2), y2, fill=color, width=width)
        # Left
        for y in range(y1, y2, dash_length * 2):
            canvas.create_line(x1, y, x1, min(y + dash_length, y2), fill=color, width=width)
        # Right
        for y in range(y1, y2, dash_length * 2):
            canvas.create_line(x2, y, x2, min(y + dash_length, y2), fill=color, width=width)
    
    def create_form_fields(self, parent):
        """Create all form input fields"""
        # Nama Penghuni
        self.create_label(parent, "Nama Penghuni")
        self.nama_entry = PlaceholderEntry(
            parent,
            placeholder="Masukkan Nama Penghuni",
            font=('Arial', 11),
            bg='#F5F5F5',
            relief='solid',
            borderwidth=1
        )
        self.nama_entry.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        # Tanggal Masuk & Nomor Telepon (same row)
        row_frame = tk.Frame(parent, bg='white')
        row_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        # Tanggal Masuk (left side)
        left_frame = tk.Frame(row_frame, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_label(left_frame, "Tanggal Masuk")
        date_container = tk.Frame(left_frame, bg='white')
        date_container.pack(fill=tk.X, padx=40) 

        self.date_entry = DateEntry(
            left_frame,
            width=30,
            background='#FF9966',
            foreground='white',
            borderwidth=1,
            date_pattern='dd/mm/yyyy',
            font=('Arial', 11)
        )
        self.date_entry.pack(fill=tk.X, ipady=6)
        
        # Nomor Telepon (right side)
        right_frame = tk.Frame(row_frame, bg='white')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_label(right_frame, "Nomor Telepon Penghuni")
        phone_frame = tk.Frame(right_frame, bg='white')
        phone_frame.pack(fill=tk.X)
        
        # +62 prefix
        prefix = tk.Label(
            phone_frame,
            text="+62",
            font=('Arial', 11),
            bg='#F5F5F5',
            fg='#666666',
            relief='solid',
            borderwidth=1
        )
        prefix.pack(side=tk.LEFT, ipady=6, ipadx=10)
        
        self.phone_entry = PlaceholderEntry(
            phone_frame,
            placeholder="Masukkan no telepon ( ex : 8123456789)",
            font=('Arial', 11),
            bg='#F5F5F5',
            relief='solid',
            borderwidth=1
        )
        self.phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(5,0))
        
        # Nomor Kamar Penghuni
        self.create_label(parent, "Nomor Kamar Penghuni")
        self.kamar_entry = PlaceholderEntry(
            parent,
            placeholder="Masukkan Nomor Kamar  Penghuni",
            font=('Arial', 11),
            bg='#F5F5F5',
            relief='solid',
            borderwidth=1
        )
        self.kamar_entry.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        # Harga Kamar Penghuni
        self.create_label(parent, "Harga Kamar Penghuni")
        self.harga_entry = PlaceholderEntry(
            parent,
            placeholder="Masukkan Harga Kamar perbulan penghuni (Rp.)",
            font=('Arial', 11),
            bg='#F5F5F5',
            relief='solid',
            borderwidth=1
        )
        self.harga_entry.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        # Username Akun Penghuni
        self.create_label(parent, "Username Akun Penghuni")
        self.username_entry = PlaceholderEntry(
            parent,
            placeholder="Masukkan Username Penghuni",
            font=('Arial', 11),
            bg='#F5F5F5',
            relief='solid',
            borderwidth=1
        )
        self.username_entry.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        # Password Penghuni
        self.create_label(parent, "Password Penghuni")
        self.password_entry = PlaceholderEntry(
            parent,
            placeholder="Masukkan Password Penghuni",
            font=('Arial', 11),
            bg='#F5F5F5',
            relief='solid',
            borderwidth=1,
            show='•'
        )
        self.password_entry.pack(fill=tk.X, padx=40, pady=(0, 30))
        
        # Submit button
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(pady=(10, 20))
        
        submit_btn = StyledButton(
            button_frame,
            text="Daftarkan Akun Penghuni",
            font=('Arial', 12, 'bold'),
            bg='#FF9966',
            fg='white',
            hover_bg='#FF8C4D',
            padx=50,
            pady=12,
            command=self.submit_form
        )
        submit_btn.pack()
    
    def create_label(self, parent, text):
        """Create a field label"""
        label = tk.Label(
            parent,
            text=text,
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#2D3142'
        )
        label.pack(anchor='w', padx=40, pady=(0, 8))
    
    def submit_form(self):
        """Handle form submission"""
        # Get values
        data = {
            'nama': self.nama_entry.get_value(),
            'tanggal_masuk': self.date_entry.get_date().strftime('%d/%m/%Y'),
            'telepon': self.phone_entry.get_value(),
            'nomor_kamar': self.kamar_entry.get_value(),
            'harga': self.harga_entry.get_value(),
            'username': self.username_entry.get_value(),
            'password': self.password_entry.get_value()
        }
        
        # Validate
        if not self.validate_form(data):
            return
        
        # Save (implement database save here)
        print("Form Data:", data)
        
        # Show success message
        messagebox.showinfo(
            "Sukses",
            f"Akun penghuni atas nama {data['nama']} berhasil didaftarkan!"
        )
        
        # Clear form
        self.clear_form()
    
    def validate_form(self, data):
        """Validate form data"""
        # Check empty fields
        for field, value in data.items():
            if not value or value.strip() == '':
                messagebox.showerror(
                    "Error",
                    f"Field {field.replace('_', ' ').title()} harus diisi!"
                )
                return False
        
        # Validate phone
        if not data['telepon'].isdigit():
            messagebox.showerror("Error", "Nomor telepon harus berupa angka!")
            return False
        
        if len(data['telepon']) < 9:
            messagebox.showerror("Error", "Nomor telepon minimal 9 digit!")
            return False
        
        # Validate username
        if ' ' in data['username']:
            messagebox.showerror("Error", "Username tidak boleh mengandung spasi!")
            return False
        
        # Validate password
        if len(data['password']) < 6:
            messagebox.showerror("Error", "Password minimal 6 karakter!")
            return False
        
        return True
    
    def clear_form(self):
        """Clear all form fields"""
        self.nama_entry.delete(0, tk.END)
        self.nama_entry._add_placeholder()
        
        self.phone_entry.delete(0, tk.END)
        self.phone_entry._add_placeholder()
        
        self.kamar_entry.delete(0, tk.END)
        self.kamar_entry._add_placeholder()
        
        self.harga_entry.delete(0, tk.END)
        self.harga_entry._add_placeholder()
        
        self.username_entry.delete(0, tk.END)
        self.username_entry._add_placeholder()
        
        self.password_entry.delete(0, tk.END)
        self.password_entry._add_placeholder()