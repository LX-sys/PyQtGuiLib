# -*- coding:utf-8 -*-
# @time:2023/5/1111:00
# @author:LX
# @file:palettetools.py
# @software:PyCharm

import math

from PyQtGuiLib.core.switchButtons.swButton import SwitchButton
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    Qt,
    QSizePolicy,
    QSpacerItem,
    QLineEdit,
    QFrame,
    QSlider,
    QFormLayout,
    QPixmap,
    qt,
    QPainter,
    QGradient,
    QLinearGradient,
    QRadialGradient,
    QConicalGradient,
    QColor,
    QRect,
    Signal,
    QStackedWidget,
    QCursor,
    QTimer,
    QPoint,
    QMouseEvent,
    QMenu,
    QAction,
    QColorDialog,
    QResizeEvent,
    QWheelEvent,
    QTabWidget,
    QTextBrowser
)
from PyQtGuiLib.styles.superPainter.superPainter import SuperPainter, VirtualObject

Handle_Linear = "linear"
Handle_Radial = "radial"
Handle_Conical = "conical"


class ColorHsv(QFrame):
    rgbaChange = Signal(QColor)

    def __init__(self):
        super().__init__()
        self.resize(300, 50)

        self.suppainter = SuperPainter()

    # 创建HSV颜色条
    def createHuePixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)  # 抗锯齿
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

    def mouseMoveEvent(self, e) -> None:
        x = e.pos().x()
        cursor = self.suppainter.virtualObj("cursor")  # 获取虚拟对象
        y,w = cursor.getVirtualArgs()[1:3]
        if 0 <= x and x <= self.width() - w:
            cursor.move(x, y)
            self.update()
            color = self.pix.toImage().pixelColor(x, y)
            self.rgbaChange.emit(color)
        super().mouseMoveEvent(e)

    def resizeEvent(self, e) -> None:
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createHuePixmap()
        if self.suppainter.isVirtualObj("cursor"):
            height = e.size().height()
            cursor = self.suppainter.virtualObj("cursor")
            old_rect = list(cursor.getVirtualArgs())
            old_rect[-1] = height
            cursor.updateArgs(*old_rect)
        super().resizeEvent(e)

    def setColor(self, color: QColor):
        # 计算颜色在颜色条中的位置
        h, s, v, a = color.getHsv()
        x = h / 360 * self.width()
        y = self.suppainter.virtualObj("cursor").getVirtualArgs()[1]
        self.suppainter.virtualObj("cursor").move(x, y)
        self.update()

    def mousePressEvent(self, e) -> None:
        cursor = self.suppainter.virtualObj("cursor")  # 获取虚拟对象
        y = cursor.getVirtualArgs()[1]
        cursor.move(e.pos().x(), y)
        cursor.updateIndexToArgs(2, 4)
        self.update()
        color = self.pix.toImage().pixelColor(e.pos().x(), y)
        self.rgbaChange.emit(color)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        cursor = self.suppainter.virtualObj("cursor")
        cursor.updateIndexToArgs(2, 1)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        # 创建出游标,并设置虚拟对象
        self.suppainter.drawPixmap(e.rect(), self.pix)
        self.suppainter.drawRect(0, 0, 1, self.height(), openAttr={"color": "white", "width": 1},
                                 virtualObjectName="cursor")

        self.suppainter.end()


class MaskWidget(QWidget):
    def __init__(self, timer):
        super().__init__()
        self.setWindowFlags(qt.FramelessWindowHint)
        self.setWindowOpacity(0.1)
        self.__timer = timer
        self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, e) -> None:
        self.__timer.stop()
        self.close()
        super().mousePressEvent(e)


# Color plate
class ColorBar(QFrame):
    rgbaChange = Signal(QColor)

    def __init__(self):
        super().__init__()
        self.__bgcolor = QColor(0, 255, 0, 255)

        self.is_half = False

        # 当前位置
        self.__cur_pos = (20, 20)
        self.__cur_pos_percentage = (0.1, 0.1)

        self.suppainter = SuperPainter()

    def setAlpha(self, a: int):
        self.__bgcolor.setAlpha(a)
        self.colorLayer()
        self.rgbaChange.emit(self.__bgcolor)

    def setBgColor(self, color: QColor):
        # Synchronous transparency
        old_a = self.__bgcolor.getRgb()[-1]
        color.setAlpha(old_a)
        self.__bgcolor = color
        self.colorLayer()
        self.rgbaChange.emit(color)

    def bgColor(self) -> QColor:
        return self.__bgcolor

    # 灰色图层
    def grayLayer(self):
        if not hasattr(self, "gray_pix"):
            self.gray_pix = QPixmap(self.size())
        else:
            self.gray_pix = self.gray_pix.scaled(self.size())
        self.gray_pix.fill(qt.transparent)
        self.createGrayPixmap()

    # 彩色图层
    def colorLayer(self):
        if not hasattr(self, "pix"):
            self.pix = QPixmap(self.size())
        else:
            self.pix = self.pix.scaled(self.size())
        self.pix.fill(qt.transparent)
        self.createPixmap()

    def createGrayPixmap(self):
        painter = QPainter(self.gray_pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor("#000"))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 2, 2)

    def createPixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#fff"))
        gradient.setColorAt(1, self.bgColor())

        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 2, 2)

    def __updateCursorPos(self, pos):
        cursor = self.suppainter.virtualObj("cursor")
        x, y = pos.x() - 10, pos.y() - 10
        self.__cur_pos = (x, y)
        self.__cur_pos_percentage = round(x / self.width(), 2), round(y / self.height(), 2)
        cursor.move(x, y)
        pixmap = self.grab()
        color = pixmap.toImage().pixelColor(pos)
        self.rgbaChange.emit(color)
        if y >= self.height() // 2:
            cursor.updateOpenAttr({"color": "white", "w": 2})
        else:
            cursor.updateOpenAttr({"color": "black", "w": 2})
        self.update()

    def mouseMoveEvent(self, e):
        self.__updateCursorPos(e.pos())
        super().mouseMoveEvent(e)

    def curColor(self) -> QColor:
        # return self.pix.toImage().pixelColor(*self.__cur_pos)
        return self.bgColor()

    def mousePressEvent(self, e):
        cursor = self.suppainter.virtualObj("cursor")
        data = [(2, 20),(3, 20),(4, 10),(5, 10)]
        for i,v in data:
            cursor.updateIndexToArgs(i, v)
        self.__updateCursorPos(e.pos())
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

    def resizeEvent(self, e) -> None:
        self.grayLayer()
        self.colorLayer()
        if self.suppainter.isVirtualObj("cursor"):
            w,h = e.size().width(),e.size().height()
            cursor = self.suppainter.virtualObj("cursor")
            cursor.move(self.__cur_pos_percentage[0] * w,
                        self.__cur_pos_percentage[1] * h)

        super().resizeEvent(e)


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
        for i, c in enumerate(g_color):
            color = QColor(g_color[c]["color"])
            temp += "stop: {} rgba({},{},{},{}),".format(i, *color.getRgb())
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


