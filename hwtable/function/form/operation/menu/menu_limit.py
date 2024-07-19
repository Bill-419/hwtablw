from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QMenu, QWidget, QTableWidget, QTableWidgetItem, QApplication
from PySide6.QtCore import Qt
from function.form.operation.menu.menu_base import MenuOperationsBase

class MenuLimitOperations(MenuOperationsBase):
    def add_additional_actions(self, menu):
        # 添加额外的菜单操作
        clear_action = menu.addAction("清空单元格")
        add_menu = menu.addMenu("添加")
        add_row_above_action = add_menu.addAction("在上方添加行")
        add_row_below_action = add_menu.addAction("在下方添加行")
        add_col_left_action = add_menu.addAction("在左侧添加列")
        add_col_right_action = add_menu.addAction("在右侧添加列")
        delete_menu = menu.addMenu("删除")
        delete_row_action = delete_menu.addAction("删除行")
        delete_col_action = delete_menu.addAction("删除列")
        set_width_action = menu.addAction("设置列宽")
        set_height_action = menu.addAction("设置行高")
        set_font_size_action = menu.addAction("设置字体大小")
        toggle_bold_action = menu.addAction("切换加粗")

        sort_menu = menu.addMenu("排序")
        sort_asc_action = sort_menu.addAction("升序")
        sort_desc_action = sort_menu.addAction("降序")

        additional_actions = {
            clear_action: self.table_operations.clear_cells,
            add_row_above_action: lambda: self.table_operations.add_rows(above=True),
            add_row_below_action: lambda: self.table_operations.add_rows(above=False),
            add_col_left_action: lambda: self.table_operations.add_columns(left=True),
            add_col_right_action: lambda: self.table_operations.add_columns(left=False),
            delete_row_action: self.table_operations.delete_rows,
            delete_col_action: self.table_operations.delete_columns,
            set_width_action: self.table_operations.set_col_width,
            set_height_action: self.table_operations.set_row_height,
            set_font_size_action: self.table_operations.set_font_size,
            toggle_bold_action: self.table_operations.toggle_bold,
            sort_asc_action: lambda: self.table_operations.sort_table_by_column(self.table.currentColumn(), ascending=True),
            sort_desc_action: lambda: self.table_operations.sort_table_by_column(self.table.currentColumn(), ascending=False)
        }
        return additional_actions

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(10, 5)
        self.table.setHorizontalHeaderLabels([f"Column {i + 1}" for i in range(5)])

        # 填充一些测试数据
        for row in range(10):
            for col in range(5):
                self.table.setItem(row, col, QTableWidgetItem(f"Item {row + 1},{col + 1}"))

        self.menu_operations = MenuLimitOperations(self.table)
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