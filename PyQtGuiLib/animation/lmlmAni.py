# -*- coding:utf-8 -*-
# @time:2022/12/1211:45
# @author:LX
# @file:lmlm.py
# @software:PyCharm

'''
    若隐若现
'''
from PyQtGuiLib.header import (
    sys,
    QApplication,
    QPropertyAnimation,
    QWidget,
    QPushButton,
    PYQT_VERSIONS,
    QGraphicsOpacityEffect,
    QThread,
    Signal
)

# 时间
class DurationTimeThread(QThread):
    finished = Signal()

    def __init__(self,lmlm:QGraphicsOpacityEffect,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.lmlm = lmlm
        self.mode = "show"
        self.dur_time = 3

    def setMode(self,mode:str):
        self.mode = mode

    def setDurationTime(self, seconds: int):
        self.dur_time = seconds

    def run(self):
        n = round((1 / self.dur_time) / 10, 2)
        opacity_v = 0
        if self.mode == "hide":
            opacity_v = 1
            n = -n

        while self.dur_time:
            self.lmlm.setOpacity(opacity_v)
            self.msleep(100)
            opacity_v += n
            if opacity_v >= 1 or opacity_v <= 0:
                break
        self.finished.emit()


# 若隐若现 动画
class LmLmAnimation(QGraphicsOpacityEffect):
    finished = Signal()  # 完成信号

    Show = "show"
    Hide = "hide"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.dtt = DurationTimeThread(self)

    def setMode(self,mode:str="show"):
        self.dtt.setMode(mode)

    # 这样写是为了,统一api的用法
    def setTargetObject(self,widget:QWidget):
        widget.setGraphicsEffect(self)

    def setDuration(self,msecs:int):
        self.dtt.setDurationTime(msecs//1000)

    def start(self):
        self.dtt.start()
        self.dtt.finished.connect(self.finished)



class Test(QWidget):
    def __init__(self):
        super(Test, self).__init__()
        self.resize(800,600)

        self.btn = QPushButton("测试",self)
        self.btn.resize(150,70)
        self.btn.move(100,100)

        self.op =LmLmAnimation()
        self.op.setMode(LmLmAnimation.Hide)
        self.op.setTargetObject(self.btn)
        self.op.setDuration(5000)
        self.op.start()
        self.op.finished.connect(lambda :print("Dasdasd"))


        '''
        geometry 位置和大小
        pos 位置
        size 大小
        windowOpacity 透明度
        alpha  自定义
        '''
        # self.ani = QPropertyAnimation()
        # self.ani.setTargetObject(self.btn)
        # self.ani.setPropertyName(b"windowOpacity")
        # self.ani.setDuration(10000)
        # self.ani.setStartValue(1)
        # self.ani.setEndValue(0.3)
        # self.ani.setStartValue(QRect(150, 30, 100, 100))
        # self.ani.setEndValue(QRect(150, 30, 200, 200))
        # self.ani.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())