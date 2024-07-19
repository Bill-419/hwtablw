from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QMenu, QWidget, QTableWidget, QTableWidgetItem, QApplication
from PySide6.QtCore import Qt
from function.form.operation.menu.menu_base import MenuOperationsBase

class CustomTableWidget(QTableWidget):
    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            print(f"Cell at ({item.row()}, {item.column()}) double clicked, but editing is blocked.")
        else:
            super().mouseDoubleClickEvent(event)

class MenuUserOperations(MenuOperationsBase):
    def __init__(self, table):
        super().__init__(table)
        try:
            self.table.cellDoubleClicked.disconnect(self.on_cell_double_clicked)
        except (RuntimeError, TypeError):
            pass  # 如果信号未连接或断开失败，则忽略

    def add_additional_actions(self, menu):
        # 用户只能执行设置单元格颜色、字体颜色和对齐方式的操作
        return {}

    def on_cell_double_clicked(self, row, column):
        # 取消双击单元格时的编辑操作
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = CustomTableWidget(10, 5)
        self.table.setHorizontalHeaderLabels([f"Column {i + 1}" for i in range(5)])

        # 填充一些测试数据
        for row in range(10):
            for col in range(5):
                self.table.setItem(row, col, QTableWidgetItem(f"Item {row + 1},{col + 1}"))

        self.menu_operations = MenuUserOperations(self.table)
        self.table.cellDoubleClicked.connect(self.menu_operations.on_cell_double_clicked)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Table Menu and Edit Test")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
