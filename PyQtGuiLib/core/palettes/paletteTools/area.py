# -*- coding:utf-8 -*-
# @time:2023/5/299:21
# @author:LX
# @file:area.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    sys,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    Signal,
    QLabel,
    QLineEdit,
    QPainter,
    QSpacerItem,
    QSizePolicy,
    Qt,
    QColor,
    QPixmap,
    qt,
    QGradient,
    QLinearGradient,
    QRadialGradient,
    QConicalGradient,
    QResizeEvent,
    QSize,
    QWindowStateChangeEvent,
    QPoint,
    QMenu,
    QAction,
    QCursor,
    QColorDialog,
    QFrame
)
import math

Handle_pure = "pure"
Handle_Linear = "linear"
Handle_Radial = "radial"
Handle_Conical = "conical"

G_Mode_Pad = "pad"
G_Mode_Repeat = "repeat"
G_Mode_Reflect = "reflect"

from PyQtGuiLib.styles.superPainter.superPainter import SuperPainter, VirtualObject


class ColorHsv(QWidget):
    rgbaChange = Signal(QColor)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(300, 50)

        self.suppainter = SuperPainter()

        self.percentage_pos = 0.0

        self.updateHSV()

    def createPix(self):
        if not hasattr(self,"pix"):
            self.pix = QPixmap(self.size())
        else:
            self.pix = self.pix.scaled(self.size())
        self.pix.fill(qt.transparent)

    def drawHSV(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing)
        gradient = QLinearGradient(self.width(), 0, 0, 0)

        i = 0.0
        gradient.setColorAt(0, QColor.fromHsvF(0, 1, 1, 1))
        while i < 1.0:
            gradient.setColorAt(i, QColor.fromHsvF(i, 1, 1, 1))
            i += 1.0 / 16.0
        gradient.setColorAt(1, QColor.fromHsvF(0, 1, 1, 1))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 0, 0)

    def updateHSV(self):
        self.createPix()
        self.drawHSV()

    # The percentage of the updated location
    def updatePercentagePos(self,cur_x:int):
        self.percentage_pos = round(cur_x / self.width(), 2)

    def sendEMitColor(self,x,y):
        self.updatePercentagePos(x)
        self.rgbaChange.emit(self.pix.toImage().pixelColor(x, y))

    def getColor(self)->QColor:
        cursor = self.suppainter.virtualObj("cursor")
        return self.pix.toImage().pixelColor(*cursor.getPos())

    def mouseMoveEvent(self, e) -> None:
        x = e.pos().x()
        cursor = self.suppainter.virtualObj("cursor")
        y,w = cursor.getVirtualArgs()[1:3]
        if 0 <= x and x <= self.width() - w:
            cursor.move(x, y)
            self.update()
            self.sendEMitColor(x,y)
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e) -> None:
        cursor = self.suppainter.virtualObj("cursor")
        y = cursor.getVirtualArgs()[1]
        x = e.pos().x()
        cursor.move(x, y)
        cursor.updateIndexToArgs(2, 4)
        self.update()
        self.sendEMitColor(x,y)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        cursor = self.suppainter.virtualObj("cursor")
        cursor.updateIndexToArgs(2, 1)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        self.suppainter.drawPixmap(e.rect(), self.pix)
        self.suppainter.drawRect(0, 0, 1, self.height(), openAttr={"color": "white", "width": 1},
                                 virtualObjectName="cursor")
        self.suppainter.end()

    def resizeEvent(self, e:QResizeEvent) -> None:
        if self.suppainter.isVirtualObj("cursor"):
            cursor = self.suppainter.virtualObj("cursor")
            x = int(self.percentage_pos*e.size().width())
            cursor.updateIndexToArgs(0,x)
        self.updateHSV()
        super().resizeEvent(e)

    def changeEvent(self, e:QWindowStateChangeEvent) -> None:
        if e.type() == e.WindowStateChange:
            if self.suppainter.isVirtualObj("cursor") and (self.isMaximized() or self.isMinimized()):
                cursor = self.suppainter.virtualObj("cursor")
                cursor.updateIndexToArgs(0,self.percentage_pos*self.width())
                self.updateHSV()
        super().changeEvent(e)


