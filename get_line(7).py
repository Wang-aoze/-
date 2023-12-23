import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
from bs4 import BeautifulSoup
import csv
import datetime
import requests
import json
import re
import time
import csv
import os
import pypinyin
import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("公交车查询")
        self.setWindowIcon(QIcon('bus.png'))
        self.setGeometry(100, 100, 500, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout_main = QVBoxLayout()
        self.central_widget.setLayout(self.layout_main)

        self.label_title = QLabel("公交车查询", self.central_widget)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 30px; color: #333; font-weight: bold; margin-top: 30px; margin-bottom: 20px;")
        self.layout_main.addWidget(self.label_title)

        self.label_icon = QLabel(self.central_widget)
        pixmap = QPixmap('bus.png')
        self.label_icon.setPixmap(pixmap.scaledToWidth(200))  # 调整图片大小
        self.label_icon.setAlignment(Qt.AlignCenter)
        self.layout_main.addWidget(self.label_icon)
        self.layout_input = QHBoxLayout()
        self.layout_main.addLayout(self.layout_input)

        self.label_city = QLabel("城市：", self.central_widget)
        self.label_city.setFixedWidth(60)
        self.label_city.setStyleSheet("font-size: 16px; color: #333; font-weight: bold;")
        self.layout_input.addWidget(self.label_city)

        self.city_edit = QLineEdit(self.central_widget)
        self.city_edit.setFixedWidth(200)
        self.city_edit.setStyleSheet("font-size: 16px; color: #333; border: 2px solid #ccc; border-radius: 8px; padding: 5px;")
        self.layout_input.addWidget(self.city_edit)

        self.button = QPushButton("查询", self.central_widget)
        self.button.setStyleSheet("font-size: 16px; color: #fff; background-color: #06C; border-radius: 8px; padding: 5px 10px;")
        self.layout_input.addWidget(self.button)
        self.button.clicked.connect(self.open_second_window)

        self.label_clock = QLabel(self.central_widget)
        self.label_clock.setAlignment(Qt.AlignCenter)
        self.label_clock.setStyleSheet("font-size: 20px; color: #333; font-weight: bold; margin-top: 20px;")
        self.layout_main.addWidget(self.label_clock)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def open_second_window(self):
        city = self.city_edit.text()

        if city:
            self.second_window = SecondWindow(city)
            self.second_window.show()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_clock.setText(current_time)


class SecondWindow(QMainWindow):
    def __init__(self, city):
        super().__init__()

        self.setWindowTitle("公交车查询")
        self.setWindowIcon(QIcon('bus.png'))
        self.setGeometry(100, 100, 600, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout_main = QVBoxLayout()
        self.central_widget.setLayout(self.layout_main)

        self.label_title = QLabel(f"{city}公交车查询", self.central_widget)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 24px; color: #333; font-weight: bold; margin-top: 30px; margin-bottom: 20px;")
        self.layout_main.addWidget(self.label_title)

        self.layout_input = QHBoxLayout()
        self.layout_main.addLayout(self.layout_input)

        self.label_line = QLabel("线路号：", self.central_widget)
        self.label_line.setFixedWidth(80)
        self.label_line.setStyleSheet("font-size: 16px; color: #333; font-weight: bold;")
        self.layout_input.addWidget(self.label_line)

        self.line_edit = QLineEdit(self.central_widget)
        self.line_edit.setFixedWidth(200)
        self.line_edit.setStyleSheet("font-size: 16px; color: #333; border: 2px solid #ccc; border-radius: 8px; padding: 5px;")
        self.layout_input.addWidget(self.line_edit)

        self.search_button = QPushButton("按线路查询", self.central_widget)
        self.search_button.setStyleSheet("font-size: 16px; color: #fff; background-color: #06C; border-radius: 8px; padding: 5px 10px;")
        self.layout_input.addWidget(self.search_button)
        self.search_button.clicked.connect(self.search_by_line)

        self.layout_input_2 = QHBoxLayout()
        self.layout_main.addLayout(self.layout_input_2)

        self.label_station = QLabel("车站名：", self.central_widget)
        self.label_station.setFixedWidth(80)
        self.label_station.setStyleSheet("font-size: 16px; color: #333; font-weight: bold;")
        self.layout_input_2.addWidget(self.label_station)

        self.station_edit = QLineEdit(self.central_widget)
        self.station_edit.setFixedWidth(200)
        self.station_edit.setStyleSheet("font-size: 16px; color: #333; border: 2px solid #ccc; border-radius: 8px; padding: 5px;")
        self.layout_input_2.addWidget(self.station_edit)

        self.search_button_2 = QPushButton("按车站查询", self.central_widget)
        self.search_button_2.setStyleSheet("font-size: 16px; color: #fff; background-color: #06C; border-radius: 8px; padding: 5px 10px;")
        self.layout_input_2.addWidget(self.search_button_2)
        self.search_button_2.clicked.connect(self.search_by_station)

        def get_location(city, line, mykey):
            print("请耐心等待")
            url_api = 'https://restapi.amap.com/v3/bus/linename?city={}&keywords={}&key={}&extensions=all'.format(city,line,mykey)
            res = requests.get(url_api).text
            rt = json.loads(res)
            i = 0
            line_name = rt['buslines'][0]['name']
            polyline = rt['buslines'][0]['polyline']
            info = [line_name, polyline]
            stop = rt['buslines'][0]['busstops']
            type = rt['buslines'][0]['type']  # 线路类型
            name = rt['buslines'][0]['name']  # 线路名称
            start_time = rt['buslines'][0]['start_time']  # 开始营运时间
            end_time = rt['buslines'][0]['end_time']  # 停止营运时间
            time_buy = ''
            try:
                time_buy = start_time + '--' + end_time
            except:
                pass
            company = rt['buslines'][0]['company']  # 公交公司
            distance = rt['buslines'][0]['distance']  # 总里程
            basic_price = rt['buslines'][0]['basic_price']  # 参考票价
            form_lines = ""
            for i in range(len(stop)):
                station = stop[i]['name']
                location = stop[i]['location']
                info_ = [line, station, location]
                form_lines += info_[1]
                if i != (len(stop) - 1):
                    form_lines += ','
                if (i + 1) % 4 == 0:
                    form_lines += '\n'
            back_lines = ""
            # 上述为正向路线，下述为反向路线
            for i in range(len(stop)):
                station = stop[len(stop) - i - 1]['name']
                location = stop[len(stop) - i - 1]['location']
                info_ = [line, station, location]
                back_lines += info_[1]
                if i != (len(stop) - 1):
                    back_lines += ','
                if (i + 1) % 4 == 0:
                    back_lines += '\n'

            # 线路名称--------name
            # 线路类型--------type
            # 运行时间--------time_buy
            # 总里程----------distance
            # 公交公司---------company
            # 正向路线---------form_lines
            # 反向路线---------back_lines

            return [name, type, time_buy, distance, company, form_lines, back_lines]

        def main(city):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'}
            # city = input("输入城市中文名称:")
            # if city:
            print("爬取中")
            pinyin_list = pypinyin.pinyin(city, style=pypinyin.NORMAL)  # 设置pypinyin的拼音风格为带声调的拼音
            pinyin_city = ''.join([item[0] for item in pinyin_list])
            all_url = f'https://{pinyin_city}.8684.cn/'
            start_html = requests.get(all_url, headers=headers)

            Soup = BeautifulSoup(start_html.text, 'html.parser')
            all_a = Soup.find('div', class_="bus-layer depth w120").find_all('a')

            for a in all_a:
                Network_list = []
                href = a['href']
                html = all_url + href
                second_html = requests.get(html, headers=headers)
                Soup2 = BeautifulSoup(second_html.text, 'html.parser')
                try:
                    all_a2 = Soup2.find('div', class_='list clearfix').find_all('a')
                except:
                    continue
                for a2 in all_a2:
                    title1 = a2.get_text()
                    Network_list.append(title1)
                filename = f"data_{city}.txt"
                file = open(filename, 'a')
                file.write(str(Network_list))
                file.close()


            f = open(f'data_{city}.txt', encoding='gbk')  # 载入的txt文件
            txt = []
            for line in f:  # 它将读取文件中的每一行，并将其存储在变量line中。然后，它使用正则表达式r"'(.*?)'"来查找每个行中以单引号括起来的子字符串，并将这些子字符串存储在变量matches中。最后，这个代码片段将匹配到的所有子字符串存储在一个名为data的列表中
                word = line
            pattern = r"'(.*?)'"
            matches = re.findall(pattern, word)
            data = list(matches)
            a = 0
            # city_chinese="长沙"#城市名称
            f = open(f'{city}公交路线.csv', 'a', encoding='utf-8-sig', newline="")
            csv_writer = csv.writer(f)
            # 构建列表头
            csv_writer.writerow(["线路名称", "线路类型", "运行时间", "总里程", "公交公司", "正向路线", "反向路线"])
            mykey = ['8e389fd8b3702f13e25c08bc8597254c', 'c6c6be310712bd43cdc2ed6697f410e3',
                     '0b56b5920e8b821212eec4c6e29ec614', '0cff5270130766ca60064716d933ca2a',
                     '30254372c5905c194be7f559bab417bc', 'a993ed09d22b3b37040efc80ebde788f',
                     '2ef85a59111146c712c2397d53f403d7', 'e3645c6ec750c1ab8f9da48bc799d9e5',
                     '617292d2f1fbd3ffc3941697d6797933', 'fa9e529c6ec07a1066da0c5e60f64acf',
                     '06842c0b424618c420fbb9876558cac7', 'baa4f672e8fd466bd4a57ad128ee82e6']
            # key提供者鸣谢（顺序）：韩建智，覃康松，徐程，徐鑫，张建波，徐英琪，葛垠鲁，孙一城，田斌,刘涵，张昊哲，李佳儒
            line_num = len(data)
            key_num = len(mykey)
            num_state = int(line_num / key_num)
            state = 0
            for i in data:
                time.sleep(0.5)
                a += 1
                if a % num_state == 0:
                    state += 1
                if a == 1:  # 加载数量
                    break
                try:
                    line_data = get_location(city, i, mykey[state])
                    csv_writer.writerow(line_data)
                except:
                    pass
            print(f'已完成，输出结果保存在：{city}公交路线.csv')
            f.close()

        csv_filename = f'{city}公交路线.csv'
        if not os.path.exists(csv_filename):
            main(city)
        else:
            # 如果文件已经存在
            print(f"{csv_filename} 文件已存在，可直接查询")

        self.result_text = QTextEdit(self.central_widget)
        self.result_text.setStyleSheet("font-size: 16px; color: #333; border: 2px solid #ccc; border-radius: 8px; padding: 5px;")
        self.layout_main.addWidget(self.result_text)

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
