"""
Header component for AnaKosware application - PyQt6 Version
Refactored: Dynamic User Info & Avatar Initials
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QLabel, QFrame, QVBoxLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QCursor, QColor

class Header(QWidget):
    """Reusable header with title and user profile"""
    
    def __init__(self, parent=None, user_name="Guest", user_role="User"):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.user_name = user_name
        self.user_role = user_role
        
        self._setup_ui()
        self._apply_styles()
        
        # Set initial state
        self.update_user_info(user_name, user_role)

    def _setup_ui(self):
        """Initialize widgets and layout"""
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(40, 0, 40, 0)
        self.main_layout.setSpacing(20)

        # 1. Left: Application Title
        self.title_label = QLabel("AnaKosware App")
        self.title_label.setObjectName("AppTitle")
        self.main_layout.addWidget(self.title_label)

        self.main_layout.addStretch()

        # 2. Right: User Profile Container
        self.profile_frame = QFrame()
        self.profile_frame.setObjectName("ProfileFrame")
        self.profile_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        profile_layout = QHBoxLayout(self.profile_frame)
        profile_layout.setContentsMargins(10, 5, 15, 5)
        profile_layout.setSpacing(12)

        # Avatar (Circle)
        self.avatar_label = QLabel() 
        self.avatar_label.setObjectName("Avatar")
        self.avatar_label.setFixedSize(40, 40)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_layout.addWidget(self.avatar_label)

        # User Info (Name & Role Stack)
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.name_label = QLabel()
        self.name_label.setObjectName("UserName")
        
        self.role_label = QLabel()
        self.role_label.setObjectName("UserRole")

        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.role_label)
        profile_layout.addWidget(info_container)

        # Dropdown Icon
        arrow_label = QLabel("▼")
        arrow_label.setObjectName("ArrowIcon")
        profile_layout.addWidget(arrow_label)

        self.main_layout.addWidget(self.profile_frame)

    def update_user_info(self, name, role):
        """
        Update nama, role, dan inisial avatar secara dinamis.
        Dipanggil oleh MainView saat login berhasil.
        """
        self.user_name = name
        self.user_role = role
        
        # Update Label Teks
        self.name_label.setText(name)
        self.role_label.setText(role)
        
        # Update Avatar dengan Inisial Nama (Misal: "Budi Santoso" -> "BS")
        initials = "U"
        if name:
            parts = name.split()
            if len(parts) >= 2:
                initials = (parts[0][0] + parts[1][0]).upper()
            elif len(parts) == 1:
                initials = parts[0][0].upper()
                
        self.avatar_label.setText(initials)

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            Header { border-bottom: 1px solid #E0E0E0; }
            
            QLabel#AppTitle {
                font-size: 22px; font-weight: 800; color: #2D3142; letter-spacing: 0.5px;
            }
            
            QFrame#ProfileFrame {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 25px;
            }
            QFrame#ProfileFrame:hover {
                background-color: #F8F9FA; border: 1px solid #E0E0E0;
            }
            
            QLabel#Avatar {
                background-color: #E8F0FE; color: #1A73E8;
                font-size: 16px; font-weight: bold;
                border-radius: 20px; border: 1px solid #D2E3FC;
            }
            
            QLabel#UserName { font-size: 14px; font-weight: 600; color: #333333; }
            QLabel#UserRole { font-size: 11px; color: #888888; font-weight: 500; }
            QLabel#ArrowIcon { font-size: 10px; color: #888888; margin-left: 4px; }
        """)

    def set_avatar_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            self.avatar_label.setPixmap(scaled)
            self.avatar_label.setText("") 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget(); window.resize(800, 100)
    layout = QVBoxLayout(window)
    header = Header(window, user_name="Reynard Anderson", user_role="Pemilik")
    layout.addWidget(header)
    window.show()
    sys.exit(app.exec())