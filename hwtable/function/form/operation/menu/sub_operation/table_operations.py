from PySide6.QtWidgets import (QMenu, QTableWidgetItem, QMainWindow, QVBoxLayout,
                               QWidget, QTextEdit, QTableWidget, QApplication)
from PySide6.QtCore import Qt
from function.form.operation.menu.sub_operation.basic_operations import BasicOperations
from function.form.operation.menu.sub_operation.set_operations import SetOperations
from function.form.operation.menu.sub_operation.merge_operations import MergeOperations

class TableOperations:
    def __init__(self, table):
        self.basic_ops = BasicOperations(table)
        self.set_ops = SetOperations(table)
        self.merge_ops = MergeOperations(table)

    def clear_cells(self):
        self.basic_ops.clear_cells()

    def add_rows(self, above):
        self.basic_ops.add_rows(above)

    def add_columns(self, left):
        self.basic_ops.add_columns(left)

    def delete_rows(self):
        self.basic_ops.delete_rows()

    def delete_columns(self):
        self.basic_ops.delete_columns()

    def align_cells(self, horizontal_alignment, vertical_alignment):
        self.basic_ops.align_cells(horizontal_alignment, vertical_alignment)

    def set_cell_color(self):
        self.set_ops.set_cell_color()

    def set_row_height(self):
        self.set_ops.set_row_height()

    def set_col_width(self):
        self.set_ops.set_col_width()

    def set_font_size(self):
        self.set_ops.set_font_size()

    def set_font_color(self):
        self.set_ops.set_font_color()

    def toggle_bold(self):
        self.set_ops.toggle_bold()

    def merge_cells(self):
        self.merge_ops.merge_cells()

    def unmerge_cells(self):
        self.merge_ops.unmerge_cells()

    def sort_table_by_column(self, column, ascending=True):
        order = Qt.AscendingOrder if ascending else Qt.DescendingOrder
        self.basic_ops.sort_table_by_column(column, order)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(10, 5)
        self.table.setHorizontalHeaderLabels([f"Column {i + 1}" for i in range(5)])

        # Set the stylesheet for the table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color:white ;
                color: black;
            }
            QTableWidget::item:selected {
                background-color: lightblue;
                color: white;
            }
            QHeaderView::section {
                background-color:white ;
                color: black;
            }
            QTableCornerButton::section {
                background-color:white;
                color: black;
            }
            QLineEdit {
                background-color: white;
                color: black;
            }
        """)

        for row in range(10):
            for col in range(5):
                self.table.setItem(row, col, QTableWidgetItem(f"Item {row + 1},{col + 1}"))

        self.table_ops = TableOperations(self.table)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("TableOperations Test")

    def open_menu(self, position):
        menu = QMenu()
        menu.addAction("清除单元格内容", self.table_ops.clear_cells)
        menu.addAction("在上方添加行", lambda: self.table_ops.add_rows(True))
        menu.addAction("在下方添加行", lambda: self.table_ops.add_rows(False))
        menu.addAction("在左侧添加列", lambda: self.table_ops.add_columns(True))
        menu.addAction("在右侧添加列", lambda: self.table_ops.add_columns(False))
        menu.addAction("删除行", self.table_ops.delete_rows)
        menu.addAction("删除列", self.table_ops.delete_columns)
        menu.addAction("左对齐", lambda: self.table_ops.align_cells(Qt.AlignLeft, Qt.AlignVCenter))
        menu.addAction("居中对齐", lambda: self.table_ops.align_cells(Qt.AlignHCenter, Qt.AlignVCenter))
        menu.addAction("右对齐", lambda: self.table_ops.align_cells(Qt.AlignRight, Qt.AlignVCenter))
        menu.addAction("设置单元格颜色", self.table_ops.set_cell_color)
        menu.addAction("设置行高", self.table_ops.set_row_height)
        menu.addAction("设置列宽", self.table_ops.set_col_width)
        menu.addAction("设置字体大小", self.table_ops.set_font_size)
        menu.addAction("设置字体颜色", self.table_ops.set_font_color)
        menu.addAction("切换粗体", self.table_ops.toggle_bold)
        menu.addAction("合并单元格", self.table_ops.merge_cells)
        menu.addAction("取消合并单元格", self.table_ops.unmerge_cells)
        menu.addAction("按列升序排序", lambda: self.table_ops.sort_table_by_column(self.table.currentColumn(), True))
        menu.addAction("按列降序排序", lambda: self.table_ops.sort_table_by_column(self.table.currentColumn(), False))
        menu.exec(self.table.viewport().mapToGlobal(position))

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
                # 使用新的方法设置文本对齐方式
                alignment = item.textAlignment()
                if alignment:
                    new_item.setData(Qt.TextAlignmentRole, alignment)
                self.table.setItem(row, column, new_item)
                QTextEdit.focusOutEvent(text_edit, event)

            text_edit.focusOutEvent = focus_out_event


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()