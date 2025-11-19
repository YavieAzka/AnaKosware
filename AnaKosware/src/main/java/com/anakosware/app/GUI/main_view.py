# # Test GUI untuk page daftarkan akun penghuni

# import tkinter as tk
# from tkinter import ttk
# from datetime import datetime
# from tkcalendar import DateEntry
# import re

# class PlaceholderEntry(tk.Entry):
#     """Custom Entry widget with placeholder functionality"""
#     def __init__(self, master=None, placeholder="", color='grey', **kwargs):
#         super().__init__(master, **kwargs)
        
#         self.placeholder = placeholder
#         self.placeholder_color = color
#         self.default_fg_color = self['fg']
        
#         self.bind("<FocusIn>", self._clear_placeholder)
#         self.bind("<FocusOut>", self._add_placeholder)
        
#         self._add_placeholder()
    
#     def _clear_placeholder(self, event=None):
#         if self['fg'] == self.placeholder_color:
#             self.delete(0, tk.END)
#             self['fg'] = self.default_fg_color
    
#     def _add_placeholder(self, event=None):
#         if not self.get():
#             self.insert(0, self.placeholder)
#             self['fg'] = self.placeholder_color


# class Sidebar(tk.Frame):
#     """Sidebar component with logo and navigation menu"""
#     def __init__(self, parent):
#         super().__init__(parent, bg='#D4C5A0', width=250)
#         self.pack_propagate(False)
        
#         # Logo section
#         self.create_logo()
        
#         # Navigation menu
#         self.create_navigation()
    
#     def create_logo(self):
#         """Create logo section at top of sidebar"""
#         logo_frame = tk.Frame(self, bg='#D4C5A0')
#         logo_frame.pack(pady=30, padx=20)
        
#         logo_label = tk.Label(
#             logo_frame,
#             text="AnaKosware",
#             font=('Arial', 20, 'bold'),
#             bg='#D4C5A0',
#             fg='#5D4E37'
#         )
#         logo_label.pack()
        
#         subtitle = tk.Label(
#             logo_frame,
#             text="Rental Management",
#             font=('Arial', 9),
#             bg='#D4C5A0',
#             fg='#7D6E57'
#         )
#         subtitle.pack()
    
#     def create_navigation(self):
#         """Create navigation menu items"""
#         menu_items = [
#             ("🏠", "Dashboard", False),
#             ("👤", "Daftar Akun Penghuni", True),
#             ("📊", "Riwayat Transaksi", False),
#             ("💬", "Feedback Record", False),
#             ("🚪", "Logout", False)
#         ]
        
#         for icon, text, is_active in menu_items:
#             self.create_menu_item(icon, text, is_active)
    
#     def create_menu_item(self, icon, text, is_active=False):
#         """Create individual menu item with hover effect"""
#         bg_color = '#B8A67D' if is_active else '#D4C5A0'
        
#         item_frame = tk.Frame(self, bg=bg_color, cursor='hand2')
#         item_frame.pack(fill=tk.X, pady=2, padx=15)
        
#         content_frame = tk.Frame(item_frame, bg=bg_color)
#         content_frame.pack(fill=tk.X, pady=12, padx=15)
        
#         icon_label = tk.Label(
#             content_frame,
#             text=icon,
#             font=('Arial', 14),
#             bg=bg_color,
#             fg='#5D4E37'
#         )
#         icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
#         text_label = tk.Label(
#             content_frame,
#             text=text,
#             font=('Arial', 11, 'bold' if is_active else 'normal'),
#             bg=bg_color,
#             fg='#5D4E37'
#         )
#         text_label.pack(side=tk.LEFT)
        
#         # Hover effects
#         if not is_active:
#             def on_enter(e):
#                 item_frame.config(bg='#C4B590')
#                 content_frame.config(bg='#C4B590')
#                 icon_label.config(bg='#C4B590')
#                 text_label.config(bg='#C4B590')
            
#             def on_leave(e):
#                 item_frame.config(bg='#D4C5A0')
#                 content_frame.config(bg='#D4C5A0')
#                 icon_label.config(bg='#D4C5A0')
#                 text_label.config(bg='#D4C5A0')
            
#             item_frame.bind('<Enter>', on_enter)
#             item_frame.bind('<Leave>', on_leave)
#             content_frame.bind('<Enter>', on_enter)
#             content_frame.bind('<Leave>', on_leave)


