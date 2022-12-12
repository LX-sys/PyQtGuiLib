

from PyQtGuiLib.header import (
    sys,
    QApplication,
    QPropertyAnimation,
    QWidget,
    QPushButton,
    PYQT_VERSIONS,
    QGraphicsOpacityEffect,
    QThread,
    Signal
)


class ZoomAnimation(QPropertyAnimation):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)