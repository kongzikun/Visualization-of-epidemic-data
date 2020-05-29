import pandas as pd
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget
from PyQt5 import QtWidgets,QtCore, QtGui
import sys
from sys import argv
import qtawesome
data = pd.read_excel('COVID-19-geographic-disbtribution-worldwide.xlsx')


#Change it to the country of your choice
country = str(argv[1])
print(str(argv[1]))

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
        self.lebal1 = QtWidgets.QLabel("                            "+country+"目前死亡率：" + str(
            total_death_percentage) + "%" + "\n\n                            "+country+"总确诊人数：" + str(
            data.Cases.sum()) + "人" + "\n\n                             "+country+"总死亡人数:" + str(data.Deaths.sum()) + "人")
        self.layout.addWidget(self.pushButton)
        self.layout.addWidget(self.lebal1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Try()
    ui.show()
    sys.exit(app.exec_())