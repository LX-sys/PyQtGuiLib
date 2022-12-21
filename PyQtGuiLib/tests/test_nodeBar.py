from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QMainWindow,
    QThread,
    Signal,
    QColor
)

from PyQtGuiLib.core.progressBar import NodeBar


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
        self.resize(800,500)

#         self.setObjectName("test")
#         self.setStyleSheet('''
# #test{
# background-color: rgb(25, 25, 25);
# }
#         ''')

        self.nodebar = NodeBar(self)
        self.nodebar.move(50,100)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestPullOverWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
