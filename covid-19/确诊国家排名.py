import heapq
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget
from PyQt5 import QtWidgets,QtCore, QtGui
import sys
import qtawesome
matplotlib.use("Qt5Agg")


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


f = Figure(figsize=(10, 8), dpi=100)
# canvs = FigureCanvas(f, )

class Mydemo(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot()
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
        # ##Download the latest data
        # url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
        # # wget.download(url)
        global a
        ##Read the data
        data = pd.read_excel(
            'COVID-19-geographic-disbtribution-worldwide.xlsx')
        a = data.groupby('dateRep').sum()
        global b
        b = data.groupby('countriesAndTerritories').sum()
        global country_list
        countrys = data['countriesAndTerritories'].values
        country_list = []
        for i in countrys:
            if i not in country_list:
                country_list.append(i)
        confirmed_list = b.iloc[:, 3].values
        global confirmed_list_d
        confirmed_list_d = []
        for i in confirmed_list:
            confirmed_list_d.append(i)

        max_number = heapq.nlargest(10, confirmed_list_d)
        max_index = []
        country_list10 = []
        for t in max_number:
            index = confirmed_list_d.index(t)
            max_index.append(index)
            confirmed_list_d[index] = 0
        for i in max_index:
            country_list10.append(country_list[i])
        f_plot2 = f.add_subplot(111)
        f_plot2.pie(max_number, labels=country_list10,
                    textprops={'fontsize': 10}, radius=1)
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
        # data1 = list(range(1000))
        self.figure1.axes.pie(max_number, labels=country_list10,
                textprops={'fontsize': 10}, radius=1)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Try()
    main_window.show()
    app.exec()
