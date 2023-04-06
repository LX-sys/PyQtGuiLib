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



        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"background-color", # pos动作 是表示移动
            "sv": "this",
            "ev": QColor(0,255,0),
            "selector":"QPushButton",
            "call":self.test
        })

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

        self.ani.addValuesAni({
            "propertyName": b"value"
        },self.rgb,QColor(100,45,200))

        # self.ani.setAniMode(Animation2.Sequential)
        self.v1 = self.ani.createAniNumbers(200,200)
        self.v2 = self.ani.createAniNumbers(230,230)
        # 再添加一个移动的动画
        self.textv = [(182, 283), (183, 287), (185, 293), (185, 296), (187, 299), (187, 304), (187, 308), (189, 313), (190, 316), (192, 318), (193, 321), (195, 322), (196, 324), (196, 325), (196, 326), (197, 326), (199, 326), (202, 328), (205, 329), (211, 331), (213, 331), (218, 332), (224, 335), (226, 335), (230, 337), (236, 337), (239, 337), (242, 337), (245, 337), (250, 337), (254,
 336), (260, 334), (266, 332), (272, 328), (276, 325), (280, 322), (283, 319), (287, 318), (290, 317), (295, 313), (299, 309), (304, 307), (308, 304), (313, 300), (318, 297), (321, 295), (324, 293), (329, 289), (334, 286), (340, 282), (342, 280), (348, 276), (350, 275), (355, 274), (358, 270), (361, 268), (363, 267), (365, 264), (367, 262), (370, 259), (374, 256),
 (375, 254), (378, 251), (380, 248), (383, 246), (385, 245), (386, 242), (387, 239), (389, 237), (392, 232), (394, 230), (397, 226), (401, 222), (405, 218), (408, 214), (410, 213), (413, 210), (414, 209), (416, 208), (417, 206), (420, 205), (422, 202), (424, 201), (425, 199), (427, 198), (430, 196), (431, 196), None]


        # 开始动画
        # self.btn.clicked.connect(self.ani.start)
        # self.ani.start()

    def test(self,obj):
        print("dsa",obj)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        op = QPen()
        op.setColor(self.rgb.values())
        op.setWidth(3)
        painter.setPen(op)
        # painter.setBrush(self.rgb.values())
        # painter.setBrush(QColor(123,45,89))
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        s,e = None,None
        for value in self.textv[:-1]:
            if s is None and e is None:
                s=e=value
            else:
                s = value
            painter.drawLine(*s,*e)
            e = value
        # painter.translate(self.width() // 2, self.height() // 2)
        # painter.scale(0.5, 0.5)
        # painter.rotate(*self.aotate_a.values())

        # painter.drawRoundedRect(*self.rect_r.values())
        # lay = AnimationLayout(e)
        #
        # painter.drawLine(QPoint(200,200),QPoint(*self.v1.values()))
        # painter.drawLine(QPoint(230,230),QPoint(*self.v2.values()))
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())