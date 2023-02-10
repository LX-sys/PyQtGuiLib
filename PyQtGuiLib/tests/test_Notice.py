from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QResizeEvent,
    QMoveEvent,
    QThread,
    Signal
)
from random import randint
from PyQtGuiLib.core import Notice,Notices

class Time(QThread):
    add = Signal()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def run(self) -> None:
        n = 0
        while True:
            self.sleep(randint(1,1))
            self.add.emit()
            if n == 5:
                break
            n+=1

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.th = Time()
        self.th.add.connect(self.test_add)
        self.th.start()


        self.notice = Notices(self)
        self.notice.setStyleSheet('''
        Notice{
        qproperty-radius:5;
        qproperty-backgroundColor:rgba(153, 241, 255,150);
        qproperty-fontSize:18;
        }
                ''')
        # self.notice.appendTip("hello wrold",5)
        # self.notice.appendTip("11111111",7000)
        # self.notice.appendTip("8888",8000)
        # self.notice.appendTip("我是通知栏",10000)
        # self.notice.show()

    def test_add(self):
        self.notice.appendTip("ttest{}".format(randint(1,1000)),5)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())