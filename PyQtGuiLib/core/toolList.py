# -*- coding:utf-8 -*-
# @time:2023/3/139:28
# @author:LX
# @file:toolList.py
# @software:PyCharm
from PyQtGuiLib.header import (
    is_mac_sys,
    QWidget,
    QVBoxLayout,
    QPushButton,
    Signal,
    QObject,
    QSpacerItem,
    QSizePolicy,
    qt
)

from PyQtGuiLib.styles import QssStyleAnalysis


class ToolListItem(QVBoxLayout):
    clicked = Signal(QObject)

    def __init__(self,text:str=None,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)
        self.__item_btn = QPushButton()
        self.__item_btn.setObjectName("itemBtn")
        self.__item_widget = QWidget()
        self.__item_widget.hide()
        self.__item_widget.setObjectName("itemWidget")

        self.__item_btn.clicked.connect(self.btn_event)

        self.addWidget(self.__item_btn)
        self.addWidget(self.__item_widget)

        # qss
        self.__btnQss = QssStyleAnalysis(self.__item_btn)
        self.__widgetQss = QssStyleAnalysis(self.__item_widget)


        if text:
            self.setText(text)

        self.defaultStyle()

    def btn_event(self):
        if self.itemWidget().isHidden():
            self.itemWidget().show()
        else:
            self.itemWidget().hide()
        self.clicked.emit(self)

    def itemBtn(self) -> QPushButton:
        return self.__item_btn

    def itemWidget(self) -> QWidget:
        return self.__item_widget

    def setText(self,text:str):
        self.itemBtn().setText(text)

    def text(self) -> str:
        return self.__item_btn.text()

    def defaultStyle(self):
        self.__btnQss.setQSS('''
            #itemBtn{
                background-color: rgb(12, 11, 15);
                color: rgb(240, 240, 240);
                font: 12pt "华文楷体";
            }
            #itemBtn:hover{
                font: 13pt "华文楷体";
                color: rgb(255, 255, 127);
            }
                ''')

        self.__widgetQss.setQSS('''
        #itemWidget{
        border:1px solid rgb(12, 11, 15);
        }
        ''')

        if is_mac_sys:
            self.__btnQss.selector("#itemBtn").updateAttr("font",'14pt "Heiti SC"')
            self.__btnQss.selector("#itemBtn:hover").updateAttr("font",'16pt "Heiti SC"')

    def clear(self):
        self.itemBtn().disconnect()
        self.removeWidget(self.itemBtn())
        self.removeWidget(self.itemWidget())
        self.itemBtn().deleteLater()
        self.itemWidget().deleteLater()


class ToolListWidget(QWidget):
    clickItem = Signal(QObject)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 样式表生效
        self.setAttribute(qt.WA_StyledBackground, True)

        self.resize(250,350)
        self.setObjectName("ToolListWidget")
        self.__core_vboy = QVBoxLayout(self)
        self.__core_vboy.setSpacing(0)
        self.__core_vboy.setContentsMargins(0,0,0,0)

        self.verSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Record all the ToolListItem
        self.__tool_items = []

        self.myEvent()
        self.defaultStyle()

    def __verSpacer(self):
        self.__core_vboy.removeItem(self.verSpacer)
        self.__core_vboy.addSpacerItem(self.verSpacer)

    def addItem(self,item:ToolListItem):
        item.clicked.connect(self.clickItem.emit)
        self.__core_vboy.addLayout(item)
        self.__tool_items.append(item)
        self.__verSpacer()

    def addItems(self,labels:list):
        for text in labels:
            item = ToolListItem(text)
            item.clicked.connect(self.clickItem.emit)
            self.__core_vboy.addLayout(item)
            self.__tool_items.append(item)
            self.__verSpacer()

    def indexItem(self,index) -> ToolListItem:
        return self.__tool_items[index]

    def removeItem(self,item:ToolListItem):
        if item in self.__tool_items:
            temp_item = self.__tool_items.pop(self.__tool_items.index(item))  # type:ToolListItem
            self.__core_vboy.removeItem(temp_item)
            temp_item.clear()

    def count(self) -> int:
        return len(self.__tool_items)

    def __top_event(self,item:ToolListItem):
        '''
            当所有节点收起时,添加一个弹簧,
            如果有一个节点是展开的,就删除弹簧
        '''
        temp = []
        for item in self.__tool_items:
            temp.append(item.itemWidget().isHidden())

        if temp.count(True) == len(self.__tool_items):
            self.__core_vboy.addSpacerItem(self.verSpacer)
        else:
            self.__core_vboy.removeItem(self.verSpacer)

    def myEvent(self):
        # Implement an event internally
        self.clickItem.connect(self.__top_event)

    def defaultStyle(self):
        self.setStyleSheet('''
        ToolListWidget{
        background-color: gray;
        }
        ''')

    def allItems(self)->[ToolListItem]:
        return self.__tool_items

    def getFoldItems(self)->[ToolListItem]:
        temp = []
        for item in self.allItems():
            if item.itemWidget().isHidden():
                temp.append(item)
        return temp

    def getUnfoldItems(self)->[ToolListItem]:
        temp = []
        for item in self.allItems():
            if not item.itemWidget().isHidden():
                temp.append(item)
        return temp