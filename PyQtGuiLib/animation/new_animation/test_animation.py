# -*- coding:utf-8 -*-
# @time:2023/4/1910:42
# @author:LX
# @file:test_animation.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QSize,
    QPoint,
    QPushButton,
    QObject,
    QSpinBox,
    QEasingCurve,
    QColor
)

import typing
from PyQtGuiLib.animation.new_animation.PropertyAnimation import PropertyAnimation
from PyQtGuiLib.animation.new_animation.animation import Animation



class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)


        self.btn = QPushButton("在5秒内完成倒计时",self)
        self.btn.resize(120,60)
        self.btn.move(30,30)
        self.btn.setStyleSheet('''
QPushButton{
background-color: rgb(85, 170, 127);
font-size:10px;
}
        ''')

        self.spbox = QSpinBox(self)
        self.spbox.resize(150,30)
        self.spbox.setValue(0)
        self.spbox.move(self.width()//2,self.height()//2)

        self.ani = Animation()

        # self.ani.addAni(self.btn.pos(),QPoint(300,300),courseFunc=self.btn.move)
        # self.ani.addAni(1,99,courseFunc=self.spbox.setValue)
        self.ani.addAni(sv=QColor(85,170,127),ev=QColor(78,70,70),targetObj=self.btn,propertyName="background-color",selector="QPushButton")


        self.ani.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())