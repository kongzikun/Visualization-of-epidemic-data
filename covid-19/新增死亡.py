import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt 
#import wget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget
from PyQt5 import QtWidgets,QtCore, QtGui
import sys
import qtawesome
matplotlib.use("Qt5Agg")

##Download the latest data
#url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
#wget.download(url)

##Read the data
data = pd.read_excel('COVID-19-geographic-disbtribution-worldwide.xlsx')

#Change it to the country of your choice
country = 'China' 

##Reverse the data
data = data.reindex(index=data.index[::-1])

##Remove the dates with no cases
data = data[data.cases != 0]

##Remove useless columns
data = data.drop(columns=['day', 'month', 'year', 'geoId', 'countryterritoryCode', 'popData2018'])

## Make the name of the columns more clean
data.rename(columns={"countriesAndTerritories": "Country", 'dateRep': 'Date', 'cases': 'Cases', 'deaths': 'Deaths'}, inplace=True)

##Use only data for specific country
data = data[data['Country'].str.contains(country)]

## Total Death Percentage
total_death_percentage = data.Deaths.sum() / data.Cases.sum() * 100
print('\nTotal Death Percentage: ' + str(total_death_percentage) + '%')

## Total Cases and Deaths
print('Total Cases: ', data.Cases.sum())
print('Total Deaths: ', data.Deaths.sum())

## Calculate Death Percentage for Each Day
percentage = []
for i in data.index : 
    percentage.append(data['Deaths'][i] / data['Cases'][i] * 100)
data['Percentage'] = percentage 

## Print the minimized dataframe
print(data)

## Plot size
matplotlib.rcParams['figure.figsize'] = (10.0, 4.0)


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
        self.figure1.axes.plot(data.set_index('Date')['Cases'], color='blue', label='Cases')
        self.figure1.axes.plot(data.set_index('Date')['Deaths'], color='orange', label='Deaths')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Try()
    ui.show()
    sys.exit(app.exec_())

## Plot for Death Percentage
# ax = plt.subplot()
# ax.plot(data.set_index('Date')['Percentage'])
# ax.set(xlabel='Date', ylabel='Percentage', title='Death Percentage')
# ax.grid()
# plt.show()
#
# ## Plot for Cases And Deaths(Greece)
# ax = plt.subplot()
# ax.set(xlabel='Date', ylabel='People', title='Cases And Deaths')
# ax.plot(data.set_index('Date')['Cases'],color='blue', label='Cases')
# ax.plot(data.set_index('Date')['Deaths'], color='orange',label='Deaths')
# ax.grid()
# ax.legend()
# plt.show()