class ColorBar(QWidget):
    rgbaChange = Signal(QColor)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.suppainter = SuperPainter()

        self.__bgColor = QColor(0, 255, 0, 255)

        self.is_hide_hand = False

        self.percentage_pos = {
            "x":0.0,
            "y":0.0
        }

        self.updateLinear()

    def setHideHand(self,b:bool):
        self.is_hide_hand = b

    def updateBgColor(self,color:QColor):
        self.__bgColor = color
        self.updateLinear()
        self.update()

    def createPix(self):
        if not hasattr(self, "pix"):
            self.pix = QPixmap(self.size())
        else:
            self.pix = self.pix.scaled(self.size())

        if not hasattr(self, "gray_pix"):
            self.gray_pix = QPixmap(self.size())
        else:
            self.gray_pix = self.gray_pix.scaled(self.size())

        self.gray_pix.fill(qt.transparent)
        self.pix.fill(qt.transparent)

    def drawLinear(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#fff"))
        gradient.setColorAt(1, self.__bgColor)

        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 2, 2)

        painter_gray = QPainter(self.gray_pix)
        painter_gray.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor("#000"))
        painter_gray.setPen(qt.NoPen)
        painter_gray.setBrush(gradient)
        painter_gray.drawRoundedRect(self.rect(), 2, 2)

    def updateLinear(self):
        self.createPix()
        self.drawLinear()

    def updatePercentagePos(self,cur_x:int,cur_y:int):
        self.percentage_pos["x"] = round(cur_x / self.width(), 2)
        self.percentage_pos["y"] = round(cur_y / self.height(), 2)

    def sendEMitColor(self,x,y):
        self.updatePercentagePos(x, y)
        self.rgbaChange.emit(self.grab().toImage().pixelColor(x,y))

    def getColor(self) -> QColor:
        cursor = self.suppainter.virtualObj("cursor")
        return self.grab().toImage().pixelColor(*cursor.getPos())

    def heightTo2Discoloration(self,cursor,y):
        if y >= self.height() // 2:
            cursor.updateOpenAttr({"color": "white", "w": 2})
        else:
            cursor.updateOpenAttr({"color": "black", "w": 2})

    def mouseMoveEvent(self, e) -> None:
        if self.is_hide_hand is False:
            cursor = self.suppainter.virtualObj("cursor")
            x,y = e.x()-8,e.y()-8
            cursor.move(x,y)
            self.updatePercentagePos(x,y)
            self.heightTo2Discoloration(cursor,y)
            self.sendEMitColor(x,y)
            self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        if self.is_hide_hand is False:
            cursor = self.suppainter.virtualObj("cursor")
            data = [(2, 16),(3, 16),(4, 8),(5, 8)]
            for i,v in data:
                cursor.updateIndexToArgs(i, v)
            x, y = e.x()-8, e.y()-8
            cursor.move(x, y)
            self.heightTo2Discoloration(cursor, y)
            self.sendEMitColor(x,y)
            self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QResizeEvent):
        if self.is_hide_hand is False:
            cursor = self.suppainter.virtualObj("cursor")
            data = [(2, 10), (3, 10), (4, 5), (5, 5)]
            for i,v in data:
                cursor.updateIndexToArgs(i, v)
            self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing)
        rect = e.rect()
        self.suppainter.drawPixmap(rect, self.pix)
        self.suppainter.drawPixmap(rect, self.gray_pix)
        if self.is_hide_hand is False:
            self.suppainter.drawRoundedRect(20, 20, 10, 10, 5, 5, openAttr={"color": "black", "w": 2},
                                            virtualObjectName="cursor")
        self.suppainter.end()

    def resizeLinearPos(self,w,h):
        if self.suppainter.isVirtualObj("cursor"):
            cursor = self.suppainter.virtualObj("cursor")
            x = int(self.percentage_pos["x"] * w)
            y = int(self.percentage_pos["y"] * h)
            cursor.move(x,y)

    def resizeEvent(self, e) -> None:
        self.resizeLinearPos(e.size().width(),e.size().height())
        self.updateLinear()
        super().resizeEvent(e)

    def changeEvent(self, e:QWindowStateChangeEvent) -> None:
        if e.type() == e.WindowStateChange:
            if self.isMaximized() or self.isMinimized():
                self.resizeLinearPos(self.width(),self.height())
                self.updateLinear()
        super().changeEvent(e)


