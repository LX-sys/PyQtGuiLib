# -*- coding:utf-8 -*-
# @time:2023/3/239:14
# @author:LX
# @file:tutorial_9.py
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
             Animation 动画框架 案例九,利用QSS属性动作,
             来 制作透明动画

             注意:使用这一类动画时,你的控件必须有qss样式
        '''
        self.btn = QPushButton("按钮", self)
        self.btn.move(50, 50)
        self.btn.resize(100, 60)
        # 这里我们写一个带透明度的背景样式
        self.btn.setStyleSheet('''
        QPushButton{
            background-color:rgba(234,234,234,255);
        }
        ''')

        # 实例化动画类
        self.ani = Animation(self)
        # 设置动画时长
        self.ani.setDuration(3000)  # 3秒

        # 添加一个QSS属性动画,通过降低rgba 中的 a属性来达到透明效果
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"background-color",
            "sv":"this",
            "ev": QColor(234,234,234,50),
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