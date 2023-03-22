# -*- coding:utf-8 -*-
# @time:2023/3/2211:15
# @author:LX
# @file:tutorial_4.py
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
             Animation 动画框架 案例四,窗口透明
             注意:该动画只能用于主窗口上,对窗口上面的控件是无效的,后面可以用别的办法做到
        '''
        # 实例化动画类
        self.ani = Animation(self)
        # 设置动画时长
        self.ani.setDuration(3000) # 2秒

        # 对窗口透明动画
        self.ani.addAni({
            "targetObj": self,
            "propertyName": b"windowOpacity",
            "sv": 1,
            "ev": 0.5
        })
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