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
    QPoint,
    QPushButton,
    QSpinBox
)

from PyQtGuiLib.animation import Animation,ParallelAnimationGroup


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
        # self.ani.setStartMode(Animation.Parallel)
        # self.ani.addAni(self.btn.pos(),QPoint(300,300),courseFunc=self.btn.move)
        # self.ani.addAni(1,99,courseFunc=self.spbox.setValue)
        # self.ani.addAni(sv="this",ev=QRect(100,100,300,300),targetObj=self.btn,propertyName="geometry")
        # self.ani.addAni(sv="5px", ev=12, targetObj=self.btn, propertyName="font-size", selector="QPushButton")
        # self.ani.addAni(sv=QColor(0,255,0),ev="#ffaa7f",targetObj=self.btn,propertyName="background-color",selector="QPushButton")
        # self.ani.addSeriesAni(sv="5px", ev=12,evs=[20,3,11], targetObj=self.btn, propertyName="font-size", selector="QPushButton")
        self.ani.addSeriesAni(sv="this", ev=QPoint(250,30),evs=[QPoint(250,250),QPoint(30,250),QPoint(30,30)],
                              targetObj=self.btn, propertyName="pos")

        self.ani2 = Animation()
        self.ani2.addSeriesAni(sv="5px", ev=12,evs=[20,3,11], targetObj=self.btn, propertyName="font-size", selector="QPushButton")

        # self.ani.start()
        self.g = ParallelAnimationGroup()
        self.g.builds([self.ani,self.ani2])
        self.g.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())