class PLCode:
    def __init__(self, pl="python"):
        self.g_type = Handle_Linear
        self.programming_language = pl
        self.grab_mode = "pad"

        self.structure = {
            "argc": "",
            "color": ""
        }

    def setGrab(self, g_type):
        self.g_type = g_type

    def setGrabMode(self, mode):
        self.grab_mode = mode

    def varName(self) -> str:
        if self.g_type == Handle_Linear:
            return "linear"
        elif self.g_type == Handle_Radial:
            return "radial"
        elif self.g_type == Handle_Conical:
            return "conical"
        else:
            return ""

    def head(self) -> str:
        if self.programming_language == "python":
            if self.g_type == Handle_Linear:
                return "linear = QLinearGradient"
            elif self.g_type == Handle_Radial:
                return "radial = QRadialGradient"
            elif self.g_type == Handle_Conical:
                return "conical = QConicalGradient"
        elif self.programming_language == "cpp":
            if self.g_type == Handle_Linear:
                return "QLinearGradient linear"
            elif self.g_type == Handle_Radial:
                return "QRadialGradient radial"
            elif self.g_type == Handle_Conical:
                return "QConicalGradient conical"
        return ""

    def getMode(self) -> str:
        symbol = ""
        if self.programming_language == "python":
            symbol = "."
        elif self.programming_language == "cpp":
            symbol = "::"

        if self.grab_mode == QGradient.PadSpread:
            return "QGradient{}PadSpread".format(symbol)
        elif self.grab_mode == QGradient.RepeatSpread:
            return "QGradient{}RepeatSpread".format(symbol)
        elif self.grab_mode == QGradient.ReflectSpread:
            return "QGradient{}ReflectSpread".format(symbol)
        return ""

    def setArgc(self, argc: str):
        self.structure["argc"] = argc

    def getArgc(self) -> str:
        return self.structure["argc"]

    def setColorCompound(self, g_color) -> str:
        temp = ""
        for c in g_color:
            c = g_color[c]
            colorScope = c["colorScope"]
            color = "QColor({},{},{},{})".format(*QColor(c["color"]).getRgb())
            temp += "{}.setColorAt({},{})\n".format(self.varName(), colorScope, color)
        self.structure["color"] = temp

    def colorCompound(self) -> str:
        return self.structure["color"]

    def build(self) -> str:
        code = "{}({})\n".format(self.head(), self.getArgc())
        if self.g_type != Handle_Conical:
            code += "{}.setSpread({})\n".format(self.varName(), self.getMode())
        code += self.colorCompound()
        return code


# 展示代码的面板
class VideCode(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.Tool)
        self.resize(520, 380)
        self.setWindowTitle("View Code")

        self.__qss_widget = QTextBrowser()
        self.__py_widget = QTextBrowser()
        self.__cpp_widget = QTextBrowser()

        self.addTab(self.__qss_widget, "QSS")
        self.addTab(self.__py_widget, "Python Qt")
        self.addTab(self.__cpp_widget, "C++ Qt")

    def setQSSCode(self, qss: str):
        self.__qss_widget.clear()
        self.__qss_widget.setText(qss)
        self.update()

    def setPyCode(self, code: str):
        self.__py_widget.clear()
        self.__py_widget.setText(code)
        self.update()

    def setCppCode(self, code: str):
        self.__cpp_widget.clear()
        self.__cpp_widget.setText(code)


# 颜色句柄
class Handle:
    def __init__(self, x, y, w, h, r=10, lh=8):
        '''

        :param x:
        :param y:
        :param w:
        :param h:
        :param r: 圆角半径
        :param lh: 游标线长
        '''
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.lh = lh

    def rect(self) -> QRect:
        return QRect(self.x, self.y, self.w, self.h)

    def getRect(self) -> tuple:
        return self.x, self.y, self.w, self.h

    def radius(self) -> int:
        return self.r

    def lineH(self) -> int:
        return self.lh


