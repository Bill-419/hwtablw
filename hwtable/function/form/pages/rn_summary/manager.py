import sys
import re
import pandas as pd
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QApplication, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QLineEdit, QMenu
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from function.form.operation.table.table import TableWidget  # 确保导入正确
from function.database.database import MongoDBHandler  # 导入MongoDBHandler

class RnSummaryManagerWindow(QMainWindow):
    def __init__(self, table=None):
        super().__init__()
        self.setWindowTitle("RN汇总")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # MongoDB 配置
        self.db_handler = MongoDBHandler("mongodb://localhost:27017/", "mydatabase", "summary")

        # 创建并添加表格
        if table is None:
            self.table_widget = TableWidget.create_table_widget()
        else:
            self.table_widget = TableWidget(table)

        # 设置列标题
        self.set_column_headers(self.table_widget.get_table())

        # 原始数据表格
        self.original_table = QTableWidget(self.table_widget.get_table().rowCount(), self.table_widget.get_table().columnCount())
        self.copy_table(self.table_widget.get_table(), self.original_table)

        # 副本表格，用于显示筛选结果
        self.filtered_table_widget = QTableWidget(self.original_table.rowCount(), self.original_table.columnCount())
        self.copy_table(self.original_table, self.filtered_table_widget)

        # 创建筛选输入框布局
        self.filter_inputs = []
        self.create_filter_inputs(layout, self.filtered_table_widget.columnCount())

        layout.addWidget(self.filtered_table_widget)

        # 创建按钮布局
        button_layout = QHBoxLayout()

        # 添加保存按钮
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_data)
        button_layout.addWidget(save_button)

        # 添加刷新按钮
        refresh_button = QPushButton("刷新")
        refresh_button.clicked.connect(self.refresh_data)
        button_layout.addWidget(refresh_button)

        # 添加导出为Excel按钮
        export_button = QPushButton("导出为Excel")
        export_button.clicked.connect(self.export_to_excel)
        button_layout.addWidget(export_button)

        layout.addLayout(button_layout)

        # 连接表格单元格变化信号
        self.filtered_table_widget.itemChanged.connect(self.sync_changes_to_original)

        # 加载表格数据
        self.load_table_data()

    def set_column_headers(self, table):
        headers = ['问题单号', '问题描述', '严重级别', '解决方案', '修改影响', '涉及制式', '涉及基站']
        table.setHorizontalHeaderLabels(headers)

    def create_filter_inputs(self, layout, num_filters):
        filter_layout = QHBoxLayout()
        for i in range(num_filters):
            filter_input = QLineEdit()
            filter_input.setPlaceholderText(f"筛选条件 {i + 1}")
            filter_layout.addWidget(filter_input)
            self.filter_inputs.append(filter_input)
        
        filter_button = QPushButton("确定")
        filter_button.clicked.connect(self.apply_combined_filter)
        filter_layout.addWidget(filter_button)
        
        layout.addLayout(filter_layout)

    def apply_combined_filter(self):
        self.copy_table(self.original_table, self.filtered_table_widget)  # 每次筛选前重置副本表格
        for row in range(self.filtered_table_widget.rowCount()):
            match = True
            for col, filter_input in enumerate(self.filter_inputs):
                filter_text = filter_input.text().strip()
                if filter_text:
                    item = self.filtered_table_widget.item(row, col)
                    if item is None or not re.search(filter_text, item.text(), re.IGNORECASE):
                        match = False
                        break
            self.filtered_table_widget.setRowHidden(row, not match)

    def sync_changes_to_original(self, item):
        # 获取当前单元格的行和列
        row = item.row()
        col = item.column()

        # 更新原始表格中的对应单元格
        original_item = self.original_table.item(row, col)
        if original_item:
            original_item.setText(item.text())
        else:
            self.original_table.setItem(row, col, QTableWidgetItem(item.text()))

    def save_data(self):
        # 保存数据到 MongoDB
        table = self.original_table
        data = []
        headers = ['问题单号', '问题描述', '严重级别', '解决方案', '修改影响', '涉及制式', '涉及基站']
        for row in range(table.rowCount()):
            row_data = {}
            for col, header in enumerate(headers):
                item = table.item(row, col)
                row_data[header] = item.text() if item else ''
            data.append(row_data)
        self.db_handler.save_table(data)
        QMessageBox.information(self, "保存成功", "表格数据已保存到数据库")

    def refresh_data(self):
        # 刷新数据的逻辑
        self.load_table_data()
        print("数据已刷新")

    def export_to_excel(self):
        table = self.filtered_table_widget
        path, _ = QFileDialog.getSaveFileName(self, "导出为Excel", "", "Excel Files (*.xlsx)")
        if path:
            data = []
            for row in range(table.rowCount()):
                row_data = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    row_data.append(item.text() if item else '')
                data.append(row_data)
            df = pd.DataFrame(data)
            df.to_excel(path, index=False, header=False)
            QMessageBox.information(self, "导出成功", f"表格已成功导出到 {path}")

    def load_table_data(self):
        # 从 MongoDB 加载数据
        data = self.db_handler.get_table()
        print(f"从MongoDB加载的数据: {data}")  # 调试输出
        if data:
            self.populate_table(data)
        else:
            self.populate_table_with_default_data()

    def populate_table(self, data):
        table = self.original_table
        table.clearContents()  # 清空现有数据
        table.setRowCount(len(data))
        table.setColumnCount(7)
        headers = ['问题单号', '问题描述', '严重级别', '解决方案', '修改影响', '涉及制式', '涉及基站']
        table.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(headers):
                try:
                    item = QTableWidgetItem(row_data[header])
                except KeyError:
                    item = QTableWidgetItem("")  # 如果数据中缺少某列，填充空白
                table.setItem(row_idx, col_idx, item)
        self.copy_table(self.original_table, self.filtered_table_widget)

    def populate_table_with_default_data(self):
        table = self.original_table
        table.setRowCount(2)
        table.setColumnCount(7)
        headers = ['问题单号', '问题描述', '严重级别', '解决方案', '修改影响', '涉及制式', '涉及基站']
        table.setHorizontalHeaderLabels(headers)
        for row in range(2):
            for col in range(7):
                item = QTableWidgetItem(f'({row}, {col})')
                table.setItem(row, col, item)
        self.copy_table(self.original_table, self.filtered_table_widget)

    def copy_table(self, source_table, target_table):
        target_table.setRowCount(source_table.rowCount())
        target_table.setColumnCount(source_table.columnCount())
        target_table.setHorizontalHeaderLabels([source_table.horizontalHeaderItem(col).text() for col in range(source_table.columnCount())])
        for row in range(source_table.rowCount()):
            for col in range(source_table.columnCount()):
                source_item = source_table.item(row, col)
                if source_item:
                    target_item = QTableWidgetItem(source_item.text())
                    target_item.setForeground(source_item.foreground())
                    target_item.setBackground(source_item.background())
                    target_table.setItem(row, col, target_item)


if __name__ == "__main__":
    app = QApplication([])

    # 创建一个示例表格
    example_table = QTableWidget(3, 7)
    for row in range(3):
        for col in range(7):
            example_table.setItem(row, col, QTableWidgetItem(str((row + 1) * (col + 1))))

    window = RnSummaryManagerWindow(example_table)
    window.show()

    app.exec()
