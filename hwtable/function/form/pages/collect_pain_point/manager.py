# import sys
# from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QApplication, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
# from PySide6.QtGui import QColor
# from PySide6.QtCore import Qt
# import pandas as pd
# from function.form.operation.table.table_limit import TableLimitWidget  # 确保导入正确

# class CollectPainPointManagerWindow(QMainWindow):
#     def __init__(self, table1=None, table2=None):
#         super().__init__()
#         self.setWindowTitle("进展与规划")
#         self.setGeometry(100, 100, 800, 600)

#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)

#         layout = QVBoxLayout(central_widget)

#         # 创建并添加第一个表格
#         if table1 is None:
#             self.table_widget1 = TableLimitWidget.create_table_widget()
#         else:
#             self.table_widget1 = TableLimitWidget(table1)

#         layout.addWidget(self.table_widget1)

#         # 创建并添加第二个表格
#         if table2 is None:
#             self.table_widget2 = TableLimitWidget.create_table_widget()
#         else:
#             self.table_widget2 = TableLimitWidget(table2)

#         layout.addWidget(self.table_widget2)

#         # 创建按钮布局
#         button_layout = QHBoxLayout()

#         # 添加第一个表格的保存按钮
#         save_button1 = QPushButton("保存第一个表格")
#         save_button1.clicked.connect(self.save_data1)
#         button_layout.addWidget(save_button1)

#         # 添加第一个表格的刷新按钮
#         refresh_button1 = QPushButton("刷新第一个表格")
#         refresh_button1.clicked.connect(self.refresh_data1)
#         button_layout.addWidget(refresh_button1)

#         # 添加第二个表格的保存按钮
#         save_button2 = QPushButton("保存第二个表格")
#         save_button2.clicked.connect(self.save_data2)
#         button_layout.addWidget(save_button2)

#         # 添加第二个表格的刷新按钮
#         refresh_button2 = QPushButton("刷新第二个表格")
#         refresh_button2.clicked.connect(self.refresh_data2)
#         button_layout.addWidget(refresh_button2)

#         # 添加导出为Excel按钮
#         export_button = QPushButton("导出为Excel")
#         export_button.clicked.connect(self.export_to_excel)
#         button_layout.addWidget(export_button)

#         layout.addLayout(button_layout)

#     def save_data1(self):
#         # 保存第一个表格的数据
#         self._save_table_data(self.table_widget1.get_table_limit(), "第一个表格数据已保存")

#     def save_data2(self):
#         # 保存第二个表格的数据
#         self._save_table_data(self.table_widget2.get_table_limit(), "第二个表格数据已保存")

#     def _save_table_data(self, table, message):
#         data = []
#         for row in range(table.rowCount()):
#             row_data = []
#             for col in range(table.columnCount()):
#                 item = table.item(row, col)
#                 row_data.append(item.text() if item else '')
#             data.append(row_data)
#         print(message, data)

#     def refresh_data1(self):
#         # 刷新第一个表格的数据
#         self._refresh_table_data(self.table_widget1.get_table_limit())
#         print("第一个表格数据已刷新")

#     def refresh_data2(self):
#         # 刷新第二个表格的数据
#         self._refresh_table_data(self.table_widget2.get_table_limit())
#         print("第二个表格数据已刷新")

#     def _refresh_table_data(self, table):
#         table.clearContents()

#     def export_to_excel(self):
#         # 导出第一个表格的数据
#         self._export_table_to_excel(self.table_widget1.get_table_limit(), "导出第一个表格为Excel")
#         # 导出第二个表格的数据
#         self._export_table_to_excel(self.table_widget2.get_table_limit(), "导出第二个表格为Excel")

#     def _export_table_to_excel(self, table, title):
#         path, _ = QFileDialog.getSaveFileName(self, title, "", "Excel Files (*.xlsx)")
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

# if __name__ == "__main__":
#     app = QApplication([])

#     # 创建两个示例表格
#     example_table1 = QTableWidget(3, 4)
#     for row in range(3):
#         for col in range(4):
#             example_table1.setItem(row, col, QTableWidgetItem(str((row + 1) * (col + 1))))

#     example_table2 = QTableWidget(2, 5)
#     for row in range(2):
#         for col in range(5):
#             example_table2.setItem(row, col, QTableWidgetItem(str((row + 1) + (col + 1))))

#     window = CollectPainPoint(example_table1, example_table2)
#     window.show()

#     app.exec()
