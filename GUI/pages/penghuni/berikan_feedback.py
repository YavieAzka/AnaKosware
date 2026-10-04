"""
Berikan Feedback Page (Penghuni View) - Modern PyQt6 Version
Style: Modern, Minimalist, Consistent with AnaKosware Design.
Fixes: Dark Mode Proof, Better UX with Text Area.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QFrame, QMessageBox, 
    QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QCursor

# --- IMPORT BACKEND ---
try:
    from feedback.feedback import FeedbackService
except ImportError:
    print("Warning: Backend FeedbackService not found.")
    FeedbackService = None

class BerikanFeedback(QWidget):
    """Halaman bagi penghuni untuk menulis dan mengirim feedback"""
    
    def __init__(self, parent=None, controller=None, current_user_id=1):
        super().__init__(parent)
        self.controller = controller
        self.current_user_id = current_user_id # ID Penghuni yang sedang login
        
        # --- Inisialisasi Service ---
        if FeedbackService:
            self.feedback_service = FeedbackService()
        else:
            self.feedback_service = None
            
        # Setup Properti Dasar
        self.setObjectName("FeedbackFormPage")
        # PENTING: Atribut ini memaksa widget merender background sesuai CSS (Fix Dark Mode)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)
        
        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self):
        """Definisi CSS Global agar tampilan konsisten & Dark Mode Proof"""
        self.setStyleSheet("""
            /* Paksa background putih */
            QWidget#FeedbackFormPage {
                background-color: white;
            }
            
            /* Typography */
            QLabel#PageTitle {
                font-family: 'Segoe UI', sans-serif;
                font-size: 26px;
                font-weight: 800;
                color: #2D3142;
            }
            QLabel#FieldLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
                color: #4A5568;
                margin-bottom: 5px;
            }
            QLabel#HelperText {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                color: #888888;
                margin-bottom: 15px;
            }
            
            /* Form Container Box */
            QFrame#FormContainer {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
            }
            
            /* Text Area Input */
            QTextEdit {
                background-color: #F8FAFC;
                border: 1px solid #CBD5E0;
                border-radius: 12px;
                padding: 15px;
                font-size: 14px;
                color: #333333; /* Teks gelap walau OS dark mode */
                font-family: 'Segoe UI', sans-serif;
            }
            QTextEdit:focus {
                background-color: white;
                border: 2px solid #FF9966; /* Orange Focus */
            }
            
            /* Submit Button */
            QPushButton {
                background-color: #FF9966;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 25px;
                padding: 12px 30px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF8C4D;
                margin-top: 2px;
            }
            QPushButton:pressed {
                background-color: #E67300;
            }
        """)

    def _setup_ui(self):
        """Membuat layout UI"""
        
        # 1. Judul Halaman
        title = QLabel("Berikan Masukan & Laporan")
        title.setObjectName("PageTitle")
        self.main_layout.addWidget(title)
        
        # 2. Form Container (Agar terlihat seperti kartu di tengah)
        self.form_container = QFrame()
        self.form_container.setObjectName("FormContainer")
        self.form_container.setMinimumWidth(500)
        self.form_container.setMaximumWidth(800)
        
        # Shadow Effect untuk Container
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.form_container.setGraphicsEffect(shadow)
        
        # Layout Form Internal
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(15)
        
        # --- Input Components ---
        
        # Label
        lbl_input = QLabel("Tuliskan keluhan, saran, atau apresiasi Anda:")
        lbl_input.setObjectName("FieldLabel")
        form_layout.addWidget(lbl_input)
        
        # Helper Text
        lbl_helper = QLabel("Masukan Anda akan membantu kami meningkatkan kualitas layanan kos.")
        lbl_helper.setObjectName("HelperText")
        lbl_helper.setWordWrap(True)
        form_layout.addWidget(lbl_helper)
        
        # Text Area (QTextEdit untuk multiline)
        self.txt_feedback = QTextEdit()
        self.txt_feedback.setPlaceholderText("Contoh: AC di kamar 101 kurang dingin, mohon dicek...")
        self.txt_feedback.setMinimumHeight(200)
        form_layout.addWidget(self.txt_feedback)
        
        form_layout.addSpacing(10)
        
        # Submit Button (Right Aligned)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_submit = QPushButton("Kirim Feedback 🚀")
        self.btn_submit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_submit.setFixedWidth(200)
        self.btn_submit.clicked.connect(self.submit_feedback)
        
        btn_layout.addWidget(self.btn_submit)
        form_layout.addLayout(btn_layout)
        
        # Menambahkan Container ke Layout Utama (Center Aligned)
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.form_container)
        center_layout.addStretch()
        
        self.main_layout.addLayout(center_layout)
        self.main_layout.addStretch() # Push ke atas

    def submit_feedback(self):
        """Mengirim data ke database"""
        isi_pesan = self.txt_feedback.toPlainText().strip()
        
        # 1. Validasi Lokal
        if not isi_pesan:
            QMessageBox.warning(self, "Peringatan", "Mohon tuliskan isi feedback terlebih dahulu.")
            return
            
        if not self.feedback_service:
            QMessageBox.information(self, "Info (Dummy)", "Feedback terkirim (Backend tidak terhubung).")
            self.txt_feedback.clear()
            return

        # 2. Kirim ke Backend
        try:
            # self.current_user_id harus diset saat login
            result = self.feedback_service.submit_feedback(self.current_user_id, isi_pesan)
            
            if result["status"] == "success":
                QMessageBox.information(self, "Berhasil", result["message"])
                self.txt_feedback.clear()
            else:
                QMessageBox.warning(self, "Gagal", result["message"])
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan sistem: {str(e)}")

# --- Test Standalone ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set font global
    app.setFont(QFont("Segoe UI", 10))
    
    # Simulasi ID User = 1
    window = BerikanFeedback(current_user_id=1)
    window.resize(900, 700)
    window.show()
    
    sys.exit(app.exec())