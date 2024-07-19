from PySide6.QtWidgets import QApplication
from window.login import LoginWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
