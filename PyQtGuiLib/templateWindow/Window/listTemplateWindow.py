# -*- coding:utf-8 -*-
# @time:2023/4/1017:42
# @author:LX
# @file:listTemplateWindow.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QListWidgetItem,
    QIcon,
    QSize,
    QPropertyAnimation,
    QGridLayout
)
from random import randint
import typing

from PyQtGuiLib.templateWindow.UI.listTemplateWindowUI import ListTemplateWindowUI

'''
    模板窗口
'''

class ListTemplateWindow(ListTemplateWindowUI):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 伸缩标记,伸缩值
        self.__flexible_flag = True
        self.__flexible_value = (260,60)

        self.listWidget.setIconSize(QSize(50,50))

        w1 = QWidget()
        w2 = QWidget()
        w3 = QWidget()
        for i in [w1,w2,w3]:
            i.setStyleSheet('''
        background-color: rgb({},{},{});
        border-radius:8px;
        '''.format(randint(1,255),randint(1,255),randint(1,255)))
        self.addItem("111",w1,r"D:\myGitProject\PyQtGuiLib\tests\temp_image\python1.png")
        self.addItem("222",w2,r"D:\myGitProject\PyQtGuiLib\tests\temp_image\python1.png")
        self.addItem("333",w3,r"D:\myGitProject\PyQtGuiLib\tests\temp_image\python1.png")

        self.myEvent()

        self.ani = QPropertyAnimation(self)
        self.ani.setTargetObject(self.left_widget)
        self.ani.setPropertyName(b"size")
        self.ani.setDuration(600)

    def addItem(self,text:typing.Union[str,QListWidgetItem],widget:QWidget,icon:str=None):
        if isinstance(text,QListWidgetItem):
            self.listWidget.addItem(text)
            return

        item = QListWidgetItem()
        item.setText(text)
        if icon:
            item.setIcon(QIcon(icon))
        self.listWidget.addItem(item)

        self.stackedWidget.addWidget(widget)

    def change_st_event(self,item:QListWidgetItem):
        index = self.listWidget.indexFromItem(item).row()
        self.stackedWidget.setCurrentIndex(index)

    def ani_value_event(self,v:QSize):
        w = v.width()
        self.left_widget.setMaximumWidth(w)

    def ani_event(self):
        self.ani.setStartValue(self.left_widget.size())
        if self.__flexible_flag:
            self.qss.selector("QListView::item:hover").removeAttr("border-right")
            self.qss.selector("QListView::item:selected").removeAttr("border-right")
            self.ani.setEndValue(QSize(self.__flexible_value[1],self.left_widget.height()))
            self.__flexible_flag = False
        else:
            self.qss.selector("QListView::item:hover").updateAttr("border-right","5px solid #0055ff;")
            self.qss.selector("QListView::item:selected").updateAttr("border-right","5px solid #0055ff")
            self.ani.setEndValue(QSize(self.__flexible_value[0], self.left_widget.height()))
            self.__flexible_flag = True

        self.ani.valueChanged.connect(self.ani_value_event)
        self.ani.start()

    def myEvent(self):
        self.listWidget.itemClicked.connect(self.change_st_event)
        self.btn_fold.clicked.connect(self.ani_event)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ListTemplateWindow()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
