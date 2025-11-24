from PyQt6.QtWidgets import (
    QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Header(QFrame):
    """Header reusable untuk halaman pemilik penghuni"""

    def __init__(self, parent=None, user_name="Ahmad Husein", user_role="Penghuni Kos"):
        super().__init__(parent)

        # Warna background dan tinggi
        self.setStyleSheet("background-color: #FCF9EA;")
        self.setFixedHeight(100)

        self.user_name = user_name
        self.user_role = user_role

        # Layout utama (horizontal)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)

        # ----- kiri: title -----
        title_label = QLabel("AnaKosware App")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2D3142;")

        # Membuat space fleksibel supaya profil ke kanan
        title_container = QHBoxLayout()
        title_container.addWidget(title_label)
        title_container.addStretch()

        # ----- kanan: profile -----
        profile_layout = QHBoxLayout()
        profile_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Avatar bulat (pakai QLabel sebagai placeholder)
        avatar = QLabel("👤")
        avatar.setFixedSize(45, 45)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background-color: #D4D4D4;
            border: 1px solid #999999;
            border-radius: 22px;
            font-size: 22px;
        """)

        # Informasi pengguna
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_label = QLabel(self.user_name)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #2D3142;")

        role_label = QLabel(self.user_role)
        role_label.setFont(QFont("Arial", 9))
        role_label.setStyleSheet("color: #666666;")

        info_layout.addWidget(name_label)
        info_layout.addWidget(role_label)

        arrow = QLabel("▼")
        arrow.setFont(QFont("Arial", 10))
        arrow.setStyleSheet("color: #666666; margin-left: 5px;")

        # Tambahkan ke layout profile
        profile_layout.addWidget(avatar)
        profile_layout.addLayout(info_layout)
        profile_layout.addWidget(arrow)

        # Tambahkan keduanya ke layout utama
        main_layout.addLayout(title_container)
        main_layout.addLayout(profile_layout)
