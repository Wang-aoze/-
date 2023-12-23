import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("公交车查询")
        self.setGeometry(100, 100, 500, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("请输入查询的城市：", self.central_widget)
        self.layout.addWidget(self.label)

        self.city_edit = QLineEdit(self.central_widget)
        self.layout.addWidget(self.city_edit)

        self.button = QPushButton("查询", self.central_widget)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.open_second_window)

    def open_second_window(self):
        city = self.city_edit.text()

        if city:
            self.second_window = SecondWindow(city)
            self.second_window.show()


class SecondWindow(QMainWindow):
    def __init__(self, city):
        super().__init__()

        self.setWindowTitle("公交车查询")
        self.setGeometry(100, 100, 600, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.line_edit = QLineEdit(self.central_widget)
        self.layout.addWidget(self.line_edit)

        self.search_button = QPushButton("按线路查询", self.central_widget)
        self.layout.addWidget(self.search_button)
        self.search_button.clicked.connect(self.search_by_line)

        self.station_edit = QLineEdit(self.central_widget)
        self.layout.addWidget(self.station_edit)

        self.search_button_2 = QPushButton("按车站查询", self.central_widget)
        self.layout.addWidget(self.search_button_2)
        self.search_button_2.clicked.connect(self.search_by_station)

        self.result_text = QTextEdit(self.central_widget)
        self.layout.addWidget(self.result_text)

        self.city = city
        self.result_list = []

    def search_by_line(self):
        line_number = self.line_edit.text()
        self.search(self.city, line_number)

    def search_by_station(self):
        station_name = self.station_edit.text()
        self.search(self.city, station_name)

    def search(self, city, search_keyword):
        with open(f'{city}公交路线.csv', 'r', encoding='utf-8-sig', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)  # 将所有行存储为列表
            first_row = rows[0]  # 第一行数据
            self.result_list = []  # 初始化查询结果列表为空
            for row in rows[1:]:  # 从第二行开始遍历
                for i, column in enumerate(row):
                    if search_keyword in column:  # 进行部分匹配的模糊搜索
                        result = [f"{first_row[i]}: {row[i]}" for i in range(len(row))]
                        output_str = ', '.join(result)
                        self.result_list.append(output_str)
            self.update_result_text()  # 查询结束后更新文本框中的内容

    def update_result_text(self):
        self.result_text.setText('\n'.join(self.result_list))  # 将查询结果列表转换为字符串并显示在文本框中


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
