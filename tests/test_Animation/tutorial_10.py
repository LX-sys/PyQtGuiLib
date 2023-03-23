# -*- coding:utf-8 -*-
# @time:2023/3/239:19
# @author:LX
# @file:tutorial_10.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QWidget,
    QPushButton,
    QColor,
    QLabel,
    QSize,
)

# 动画框架
from PyQtGuiLib.animation import Animation


class Test(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(600, 600)
        '''
             Animation 动画框架 案例十, 插值动画
        '''
        self.btn = QPushButton("按钮", self)
        self.btn.move(50, 50)
        self.btn.resize(100, 60)

        # 实例化动画类
        self.ani = Animation(self)
        # 设置动画时长
        self.ani.setDuration(3000)  # 3秒

        # 添加一个动画,
        '''
            atv 表示插值动画属性,
            语法格式:
            时间段取值: 0-1
            [(时间段,动画值)]   # 这种格式可以自己设置,每个动画值在整个动画时长中的占比   
            or
            [动画值]   # 这种格式,所有动画时长会被均匀分配
        '''
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"size",
            "sv":"this",
            "atv":[(0.3,QSize(200,120)),(0.7,QSize(150,30)),(0.9,QSize(200,200))],
            # "atv":[QSize(200,120),QSize(150,30),QSize(200,200)],
            "ev": QSize(100,60),
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