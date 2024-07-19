from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QApplication
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from function.form.operation.menu.menu_user import MenuUserOperations,CustomTableWidget

class TableUserWidget(QWidget):
    def __init__(self, table=None):
        super().__init__()

        if table is None:
            self.table = CustomTableWidget(6, 6)
            self.items = []  # 存储所有的QTableWidgetItem对象
            for row in range(6):
                for col in range(6):
                    item = QTableWidgetItem(f"Item {row + 1},{col + 1}")
                    item.setBackground(QColor("#ffffff"))  # 设置默认背景颜色为白色
                    item.setForeground(QColor("#000000"))  # 设置默认字体颜色为黑色
                    self.table.setItem(row, col, item)
                    self.items.append(item)  # 将item添加到列表中
        else:
            self.table = table

        self.menu_operations = MenuUserOperations(self.table)
        self.table.cellDoubleClicked.connect(self.menu_operations.on_cell_double_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

        # 创建上下文菜单
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.menu_operations.open_menu)

    def get_table_user(self):
        return self.table

    @staticmethod
    def create_table_user_widget():
        return TableUserWidget()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TableUserWidget Test")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 创建并添加TableUserWidget
        self.table_user_widget = TableUserWidget.create_table_user_widget()
        layout.addWidget(self.table_user_widget)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
