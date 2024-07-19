from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self, is_admin):
        super().__init__()
        self.is_admin = is_admin
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.title_label = QLabel("KPI原则", alignment=Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("这里是KPI原则的描述文本。" * 10)  # 300多个字的文本
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.button1 = QPushButton("按钮1")
        self.button2 = QPushButton("按钮2")
        self.button3 = QPushButton("按钮3")
        self.button4 = QPushButton("按钮4")

        self.button1.clicked.connect(lambda: self.handle_button_click(1))
        self.button2.clicked.connect(lambda: self.handle_button_click(2))
        self.button3.clicked.connect(lambda: self.handle_button_click(3))
        self.button4.clicked.connect(lambda: self.handle_button_click(4))

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)

    def handle_button_click(self, button_number):
        from window.admin_settings import permissions  # 导入权限设置

        username = "user"  # 这里应替换为实际的用户名

        if username in permissions and permissions[username][f"page{button_number}"]:
            if self.is_admin:
                self.open_page(button_number)
            else:
                self.open_page(button_number)
        else:
            QMessageBox.warning(self, "Error", "You do not have permission to access this page.")

    def open_page(self, button_number):
        if self.is_admin:
            from window.page1 import Page1  # 延迟导入以避免循环导入
            from window.page2 import Page2
            from window.page3 import Page3
            from window.page4 import Page4
        else:
            from window.page1 import Page1  # 延迟导入以避免循环导入
            from window.page2 import Page2
            from window.page3 import Page3
            from window.page4 import Page4

        if button_number == 1:
            self.page = Page1()
        elif button_number == 2:
            self.page = Page2()
        elif button_number == 3:
            self.page = Page3()
        elif button_number == 4:
            self.page = Page4()

        self.page.show()

