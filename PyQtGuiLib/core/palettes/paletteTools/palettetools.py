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

from PyQtGuiLib.core.palettes.paletteTools.area import PureColorWidget,Linear,Radial,Conical


class PaletteTools(PaletteToolsUI):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.pureColorWidget = PureColorWidget()
        self.linearWidget = Linear()
        self.radialWidget = Radial()
        self.conicalWidget = Conical()

        self.addColorWidget(self.pureColorWidget)
        self.addColorWidget(self.linearWidget)
        self.addColorWidget(self.radialWidget)
        self.addColorWidget(self.conicalWidget)

        self.state_action_bar.clicked.connect(self.setCurrentIndex)
        self.gm_action_bar.clicked.connect(self.switchSpread_event)
        self.it_action_bar.switchClicked.connect(self.hide_hand_event)

        self.pureColorWidget.rgbaChange.connect(self.it_action_bar.updateHexView)

    def switchSpread_event(self,spread):
        self.linearWidget.setSpread(spread)
        self.radialWidget.setSpread(spread)
        self.conicalWidget.setSpread(spread)

    def hide_hand_event(self,b):
        self.pureColorWidget.setHideHand(b)
        self.linearWidget.setHideHand(b)
        self.radialWidget.setHideHand(b)
        self.conicalWidget.setHideHand(b)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PaletteTools()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
