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
    QColor,
    QPainter,
    qt,
    QPen
)

# 动画框架
from PyQtGuiLib.animation import Animation


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        '''
             Animation 动画框架 案例一,移动一个按钮
        '''

        self.btn = QPushButton("画勾",self)
        self.btn.setStyleSheet('''
        QPushButton{
            background-color:rgb(50,100,200);
            color:rgb(255,0,0);
        }
        ''')
        self.btn.move(50,50)
        self.btn.resize(100,60)

        # 实例化动画类
        self.ani = Animation(self)
        # 设置动画时长
        self.ani.setDuration(1000)

        # self.ani.setAniMode(Animation2.Sequential)

        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"pos", # pos动作 是表示移动
            "sv": self.btn.pos(),
            "ev": QPoint(300,100)
        })
        a = self.ani.getAni(0)


        # self.ani.addAni({
        #     "targetObj": self.btn,
        #     "propertyName": b"background-color", # pos动作 是表示移动
        #     "sv": "this",
        #     "ev": QColor(0,255,0),
        #     "selector":"QPushButton",
        #     "comment": "hello"
        # })

        # self.ani.addSeriesAni({
        #     "targetObj": self.btn,
        #     "propertyName": b"size",
        #     "sv": self.btn.size(),
        #     "ev": QSize(150, 150),
        #     "comment": "hello"
        # },[QSize(50,50),QSize(100,100),QSize(30,30),QSize(80, 80)])
        # print(self.ani.getAni(0))
        # 混合动画模式
        # self.ani.addBlend([
        #     {
        #         "targetObj": self.btn,
        #         "propertyName": b"pos",
        #         "sv": self.btn.pos(),
        #         "ev": QPoint(300, 100),
        #     },
        #     {
        #         "targetObj": self.btn,
        #         "propertyName": b"background-color",
        #         "sv": "this",
        #         "ev": QColor(0, 255, 0),
        #         "selector": "QPushButton",
        #     },
        #     {
        #         "targetObj": self.btn,
        #         "propertyName": b"size",
        #         "sv": "this",
        #         "ev": QSize(100, 100),
        #         # "blendFlag": True
        #     },
        #     {
        #         "targetObj": self.btn,
        #         "propertyName": b"border-radius",
        #         "sv": 0,
        #         "ev": 50,
        #         "selector": "QPushButton",
        #         # "blendFlag": True
        #     },
        # ])

        # self.rect_r = self.ani.createAniNumbers(150,130,100,100,5,5)
        #
        self.rgb = self.ani.createAniColor(255,0,0)
        # #
        # self.ani.addValuesAni({
        #     "propertyName": b"value"
        # },self.rect_r,
        # [400,400,30,30,1,1])
        #
        # self.ani.addValuesAni({
        #     "propertyName": b"value"
        # },self.rgb,QColor(100,45,200))

        # self.ani.setAniMode(Animation2.Sequential)
        self.v1 = self.ani.createAniNumbers(200,200)
        self.v2 = self.ani.createAniNumbers(230,230)
        # self.ani.addValuesAni({
        #     "propertyName": b"value"
        # },self.v1,
        # [230,230])
        # self.ani.addValuesAni({
        #     "propertyName": b"value"
        # },self.v2,
        # [260,150])

        # 开始动画
        # self.btn.clicked.connect(self.ani.start)
        # self.ani.start()

    # def paintEvent(self, e) -> None:
    #     painter = QPainter(self)
    #     op = QPen()
    #     op.setColor(self.rgb.values())
    #     op.setWidth(3)
    #     painter.setPen(op)
    #     # painter.setBrush(self.rgb.values())
    #     # painter.setBrush(QColor(123,45,89))
    #     painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
    #
    #     # painter.translate(self.width() // 2, self.height() // 2)
    #     # painter.scale(0.5, 0.5)
    #     # painter.rotate(*self.aotate_a.values())
    #
    #     # painter.drawRoundedRect(*self.rect_r.values())
    #     # lay = AnimationLayout(e)
    #
    #     painter.drawLine(QPoint(200,200),QPoint(*self.v1.values()))
    #     painter.drawLine(QPoint(230,230),QPoint(*self.v2.values()))
    #     painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())