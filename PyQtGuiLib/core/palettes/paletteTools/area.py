# -*- coding:utf-8 -*-
# @time:2023/5/299:21
# @author:LX
# @file:area.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
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
    QImage,
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

        self.percentage_pos = {
            "x":0.0,
            "y":0.0
        }

        self.updateLinear()

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
        cursor = self.suppainter.virtualObj("cursor")
        x,y = e.x()-8,e.y()-8
        cursor.move(x,y)
        self.updatePercentagePos(x,y)
        self.heightTo2Discoloration(cursor,y)
        self.sendEMitColor(x,y)
        self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
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
            "pos_percentage": [],
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


class GradientWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.g_type = Handle_Linear
        self.ginfo = None # type:LinearInfo

        self.suppainter = SuperPainter()

        # 当前鼠标左键选择的句柄
        self.cur_click_hand = None  # type:VirtualObject

    def createPix(self):
        if not hasattr(self,"obj_pix"):
            self.obj_pix = QPixmap(self.size())
        else:
            self.obj_pix = self.obj_pix.scaled(self.size())
        self.obj_pix.fill(qt.transparent)

    def drawLayer(self):
        type_dict = {
            Handle_Linear:QLinearGradient,
            Handle_Radial:QRadialGradient,
            Handle_Conical:QConicalGradient,
        }

        self.g_obj = type_dict[self.g_type](*self.ginfo.pos())

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
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton:
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

        for hand in self.ginfo.handles():
            rect = hand["handle"][:4]
            rs = hand["handle"][4],hand["handle"][4]
            self.suppainter.drawRoundedRect(*rect,*rs,openAttr=hand["openAttr"],
                                            brushAttr=hand["brushAttr"],
                                            virtualObjectName=hand["vobj"])

        self.suppainter.end()

    def fckResize(self,hand):
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


class LinearWidget(GradientWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.g_type = Handle_Linear
        self.ginfo = LinearInfo()

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


class RadialWidget(GradientWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.g_type = Handle_Radial
        self.ginfo = RadialInfo()

        self.updateLayer()

    def fckResize(self,vname,pos,pos_dict):
        if vname == "radial_1":
            pass
        elif vname == "radial_2":
            pass
        elif vname == "radial_3":
            pass

    def fckGradient(self,vname,e):
        print(vname)
        if vname == "radial_1":
            self.ginfo.pos()[0] = e.x()
            self.ginfo.pos()[1] = e.y()
        elif vname == "radial_2":
            self.ginfo.pos()[3] = e.x()
            self.ginfo.pos()[4] = e.y()
        elif vname == "radial_3":
            x1,y1 = self.ginfo.pos()[:2]
            sqrt_n = int(math.sqrt(math.pow(e.x() - x1, 2) + math.pow(e.y() - y1, 2)))
            self.ginfo.pos()[2] = sqrt_n


class ConicalWidget(GradientWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.g_type = Handle_Conical
        self.ginfo = ConicalInfo()

        self.updateLayer()

    def fckResize(self,vname,pos,pos_dict):
        print(vname,pos,pos_dict)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RadialWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
