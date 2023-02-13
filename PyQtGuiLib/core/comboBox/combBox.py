# -*- coding:utf-8 -*-
# @time:2023/2/1313:52
# @author:LX
# @file:combBox.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    Qt,
    QGraphicsDropShadowEffect,
    QWidget,
    QLineEdit,
    qt,
    QListWidget,
    Widget,
    Signal,
    QSize,
    QResizeEvent,
    QPropertyAnimation
)


from PyQt5.QtWidgets import QMessageBox

class LineEdit(QLineEdit):
    clicked = Signal(bool)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.press = False

    def mousePressEvent(self, e) -> None:
        self.setEnabled(False)
        if self.press is False:
            self.clicked.emit(True)
            self.press = True
        else:
            self.clicked.emit(False)
            self.press = False
        self.setEnabled(True)
        # super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        super().mouseReleaseEvent(e)


class ComBox(Widget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowFlags(qt.FramelessWindowHint)
        self.setAttribute(qt.WA_TranslucentBackground,True)

        self.shadowX,self.shadowY = 10,10
        self.spacing = 0


        # 输入框高度
        self.line_height = 40

        # 展开区域高度
        self.list_widget_height = 300


        self.Init()
        self.myEvent()

        self.resize(500, 300)

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            super().resize(QSize(args[0].width(),args[1].height()+10))
            self.line_height = args[1].height()
        else:
            super().resize(args[0],args[1]+10)
            # self.line_height = args[1]

        self.line.resize(self.width() - self.shadowX, self.line_height)
        self.line.move(0, 0)

        self.list_widget.move(0, self.line.height() + self.spacing)
        self.list_widget.resize(self.width() - self.shadowX,0)

    def Init(self):
        self.line = LineEdit(self)
        self.list_widget = QListWidget(self)
        self.defaultStyle()
        self.shadow()
        self.updateGeometry()

        self.list_widget.resize(self.width(),0)
        print("dsa")
        self.resize(self.width(), self.line.height())

    def hideListWidget(self):
        def callback():
            self.resize(self.width(), self.line.height())
        self.ani(self.list_widget.size(), QSize(self.width() - self.shadowX, 0),callback)

    def showListWidget(self):
        self.resize(self.width(),self.line.height()+self.list_widget_height+10)
        self.ani(QSize(self.width()- self.shadowX,0),
                 QSize(self.width() - self.shadowX,self.list_widget_height - self.line.height() - self.shadowY))


    def shadow(self):
        self.line_shadow = QGraphicsDropShadowEffect(self)
        self.line_shadow.setBlurRadius(9)
        self.line_shadow.setOffset(5,5)
        self.line_shadow.setColor(qt.gray)
        self.line.setGraphicsEffect(self.line_shadow)

        self.widget_shadow = QGraphicsDropShadowEffect(self)
        self.widget_shadow.setBlurRadius(9)
        self.widget_shadow.setOffset(5, 5)
        self.widget_shadow.setColor(qt.gray)
        self.list_widget.setGraphicsEffect(self.widget_shadow)

    def defaultStyle(self):
        self.setStyleSheet('''
        QLineEdit,QListWidget{
        border:none;
        }
        QLineEdit{
        }
        QListWidget{
        background-color: rgb(221, 221, 110);
        }
        ''')

    def updateGeometry(self):
        self.line.resize(self.width()- self.shadowX, self.line_height)
        self.line.move(0, 0)

        self.list_widget.move(0, self.line.height() + self.spacing)
        self.list_widget.resize(self.width() - self.shadowX, self.list_widget_height - self.line.height() - self.shadowY)

        self.resize(self.width(),
                    self.line.height()+self.spacing+self.list_widget_height)

    def myEvent(self):
        self.line.clicked.connect(self.listExpansion_Event)

    def listExpansion_Event(self,b):
        if b:
            self.showListWidget()
        else:
            self.hideListWidget()

    def ani(self,s:QSize,e:QSize,callback=None):
        ani = QPropertyAnimation(self.list_widget, b"size", self)
        ani.setStartValue(s)
        ani.setEndValue(e)
        ani.setDuration(200)
        if callback:
            ani.finished.connect(callback)
        ani.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ComBox()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())