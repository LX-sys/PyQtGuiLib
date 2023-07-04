# -*- coding:utf-8 -*-
# @time:2023/4/1910:42
# @author:LX
# @file:test_animation.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPoint,
    QPushButton,
    QSpinBox
)

from PyQtGuiLib.animation import Animation,ParallelAnimationGroup


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)


        self.btn = QPushButton("在5秒内完成倒计时",self)
        self.btn.resize(120,60)
        self.btn.move(30,30)
        self.btn.setStyleSheet('''
QPushButton{
background-color: rgb(85, 170, 127);
font-size:10px;
}
        ''')

        self.stopbtn = QPushButton("暂停",self)


        self.ani = Animation()
        self.ani.addAni(self.btn.pos(),QPoint(300,300),courseFunc=self.btn.move,duration=5000,loopCount=-1)

        self.ani.start()

        self.stopbtn.clicked.connect(self.test)

    def test(self):
        if self.ani.state() == Animation.START:
            self.ani.paused()
        else:
            self.ani.resume()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())