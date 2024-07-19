from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
import sys

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 250)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_credentials)

        self.admin_settings_button = QPushButton("Admin Settings")
        self.admin_settings_button.clicked.connect(self.open_admin_settings)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.admin_settings_button)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # 预定义的用户名和密码
        predefined_username = "admin"
        predefined_password = "admin"

        # 验证用户名和密码
        if username == predefined_username and password == predefined_password:
            self.accept_login(is_admin=True)
        elif username == "user" and password == "user":
            self.accept_login(is_admin=False)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def accept_login(self, is_admin):
        from window.main_window import MainWindow  # 延迟导入以避免循环导入

        self.main_window = MainWindow(is_admin)
        self.main_window.show()
        self.close()

    def open_admin_settings(self):
        from window.admin_settings import AdminSettingsWindow  # 延迟导入以避免循环导入

        self.admin_settings_window = AdminSettingsWindow()
        self.admin_settings_window.show()