# class Header(tk.Frame):
#     """Header component with title and user profile"""
#     def __init__(self, parent):
#         super().__init__(parent, bg='white', height=80)
#         self.pack_propagate(False)
        
#         # Title on left
#         title_label = tk.Label(
#             self,
#             text="AnaKosware App",
#             font=('Arial', 18, 'bold'),
#             bg='white',
#             fg='#333333'
#         )
#         title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
#         # User profile on right
#         self.create_user_profile()
    
#     def create_user_profile(self):
#         """Create user profile dropdown area"""
#         profile_frame = tk.Frame(self, bg='white')
#         profile_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
#         # Avatar circle
#         avatar = tk.Label(
#             profile_frame,
#             text="👤",
#             font=('Arial', 24),
#             bg='white'
#         )
#         avatar.pack(side=tk.LEFT, padx=(0, 10))
        
#         # User info
#         info_frame = tk.Frame(profile_frame, bg='white')
#         info_frame.pack(side=tk.LEFT)
        
#         name_label = tk.Label(
#             info_frame,
#             text="Ibu Kos",
#             font=('Arial', 12, 'bold'),
#             bg='white',
#             fg='#333333'
#         )
#         name_label.pack(anchor='w')
        
#         role_label = tk.Label(
#             info_frame,
#             text="Pemilik Kos",
#             font=('Arial', 9),
#             bg='white',
#             fg='#666666'
#         )
#         role_label.pack(anchor='w')
        
#         # Dropdown arrow
#         dropdown_arrow = tk.Label(
#             profile_frame,
#             text="▼",
#             font=('Arial', 8),
#             bg='white',
#             fg='#666666',
#             cursor='hand2'
#         )
#         dropdown_arrow.pack(side=tk.LEFT, padx=(10, 0))


# class RegisterTenantForm(tk.Frame):
#     """Registration form for new tenants"""
#     def __init__(self, parent):
#         super().__init__(parent, bg='white')
        
#         # Form title
#         title_label = tk.Label(
#             self,
#             text="Daftar Akun Penghuni Baru",
#             font=('Arial', 16, 'bold'),
#             bg='white',
#             fg='#333333'
#         )
#         title_label.pack(pady=(20, 20), padx=30, anchor='w')
        
#         # Form container with dashed border
#         self.create_form_container()
    
#     def create_form_container(self):
#         """Create the main form container with dashed border"""
#         # Container frame
#         container = tk.Frame(self, bg='white', highlightbackground='#D8BFD8', 
#                            highlightthickness=2, relief='solid')
#         container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
#         # Inner padding frame
#         inner_frame = tk.Frame(container, bg='white')
#         inner_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
#         # Create form fields
#         self.create_form_fields(inner_frame)
    
#     def create_form_fields(self, parent):
#         """Create all form input fields"""
#         # Nama Penghuni
#         self.create_input_field(parent, "Nama Penghuni", 
#                                placeholder="Masukkan nama lengkap penghuni", row=0)
        
#         # Row with Date and Phone
#         date_phone_frame = tk.Frame(parent, bg='white')
#         date_phone_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)
#         date_phone_frame.columnconfigure(0, weight=1)
#         date_phone_frame.columnconfigure(1, weight=1)
        
#         # Tanggal Masuk
#         date_frame = tk.Frame(date_phone_frame, bg='white')
#         date_frame.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        
#         date_label = tk.Label(
#             date_frame,
#             text="Tanggal Masuk",
#             font=('Arial', 10),
#             bg='white',
#             fg='#555555'
#         )
#         date_label.pack(anchor='w', pady=(0, 5))
        
#         self.date_entry = DateEntry(
#             date_frame,
#             width=25,
#             background='#FF9966',
#             foreground='white',
#             borderwidth=1,
#             date_pattern='dd/mm/yyyy',
#             font=('Arial', 10)
#         )
#         self.date_entry.pack(fill=tk.X)
        
#         # Nomor Telepon
#         phone_frame = tk.Frame(date_phone_frame, bg='white')
#         phone_frame.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        
#         phone_label = tk.Label(
#             phone_frame,
#             text="Nomor Telepon Penghuni",
#             font=('Arial', 10),
#             bg='white',
#             fg='#555555'
#         )
#         phone_label.pack(anchor='w', pady=(0, 5))
        
