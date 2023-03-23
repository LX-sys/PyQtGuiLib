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
from PyQtGuiLib.animation.animationLayout import AnimationLayout

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(1200,800)


        self.swBtn = QPushButton("开关",self)
        self.swBtn.move(150,50)

        self.btn = QPushButton("测试",self)
#         self.btn.setStyleSheet('''
# QPushButton{
# background-color: rgb(75, 153, 0);
# color:rgb(0,0,0);
# font-size:18px;
# border-width:3px;
# border-color:rgb(255, 0, 0);
# border-style:solid;
# border-left-width:2px;
# border-left-color:rgb(255, 170, 0);
# border-top-color:rgb(255, 170, 0);
# border-bottom-color:rgb(255, 170, 0);
# font-family:"华文新魏";
# }
#         ''')
        g = QLinearGradient(QPoint(300,20),QPoint(430,80))
        g.setColorAt(0,qt.red)
        g.setColorAt(0.5,qt.blue)
        g.setColorAt(1,qt.yellow)

        self.btn.move(300,20)
        self.btn.resize(130,60)
        self.ani = Animation(self)
        self.ani.setDuration(3000)
        # self.ani.setAniMode(Animation.Sequential)

        self.swBtn.clicked.connect(lambda :self.ani.aniSwitch(self.swBtn))
        # self.rect_r = self.ani.createAniNumbers(self.width()//2,self.height()//2,300,100,0,0)
        # self.rgb = self.ani.createAniColor(0,255,0)
        # self.aotate_a = self.ani.createAniNumbers(0)
        # ---
        # self.ani.addValuesAni({
        #     "propertyName": b"value",
        # },self.rect_r,
        # [10,300,80,80,5,5])
        # self.ani.addValuesAni({
        #     "propertyName": b"value",
        # },self.rgb,
        # QColor(255,0,0)
        # )
        # self.ani.addValuesAni({
        #     "propertyName": b"value",
        # },self.aotate_a,
        # [360])
        self.shadow = self.ani.createAniShadow(0,0,1,QColor(0,0,255))
        self.ani.addValuesAni({
            "targetObj": self.btn,
            "propertyName": b"shadow",
            "isEffect":True
        },self.shadow,
        [0,0,60,QColor(255,0,0)])

        self.ani.start()

    def test(self,obj):
        print("obj:",obj,123)

    # def paintEvent(self, e) -> None:
    #     painter = QPainter(self)
    #     painter.setBrush(self.rgb.values())
    #     painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
    #
    #     painter.translate(self.width() // 2, self.height() // 2)
    #     painter.scale(0.5, 0.5)
    #     painter.rotate(*self.aotate_a.values())
    #
    #     painter.drawRoundedRect(*self.rect_r.values())
    #     # lay = AnimationLayout(e)
    #
    #
    #
    #     painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()
    # win.showMaximized()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
