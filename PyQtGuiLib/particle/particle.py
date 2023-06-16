# -*- coding:utf-8 -*-
# @time:2023/4/2014:53
# @author:LX
# @file:particle.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QColor,
    QSize,
    QPoint,
    QTimer,
    QPointF,
    QPainter,
    QBrush,
    QOpenGLWidget,
    QMouseEvent,
    QPropertyAnimation,
    QObject,
    QEasingCurve
)

import random

from functools import partial

def rcolor()->QColor:
    return QColor(random.randint(0,255),random.randint(0,255),random.randint(0,255))


# 粒子的位置和速度
class ParticleAttr:
    def __init__(self, pos:QPoint):
        self.pos = pos
        self.speed = QPointF((0.5 - random.random()) * 2, (0.5 - random.random()) * 2)

        self._flag = True
        self._num = 100
        self._cnum = 0
        self.update(pos)

    def update(self,pos):
        self.pos = pos
        # self.pos += QPointF(x,y)+self.mpos


class ParticleSystem:
    def __init__(self, num_particles,parent):
        self.particles = [ParticleAttr(QPointF(random.random() * 400+100, random.random() * 200+100)) for _ in range(num_particles)]
        self.parent = parent

        self._bru = QBrush(rcolor())
        self.mpos = QPointF(10,10)

    # 更新粒子的位置
    def update(self):
        es = [QEasingCurve.SineCurve,QEasingCurve.InCurve,QEasingCurve.OutCurve,
              QEasingCurve.CosineCurve,QEasingCurve.Linear]


        for particle in self.particles:
            ani = QPropertyAnimation(QObject(),b"pos",self.parent)
            ani.setEasingCurve(random.choice(es))
            # ani.setEasingCurve(es[-1])
            ani.setStartValue(QPoint(int(particle.pos.x()),int(particle.pos.y())))
            ani.setEndValue(self.mpos-QPoint(random.randint(20,60),
                            random.randint(20,60))
                            )
            ani.valueChanged.connect(partial(self.ani_event,particle))
            ani.start()


    def ani_event(self,particle,pos):
        particle.update(pos)
        self.parent.update()


    def setMouPos(self,pos:QPointF):
        self.mpos = pos

    # 绘制粒子
    def draw(self, painter):
        for particle in self.particles:
            painter.setBrush(self._bru)
            painter.drawEllipse(particle.pos, 3, 3)


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.setGeometry(100, 100, 400, 400)

        self.particle_system = ParticleSystem(100)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(30)

        self.setMouseTracking(True)

        self.mouPos = QPointF(10,10)

    def mouseMoveEvent(self,e:QMouseEvent) -> None:
        self.particle_system.updateMouPos(QPointF(e.pos()))
        super().mouseMoveEvent(e)

    def update_particles(self):
        self.particle_system.update()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.particle_system.draw(painter)


class Test2(QWidget):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)

        self.part = ParticleSystem(200,self)

    def mouseMoveEvent(self, e:QMouseEvent):
        # print(e)
        self.part.setMouPos(e.pos())
        self.part.update()
        super().mouseMoveEvent(e)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.part.draw(painter)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test2()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())