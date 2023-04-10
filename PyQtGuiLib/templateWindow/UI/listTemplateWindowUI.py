# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'listTemplateWindowUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQtGuiLib.header import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QSize,
    QPushButton,
    qt,
    QGridLayout
)

from PyQtGuiLib.core import SlideShow
from PyQtGuiLib.styles import QssStyleAnalysis


class ListTemplateWindowUI(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowTitle("ListTemplateWindow")
        self.setupUi()
        self.defaultStyle()

    def setupUi(self):
        self.resize(1229, 746)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_widget = QWidget(self)
        self.left_widget.setMaximumSize(QSize(260, 16777215))
        # self.left_widget.setStyleSheet("border: 1px solid rgb(170, 170, 127);")
        self.left_widget.setObjectName("left_widget")
        self.verticalLayout = QVBoxLayout(self.left_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_widget = QWidget(self.left_widget)
        self.title_widget.setMinimumSize(QSize(0, 100))
        self.title_widget.setMaximumSize(QSize(16777215, 100))
        # self.title_widget.setStyleSheet("border: 1px solid rgb(0, 85, 255);")
        self.title_widget.setObjectName("title_widget")
        self.verticalLayout.addWidget(self.title_widget)
        self.listWidget = QListWidget(self.left_widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout.addWidget(self.left_widget)
        self.body_widget = QWidget(self)
        # self.body_widget.setStyleSheet("border: 1px solid rgb(0, 170, 255);")
        self.body_widget.setObjectName("body_widget")
        self.verticalLayout_2 = QVBoxLayout(self.body_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.head_widget = QWidget(self.body_widget)
        self.head_widget.setMinimumSize(QSize(0, 100))
        self.head_widget.setMaximumSize(QSize(16777215, 100))
        # self.head_widget.setStyleSheet("border:1px solid rgb(85, 85, 0);")
        self.head_widget.setObjectName("head_widget")
        self.horizontalLayout_2 = QHBoxLayout(self.head_widget)
        self.horizontalLayout_2.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.head_left_widget = QWidget(self.head_widget)
        self.head_left_widget.setMinimumSize(QSize(90, 0))
        self.head_left_widget.setMaximumSize(QSize(90, 16777215))
        self.head_left_widget.setObjectName("head_left_widget")
        self.horizontalLayout_2.addWidget(self.head_left_widget)
        self.head_middle_widget = QWidget(self.head_widget)
        self.head_middle_widget.setObjectName("head_middle_widget")
        self.horizontalLayout_2.addWidget(self.head_middle_widget)
        self.head_right_widget = QWidget(self.head_widget)
        self.head_right_widget.setMinimumSize(QSize(141, 0))
        self.head_right_widget.setMaximumSize(QSize(90, 16777215))
        self.head_right_widget.setObjectName("head_right_widget")
        self.horizontalLayout_2.addWidget(self.head_right_widget)
        self.verticalLayout_2.addWidget(self.head_widget)
        self.shell_st = QWidget(self.body_widget)
        self.shell_gboy = QGridLayout(self.shell_st)
        self.shell_gboy.setContentsMargins(9,9,9,9)
        self.stackedWidget = SlideShow()
        # self.stackedWidget.setStyleSheet("border:1px solid rgb(255, 170, 0);")
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout_2.addWidget(self.shell_st)
        self.horizontalLayout.addWidget(self.body_widget)
        self.shell_gboy.addWidget(self.stackedWidget)

        self.listWidget.setVerticalScrollBarPolicy(qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(qt.ScrollBarAlwaysOff)
        self.stackedWidget.setButtonsHide(True)

        self.gboy = QGridLayout(self.head_left_widget)
        self.gboy.setContentsMargins(0,0,0,0)
        self.gboy.setSpacing(0)
        self.btn_fold = QPushButton()
        self.btn_fold.setStyleSheet(r'''
        background-color: rgb(234, 234, 234);
        border:none;
        font: 14pt "黑体";
        ''')
        self.btn_fold.setText("三")
        self.btn_fold.setFixedSize(50,50)
        self.gboy.addWidget(self.btn_fold)

    def defaultStyle(self):
        self.qss = QssStyleAnalysis(self.listWidget)
        self.qss.setQSS('''
QListView {
border:none;
outline: 0px;
background-color: #fff;
color: #000;
font: 14pt "黑体";
}
QListView::item{
padding: 5px;
}
QListView::item:hover{
border-right:5px solid #0055ff;
background-color: rgba(170, 255, 255,100);
color: #000;
}
QListView::item:selected{
border-right:5px solid #0055ff;
background-color: rgba(170, 255, 255,200);
color: #000;
}
        ''')
        # print(self.qss.toStr())
        # self.listWidget.setStyleSheet(self.qss.toStr())