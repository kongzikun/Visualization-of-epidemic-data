import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import matplotlib
import pandas as pd
import qtawesome

import numpy
#import wget
matplotlib.use("Qt5Agg")

print("666")
def spider2():
    ##Download the latest data
    #url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
    #wget.download(url)
    global a
    ##Read the data
    data = pd.read_excel(
        'COVID-19-geographic-disbtribution-worldwide.xlsx')
    a = data.groupby('dateRep').sum()
    print()
    # print(a)
    # print(a.iloc[:, 3])


class Mydemo(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        spider2()
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(2, 1, 1)
        self.axes1 = self.fig.add_subplot(2, 1, 2)

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
        self.layout = QVBoxLayout(self)
        self.setFixedSize(960, 700)
        self.figure1 = Mydemo(width=5, height=4, dpi=100)
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
        self.layout.addWidget(self.figure1)
        #data1 = list(range(1000))
        self.figure1.axes.plot(a.iloc[:, 4], label='死亡')
        self.figure1.axes1.plot(a.iloc[:, 3], label='确诊')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Try()
    ui.show()
    sys.exit(app.exec_())