class PureColorWidget(QWidget):
    rgbaChange = Signal(QColor)
    hsvRgbaChange = Signal(QColor)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,500)

        self.vlay = QVBoxLayout(self)

        self.colorbar = ColorBar()
        self.colorbar.setMinimumHeight(100)

        self.hsv = ColorHsv(self)
        self.hsv.setFixedHeight(50)
        self.hsv.rgbaChange.connect(self.colorbar.updateBgColor)

        self.vlay.addWidget(self.colorbar)
        self.vlay.addWidget(self.hsv)

        self.colorbar.rgbaChange.connect(self.rgbaChange.emit)
        self.hsv.rgbaChange.connect(self.hsvRgbaChange.emit)

    def setHideHand(self,b:bool):
        self.colorbar.setHideHand(b)

    def getColor(self)->QColor:
        return self.colorbar.getColor()

# ----------------------------以上是纯色图形的实现 --------------------------------


class GradientInfo:
    def __init__(self):
        self.info = {
            "pos": [],
            "pos_percentage":[],
            "gColor": {
                # handle_n is the specified naming rule
                "handle_1": {
                    "colorScope": 0,
                    "color": qt.red
                },
                "handle_2": {
                    "colorScope": 1,
                    "color": qt.blue
                }
            },
            # The linear gradient has only two handles
            "handle": [
                {
                    "vobj": "linear_1",
                    "handle": [],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.red},
                    "pos_percentage": {"x":0.0,"y":0.0}
                },
                {
                    "vobj": "linear_2",
                    "handle": [],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.blue},
                    "pos_percentage": {"x":0.0,"y":0.0}
                }
            ]
        }
        self.__max_hand_id = 2

    def getNewName(self)->str:
        self.addID()
        return "handle_{}".format(self.getID())

    def appendColor(self,colorScope,color):
        self.colors()[self.getNewName()]={
            "colorScope":colorScope,
            "color":color
        }

    def updateColorScope(self,hand_id,colorScope):
        self.colors()[hand_id]["colorScope"] = colorScope

    def updateColor(self,hand_id,color):
        self.colors()[hand_id]["color"] = color

    def delColor(self,hand_id):
        del self.colors()[hand_id]

    def addID(self):
        self.__max_hand_id+=1

    def getID(self) -> int:
        return self.__max_hand_id

    def colors(self) -> list:
        return self.info["gColor"]

    def pos(self) -> list:
        return self.info["pos"]

    def handles(self) -> list:
        return self.info["handle"]


class LinearInfo(GradientInfo):
    def __init__(self):
        super().__init__()
        self.info = {
            "pos": [0, 50, 330, 50],
            "pos_percentage": {"x":0.0,"y":0.0,"x1":0.0,"y1":0.0},
            "gColor": {
                # handle_n is the specified naming rule
                "handle_1": {
                    "colorScope": 0,
                    "color": qt.red
                },
                "handle_2": {
                    "colorScope": 1,
                    "color": qt.blue
                }
            },
            # The linear gradient has only two handles
            "handle": [
                {
                    "vobj": "linear_1",
                    "handle": [0, 50, 16, 16, 8, 40],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.red},
                    "pos_percentage":  {"x":0.0,"y":0.0}
                },
                {
                    "vobj": "linear_2",
                    "handle": [335, 50, 16, 16, 8, 40],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.blue},
                    "pos_percentage":  {"x":0.0,"y":0.0}
                }
            ]
        }


class RadialInfo(GradientInfo):
    def __init__(self):
        super().__init__()
        self.info = {
            "pos": [100, 100, 50, 80, 80],
            "pos_percentage": {"x":0.0,"y":0.0,"x1":0.0,"y1":0.0},
            "gColor": {
                # handle_n is the specified naming rule
                "handle_1": {
                    "colorScope": 0,
                    "color": qt.white
                },
                "handle_2": {
                    "colorScope": 1,
                    "color": qt.black
                }
            },
            "handle": [
                {
                    "vobj": "radial_1",
                    "handle": [100, 100, 16, 16, 8, 40],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.red},
                    "pos_percentage":  {"x":0.0,"y":0.0}
                },
                {
                    "vobj": "radial_2",
                    "handle": [80, 80, 14, 14, 7, 40],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.blue},
                    "pos_percentage":  {"x":0.0,"y":0.0}
                },
                {
                    "vobj": "radial_3",
                    "handle": [120, 80, 14, 14, 7, 40],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.gray},
                    "pos_percentage":  {"x":0.0,"y":0.0}
                }

            ]
        }


