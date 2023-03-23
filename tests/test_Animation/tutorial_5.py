# -*- coding:utf-8 -*-
# @time:2023/3/2211:19
# @author:LX
# @file:tutorial_5.py
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
             Animation 动画框架 案例五,串行动画
             让一个按钮先移动完成之后,在变大,
             
             注意: 动作的执行顺序,与添加动作的顺序有关
        '''

        self.btn = QPushButton("按钮",self)
        self.btn.move(50,50)
        self.btn.resize(100,60)

        # 实例化动画类
        self.ani = Animation(self)
        # 关键设置(Animation.Sequential 表示串行动画)
        self.ani.setAniMode(Animation.Sequential) # Animation.Parallel 这个是默认设置,也就是并行动画
        # 设置动画时长
        self.ani.setDuration(2000) # 2秒

        # 再添加一个移动的动画
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"pos",
            "sv": self.btn.pos(),
            "ev": QPoint(300, 100)
        })
        # 对按钮添加缩放动画
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"size",
            "sv": self.btn.size(),
            "ev": QSize(150, 100)
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