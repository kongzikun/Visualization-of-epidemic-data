# coding:utf-8

from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QFrame
import sys
import qtawesome 
import numpy as np
import os
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget
import matplotlib
import pandas as pd
import numpy
import wget
##Download the latest data
url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
wget.download(url)

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
#print(data)



class MainUi(QtWidgets.QMainWindow):
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("疫情数据分析软件")


    def init_ui(self):
        self.setFixedSize(960,700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.frame = QFrame(self)
        self.left_layout = QtWidgets.QGridLayout(self.frame)  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格
        self.main_widget.setStyleSheet('''
            QWidget#left_widget{
            background:gray;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
            }
            ''')

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格



        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_close.clicked.connect(self.close)
        self.left_visit = QtWidgets.QPushButton("") # 空白按钮
        self.left_visit.clicked.connect(self.showMaximized)
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_mini.clicked.connect(self.showMinimized)
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid blue;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        ''')
        self.left_label_1 = QtWidgets.QPushButton("国内疫情")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("全球疫情")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.area-chart',color='white'),"死亡/新增确诊")
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.clicked.connect(self.btn1_clicked)
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.pie-chart',color='white'),"江西疫情情况")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(self.btn2_clicked)
        self.left_button_3 = QtWidgets.QPushButton(
            qtawesome.icon('fa.line-chart', color='white'), "治愈/死亡率")
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.clicked.connect(self.btn3_clicked)
        self.left_button_4 = QtWidgets.QPushButton(
            qtawesome.icon('fa.bar-chart', color='white'), "确诊国家排名")
        self.left_button_4.setObjectName('left_button')
        self.left_button_4.clicked.connect(self.btn4_clicked)
        self.left_button_5 = QtWidgets.QPushButton(
            qtawesome.icon('fa.line-chart', color='white'), "治愈/死亡率")
        self.left_button_5.setObjectName('left_button')
        self.left_button_5.clicked.connect(self.btn5_clicked)
        self.left_button_6 = QtWidgets.QPushButton(
            qtawesome.icon('fa.area-chart', color='white'), "死亡/新增确诊")
        self.left_button_6.setObjectName('left_button')
        self.left_button_6.clicked.connect(self.btn6_clicked)
        self.left_button_7 = QtWidgets.QPushButton(
            qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_7.clicked.connect(self.btn7_clicked)
        self.left_button_8 = QtWidgets.QPushButton(
            qtawesome.icon('fa.info-circle', color='white'), "数据来源")
        self.left_button_8.setObjectName('left_button')
        self.left_button_8.clicked.connect(self.btn8_clicked)
        self.left_button_9 = QtWidgets.QPushButton(
            qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_9.setObjectName('left_button')
        self.left_button_9.clicked.connect(self.btn9_clicked)
        self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_mini, 0,0,1,1)
        self.left_layout.addWidget(self.left_close, 0, 2,1,1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1,1,0,1,3)
        self.left_layout.addWidget(self.left_button_1, 2, 0,1,3)
        self.left_layout.addWidget(self.left_button_2, 3, 0,1,3)
        self.left_layout.addWidget(self.left_button_3, 4, 0,1,3)
        self.left_layout.addWidget(self.left_label_2, 5, 0,1,3)
        self.left_layout.addWidget(self.left_button_4, 6, 0,1,3)
        self.left_layout.addWidget(self.left_button_5, 7, 0,1,3)
        self.left_layout.addWidget(self.left_button_6, 8, 0,1,3)
        self.left_layout.addWidget(self.left_label_3, 9, 0,1,3)
        self.left_layout.addWidget(self.left_button_7, 10, 0,1,3)
        self.left_layout.addWidget(self.left_button_8, 11, 0,1,3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小

        
        self.right_playlist_widget = QtWidgets.QWidget()  # 部件
        self.right_playlist_layout = QtWidgets.QGridLayout()  # 网格布局
        self.right_playlist_widget.setLayout(self.right_playlist_layout)


        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.right_widget.setStyleSheet('''
    QWidget#right_widget{
        color:#232C51;
        background:white;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-top-right-radius:10px;
        border-bottom-right-radius:10px;
    }
    QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
