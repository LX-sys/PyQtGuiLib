from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QMainWindow,
    QThread,
    Signal,
    QColor
)

from PyQtGuiLib.core.progressBar import CircularBar


class DurationTimeThread(QThread):
    added = Signal(int)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def run(self) -> None:
        n=1
        while True:
            self.added.emit(n)
            n+=1
            self.msleep(80)
            if n == 100+1:
                break

class TestPullOverWidget(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(500,500)

        self.setObjectName("test")
        self.setStyleSheet('''
#test{
background-color: rgb(25, 25, 25);
}
        ''')

        self.th = DurationTimeThread()
        self.th.added.connect(self.test)


        self.cir = CircularBar(self)
        self.cir.resize(150,150)
        self.cir.setVariableLineSegment(CircularBar.Double)
        self.cir.setOuterStyle(CircularBar.CustomDashLine)
        self.cir.setOuterDashPattern([2,3,5,6])
        self.cir.setInnerStyle(CircularBar.DashLine)
        self.cir.setTextSize(15)
        self.cir.move(50,50)
        self.cir.valueChange.connect(lambda v:print("v:",v))

        self.th.start()

    def test(self,n):
        self.cir.setValue(n)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestPullOverWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())