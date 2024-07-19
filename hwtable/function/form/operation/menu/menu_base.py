from PySide6.QtWidgets import (QMenu, QTextEdit, QTableWidgetItem, QMainWindow,
                               QVBoxLayout, QWidget, QTableWidget, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from function.form.operation.menu.sub_operation.table_operations import TableOperations

class MenuOperationsBase:
    def __init__(self, table):
        self.table = table  # 表格对象
        self.table_operations = TableOperations(table)

        # 连接信号和槽
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)

        # 用于存储原始和编辑后的文本
        self.original_texts = {}
        self.edited_texts = {}

    def add_common_actions(self, menu):
        # 添加设置单元格颜色、字体颜色和对齐方式的操作到菜单
        set_color_action = menu.addAction("设置单元格颜色")
        set_font_color_action = menu.addAction("设置字体颜色")
        align_menu = menu.addMenu("对齐单元格")
        align_left_action = align_menu.addAction("左对齐")
        align_center_action = align_menu.addAction("居中对齐")
        align_right_action = align_menu.addAction("右对齐")

        actions = {
            set_color_action: self.table_operations.set_cell_color,
            set_font_color_action: self.table_operations.set_font_color,
            align_left_action: lambda: self.table_operations.align_cells(Qt.AlignLeft, Qt.AlignVCenter),
            align_center_action: lambda: self.table_operations.align_cells(Qt.AlignHCenter, Qt.AlignVCenter),
            align_right_action: lambda: self.table_operations.align_cells(Qt.AlignRight, Qt.AlignVCenter),
        }
        return actions

    def add_additional_actions(self, menu):
        # 添加额外的菜单操作
        return {}

    def open_menu(self, position):
        menu = QMenu()  # 创建右键菜单
        actions = self.add_common_actions(menu)
        additional_actions = self.add_additional_actions(menu)
        actions.update(additional_actions)

        # 执行选择的操作
        action = menu.exec(self.table.viewport().mapToGlobal(position))

        # 根据用户选择执行相应操作
        if action in actions:
            actions[action]()

    def on_cell_double_clicked(self, row, column):
        item = self.table.item(row, column)
        if item:
            text_edit = QTextEdit()
            text_edit.setPlainText(item.text())
            self.table.setCellWidget(row, column, text_edit)
            text_edit.setFocus()
            text_edit.setFont(item.font())
            text_edit.setAlignment(Qt.AlignmentFlag(item.textAlignment()))

            def focus_out_event(event):
                text = text_edit.toPlainText()
                self.table.removeCellWidget(row, column)
                new_item = QTableWidgetItem(text)
                new_item.setForeground(item.foreground())
                new_item.setBackground(item.background())
                new_item.setFont(item.font())
                alignment = item.textAlignment()
                if alignment:
                    new_item.setData(Qt.TextAlignmentRole, alignment)
                self.table.setItem(row, column, new_item)
                QTextEdit.focusOutEvent(text_edit, event)

            text_edit.focusOutEvent = focus_out_event


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