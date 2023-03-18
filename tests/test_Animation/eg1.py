# -*- coding:utf-8 -*-
# @time:2023/3/1718:07
# @author:LX
# @file:eg1.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPoint,
    qt,
    QPushButton,
    QSize,
    QPainter,
    QColor,
    QLinearGradient,
    QRect
)

from PyQtGuiLib.animation import Animation

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.swBtn = QPushButton("开关",self)
        self.swBtn.move(150,50)

        self.btn = QPushButton("测试",self)
        self.btn.setStyleSheet('''
QPushButton{
background-color: rgb(75, 153, 0);
color:rgb(0,0,0);
font-size:18px;
border-width:3px;
border-color:rgb(255, 0, 0);
border-style:solid;
border-left-width:2px;
border-left-color:rgb(255, 170, 0);
border-top-color:rgb(255, 170, 0);
border-bottom-color:rgb(255, 170, 0);
font-family:"华文新魏";
}
        ''')
        g = QLinearGradient(QPoint(150,50),QPoint(150,150))
        g.setColorAt(0,qt.red)
        g.setColorAt(0.5,qt.blue)
        g.setColorAt(1,qt.yellow)

        self.btn.move(50,50)
        self.btn.resize(130,60)
        self.ani = Animation(self,Animation.Draw)
        self.ani.setDuration(1000)
        # self.ani.setAniMode(Animation.Sequential)

        self.swBtn.clicked.connect(lambda :self.ani.aniSwitch(self.swBtn))

        # self.ani.addAni({
        #     "targetObj":self.btn,
        #     "propertyName":b"geometry",
        #     "sv":self.btn.rect(),
        #     "ev":QRect(300,150,150,150),
        #     "call":self.test
        # })
        # self.ani.addAni({
        #     "targetObj":self.btn,
        #     "propertyName":b"size",
        #     "sv":self.btn.size(),
        #     "ev":QSize(200,100),
        #     "call":self.test
        # })
        # self.ani.addAni({
        #     "targetObj":self.btn,
        #     "propertyName":b"pos",
        #     "sv":self.btn.pos(),
        #     "ev":QPoint(200,100),
        #     "call":self.test
        # })
        # self.ani.addAni({
        #     "targetObj": self.btn,
        #     "propertyName": b"background-color",
        #     "sv": "this",#
        #     "ev": QColor(75,153,255),#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # })

        # 连续动画测试
        # self.ani.setAniMode(Animation.Sequential)
        # self.ani.addSeriesAni({
        #     "targetObj":self.btn,
        #     "propertyName":b"size",
        #     "sv":self.btn.size(),
        #     "ev":QSize(200,100),
        #     "call":self.test
        # },
        # [QSize(50,50),QSize(30,30),QSize(200,200),QSize(30,30)])
        # self.ani.addAnis({
        #     "targetObj": self.btn,
        #     "propertyName": b"pos",
        #     "sv": self.btn.pos(),#
        #     "ev": QPoint(300,300),#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # },{
        #     "targetObj": self.btn,
        #     "propertyName": b"fontSize",
        #     "sv": 18,#
        #     "ev": 28,#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # },{
        #     "targetObj": self.btn,
        #     "propertyName": b"borderWidth",
        #     "sv": 1,#
        #     "ev": 5,#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # },{
        #     "targetObj": self.btn,
        #     "propertyName": b"borderColor",
        #     "sv": QColor(0,255,0),#
        #     "ev": QColor(0,0,255),#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # },{
        #     "targetObj": self.btn,
        #     "propertyName": b"borderRadius",
        #     "sv": 1,#
        #     "ev": 6,#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # })

        # self.ani.addAnis({
        #     "targetObj":self.btn,
        #     "propertyName":b"border-left-color",
        #     "sv":QColor(255,0,0),
        #     "ev":QColor(0,255,0),
        #     "selector": "QPushButton",
        # },{
        #     "targetObj":self.btn,
        #     "propertyName":b"border-left-width",
        #     "sv":1,
        #     "ev":10,
        #     "selector": "QPushButton",
        # },{
        #     "targetObj":self.btn,
        #     "propertyName":b"border-top-color",
        #     "sv":QColor(255,0,0),
        #     "ev":QColor(0,255,0),
        #     "selector": "QPushButton",
        # },{
        #     "targetObj":self.btn,
        #     "propertyName":b"border-bottom-color",
        #     "sv":QColor(255,0,0),
        #     "ev":QColor(0,255,0),
        #     "selector": "QPushButton",
        # })
        # self.ani.addAni({
        #     "targetObj": self.btn,
        #     "propertyName": b"font-size",
        #     "sv": 18,
        #     "ev": 30,
        #     "call": self.test,
        #     "selector":"QPushButton"
        # })
        # self.ani.addAni({
        #     "targetObj": self.btn,
        #     "propertyName": b"color",
        #     "sv": QColor(0,0,0),
        #     "atv":[QColor(255,0,0),QColor(255,0,0)],
        #     "ev": QColor(0,255,0),
        #     "call": self.test,
        #     "selector":"QPushButton"
        # })
        # self.ani.addAni({
        #     "targetObj": self.btn,
        #     "propertyName": b"font-size",
        #     "sv": "this",#
        #     "ev": 38,#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # })
        # self.ani.addAni({
        #     "targetObj": self,
        #     "propertyName": b"windowOpacity",
        #     "sv": 1,
        #     "ev": 0.5,
        #     "call": self.test,
        #     # "selector":"QPushButton"
        # })
        self.r = self.ani.aniNumber(0)
        self.myrect = QRect(100, 100, 60, 60)
        self.rect_ = self.ani.aniNumbers(400,400,300,100)
        self.rgb = self.ani.aniNumbers(0,255,0)
        # self.ani.addAni({
        #     "propertyName":b"value",
        #     "sv":self.r,
        #     "ev":10,
        #     "call":self.test
        # })
        # self.ani.addSeriesAni({
        #     "propertyName":b"value",
        #     "sv":self.r,
        #     "ev":10,
        #     "call":self.test
        # },[0,8,8])
        # ---
        self.ani.addAni({
            "propertyName": b"value",
            "sv": self.r,
            "ev":10,
            "call": self.test
        })
        self.ani.addValuesAni({
            "propertyName": b"value",
        },self.rect_.numberObjs(),
        [10,300,80,80])
        self.ani.addValuesAni({
            "propertyName": b"value",
        },self.rgb.numberObjs(),
        [255,0,0])
        self.ani.start()

    def test(self,obj):
        print("obj:",obj,123)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setBrush(QColor(*self.rgb.numbers()))
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        # painter.rotate(self.rotate_a.valve())
        # print(self.r.number())
        painter.drawRoundedRect(*self.rect_.numbers(),self.r.number(),self.r.number())
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
