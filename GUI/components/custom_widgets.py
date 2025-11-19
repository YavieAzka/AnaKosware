"""
Custom widgets for AnaKosware application.
"""
import tkinter as tk


class PlaceholderEntry(tk.Entry):
    """Entry widget with placeholder text functionality"""
    
    def __init__(self, master=None, placeholder="", color='#999999', **kwargs):
        super().__init__(master, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg'] if self['fg'] else 'black'
        
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        self._add_placeholder()
    
    def _clear_placeholder(self, event=None):
        """Clear placeholder when field gets focus"""
        if self['fg'] == self.placeholder_color:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color
    
    def _add_placeholder(self, event=None):
        """Add placeholder when field loses focus and is empty"""
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color
    
    def get_value(self):
        """Get actual value excluding placeholder"""
        value = self.get()
        if self['fg'] == self.placeholder_color:
            return ""
        return value


class StyledButton(tk.Button):
    """Button with hover effects"""
    
    def __init__(self, master=None, hover_bg=None, **kwargs):
        # Default styling
        default_style = {
            'relief': 'flat',
            'cursor': 'hand2',
            'borderwidth': 0
        }
        
        for key, value in default_style.items():
            if key not in kwargs:
                kwargs[key] = value
        
        super().__init__(master, **kwargs)
        
        self.default_bg = self['bg']
        self.hover_bg = hover_bg if hover_bg else self._darken_color(self.default_bg)
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        """Change background on hover"""
        self.config(bg=self.hover_bg)
    
    def _on_leave(self, event):
        """Restore background"""
        self.config(bg=self.default_bg)
    
    def _darken_color(self, hex_color):
        """Darken a hex color"""
        if not hex_color or hex_color == 'systemButtonFace':
            return '#D0D0D0'
        
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(int(c * 0.85) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darker_rgb)