#         phone_input_frame = tk.Frame(phone_frame, bg='white')
#         phone_input_frame.pack(fill=tk.X)
        
#         prefix_label = tk.Label(
#             phone_input_frame,
#             text="+62",
#             font=('Arial', 10),
#             bg='#F5F5F5',
#             fg='#555555',
#             padx=10,
#             relief='solid',
#             borderwidth=1
#         )
#         prefix_label.pack(side=tk.LEFT)
        
#         self.phone_entry = PlaceholderEntry(
#             phone_input_frame,
#             placeholder="8123456789",
#             font=('Arial', 10),
#             relief='solid',
#             borderwidth=1,
#             bg='#F5F5F5'
#         )
#         self.phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
#         # Nomor Kamar
#         self.create_input_field(parent, "Nomor Kamar Penghuni", 
#                                placeholder="Contoh: 101, 202, A1", row=2)
        
#         # Harga Kamar
#         self.create_input_field(parent, "Harga Kamar Penghuni", 
#                                placeholder="Rp. 1.500.000", row=3)
        
#         # Username
#         self.create_input_field(parent, "Username Akun Penghuni", 
#                                placeholder="Masukkan username untuk login", row=4)
        
#         # Password
#         self.create_input_field(parent, "Password Penghuni", 
#                                placeholder="Masukkan password", row=5, is_password=True)
        
#         # Submit button
#         self.create_submit_button(parent)
    
#     def create_input_field(self, parent, label_text, placeholder="", row=0, is_password=False):
#         """Create a labeled input field"""
#         label = tk.Label(
#             parent,
#             text=label_text,
#             font=('Arial', 10),
#             bg='white',
#             fg='#555555'
#         )
#         label.grid(row=row, column=0, sticky='w', pady=(10, 5), columnspan=2)
        
#         if is_password:
#             entry = PlaceholderEntry(
#                 parent,
#                 placeholder=placeholder,
#                 font=('Arial', 10),
#                 relief='solid',
#                 borderwidth=1,
#                 bg='#F5F5F5',
#                 show='•'
#             )
#         else:
#             entry = PlaceholderEntry(
#                 parent,
#                 placeholder=placeholder,
#                 font=('Arial', 10),
#                 relief='solid',
#                 borderwidth=1,
#                 bg='#F5F5F5'
#             )
        
#         entry.grid(row=row, column=1, sticky='ew', pady=(10, 5))
#         parent.columnconfigure(1, weight=1)
        
#         return entry
    
#     def create_submit_button(self, parent):
#         """Create the submit button with hover effect"""
#         button_frame = tk.Frame(parent, bg='white')
#         button_frame.grid(row=6, column=0, columnspan=2, pady=(30, 10))
        
#         submit_btn = tk.Button(
#             button_frame,
#             text="Daftarkan Akun Penghuni",
#             font=('Arial', 12, 'bold'),
#             bg='#FF9966',
#             fg='white',
#             relief='flat',
#             cursor='hand2',
#             padx=40,
#             pady=12,
#             command=self.submit_registration
#         )
#         submit_btn.pack()
        
#         # Hover effects
#         def on_enter(e):
#             submit_btn.config(bg='#FF8C4D')
        
#         def on_leave(e):
#             submit_btn.config(bg='#FF9966')
        
#         submit_btn.bind('<Enter>', on_enter)
#         submit_btn.bind('<Leave>', on_leave)
    
#     def submit_registration(self):
#         """Handle form submission"""
#         print("Registration submitted!")
#         # Add validation and submission logic here


# class AnaKoswareApp(tk.Tk):
#     """Main application window"""
#     def __init__(self):
#         super().__init__()
        
#         # Window configuration
#         self.title("AnaKosware - Tenant Registration")
#         self.geometry("1280x800")
#         self.configure(bg='white')
        
#         # Make window non-resizable for consistent layout
#         self.resizable(False, False)
        
#         # Create main layout
#         self.create_layout()
    
#     def create_layout(self):
#         """Create the main application layout"""
#         # Sidebar (left side, ~20% width)
#         sidebar = Sidebar(self)
#         sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
#         # Main content area (right side, ~80% width)
#         main_content = tk.Frame(self, bg='white')
#         main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
#         # Header
#         header = Header(main_content)
#         header.pack(fill=tk.X)
        
#         # Separator line
#         separator = tk.Frame(main_content, bg='#E0E0E0', height=1)
#         separator.pack(fill=tk.X)
        
