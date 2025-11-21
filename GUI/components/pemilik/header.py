"""
Header component for AnaKosware application - PyQt6 Version
Refactored: Modern, Minimalist, Consistent with Dashboard styling.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QLabel, QFrame, QVBoxLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QCursor, QColor

class Header(QWidget):
    """Reusable header with title and user profile"""
    
    def __init__(self, parent=None, user_name="Ibu Kos", user_role="Pemilik Kos"):
        super().__init__(parent)
        self.setFixedHeight(80) # Sedikit lebih compact agar elegan
        self.user_name = user_name
        self.user_role = user_role
        
        # Setup UI
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Initialize widgets and layout"""
        # Main Horizontal Layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(40, 0, 40, 0) # Match Dashboard margins
        self.main_layout.setSpacing(20)

        # 1. Left: Application Title
        self.title_label = QLabel("AnaKosware App")
        self.title_label.setObjectName("AppTitle")
        self.main_layout.addWidget(self.title_label)

        # Spacer to push profile to right
        self.main_layout.addStretch()

        # 2. Right: User Profile Container (Frame clickable)
        self.profile_frame = QFrame()
        self.profile_frame.setObjectName("ProfileFrame")
        self.profile_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        profile_layout = QHBoxLayout(self.profile_frame)
        profile_layout.setContentsMargins(10, 5, 15, 5)
        profile_layout.setSpacing(12)

        # Avatar (Circle)
        self.avatar_label = QLabel("👤") # Default icon
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

        self.name_label = QLabel(self.user_name)
        self.name_label.setObjectName("UserName")
        
        self.role_label = QLabel(self.user_role)
        self.role_label.setObjectName("UserRole")

        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.role_label)
        profile_layout.addWidget(info_container)

        # Dropdown Icon
        arrow_label = QLabel("▼")
        arrow_label.setObjectName("ArrowIcon")
        profile_layout.addWidget(arrow_label)

        self.main_layout.addWidget(self.profile_frame)

    def _apply_styles(self):
        """Apply Modern CSS/QSS"""
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            /* Main Container Border */
            Header {
                border-bottom: 1px solid #E0E0E0;
            }
            /* App Title */
            QLabel#AppTitle {
                font-size: 22px;
                font-weight: 800;
                color: #2D3142;
                letter-spacing: 0.5px;
            }
            /* Profile Frame Container */
            QFrame#ProfileFrame {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 25px; /* Pill shape */
            }
            QFrame#ProfileFrame:hover {
                background-color: #F8F9FA;
                border: 1px solid #E0E0E0;
            }
            /* Avatar Circle */
            QLabel#Avatar {
                background-color: #E8F0FE;
                color: #1A73E8;
                font-size: 18px;
                border-radius: 20px; /* Half of size 40px */
                border: 1px solid #D2E3FC;
            }
            /* Text Styles */
            QLabel#UserName {
                font-size: 14px;
                font-weight: 600;
                color: #333333;
            }
            QLabel#UserRole {
                font-size: 11px;
                color: #888888;
                font-weight: 500;
            }
            QLabel#ArrowIcon {
                font-size: 10px;
                color: #888888;
                margin-left: 4px;
            }
        """)

    def set_avatar_image(self, image_path):
        """
        Mengganti avatar dengan gambar file jika ada.
        Otomatis membuat gambar menjadi bulat (masking).
        """
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Scale pixmap
            size = 40
            scaled_pixmap = pixmap.scaled(
                size, size, 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Create circular mask logic could be added here, 
            # but for simple usage, we set the pixmap directly
            # and rely on border-radius (works better with stylesheets on QFrame wrapping label, 
            # but for QLabel directly, border-radius clips background, not content in Qt5/6 sometimes).
            # Simple approach:
            self.avatar_label.setPixmap(scaled_pixmap)
            self.avatar_label.setText("") # Clear emoji


# --- Block Test Standalone ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Setup main window container for demo
    window = QWidget()
    window.setWindowTitle("Header Component Test")
    window.resize(1000, 400)
    window.setStyleSheet("background-color: #F0F2F5;") # Background abu-abu untuk kontras
    
    layout = QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)
    
    # 1. Add Header
    header = Header(window, user_name="Budi Santoso", user_role="Super Admin")
    layout.addWidget(header)
    
    # 2. Add Dummy Content Area
    content = QLabel("Halaman Konten Utama Disini")
    content.setAlignment(Qt.AlignmentFlag.AlignCenter)
    content.setStyleSheet("font-size: 20px; color: #AAA;")
    layout.addWidget(content, stretch=1)
    
    window.show()
    sys.exit(app.exec())