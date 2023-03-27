# -*- coding:utf-8 -*-
# @time:2023/3/2713:53
# @author:LX
# @file:1.py
# @software:PyCharm
# -*- coding:utf-8 -*-
# @time:2023/3/2210:55
# @author:LX
# @file:tutorial_1.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QWidget,
    QPushButton,
    QRect,
    QPoint,
    QSize,
    QColor
)

# 动画框架
from PyQtGuiLib.animation import Animation
from PyQtGuiLib.animation.animation import Animation2

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        '''
             Animation 动画框架 案例一,移动一个按钮
        '''

        self.btn = QPushButton("按钮",self)
        self.btn.setStyleSheet('''
        QPushButton{
            background-color:rgb(50,100,200);
            color:rgb(255,0,0);
        }
        ''')
        self.btn.move(50,50)
        self.btn.resize(100,60)

        # 实例化动画类
        self.ani = Animation2(self)
        # 设置动画时长
        self.ani.setDuration(1000) # 2秒
        # 对按钮添加移动动画
        '''
            addAni() 这个方法是一个非常常用的函数,用于添加一个动画
            参数是一个json格式,
            这里使用的参数含义
            targetObj:表示动画的作用对象
            propertyName: 动画的动作
            sv:起始值
            ev:结束值
        '''
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"pos", # pos动作 是表示移动
            "sv": self.btn.pos(),
            "ev": QPoint(300,100),
        })
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"background-color", # pos动作 是表示移动
            "sv": "this",
            "ev": QColor(0,255,0),
            "selector":"QPushButton"
        })
        self.ani.addSeriesAni({
            "targetObj": self.btn,
            "propertyName": b"size",
            "sv": self.btn.size(),
            "ev": QSize(150, 150),
        },[QSize(50,50),QSize(100,100),QSize(30,30),QSize(80, 80)])
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