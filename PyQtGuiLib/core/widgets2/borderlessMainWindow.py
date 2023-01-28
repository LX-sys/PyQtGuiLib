from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QPushButton
)
'''
    新无边框窗口主窗口
'''
from PyQtGuiLib.core.widgets2 import WidgetABC
from PyQtGuiLib.core.widgets2.titleBar import TitleBar
from PyQtGuiLib.core.widgets.statusBar import StatusBar


class BorderlessMainWindow(WidgetABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.test_w = WidgetABC(self)
        self.test_w.resize(60,60)
        self.test_w.move(50,50)
        self.test_w.setRestrictedOperation(True)
        self.test_w.setObjectName("test")
        self.test_w.setStyleSheet('''
        #test{
            qproperty-backgroundColor: rgba(200, 200, 255,255);
            qproperty-radius:3;
        }
        #     ''')
        # self.titlebar = TitleBar(self)
        # self.titlebar.setBtnStyle(TitleBar.WinStyle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BorderlessMainWindow()
    win.setStyleSheet('''
BorderlessMainWindow{
    qproperty-backgroundColor: rgba(165, 138, 255,200);
    qproperty-radius:0;
}
    ''')
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())