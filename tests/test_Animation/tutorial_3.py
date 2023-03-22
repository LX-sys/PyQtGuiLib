# -*- coding:utf-8 -*-
# @time:2023/3/2211:09
# @author:LX
# @file:tutorial_3.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QWidget,
    QPushButton,
    QRect,
    QPoint,
    QSize
)

# 动画框架
from PyQtGuiLib.animation import Animation

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        '''
             Animation 动画框架 案例三,移动按钮的同时改变大小
             再这个案例中可以学习 添加多个动作
        '''

        self.btn = QPushButton("按钮",self)
        self.btn.move(50,50)
        self.btn.resize(100,60)

        # 实例化动画类
        self.ani = Animation(self)
        # 设置动画时长
        self.ani.setDuration(2000) # 2秒

        # 对按钮添加缩放动画
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"size",
            "sv": self.btn.size(),
            "ev": QSize(150,100)
        })
        # 再添加一个移动的动画
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"pos",
            "sv": self.btn.pos(),
            "ev": QPoint(300,100)
        })

        # ----------------------------------------------
        # 当然下面这个方法也可以达到和上面两个动作一样的效果,在运行这个动作时,请先注释上面两个动作
        # self.ani.addAni({
        #     "targetObj": self.btn,
        #     "propertyName": b"geometry",
        #     "sv": self.btn.rect(),
        #     "ev": QRect(300,100,150,150)
        # })

        # 开始动画
        self.ani.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())