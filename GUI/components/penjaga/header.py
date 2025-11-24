from PyQt6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Header(QWidget):
    """Reusable header component for AnaKosware application."""

    def __init__(self, parent=None, user_name="Asep", user_role="Penjaga Kos"):
        super().__init__(parent)
        self.user_name = user_name
        self.user_role = user_role

        self.setStyleSheet("background-color: #FCF9EA;")  # set background color
        self.setFixedHeight(100)  # fix height

        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        # Title section (Left)
        title_label = QLabel("AnaKosware App")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2D3142;")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Profile section (Right)
        profile_layout = QHBoxLayout()
        profile_layout.setSpacing(10)

        # Avatar Circle Placeholder
        avatar = QLabel("👤")
        avatar.setFont(QFont("Arial", 22))
        avatar.setFixedSize(45, 45)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            border-radius: 22px;
            background-color: #D4D4D4;
            border: 1px solid #999;
        """)

        profile_layout.addWidget(avatar)

        # Name + Role Vertical Layout
        info_layout = QVBoxLayout()
        name_label = QLabel(self.user_name)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        role_label = QLabel(self.user_role)
        role_label.setFont(QFont("Arial", 9))

        info_layout.addWidget(name_label)
        info_layout.addWidget(role_label)
        profile_layout.addLayout(info_layout)

        # Dropdown arrow
        arrow = QLabel("▼")
        arrow.setFont(QFont("Arial", 10))
        profile_layout.addWidget(arrow)

        # Add profile layout to main layout
        main_layout.addLayout(profile_layout)
        main_layout.setAlignment(profile_layout, Qt.AlignmentFlag.AlignRight)

        # Bottom border line
        self.shadow = QFrame()
        self.shadow.setFrameShape(QFrame.Shape.HLine)
        self.shadow.setStyleSheet("color: #C8C8C8; background-color: #C8C8C8;")
        self.shadow.setFixedHeight(3)

        # layout trick to add bottom line
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addLayout(main_layout)
        outer_layout.addWidget(self.shadow)
