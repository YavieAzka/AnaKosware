"""
Sidebar component for AnaKosware application.
"""
from PIL import Image, ImageTk
import os
import tkinter as tk



class Sidebar(tk.Frame):
    """Reusable sidebar with navigation menu"""
    
    def __init__(self, parent, on_menu_click=None, active_menu='dashboard'):
            super().__init__(parent, bg='#EFE5B7', width=250)
            self.pack_propagate(False)
            
            self.on_menu_click = on_menu_click
            self.active_menu = active_menu
            
            self.create_logo()
            self.create_navigation()
            self.create_logout()
        
    def create_logo(self):
        """Create logo section at top"""

        logo_frame = tk.Frame(self, bg='#EFE5B7')
        logo_frame.pack(pady=(40, 40))

        # Load logo image
        logo_path = os.path.join("assets", "image", "AnaKosware Logo.png")

        # Open and resize
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((180, 180), Image.LANCZOS)

        # Convert to PhotoImage
        self.logo_photo = ImageTk.PhotoImage(logo_img)

        # Display the image
        logo_label = tk.Label(logo_frame, image=self.logo_photo, bg='#EFE5B7')
        logo_label.pack()

        # Logo text
        # logo_text = tk.Label(
        #     logo_frame,
        #     text="anakosware",
        #     font=('Arial', 12, 'bold'),
        #     bg='#EFE5B7',
        #     fg='#2D3142'
        # )
        # logo_text.pack()
    
    def create_navigation(self):
        """Create navigation menu items"""
        menu_items = [
            ("🏠", "Dashboard", "dashboard"),
            ("👤", "Daftar Akun Penghuni", "register_tenant"),
            ("📊", "Riwayat Transaksi", "transaction"),
            ("👍", "Feedback Record", "feedback")
        ]
        
        for icon, text, menu_id in menu_items:
            self.create_menu_item(icon, text, menu_id)
    
    def create_menu_item(self, icon, text, menu_id):
        """Create individual menu item"""
        is_active = (menu_id == self.active_menu)
        
        # Container with padding
        container = tk.Frame(self, bg='#EFE5B7')
        container.pack(fill=tk.X, padx=10, pady=0)
        
        # Menu item frame
        bg_color = 'white' if is_active else '#EFE5B7'
        item_frame = tk.Frame(container, bg=bg_color, cursor='hand2')
        item_frame.pack(fill=tk.X, pady=1)
        
        # Add rounded effect for active item
        if is_active:
            item_frame.config(relief='flat')
        
        # Content frame
        content = tk.Frame(item_frame, bg=bg_color)
        content.pack(fill=tk.X, padx=12, pady=5)
        
        # Icon
        icon_label = tk.Label(
            content,
            text=icon,
            font=('Arial', 14),
            bg=bg_color,
            fg='#2D3142'
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Text
        text_label = tk.Label(
            content,
            text=text,
            font=('Arial', 10, 'bold' if is_active else 'normal'),
            bg=bg_color,
            fg='#2D3142'
        )
        text_label.pack(side=tk.LEFT)
        
        # Click handler
        if self.on_menu_click:
            def click(e):
                self.on_menu_click(menu_id)
            
            item_frame.bind('<Button-1>', click)
            content.bind('<Button-1>', click)
            icon_label.bind('<Button-1>', click)
            text_label.bind('<Button-1>', click)
        
        # Hover effect for inactive items
        if not is_active:
            def on_enter(e):
                item_frame.config(bg='#DCC9A0')
                content.config(bg='#DCC9A0')
                icon_label.config(bg='#DCC9A0')
                text_label.config(bg='#DCC9A0')
            
            def on_leave(e):
                item_frame.config(bg='#EFE5B7')
                content.config(bg='#EFE5B7')
                icon_label.config(bg='#EFE5B7')
                text_label.config(bg='#EFE5B7')
            
            item_frame.bind('<Enter>', on_enter)
            item_frame.bind('<Leave>', on_leave)
            content.bind('<Enter>', on_enter)
            content.bind('<Leave>', on_leave)
    
    def create_logout(self):
        """Create logout button at bottom"""
        # Spacer to push logout to bottom
        spacer = tk.Frame(self, bg='#EFE5B7')
        spacer.pack(fill=tk.BOTH, expand=True)
        
        # Logout item
        logout_container = tk.Frame(self, bg='#EFE5B7')
        logout_container.pack(fill=tk.X, padx=15, pady=3)
        
        logout_frame = tk.Frame(logout_container, bg='#EFE5B7', cursor='hand2')
        logout_frame.pack(fill=tk.X, pady=5)
        
        content = tk.Frame(logout_frame, bg='#EFE5B7')
        content.pack(fill=tk.X, padx=15, pady=10)
        
        icon = tk.Label(content, text="🚪", font=('Arial', 14), 
                       bg='#EFE5B7', fg='#2D3142')
        icon.pack(side=tk.LEFT, padx=(0, 10))
        
        text = tk.Label(content, text="Logout", font=('Arial', 10),
                       bg='#EFE5B7', fg='#2D3142')
        text.pack(side=tk.LEFT)
        
        if self.on_menu_click:
            def logout_click(e):
                self.on_menu_click('logout')
            
            logout_frame.bind('<Button-1>', logout_click)
            content.bind('<Button-1>', logout_click)
            icon.bind('<Button-1>', logout_click)
            text.bind('<Button-1>', logout_click)