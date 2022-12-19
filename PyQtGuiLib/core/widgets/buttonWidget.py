from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    Qt,
    QMouseEvent,
    Signal
)

from PyQtGuiLib.core.widgets import RoundWidget


'''
    可点击的窗口
'''
class ButtonWidget(RoundWidget):
    clicked = Signal()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ButtonWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())