''')
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.search_icon.setObjectName('right_button')
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入你想要查询的国家的英文名，回车以查询该国家的情况")
        self.right_bar_widget_search_input.returnPressed.connect(self.lineEdit_function)

        self.right_bar_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)
        self.right_label_2 = QtWidgets.QLabel("                             中国目前死亡率："+str(total_death_percentage)+"%"+"\n\n                             中国总确诊人数："+str(data.Cases.sum())+"人"+"\n\n                             中国总死亡人数:"+str(data.Deaths.sum())+"人"+"\n\n\n\n2019新型冠状病毒，2020年1月12日被世界卫生组织命名为2019-nCoV ，2020年2月11日被国际病毒分类委员\n会命名为SARS-CoV-2 。美国《科学》杂志网站12日报道说，国际病毒分类学委员会冠状病毒研究小组主席约\n翰·齐布尔表示，他们是根据基因测序等方面的分类学研究提出这个名称，“这一名称与SARS疾病之间没有关\n联”。钟南山院士9日在接受媒体采访时也曾表示，新型冠状病毒与SARS冠状病毒是同一类，但不是同一种。\n   冠状病毒是一个大型病毒家族,已知可引起感冒以及中东呼吸综合征[MERS]和严重急性呼吸综合征[SARS]\n等较严重疾病.新型冠状病毒是以前从未在人体中发现的冠状病毒新毒株。2019年12月以来,湖北省武汉市持续\n开展流感及相关疾病监测,发现多起病毒性肺炎病例,均诊断为病毒性肺炎/肺部感染人感染了冠状病毒后常见\n体征有呼吸道症状:发热;咳嗽;气促和呼吸困难等.在较严重病例中,感染可导致肺炎;严重急性呼吸综合征;肾\n衰竭;甚至死亡.目前对于新型冠状病毒所致疾病没有特异治疗方法。但许多症状是可以处理的，因此需根据患\n者临床情况进行治疗。此外，对感染者的辅助护理可能非常有效。做好自我保护包括;保持基本的手部和呼吸\n道卫生,坚持安全饮食习惯,并尽可能避免与任何表现出有呼吸道疾病症状(如咳嗽和打喷嚏等)的人密切接触。\n\n    疫情爆发至今已经有四个多月的时间了，越来越多的人们投入到这场战‘疫’之中，他们奋斗在抵抗新冠\n病毒的第一防线，甚至为之奉献生命。\n  在这个严峻的时期，我以数据分析为主，基于大数据分析以可视化方式实时动态展现疫情发展，预测疫情为\n科学决策提供支持。")
        self.right_label_2.setObjectName('right_label')
        self.right_layout.addWidget(self.right_label_2, 1, 0, 1, 3)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)
        self.right_bar_widget_search_input.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')

        self.right_bar_widget_search_input.text()


    #def mail_setting(self):
        #log.debug("open mail settings")
        
        # 需要通过self实例化为全局变量，不加self的话，一运行就被回收，也就无法显示。
        #self.mail_set = Try()
        #self.mail_set.show()    

    def btn1_clicked(self):
        print("01")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/新增死亡.py")
    def btn2_clicked(self):
        print("02")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/江西数据.py")


    def btn3_clicked(self):
        print("03")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/中国死亡率.py")


    def btn4_clicked(self):
        print("04")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/确诊国家排名.py")


    def btn5_clicked(self):
        print("05")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/世界死亡率.py")



    def btn6_clicked(self):
        print("06")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/go.py")


    def btn7_clicked(self):
        print("07")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/反馈建议.py")


    def btn8_clicked(self):
        print("08")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/数据来源.py")


    def btn9_clicked(self):
        print("09")
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/遇到问题.py")


    def lineEdit_function(self):
        print("555")
        print(self.right_bar_widget_search_input.text())
        txt = str(self.right_bar_widget_search_input.text())
        os.system("C:\\ProgramData\\Anaconda3\\python.exe D:/covid-19/search1.py " + txt)

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
