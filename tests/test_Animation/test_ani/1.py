import sys
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import QTimer, QPointF, Qt
from PyQt5.QtWidgets import QApplication, QWidget
import random

class Particle:
    def __init__(self, pos):
        self.pos = pos
        self.speed = QPointF((0.5 - random.random()) * 2, (0.5 - random.random()) * 2)

    def update(self):
        self.pos += self.speed


class ParticleSystem:
    def __init__(self, num_particles):
        self.particles = [Particle(QPointF(random.random() * 400, random.random() * 400)) for _ in range(num_particles)]

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self, painter):
        brush = QBrush(QColor(255, 255, 255))
        for particle in self.particles:
            painter.setBrush(brush)
            painter.drawEllipse(particle.pos, 2, 2)


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 400, 400)

        self.particle_system = ParticleSystem(20000)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(10)

    def update_particles(self):
        self.particle_system.update()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.particle_system.draw(painter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
