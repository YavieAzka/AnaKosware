"""
Header component for AnaKosware application.
"""
import tkinter as tk


class Header(tk.Frame):
    """Reusable header with title and user profile"""
    
    # def __init__(self, parent, user_name="Ibu Kos", user_role="Pemilik Kos"):
    #     super().__init__(parent, bg='#FCF9EA', height=100)
    #     self.pack(fill=tk.X)
    #     self.pack_propagate(False)
        
    #     self.user_name = user_name
    #     self.user_role = user_role
        
    #     self.create_title()
    #     self.create_user_profile()
        
    #     # Add bottom border line
    #     shadow1 = tk.Frame(self, bg='#C8C8C8', height=3)   # garis gelap (lebih tebal)
    #     shadow1.pack(side=tk.BOTTOM, fill=tk.X)

    #     shadow2 = tk.Frame(self, bg='#E8E8E8', height=2)   # garis terang (layer kedua)
    #     shadow2.pack(side=tk.BOTTOM, fill=tk.X)

    #     # Force redraw width to match parent
    #     self.update_idletasks()
    #     self.config(width=self.master.winfo_width())

    def __init__(self, parent, user_name="Ibu Kos", user_role="Pemilik Kos"):
        super().__init__(parent, bg='#FCF9EA', height=100)
        self.pack(fill=tk.X)
        self.pack_propagate(False)

        self.user_name = user_name
        self.user_role = user_role
        
        # Buat grid 2 kolom: kiri (title), kanan (profile)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # Title (kolom kiri)
        title_frame = tk.Frame(self, bg='#FCF9EA')
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        self.create_title(title_frame)

        # Profile (kolom kanan)
        profile_frame = tk.Frame(self, bg='#FCF9EA')
        profile_frame.grid(row=0, column=1, sticky="e", padx=30)
        self.create_user_profile(profile_frame)

        # Shadow border
        shadow = tk.Frame(self, bg="#C8C8C8", height=3)
        shadow.grid(row=1, column=0, columnspan=2, sticky="ew")

    
    def create_title(self, parent):
        """Create app title on left"""
        title = tk.Label(
            parent,
            text="AnaKosware App",
            font=('Arial', 20, 'bold'),
            bg='#FCF9EA',
            fg='#2D3142'
        )
        title.pack(anchor = "w")
    
    def create_user_profile(self, parent):
        """Create user profile section on right"""
        profile_frame = tk.Frame(parent, bg='#FCF9EA', cursor='hand2')
        profile_frame.pack(side=tk.RIGHT)
        
        # Avatar (circular shape)
        avatar_canvas = tk.Canvas(profile_frame, width=45, height=45, 
                                 bg='#FCF9EA', highlightthickness=0)
        avatar_canvas.pack(side=tk.LEFT, padx=(0, 12))
        
        # Draw circular avatar with image placeholder
        avatar_canvas.create_oval(2, 2, 43, 43, fill='#D4D4D4', outline='#999999', width=1)
        avatar_canvas.create_text(22, 22, text="👤", font=('Arial', 20))
        
        # User info
        info_frame = tk.Frame(profile_frame, bg='#FCF9EA')
        info_frame.pack(side=tk.LEFT)
        
        name_label = tk.Label(
            info_frame,
            text=self.user_name,
            font=('Arial', 12, 'bold'),
            bg='#FCF9EA',
            fg='#2D3142'
        )
        name_label.pack(anchor='w')
        
        role_label = tk.Label(
            info_frame,
            text=self.user_role,
            font=('Arial', 9),
            bg='#FCF9EA',
            fg='#666666'
        )
        role_label.pack(anchor='w')
        
        # Dropdown arrow
        arrow = tk.Label(
            profile_frame,
            text="▼",
            font=('Arial', 8),
            bg='#FCF9EA',
            fg='#666666'
        )
        arrow.pack(side=tk.LEFT, padx=(10, 0))
