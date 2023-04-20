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
    QOpenGLWidget
)

import random


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

    def update(self):
        if self._flag and self._cnum < self._num:
            self.pos += self.speed
            self._cnum += 1
            if self._cnum == 100:
                self._flag = False
        elif self._flag is False and self._cnum != 0:
            self.pos -= self.speed
            self._cnum -= 1
            if self._cnum == 0:
                self._flag = True


class ParticleSystem:
    def __init__(self, num_particles):
        self.particles = [ParticleAttr(QPointF(random.random() * 400+100, random.random() * 200+100)) for _ in range(num_particles)]

        self._bru = QBrush(rcolor())
        self.ss = random.randint(1,5)
        self.ee = random.randint(1,5)

    # 更新粒子的位置
    def update(self):
        for particle in self.particles:
            particle.update()

    # 绘制粒子
    def draw(self, painter):
        for particle in self.particles:
            painter.setBrush(self._bru)
            painter.drawEllipse(particle.pos, 3, 3)


class Test(QOpenGLWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.setGeometry(100, 100, 400, 400)

        self.particle_system = ParticleSystem(8000)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(30)

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

        self.gp = Test(self)
        self.gp.resize(600,600)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test2()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())