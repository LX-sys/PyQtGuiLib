from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QPushButton
)
from PyQtGuiLib.core.widgets import WidgetABC

'''
    新无边框窗口
'''

class BorderlessWidget(WidgetABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)