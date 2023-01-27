from PyQtGuiLib.core.widgets.borderlessWidgetABC import (
    PYQT_VERSIONS,
    QApplication,
    sys,
)
from PyQtGuiLib.core.widgets2 import WidgetABC

'''
    新无边框窗口
'''



class BorderlessWidget(WidgetABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BorderlessWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())