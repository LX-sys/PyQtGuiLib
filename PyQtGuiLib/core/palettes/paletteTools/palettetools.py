# -*- coding:utf-8 -*-
# @time:2023/5/2718:58
# @author:LX
# @file:palettetools.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    Signal,
    QLabel,
    QLineEdit,
    QPainter,
    QLinearGradient,
    QSpacerItem,
    QSizePolicy,
    Qt
)

from PyQtGuiLib.core.palettes.paletteTools.paletteToolUI import (
    PaletteToolsUI,
    Handle_pure,
    Handle_Linear,
    Handle_Radial,
    Handle_Conical,
    G_Mode_Pad,
    G_Mode_Repeat,
    G_Mode_Reflect
)


class PaletteTools(PaletteToolsUI):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PaletteTools()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
