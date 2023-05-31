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
    PureColorOperationUI,
    LinearOperationUI,
    RadialOperationUI,
    ConicalOperationUI,
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
    clickStrColor = Signal(str)
    clickSolidColor = Signal(str)  # 这个信号需要开启才能用

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.isRealTimeSignal = False

        self.pureColorOperation = PureColorOperationUI()
        self.linearOperation = LinearOperationUI()
        self.radialOperation = RadialOperationUI()
        self.conicalOperation = ConicalOperationUI()
        self.addOperationWidget(self.pureColorOperation)
        self.addOperationWidget(self.linearOperation)
        self.addOperationWidget(self.radialOperation)
        self.addOperationWidget(self.conicalOperation)

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
        self.pureColorWidget.rgbaChange.connect(self.pureColorOperation.updateRGB)

        self.it_action_bar.strawColored.connect(self.pureColorOperation.updateRGB)
        self.it_action_bar.strawColored.connect(self.pureColorWidget.colorbar.updateBgColor)  # 吸管颜色同步的纯色界面

        def __updateHexView():
            color = self.pureColorWidget.colorbar.getColor()
            self.it_action_bar.updateHexView(color)
            self.pureColorOperation.updateRGB(color)

        self.pureColorWidget.hsvRgbaChange.connect(__updateHexView)

        #
        self.pureColorOperation.clickColor.connect(lambda :self.sendStrColor(Handle_pure,None))
        self.linearOperation.clickQSS.connect(lambda :self.sendStrColor(Handle_Linear,self.linearWidget))
        self.radialOperation.clickQSS.connect(lambda :self.sendStrColor(Handle_Radial,self.radialWidget))
        self.conicalOperation.clickQSS.connect(lambda :self.sendStrColor(Handle_Conical,self.conicalWidget))

    # 开启实时信号,默认不启用
    def setEnableRealTimeSignal(self,b:bool):
        if self.isRealTimeSignal is False and b:
            # 实时信号
            self.pureColorWidget.rgbaChange.connect(
                lambda color: self.clickSolidColor.emit("rgba({},{},{},{})".format(*color.getRgb())))
            self.pureColorWidget.hsvRgbaChange.connect(
                lambda color: self.clickSolidColor.emit("rgba({},{},{},{})".format(*color.getRgb())))
            #
            for gobj in [self.linearWidget,self.radialWidget,self.conicalWidget]:
                gobj.qssed.connect(lambda qss: self.clickSolidColor.emit(qss))
            self.isRealTimeSignal = True
        elif b is False and self.isRealTimeSignal:
            self.pureColorWidget.rgbaChange.disconnect()
            self.pureColorWidget.hsvRgbaChange.disconnect()
            #
            for gobj in [self.linearWidget, self.radialWidget, self.conicalWidget]:
                gobj.qssed.disconnect()
            self.isRealTimeSignal = False

    def sendStrColor(self,g_type,obj):
        if g_type == Handle_pure:
            color = self.pureColorWidget.colorbar.getColor()
            self.clickStrColor.emit("rgba({},{},{},{})".format(*color.getRgb()))
        elif obj:
            self.clickStrColor.emit(obj.getQSS())

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
