from PySide6.QtWidgets import (QMenu, QTextEdit, QTableWidgetItem, QMainWindow,
                               QVBoxLayout, QWidget, QTableWidget, QApplication,
                               QColorDialog, QInputDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class SetOperations:
    def __init__(self, table):
        self.table = table  # 保存对表格控件的引用

    def set_cell_color(self):
        color = QColorDialog.getColor()  # 打开颜色选择对话框
        if color.isValid():  # 如果选中的颜色有效
            for index in self.table.selectedIndexes():  # 遍历所有选中的单元格
                item = self.table.item(index.row(), index.column())
                if not item:  # 如果单元格不存在，创建新的单元格
                    item = QTableWidgetItem()
                    self.table.setItem(index.row(), index.column(), item)
                item.setBackground(color)  # 设置单元格的背景颜色

    def set_row_height(self):
        rows = set(index.row() for index in self.table.selectedIndexes())  # 获取所有选中的行
        height, ok = QInputDialog.getInt(self.table, "Set Row Height", "Enter new row height:", 30, 10, 500, 1)  # 打开输入对话框获取新的行高
        if ok:  # 如果用户点击确认
            for row in rows:
                self.table.setRowHeight(row, height)  # 设置行高

    def set_col_width(self):
        cols = set(index.column() for index in self.table.selectedIndexes())  # 获取所有选中的列
        width, ok = QInputDialog.getInt(self.table, "Set Column Width", "Enter new column width:", 100, 10, 500, 1)  # 打开输入对话框获取新的列宽
        if ok:  # 如果用户点击确认
            for col in cols:
                self.table.setColumnWidth(col, width)  # 设置列宽

    def set_font_size(self):
        size, ok = QInputDialog.getInt(self.table, "Set Font Size", "Enter new font size:", 10, 1, 100, 1)  # 打开输入对话框获取新的字体大小
        if ok:  # 如果用户点击确认
            for index in self.table.selectedIndexes():  # 遍历所有选中的单元格
                item = self.table.item(index.row(), index.column())
                if item is None:  # 如果单元格不存在，创建新的单元格
                    item = QTableWidgetItem()
                    self.table.setItem(index.row(), index.column(), item)
                widget = self.table.cellWidget(index.row(), index.column())
                if widget:  # 如果单元格是一个特殊控件
                    font = widget.font()  # 获取控件的字体
                    font.setPointSize(size)  # 设置字体大小
                    widget.setFont(font)
                else:
                    font = item.font()  # 获取单元格字体
                    font.setPointSize(size)  # 设置字体大小
                    item.setFont(font)

    def set_font_color(self):
        color = QColorDialog.getColor()  # 打开颜色选择对话框
        if color.isValid():  # 如果选中的颜色有效
            for index in self.table.selectedIndexes():  # 遍历所有选中的单元格
                item = self.table.item(index.row(), index.column())
                if item is None:  # 如果单元格不存在，创建新的单元格
                    item = QTableWidgetItem()
                    self.table.setItem(index.row(), index.column(), item)
                item.setForeground(color)  # 设置单元格的字体颜色
                item.setText(item.text())  # 强制更新单元格内容以刷新显示
            self.table.viewport().update()  # 更新视图以应用颜色更改

    def toggle_bold(self):
        for index in self.table.selectedIndexes():  # 遍历所有选中的单元格
            item = self.table.item(index.row(), index.column())
            if item is None:  # 如果单元格不存在，创建新的单元格
                item = QTableWidgetItem()
                self.table.setItem(index.row(), index.column(), item)
            widget = self.table.cellWidget(index.row(), index.column())
            if widget:  # 如果单元格是一个特殊控件
                font = widget.font()  # 获取控件的字体
                font.setBold(not font.bold())  # 切换字体粗体状态
                widget.setFont(font)
            else:
                font = item.font()  # 获取单元格字体
                font.setBold(not font.bold())  # 切换字体粗体状态
                item.setFont(font)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(10, 5)
        self.table.setHorizontalHeaderLabels([f"Column {i+1}" for i in range(5)])

        # Set the stylesheet for the table
        # 设置样式表
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: lightblue;
            }
            QHeaderView::section {
                background-color: black;
                color: white;
            }
            QTableCornerButton::section {
                background-color: black;
                color: white;
            }
            QLineEdit {
                background-color: grey;
                color: black;
            }
        """)

        for row in range(10):
            for col in range(5):
                self.table.setItem(row, col, QTableWidgetItem(f"Item {row+1},{col+1}"))

        self.set_operations = SetOperations(self.table)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Table SetOperations Test")

    def open_menu(self, position):
        menu = QMenu()  # 创建右键菜单
        menu.addAction("设置单元格颜色", self.set_operations.set_cell_color)
        menu.addAction("设置行高", self.set_operations.set_row_height)
        menu.addAction("设置列宽", self.set_operations.set_col_width)
        menu.addAction("设置字体大小", self.set_operations.set_font_size)
        menu.addAction("设置字体颜色", self.set_operations.set_font_color)
        menu.addAction("切换粗体", self.set_operations.toggle_bold)
        menu.exec(self.table.viewport().mapToGlobal(position))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
