# -*- coding:utf-8 -*-
# @time:2023/3/239:06
# @author:LX
# @file:tutorial_8.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QWidget,
    QPushButton,
    QColor,
    QLabel
)

# 动画框架
from PyQtGuiLib.animation import Animation


class Test(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(600, 600)
        '''
             Animation 动画框架 案例八,QSS属性动画特性二,动态QSS属性动画
             背景和前景色动画

             注意:使用这一类动画时,你的控件必须有qss样式
        '''
        self.btn = QPushButton("按钮", self)
        self.btn.move(50, 50)
        self.btn.resize(100, 60)
        # 写一个简单,标准的样式,按钮添加一个背景颜色
        '''
            在上一个案例中,我们知道这个简单标准的QSS动画,
            那么我们去掉QSS中 background-color 这个属性在运行
        '''
        self.btn.setStyleSheet('''
        QPushButton{
            color:rgb(255,0,0);
        }
        ''')

        # 实例化动画类
        self.ani = Animation(self)
        # 设置动画时长
        self.ani.setDuration(3000)  # 3秒

        # 添加一个QSS属性动画
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"background-color",
            # "sv":"this",  # 注意: 在对原本控件中没有样式经行动画时,是不允许使用 "this" 指向自己的
            "sv": QColor(0,255,0),
            "ev": QColor(200, 200, 100),
            "selector": "QPushButton"
        })
        # 开始动画
        self.ani.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())