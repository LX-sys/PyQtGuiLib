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
        while True:
            self.sleep(1)
            self.add.emit()

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.th = Time()
        self.th.add.connect(self.test_add)
        self.th.start()


        self.notice = Notices(self)
        self.notice.appendTip("hello wrold",5000)
        # self.notice.appendTip("11111111",5000)
        # self.notice.appendTip("11111111",5000)
        # self.notice.setText("我是通知栏",8000)
        self.notice.setStyleSheet('''
Notice{
qproperty-radius:5;
qproperty-backgroundColor:rgba(153, 241, 255,150);
qproperty-fontSize:18;
}
        ''')
        self.notice.show()

    def test_add(self):
        self.notice.appendTip("ttest{}".format(randint(1,1000)),randint(4000,7000))
        self.notice.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())