"""
Main application (pemilik view) controller for AnaKosware.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import tkinter as tk
from tkinter import messagebox

# Import components
from components.pemilik.sidebar import Sidebar
from components.pemilik.header import Header

# Import pages
from pages.pemilik.daftar_akun_penghuni import DaftarAkunPenghuni


class MainViewPemilik(tk.Tk):
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
        
        print("Dashboard sedang dimuat...")

        # Import dan tampilkan DashboardPenghuni
        from pages.pemilik.dashboard import DashboardPenghuni
        page = DashboardPenghuni(self.page_container, self)
        page.pack(fill=tk.BOTH, expand=True)
    
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
    app = MainViewPemilik()
    app.mainloop()