class ConicalInfo(GradientInfo):
    def __init__(self):
        super().__init__()
        self.info = {
            "pos": [108, 108, 90],
            "pos_percentage": {"x":0.0,"y":0.0},
            "gColor": {
                # handle_n is the specified naming rule
                "handle_1": {
                    "colorScope": 0,
                    "color": qt.red
                },
                "handle_2": {
                    "colorScope": 1,
                    "color": qt.blue
                }
            },
            "handle": [
                {
                    "vobj": "conical_1",
                    "handle": [100, 100, 16, 16, 8, 40],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.red},
                    "pos_percentage":  {"x":0.0,"y":0.0}
                },
                {
                    "vobj": "conical_2",
                    "handle": [80, 80, 14, 14, 7, 40],
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.blue},
                    "pos_percentage":  {"x":0.0,"y":0.0}
                }

            ]
        }
# ----------------------------以上是绘制渐变图形所需的信息--------------------------------


class CodeQSS:
    def __init__(self, code_type="qss"):
        self.code_type = code_type
        self.grab_type = Handle_Linear
        self.grab_mode = "pad"

        self.structure = {
            "head": "qlineargradient({}",
            "pos": "",
            "color": ""
        }

    def setGrab(self, g_type):
        self.grab_type = g_type

    def setGrabMode(self, mode):
        self.grab_mode = mode

    def posArgc(self) -> str:
        return self.structure["pos"]

    def setColorCompound(self, g_color):
        temp = ""
        for hand_id, value in g_color.items():
            colorScope = value["colorScope"]
            color = QColor(value["color"])
            temp += "stop: {} rgba({},{},{},{}),".format(colorScope, *color.getRgb())
        self.structure["color"] = temp[:-1] + ");"

    def colorCompound(self) -> str:
        return self.structure["color"]

    def build(self) -> str:
        if self.grab_type != Handle_Conical:
            if self.grab_mode == QGradient.RepeatSpread:
                mode = "repeat"
            elif self.grab_mode == QGradient.ReflectSpread:
                mode = "reflect"
            else:
                mode = "pad"
            head = self.structure["head"].format("spread:" + mode + ",")
        else:
            head = self.structure["head"].format("")
        pos = self.posArgc() + ","
        return head + pos + self.colorCompound()


class CodeQSSLinear(CodeQSS):
    def __init__(self):
        super().__init__()

    def setPosArgc(self, x1, y1, x2, y2):
        t = "x1:{},y1:{},x2:{},y2:{}"
        self.structure["pos"] = t.format(x1, y1, x2, y2)


class CodeQSSRadial(CodeQSS):
    def __init__(self):
        super().__init__()
        self.structure["head"] = "qradialgradient({}"

    def setPosArgc(self, cx, cy, r, fx, fy):
        t = "cx:{},cy:{},radius:{},fx:{},fy:{}"
        self.structure["pos"] = t.format(cx, cy, r, fx, fy)


class CodeQSSConical(CodeQSS):
    def __init__(self):
        super().__init__()
        self.grab_type = Handle_Conical
        self.structure["head"] = "qconicalgradient({}"

    def setPosArgc(self, cx, cy, angle):
        t = "cx:{},cy:{},angle:{}"
        self.structure["pos"] = t.format(cx, cy, angle)
# ----------------------------以上是生成渐变QSS类--------------------------------


