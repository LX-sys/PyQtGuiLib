
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QPropertyAnimation,
    QWidget,
    QPushButton,
    QPoint,
    QEasingCurve,
    QGraphicsOpacityEffect,
    QThread,
    Signal,
    QByteArray
)


class MoveAnimation(QPropertyAnimation):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # self.setPropertyName(b"pos")

    # 设置动作组
    def setActionGroup(self,actions:[QPoint]):
        pass
        # n = round(1/len(actions), 2)
        # number = 0
        # self.setStartValue()
        # for pos in actions:
        #     self.setKeyValueAt(number,pos)
        #     number += n



class Test(QWidget):
    def __init__(self):
        super(Test, self).__init__()
        self.resize(800,600)

        self.btn = QPushButton("测试",self)
        self.btn.resize(150,70)
        self.btn.move(100,100)

        self.move_ani = MoveAnimation(self)
        self.move_ani.setPropertyName(QByteArray(b"pos"))
        self.move_ani.setTargetObject(self.btn)
        # self.move_ani.setActionGroup([QPoint(250,100),QPoint(350,150),QPoint(450,250)])
        self.move_ani.setKeyValueAt(0,QPoint(250,100))
        self.move_ani.setKeyValueAt(0.33,QPoint(350,150))
        self.move_ani.setKeyValueAt(0.66,QPoint(450,250))
        self.move_ani.setKeyValueAt(1,QPoint(550,350))

        self.move_ani.setDuration(3000)
        # self.move_ani.setEasingCurve(QEasingCurve.OutBounce)
        self.move_ani.start()
        '''
        geometry 位置和大小
        pos 位置
        size 大小
        windowOpacity 透明度
        alpha  自定义
        '''
        # self.ani = QPropertyAnimation()
        # self.ani.setTargetObject(self.btn)
        # self.ani.setPropertyName(b"windowOpacity")
        # self.ani.setDuration(10000)
        # self.ani.setStartValue(1)
        # self.ani.setEndValue(0.3)
        # self.ani.setStartValue(QRect(150, 30, 100, 100))
        # self.ani.setEndValue(QRect(150, 30, 200, 200))
        # self.ani.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())