#         # Registration form
#         form = RegisterTenantForm(main_content)
#         form.pack(fill=tk.BOTH, expand=True)


# if __name__ == "__main__":
#     app = AnaKoswareApp()
#     app.mainloop()

"""
Main application controller for AnaKosware.
"""
"""
Main application controller for AnaKosware.
"""
import tkinter as tk
from tkinter import messagebox

# Import components
from components.pemilik.sidebar import Sidebar
from components.pemilik.header import Header

# Import pages
from pages.pemilik.daftar_akun_penghuni import DaftarAkunPenghuni


class AnaKoswareApp(tk.Tk):
    """Main application window and controller"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("AnaKosware - Sistem Manajemen Kos")
        self.geometry("1280x800")
        self.configure(bg='white')
        self.resizable(False, False)
        
        # Current user info
        self.current_user_name = "Ibu Kos"
        self.current_user_role = "Pemilik Kos"
        
        # Create main layout
        self.create_layout()
        
        # Show initial page
        self.show_register_tenant()
    
    def create_layout(self):
        """Create main application layout"""
        # Main container
        self.main_container = tk.Frame(self, bg='white')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(
            self.main_container,
            on_menu_click=self.handle_navigation,
            active_menu='register_tenant'
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Content area (right side)
        self.content_area = tk.Frame(self.main_container, bg='white')
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header
        self.header = Header(
            self.content_area,
            user_name=self.current_user_name,
            user_role=self.current_user_role
        )
        self.header.pack(fill=tk.X)
        
        # Page container
        self.page_container = tk.Frame(self.content_area, bg='white')
        self.page_container.pack(fill=tk.BOTH, expand=True)
    
    def handle_navigation(self, menu_id):
        """Handle sidebar menu clicks"""
        if menu_id == 'dashboard':
            self.show_dashboard()
        elif menu_id == 'register_tenant':
            self.show_register_tenant()
        elif menu_id == 'transaction':
            self.show_transaction()
        elif menu_id == 'feedback':
            self.show_feedback()
        elif menu_id == 'logout':
            self.handle_logout()
        
        # Update sidebar active state
        self.update_sidebar(menu_id)
    
    def update_sidebar(self, active_menu):
        """Update sidebar to show active menu"""
        self.sidebar.destroy()
        self.sidebar = Sidebar(
            self.main_container,
            on_menu_click=self.handle_navigation,
            active_menu=active_menu
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
    
    def clear_page(self):
        """Clear current page content"""
        for widget in self.page_container.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard page"""
        self.clear_page()
        self.title("AnaKosware - Dashboard")
        
        # TODO: Import dan tampilkan DashboardView
        placeholder = tk.Label(
            self.page_container,
            text="Dashboard Page\n(Coming Soon)",
            font=('Arial', 24),
            bg='white',
            fg='#999999'
        )
        placeholder.pack(expand=True)
    
    def show_register_tenant(self):
        """Show register tenant page"""
        self.clear_page()
        self.title("AnaKosware - Daftar Akun Penghuni")
        
        page = DaftarAkunPenghuni(self.page_container, self)
        page.pack(fill=tk.BOTH, expand=True)
    
    def show_transaction(self):
        """Show transaction history page"""
        self.clear_page()
        self.title("AnaKosware - Riwayat Transaksi")
        
        # TODO: Import dan tampilkan TransactionView
        placeholder = tk.Label(
            self.page_container,
            text="Riwayat Transaksi Page\n(Coming Soon)",
            font=('Arial', 24),
            bg='white',
            fg='#999999'
        )
        placeholder.pack(expand=True)
    
    def show_feedback(self):
        """Show feedback page"""
        self.clear_page()
        self.title("AnaKosware - Feedback Record")
        
        # TODO: Import dan tampilkan FeedbackView
        placeholder = tk.Label(
            self.page_container,
            text="Feedback Record Page\n(Coming Soon)",
            font=('Arial', 24),
            bg='white',
            fg='#999999'
        )
        placeholder.pack(expand=True)
    
    def handle_logout(self):
        """Handle logout"""
        response = messagebox.askyesno(
            "Logout",
            "Apakah Anda yakin ingin logout?"
        )
        
        if response:
            print("Logging out...")
            self.destroy()


if __name__ == "__main__":
    app = AnaKoswareApp()
    app.mainloop()