class GradientWidget(QWidget):
    qssed = Signal(str)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.g_type = Handle_Linear
        self.ginfo = None # type:LinearInfo

        self.suppainter = SuperPainter()

        self.spread = QGradient.PadSpread

        self.is_hide_hand = False
        # 当前鼠标左键选择的句柄
        self.cur_click_hand = None  # type:VirtualObject

        self.code_obj = None

    def setCodeObj(self,code):
        self.code_obj = code

    def __updateAll(self):
        self.qssed.emit(self.qss())
        self.updateLayer()
        self.update()

    def updateColorScope(self,hand_id,colorScope):
        self.ginfo.updateColorScope(hand_id,colorScope)
        self.__updateAll()

    def updateColor(self,hand_id,color):
        self.ginfo.updateColor(hand_id,color)
        self.__updateAll()

    def appendColor(self,colorScope,color):
        self.ginfo.appendColor(colorScope,color)
        self.__updateAll()

    def delColor(self,hand_id):
        self.ginfo.delColor(hand_id)
        self.__updateAll()

    def setHideHand(self,b:bool):
        self.is_hide_hand = b

    def createPix(self):
        if not hasattr(self,"obj_pix"):
            self.obj_pix = QPixmap(self.size())
        else:
            self.obj_pix = self.obj_pix.scaled(self.size())
        self.obj_pix.fill(qt.transparent)

    def setSpread(self,spread):
        spread_dict = {
            "pad":QGradient.PadSpread,
            "repeat":QGradient.RepeatSpread,
            "reflect":QGradient.ReflectSpread
        }
        self.spread = spread_dict[spread]
        self.updateLayer()
        self.update()

    def drawLayer(self):
        type_dict = {
            Handle_Linear:QLinearGradient,
            Handle_Radial:QRadialGradient,
            Handle_Conical:QConicalGradient,
        }

        self.g_obj = type_dict[self.g_type](*self.ginfo.pos())
        if self.g_type in [Handle_Linear,Handle_Radial]:
            self.g_obj.setSpread(self.spread)

        for c in self.ginfo.colors().values():
            self.g_obj.setColorAt(c["colorScope"], c["color"])

        painter = QPainter(self.obj_pix)
        painter.setRenderHints(qt.Antialiasing)
        painter.setPen(qt.NoPen)
        painter.setBrush(self.g_obj)
        painter.drawRect(self.rect())

    def updateLayer(self):
        self.createPix()
        self.drawLayer()

    def updatePercentagePos(self,x,y):
        for hand in self.ginfo.handles():
            if hand["vobj"] == self.cur_click_hand.virName():
                hand["pos_percentage"]["x"] = round(x / self.width(), 2)
                hand["pos_percentage"]["y"] = round(y / self.height(), 2)

    def fckGradient(self,vname,e):
        # 具体的渐变实现交给子类
        pass

    def mouseMoveEvent(self, e) -> None:
        if self.cur_click_hand:
            r = self.cur_click_hand.getVirtualArgs()[4]  # radius
            x,y = e.x()-r,e.y()-r
            self.fckGradient(self.cur_click_hand.virName(),e)
            self.cur_click_hand.move(x,y)
            self.updatePercentagePos(x,y)
            self.updateLayer()
            self.update()
        self.qssed.emit(self.qss())
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton and self.is_hide_hand is False:
            for hand in self.ginfo.handles():
                c_hand = self.suppainter.virtualObj(hand["vobj"])
                if c_hand.isClick(e):
                    c_hand.updateOpenAttr({"c": "#fff", "w": 3})
                    self.cur_click_hand = c_hand
                    r = c_hand.getVirtualArgs()[4]  # radius
                    x, y = e.x() - r, e.y() - r
                    self.updatePercentagePos(x,y)
                    break
            self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        if self.is_hide_hand is False:
            for hand in self.ginfo.handles():
                c_hand = self.suppainter.virtualObj(hand["vobj"])
                if c_hand.isClick(e):
                    c_hand.updateOpenAttr({"c": "#000", "w": 2})
            self.cur_click_hand = None
            self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing)

        self.suppainter.drawPixmap(e.rect(),self.obj_pix)

        if self.is_hide_hand is False:
            for hand in self.ginfo.handles():
                rect = hand["handle"][:4]
                rs = hand["handle"][4],hand["handle"][4]
                self.suppainter.drawRoundedRect(*rect,*rs,openAttr=hand["openAttr"],
                                                brushAttr=hand["brushAttr"],
                                                virtualObjectName=hand["vobj"])

        self.suppainter.end()

    def fckResize(self,vname,pos,pos_dict):
        # 渐变随窗口的变化而变化,由子类实现
        pass

    def updateResize(self,w,h):
        for hand in self.ginfo.handles():
            vname = hand["vobj"]
            if self.suppainter.isVirtualObj(vname):
                c_hand = self.suppainter.virtualObj(vname)
                hand["handle"][0] = int(hand["pos_percentage"]["x"]*w)
                hand["handle"][1] = int(hand["pos_percentage"]["y"]*h)
                self.fckResize(vname,self.ginfo.pos(),self.ginfo.info["pos_percentage"])
                c_hand.move(*hand["handle"][:2])

    def resizeEvent(self, e) -> None:
        w, h = e.size().width(), e.size().height()
        self.updateResize(w,h)
        self.updateLayer()
        super().resizeEvent(e)

    def changeEvent(self, e:QWindowStateChangeEvent) -> None:
        if e.type() == e.WindowStateChange:
            if self.isMaximized() or self.isMinimized():
                self.updateResize(self.width(),self.height())
                self.updateLayer()
        super().changeEvent(e)

    def qss(self):
        self.code_obj.setGrab(self.g_type)
        self.code_obj.setGrabMode(self.spread)
        self.code_obj.setColorCompound(self.ginfo.colors())
        return self.code_obj.build()


