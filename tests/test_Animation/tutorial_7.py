# -*- coding:utf-8 -*-
# @time:2023/3/2211:27
# @author:LX
# @file:tutorial_7.py
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
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        '''
             Animation 动画框架 案例七,
             从这个案例开始讲解 QSS属性动画
             
             注意:使用这一类动画时,你的控件必须有qss样式
             
             QSS属性动画,暂时不支持渐变
        '''
        self.btn = QPushButton("按钮",self)
        self.btn.move(50,50)
        self.btn.resize(100,60)
        # 写一个简单,标准的样式,按钮添加一个背景颜色
        self.btn.setStyleSheet('''
        QPushButton{
            background-color:rgb(50,100,200);
            color:rgb(255,0,0);
        }
        ''')

        # 实例化动画类
        self.ani = Animation(self)
        # 设置动画时长
        self.ani.setDuration(3000) # 2秒

        # 添加一个QSS属性动画
        self.ani.addAni({
            "targetObj":self.btn,
            "propertyName": b"background-color", # 这里的动作名称与你的样式中必须一致
            "sv": "this",
            "ev": QColor(200,200,100),
            "selector":"QPushButton"  # 对于属性动画来说,这个参数是必须的,参数内容就对应者选择器名称
        })
        # 前景色,也跟着一起变
        self.ani.addAni({
            "targetObj":self.btn,
            "propertyName": b"color",
            "sv": "this",
            "ev": QColor(0,200,0),
            "selector":"QPushButton"
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