# 渐变信息类
class GradientInfo:
    class InfoABC:
        def __init__(self):
            self.info = {
                "pos": [0, 50, 0, 50],
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
                        "handle": Handle(5, 5, 16, 16, 8, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.red},
                        "pos_percentage": (0.0, 0.0)
                    },
                    {
                        "vobj": "linear_2",
                        "handle": Handle(335, 5, 16, 16, 8, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.blue},
                        "pos_percentage": (0.0, 0.0)
                    }
                ]
            }
            self.max_hand_id = 2

        def idAdd(self) -> int:
            self.max_hand_id += 1
            return self.max_hand_id

        def updateHandPos(self, hand_vobj: str, pos_percentage):
            pass

        def getPos(self) -> list:
            return self.info["pos"]

        def colorCount(self) -> int:
            return len(self.info["gColor"])

        def Colors(self) -> dict:
            return self.info["gColor"]

        def updateStart(self, e):
            self.info["pos"][0] = e.x()
            self.info["pos"][1] = e.y()

        def updateSpread(self, e):
            self.info["pos"][2] = e.x()
            self.info["pos"][3] = e.y()

        def updateColor(self, hand_id: str, colorScope=None, color=None):
            if colorScope:
                self.Colors()[hand_id]["colorScope"] = colorScope
            if color:
                self.Colors()[hand_id]["color"] = color

        def handle(self) -> list:
            return self.info["handle"]

        def appendColor(self, colorScope, color):
            name = "handle_{}".format(self.idAdd())
            self.info["gColor"][name] = {
                "colorScope": colorScope,
                "color": color
            }

        def removeHande(self, hand_id):
            del self.Colors()[hand_id]

    class Linear(InfoABC):
        def __init__(self):
            super().__init__()
            self.info = {
                "pos": [0, 50, 330, 50],
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
                        "handle": Handle(0, 50, 16, 16, 8, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.red},
                        "pos_percentage": (0.0, 0.0)
                    },
                    {
                        "vobj": "linear_2",
                        "handle": Handle(335, 50, 16, 16, 8, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.blue},
                        "pos_percentage": (0.9, 0.0)
                    }
                ]
            }

        def updateHandPos(self, hand_vobj: str, pos_percentage):
            if hand_vobj == "linear_1":
                self.handle()[0]["pos_percentage"] = pos_percentage
            if hand_vobj == "linear_2":
                self.handle()[1]["pos_percentage"] = pos_percentage

        def updateSize(self, w, h):
            self.info["pos"][2] = w
            self.info["pos"][3] = h

    class Radial(InfoABC):
        def __init__(self):
            super().__init__()
            self.info = {
                "pos": [100, 100, 50, 80, 80],
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
                        "handle": Handle(100, 100, 16, 16, 8, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.red},
                        "pos_percentage": (0.0, 0.0)
                    },
                    {
                        "vobj": "radial_2",
                        "handle": Handle(80, 80, 14, 14, 7, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.blue},
                        "pos_percentage": (0.0, 0.0)
                    },
                    {
                        "vobj": "radial_3",
                        "handle": Handle(120, 80, 14, 14, 7, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.gray},
                        "pos_percentage": (0.0, 0.0)
                    }

                ]
            }

        def updateHandPos(self, hand_vobj: str, pos_percentage):
            if hand_vobj == "radial_1":
                self.handle()[0]["pos_percentage"] = pos_percentage
            if hand_vobj == "radial_2":
                self.handle()[1]["pos_percentage"] = pos_percentage

        def updateCenterPos(self, e):
            if isinstance(e,QPoint):
                self.info["pos"][0] = e.x()
                self.info["pos"][1] = e.y()
            else:
                self.info["pos"][0] = e.pos().x()
                self.info["pos"][1] = e.pos().y()

        def updateCenterPos2(self, e):
            if isinstance(e,QPoint):
                self.info["pos"][3] = e.x()
                self.info["pos"][4] = e.y()
            else:
                self.info["pos"][3] = e.pos().x()
                self.info["pos"][4] = e.pos().y()

        # 更新外圈大小
        def updateOuterSize(self, n: int):
            self.info["pos"][2] = n

    class Conical(InfoABC):
        def __init__(self):
            super().__init__()
            self.info = {
                "pos": [108, 108, 90],
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
                        "handle": Handle(100, 100, 16, 16, 8, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.red},
                        "pos_percentage": (0.0, 0.0)
                    },
                    {
                        "vobj": "conical_2",
                        "handle": Handle(80, 80, 14, 14, 7, 40),
                        "openAttr": {"c": "#000", "w": 2},
                        "brushAttr": {"c": qt.blue},
                        "pos_percentage": (0.0, 0.0)
                    }

                ]
            }

        def updateHandPos(self, hand_vobj: str, pos_percentage):
            if hand_vobj == "conical_1":
                self.handle()[0]["pos_percentage"] = pos_percentage
            if hand_vobj == "conical_2":
                self.handle()[1]["pos_percentage"] = pos_percentage

        def updateCenter(self, e):
            if isinstance(e,QPoint):
                self.info["pos"][0] = e.x()
                self.info["pos"][1] = e.y()
            else:
                self.info["pos"][0] = e.pos().x()
                self.info["pos"][1] = e.pos().y()

        def updateAngle(self, a: int):
            self.info["pos"][2] = a

    def __init__(self):
        self.__linear = self.Linear()
        self.__radial = self.Radial()
        self.__conical = self.Conical()

    def getLinear(self) -> Linear:
        return self.__linear

    def getRadial(self) -> Radial:
        return self.__radial

    def getConical(self) -> Conical:
        return self.__conical

    def getObj(self, g_type):
        if g_type == Handle_Linear:
            return self.getLinear()
        elif g_type == Handle_Radial:
            return self.getRadial()
        elif g_type == Handle_Conical:
            return self.getConical()
        return None

    def updatePos(self, g_type: str, hand_id: str, color_scope=None):
        self.getObj(g_type).updateColor(hand_id, colorScope=color_scope)

    def updateColor(self, g_type: str, hand_id: str, color=None):
        self.getObj(g_type).updateColor(hand_id, color=color)

    def newColor(self, g_type: str, colorScope, color):
        self.getObj(g_type).appendColor(colorScope, color)

    def delColor(self, g_type: str, hand_id: str):
        self.getObj(g_type).removeHande(hand_id)