class LinearWidget(GradientWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.g_type = Handle_Linear
        self.ginfo = LinearInfo()

        self.code = CodeQSSLinear()
        self.setCodeObj(self.code)

        self.updateLayer()

    def fckResize(self,vname,pos,pos_dict):
        if vname == "linear_1":
            pos[0] = int(pos_dict["x"]*self.width())
            pos[1] = int(pos_dict["y"]*self.height())
        elif vname == "linear_2":
            pos[2] = int(pos_dict["x1"]*self.width())
            pos[3] = int(pos_dict["y1"]*self.height())

    def fckGradient(self,vname,e):
        if vname == "linear_1":
            self.ginfo.pos()[0] = e.x()
            self.ginfo.pos()[1] = e.y()
            self.ginfo.info["pos_percentage"]["x"] = round(e.x()/self.width(),2)
            self.ginfo.info["pos_percentage"]["y"] = round(e.y()/self.height(),2)
        elif vname == "linear_2":
            self.ginfo.pos()[2] = e.x()
            self.ginfo.pos()[3] = e.y()
            self.ginfo.info["pos_percentage"]["x1"] = round(e.x() / self.width(), 2)
            self.ginfo.info["pos_percentage"]["y1"] = round(e.y() / self.height(), 2)

        x,y,x1,y1 = self.ginfo.pos()
        if x and y and x1 and y1:
            x,y = round(x/self.width(),3),round(y/self.height(),3)
            x1,y1 = round(x1/self.width(),3),round(y1/self.height(),3)
            self.code.setPosArgc(x,y,x1,y1)


class RadialWidget(GradientWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.g_type = Handle_Radial
        self.ginfo = RadialInfo()

        self.code = CodeQSSRadial()
        self.setCodeObj(self.code)

        self.updateLayer()

    def fckResize(self,vname,pos,pos_dict):
        if vname == "radial_1":
            pos[0] = int(pos_dict["x"] * self.width())
            pos[1] = int(pos_dict["y"] * self.height())
        elif vname == "radial_2":
            pos[3] = int(pos_dict["x1"] * self.width())
            pos[4] = int(pos_dict["y1"] * self.height())
        elif vname == "radial_3":
            pass

    def fckGradient(self,vname,e):
        if vname == "radial_1":
            self.ginfo.pos()[0] = e.x()
            self.ginfo.pos()[1] = e.y()
            self.ginfo.info["pos_percentage"]["x"] = round(e.x()/self.width(),2)
            self.ginfo.info["pos_percentage"]["y"] = round(e.y()/self.height(),2)
        elif vname == "radial_2":
            self.ginfo.pos()[3] = e.x()
            self.ginfo.pos()[4] = e.y()
            self.ginfo.info["pos_percentage"]["x1"] = round(e.x() / self.width(), 2)
            self.ginfo.info["pos_percentage"]["y1"] = round(e.y() / self.height(), 2)
        elif vname == "radial_3":
            x1,y1 = self.ginfo.pos()[:2]
            sqrt_n = int(math.sqrt(math.pow(e.x() - x1, 2) + math.pow(e.y() - y1, 2)))
            self.ginfo.pos()[2] = sqrt_n

        x, y, r, x1, y1 = self.ginfo.pos()
        if x and y and x1 and y1:
            r = round(r/ self.width(), 3)*2
            x,y = round(x/self.width(),3),round(y/self.height(),3)
            x1,y1 = round(x1/self.width(),3),round(y1/self.height(),3)
            self.code.setPosArgc(x,y,r,x1,y1)


class ConicalWidget(GradientWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.g_type = Handle_Conical
        self.ginfo = ConicalInfo()

        self.code = CodeQSSConical()
        self.setCodeObj(self.code)

        self.updateLayer()

    def fckResize(self,vname,pos,pos_dict):
        if vname == "conical_1":
            pos[0] = int(pos_dict["x"]*self.width())
            pos[1] = int(pos_dict["y"]*self.height())
        elif vname == "conical_2":
            pass

    def fckGradient(self,vname,e):
        if vname == "conical_1":
            self.ginfo.pos()[0] = e.x()
            self.ginfo.pos()[1] = e.y()
            self.ginfo.info["pos_percentage"]["x"] = round(e.x() / self.width(), 2)
            self.ginfo.info["pos_percentage"]["y"] = round(e.y() / self.height(), 2)
        elif vname == "conical_2":
            x,y = self.ginfo.pos()[:2]
            angle_arc = math.atan2(e.y() - y, e.x() - x)
            angle = angle_arc * 180 / math.pi
            self.ginfo.pos()[2] = -int(angle)

        x,y,a = self.ginfo.pos()
        if x and y:
            x,y = round(x/self.width(),3),round(y/self.height(),3)
            self.code.setPosArgc(x,y,a)

# ----------------------------以上是绘制渐变图形--------------------------------


HAND_ID_TYPE = str


class ColorOperation(QWidget):
    colorScoped = Signal(HAND_ID_TYPE,float)
    colored = Signal(HAND_ID_TYPE,QColor)
    newColored = Signal(float,QColor)
    delColored = Signal(HAND_ID_TYPE)

    def __init__(self,g_type="linear",*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(60)

        self.suppainter = SuperPainter()

        if g_type == Handle_Radial:
            handle1_color = qt.white
            handle2_color = qt.black
        else:
            handle1_color = qt.red
            handle2_color = qt.blue

        self.handles = [
            {
                "vobj": "handle_1",
                "handle": [5, 5, 20, 20, 10, 40],
                "openAttr": {"c": "#000", "w": 2},
                "brushAttr": {"c": handle1_color},
                "colorScope": 0,
                "color": handle1_color
            },
            {
                "vobj": "handle_2",
                "handle": [335, 5, 20, 20, 10, 40],
                "openAttr": {"c": "#000", "w": 2},
                "brushAttr": {"c": handle2_color},
                "colorScope": 1,
                "color": handle2_color
            }
        ]

        # The id only increases and does not decrease, maintaining uniqueness
        self.max_handle_id = 2

        self.g_type = g_type

        self.cursor_flag = None

        self._right_pressed_pos = QPoint(0,0)

        self.updatePix()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_event)

    def menu_event(self):
        menu_ = QMenu(self)

        new_cursor = QAction("新建游标", self)
        del_cursor = QAction("删除游标", self)
        update_color = QAction("更新颜色", self)
        new_cursor.triggered.connect(self.createCursor_event)
        del_cursor.triggered.connect(self.delCursor_event)
        update_color.triggered.connect(self.updateCursorColor_event)
        menu_.addAction(new_cursor)
        menu_.addAction(del_cursor)
        menu_.addAction(update_color)

        menu_.popup(QCursor.pos())

    def getHandle(self, vname: str):
        for info in self.handles:
            if info["vobj"] == vname:
                return info
        return None

    def createCursor_event(self):
        if not self._right_pressed_pos:
            return

        x = self._right_pressed_pos.x()
        self.max_handle_id += 1

        structure = {
            "vobj": "handle_{}".format(self.max_handle_id),
            "handle": [x, 5, 20, 20, 10, 40],
            "openAttr": {"c": "#000", "w": 2},
        }

        color = QColorDialog.getColor()
        if color.isValid():
            v = round(1 / self.width() * x,2)
            structure["brushAttr"] = {"c": color}
            structure["colorScope"] = v
            structure["color"] = color
            self.handles.append(structure)
            self.newColored.emit(v,color)
            self.updatePix()
            self.update()
        self._right_pressed_pos = None

    def updateCursorColor_event(self):
        if not self._right_pressed_pos:
            return
        for vname in self.vObjs():
            cursor = self.suppainter.virtualObj(vname)
            if cursor.isClick(self._right_pressed_pos):
                color = QColorDialog.getColor()
                if color.isValid():
                    hand = self.getHandle(vname)
                    hand["brushAttr"]["c"] = color
                    hand["color"] = color
                    self.colored.emit(vname,color)
                    break
        self.updatePix()
        self.update()
        self._right_pressed_pos = None

    def delCursor_event(self):
        if not self._right_pressed_pos:
            return

        for vname in self.vObjs():
            cursor = self.suppainter.virtualObj(vname)
            if cursor.isClick(self._right_pressed_pos):
                self.handles.remove(self.getHandle(vname))
                self.delColored.emit(vname)
                break

        self.updatePix()
        self.update()
        self._right_pressed_pos = None

    def vObjs(self) -> list:
        return [vname["vobj"] for vname in self.handles]

    def updatePix(self):
        if not hasattr(self, "pix"):
            self.pix = QPixmap(self.size())
        else:
            self.pix = self.pix.scaled(self.size())
        self.pix.fill(qt.transparent)

        h2 = self.height() // 2
        linear = QLinearGradient(0, h2, self.width(), h2)

        for cursor in self.handles:
            linear.setColorAt(cursor["colorScope"], cursor["color"])

        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)
        painter.setPen(qt.NoPen)
        painter.setBrush(linear)
        painter.drawRoundedRect(self.rect(), 5, 5)

    def updateColorScope(self, cursor_name, v):
        for hand in self.handles:
            if hand["vobj"] == cursor_name:
                hand["colorScope"] = v
                break

    def mouseMoveEvent(self, e) -> None:
        if self.cursor_flag and e.buttons() == Qt.LeftButton:
            cursor = self.suppainter.virtualObj(self.cursor_flag)
            if e.x() + cursor.getWidth() // 2 >= cursor.getWidth() // 2 \
                    and e.x() <= self.width():
                cursor.updateIndexToArgs(0, e.x() - cursor.getWidth() // 2)
                v = round(1 / self.width() * e.x(),2)
                self.updateColorScope(self.cursor_flag, v)
                self.colorScoped.emit(self.cursor_flag, v)
                self.updatePix()
            self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton:
            for vname in self.vObjs():
                cursor = self.suppainter.virtualObj(vname)
                if cursor.isClick(e):
                    color = QColor(cursor.getVirtualBrushAttr()["c"])
                    reverse_color = QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())
                    cursor.updateOpenAttr({"c": reverse_color, "w": 3})
                    cursor.updateIndexToArgs(5, self.height()-10)
                    self.cursor_flag = vname
                    break
                else:
                    self.cursor_flag = ""
            self.update()
        elif e.buttons() == Qt.RightButton:
            self._right_pressed_pos = QPoint(e.pos().x(), e.pos().y())
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        self.cursor_flag = ""
        for vname in self.vObjs():
            cursor = self.suppainter.virtualObj(vname)
            cursor.updateOpenAttr({"c": "#000", "w": 2})
            cursor.updateIndexToArgs(5, 40)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing)

        self.suppainter.drawPixmap(e.rect(),self.pix)

        for hand in self.handles:
            rect = hand["handle"][:4]
            rs = hand["handle"][4]
            line_h =hand["handle"][5]
            self.suppainter.drawCursor(*rect,rs,line_h,
                                        openAttr=hand["openAttr"],
                                        brushAttr=hand["brushAttr"],
                                        virtualObjectName=hand["vobj"]
                                       )

        self.suppainter.end()

    def resizeEvent(self, e: QResizeEvent) -> None:
        width = e.size().width()
        for hand in self.handles:
            if self.suppainter.isVirtualObj(hand["vobj"]):
                cursor = self.suppainter.virtualObj(hand["vobj"])
                new_pos = int(width * hand["colorScope"])
                if new_pos >= width:
                    new_pos -= 20
                cursor.updateIndexToArgs(0, new_pos)
        self.updatePix()
        super().resizeEvent(e)

# ----------------------------渐变图形 通用的操作台--------------------------------


class CombinationFigure(QWidget):
    qssed = Signal(str)

    def __init__(self,g_type,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,500)
        self.vlay = QVBoxLayout(self)

        if g_type == Handle_Linear:
            self.widget = LinearWidget()
        elif g_type == Handle_Radial:
            self.widget = RadialWidget()
        elif g_type == Handle_Conical:
            self.widget = ConicalWidget()
        else:
            raise Exception("no!")

        self.cop = ColorOperation()

        self.vlay.addWidget(self.widget)
        self.vlay.addWidget(self.cop)

        self.widget.qssed.connect(self.qssed.emit)

        self.cop.colorScoped.connect(self.widget.updateColorScope)
        self.cop.colored.connect(self.widget.updateColor)
        self.cop.newColored.connect(self.widget.appendColor)
        self.cop.delColored.connect(self.widget.delColor)

    def setHideHand(self,b:bool):
        self.widget.setHideHand(b)

    def setSpread(self,spread):
        self.widget.setSpread(spread)

    def getQSS(self) -> str:
        return self.widget.qss()


class Linear(CombinationFigure):
    def __init__(self,*args,**kwargs):
        super().__init__(Handle_Linear,*args,**kwargs)


class Radial(CombinationFigure):
    def __init__(self,*args,**kwargs):
        super().__init__(Handle_Radial,*args,**kwargs)


class Conical(CombinationFigure):
    def __init__(self,*args,**kwargs):
        super().__init__(Handle_Conical,*args,**kwargs)
