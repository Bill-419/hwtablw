# import sys
# import re
# from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QApplication, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QLineEdit, QMenu, QInputDialog, QLabel, QDialog
# from PySide6.QtGui import QAction, QColor
# from PySide6.QtCore import Qt
# import pandas as pd
# from function.form.operation.table.table_user import TableUserWidget, CustomTableWidget
# from function.form.operation.menu.menu_user import MenuUserOperations

# class CollectPainPointUserWindow(QMainWindow):
#     def __init__(self, table=None):
#         super().__init__()
#         self.setWindowTitle("进展与规划")
#         self.setGeometry(100, 100, 800, 600)

#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)

#         layout = QVBoxLayout(central_widget)

#         # 创建搜索功能布局
#         search_layout = QHBoxLayout()
#         self.search_input = QLineEdit()
#         self.search_input.setPlaceholderText("输入搜索条件（支持正则表达式）")
#         search_button = QPushButton("搜索")
#         search_button.clicked.connect(self.apply_search)
#         search_layout.addWidget(self.search_input)
#         search_layout.addWidget(search_button)
#         layout.addLayout(search_layout)

#         # 原始表格数据
#         if table is None:
#             self.original_table_widget = TableUserWidget.create_table_user_widget()
#         else:
#             self.original_table_widget = TableUserWidget(table)

#         # 设置列标题
#         self.set_column_headers(self.original_table_widget.get_table_user())

#         # 副本表格，用于显示筛选结果
#         self.filtered_table_widget = CustomTableWidget(self.original_table_widget.get_table_user().rowCount(), self.original_table_widget.get_table_user().columnCount())
#         self.copy_table(self.original_table_widget.get_table_user(), self.filtered_table_widget)

#         # 创建筛选输入框布局
#         self.filter_inputs = []
#         self.create_filter_inputs(layout, self.filtered_table_widget.columnCount())

#         layout.addWidget(self.filtered_table_widget)

#         # 创建按钮布局
#         button_layout = QHBoxLayout()

#         # 添加保存按钮
#         save_button = QPushButton("保存")
#         save_button.clicked.connect(self.save_data)
#         button_layout.addWidget(save_button)

#         # 添加刷新按钮
#         refresh_button = QPushButton("刷新")
#         refresh_button.clicked.connect(self.refresh_data)
#         button_layout.addWidget(refresh_button)

#         # 添加导出为Excel按钮
#         export_button = QPushButton("导出为Excel")
#         export_button.clicked.connect(self.export_to_excel)
#         button_layout.addWidget(export_button)

#         # 添加新增提交按钮
#         new_entry_button = QPushButton("新增提交")
#         new_entry_button.clicked.connect(self.show_new_entry_window)
#         button_layout.addWidget(new_entry_button)

#         layout.addLayout(button_layout)

#         # 连接表头右击事件
#         self.filtered_table_widget.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
#         self.filtered_table_widget.horizontalHeader().customContextMenuRequested.connect(self.open_header_menu)

#         # 初始化筛选条件字典
#         self.filter_conditions = {}

#     def set_column_headers(self, table):
#         headers = [f"列 {col + 1}" for col in range(table.columnCount())]
#         table.setHorizontalHeaderLabels(headers)

#     def create_filter_inputs(self, layout, num_filters):
#         filter_layout = QHBoxLayout()
#         for i in range(num_filters):
#             filter_input = QLineEdit()
#             filter_input.setPlaceholderText(f"筛选条件{i + 1}")
#             filter_layout.addWidget(filter_input)
#             self.filter_inputs.append(filter_input)
        
#         filter_button = QPushButton("确定")
#         filter_button.clicked.connect(self.apply_combined_filter)
#         filter_layout.addWidget(filter_button)
        
#         layout.addLayout(filter_layout)

#     def open_header_menu(self, position):
#         menu = QMenu()

#         # 获取被点击的列
#         column = self.filtered_table_widget.horizontalHeader().logicalIndexAt(position)

#         # 创建筛选动作
#         filter_action = QAction(f"筛选第 {column + 1} 列", self)
#         filter_action.triggered.connect(lambda: self.filter_column(column))
#         menu.addAction(filter_action)

#         menu.exec(self.filtered_table_widget.horizontalHeader().mapToGlobal(position))

#     def filter_column(self, column):
#         filter_text, ok = QInputDialog.getText(self, "筛选", f"输入筛选条件 (第 {column + 1} 列):")
#         if ok:
#             self.filter_conditions[column] = filter_text.strip().lower()
#             self.apply_combined_filter()

#     def apply_combined_filter(self):
#         self.copy_table(self.original_table_widget.get_table_user(), self.filtered_table_widget)  # 每次筛选前重置副本表格
#         for row in range(self.filtered_table_widget.rowCount()):
#             match = True
#             for col, filter_input in enumerate(self.filter_inputs):
#                 filter_text = filter_input.text().strip().lower()
#                 if filter_text:
#                     item = self.filtered_table_widget.item(row, col)
#                     if item is None or filter_text not in item.text().lower():
#                         match = False
#                         break
#             self.filtered_table_widget.setRowHidden(row, not match)

