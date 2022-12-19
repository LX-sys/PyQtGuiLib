from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
)
from PyQtGuiLib.core.widgets import ButtonWidget
from PyQtGuiLib.core.pullOver import PullOver

class TestPullOverWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(500,500)

        self.show_btn = ButtonWidget()
        self.show_btn.resize(70, 70)
        self.show_btn.setObjectName("show_btn")
        self.show_btn.setStyleSheet('''
        #show_btn{
        background-color:green;
        border-radius:35px;
        }
        ''')

        # 窗口靠边功能
        self.pullOver = PullOver(self)
        self.pullOver.pullover(self.show_btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestPullOverWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
