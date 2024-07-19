# window.py

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from function.form.operation.table.table import create_table_widget  # 导入表格创建函数
import sys

class TableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Window")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 创建并添加表格
        self.table_widget = create_table_widget()
        layout.addWidget(self.table_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TableWindow()
    window.show()

    sys.exit(app.exec())
