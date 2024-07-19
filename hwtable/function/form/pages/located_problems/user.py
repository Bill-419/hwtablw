import sys
import re
import pandas as pd
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QApplication, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QLineEdit
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from pymongo import MongoClient
from function.form.operation.table.table import TableWidget  # 确保导入正确

class MongoDBHandler:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_table(self, data):
        self.collection.delete_many({})
        self.collection.insert_many(data)

    def get_table(self):
        return list(self.collection.find({}, {"_id": 0}))

class RnSummaryUserWindow(QMainWindow):
    def __init__(self, table=None):
        super().__init__()
        self.setWindowTitle("RN汇总")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # MongoDB 配置
        self.db_handler = MongoDBHandler("mongodb://localhost:27017/", "mydatabase", "summary1")
        self.db_handler2 = MongoDBHandler("mongodb://localhost:27017/", "mydatabase", "other_collection1")

        # 创建并添加表格
        if table is None:
            self.table_widget = TableWidget.create_table_widget()
        else:
            self.table_widget = TableWidget(table)

        # 设置列标题
        self.set_column_headers(self.table_widget.get_table())

        # 原始数据表格
        self.original_table = TableWidget.create_table_widget()
        self.copy_table(self.table_widget.get_table(), self.original_table.get_table())

        # 副本表格，用于显示筛选结果
        self.filtered_table_widget = TableWidget.create_table_widget()
        self.copy_table(self.original_table.get_table(), self.filtered_table_widget.get_table())

        # 创建筛选输入框布局
        self.filter_inputs = []
        self.create_filter_inputs(layout, self.filtered_table_widget.get_table().columnCount())

        layout.addWidget(self.filtered_table_widget)

        # 创建第二个表格
        self.table_widget2 = TableWidget.create_table_widget()
        self.set_column_headers(self.table_widget2.get_table())

        layout.addWidget(self.table_widget2)

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

        # 添加变更按钮
        change_button = QPushButton("变更")
        change_button.clicked.connect(self.clear_and_load_to_first_table)
        button_layout.addWidget(change_button)

        layout.addLayout(button_layout)

        # 连接表格单元格变化信号
        self.filtered_table_widget.get_table().itemChanged.connect(self.sync_changes_to_original)

        # 加载表格数据
        self.load_table_data()

    def set_column_headers(self, table):
        headers = ['影响版本', '定位模块', '定位人', '问题引入模块', '是否补充RN', '引入版本', '修复版本', '备注']
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
        self.copy_table(self.original_table.get_table(), self.filtered_table_widget.get_table())  # 每次筛选前重置副本表格
        for row in range(self.filtered_table_widget.get_table().rowCount()):
            match = True
            for col, filter_input in enumerate(self.filter_inputs):
                filter_text = filter_input.text().strip()
                if filter_text:
                    item = self.filtered_table_widget.get_table().item(row, col)
                    if item is None or not re.search(filter_text, item.text(), re.IGNORECASE):
                        match = False
                        break
            self.filtered_table_widget.get_table().setRowHidden(row, not match)

    def sync_changes_to_original(self, item):
        # 获取当前单元格的行和列
        row = item.row()
        col = item.column()

        # 更新原始表格中的对应单元格
        original_item = self.original_table.get_table().item(row, col)
        if original_item:
            original_item.setText(item.text())
        else:
            self.original_table.get_table().setItem(row, col, QTableWidgetItem(item.text()))

    def save_data(self):
        # 保存第一个表格数据到 MongoDB
        self._save_table_data(self.original_table.get_table(), self.db_handler, "第一个表格数据已保存")

        # 保存第二个表格数据到 MongoDB
        self._save_table_data(self.table_widget2.get_table(), self.db_handler2, "第二个表格数据已保存")

    def _save_table_data(self, table, db_handler, message):
        data = []
        headers = ['影响版本', '定位模块', '定位人', '问题引入模块', '是否补充RN', '引入版本', '修复版本', '备注']
        for row in range(table.rowCount()):
            row_data = {}
            for col, header in enumerate(headers):
                item = table.item(row, col)
                row_data[header] = item.text() if item else ''
            data.append(row_data)
        db_handler.save_table(data)
        QMessageBox.information(self, "保存成功", message)

    def refresh_data(self):
        # 刷新数据的逻辑
        self.load_table_data()
        print("数据已刷新")

    def export_to_excel(self):
        table = self.filtered_table_widget.get_table()
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
        table = self.original_table.get_table()
        table.clearContents()  # 清空现有数据
        table.setRowCount(len(data) + 5)  # 加5行空白行
        table.setColumnCount(8)
        headers = ['影响版本', '定位模块', '定位人', '问题引入模块', '是否补充RN', '引入版本', '修复版本', '备注']
        table.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(headers):
                try:
                    cell_data = row_data.get(header, "")
                    item = QTableWidgetItem(cell_data)
                    table.setItem(row_idx, col_idx, item)
                except KeyError:
                    item = QTableWidgetItem("")  # 如果数据中缺少某列，填充空白
                    table.setItem(row_idx, col_idx, item)
        self.copy_table(self.original_table.get_table(), self.filtered_table_widget.get_table())

    def populate_table_with_default_data(self):
        table = self.original_table.get_table()
        table.setRowCount(7)  # 设置2行数据 + 5行空白行
        table.setColumnCount(8)
        headers = ['影响版本', '定位模块', '定位人', '问题引入模块', '是否补充RN', '引入版本', '修复版本', '备注']
        table.setHorizontalHeaderLabels(headers)
        for row in range(2):
            for col in range(8):
                item = QTableWidgetItem(f'({row}, {col})')
                table.setItem(row, col, item)
        self.copy_table(self.original_table.get_table(), self.filtered_table_widget.get_table())

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

    def clear_and_load_to_first_table(self):
        table1 = self.original_table.get_table()
        table2 = self.table_widget2.get_table()

        # 将第二个表格的数据加载到第一个表格的最后
        data = []
        for row in range(table2.rowCount()):
            row_data = []
            empty_row = True
            for col in range(table2.columnCount()):
                item = table2.item(row, col)
                cell_data = item.text() if item else ''
                if cell_data.strip():  # 如果单元格不为空
                    empty_row = False
                row_data.append(cell_data)
            if not empty_row:  # 只添加非空行
                data.append(row_data)
        
        # 清空第二个表格并保留空白行
        table2.clearContents()
        table2.setRowCount(5)

        # 将数据加载到第一个表格的最后
        current_row_count = table1.rowCount()
        table1.setRowCount(current_row_count + len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                table1.setItem(current_row_count + row_idx, col_idx, item)

        # 保存两个表格数据
        self.save_data()

        QMessageBox.information(self, "操作成功", "数据已从第二个表格加载到第一个表格并保存")

if __name__ == "__main__":
    app = QApplication([])

    # 创建一个示例表格
    example_table1 = TableWidget.create_table_widget()
    example_table1_table = example_table1.get_table()
    for row in range(3):
        for col in range(8):
            example_table1_table.setItem(row, col, QTableWidgetItem(str((row + 1) * (col + 1))))

    example_table2 = TableWidget.create_table_widget()
    example_table2_table = example_table2.get_table()
    for row in range(2):
        for col in range(8):
            example_table2_table.setItem(row, col, QTableWidgetItem(str((row + 1) + (col + 1))))

    window = RnSummaryUserWindow(example_table1)
    window.show()

    app.exec()
