# coding=utf-8
import csv
# from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pyqtgraph as pg
from scipy.optimize import curve_fit
import xlrd
#import xlwt

from PyQt5.QtWidgets import QDialog,QApplication,QFileDialog,QGridLayout,QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon,QPainter, QBrush,QColor
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# from Ui_pyqt_matplot import Ui_MainWindow
from pyqt_matplot1 import Ui_MainWindow
import matplotlib as mpl

import pandas as pd
# from openpyxl import load_workbook

'''
利用matplotlib画图，显示中文字符
'''
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文
mpl.rcParams['axes.unicode_minus'] = False # 设置支持负号显示

# # 在我的 notebook 里，要设置下面两行才能显示中文
# plt.rcParams['font.family'] = ['sans-serif']
# # 如果是在 PyCharm 里，只要下面一行，上面的一行可以删除
# plt.rcParams['font.sans-serif'] = ['SimHei']



#创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
    # #第四步：就是画图，【可以在此类中画，也可以在其它类中画】
    # def plotsin(self):
    #     self.axes0 = self.fig.add_subplot(111)
    #     t = np.arange(0.0, 3.0, 0.01)
    #     s = np.sin(2 * np.pi * t)
    #     self.axes0.plot(t, s)
    # def plotcos(self):
    #     t = np.arange(0.0, 3.0, 0.01)
    #     s = np.sin(2 * np.pi * t)
    #     self.axes.plot(t, s)




class MyMainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(MyMainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("至微生物  细菌感知检测系统")             #设置ui界面名字
        self.setMinimumSize(0, 0)

        # 第五步：定义MyFigure类的一个实例
        # self.F = MyFigure(width=3, height=2, dpi=100)
        # self.F1 = MyFigure(width=5, height=4, dpi=100)
        # self.F.plotsin()
        # self.plot_fit_data()
        # 第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox
        self.gridlayout1 = QGridLayout(self.groupBox_2)  # 继承容器groupBox
        # self.gridlayout.addWidget(self.F,0,1)

        # 补充：另创建一个实例绘图并显示
        # self.plotother()

        # ===========================================================
        #                       对Ui界面外加的功能，如：设置Menu菜单等
        # ===========================================================
        self.statusBar().showMessage('准备就绪')        #软件底部的状态栏


        exitAct = QAction('退出(&E)', self)     #创建一个具有特定图标和“退出”标签的动作 exitAct = QAction(QIcon('exit.png'), '退出(&E)', self)
        exitAct.setShortcut('Ctrl+Q')           #定义快捷方式
        exitAct.setStatusTip('退出程序')        #当我们将鼠标指针悬停在菜单项上时，第三行创建状态栏显示在状态栏中
        #当我们选择这个特定的动作时，发出触发信号。 信号连接到QApplication小部件的quit()方法。 这终止了应用程序。
        exitAct.triggered.connect(qApp.quit)

        saveMenu = QMenu('保存方式(&S)', self)
        saveAct = QAction( '保存...', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('保存文件')
        saveasAct = QAction(QIcon('saveas.png'), '另存为...(&O)', self)
        saveasAct.setStatusTip('文件另存为')
        saveMenu.addAction(saveAct)
        saveMenu.addAction(saveasAct)

        newAct = QAction( '新建(&N)', self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip('新建文件')

        #创建打开文件菜单，并连接到open_file函数和creat_table_show函数
        openfileAct = QAction('打开文件($Q)', self)
        openfileAct.setShortcut('Ctrl+Q')
        openfileAct.setStatusTip('打开文件')
        # 当我们选择这个特定的动作时，发出触发信号。 信号连接到open_file（）和creat_table_show方法。
        openfileAct.triggered.connect(self.open_file)
        openfileAct.triggered.connect(self.creat_table_show)  # 点击打开文件按钮 并读取原数据显示


        menubar = self.menuBar()                #menuBar（）方法创建一个菜单栏
        fileMenu = menubar.addMenu('文件(&F)')  #增加了“&”这个符号，增加这个符号后，当我们按住“Alt+F”的时候就能快速打开文件这个菜单
        fileMenu.addAction(openfileAct)
        fileMenu.addAction(newAct)              #addAction（）添加操作
        fileMenu.addMenu(saveMenu)              #addMenu（）创建文件菜单
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('帮助(&H)')  #并行增加了一个帮助菜单

        # ===========================================================
        #                   对Ui界面里面图的默认参数设置
        # ===========================================================


        # pg.setConfigOption('background', 'w')
        # pg.setConfigOption('foreground', 'k')
        # self.plot1.setAutoVisible(y=True)
        # self.plot2.setAutoVisible(y=True)
        # self.plot1.showGrid(True, True)     #对图生成网格，为了更好看
        # self.plot2.showGrid(True, True)     #对图生成网格，为了更好看

        # self.plot1.setConfigOption('background', 'w')
        # self.plot1.setConfigOption('foreground', 'k')
        # self.plot2.setConfigOption('background', 'w')
        # self.plot2.setConfigOption('foreground', 'k')

        # ===========================================================
        #       对Ui界面里面Qlabel或者Text Browser显示设置字体大小的
        # ===========================================================

        # 设置字体大小的
        font = QtGui.QFont()
        font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
        font.setPointSize(18)  # 括号里的数字可以设置成自己想要的字体大小
        # self.Result.setFont(font)


        # ===========================================================
        #       对QTableWidget 进行设置
        # ===========================================================
        # 对数据曲线交互表Interactive_Cells的操作
        # self.Interactive_Cells.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")       #设置表头背景色
        # self.Interactive_Cells.setStyleSheet("selection-background-color:Red;")  #设置选中背景色

        # self.Interactive_Cells.item(1, 0).setStyleSheet("QHeaderView::section{background:gray;}")

        # ===========================================================
        #              对数据显示表Data_Display_Cells的操作
        # ===========================================================
        self.Data_Display_Cells.setSelectionBehavior(QAbstractItemView.SelectRows)  #设置表格整行选中
        self.Data_Display_Cells.setEditTriggers(QAbstractItemView.NoEditTriggers)   #将表格变为禁止编辑

        # ===========================================================
        #              对颜色标注的设置操作
        # ===========================================================
        self.label_negative_dimgray.setStyleSheet('border-width: 1px;'
                                                   'border-style: solid;'
                                                   'border-color: dimgray;'
                                                   'background-color: dimgray;')
        self.label_positive_purple.setStyleSheet('border-width: 1px;'
                                                   'border-style: solid;'
                                                   'border-color: purple;'
                                                   'background-color: purple;')
        self.label_invalid_darkgray.setStyleSheet('border-width: 1px;'
                                                 'border-style: solid;'
                                                 'border-color: darkgray;'
                                                 'background-color: darkgray;')
        self.label_green.setStyleSheet('border-width: 1px;'
                                                 'border-style: solid;'
                                                 'border-color: green;'
                                                 'background-color: green;')
        self.label_orange.setStyleSheet('border-width: 1px;'
                                                 'border-style: solid;'
                                                 'border-color: orange;'
                                                 'background-color: orange;')
        self.label_red.setStyleSheet('border-width: 1px;'
                                                 'border-style: solid;'
                                                 'border-color: red;'
                                                 'background-color: red;')


        self.label_negative_dimgray_2.setStyleSheet('border-width: 1px;'
                                                  'border-style: solid;'
                                                  'border-color: dimgray;'
                                                  'background-color: dimgray;')
        self.label_positive_purple_2.setStyleSheet('border-width: 1px;'
                                                 'border-style: solid;'
                                                 'border-color: purple;'
                                                 'background-color: purple;')
        self.label_invalid_darkgray_2.setStyleSheet('border-width: 1px;'
                                                  'border-style: solid;'
                                                  'border-color: darkgray;'
                                                  'background-color: darkgray;')
        self.label_green_2.setStyleSheet('border-width: 1px;'
                                       'border-style: solid;'
                                       'border-color: green;'
                                       'background-color: green;')
        self.label_orange_2.setStyleSheet('border-width: 1px;'
                                        'border-style: solid;'
                                        'border-color: orange;'
                                        'background-color: orange;')
        self.label_red_2.setStyleSheet('border-width: 1px;'
                                     'border-style: solid;'
                                     'border-color: red;'
                                     'background-color: red;')

        self.label_green_3.setStyleSheet('border-width: 1px;'
                                         'border-style: solid;'
                                         'border-color: green;'
                                         'background-color: green;')
        self.label_orange_3.setStyleSheet('border-width: 1px;'
                                          'border-style: solid;'
                                          'border-color: orange;'
                                          'background-color: orange;')
        self.label_red_3.setStyleSheet('border-width: 1px;'
                                       'border-style: solid;'
                                       'border-color: red;'
                                       'background-color: red;')


        # ===========================================================
        #                       点击事件
        # ===========================================================
        self.Open_File.clicked.connect(self.open_file)  # 点击打开文件按钮 并显示文件路径
        # self.Open_File.clicked.connect(MyMainWindow.data_tianlong_matplotlib)
        self.Open_File.clicked.connect(self.creat_table_show)  # 点击打开文件按钮 并读取原数据显示


        self.Start_Plot.clicked.connect(self.plot_fit_data_matplotlib)  # 点击按键开始绘图
        self.Start_Plot.clicked.connect(self.Data_Display_Cells_show)   #第二页右下角计算数据的显示

        self.Export.clicked.connect(self.printExcel)    # 导出文件

        # self.vLine1 = pg.InfiniteLine(angle=90, movable=False)
        # self.hLine1 = pg.InfiniteLine(angle=0, movable=False)
        # self.plot1.addItem(self.vLine1, ignoreBounds=True)
        # self.plot1.addItem(self.hLine1, ignoreBounds=True)
        # self.vb1 = self.plot1.vb
        # # 将鼠标移动事件，设置触发函数self.mouseMoved
        # self.proxy = pg.SignalProxy(self.plot1.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)


        # self.plot.clicked.connect(self.plot_fit_data)  # 点击按键开始绘图
        # self.plot.clicked.connect(self.plot_fit_data)  # 点击按键开始绘图
        # self.plot.clicked.connect(self.plotother)



        #第五步：定义MyFigure类的一个实例
        # self.F = MyFigure(width=3, height=2, dpi=100)
        # self.F1 = MyFigure(width=5, height=4, dpi=100)
        #self.F.plotsin()
        #self.plot_fit_data()
        #第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。

        #self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox

        #self.gridlayout.addWidget(self.F,0,1)

        #补充：另创建一个实例绘图并显示
        #self.plotother()



        # ===========================================================
        #             Parameters
        # ===========================================================
        self.file_name=''

        self.x_axel = []            #x轴的值，循环数   列表
        self.x_axel_name = []       #x轴的名字        列表

        self.y_axel = []            #总的y值          列表中的列表
        self.y_axel1 = []           #第一个表的y值     列表中的列表
        self.y_axel2 = []           #第二个表的y值     列表中的列表
        self.y_axel_name = []       #y轴的名字        列表

        self.ct1 = []               # 第一个表的Ct值  列表
        self.ct2 = []               # 第一个表的Ct值  列表

        self.popt_all = []          #curve_fit后得到的两个sheet一起参数值      列表中的列表
        self.popt_1 = []            #curve_fit后得到的第一个sheet参数值        列表中的列表
        self.popt_2 = []            #curve_fit后得到的第二个sheet参数值        列表中的列表

        self.del_ct = []            #第一个表和第二个表的ΔCT值             列表
        self.del_ct_dic = []        #第一个表和第二个表的 名字和ΔCT值       字典


        self.del_del_ct_one = []    #数据只有一个竖列的第一个竖列的ΔΔCT值             列表
        self.del_del_ct_two = []    #数据只有两个竖列的第二个竖列的ΔΔCT值             列表
        self.del_del_ct_three = []  #数据只有三个竖列的第三个竖列的ΔΔCT值             列表
        self.del_del_ct_flor = []   #数据只有四个竖列的第四个竖列的ΔΔCT值             列表

        self.del2_ct = []           #ΔΔCT值，涵盖了上面的四个列表                                      列表中的列表
        self.del2_ct_flatten = []   #把ΔΔCT值拉成一维                                                 列表
        self.del_del_ct = []             #ΔΔCT值，涵盖了上面的四个列表,和del2_ct差不多，用于最后结果数据表的输出            列表中的列表


        self.x_axel1 = ['B','C', 'D', 'E', 'F', 'G', 'H']       #ΔΔCT图和孔位的图的横坐标：孔位

        # self.del_del_ct_one_name = []       #数据只有一个竖列的第一个竖列的名字             列表
        # self.del_del_ct_two_name = []       #数据只有两个竖列的第二个竖列的名字             列表
        # self.del_del_ct_three_name = []     #数据只有三个竖列的第三个竖列的名字             列表
        # self.del_del_ct_flor_name = []      #数据只有四个竖列的第四个竖列的名字             列表

        self.del_del_ct_one_name = [1,2,3,4,5,6]  # 数据只有一个竖列的第一个竖列的名字             列表
        self.del_del_ct_two_name = [7,8,9,10,11,12]  # 数据只有两个竖列的第二个竖列的名字             列表
        self.del_del_ct_three_name = [13,14,15,16,17,18]  # 数据只有三个竖列的第三个竖列的名字             列表
        self.del_del_ct_flor_name = [19,20,21,22,23,24]  # 数据只有四个竖列的第四个竖列的名字             列表

        self.del_del_ct_one_dic = []        #数据只有一个竖列的第一个竖列的名字和ΔΔCT值绑定            字典
        self.del_del_ct_two_dic = []        #数据只有两个竖列的第二个竖列的名字和ΔΔCT值绑定            字典
        self.del_del_ct_three_dic = []      #数据只有三个竖列的第三个竖列的名字和ΔΔCT值绑定            字典
        self.del_del_ct_flor_dic = []       #数据只有四个竖列的第四个竖列的名字和ΔΔCT值绑定            字典

        # 设置偏移量
        self.offset = 20

        self.analysis_report_table_list = ['优','良','中']




        self.printDict = {}








    #     # ===========================================================
    #     #                       画图函数-用的pyqtgrapth
    #     # ===========================================================
    #
    # def plot_fit_data_pyqtgrapth(self):
    #     x_axel, x_axel_name, y_axel, y_axel1, y_axel2, y_axel_name, popt_all, popt_1, popt_2, del_ct, del_ct_dic, \
    #     del_del_ct_one, del_del_ct_two, del_del_ct_three, del_del_ct_flor, del_del_ct, \
    #     del_del_ct_one_dic, del_del_ct_two_dic, del_del_ct_three_dic, del_del_ct_flor_dic, \
    #     del_del_ct_one_name, del_del_ct_two_name, del_del_ct_three_name, del_del_ct_flor_name = MyMainWindow.data_tianlong(self)
    #
    #     # =============第一张图--原始数据显示图==========
    #
    #
    #     """
    #             Set the label for an axis. Basic HTML formatting is allowed.
    #
    #             ==============  =================================================================
    #             **Arguments:**
    #             axis            must be one of 'left', 'bottom', 'right', or 'top'
    #             text            text to display along the axis. HTML allowed.
    #             units           units to display after the title. If units are given,
    #                             then an SI prefix will be automatically appended
    #                             and the axis values will be scaled accordingly.
    #                             (ie, use 'V' instead of 'mV'; 'm' will be added automatically)
    #             ==============  =================================================================
    #     """
    #     self.plot1.setLabel('left', "荧光值")      #设置y轴名称
    #     self.plot1.setLabel('bottom', "循环数")  #设置x轴名称
    #
    #
    #     #FAM
    #     for i in range(len(y_axel1)):
    #         self.plot1.plot(x_axel,MyMainWindow.func(x_axel, popt_1[i][0], popt_1[i][1], popt_1[i][2], popt_1[i][3],
    #                                       popt_1[i][4]), pen=pg.mkPen(width=2,color=pg.intColor(i),style=QtCore.Qt.SolidLine),name='red plot')
    #
    #     #VIC
    #     for i in range(len(y_axel2)):
    #         self.plot1.plot(x_axel,MyMainWindow.func(x_axel, popt_2[i][0], popt_2[i][1], popt_2[i][2], popt_2[i][3],
    #                                       popt_2[i][4]), pen=pg.mkPen(width=2,color=pg.intColor(i+1),style=QtCore.Qt.DashLine))
    #
    #     #总的
    #     # for i in range(len(y_axel)):
    #     #     self.plot1.plot(x_axel,MyMainWindow.func(x_axel, popt_all[i][0], popt_all[i][1], popt_all[i][2], popt_all[i][3],\
    #     #                       popt_all[i][4]), pen = pg.mkPen(width=2, color='b'))
    #
    #     # self.plot1.close()
    #
    #     # =============第二张图--孔数-ΔΔCT曲线==========
    #     # x_axel1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    #     yuzhi = [1] * 7
    #     if len(del_ct) // 8 == 1:
    #         label1 = y_axel_name[0][-1]
    #         self.plot2.plot(x_axel1, del_del_ct_one, pen=pg.mkPen(width=0.5,color='b'),symbol='s')
    #
    #         self.plot2.plot(x_axel1, yuzhi, linestyle='--', color='b', linewidth='2')
    #
    #         for i in range(len(del_del_ct_one)):
    #             self.plot2.annotate(text=del_del_ct_one_name[i], xy=(x_axel1[i], del_del_ct_one[i]),
    #                              xytext=(x_axel1[i], del_del_ct_one[i]))
    #
    #
    #         # 散点图
    #         # F1.axes.scatter(x_axel1, del_del_ct_one, marker='x', color='red', s=40, label=label1)
    #         # self.plot2.legend()
    #     elif len(del_ct) // 8 == 2:
    #         label1 = y_axel_name[0][-1]
    #         label2 = y_axel_name[1][-1]
    #         self.plot2.plot(x_axel1, del_del_ct_one, linestyle='-', marker='*', color='red', linewidth='2',
    #                      label=label1)
    #         self.plot2.plot(x_axel1, del_del_ct_two, linestyle='-', marker='d', color='g', linewidth='2',
    #                      label=label2)
    #
    #         self.plot2.plot(x_axel1, yuzhi, linestyle='--', color='b', linewidth='3')
    #
    #         for i in range(len(del_del_ct_one)):
    #             self.plot2.annotate(text=del_del_ct_one_name[i], xy=(x_axel1[i], del_del_ct_one[i]),
    #                              xytext=(x_axel1[i], del_del_ct_one[i]),textcoords="offset points")
    #             self.plot2.annotate(text=del_del_ct_two_name[i], xy=(x_axel1[i], del_del_ct_two[i]),
    #                              xytext=(x_axel1[i], del_del_ct_two[i]),textcoords="offset points")
    #
    #         # 散点图
    #         # F1.axes.scatter(x_axel1, del_del_ct_two1, marker='x', color='r', s=40, label=label1)
    #         # F1.axes.scatter(x_axel1, del_del_ct_two2, marker='+', color='g', s=40, label=label2)
    #         # self.plot2.legend()
    #     elif len(del_ct) // 8 == 3:
    #         label1 = y_axel_name[0][-1]
    #         label2 = y_axel_name[1][-1]
    #         label3 = y_axel_name[2][-1]
    #         self.plot2.plot(x_axel1, del_del_ct_one, linestyle='-', marker='*', color='red', linewidth='2',
    #                      label=label1)
    #         self.plot2.plot(x_axel1, del_del_ct_two, linestyle='-', marker='d', color='g', linewidth='2',
    #                      label=label2)
    #         self.plot2.plot(x_axel1, del_del_ct_three, linestyle='-', marker='o', color='purple', linewidth='2',
    #                      label=label3)
    #
    #         self.plot2.plot(x_axel1, yuzhi, linestyle='--', color='b', linewidth='3')
    #         # 散点图
    #         # F1.axes.scatter(x_axel1, del_del_ct_three1, marker='x', color='r', s=40, label=label1)
    #         # F1.axes.scatter(x_axel1, del_del_ct_three2, marker='+', color='g', s=40, label=label2)
    #         # F1.axes.scatter(x_axel1, del_del_ct_three3, marker='o', color='b', s=40, label=label3)
    #         self.plot2.legend()
    #     else:
    #         # label1 = x_axel_name[0][-1]
    #         # label2 = x_axel_name[1][-1]
    #         # label3 = x_axel_name[2][-1]
    #         # label4 = x_axel_name[3][-1]
    #         self.plot2.plot(x_axel1, del_del_ct_flor1, linestyle='-', marker='*', color='red', linewidth='2',
    #                      label='1')
    #         self.plot2.plot(x_axel1, del_del_ct_flor2, linestyle='-', marker='d', color='g', linewidth='2', label='2')
    #         self.plot2.plot(x_axel1, del_del_ct_flor3, linestyle='-', marker='o', color='purple', linewidth='2',
    #                      label='3')
    #         self.plot2.plot(x_axel1, del_del_ct_flor4, linestyle='-', marker='^', color='black', linewidth='2',
    #                      label='4')
    #
    #         self.plot2.plot(x_axel1, yuzhi, linestyle='--', color='b', linewidth='3')
    #         # 散点图
    #         # F1.axes.scatter(x_axel1, del_del_ct_flor1, marker='x', color='r', s=40, label='1')
    #         # F1.axes.scatter(x_axel1, del_del_ct_flor2, marker='+', color='g', s=40, label='2')
    #         # F1.axes.scatter(x_axel1, del_del_ct_flor3, marker='o', color='b', s=40, label='3')
    #         # F1.axes.scatter(x_axel1, del_del_ct_flor4, marker='^', color='black', s=40, label='4')
    #         self.plot2.legend()
    #     for key in list(del_ct_dic.keys()):
    #         if del_ct_dic[key] < 3:
    #             F1.axes.bar(key, del_ct_dic[key], fc='r')
    #             # pg.BarGraphItem(key, del_ct_dic[key],fc='r')
    #         else:
    #             F1.axes.bar(key, del_ct_dic[key], fc='g')
    #
    #     self.gridlayout.addWidget(F1, 0, 2)
    #
    #     # # 暂不用的图------柱状图，大于阈值为绿色，小于阈值为红色
    #     # # 柱状图plt.bar
    #     # F1 = MyFigure(width=5, height=4, dpi=100)
    #     # F1.fig.suptitle("孔数-Delta_ct曲线")
    #     # for key in list(del_ct_dic.keys()):
    #     #     if del_ct_dic[key] < 3:
    #     #         F1.axes.bar(key, del_ct_dic[key], fc='r')
    #     #         # pg.BarGraphItem(key, del_ct_dic[key],fc='r')
    #     #     else:
    #     #         F1.axes.bar(key, del_ct_dic[key], fc='g')
    #     # self.gridlayout.addWidget(F1, 0, 2)

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plot1.sceneBoundingRect().contains(pos):
            mousePoint = self.vb1.mapSceneToView(pos)
            # 一定要注意用float，这个bug花了一个小时才找出来。注意图中y值变化时刻的x，发现都是x超过整数时才变化，找出的本bug
            index = float(mousePoint.x())
            # 当未启动时，鼠标移动，只显示x的值
            if len(self.simulationTime) == 0:
                self.label1.setText(
                    "<span style='font-size: 12pt'>SimTime=%0.2f s,   <span style='color: white'>ConTime=   s</span>" % (
                        mousePoint.x()))
                # self.label1.setText("<span style='font-size: 12pt;color: white'>SimTime=%0.1f s, ConTime=    </span>" % (mousePoint.x()))
            # 调整，使label精确显示y值
            if len(self.simulationTime) >= 2 and index > self.simulationTime[0] and index < self.simulationTime[-1]:
                for i in range(len(self.simulationTime)):
                    if self.simulationTime[i] <= index < self.simulationTime[i + 1]:
                        self.label1.setText(
                            "<span style='font-size: 12pt'>SimTime=%0.2f s,   <span style='color: white'>ConTime=%0.2f s</span>" % (
                            mousePoint.x(), self.consensusLatency[i]))
                        break
            self.vLine1.setPos(mousePoint.x())
            self.hLine1.setPos(mousePoint.y())

    # def plotother_matplotlib(self):
    #     x_axel, x_axel_name, y_axel, y_axel1, y_axel2, y_axel_name, popt_all,popt_1, popt_2, del_ct, del_ct_dic = MainDialogImgBW.data_tianlong(file_name)
    #     F1 = MyFigure(width=5, height=4, dpi=100)
    #     F1.fig.suptitle("孔数-Delta_ct曲线")
    #     for key in list(del_ct_dic.keys()):
    #         if del_ct_dic[key] < 3:
    #             F1.axes.bar(key, del_ct_dic[key], fc='r')
    #             # pg.BarGraphItem(key, del_ct_dic[key],fc='r')
    #         else:
    #             F1.axes.bar(key, del_ct_dic[key], fc='g')
    #     self.gridlayout.addWidget(F1, 0, 2)


    # ===========================================================
    #                       打开文件函数
    # ===========================================================
    def open_file(self):

        file_name1 = QFileDialog.getOpenFileName(self, '打开文件','./')


        self.file_name=file_name1[0]

        self.File_Path.setText(self.file_name)





    # ===========================================================
    #                      第四个窗口显示excel原始数据
    # ===========================================================
    def creat_table_show(self):
        ###===========读取表格，转换表格，===========================================
        if len(self.file_name) > 0:
            input_table = pd.read_excel(self.file_name,sheet_name='FAM')     #读取第一个sheet 'FAM' 里面数据
            input_table1 = pd.read_excel(self.file_name, sheet_name='HEX')   #读取第二个sheet 'VIC' 里面数据
            # sheet1 = input_table.sheets()[0]
            # print(input_table)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]
            input_table_header = input_table.columns.values.tolist()
            # print(input_table_rows)         #32
            # print(input_table_colunms)      #18
            # print(input_table_header)       #['Unnamed: 0', '循环数', 'A2', 'A3', 'B2', 'B3', 'C2', 'C3', 'D2', 'D3', 'E2', 'E3', 'F2', 'F3', 'G2', 'G3', 'H2', 'H3']
            input_table_rows1 = input_table1.shape[0]
            input_table_colunms1 = input_table1.shape[1]
            input_table_header1 = input_table1.columns.values.tolist()

            ###===========读取表格，转换表格，============================================
            ###======================给tablewidget设置行列表头===========================

            self.Tablet_view_data.setColumnCount(input_table_colunms)
            self.Tablet_view_data.setRowCount(input_table_rows)
            self.Tablet_view_data.setHorizontalHeaderLabels(input_table_header)

            self.Tablet_view_data_2.setColumnCount(input_table_colunms1)
            self.Tablet_view_data_2.setRowCount(input_table_rows1)
            self.Tablet_view_data_2.setHorizontalHeaderLabels(input_table_header1)


            ###======================给tablewidget设置行列表头============================

            ###================遍历表格每个元素，同时添加到tablewidget中========================
            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
                # print(input_table_rows_values)
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                # print(input_table_rows_values_list)
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]
                    # print(input_table_items_list)
                    # print(type(input_table_items_list))

                    ###==============将遍历的元素添加到tablewidget中并显示=======================

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.Tablet_view_data.setItem(i, j, newItem)

                for i in range(input_table_rows1):
                    input_table_rows_values1 = input_table1.iloc[[i]]
                    # print(input_table_rows_values)
                    input_table_rows_values_array1 = np.array(input_table_rows_values1)
                    input_table_rows_values_list1 = input_table_rows_values_array1.tolist()[0]
                    # print(input_table_rows_values_list)
                    for j in range(input_table_colunms1):
                        input_table_items_list1 = input_table_rows_values_list1[j]
                        # print(input_table_items_list)
                        # print(type(input_table_items_list))

                        ###==============将遍历的元素添加到tablewidget中并显示=======================

                        input_table_items1 = str(input_table_items_list1)
                        newItem1 = QTableWidgetItem(input_table_items1)
                        newItem1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.Tablet_view_data_2.setItem(i, j, newItem1)

                    ###================遍历表格每个元素，同时添加到tablewidget中========================
        else:
            self.centralWidget.show()



    # ===========================================================
    #                       数据处理
    # ===========================================================
    def data_tianlong_matplotlib(self):
        '''
        读取数据
        '''

        xls = xlrd.open_workbook(self.file_name)
        sheet1 = xls.sheets()[0]
        sheet2 = xls.sheets()[1]

        '''
        X轴数据
        '''

        for i in range(1, sheet1.nrows):
            self.x_axel.append(sheet1.row_values(i)[1])
        self.x_axel_name = sheet1.row_values(0)[1]
        # print(x_axel_name)
        # print(x_axel)
        '''
        Y轴数据
        '''

        self.y_axel_name = sheet1.row_values(0)[2:]
        for i in range(2, len(self.y_axel_name) + 2):
            self.y_axel1.append(sheet1.col_values(i)[1:])
        for i in range(2, len(self.y_axel_name) + 2):
            self.y_axel2.append(sheet2.col_values(i)[1:])
        self.y_axel = self.y_axel1 + self.y_axel2
        # print(len(y_axel), y_axel)
        # print(len(y_axel1), y_axel1)
        # print(len(y_axel1), y_axel2)
        # print(y_axel_name)

        # Fuc_fit
        # param_bounds = ([-np.inf,0,15,-np.inf],[np.inf,np.inf,30,np.inf])
        param_bounds = ([-np.inf, -np.inf, -np.inf, 15, -np.inf], [np.inf, np.inf, np.inf, 35, np.inf])


        for i in range(len(self.y_axel)):
            popt=[]
            pcov=[]
            popt, pcov = curve_fit(MyMainWindow.func, self.x_axel, self.y_axel[i], bounds=param_bounds)
            # popt, pcov = curve_fit(MyMainWindow.func, self.x_axel, self.y_axel[i])
            self.popt_all.append(popt)
            if i < len(self.y_axel1):
                self.popt_1.append(popt)
                self.ct1.append(popt[3])
            else:
                self.popt_2.append(popt)
                self.ct2.append(popt[3])




        #print(popt_all)
        # print(len(popt_all))
        # print(len(xc1), xc1)
        # print(len(xc2), xc2)

        # delt CT的值
        # del_ct = []
        for i in range(len((self.y_axel1))):
            # del_ct.append(abs(xc2[i] - xc1[i]))
            self.del_ct.append(self.ct2[i] - self.ct1[i])
        # print(len(del_ct), del_ct)
        self.del_ct_dic = dict(zip(self.y_axel_name, self.del_ct))
        # print(del_ct_dic)



        # delt delt CT的值

        del2_ct = []

        if len(self.del_ct)//8==1:
            # del_del_ct_one=[del_ct[0]]

            self.del_del_ct.append([0])
            self.del2_ct = [[self.del_ct[0]]]

            for i in range(1,8):
                # del_del_ct_one.append(del_ct[i]-del_ct[1])

                self.del_del_ct_one.append(self.del_ct[i] - self.del_ct[1])

                self.del_del_ct[0].append(self.del_ct[i] - self.del_ct[1])

                self.del2_ct[0].append(self.del_ct[i]-self.del_ct[1])

                # self.del_del_ct_one_name.append(self.y_axel_name[i])

            del_del_ct_one_dic = dict(zip(self.del_del_ct_one_name, self.del_del_ct_one))

        elif len(self.del_ct)//8==2:
            # del_del_ct_two1 = [del_ct[0]]
            # del_del_ct_two2 = [del_ct[1]]

            self.del_del_ct.append([0])
            self.del_del_ct.append([0])

            self.del2_ct.append([self.del_ct[0]])
            self.del2_ct.append([self.del_ct[1]])

            for i in range(1,8):

                self.del_del_ct_one.append(self.del_ct[i * 2] - self.del_ct[2])
                self.del_del_ct_two.append(self.del_ct[i * 2 + 1] - self.del_ct[3])

                self.del_del_ct[0].append(self.del_ct[i * 2] - self.del_ct[2])
                self.del_del_ct[1].append(self.del_ct[i * 2 + 1] - self.del_ct[3])

                self.del2_ct[0].append(self.del_ct[i*2]-self.del_ct[2])
                self.del2_ct[1].append(self.del_ct[i*2+1]-self.del_ct[3])

                # self.del_del_ct_one_name.append(self.y_axel_name[i * 2])
                # self.del_del_ct_two_name.append(self.y_axel_name[i * 2 + 1])


            del_del_ct_one_dic = dict(zip(self.del_del_ct_one_name, self.del_del_ct_one))
            del_del_ct_two_dic = dict(zip(self.del_del_ct_two_name, self.del_del_ct_two))

        elif len(self.del_ct)//8==3:

            self.del_del_ct.append([0])
            self.del_del_ct.append([0])
            self.del_del_ct.append([0])

            self.del2_ct.append([self.del_ct[0]])
            self.del2_ct.append([self.del_ct[1]])
            self.del2_ct.append([self.del_ct[2]])


            for i in range(1,8):

                self.del_del_ct_one.append(self.del_ct[i * 3] -self.del_ct[3])
                self.del_del_ct_two.append(self.del_ct[i * 3 + 1] - self.del_ct[4])
                self.del_del_ct_three.append(self.del_ct[i * 3 + 2] - self.del_ct[5])

                self.del_del_ct[0].append(self.del_ct[i * 3] -self.del_ct[3])
                self.del_del_ct[1].append(self.del_ct[i * 3 + 1] - self.del_ct[4])
                self.del_del_ct[2].append(self.del_ct[i * 3 + 2] - self.del_ct[5])

                self.del2_ct[0].append(self.del_ct[i*3]-self.del_ct[3])
                self.del2_ct[1].append(self.del_ct[i*3+1]-self.del_ct[4])
                self.del2_ct[2].append(self.del_ct[i*3+2]-self.del_ct[5])

                # self.del_del_ct_one_name.append(self.y_axel_name[i * 3])
                # self.del_del_ct_two_name.append(self.y_axel_name[i * 3 + 1])
                # self.del_del_ct_three_name.append(self.y_axel_name[i * 3 + 2])

            del_del_ct_one_dic = dict(zip(self.del_del_ct_one_name, self.del_del_ct_one))
            del_del_ct_two_dic = dict(zip(self.del_del_ct_two_name, self.del_del_ct_two))
            del_del_ct_three_dic = dict(zip(self.del_del_ct_three_name, self.del_del_ct_three))

        else:

            self.del_del_ct.append([0])
            self.del_del_ct.append([0])
            self.del_del_ct.append([0])
            self.del_del_ct.append([0])

            self.del2_ct.append([self.del_ct[0]])
            self.del2_ct.append([self.del_ct[1]])
            self.del2_ct.append([self.del_ct[2]])
            self.del2_ct.append([self.del_ct[3]])

            for i in range(1, 8):

                self.del_del_ct_one.append(self.del_ct[i * 4] - self.del_ct[4])
                self.del_del_ct_two.append(self.del_ct[i * 4 + 1] - self.del_ct[5])
                self.del_del_ct_three.append(self.del_ct[i * 4 + 2] - self.del_ct[6])
                self.del_del_ct_flor.append(self.del_ct[i * 4 + 3] - self.del_ct[7])

                self.del_del_ct[0].append(self.del_ct[i * 4] - self.del_ct[4])
                self.del_del_ct[1].append(self.del_ct[i * 4 + 1] - self.del_ct[5])
                self.del_del_ct[2].append(self.del_ct[i * 4 + 2] - self.del_ct[6])
                self.del_del_ct[3].append(self.del_ct[i * 4 + 3] - self.del_ct[7])

                self.del2_ct[0].append(self.del_ct[i*4]-self.del_ct[4])
                self.del2_ct[1].append(self.del_ct[i*4+1]-self.del_ct[5])
                self.del2_ct[2].append(self.del_ct[i*4+2]-self.del_ct[6])
                self.del2_ct[3].append(self.del_ct[i*4+3]-self.del_ct[7])

                # self.del_del_ct_one_name.append(self.y_axel_name[i * 4])
                # self.del_del_ct_two_name.append(self.y_axel_name[i * 4 + 1])
                # self.del_del_ct_three_name.append(self.y_axel_name[i * 4 + 2])
                # self.del_del_ct_flor_name.append(self.y_axel_name[i * 4 + 3])

            del_del_ct_one_dic = dict(zip(self.del_del_ct_one_name, self.del_del_ct_one))
            del_del_ct_two_dic = dict(zip(self.del_del_ct_two_name, self.del_del_ct_two))
            del_del_ct_three_dic = dict(zip(self.del_del_ct_three_name, self.del_del_ct_three))
            del_del_ct_flor_dic = dict(zip(self.del_del_ct_flor_name, self.del_del_ct_flor))


        for j in range(8):
            for i in range(len(self.del2_ct)):
                self.del2_ct_flatten.append(self.del2_ct[i][j])

        # '''tip bug: 如果没有计算，就不会产生printDict变量，因此没有计算时，print按钮要不可用'''
        global printDict
        printDict = {'columnName':self.y_axel_name, 'xc1':self.ct1, 'xc2':self.ct2, 'del2_ct':self.del2_ct, 'del_ct':self.del_ct}

        # self.de


        return self.x_axel, self.x_axel_name, self.y_axel, self.y_axel1, self.y_axel2, self.y_axel_name, self.popt_all, self.popt_1, self.popt_2, self.del_ct, self.del_ct_dic, \
            self.del_del_ct_one, self.del_del_ct_two,self.del_del_ct_three,self.del_del_ct_flor,self.del_del_ct,\
            self.del_del_ct_one_dic,self.del_del_ct_two_dic,self.del_del_ct_three_dic,self.del_del_ct_flor_dic, \
            self.del_del_ct_one_name,self.del_del_ct_two_name,self.del_del_ct_three_name,self.del_del_ct_flor_name,\
            self.del2_ct_flatten


    # ===========================================================
    #                       最上角数据导出函数
    # ===========================================================
    def printExcel(self):

        ''' 把del2_ct的数据拉成一维，存放入del2_ct_flatten中 '''
        del2_ct = printDict['del2_ct']
        del2_ct_flatten = []
        for j in range(8):
            for i in range(len(del2_ct)):
                del2_ct_flatten.append(del2_ct[i][j])

        data = []  # 存储全部数据
        data.append(printDict['xc1'])
        data.append(printDict['xc2'])
        data.append(printDict['del_ct'])
        data.append(del2_ct_flatten)


        column = printDict['columnName']
        index = ['CTFam', 'CTVic', 'delt_CT', 'delt2_CT']
        df = pd.DataFrame(data=data, columns=column, index=index)
        df.index.name = '自定义参数'

        # print(file_name)
        # writer = pd.ExcelWriter(file_name, engine='openpyxl')
        # book = load_workbook(file_name)
        # writer.book = book
        # writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        # data.to_excel(writer, sheet_name='汇总',index=False)
        # writer.save()
        # print('导出成功！！')

        import xlwings
        wb = xlwings.Book(self.file_name)
        last_sheet_name=wb.sheets[-1].name
        # 在wb中新建一张新的sheet.可以指定位置
        sht = wb.sheets.add(name="汇总", before=None, after=last_sheet_name)
        # df.values 不然会插入df的索引
        sht.range("A1").value = df
        wb.save()
        wb.close()
        print('导出成功！！')


    # ===========================================================
    #                       定义函数拟合函数
    # ===========================================================
    def func(x, A=None, B=None, C=None, Xc=None, y0=None):
        # return A / (1 + exp(-B * (x - Xc))) + y0
        # data=A * (x - Xc)
        # if data>=0:
        #     return B / (1 + exp(-A * (x - Xc)))+y0
        # else:
        #     return B*exp(A * (x - Xc)) / (1 + exp(A * (x - Xc)))+y0
        # return B / (C + exp(-A * (x - Xc))) + y0

        return B * (C + np.tanh(A * (x - Xc))) + y0

    # ===========================================================
    #                       定义画图的多种颜色函数
    # ===========================================================
    def muty_color(self):
        # 添加随机多种颜色选择
        color = []
        for name, hex in matplotlib.colors.cnames.items():
            color.append(name)
        return color

    # ===========================================================
    #                       画图函数-用的matplotlib
    # ===========================================================

    def plot_fit_data_matplotlib(self):
        x_axel, x_axel_name, y_axel, y_axel1, y_axel2, y_axel_name, popt_all, popt_1, popt_2, del_ct, del_ct_dic, \
        del_del_ct_one, del_del_ct_two, del_del_ct_three, del_del_ct_flor, del_del_ct, \
        del_del_ct_one_dic, del_del_ct_two_dic, del_del_ct_three_dic, del_del_ct_flor_dic, \
        del_del_ct_one_name, del_del_ct_two_name, del_del_ct_three_name, del_del_ct_flor_name , del2_ct_flatten= MyMainWindow.data_tianlong_matplotlib(
            self)

        F = MyFigure(width=6, height=5, dpi=100)
       # F.fig.suptitle("函数拟合后的原始数据图")
        F.axes.set_xlabel('循环数')
        F.axes.set_ylabel('荧光强度值')


        color = MyMainWindow.muty_color(self)
        for i in range(len(y_axel)):
            F.axes.plot(x_axel,
                        MyMainWindow.func(x_axel, popt_all[i][0], popt_all[i][1], popt_all[i][2], popt_all[i][3],
                                             popt_all[i][4]), color=color[i], linestyle="-", marker='.')
        # for i in range(len((y_axel1))):
        #     F.axes.plot(x_axel, MainDialogImgBW.func(x_axel, popt_1[i][0], popt_1[i][1], popt_1[i][2], popt_1[i][3], popt_1[i][4]),
        #              color=color[i], linestyle="-", marker='.')
        #
        # for i in range(len((y_axel2))):
        #     # plt.plot(x_axel, y_axel[i], color=color[i],linestyle="-",marker='.')
        #     F.axes.plot(x_axel, MainDialogImgBW.func(x_axel, popt_2[i][0], popt_2[i][1], popt_2[i][2], popt_2[i][3], popt_2[i][4]),
        #              color=color[i], linestyle="-", marker='.')

        self.gridlayout.addWidget(F, 0, 1)

        F1 = MyFigure(width=5, height=4, dpi=100)
        #F1.fig.suptitle("孔数-ΔΔCT曲线")
        # x_axel1=['A','B','C','D','E','F','G','H']
        F1.axes.set_xlabel('孔数')
        F1.axes.set_ylabel('ΔΔCT值')

        x_axel1=self.x_axel1
        yuzhi = [1] * 6
        text1 = ''
        text2 = ''
        text3 = ''
        text4 = ''
        if len(del_ct) // 8 == 1:
            label1 = y_axel_name[0][-1]
            # F1.axes.plot(x_axel1, del_del_ct_one, linestyle='-', marker='*', color='red', linewidth='2', label=label1)

            F1.axes.plot(x_axel1[1:], yuzhi, linestyle='--', color='b', linewidth='1', label='标准线')

            # 在图上面每个点旁边标上标注
            # for i in range(len(del_del_ct_one)):
            #     F1.axes.annotate(text=del_del_ct_one_name[i], xy=(x_axel1[i], del_del_ct_one[i]),
            #                      xytext=(x_axel1[i], del_del_ct_one[i]))

            # 散点图
            # F1.axes.scatter(x_axel1, del_del_ct_one, marker='x', color='red', s=40, label=label1)

            if self.del_ct[1]>2:
                text1 = '第%s竖列阴性对照有问题，该列数据无效！\n\n' % label1
                MyMainWindow.background_color_negative_invalid(self,lable=label1)
            else:
                for i in range(1,7):
                    if del_del_ct_one[i]>1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='g', s=120, label=label1)
                        MyMainWindow.background_color(self, lable=label1, i=i, color='green',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=0)

                    elif del_del_ct_one[i]<0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='r', s=40, label=label1)
                        MyMainWindow.background_color(self, lable=label1, i=i, color='red',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='orange', s=40, label=label1)
                        MyMainWindow.background_color(self, lable=label1, i=i, color='orange',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=2)

                    F1.axes.annotate(text=del_del_ct_one_name[i-1], xy=(x_axel1[i], del_del_ct_one[i]),
                                     xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')


            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=label1,
                                         input_table_items_list=self.ct1)  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=label1,
                                         input_table_items_list=self.ct2)  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=label1,
                                         input_table_items_list=self.del_ct)  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=label1,
                                         input_table_items_list=self.del2_ct_flatten)  # 步长为2取值


            # F1.axes.legend()






        elif len(del_ct) // 8 == 2:
            label1 = y_axel_name[0][-1]
            label2 = y_axel_name[1][-1]
            #折线图
            # F1.axes.plot(x_axel1, del_del_ct_one, linestyle='-', marker='*', color='red', linewidth='2', label=label1)
            # F1.axes.plot(x_axel1, del_del_ct_two, linestyle='-', marker='d', color='g', linewidth='2', label=label2)

            F1.axes.plot(x_axel1[1:], yuzhi, linestyle='--', color='b', linewidth='1', label='标准线')

            #在图上面每个点旁边标上标注
            # for i in range(len(del_del_ct_one)):
            #     F1.axes.annotate(text=del_del_ct_one_name[i], xy=(x_axel1[i], del_del_ct_one[i]),
            #                      xytext=(x_axel1[i], del_del_ct_one[i]), textcoords="offset points")
            #     F1.axes.annotate(text=del_del_ct_two_name[i], xy=(x_axel1[i], del_del_ct_two[i]),
            #                      xytext=(x_axel1[i], del_del_ct_two[i]), textcoords="offset points")

            # 散点图
            # F1.axes.scatter(x_axel1, del_del_ct_two1, marker='x', color='r', s=40, label=label1)
            # F1.axes.scatter(x_axel1, del_del_ct_two2, marker='+', color='g', s=40, label=label2)



            if self.del_ct[2]>2:
                text1 = '第%s竖列阴性对照有问题，该列数据无效！\n' % label1
                MyMainWindow.background_color_negative_invalid(self, lable=label1)
            else:
                #画图
                for i in range(1,7):
                    if del_del_ct_one[i]>1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='g', s=120, label=label1)

                        MyMainWindow.background_color(self,lable=label1,i=i,color='green',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self,i=i,three_of_one=0)

                    elif del_del_ct_one[i]<0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='r', s=40, label=label1)

                        MyMainWindow.background_color(self, lable=label1,i=i,color='red',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='orange', s=40, label=label1)

                        MyMainWindow.background_color(self, lable=label1,i=i,color='orange',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=2)

                    #添标注
                    F1.axes.annotate(text=del_del_ct_one_name[i-1], xy=(x_axel1[i], del_del_ct_one[i]),
                                         xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')


            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=label1, input_table_items_list=self.ct1[::2])   #步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=label1, input_table_items_list=self.ct2[::2])   #步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=label1, input_table_items_list=self.del_ct[::2])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=label1, input_table_items_list=self.del2_ct_flatten[::2])  # 步长为2取值


            if self.del_ct[3]>2:
                text2 = '第%s竖列阴性对照有问题，该列数据无效！\n\n' % label2
                MyMainWindow.background_color_negative_invalid(self, lable=label2)
            else:
                for i in range(1,7):
                    if del_del_ct_two[i] > 1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o',  color='g', s=120, label=label2)

                        MyMainWindow.background_color(self, lable=label2,i=i,color='green',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i+6, three_of_one=0)
                    elif del_del_ct_two[i] < 0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o', color='r', s=40, label=label2)

                        MyMainWindow.background_color(self, lable=label2,i=i,color='red',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 6, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o', color='orange', s=40,label=label2)

                        MyMainWindow.background_color(self, lable=label2,i=i,color='orange',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 6, three_of_one=2)

                    #添加标注
                    F1.axes.annotate(text=del_del_ct_two_name[i-1], xy=(x_axel1[i], del_del_ct_two[i]),
                                         xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')


            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=label2,input_table_items_list=self.ct1[1::2])   # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=label2, input_table_items_list=self.ct2[1::2])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=label2,
                                         input_table_items_list=self.del_ct[1::2])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=label2,
                                         input_table_items_list=self.del2_ct_flatten[1::2])  # 步长为2取值

            # F1.axes.legend()
            # F1.axes.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)




        elif len(del_ct) // 8 == 3:
            label1 = y_axel_name[0][-1]
            label2 = y_axel_name[1][-1]
            label3 = y_axel_name[2][-1]
            #折线图
            # F1.axes.plot(x_axel1, del_del_ct_one, linestyle='-', marker='*', color='red', linewidth='2', label=label1)
            # F1.axes.plot(x_axel1, del_del_ct_two, linestyle='-', marker='d', color='g', linewidth='2', label=label2)
            # F1.axes.plot(x_axel1, del_del_ct_three, linestyle='-', marker='o', color='purple', linewidth='2',
            #              label=label3)

            F1.axes.plot(x_axel1[1:], yuzhi, linestyle='--', color='b', linewidth='1', label='标准线')


            #在图上面每个点旁边标上标注
            # for i in range(len(del_del_ct_one)):
            #     F1.axes.annotate(text=del_del_ct_one_name[i], xy=(x_axel1[i], del_del_ct_one[i]),
            #                      xytext=(x_axel1[i], del_del_ct_one[i]))
            #     F1.axes.annotate(text=del_del_ct_two_name[i], xy=(x_axel1[i], del_del_ct_two[i]),
            #                      xytext=(x_axel1[i], del_del_ct_two[i] + 0.1))
            #     F1.axes.annotate(text=del_del_ct_three_name[i], xy=(x_axel1[i], del_del_ct_three[i]),
            #                      xytext=(x_axel1[i], del_del_ct_three[i] + 0.1))

            # 散点图，散点图可以逐个画点
            # F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='x', color='r', s=40, label=label1)
            # F1.axes.scatter(x_axel1, del_del_ct_two, marker='+', color='g', s=40, label=label2)
            # F1.axes.scatter(x_axel1, del_del_ct_three, marker='o', color='b', s=40, label=label3)

            if self.del_ct[3] > 2:
                text1 = '第%s竖列阴性对照有问题，该列数据无效！\n' % label1
                MyMainWindow.background_color_negative_invalid(self, lable=label1)
            else:
                for i in range(1,7):
                    if del_del_ct_one[i]>1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='g', s=120, label=label1)
                        MyMainWindow.background_color(self, lable=label1, i=i, color='green',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=0)
                    elif del_del_ct_one[i]<0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='r', s=40, label=label1)
                        MyMainWindow.background_color(self, lable=label1, i=i, color='red',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='orange', s=40, label=label1)
                        MyMainWindow.background_color(self, lable=label1, i=i, color='orange',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=2)

                    F1.axes.annotate(text=del_del_ct_one_name[i-1], xy=(x_axel1[i], del_del_ct_one[i]),
                                         xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')


            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=label1,
                                         input_table_items_list=self.ct1[::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=label1,
                                         input_table_items_list=self.ct2[::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=label1,
                                         input_table_items_list=self.del_ct[::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=label1,
                                         input_table_items_list=self.del2_ct_flatten[::3])  # 步长为2取值

            if self.del_ct[4] > 2:
                text2 = '第%s竖列阴性对照有问题，该列数据无效！\n' % label2
                MyMainWindow.background_color_negative_invalid(self, lable=label2)
            else:
                for i in range(1,7):
                    if del_del_ct_two[i] > 1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o',  color='g', s=120, label=label2)
                        MyMainWindow.background_color(self, lable=label2, i=i, color='green',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i+6, three_of_one=0)
                    elif del_del_ct_two[i] < 0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o', color='r', s=40, label=label2)
                        MyMainWindow.background_color(self, lable=label2, i=i, color='red',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 6, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o', color='orange', s=40,label=label2)
                        MyMainWindow.background_color(self, lable=label2, i=i, color='orange',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 6, three_of_one=2)
                    F1.axes.annotate(text=del_del_ct_two_name[i-1], xy=(x_axel1[i], del_del_ct_two[i]),
                                         xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')


            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=label2,
                                         input_table_items_list=self.ct1[1::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=label2,
                                         input_table_items_list=self.ct2[1::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=label2,
                                         input_table_items_list=self.del_ct[1::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=label2,
                                         input_table_items_list=self.del2_ct_flatten[1::3])  # 步长为2取值

            if self.del_ct[5] > 2:
                text3 = '第%s竖列阴性对照有问题，该列数据无效！\n\n' % label3
                MyMainWindow.background_color_negative_invalid(self, lable=label3)
            else:
                for i in range(1,7):
                    if del_del_ct_three[i] > 1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_three[i], marker='o', color='g', s=120, label=label3)
                        MyMainWindow.background_color(self, lable=label3, i=i, color='green',input_table_items_list=del_del_ct_three_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 12, three_of_one=0)
                    elif del_del_ct_three[i] < 0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_three[i], marker='o', color='r', s=40, label=label3)
                        MyMainWindow.background_color(self, lable=label3, i=i, color='red',input_table_items_list=del_del_ct_three_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 12, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_three[i], marker='o', color='orange', s=40, label=label3)
                        MyMainWindow.background_color(self, lable=label3, i=i, color='orange',input_table_items_list=del_del_ct_three_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 12, three_of_one=2)

                    F1.axes.annotate(text=del_del_ct_three_name[i-1], xy=(x_axel1[i], del_del_ct_three[i]),
                                         xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')

            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=label3,
                                         input_table_items_list=self.ct1[2::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=label3,
                                         input_table_items_list=self.ct2[2::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=label3,
                                         input_table_items_list=self.del_ct[2::3])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=label3,
                                         input_table_items_list=self.del2_ct_flatten[2::3])  # 步长为2取值




            # F1.axes.legend()



        else:
            # label1 = x_axel_name[0][-1]
            # label2 = x_axel_name[1][-1]
            # label3 = x_axel_name[2][-1]
            # label4 = x_axel_name[3][-1]

            #折线图
            # F1.axes.plot(x_axel1, del_del_ct_one, linestyle='-', marker='*', color='red', linewidth='2', label='1')
            # F1.axes.plot(x_axel1, del_del_ct_two, linestyle='-', marker='d', color='g', linewidth='2', label='2')
            # F1.axes.plot(x_axel1, del_del_ct_three, linestyle='-', marker='o', color='purple', linewidth='2', label='3')
            # F1.axes.plot(x_axel1, del_del_ct_flor, linestyle='-', marker='^', color='black', linewidth='2', label='4')

            F1.axes.plot(x_axel1[1:], yuzhi, linestyle='--', color='b', linewidth='1', label='标准线')
            # 散点图
            # F1.axes.scatter(x_axel1, del_del_ct_one, marker='x', color='r', s=40, label='1')
            # F1.axes.scatter(x_axel1, del_del_ct_two, marker='+', color='g', s=40, label='2')
            # F1.axes.scatter(x_axel1, del_del_ct_three, marker='o', color='b', s=40, label='3')
            # F1.axes.scatter(x_axel1, del_del_ct_flor, marker='^', color='black', s=40, label='4')

            # 在图上面每个点旁边标上标注
            # for i in range(len(del_del_ct_one)):
            #     F1.axes.annotate(text=del_del_ct_one_name[i], xy=(x_axel1[i], del_del_ct_one[i]),
            #                      xytext=(x_axel1[i], del_del_ct_one[i]))
            #     F1.axes.annotate(text=del_del_ct_two_name[i], xy=(x_axel1[i], del_del_ct_two[i]),
            #                      xytext=(x_axel1[i], del_del_ct_two[i] + 0.1))
            #     F1.axes.annotate(text=del_del_ct_three_name[i], xy=(x_axel1[i], del_del_ct_three[i]),
            #                      xytext=(x_axel1[i], del_del_ct_three[i] + 0.1))
            #     F1.axes.annotate(text=del_del_ct_flor_name[i], xy=(x_axel1[i], del_del_ct_flor[i]),
            #                      xytext=(x_axel1[i], del_del_ct_flor[i] + 0.1))

            if self.del_ct[4] > 2:
                text1 = '第1竖列阴性对照有问题，该列数据无效！\n'
                MyMainWindow.background_color_negative_invalid(self, lable=1)
            else:
                for i in range(1,7):
                    if del_del_ct_one[i]>1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='g', s=120, label='1')
                        MyMainWindow.background_color(self, lable=1, i=i, color='green',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=0)
                    elif del_del_ct_one[i]<0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='r', s=40, label='1')
                        MyMainWindow.background_color(self, lable=1, i=i, color='red',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_one[i], marker='o', color='orange', s=40, label='1')
                        MyMainWindow.background_color(self, lable=1, i=i, color='orange',input_table_items_list=del_del_ct_one_name)
                        MyMainWindow.analysis_report_table_color(self, i=i, three_of_one=2)
                    #点旁边标注
                    F1.axes.annotate(text=del_del_ct_one_name[i-1], xy=(x_axel1[i], del_del_ct_one[i]),
                                         xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')

            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=1,
                                         input_table_items_list=self.ct1[::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=1,
                                         input_table_items_list=self.ct2[::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=1,
                                         input_table_items_list=self.del_ct[::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=1,
                                         input_table_items_list=self.del2_ct_flatten[::4])  # 步长为2取值

            if self.del_ct[5] > 2:
                text2 = '第2竖列阴性对照有问题，该列数据无效！\n'
                MyMainWindow.background_color_negative_invalid(self, lable=2)
            else:
                for i in range(1,7):
                    if del_del_ct_two[i] > 1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o',  color='g', s=120, label='2')
                        MyMainWindow.background_color(self, lable=2, i=i, color='green',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i+6, three_of_one=0)
                    elif del_del_ct_two[i] < 0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o', color='r', s=40, label='2')
                        MyMainWindow.background_color(self, lable=2, i=i, color='red',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 6, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_two[i], marker='o', color='orange', s=40,label='2')
                        MyMainWindow.background_color(self, lable=2, i=i, color='orange',input_table_items_list=del_del_ct_two_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 6, three_of_one=2)
                    # 点旁边标注
                    F1.axes.annotate(text=del_del_ct_two_name[i-1], xy=(x_axel1[i], del_del_ct_two[i]),
                                     xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')

            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=2,
                                         input_table_items_list=self.ct1[1::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=2,
                                         input_table_items_list=self.ct2[1::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=2,
                                         input_table_items_list=self.del_ct[1::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=2,
                                         input_table_items_list=self.del2_ct_flatten[1::4])  # 步长为2取值


            if self.del_ct[6] > 2:
                text3 = '第3竖列阴性对照有问题，该列数据无效！\n'
                MyMainWindow.background_color_negative_invalid(self, lable=3)
            else:
                for i in range(1,7):
                    if del_del_ct_three[i] > 1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_three[i], marker='o', color='g', s=120, label='3')
                        MyMainWindow.background_color(self, lable=3, i=i, color='green',input_table_items_list=del_del_ct_three_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 12, three_of_one=0)
                    elif del_del_ct_three[i] < 0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_three[i], marker='o', color='r', s=40, label='3')
                        MyMainWindow.background_color(self, lable=3, i=i, color='red',input_table_items_list=del_del_ct_three_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 12, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_three[i], marker='o', color='orange', s=40, label='3')
                        MyMainWindow.background_color(self, lable=3, i=i, color='orange',input_table_items_list=del_del_ct_three_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 12, three_of_one=2)
                    # 点旁边标注
                    F1.axes.annotate(text=del_del_ct_three_name[i-1], xy=(x_axel1[i], del_del_ct_three[i]),
                                     xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')


            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=3,
                                         input_table_items_list=self.ct1[2::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=3,
                                         input_table_items_list=self.ct2[2::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=3,
                                         input_table_items_list=self.del_ct[2::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=3,
                                         input_table_items_list=self.del2_ct_flatten[2::4])  # 步长为2取值

            if self.del_ct[7] > 2:
                text4 = '第4竖列阴性对照有问题，该列数据无效！\n\n'
                MyMainWindow.background_color_negative_invalid(self, lable=4)
            else:
                for i in range(1,7):
                    if del_del_ct_flor[i] > 1.1:
                        F1.axes.scatter(x_axel1[i], del_del_ct_flor[i], marker='o', color='g', s=120, label='4')
                        MyMainWindow.background_color(self, lable=4, i=i, color='green',input_table_items_list=del_del_ct_flor_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 18, three_of_one=0)
                    elif del_del_ct_three[i] < 0.9:
                        F1.axes.scatter(x_axel1[i], del_del_ct_flor[i], marker='o', color='r', s=40, label='4')
                        MyMainWindow.background_color(self, lable=4, i=i, color='red',input_table_items_list=del_del_ct_flor_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 18, three_of_one=1)
                    else:
                        F1.axes.scatter(x_axel1[i], del_del_ct_flor[i], marker='o', color='orange', s=40, label='4')
                        MyMainWindow.background_color(self, lable=4, i=i, color='orange',input_table_items_list=del_del_ct_flor_name)
                        MyMainWindow.analysis_report_table_color(self, i=i + 18, three_of_one=2)
                    # 点旁边标注
                    F1.axes.annotate(text=del_del_ct_flor_name[i-1], xy=(x_axel1[i], del_del_ct_flor[i]),
                                     xytext=(0.4 *self.offset, -0.17 *self.offset), textcoords='offset points')


            # 数据表格显示
            MyMainWindow.data_table_show(self, Tablet=self.ct_fam_table, input_table_rows=8,
                                         input_table_colunm=4,
                                         input_table_items_list=self.ct1[3::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.ct_vic_table, input_table_rows=8,
                                         input_table_colunm=4,
                                         input_table_items_list=self.ct2[3::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_ct_table, input_table_rows=8,
                                         input_table_colunm=4,
                                         input_table_items_list=self.del_ct[3::4])  # 步长为2取值
            MyMainWindow.data_table_show(self, Tablet=self.del_del_ct_table, input_table_rows=8,
                                         input_table_colunm=4,
                                         input_table_items_list=self.del2_ct_flatten[3::4])  # 步长为2取值


            # F1.axes.legend()

        self.gridlayout1.addWidget(F1, 0, 1)


        # 对于最后结果数据表的输出
        ''' 把del2_ct的数据拉成一维，存放入del2_ct_flatten中 '''
        # print(len(del_del_ct),del_del_ct)
        # print(len(del_del_ct[0]),del_del_ct[0])
        del2_ct_flatten = []
        for j in range(8):
            for i in range(len(del_del_ct)):
                del2_ct_flatten.append(del_del_ct[i][j])

        result_dic1 = dict(zip(y_axel_name, del2_ct_flatten))
        # print(del_ct_dic)
        global result_dic
        result_dic = []

        for key in list(result_dic1.keys()):
            if result_dic1[key] > 1:
                result_dic.append(key)
                # del del_ct_dic[key]
            else:
                continue

        #判断实验阴性对照是否有问题

        if text1 or text2 or text3 or text4 != '':
            self.Result.setText("{}{}{}{}{}孔 消杀计量足够!\n\n消杀率：百分之99.9".format(text1,text2,text3,text4,result_dic))
        else:
            self.Result.setText("阴性对照组全部正常，实验有效！\n\n{}孔 消杀计量足够!\n\n消杀率：百分之99.9".format( result_dic))





    # ===========================================================
    #                    第二页右下角各孔计算数据显示
    # ===========================================================
    def Data_Display_Cells_show(self):
        self.Data_Display_Cells.setRowCount(len(self.y_axel_name))       #设置行数
        self.Data_Display_Cells.setVerticalHeaderLabels(self.y_axel_name)   #设置列表头
        Data_Display_Cells_table=[self.ct1,self.ct2,self.del_ct,self.del2_ct_flatten]
        for i in range(4):
            for j in range(len(self.y_axel_name)):
                newItem = QTableWidgetItem(str(Data_Display_Cells_table[i][j]).split('.')[0] + '.' + str(Data_Display_Cells_table[i][j]).split('.')[1][:3])
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.Data_Display_Cells.setItem(j, i, newItem)




    # ===========================================================
    #                    第三页的各孔计算数据显示
    # ===========================================================
    def data_table_show(self,Tablet,input_table_rows,input_table_colunm,input_table_items_list):
        for i in range(input_table_rows):
            ###==============将遍历的元素添加到tablewidget中并显示=======================
            # newItem = QTableWidgetItem(str(input_table_items_list[i]))
            newItem = QTableWidgetItem(str(input_table_items_list[i]).split('.')[0] + '.' + str(input_table_items_list[i]).split('.')[1][:3])
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            Tablet.setItem(i, (int(input_table_colunm)-1), newItem)


    # ===========================================================
    #                  设置单元格颜色
    # ===========================================================
    def background_color(self,lable,i,color,input_table_items_list):
        newItem = QTableWidgetItem(str(input_table_items_list[i - 1]))
        newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.Interactive_Cells.setItem(i, (int(lable) - 1), newItem)
        # self.analysis_report_table.setItem(i, (int(lable) - 1), newItem)



        self.Interactive_Cells.setItem(0, int(lable)-1, QtWidgets.QTableWidgetItem())
        self.Interactive_Cells.item(0, (int(lable)-1)).setBackground(QColor('dimgray'))

        self.Interactive_Cells.setItem(1, int(lable) - 1, QtWidgets.QTableWidgetItem())
        self.Interactive_Cells.item(1, (int(lable) - 1)).setBackground(QColor('purple'))

        # self.Interactive_Cells.setItem(i + 1, int(lable) - 1, QtWidgets.QTableWidgetItem())
        self.Interactive_Cells.setItem(i + 1, int(lable) - 1, newItem)
        self.Interactive_Cells.item(i + 1, (int(lable) - 1)).setBackground(QColor(color))



        self.analysis_report_table.setItem(0, int(lable)-1, QtWidgets.QTableWidgetItem())
        self.analysis_report_table.item(0, (int(lable)-1)).setBackground(QColor('dimgray'))

        self.analysis_report_table.setItem(1, int(lable) - 1, QtWidgets.QTableWidgetItem())
        self.analysis_report_table.item(1, (int(lable) - 1)).setBackground(QColor('purple'))

        # self.analysis_report_table.setItem(i + 1, int(lable) - 1, QtWidgets.QTableWidgetItem())
        self.analysis_report_table.setItem(i + 1, int(lable) - 1, QTableWidgetItem(str(input_table_items_list[i - 1])))
        self.analysis_report_table.item(i + 1, (int(lable) - 1)).setBackground(QColor(color))

    # ===========================================================
    #                  设置第一张报表单元格颜色
    # ===========================================================
    def analysis_report_table_color(self,i,three_of_one):
        newItem = QTableWidgetItem(str(self.analysis_report_table_list[three_of_one]))
        newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        if three_of_one==0:
            color='green'
        elif three_of_one==1:
            color = 'orange'
        else:
            color = 'red'

        if i<=12:
            Table=self.analysis_report_table_1

        else:
            Table = self.analysis_report_table_2
            i=i-12

        Table.setItem(i - 1, three_of_one, newItem)
        Table.item(i - 1, three_of_one).setBackground(QColor(color))



    def background_color_negative_invalid(self, lable):
        for j in range(8):
            self.Interactive_Cells.setItem(j, int(lable) - 1, QtWidgets.QTableWidgetItem())
            self.Interactive_Cells.item(j, (int(lable) - 1)).setBackground(QColor('darkgray'))

            self.analysis_report_table.setItem(j, int(lable) - 1, QtWidgets.QTableWidgetItem())
            self.analysis_report_table.item(j, (int(lable) - 1)).setBackground(QColor('darkgray'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MyMainWindow()
    main.show()
    #app.installEventFilter(main)
    sys.exit(app.exec_())

#pyinstaller -F -i 33.ico zwsw666_gui_v2.py -w

#pyuic5 -o pyqt_matplot1.py pyqt_matplot1.ui    ui文件转py文件