#     def apply_search(self):
#         search_text = self.search_input.text().strip()
#         if not search_text:
#             return
#         self.copy_table(self.original_table_widget.get_table_user(), self.filtered_table_widget)  # 每次搜索前重置副本表格
#         pattern = re.compile(search_text, re.IGNORECASE)
#         for row in range(self.filtered_table_widget.rowCount()):
#             match = False
#             for col in range(self.filtered_table_widget.columnCount()):
#                 item = self.filtered_table_widget.item(row, col)
#                 if item and pattern.search(item.text()):
#                     match = True
#                     break
#             self.filtered_table_widget.setRowHidden(row, not match)

#     def save_data(self):
#         # 保存数据的逻辑
#         table = self.original_table_widget.get_table_user()
#         data = []
#         for row in range(table.rowCount()):
#             row_data = []
#             for col in range(table.columnCount()):
#                 item = table.item(row, col)
#                 row_data.append(item.text() if item else '')
#             data.append(row_data)
#         print("数据已保存:", data)

#     def refresh_data(self):
#         # 刷新数据的逻辑
#         self.copy_table(self.original_table_widget.get_table_user(), self.filtered_table_widget)
#         for row in range(self.filtered_table_widget.rowCount()):
#             self.filtered_table_widget.setRowHidden(row, False)  # 显示所有行
#         self.filter_conditions.clear()  # 清空筛选条件
#         for filter_input in self.filter_inputs:
#             filter_input.clear()
#         self.search_input.clear()  # 清空搜索输入框
#         print("数据已刷新")

#     def export_to_excel(self):
#         table = self.filtered_table_widget
#         path, _ = QFileDialog.getSaveFileName(self, "导出为Excel", "", "Excel Files (*.xlsx)")
#         if path:
#             data = []
#             for row in range(table.rowCount()):
#                 row_data = []
#                 for col in range(table.columnCount()):
#                     item = table.item(row, col)
#                     row_data.append(item.text() if item else '')
#                 data.append(row_data)
#             df = pd.DataFrame(data)
#             df.to_excel(path, index=False, header=False)
#             QMessageBox.information(self, "导出成功", f"表格已成功导出到 {path}")

#     def copy_table(self, source_table, target_table):
#         target_table.setRowCount(source_table.rowCount())
#         target_table.setColumnCount(source_table.columnCount())
#         target_table.setHorizontalHeaderLabels([source_table.horizontalHeaderItem(col).text() for col in range(source_table.columnCount())])
#         for row in range(source_table.rowCount()):
#             for col in range(source_table.columnCount()):
#                 source_item = source_table.item(row, col)
#                 if source_item:
#                     target_item = QTableWidgetItem(source_item.text())
#                     target_item.setForeground(source_item.foreground())
#                     target_item.setBackground(source_item.background())
#                     target_table.setItem(row, col, target_item)

#     def show_new_entry_window(self):
#         new_entry_window = QDialog(self)
#         new_entry_window.setWindowTitle("新增提交")
#         new_entry_window.setGeometry(150, 150, 600, 400)

#         new_entry_layout = QVBoxLayout(new_entry_window)

#         # 固定的列标题和文本内容
#         column_titles = ["标题1", "标题2", "标题3", "标题4"]
#         fixed_texts = ["固定内容1", "固定内容2", "固定内容3", "固定内容4"]

#         # 创建用于显示固定文本信息的布局
#         info_layout = QHBoxLayout()
#         for text in fixed_texts:
#             label = QLabel(text)
#             label.setStyleSheet("background-color: white; color: black; padding: 5px; border: 1px solid black;")
#             info_layout.addWidget(label)
        
#         new_entry_layout.addLayout(info_layout)

#         # 创建只有一行的表格
#         single_row_table = CustomTableWidget(1, len(column_titles))
#         single_row_table.setHorizontalHeaderLabels(column_titles)
#         new_entry_layout.addWidget(single_row_table)

#         # 添加保存和刷新按钮
#         button_layout = QHBoxLayout()
#         save_button = QPushButton("保存")
#         save_button.clicked.connect(lambda: self.save_new_entry(single_row_table))
#         button_layout.addWidget(save_button)

#         refresh_button = QPushButton("刷新")
#         refresh_button.clicked.connect(lambda: self.refresh_new_entry(single_row_table))
#         button_layout.addWidget(refresh_button)

#         new_entry_layout.addLayout(button_layout)

#         new_entry_window.exec()

#     def save_new_entry(self, single_row_table):
#         # 保存新增条目的逻辑
#         data = []
#         for col in range(single_row_table.columnCount()):
#             item = single_row_table.item(0, col)
#             data.append(item.text() if item else '')
#         print("新增数据已保存:", data)

#     def refresh_new_entry(self, single_row_table):
#         # 清空表格内容
#         for col in range(single_row_table.columnCount()):
#             single_row_table.setItem(0, col, QTableWidgetItem(''))

# if __name__ == "__main__":
#     app = QApplication([])

#     # 创建一个示例表格
#     example_table = CustomTableWidget(3, 4)
#     for row in range(3):
#         for col in range(4):
#             example_table.setItem(row, col, QTableWidgetItem(str((row + 1) * (col + 1))))

#     window = CollectPainPointUserWindow(example_table)
#     window.show()

#     app.exec()