# 渐变变板
class GradientWidget(QFrame):
    gradientQSSCoded = Signal(str)

    def __init__(self, grab_type="conical", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.suppainter = SuperPainter()

        self.grab_type = grab_type
        self.grab_mode = QGradient.PadSpread

        self.gradientInfo = GradientInfo()

        self.isHideHand = False

        # -- QSS or Programming language Generate
        self.code_linear = CodeQSSLinear()
        self.code_radial = CodeQSSRadial()
        self.code_conical = CodeQSSConical()
        self.pl_code_py = PLCode("python")
        self.pl_code_cpp = PLCode("cpp")
        # ---

        self.updateAllPix()
        self.createHandle()

    def setViewCode(self, obj):
        self.view_code = obj

    def setGrabType(self, g_type: str):
        self.grab_type = g_type

    def grabType(self) -> str:
        return self.grab_type

    def setGrabMode(self, mode: str):
        if mode == "pad":
            self.grab_mode = QGradient.PadSpread
        if mode == "repeat":
            self.grab_mode = QGradient.RepeatSpread
        if mode == "reflect":
            self.grab_mode = QGradient.ReflectSpread

        self.updateAllPix()

    def createPix(self, g_type):
        if g_type == Handle_Linear:
            if not hasattr(self, "linear_pix"):
                self.linear_pix = QPixmap(self.size())
            else:
                self.linear_pix = self.linear_pix.scaled(self.size())
            obj_pix = self.linear_pix
            info_obj = self.gradientInfo.getLinear()
            obj_g = QLinearGradient(*info_obj.getPos())
        elif g_type == Handle_Radial:
            if not hasattr(self, "radia_pix"):
                self.radia_pix = QPixmap(self.size())
                self.radia_outer_pix = QPixmap(self.size())
            else:
                self.radia_pix = self.radia_pix.scaled(self.size())
                self.radia_outer_pix = self.radia_outer_pix.scaled(self.size())
            self.radia_outer_pix.fill(qt.transparent)
            obj_pix = self.radia_pix
            info_obj = self.gradientInfo.getRadial()
            obj_g = QRadialGradient(*info_obj.getPos())
        elif g_type == Handle_Conical:
            if not hasattr(self, "conical_pix"):
                self.conical_pix = QPixmap(self.size())
            else:
                self.conical_pix = self.conical_pix.scaled(self.size())
            obj_pix = self.conical_pix
            info_obj = self.gradientInfo.getConical()
            obj_g = QConicalGradient(*info_obj.getPos())
        else:
            obj_pix = None
            obj_g = None
            info_obj = None

        if obj_pix and obj_g and info_obj:
            obj_pix.fill(qt.transparent)

            obj_g.setSpread(self.grab_mode)
            for c in info_obj.Colors().values():
                obj_g.setColorAt(c["colorScope"], c["color"])

            painter = QPainter(obj_pix)
            painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

            painter.setPen(qt.NoPen)
            painter.setBrush(obj_g)
            painter.drawRect(self.rect())

    def getPixObj(self, g_type) -> QPixmap:
        if g_type == Handle_Linear:
            return self.linear_pix
        elif g_type == Handle_Radial:
            return self.radia_pix
        elif g_type == Handle_Conical:
            return self.conical_pix
        else:
            return None

    def updateAllPix(self):
        for g_type in [Handle_Linear, Handle_Radial, Handle_Conical]:
            self.createPix(g_type)
        self.update()

    def createHandle(self):
        if self.grab_type in [Handle_Linear, Handle_Radial, Handle_Conical]:
            self.cur_checked_hand = None

    # ---- 同步  渐变 外部事件 - 触发接口 ---
    def syncPos(self, g_type, hand_id, color_scope):
        self.gradientInfo.updatePos(g_type, hand_id, color_scope=color_scope)
        self.createPix(g_type)
        self.update()

    def syncColor(self, g_type, hand_id, color):
        self.gradientInfo.updateColor(g_type, hand_id, color=color)
        self.createPix(g_type)
        self.update()

    def syncNewColor(self, g_type, colorScope, color):
        self.gradientInfo.newColor(g_type, colorScope, color)
        self.createPix(g_type)
        self.update()

    def syncDelColor(self, g_type, hand_id: str):
        self.gradientInfo.delColor(g_type, hand_id)
        self.createPix(g_type)
        self.update()

    # --------同步  渐变 外部事件 - 触发接口 ---

    # --------生成代码
    def buildCodeQSS(self, g_type):
        if g_type == Handle_Linear:
            obj = self.code_linear
            x1, y1, x2, y2 = self.gradientInfo.getLinear().getPos()
            x1, y1 = round(x1 / self.width(), 3), round(y1 / self.height(), 3)
            x2, y2 = round(x2 / self.width(), 3), round(y2 / self.height(), 3)
            argc = x1, y1, x2, y2
        elif g_type == Handle_Radial:
            obj = self.code_radial
            cx, cy, r, fx, fy = self.gradientInfo.getRadial().getPos()
            cx, cy = round(cx / self.width(), 3), round(cy / self.height(), 3)
            fx, fy = round(fx / self.width(), 3), round(fy / self.height(), 3)
            w = self.suppainter.virtualObj("radial_3").getVirtualArgs()[0]
            rr = round(w / self.width(), 2)
            argc = cx, cy, rr, fx, fy
        elif g_type == Handle_Conical:
            obj = self.code_conical
            cx, cy, angle = self.gradientInfo.getConical().getPos()
            cx, cy = round(cx / self.width(), 3), round(cy / self.height(), 3)
            argc = cx, cy, int(math.fabs(angle))
        else:
            obj = None

        if obj:
            obj.setGrabMode(self.grab_mode)
            obj.setPosArgc(*argc)
            obj.setColorCompound(self.gradientInfo.getObj(g_type).Colors())
            g_qss = obj.build()
            self.gradientQSSCoded.emit(g_qss) # send single
            self.view_code.setQSSCode(g_qss)

    def buildCodePL(self, pl, obj, g_type):
        if pl == "python":
            code_obj = self.pl_code_py
        elif pl == "cpp":
            code_obj = self.pl_code_cpp
        else:
            code_obj = None

        if code_obj:
            code_obj.setGrab(g_type)
            code_obj.setGrabMode(self.grab_mode)
            if g_type == Handle_Conical:
                argc = "{},{},{}".format(*obj.getPos())
            elif g_type == Handle_Radial:
                argc = "{},{},{},{},{}".format(*obj.getPos())
            else:
                argc = "{},{},{},{}".format(*obj.getPos())
            code_obj.setArgc(argc)
            code_obj.setColorCompound(obj.Colors())
            if pl == "python":
                self.view_code.setPyCode(code_obj.build())
            elif pl == "cpp":
                self.view_code.setCppCode(self.pl_code_cpp.build())

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.cur_checked_hand and self.isHideHand is False:
            hand = self.cur_checked_hand  # type:VirtualObject
            x, y = e.x()-8, e.y()-8
            hand.move(x, y)

            p_x, p_y = round(x / self.width(), 2), round(y / self.height(), 2)

            if self.rect().contains(e.pos()):
                if self.grab_type == Handle_Linear:
                    info_obj = self.gradientInfo.getLinear()
                    if hand.virName() == "linear_1":
                        info_obj.updateStart(e)
                    elif hand.virName() == "linear_2":
                        info_obj.updateSpread(e)
                elif self.grab_type == Handle_Radial:
                    info_obj = self.gradientInfo.getRadial()
                    if hand.virName() == "radial_1":
                        info_obj.updateCenterPos(e)
                    if hand.virName() == "radial_2":
                        info_obj.updateCenterPos2(e)
                    if hand.virName() == "radial_3":
                        # The distance between any two points on the rectangle
                        x1, y1 = info_obj.getPos()[:2]
                        sqrt_n = int(math.sqrt(math.pow(x - x1, 2) + math.pow(y - y1, 2)))
                        info_obj.updateOuterSize(sqrt_n)
                elif self.grab_type == Handle_Conical:
                    info_obj = self.gradientInfo.getConical()
                    if hand.virName() == "conical_1":
                        info_obj.updateCenter(e)
                    if hand.virName() == "conical_2":
                        # Any point of the rectangle, the formula for radians
                        x1, y1 = info_obj.getPos()[:2]
                        angle_arc = math.atan2(y - y1, x - x1)
                        angle = angle_arc * 180 / math.pi
                        info_obj.updateAngle(int(-angle))
                info_obj.updateHandPos(hand.virName(), (p_x, p_y))
                # qss code and pl code
                self.buildCodeQSS(self.grab_type)
                self.buildCodePL("python", info_obj, self.grab_type)
                self.buildCodePL("cpp", info_obj, self.grab_type)
                # qss ---- up
                self.createPix(self.grab_type)
                self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            hand_obj = self.gradientInfo.getObj(self.grab_type).handle()
            if hand_obj and self.isHideHand is False:
                for hand in hand_obj:
                    c_hand = self.suppainter.virtualObj(hand["vobj"])
                    if c_hand.isClick(e):
                        c_hand.updateOpenAttr({"c": "#fff", "w": 3})
                        self.cur_checked_hand = c_hand
                        break
                self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        hand_obj = self.gradientInfo.getObj(self.grab_type).handle()
        if hand_obj and self.isHideHand is False:
            for hand in hand_obj:
                c_hand = self.suppainter.virtualObj(hand["vobj"])
                c_hand.updateOpenAttr({"c": "#000", "w": 2})
            self.update()
            self.cur_checked_hand = None
        super().mouseReleaseEvent(e)

    def setHideHand(self, b: bool):
        self.isHideHand = b
        self.update()

    def paintEvent(self, e):
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

        pix = self.getPixObj(self.grab_type)
        if pix:
            self.suppainter.drawPixmap(e.rect(), pix)
        handle = self.gradientInfo.getObj(self.grab_type).handle()
        if handle and self.isHideHand is False:
            for hand in handle:
                r = hand["handle"].radius()
                self.suppainter.drawRoundedRect(*hand["handle"].getRect(),
                                                r, r,
                                                openAttr=hand["openAttr"],
                                                brushAttr=hand["brushAttr"],
                                                virtualObjectName=hand["vobj"]
                                                )
        self.suppainter.end()


    def resizeEvent(self, e: QResizeEvent):
        w, h = e.size().width(), e.size().height()
        for hand in self.gradientInfo.getObj(self.grab_type).handle():
            vobj = hand["vobj"]
            if vobj == "radial_3":
                continue
            if self.suppainter.isVirtualObj(vobj):
                p_x, p_y = hand["pos_percentage"]
                cursor = self.suppainter.virtualObj(vobj)
                cursor.move(round(w * p_x, 2), round(h * p_y, 2))

        p_x, p_y = self.gradientInfo.getObj(self.grab_type).handle()[0]["pos_percentage"]
        if self.grab_type == Handle_Linear:
            p_x2, p_y2=self.gradientInfo.getObj(self.grab_type).handle()[1]["pos_percentage"]
            self.gradientInfo.getObj(self.grab_type).updateStart(QPoint(int(w * p_x)+8, int(h * p_y)+8))
            self.gradientInfo.getObj(self.grab_type).updateSpread(QPoint(int(w * p_x2)+8, int(h * p_y2)+8))
        elif self.grab_type == Handle_Radial:
            p_x2, p_y2 = self.gradientInfo.getObj(self.grab_type).handle()[1]["pos_percentage"]
            self.gradientInfo.getObj(self.grab_type).updateCenterPos(QPoint(int(w * p_x) + 8, int(h * p_y) + 8))
            self.gradientInfo.getObj(self.grab_type).updateCenterPos2(QPoint(int(w * p_x2) + 8, int(h * p_y2) + 8))
        elif self.grab_type == Handle_Conical:
            self.gradientInfo.getObj(self.grab_type).updateCenter(QPoint(int(w * p_x)+8, int(h * p_y)+8))
        self.createPix(self.grab_type)
        self.update()
        super().resizeEvent(e)


# -----------------------------


# 渐变通用操作台
class ColorOperation(QFrame):
    syncPosed = Signal(str, str, float)
    syncColor = Signal(str, str, QColor)
    syncNewColor = Signal(str, float, QColor)
    syncDelColor = Signal(str, str)

    def __init__(self, g_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(80)

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
                "handle": Handle(5, 5, 20, 20, 10, 40),
                "openAttr": {"c": "#000", "w": 2},
                "brushAttr": {"c": handle1_color},
                "colorScope": 0,
                "color": handle1_color
            },
            {
                "vobj": "handle_2",
                "handle": Handle(335, 5, 20, 20, 10, 40),
                "openAttr": {"c": "#000", "w": 2},
                "brushAttr": {"c": handle2_color},
                "colorScope": 1,
                "color": handle2_color
            }
        ]

        # The id only increases and does not decrease, maintaining uniqueness
        self.max_handle_id = 2

        self.g_type = g_type

        self.cursor_flag = ""
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

    def createCursor_event(self):
        if not self._right_pressed_pos:
            return

        x = self._right_pressed_pos.x()
        self.max_handle_id += 1
        structure = {
            "vobj": "handle_{}".format(self.max_handle_id),
            "handle": Handle(x, 5, 20, 20, 10, 40),
            "openAttr": {"c": "#000", "w": 2},
        }
        color = QColorDialog.getColor()
        if color.isValid():
            structure["brushAttr"] = {"c": color}
            structure["colorScope"] = 1 / self.width() * x
            structure["color"] = color
            self.handles.append(structure)
            self.syncNewColor.emit(self.g_type, round(1 / self.width() * x, 2), color)
            self.updatePix()
            self.update()
        self._right_pressed_pos = None

    def getHandle(self, vname: str):
        for info in self.handles:
            if info["vobj"] == vname:
                return info
        return None

    def delCursor_event(self):
        if not self._right_pressed_pos:
            return

        for vname in self.vObjs():
            cursor = self.suppainter.virtualObj(vname)
            if cursor.isClick(self._right_pressed_pos):
                self.handles.remove(self.getHandle(vname))
                #
                self.syncDelColor.emit(self.g_type, vname)
                break

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
                    self.syncColor.emit(self.g_type, vname, color)
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

    # 根据游标名称,更新colorScope
    def updateColorScope(self, cursor_name, v):
        for hand in self.handles:
            if hand["vobj"] == cursor_name:
                hand["colorScope"] = v
                break

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.cursor_flag and e.buttons() == Qt.LeftButton:
            cursor = self.suppainter.virtualObj(self.cursor_flag)
            if e.x() + cursor.getWidth() // 2 >= cursor.getWidth() // 2 \
                    and e.x() <= self.width():
                cursor.updateIndexToArgs(0, e.x() - cursor.getWidth() // 2)
                self.updateColorScope(self.cursor_flag, 1 / self.width() * e.x())
                self.updatePix()
                # 发送 游标信息
                self.syncPosed.emit(self.g_type, self.cursor_flag,
                                    round(1 / self.width() * e.x(), 2))
            self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            for vname in self.vObjs():
                cursor = self.suppainter.virtualObj(vname)
                if cursor.isClick(e):
                    r, b, g, a = QColor(cursor.getVirtualBrushAttr()["c"]).getRgb()
                    reverse_color = QColor(255 - r, 255 - b, 255 - g)
                    cursor.updateOpenAttr({"c": reverse_color, "w": 3})
                    cursor.updateIndexToArgs(5, 50)
                    self.cursor_flag = vname
                    break
                else:
                    self.cursor_flag = ""
            self.update()
        elif e.buttons() == Qt.RightButton:
            self._right_pressed_pos = QPoint(e.pos().x(), e.pos().y())
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.cursor_flag = ""
        for vname in self.vObjs():
            cursor = self.suppainter.virtualObj(vname)
            cursor.updateOpenAttr({"c": "#000", "w": 2})
            cursor.updateIndexToArgs(5, 40)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

        self.suppainter.setPen(qt.NoPen)
        rect = QRect(0, self.height() - 50, self.width(), self.height())
        self.suppainter.drawPixmap(rect, self.pix)

        # 绘制句柄
        for cursor in self.handles:
            handle_obj = cursor["handle"]
            self.suppainter.drawCursor(*handle_obj.getRect(),
                                       handle_obj.radius(),
                                       handle_obj.lineH(),
                                       openAttr=cursor["openAttr"],
                                       brushAttr=cursor["brushAttr"],
                                       virtualObjectName=cursor["vobj"]
                                       )
        self.suppainter.end()

    def resizeEvent(self, e: QResizeEvent) -> None:
        width = e.size().width()
        for hand in self.handles:
            if self.suppainter.isVirtualObj(hand["vobj"]):
                cursor = self.suppainter.virtualObj(hand["vobj"])
                new_pos = width * hand["colorScope"]
                if new_pos >= width:
                    new_pos -= 20
                cursor.updateIndexToArgs(0, new_pos)
        self.updatePix()
        super().resizeEvent(e)


# -------------------------------


# 调色工具
class PaletteTools(QWidget):
    clickColor = Signal(QColor)
    qssColored = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("widget")
        self.setWindowTitle("Palette")
        self.resize(600, 400)

        # Pipette timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateColor)

        self.view_code = VideCode()

        self.setUI()
        self.myEvent()

    def setUI(self):
        self.__lay = QVBoxLayout(self)

        self.__top_lay = QHBoxLayout()
        self.__top_lay.setSpacing(20)
        self.pure_color_btn = QPushButton()  # 纯色按钮
        self.line_btn = QPushButton()  # 线性渐变按钮
        self.radial_btn = QPushButton()  # 径向渐变按钮
        self.conical_btn = QPushButton()  # 角度渐变按钮
        self.pure_color_btn.setObjectName("pure_color_btn")
        self.line_btn.setObjectName("line_btn")
        self.radial_btn.setObjectName("repeat_btn")
        self.conical_btn.setObjectName("reflect_btn")
        self.pure_color_btn.setToolTip("纯色")
        self.line_btn.setToolTip("线性渐变")
        self.radial_btn.setToolTip("径向渐变")
        self.conical_btn.setToolTip("角度渐变")

        #
        self.pad_btn = QPushButton()
        self.rep_btn = QPushButton()
        self.ref_btn = QPushButton()
        self.pad_btn.setObjectName("Pad")
        self.rep_btn.setObjectName("Rep")
        self.ref_btn.setObjectName("Ref")

        self.__spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.demonstration_color_l = QLabel()

        self.demonstration_color_l.setFixedSize(24, 24)
        self.color_straw_btn = QPushButton()  # 吸管
        self.color_straw_btn.setObjectName("color_straw_btn")
        self.color_straw_btn.setText("吸")
        self.color_straw_btn.setFixedSize(24, 24)
        self.hand_btn = SwitchButton()
        self.hand_btn.setShape(SwitchButton.Shape_Square)
        self.hand_btn.setFixedSize(50, 24)
        self.hex_line = QLineEdit()
        self.hex_line.setFixedSize(100, 24)
        self.hex_line.setText("#00ff00")

        for btn in [self.pure_color_btn, self.line_btn, self.radial_btn, self.conical_btn]:
            btn.setFixedSize(24, 24)
            self.__top_lay.addWidget(btn, )

        for btn in [self.pad_btn, self.rep_btn, self.ref_btn]:
            btn.setFixedSize(48, 24)
            self.__top_lay.addWidget(btn, )

        self.__top_lay.addItem(self.__spacer)
        self.__top_lay.addWidget(self.demonstration_color_l)
        self.__top_lay.addWidget(self.color_straw_btn)
        self.__top_lay.addWidget(self.hand_btn)
        self.__top_lay.addWidget(self.hex_line)

        # 中间层
        self.__middle_lay = QHBoxLayout()
        self.__middle_lay.setContentsMargins(0, 0, 0, 0)
        self.__middle_lay.setSpacing(3)

        # ---

        # 纯色,线性渐变,径向渐变,角度渐变
        self.st = QStackedWidget()
        self.st_pure_color_wideget = QWidget()
        self.st_linear_widget = QWidget()
        self.st_radial_widget = QWidget()
        self.st_conicalt_widget = QWidget()
        self.st.addWidget(self.st_pure_color_wideget)
        self.st.addWidget(self.st_linear_widget)
        self.st.addWidget(self.st_radial_widget)
        self.st.addWidget(self.st_conicalt_widget)

        self.pureColorWidget()
        for g_type in [Handle_Linear,Handle_Radial,Handle_Conical]:
            self.grabColorWidget(g_type)
        # -----

        # 不同颜色的操作太区域
        self.operation_st = QStackedWidget()
        self.operation_st.setFixedWidth(100)

        # 操作台
        self.pureColorOperation()
        self.linearColorOperation()
        self.radialColorOperation()
        self.conicalColorOperation()

        self.__lay.addLayout(self.__top_lay)
        self.__lay.addLayout(self.__middle_lay)

        # 初始化演示色块
        self.setDemonstrationColor(self.color_bar.bgColor())
        self.setStyleSheet('''
#widget{
background-color:#0b4a2d;
}
#color_straw_btn{
font: 10pt "等线";
background-color: rgb(20, 134, 79);
color: rgb(232, 232, 232);
border:1px solid rgb(85, 170, 127);
border-radius:2px;
}
#color_straw_btn:pressed{
background-color:rgb(14, 95, 56)
}
#pure_color_btn,#line_btn,#repeat_btn,#reflect_btn{
border-radius:12px;
border:2px solid rgba(0,0,0,255);
}
#pure_color_btn:hover,#line_btn:hover,#repeat_btn:hover,#reflect_btn:hover{
border:3px solid rgba(0,0,0,255);
}
#pure_color_btn:pressed,#line_btn:pressed,#repeat_btn:pressed,#reflect_btn:pressed{
border:2px solid rgba(0,0,0,255);
}
#pure_color_btn{
background-color: rgb(255, 170, 0);
}
#line_btn{
background-color:qlineargradient(spread:pad,x1:0.002,y1:0.457,x2:0.957,y2:0.463,stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
#repeat_btn{
background-color:qradialgradient(spread:pad,cx:0.436,cy:0.483,radius:0.462,fx:0.47,fy:0.533,stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
#reflect_btn{
background-color:qconicalgradient(cx:0.448, cy:0.42, angle:120 stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
QLabel{
color: rgb(108, 210, 171);
font: 11pt "等线";
}
#colorButton,#linear_view{
border-radius:5px;
background-color: rgb(88, 142, 128);
color: rgb(255, 255, 255);
font: 11pt "等线";
}
QLineEdit{
border:none;
background-color: rgba(23, 154, 93,100);
color: rgb(209, 209, 209);
}

#Pad:hover,#Rep:hover,#Ref:hover{
border:2px solid white;
}
#Pad,#Rep,#Ref,#Pad:pressed,#Rep:pressed,#Ref:pressed{
border:2px solid back;
border-radius:3px;
}
#Pad{
background-color: qlineargradient(spread:pad, x1:0.001, y1:0.471, x2:1, y2:0.482955, stop:0 rgba(232, 200, 97, 255), stop:1 rgba(174, 174, 174, 255));
}
#Rep{
background-color:qlineargradient(spread:repeat, x1:0.33, y1:0.482364, x2:0.63, y2:0.477273, stop:0 rgba(232, 200, 97, 255), stop:1 rgba(174, 174, 174, 255));
}
#Ref{
background-color:qlineargradient(spread:reflect, x1:0.554, y1:0.475, x2:0.63, y2:0.477273, stop:0 rgba(232, 200, 97, 255), stop:1 rgba(174, 174, 174, 255));
}

        ''')

    def updateColor(self):
        if hasattr(self, "maskWidget"):
            self.maskWidget.move(QCursor.pos() - QPoint(50, 50))
        # straw
        pos = QCursor.pos()
        screen = QApplication.primaryScreen()
        if screen is not None:
            pixmap = screen.grabWindow(0, pos.x(), pos.y(), 1, 1)
            color = pixmap.toImage().pixelColor(0, 0)
            self.setDemonstrationColor(color)
            self.setLabelRGB(color)
            self.hex_line.setText(color.name())

    # 纯色面板
    def pureColorWidget(self):
        self.__m_v_lay = QVBoxLayout(self.st_pure_color_wideget)
        self.color_bar = ColorBar()
        self.hsv_widget = QWidget()
        self.hsv_widget.setFixedHeight(50)
        self.__hsv_lay = QVBoxLayout(self.hsv_widget)
        self.hsv = ColorHsv()
        self.hsv.setFixedHeight(15)
        self.splider = QSlider()
        self.splider.setMinimum(0)
        self.splider.setMaximum(255)
        self.splider.setValue(255)
        self.splider.setOrientation(Qt.Horizontal)
        self.__hsv_lay.addWidget(self.hsv)
        self.__hsv_lay.addWidget(self.splider)

        self.__m_v_lay.addWidget(self.color_bar)
        self.__m_v_lay.addWidget(self.hsv_widget)

        self.__middle_lay.addWidget(self.st)

    # 纯色操作台
    def pureColorOperation(self):
        self._m_r_widget = QWidget()
        self._m_r_lay = QVBoxLayout(self._m_r_widget)
        self._m_r_widget.setFixedWidth(100)

        self.operation_st.addWidget(self._m_r_widget)

        self.label_r, self.label_g, self.label_b, self.label_a = [
            QLabel("红(R)"),
            QLabel("绿(G)"),
            QLabel("蓝(B)"),
            QLabel("透(A)"),
        ]
        self.lineedit_r, self.lineedit_g, self.lineedit_b, self.lineedit_a = [
            QLineEdit(), QLineEdit(),
            QLineEdit(), QLineEdit()
        ]
        for line in [self.lineedit_r, self.lineedit_g, self.lineedit_b, self.lineedit_a]:
            line.setText("255")
        self.lineedit_a.setText("255")
        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.label_r, self.lineedit_r)
        self.formLayout.addRow(self.label_g, self.lineedit_g)
        self.formLayout.addRow(self.label_b, self.lineedit_b)
        self.formLayout.addRow(self.label_a, self.lineedit_a)
        self.colorButton = QPushButton("获取颜色")
        self.colorButton.setFixedSize(90, 30)
        self.colorButton.setObjectName("colorButton")
        self.formLayout.setWidget(self.formLayout.rowCount(), QFormLayout.SpanningRole, self.colorButton)

        self._m_r_lay.addLayout(self.formLayout)

        self.__middle_lay.addWidget(self.operation_st)

    # 线性,径向,辐射面板
    def grabColorWidget(self,g_type):
        if g_type == Handle_Linear:
            self.__line_vlay = QVBoxLayout(self.st_linear_widget)
            self.linearGradient_widget = GradientWidget(Handle_Linear)
            self.linearOperation_color = ColorOperation(Handle_Linear)
            vlay = self.__line_vlay
            gradient_widget = self.linearGradient_widget
            operation_color = self.linearOperation_color
        elif g_type == Handle_Radial:
            self.__radial_vlay = QVBoxLayout(self.st_radial_widget)
            self.radialGradient_widget = GradientWidget(Handle_Radial)
            self.radialOperation_color = ColorOperation(Handle_Radial)
            vlay = self.__radial_vlay
            gradient_widget = self.radialGradient_widget
            operation_color = self.radialOperation_color
        elif g_type == Handle_Conical:
            self.__conical_vlay = QVBoxLayout(self.st_conicalt_widget)
            self.conicalGradient_widget = GradientWidget(Handle_Conical)
            self.conicalOperation_color = ColorOperation(Handle_Conical)
            vlay = self.__conical_vlay
            gradient_widget = self.conicalGradient_widget
            operation_color = self.conicalOperation_color

        gradient_widget.setViewCode(self.view_code)

        operation_color.syncPosed.connect(
            lambda p_type, hand_id, color_scope: gradient_widget.syncPos(p_type, hand_id, color_scope))
        operation_color.syncColor.connect(
            lambda p_type, hand_id, color: gradient_widget.syncColor(p_type, hand_id, color))
        operation_color.syncNewColor.connect(
            lambda p_type, colorScope, color: gradient_widget.syncNewColor(p_type, colorScope, color))
        operation_color.syncDelColor.connect(
            lambda p_type, hand_id: gradient_widget.syncDelColor(p_type, hand_id))

        vlay.addWidget(gradient_widget)
        vlay.addWidget(operation_color)

    # 线性右侧操作区域
    def linearColorOperation(self):
        self._m_r_line_widget = QWidget()
        self._m_r_line_widget.setFixedWidth(100)

        # 待写
        self.linear_view = QPushButton(self._m_r_line_widget)
        self.linear_view.setObjectName("linear_view")
        self.linear_view.resize(100,24)
        self.linear_view.setText("显示代码")
        self.linear_qss = QPushButton(self._m_r_line_widget)
        self.linear_qss.resize(100,24)
        self.linear_qss.setText("QSS")
        self.linear_qss.move(5,30)

        self.operation_st.addWidget(self._m_r_line_widget)

    # 径向右侧操作区域
    def radialColorOperation(self):
        self._m_r_radial_widget = QWidget()
        self._m_r_radial_widget.setFixedWidth(100)

        self.radial_view = QPushButton(self._m_r_radial_widget)
        self.radial_view.setObjectName("radial_view")
        self.radial_view.resize(100, 24)
        self.radial_view.setText("显示代码")

        self.operation_st.addWidget(self._m_r_radial_widget)

    # 径向右侧操作区域
    def conicalColorOperation(self):
        self._m_r_conical_widget = QWidget()
        self._m_r_conical_widget.setFixedWidth(100)

        self.conical_view = QPushButton(self._m_r_conical_widget)
        self.conical_view.setObjectName("conical_view")
        self.conical_view.resize(100, 24)
        self.conical_view.setText("显示代码")

        self.operation_st.addWidget(self._m_r_conical_widget)

    def setLabelRGB(self, c: QColor):
        r, g, b, a = c.getRgb()
        self.lineedit_r.setText(str(r))
        self.lineedit_g.setText(str(g))
        self.lineedit_b.setText(str(b))

    def setDemonstrationColor(self, color: QColor):
        self.demonstration_color_l.setStyleSheet('''
        border-radius:3px;
        background-color:rgba({},{},{},{});
        '''.format(*color.getRgb()))

    def __update_color_event(self, c):
        self.setLabelRGB(c)
        self.hex_line.setText(c.name())
        self.setDemonstrationColor(c)
        self.update()

    # Updates the color block rgb event
    def __update_rgb_event(self, c: QColor):
        self.color_bar.setBgColor(QColor(c))
        self.setLabelRGB(self.color_bar.curColor())
        self.setDemonstrationColor(self.color_bar.curColor())
        self.update()

    # Update transparency
    def update_a_event(self, value: int):
        self.color_bar.setAlpha(value)
        self.lineedit_a.setText(str(value))
        self.setDemonstrationColor(self.color_bar.curColor())
        self.update()

    # emit
    def __emit_color_event(self):
        self.clickColor.emit(QColor(self.hex_line.text()))

    def straw_event(self):
        self.maskWidget = MaskWidget(self.timer)
        # size = desktopAllSize()
        # self.maskWidget.move(-size.width()//2,0)
        # self.maskWidget.resize(size)
        self.maskWidget.resize(100, 100)
        self.maskWidget.show()
        self.timer.start(50)

    def myEvent(self):
        def change_btn_event(index):
            self.st.setCurrentIndex(index)
            self.operation_st.setCurrentIndex(index)

        self.pure_color_btn.clicked.connect(lambda: change_btn_event(0))
        self.line_btn.clicked.connect(lambda: change_btn_event(1))
        self.radial_btn.clicked.connect(lambda: change_btn_event(2))
        self.conical_btn.clicked.connect(lambda: change_btn_event(3))

        # mode change
        def change_mode(mode):
            self.linearGradient_widget.setGrabMode(mode)
            self.radialGradient_widget.setGrabMode(mode)
            self.conicalGradient_widget.setGrabMode(mode)

        self.pad_btn.clicked.connect(lambda: change_mode("pad"))
        self.rep_btn.clicked.connect(lambda: change_mode("repeat"))
        self.ref_btn.clicked.connect(lambda: change_mode("reflect"))

        #
        def hide_hand_event(b):
            self.linearGradient_widget.setHideHand(b)
            self.radialGradient_widget.setHideHand(b)
            self.conicalGradient_widget.setHideHand(b)

        self.hand_btn.clicked.connect(hide_hand_event)

        # view
        def __view():
            self.view_code.show()

        self.linear_view.clicked.connect(__view)
        self.radial_view.clicked.connect(__view)
        self.conical_view.clicked.connect(__view)

        self.hsv.rgbaChange.connect(self.__update_rgb_event)
        self.color_bar.rgbaChange.connect(self.__update_color_event)

        self.splider.valueChanged.connect(self.update_a_event)

        self.colorButton.clicked.connect(self.__emit_color_event)

        self.color_straw_btn.clicked.connect(self.straw_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PaletteTools()
    # win = ColorBar()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
