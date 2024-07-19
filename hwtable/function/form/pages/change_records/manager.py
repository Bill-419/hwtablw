import sys
import pandas as pd
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QApplication, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
from function.form.operation.table.table import TableWidget
from function.database.database import MongoDBHandler

class ChangeRecordsManagerWindow(QMainWindow):
    def __init__(self, table=None):
        super().__init__()
        self.setWindowTitle("进展与规划")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        # MongoDB 配置
        self.db_handler = MongoDBHandler("mongodb://localhost:27017/", "mydatabase", "change_records")

        # 创建并添加表格
        if table is None:
            self.table_widget = TableWidget.create_table_widget()
        else:
            self.table_widget = TableWidget(table)

        self.layout.addWidget(self.table_widget)

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

        self.layout.addLayout(button_layout)

        # 加载表格数据
        self.load_table_data()

    def add_summary_row(self):
        table = self.table_widget.get_table()
        summary_row_idx = table.rowCount()
        table.insertRow(summary_row_idx)
        for col in range(table.columnCount()):
            col_sum = 0
            all_numbers = True
            all_blank = True
            for row in range(summary_row_idx):
                item = table.item(row, col)
                if item and item.text().strip():
                    all_blank = False
                    if item.text().replace('.', '', 1).isdigit():
                        col_sum += float(item.text())
                    else:
                        all_numbers = False
                        break
            summary_item = QTableWidgetItem()
            if all_numbers and not all_blank:
                summary_item.setText(str(col_sum))
            summary_item.setForeground(QColor(Qt.black))  # 设置字体颜色为黑色
            summary_item.setBackground(QColor(Qt.yellow))  # 设置背景颜色为黄色
            summary_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            table.setItem(summary_row_idx, col, summary_item)

    def save_data(self):
        # 保存数据到 MongoDB
        table = self.table_widget.get_table()
        # 删除最后一行（总和行）
        if table.rowCount() > 0:
            table.removeRow(table.rowCount() - 1)
        
        data = []
        headers = ['测试领域', '序号', '平台名称', '镜像信息', '平台owner', 'PI3测试用例总数', 'PI3用例测试进展', 'TR4A用例测试进展', 'TR5用例总数', 'TR5用例测试进展']
        
        for row in range(table.rowCount()):
            row_data = {}
            for col, header in enumerate(headers):
                item = table.item(row, col)
                if item:
                    font = item.font()
                    row_data[header] = {
                        'text': item.text(),
                        'foreground': item.foreground().color().name(),
                        'background': item.background().color().name(),
                        'alignment': item.textAlignment(),
                        'font': {
                            'bold': font.bold(),
                            'size': font.pointSize()
                        },
                        'row_height': table.rowHeight(row),
                        'column_width': table.columnWidth(col)
                    }
                else:
                    row_data[header] = {
                        'text': '',
                        'foreground': QColor(Qt.black).name(),
                        'background': QColor(Qt.white).name(),
                        'alignment': int(Qt.AlignLeft | Qt.AlignVCenter),
                        'font': {
                            'bold': False,
                            'size': 10
                        },
                        'row_height': table.rowHeight(row),
                        'column_width': table.columnWidth(col)
                    }
            data.append(row_data)

        # 保存合并单元格信息
        merged_cells = []
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                if table.rowSpan(row, col) > 1 or table.columnSpan(row, col) > 1:
                    merged_cells.append({
                        'row': row,
                        'col': col,
                        'row_span': table.rowSpan(row, col),
                        'col_span': table.columnSpan(row, col)
                    })

        self.db_handler.save_table(data)
        self.db_handler.save_merged_cells(merged_cells)
        QMessageBox.information(self, "保存成功", "表格数据已保存到数据库")
        # 重新添加总和行
        self.add_summary_row()

    def refresh_data(self):
        # 刷新数据的逻辑
        table = self.table_widget.get_table()
        if table.rowCount() > 0:
            table.removeRow(table.rowCount() - 1)
        self.load_table_data()

        table = self.table_widget.get_table()
        if table.rowCount() > 0:
            table.removeRow(table.rowCount() - 2)
        print("数据已刷新")

    def export_to_excel(self):
        table = self.table_widget.get_table()
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
        data = self.db_handler.get_table()
        if data:
            self.populate_table(data)
        else:
            self.populate_table_with_default_data()
        self.add_summary_row()

    def populate_table(self, data):
        table = self.table_widget.get_table()
        table.clearContents()  # 清空现有数据
        table.setRowCount(len(data))
        table.setColumnCount(10)
        headers = ['测试领域', '序号', '平台名称', '镜像信息', '平台owner', 'PI3测试用例总数', 'PI3用例测试进展', 'TR4A用例测试进展', 'TR5用例总数', 'TR5用例测试进展']
        table.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(headers):
                cell_data = row_data.get(header, {})
                if isinstance(cell_data, dict):
                    item = QTableWidgetItem(cell_data.get('text', ''))
                    item.setForeground(QColor(cell_data.get('foreground', QColor(Qt.black).name())))
                    item.setBackground(QColor(cell_data.get('background', QColor(Qt.white).name())))
                    item.setTextAlignment(cell_data.get('alignment', int(Qt.AlignLeft | Qt.AlignVCenter)))
                    font = item.font()
                    font.setBold(cell_data.get('font', {}).get('bold', False))
                    font.setPointSize(cell_data.get('font', {}).get('size', 10))
                    item.setFont(font)
                    table.setItem(row_idx, col_idx, item)
                    table.setRowHeight(row_idx, cell_data.get('row_height', table.rowHeight(row_idx)))
                    table.setColumnWidth(col_idx, cell_data.get('column_width', table.columnWidth(col_idx)))
                else:
                    item = QTableWidgetItem(cell_data)
                    item.setForeground(QColor(Qt.black))
                    item.setBackground(QColor(Qt.white))
                    table.setItem(row_idx, col_idx, item)

        # 加载合并单元格信息
        merged_cells = self.db_handler.get_merged_cells()
        for cell in merged_cells:
            table.setSpan(cell['row'], cell['col'], cell['row_span'], cell['col_span'])

    def populate_table_with_default_data(self):
        table = self.table_widget.get_table()
        table.setRowCount(2)
        table.setColumnCount(11)
        headers = ['测试领域', '序号', '平台名称', '镜像信息', '平台owner', 'PI3测试用例总数', 'PI3用例测试进展', 'TR4A用例测试进展', 'TR5用例总数', 'TR5用例测试进展']
        table.setHorizontalHeaderLabels(headers)
        for row in range(2):
            for col in range(11):
                item = QTableWidgetItem(f'({row}, {col})')
                item.setForeground(QColor(Qt.black))  # 设置字体颜色为黑色
                item.setBackground(QColor(Qt.white))  # 设置背景颜色为白色
                table.setItem(row, col, item)
        self.add_summary_row()

if __name__ == "__main__":
    app = QApplication([])

    window = ChangeRecordsManagerWindow()
    window.show()

    app.exec()
