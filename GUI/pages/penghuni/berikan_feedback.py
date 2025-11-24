from PyQt6.QtWidgets import (
    QWidget, QLabel, QTextEdit, QVBoxLayout, QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from components.penghuni.star_rating import StarRating  # versi PyQt6
from components.custom_widgets import StyledButton      # versi PyQt6


class BerikanFeedback(QWidget):
    """Halaman untuk mengisi feedback pengguna (versi PyQt6)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.placeholder = "Berikan feedback..."
        self.create_content()

    def create_content(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        # ============================
        # JUDUL
        # ============================
        title = QLabel("Feedback Kos Melati")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2D3142;")
        layout.addWidget(title)

        # ============================
        # DESKRIPSI
        # ============================
        description = QLabel(
            "Berikan rating dan feedback Anda terhadap layanan dan fasilitas Kos Melati "
            "agar kami dapat terus meningkatkan kualitas kos."
        )
        description.setFont(QFont("Arial", 12))
        description.setWordWrap(True)
        description.setStyleSheet("color: #666666;")
        layout.addWidget(description)

        # ============================
        # LABEL RATING
        # ============================
        rating_label = QLabel("Rating")
        rating_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        rating_label.setStyleSheet("color: #333333;")
        layout.addWidget(rating_label)

        # ============================
        # STAR RATING COMPONENT
        # ============================
        self.rating_value = 0

        self.star_rating = StarRating(
            parent=self,
            on_rating_changed=self.set_rating  # callback saat rating berubah
        )
        layout.addWidget(self.star_rating)

        # ============================
        # LABEL FEEDBACK
        # ============================
        message_label = QLabel("Pesan Feedback")
        message_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        message_label.setStyleSheet("color: #333333;")
        layout.addWidget(message_label)

        # ============================
        # TEXT AREA FEEDBACK
        # ============================
        self.feedback_text = QTextEdit()
        self.feedback_text.setFont(QFont("Arial", 12))
        self.feedback_text.setFixedHeight(160)
        self.feedback_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #c9c9c9;
                border-radius: 8px;
                padding: 6px;
                color: #999999;
            }
        """)

        self.feedback_text.setText(self.placeholder)

        self.feedback_text.focusInEvent = self.remove_placeholder
        self.feedback_text.focusOutEvent = self.add_placeholder

        layout.addWidget(self.feedback_text)

        # ============================
        # SUBMIT BUTTON
        # ============================
        submit_btn = StyledButton(
            text="Submit Feedback",
            fontsize=12,
            bold=True,
            bg="#F8A80F",
            fg="white",
            hover_bg="#FFB84D",
            callback=self.submit_feedback
        )
        submit_btn.setFixedWidth(200)
        submit_btn.setFixedHeight(40)
        layout.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)

    # ===========================================================
    # CALLBACK SET RATING
    # ===========================================================
    def set_rating(self, value):
        self.rating_value = value

    # ===========================================================
    # PLACEHOLDER HANDLING
    # ===========================================================
    def remove_placeholder(self, event):
        if self.feedback_text.toPlainText().strip() == self.placeholder:
            self.feedback_text.setPlainText("")
            self.feedback_text.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #c9c9c9;
                    border-radius: 8px;
                    padding: 6px;
                    color: black;
                }
            """)
        super().focusInEvent(event)

    def add_placeholder(self, event):
        if not self.feedback_text.toPlainText().strip():
            self.feedback_text.setPlainText(self.placeholder)
            self.feedback_text.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #c9c9c9;
                    border-radius: 8px;
                    padding: 6px;
                    color: #999999;
                }
            """)
        super().focusOutEvent(event)

    # ===========================================================
    # SUBMIT FEEDBACK
    # ===========================================================
    def submit_feedback(self):
        rating = self.rating_value
        feedback = self.feedback_text.toPlainText().strip()

        if feedback == self.placeholder:
            feedback = ""

        # Validasi
        if rating == 0 or feedback == "":
            QMessageBox.warning(
                self, "Peringatan",
                "Rating dan pesan feedback harus diisi dengan benar!"
            )
            return

        confirm = QMessageBox.question(
            self,
            "Submit Feedback",
            "Apakah Anda yakin untuk submit feedback ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            print(f"Rating: {rating} | Feedback: {feedback}")

            QMessageBox.information(
                self,
                "Submit Feedback Berhasil",
                "Terima kasih sudah memberikan feedback! 😊"
            )

            # Reset form
            self.star_rating.reset_rating()
            self.rating_value = 0

            self.feedback_text.setPlainText(self.placeholder)
            self.feedback_text.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #c9c9c9;
                    border-radius: 8px;
                    padding: 6px;
                    color: #999999;
                }
            """)


# Standalone Preview
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = BerikanFeedback()
    w.resize(600, 600)
    w.show()
    sys.exit(app.exec())
