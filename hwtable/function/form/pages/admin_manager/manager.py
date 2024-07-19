from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QApplication, QHBoxLayout, QTableWidgetItem
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Qt
import sys
from function.form.operation.table.table_limit import TableLimitWidget  # 确保导入正确
from function.database.database import MongoDBHandler

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

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # 预定义的用户名和密码
        predefined_username = "admin"
        predefined_password = "admin"

        # 验证用户名和密码
        if username == predefined_username and password == predefined_password:
            self.accept_login()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def accept_login(self):
        self.main_window = AdminManagerWindow()
        self.main_window.show()
        self.main_window.load_table_data()
        self.close()

class AdminManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Manager")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 添加权限管理标签
        label = QLabel("Permissions Management:")
        layout.addWidget(label)

        # 创建并添加表格
        self.table_widget = self.create_table_limit_widget()
        layout.addWidget(self.table_widget)

        # 添加刷新和保存按钮
        button_layout = QHBoxLayout()
        refresh_button = QPushButton("Refresh")
        save_button = QPushButton("Save")

        button_layout.addWidget(refresh_button)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)

        refresh_button.clicked.connect(self.refresh_data)
        save_button.clicked.connect(self.save_data)

        # MongoDB 配置
        self.db_handler = MongoDBHandler("mongodb://localhost:27017/", "mydatabase", "mycollection")

    def create_table_limit_widget(self):
        # 使用 TableWidget 而不是 QTableWidget
        table_widget = TableLimitWidget()
        self._customize_table(table_widget.table)  # 传递实际的 QTableWidget 对象
        return table_widget

    def _customize_table(self, table):
        headers = ['Account', 'Password', 'Page1 Permission', 'Page2 Permission', 'Page3 Permission', 'Page4 Permission']
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(2)  # 默认2行
        table.setColumnCount(6)  # 默认6列
        for row in range(2):
            for col in range(6):
                item = QTableWidgetItem(f'({row}, {col})')
                item.setForeground(QBrush(QColor(Qt.black)))  # 设置字体颜色为黑色
                item.setBackground(QBrush(QColor(Qt.white)))  # 设置背景颜色为白色
                table.setItem(row, col, item)

    def load_table_data(self):
        # 加载表格数据的逻辑，可以是从服务器获取数据
        data = self.db_handler.get_table()
        if data:
            self.populate_table(data)
        else:
            self._customize_table(self.table_widget.table)  # 使用默认数据

    def populate_table(self, data):
        table = self.table_widget.table
        table.setRowCount(len(data))
        table.setColumnCount(6)  # 默认6列
        headers = ['Account', 'Password', 'Page1 Permission', 'Page2 Permission', 'Page3 Permission', 'Page4 Permission']
        table.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data.values()):
                table_item = QTableWidgetItem(item)
                table_item.setForeground(QBrush(QColor(Qt.black)))  # 设置字体颜色为黑色
                table_item.setBackground(QBrush(QColor(Qt.white)))  # 设置背景颜色为白色
                table.setItem(row_idx, col_idx, table_item)

    def refresh_data(self):
        # 刷新数据的逻辑
        self.load_table_data()

    def save_data(self):
        # 保存数据的逻辑
        table = self.table_widget.table
        data = []
        for row in range(table.rowCount()):
            row_data = {}
            headers = ['Account', 'Password', 'Page1 Permission', 'Page2 Permission', 'Page3 Permission', 'Page4 Permission']
            for col, header in enumerate(headers):
                item = table.item(row, col)
                row_data[header] = item.text() if item else 'no' if 'Permission' in header else ''
            data.append(row_data)
        self.db_handler.save_table(data)
        QMessageBox.information(self, "保存成功", "表格数据已保存到数据库")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
