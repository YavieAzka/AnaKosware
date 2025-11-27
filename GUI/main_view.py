import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

# Import Login Page
from GUI.pages.login.login_page import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    # Load Login Window
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())