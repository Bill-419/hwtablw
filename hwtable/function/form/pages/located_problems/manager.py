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

    def save_merged_cells(self, merged_cells):
        self.collection.update_one({"type": "merged_cells"}, {"$set": {"merged_cells": merged_cells}}, upsert=True)

    def get_merged_cells(self):
        result = self.collection.find_one({"type": "merged_cells"})
        return result["merged_cells"] if result else []

    def append_table(self, data):
        self.collection.insert_many(data)

class RnSummaryUserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RN汇总")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # MongoDB 配置
        self.db_handler = MongoDBHandler("mongodb://localhost:27017/", "mydatabase", "summary")
        self.db_handler2 = MongoDBHandler("mongodb://localhost:27017/", "mydatabase", "other_collection")

        # 创建并添加第一个表格
        self.table_widget1 = TableWidget.create_table_widget()
        self.set_column_headers(self.table_widget1.get_table())

        layout.addWidget(self.table_widget1)

        # 创建第二个表格
        self.table_widget2 = TableWidget.create_table_widget()
        self.set_column_headers(self.table_widget2.get_table())

        layout.addWidget(self.table_widget2)

        # 创建按钮布局
        button_layout = QHBoxLayout()

        # 添加保存第一个表格按钮
        save_button1 = QPushButton("保存第一个表格")
        save_button1.clicked.connect(self.save_data1)
        button_layout.addWidget(save_button1)

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

        # 加载表格数据
        self.load_table_data()

    def set_column_headers(self, table):
        headers = ['影响版本', '定位模块', '定位人', '问题引入模块', '是否补充RN', '引入版本', '修复版本', '备注']
        table.setHorizontalHeaderLabels(headers)

    def save_data1(self):
        # 保存第一个表格数据到 MongoDB
        self._save_table_data(self.table_widget1.get_table(), self.db_handler, "第一个表格数据已保存")

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
        # 刷新第一个表格的数据
        data = self.db_handler.get_table()
        self.populate_table(self.table_widget1.get_table(), data)
        print("数据已刷新")

    def export_to_excel(self):
        table = self.table_widget1.get_table()
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
            self.populate_table(self.table_widget1.get_table(), data)
        else:
            self.populate_table_with_default_data()

    def populate_table(self, table, data):
        table.clearContents()  # 清空现有数据
        table.setRowCount(len(data))  # 不加空白行
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

    def populate_table_with_default_data(self):
        table = self.table_widget1.get_table()
        table.setRowCount(2)  # 设置2行数据
        table.setColumnCount(8)
        headers = ['影响版本', '定位模块', '定位人', '问题引入模块', '是否补充RN', '引入版本', '修复版本', '备注']
        table.setHorizontalHeaderLabels(headers)
        for row in range(2):
            for col in range(8):
                item = QTableWidgetItem(f'({row}, {col})')
                table.setItem(row, col, item)

    def clear_and_load_to_first_table(self):
        table1 = self.table_widget1.get_table()
        table2 = self.table_widget2.get_table()

        # 获取第二个表格的数据并添加到第一个表格的末尾
        data = self._extract_table_data(table2)
        self._append_data_to_table(table1, data)

        # 清空第二个表格并保留一行空白行
        table2.clearContents()
        table2.setRowCount(1)

        # 保存第一个表格数据到数据库
        self.save_data1()

        QMessageBox.information(self, "操作成功", "数据已从第二个表格加载到第一个表格并保存")

    def _extract_table_data(self, table):
        data = []
        headers = ['影响版本', '定位模块', '定位人', '问题引入模块', '是否补充RN', '引入版本', '修复版本', '备注']
        for row in range(table.rowCount()):
            row_data = {}
            empty_row = True
            for col, header in enumerate(headers):
                item = table.item(row, col)
                cell_data = item.text() if item else ''
                if cell_data.strip():  # 如果单元格不为空
                    empty_row = False
                row_data[header] = cell_data
            if not empty_row:  # 只添加非空行
                data.append(row_data)
        return data

    def _append_data_to_table(self, table, data):
        current_row_count = table.rowCount()
        table.setRowCount(current_row_count + len(data))
        headers = ['影响版本', '定位模块', '定位人', '问题引入模块', '是否补充RN', '引入版本', '修复版本', '备注']
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(headers):
                item = QTableWidgetItem(row_data[header])
                table.setItem(current_row_count + row_idx, col_idx, item)

if __name__ == "__main__":
    app = QApplication([])

    window = RnSummaryUserWindow()
    window.show()

    app.exec()
