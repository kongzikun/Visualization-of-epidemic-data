import time
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import matplotlib
import qtawesome
import pandas as pd
import numpy
matplotlib.use("Qt5Agg")


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
provinces = []
now_confirm_list = []  # 现有确诊
confirm_list = []  # 确诊
suspect_list = []  # 疑似
dead_list = []  # 死亡
heal_list = []  # 治愈

class Mydemo(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        #spider()
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot()
        #self.axes1 = self.fig.add_subplot(2, 1, 2)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
class Try(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        # 抓取腾讯疫情实时json数据
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(
            time.time() * 1000)
        datas = json.loads(requests.get(url=url).json()['data'])
        # 设置全局变量
        global data
        data = datas['areaTree'][0]['children']
        data.sort(key=lambda x: x['total']['confirm'], reverse=True)  # 以item['total']['confirm']格式的值去做排序，将排序结果按降序排列
        # print(data)
        # 遍历data,获取各列数据
        for item in data:
            provinces.append(item['name'])
            confirm_list.append(item['total']['confirm'])
            now_confirm_list.append(item['total']['nowConfirm'])
            suspect_list.append(item['total']['suspect'])
            dead_list.append(item['total']['dead'])
            heal_list.append(item['total']['heal'])
        jx_city_list = []
        jx_confirm_list = []
        # 在各省数据里，找江西数据
        for item in data:
            if item['name'] == '江西':
                # 在江西遍历各市数据
                for item2 in item['children']:
                    # print(item2)
                    jx_city_list.append(item2['name'])
                    jx_confirm_list.append(item2['total']['confirm'])
                print(jx_city_list)
                print(jx_confirm_list)

        jx_city_list = []
        jx_confirm_list = []
        # 在各省数据里，找江西数据
        for item in data:
            if item['name'] == '江西':
                # 在江西遍历各市数据
                for item2 in item['children']:
                    # print(item2)
                    jx_city_list.append(item2['name'])
                    jx_confirm_list.append(item2['total']['confirm'])
                print(jx_city_list)
                print(jx_confirm_list)

                  # 跳出第一个循环

        self.layout = QVBoxLayout(self)
        self.setFixedSize(960, 700)
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # Dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.pushButton = QtWidgets.QPushButton(
            qtawesome.icon('fa.window-close', color='white'), "")
        self.pushButton.setGeometry(QtCore.QRect(30, 30, 28, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close)
        self.layout.addWidget(self.pushButton)
        self.figure1 = Mydemo(width=5, height=4, dpi=100)
        self.layout.addWidget(self.figure1)
        #data1 = list(range(1000))
        #self.figure1 = f.add_subplot()
        #self.figure1 = f.add_subplot()
        self.figure1.axes.pie(jx_confirm_list, labels=jx_city_list,
                    textprops={'fontsize': 6},radius=1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Try()
    ui.show()
    app.exec()