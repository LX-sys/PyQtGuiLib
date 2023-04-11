# -*- coding:utf-8 -*-
# @time:2023/4/1110:30
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
    QGridLayout,
    qt,
    Qt,
    QMenu,
    QAction,
    QPoint,
    QGraphicsDropShadowEffect,
    QColor
)
from random import randint
import typing

from PyQtGuiLib.templateWindow.UI.listTemplateWindowUI import ListTemplateWindowUI


class ListTemplateWindow(ListTemplateWindowUI):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 伸缩标记,伸缩值
        self.__flexible_flag = True
        self.__flexible_value = (260,60)

        self.listWidget.setIconSize(QSize(50,50))

        self.__ani = QPropertyAnimation(self)
        self.__ani.setTargetObject(self.listWidget)
        self.__ani.setPropertyName(b"size")
        self.__ani.setDuration(600)

        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.__shadow = QGraphicsDropShadowEffect(self)
        self.__shadow.setOffset(0,0)
        self.__shadow.setBlurRadius(30)
        self.__shadow.setColor(QColor("#8ab2e7"))
        self.btn_head_picture.setGraphicsEffect(self.__shadow)

        # 菜单列表
        self.__menus = []
        self.__meun_list = []

        self.__myEvent()
        self.__builtInMenu()

    def __builtInMenu(self):
        self.addMenus([{
            "text":"隐藏/显示菜单(内置功能)",
            "call":self.sidebar_event
            },
            # {
            #     "text":"窗口切换模式"
            #     "call":
            # }
        ])

    def addMenu(self,item:dict):
        self.__menus.append(item)

    def addMenus(self,items:typing.List[dict]):
        for item in items:
            self.addMenu(item)

    def removeMenu(self,text:str):
        del self.__menus[text]

    def __menu_event(self):
        if not self.__menus:
            return

        self.menu = QMenu(self)
        self.menu.setStyleSheet('''
        QMenu {
        border:none;
        font: 12pt "黑体";
        border-radius:5px;
        padding: 0,0,0,15px;
        }
        QMenu::item:selected{
        background-color:#789ac9;
        }
                ''')

        for act in self.__menus:
            text = act["text"]
            call = act.get("call",None)
            obj = act.get("obj",None)
            if obj is None:
                act["obj"] = QAction(text)
                obj = act["obj"]
                if call:
                    obj.triggered.connect(call)
            self.menu.addAction(obj)

        if self.listWidget.isHidden():
            x = self.btn_head_picture.x() + self.x()
        else:
            x = self.btn_head_picture.x() + self.x() + self.listWidget.width()
        y = self.btn_head_picture.y()+self.y()+self.head_middle_widget.height() + 10

        pos = QPoint(x,y)
        self.menu.popup(pos)

    # 设置头像
    def setHeadPicture(self,path:str,size:tuple=(100,100)):
        self.btn_head_picture.setIconSize(QSize(*size))
        self.btn_head_picture.setIcon(QIcon(path))

    def addItem(self,text:typing.Union[str,QListWidgetItem],widget:QWidget,icon:str=None):
        if isinstance(text,QListWidgetItem):
            if icon:
                text.setIcon(QIcon(icon))
            self.listWidget.addItem(text)
            return

        item = QListWidgetItem()
        item.setText(text)
        if icon:
            item.setIcon(QIcon(icon))
        self.listWidget.addItem(item)
        self.stackedWidget.addWidget(widget)

    # 添加头部窗口
    def addHeadWidget(self,widget:QWidget):
        self.head_middle_vbody.addWidget(widget)

    # 隐藏/显示侧边栏
    def sidebar_event(self):
        if self.listWidget.isHidden():
            self.listWidget.show()
            self.btn_fold.show()
        else:
            self.listWidget.hide()
            self.btn_fold.hide()

    # 通过索引隐藏/显示,某个item
    def setHideItem(self,index:int,b:bool=True):
        item = self.listWidget.item(index) # type:QListWidgetItem
        item.setHidden(b)

    def __ani_event(self):
        if self.stackedWidget.count() < 1:
            return

        self.__ani.setStartValue(self.listWidget.size())
        if self.__flexible_flag:
            # self.qss.selector("QListView::item:hover").removeAttr("border-right")
            self.qss.selector("QListView::item:selected").removeAttr("border-right")
            self.__ani.setEndValue(QSize(self.__flexible_value[1],self.listWidget.height()))
            self.__flexible_flag = False
        else:
            # self.qss.selector("QListView::item:hover").updateAttr("border-right","5px solid #0055ff;")
            self.qss.selector("QListView::item:selected").updateAttr("border-right","5px solid #0055ff")
            self.__ani.setEndValue(QSize(self.__flexible_value[0], self.listWidget.height()))
            self.__flexible_flag = True

        self.__ani.valueChanged.connect(lambda v:self.listWidget.setMaximumWidth(v.width()))
        self.__ani.start()

    def __change_st_event(self,item:QListWidgetItem):
        index = self.listWidget.indexFromItem(item).row()
        self.stackedWidget.setCurrentIndex(index)

    def __myEvent(self):
        self.listWidget.itemClicked.connect(self.__change_st_event)
        self.btn_fold.clicked.connect(self.__ani_event)
        self.btn_head_picture.clicked.connect(self.__menu_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ListTemplateWindow()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
