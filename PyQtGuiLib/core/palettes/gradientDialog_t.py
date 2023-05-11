'''

    渐变编辑器
    唯一的不足,窗口大小变化时,渐变区域上的手柄不会跟随变化
'''

import math
import abc
from GUI.genericWidget import GenericMainWindow
from GUI.customControl.generalModel import *
from GUI.customControl.color.colorPlate import PlateDialog
from typing import List


class MyGradientAbstract(metaclass=abc.ABCMeta):
    # def __init__(self, *args, **kwargs):
    #     pass

    @abc.abstractmethod
    def x(self, x: int = None) -> [int, None]:
        pass

    @abc.abstractmethod
    def y(self, y: int = None) -> [int, None]:
        pass

    @abc.abstractmethod
    def pos(self, x: int = None, y: int = None) -> [tuple, None]:
        pass

    @abc.abstractmethod
    def width(self, w: int = None) -> [int, None]:
        pass

    @abc.abstractmethod
    def height(self, h: int = None) -> [int, None]:
        pass

    @abc.abstractmethod
    def size(self, w: int = None, h: int = None) -> [tuple, None]:
        pass

    @abc.abstractmethod
    def pix(self, pix: QPixmap = None) -> [QPixmap, None]:
        '''
            返回pix
        :param pix:
        :return:
        '''
        pass

    @abc.abstractmethod
    def createPix(self) -> None:
        '''
            创建pix
        :return:
        '''
        pass

    @abc.abstractmethod
    def createGradient(self, gradient_: [QLinearGradient, QRadialGradient, QConicalGradient]) -> None:
        pass

    @abc.abstractmethod
    def updateGradient(self) -> None:
        pass

    # 渐变方式
    @abc.abstractmethod
    def spread(self, spread: str = None) -> [str, None]:
        pass

    # 鼠标判断范围
    @abc.abstractmethod
    def isMouseScope(self, e: QtGui.QMouseEvent):
        pass

    def conversion(self, qss: bool = False) -> tuple:
        pass

    def handle(self, painter: QPainter) -> None:
        pass

    def move(self, e: QtGui.QMouseEvent) -> None:
        pass

    def pressed(self, e: QtGui.QMouseEvent):
        pass

    def release(self, e: QtGui.QMouseEvent) -> None:
        pass


# 渐变 停止点 颜色值
class GradientStopColor:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance:

            return cls.__instance
        else:
            obj = object.__new__(cls, *args, **kwargs)
            cls.__instance = obj
            return cls.__instance

    def __init__(self):
        # 渐变的 停止点 和 颜色
        self._gradient_list = [
            (0.0, QColor("blue")),
            (1.0, QColor("red")),
        ]

    def __getitem__(self, item: int) -> tuple:
        return self._gradient_list[item]

    def __setitem__(self, key: int, value: tuple):
        self._gradient_list[key] = value
        self._sort_gradient()

    def add(self, stop: float, color: QColor) -> None:
        self._gradient_list.append((stop, color))
        self._sort_gradient()

    def gradientList(self) -> List[tuple]:
        return self._gradient_list

    # 删除创建的终止点
    def removeStopAtPosition(self, n: int) -> None:
        if n >= 0 and n <= len(self._gradient_list) - 1:
            del self._gradient_list[n]
            self._sort_gradient()

    # 排序(小 -> 大)
    def _sort_gradient(self) -> None:
        self._gradient_list = sorted(self._gradient_list, key=lambda g: g[0])


class MyGradient(MyGradientAbstract):

    def __init__(self, x: int, y: int, w: int, h: int):
        super(MyGradient, self).__init__()
        self._pix = None  # type:[QPixmap,None]
        self._gradient = None  # type:[QLinearGradient,QRadialGradient,QConicalGradient,QGradient,None]
        self._type = ""  # 渐变的类型
        self._spread = "pad"  # 渐变方式
        self._Outer_radius = 10  # 外圈半径
        self._angle = 30  # 渐变角度
        self._lock = True  # 锁
        self._x, self._y = x, y
        self._width, self._height = w, h
        self.gradientStopColor = GradientStopColor()

    def x(self, x: int = None) -> [int, None]:
        if x or x == 0:
            self._x = x
            return
        return self._x

    def y(self, y: int = None) -> [int, None]:
        if y or y == 0:
            self._y = y
            return
        return self._y

    def pos(self, x: int = None, y: int = None) -> [tuple, None]:
        return self.x(x), self.y(y)

    def width(self, w: int = None) -> [int, None]:
        if w or w == 0:
            self._width = w
            return
        return self._width

    def height(self, h: int = None) -> [int, None]:
        if h or h == 0:
            self._height = h
            return
        return self._height

    def size(self, w: int = None, h: int = None) -> [tuple, None]:
        return self.width(w), self.height(h)

    # 外圈半径
    def outerRadius(self, r: int = None) -> [int, None]:
        if r or r == 0:
            self._Outer_radius = r
            return
        return self._Outer_radius

    # 角度
    def angle(self, a: int = None) -> [int, None]:
        if a or a == 0:
            self._angle = a
            return
        return self._angle

    def pix(self, pix: QPixmap = None) -> [QPixmap, None]:
        if pix:
            self._pix = pix
            return None
        return self._pix

    def createPix(self) -> None:
        self._pix = QPixmap(*self.size())
        self._pix.fill(Qt.transparent)

    # 根据不同类型来决定参数的变化
    def parameter(self, gradient_: [QLinearGradient, QRadialGradient, QConicalGradient]) -> tuple:
        if gradient_ == QLinearGradient:
            return *self.pos(), *self.size()
        if gradient_ == QRadialGradient:
            return *self.pos(), self.outerRadius(), *self.size()
        if gradient_ == QConicalGradient:
            return *self.pos(), self.angle()

    def createGradient(self, gradient_: [QLinearGradient, QRadialGradient, QConicalGradient]) -> None:
        painter = QPainter(self.pix())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = gradient_(*self.parameter(gradient_))
        self._gradient = gradient_  # 保存对象
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

    def updateGradient(self) -> None:
        pix = QPixmap(*self.size())
        self.pix(pix)
        painter = QPainter(self.pix())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = self._gradient(*self.parameter(self._gradient))
        # gradient.setSpread(self.getSpread())
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

    # 鼠标判断范围
    def isMouseScope(self, e: QtGui.QMouseEvent):
        if (e.x() >= self.x() and e.x() <= self.x() + self.width() and
                e.y() >= self.y() and e.y() <= self.y() + self.height()
        ):
            return True
        return False

    def spread(self, spread: str = None) -> [str, None]:
        if spread:
            self._spread = spread
            return None

        if self._spread == "pad":
            return QGradient.PadSpread
        if self._spread == "repeat":
            return QGradient.RepeatSpread
        if self._spread == "reflect":
            return QGradient.ReflectSpread

    def spreadStr(self) -> str:
        return self._spread

    # 加锁
    def lock(self):
        self._lock = False

    # 获取锁
    def getLock(self):
        return self._lock

    # 解锁
    def unlock(self):
        self._lock = True


# 线性渐变类
class Line(MyGradient):
    def __init__(self, x: int, y: int, w: int, h: int):
        super(Line, self).__init__(x, y, w, h)
        self._hand_r = 16
        # 两个手柄位置,并初始化在两侧
        self._handlePos = {"blue": [x,
                                    y + h // 2],
                           "red": [x + w - self._hand_r,
                                   y + h // 2]}
        self._handle = "red"  # 当前手柄
        self._qss = {"pad": {"template": "qlineargradient(spread:pad,x1:{},y1:{},x2:{},y2:{},",
                             "qss": ""},
                     "repeat": {"template": "qlineargradient(spread:repeat,x1:{},y1:{},x2:{},y2:{},",
                                "qss": ""},
                     "reflect": {"template": "qlineargradient(spread:reflect,x1:{},y1:{},x2:{},y2:{},",
                                 "qss": ""}
                     }
        # 设置渐变方式
        self.spread("pad")
        self.createPix()
        self.createGradient(QLinearGradient)

    def QSS(self, model: bool = False) -> [str, None]:
        if model:
            return self._qss[self.spreadStr()]["qss"]

        qss = ""
        for stop, color in self.gradientStopColor.gradientList():
            qss += "stop:" + str(stop) + " "
            qss += "rgba{}".format(color.getRgb()) + ","

        pad_qss = self._qss[self.spreadStr()]["template"].format(
            *self.conversion(True)) + qss + ";"
        pad_qss = pad_qss.replace(",;", ");")
        self._qss[self.spreadStr()]["qss"] = pad_qss

    def createGradient(self, gradient_: [QLinearGradient, QRadialGradient, QConicalGradient]) -> None:
        painter = QPainter(self.pix())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        # print(self.conversion(True))
        gradient = gradient_(*self.conversion())
        self._gradient = gradient_  # 保存对象
        gradient.setSpread(self.spread())
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

    def updateGradient(self) -> None:
        pix = QPixmap(*self.size())
        self.pix(pix)
        painter = QPainter(self.pix())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = self._gradient(*self.conversion())
        gradient.setSpread(self.spread())
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

        self.QSS()

    # 将位置参数，转换成渐变可用参数(False)
    # 如果参数为True 则生成QSS样式中的可用参数
    def conversion(self, qss: bool = False) -> tuple:
        if qss:
            x1 = round((self._handlePos["blue"][0] - self.x()) / self.width(), 3)
            y1 = round((self._handlePos["blue"][1] - self.y()) / self.height(), 3)
            x2 = round((self._handlePos["red"][0] - self.x()) / self.width(), 3)
            y2 = round((self._handlePos["red"][1] - self.y()) / self.height(), 3)
            return x1, y1, x2, y2

        return (self._handlePos["blue"][0] - self.x(), self._handlePos["blue"][1] - self.y(),
                self._handlePos["red"][0] - self.x(), self._handlePos["red"][1] - self.y())

    # 直径
    def diameter(self):
        return self._hand_r * 2

    # 当前手柄
    def handleIng(self, handle: str = None):
        if handle:
            self._handle = handle
            return
        return self._handle

    # 手柄坐标x
    def handleX(self, x: int = None):
        if x or x == 0:
            self._handlePos[self.handleIng()][0] = x
            return
        return self._handlePos[self.handleIng()][0]

    # 手柄坐标y
    def handleY(self, y: int = None):
        if y or y == 0:
            self._handlePos[self.handleIng()][1] = y
            return
        return self._handlePos[self.handleIng()][1]

    # 手柄坐标(x,y)
    def handlePos(self, x: int = None, y: int = None):
        return self.handleX(x), self.handleY(y)

    # 判断鼠标是否点在手柄上
    def isMouseHandle(self, e: QtGui.QMouseEvent):
        # 根据点击位置来确认 当前手柄
        for key, pos in self._handlePos.items():
            if (e.x() >= pos[0] and e.x() <= pos[0] + self.diameter() // 2 and
                    e.y() >= pos[1] and e.y() <= pos[1] + self.diameter() // 2
            ):
                self.handleIng(key)
                return True
        return False

    # 操作线性渐变的手柄
    def handle(self, painter: QPainter):
        r = self._hand_r

        # 画出两个手柄
        painter.setBrush(Qt.blue)
        painter.drawEllipse(*self._handlePos["blue"], r, r)

        painter.setBrush(Qt.red)
        painter.drawEllipse(*self._handlePos["red"], r, r)

    def move(self, e: QtGui.QMouseEvent):
        if self.getLock() and self.isMouseScope(e):
            self.handlePos(e.x(), e.y())

    def pressed(self, e: QtGui.QMouseEvent):
        # 如果鼠标点在手柄上,则解锁
        if self.isMouseHandle(e):
            self.unlock()

    def release(self, e: QtGui.QMouseEvent):
        # 鼠标弹起时加锁
        self.lock()


# 径向渐变类
class Repeat(MyGradient):
    def __init__(self, x: int, y: int, w: int, h: int):
        super(Repeat, self).__init__(x, y, w, h)
        self._hand_r = 16
        self._out_hand_r = self.width()  # 外圆半径
        # 两个手柄位置,并初始化在两侧
        self._handlePos = {"blue": [x,
                                    y + self.height() // 2],
                           "red": [x + self.width() - self._hand_r,
                                   y + self.height() // 2],
                           "r": self.width() // 2}
        self._handle = "red"  # 当前手柄

        self._qss = {"pad": {"template": "qradialgradient(spread:pad,cx:{},cy:{},radius:{},fx:{},fy:{},",
                             "qss": ""},
                     "repeat": {"template": "qradialgradient(spread:repeat,cx:{},cy:{},radius:{},fx:{},fy:{},",
                                "qss": ""},
                     "reflect": {"template": "qradialgradient(spread:reflect,cx:{},cy:{},radius:{},fx:{},fy:{},",
                                 "qss": ""}
                     }
        self.spread("pad")
        self.createPix()
        self.createGradient(QRadialGradient)

    def QSS(self, model: bool = False) -> [str, None]:
        if model:
            return self._qss[self.spreadStr()]["qss"]

        qss = ""
        for stop, color in self.gradientStopColor.gradientList():
            qss += "stop:" + str(stop) + " "
            qss += "rgba{}".format(color.getRgb()) + ","

        pad_qss = self._qss[self.spreadStr()]["template"].format(
            *self.conversion(True)) + qss + ";"
        pad_qss = pad_qss.replace(",;", ");")
        self._qss[self.spreadStr()]["qss"] = pad_qss

    def conversion(self, qss: bool = False) -> tuple:
        if qss:
            x1 = round((self._handlePos["blue"][0] - self.x()) / self.width(), 3)
            y1 = round((self._handlePos["blue"][1] - self.y()) / self.height(), 3)
            r = round(self._handlePos["r"] / self.width(), 3)
            x2 = round((self._handlePos["red"][0] - self.x()) / self.width(), 3)
            y2 = round((self._handlePos["red"][1] - self.y()) / self.height(), 3)
            return x1, y1, r, x2, y2

        return (self._handlePos["blue"][0] - self.x(), self._handlePos["blue"][1] - self.y(), self._handlePos["r"],
                self._handlePos["red"][0] - self.x(), self._handlePos["red"][1] - self.y())

    def createGradient(self, gradient_: [QLinearGradient, QRadialGradient, QConicalGradient]) -> None:
        painter = QPainter(self.pix())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = gradient_(*self.conversion())
        self._gradient = gradient_  # 保存对象
        gradient.setSpread(self.spread())
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

    def updateGradient(self) -> None:
        pix = QPixmap(*self.size())
        self.pix(pix)
        painter = QPainter(self.pix())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = self._gradient(*self.conversion())
        gradient.setSpread(self.spread())
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

        self.QSS()

    # 直径
    def diameter(self):
        return self._hand_r * 2

    # 当前手柄
    def handleIng(self, handle: str = None):
        if handle:
            self._handle = handle
            return
        return self._handle

    # 手柄坐标x
    def handleX(self, x: int = None):
        if x or x == 0:
            self._handlePos[self.handleIng()][0] = x
            return
        return self._handlePos[self.handleIng()][0]

    # 手柄坐标y
    def handleY(self, y: int = None):
        if y or y == 0:
            self._handlePos[self.handleIng()][1] = y
            return
        return self._handlePos[self.handleIng()][1]

        # 手柄坐标(x,y)

    def handlePos(self, x: int = None, y: int = None):
        return self.handleX(x), self.handleY(y)

    # 判断鼠标是否点到半径圈
    def isMouseRadius(self, e: QtGui.QMouseEvent):
        # 鼠标点击范围 = 外圈整个范围 - 内圈圆
        diameter = self._out_hand_r * 2  # 外圈直径
        x = abs(int(self._handlePos["blue"][0] - diameter // 2))
        y = abs(int(self._handlePos["blue"][1] - diameter // 2))

        if (
                e.x() > x and e.x() < x + diameter and
                e.y() > y and e.y() < y + diameter and
                not self.isMouseHandle(e)  # 如果点击在内圈上,则去反
        ):
            return True
        return False

    # 判断鼠标是否点在手柄上
    def isMouseHandle(self, e: QtGui.QMouseEvent):
        # 根据点击位置来确认 当前手柄
        for key, pos in self._handlePos.items():
            if type(pos) != list:
                continue
            if (e.x() >= pos[0] and e.x() <= pos[0] + self.diameter() // 2 and
                    e.y() >= pos[1] and e.y() <= pos[1] + self.diameter() // 2
            ):
                self.handleIng(key)
                return True
        return False

    # 操作线性渐变的手柄
    def handle(self, painter: QPainter):
        r = self._hand_r

        # 画出两个手柄
        painter.setBrush(Qt.blue)
        painter.drawEllipse(*self._handlePos["blue"], r, r)

        painter.setBrush(Qt.red)
        painter.drawEllipse(*self._handlePos["red"], r, r)

        _out_r = self._out_hand_r
        x = int(self._handlePos["blue"][0] - _out_r // 2 + self._hand_r // 2)
        y = int(self._handlePos["blue"][1] - _out_r // 2 + self._hand_r // 2)

        # 画出外圈圆
        painter.setPen(Qt.white)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(x, y,
                            _out_r, _out_r)

    def pressed(self, e: QtGui.QMouseEvent):
        # 如果鼠标点在手柄上,则解锁
        if self.isMouseHandle(e):
            self.unlock()

    def release(self, e: QtGui.QMouseEvent):
        # 鼠标弹起时加锁
        self.lock()

    def move(self, e: QtGui.QMouseEvent):
        if self.getLock() and self.isMouseScope(e):
            self.handlePos(e.x(), e.y())

        if self.isMouseScope(e) and self.isMouseRadius(e):
            self._out_hand_r = e.x()
            self._handlePos["r"] = self._out_hand_r // 2


# 角度渐变
class Reflect(MyGradient):
    def __init__(self, x: int, y: int, w: int, h: int):
        super(Reflect, self).__init__(x, y, w, h)
        self._handle_r = 16  # 蓝球半径
        self._out_handle_r = 50  # 线圈半径
        self._grey_handle_r = 10  # 灰色小球半径
        self._angle = 30
        # 角度
        self._Angle = [0, 0, self._angle]
        # 两个手柄位置,并初始化在两侧
        self._handlePos = {"blue": [x,
                                    y + self.height() // 2],
                           "grey": [x + self.width() - self._handle_r,
                                    y + self.height() // 2],
                           "angle": self._angle}
        self._handle = "blue"
        self._qss = {"template": "qconicalgradient(cx:{}, cy:{}, angle:{} ",
                     "qss": ""
                     }
        self.createPix()
        self.createGradient(QConicalGradient)

    # 直径
    def diameter(self):
        return self._handle_r * 2

    def QSS(self, model: bool = False) -> [str, None]:
        if model:
            return self._qss["qss"]

        qss = ""
        for stop, color in self.gradientStopColor.gradientList():
            qss += "stop:" + str(stop) + " "
            qss += "rgba{}".format(color.getRgb()) + ","

        pad_qss = self._qss["template"].format(
            *self.conversion(True)) + qss + ";"
        pad_qss = pad_qss.replace(",;", ");")
        self._qss["qss"] = pad_qss

    def conversion(self, qss: bool = False) -> tuple:
        x = round((self._handlePos["blue"][0] - self.x()) / self.width(), 3)
        y = round((self._handlePos["blue"][1] - self.y()) / self.height(), 3)
        a = self._angle
        if qss:
            return x, y, a
        # 角度渐变比较特殊,是以中心为扩散点
        return (self._handlePos["blue"][0] - self.x() + self._handle_r // 2,
                self._handlePos["blue"][1] - self.y() + self._handle_r // 2, self._angle)

    # 当前手柄
    def handleIng(self, handle: str = None):
        if handle:
            self._handle = handle
            return
        return self._handle

    # 手柄坐标x
    def handleX(self, x: int = None):
        if x or x == 0:
            self._handlePos[self.handleIng()][0] = x
            return
        return self._handlePos[self.handleIng()][0]

    # 手柄坐标y
    def handleY(self, y: int = None):
        if y or y == 0:
            self._handlePos[self.handleIng()][1] = y
            return
        return self._handlePos[self.handleIng()][1]

    # 手柄坐标(x,y)
    def handlePos(self, x: int = None, y: int = None):
        return self.handleX(x), self.handleY(y)

    def createGradient(self, gradient_: [QLinearGradient, QRadialGradient, QConicalGradient]) -> None:
        painter = QPainter(self.pix())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = gradient_(*self.conversion())
        self._gradient = gradient_  # 保存对象
        # gradient.setSpread(self.spread())
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

    def updateGradient(self) -> None:
        pix = QPixmap(*self.size())
        self.pix(pix)
        painter = QPainter(self.pix())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = self._gradient(*self.conversion())
        # gradient.setSpread(self.spread())
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

        self.QSS()

    def greyBallPos(self) -> tuple:
        outer_r = self._out_handle_r // 2  # 外圈半径
        bx = int(self._handlePos["blue"][0] - outer_r + self._handle_r // 2)
        by = int(self._handlePos["blue"][1] - outer_r + self._handle_r // 2)
        x, y = abs(bx + outer_r - self._grey_handle_r // 2), abs(by + outer_r - self._grey_handle_r // 2)
        # 求角度的弧度 = self._angle*math.pi/180
        radian = math.radians(self._angle)
        gx = int(x + outer_r * math.cos(radian))
        gy = int(y + outer_r * math.sin(radian))
        return gx, gy

    def handle(self, painter: QPainter):
        r = self._handle_r
        painter.setBrush(Qt.blue)
        painter.drawEllipse(self._handlePos["blue"][0],
                            self._handlePos["blue"][1],
                            r, r)

        # 画出轨迹
        r = self._out_handle_r
        x = int(self._handlePos["blue"][0] - r // 2 + self._handle_r // 2)
        y = int(self._handlePos["blue"][1] - r // 2 + self._handle_r // 2)
        painter.setPen(Qt.white)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(x, y, r, r)

        gx, gy = self.greyBallPos()
        # 画出角度调整球
        painter.setBrush(Qt.gray)
        painter.drawEllipse(gx, gy, self._grey_handle_r, self._grey_handle_r)
        self._handlePos["grey"][0] = gx
        self._handlePos["grey"][1] = gy
        # if self._flge_text:
        # 画出角度数字
        painter.drawText(gx, gy, str(self.angle()))

    def isMouseHandle(self, e: QtGui.QMouseEvent):
        # 根据点击位置来确认 当前手柄
        for key, pos in self._handlePos.items():
            if type(pos) != list:
                continue
            if (e.x() >= pos[0] and e.x() <= pos[0] + self.diameter() // 2 and
                    e.y() >= pos[1] and e.y() <= pos[1] + self.diameter() // 2
            ):
                self.handleIng(key)
                return True
        return False

    def isMouseGrey(self, e: QtGui.QMouseEvent):
        if (e.x() >= self._handlePos["grey"][0] and e.x() <= self._handlePos["grey"][0] + self._grey_handle_r and
                e.y() >= self._handlePos["grey"][1] and e.y() <= self._handlePos["grey"][1] + self._grey_handle_r
        ):
            return True
        return False

    def move(self, e: QtGui.QMouseEvent) -> None:
        if self.getLock() and self.isMouseScope(e):
            self.handlePos(e.x(), e.y())

        if self.isMouseScope(e) and self.isMouseGrey(e):
            # 基本完成
            if self.angle() < 360:  # 角度不能超过360
                self._handlePos["angle"] = self.angle()
                self.angle(self.angle() + 1)
            else:
                self._handlePos["angle"] = 0
                self.angle(0)

    def pressed(self, e: QtGui.QMouseEvent):
        # 如果鼠标点在手柄上,则解锁
        if self.isMouseHandle(e):
            self.unlock()

    def release(self, e: QtGui.QMouseEvent):
        # 鼠标弹起时加锁
        self.lock()


# 渐变停止器
class GradientStop(MyGradient):
    def __init__(self, x: int, y: int, w: int, h: int = 50):
        super(GradientStop, self).__init__(x, y, w, h)
        # 色板对话框
        self.color_palte = PlateDialog()
        self._colorflag = False  # 是否显示的标记

        self.gradientStopColor = GradientStopColor()
        self.ellipse_r = 8
        self._drag_position = None
        self._old_drag_position = None

    def colorFlag(self, b: bool = None):
        if b:
            self._colorflag = b
            return
        return self._colorflag

    def getOldDragPosition(self) -> int:
        return self._old_drag_position

    # 直径
    def diameter(self):
        return self.ellipse_r * 2

    # 创建渐变终止器
    def createGradientStops(self):
        self.gradientPlatePix = QPixmap(*self.size())
        self.gradientPlatePix.fill(Qt.transparent)
        # 赋值
        self.pix(self.gradientPlatePix)

        painter = QPainter(self.gradientPlatePix)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

    def updateGradientStops(self):
        # 更新大小
        self.gradientPlatePix = QPixmap(*self.size())
        # 赋值
        self.pix(self.gradientPlatePix)

        painter = QPainter(self.gradientPlatePix)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        for stop, color in self.gradientStopColor.gradientList():
            gradient.setColorAt(stop, color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, *self.size())

    def handle(self, painter: QPainter) -> None:
        # 渐变终止器圈
        for stop, c in self.gradientStopColor.gradientList():
            painter.setBrush(c)
            painter.drawEllipse(int(self.x() + self.width() * stop - self.ellipse_r),
                                self.y() + 15,
                                self.diameter(), self.diameter())

    # 判断鼠标是否在渐变终止器的区域
    def isGradientStopArea(self, e: QtGui.QMouseEvent):
        if (e.x() >= self.x() and
                e.x() <= self.x() + self.width() - self.ellipse_r and
                e.y() >= self.y() and
                e.y() <= self.y() + self.height() - self.ellipse_r
        ):
            return True
        return False

    def doubleClick(self, e: QtGui.QMouseEvent):
        if self.isGradientStopArea(e):
            # 双击添加圆圈
            stop = (e.x() - self.x()) / self.width()
            self.gradientStopColor.add(round(stop, 3), QColor("white"))
            # 立刻设置当前值
            for n, (stop_v, color) in enumerate(self.gradientStopColor.gradientList()):
                if stop_v == stop:
                    self._old_drag_position = n  # 给右键变色存值
            self.updateGradientStops()

    def pressed(self, e: QtGui.QMouseEvent):
        for n, (stop_v, color) in enumerate(self.gradientStopColor.gradientList()):
            if (e.x() >= stop_v * self.width() + self.x() - self.diameter() and
                    e.x() <= stop_v * self.width() + self.x() + self.diameter()
            ):
                if e.buttons() == Qt.LeftButton:
                    self._drag_position = n
                    self._old_drag_position = n  # 给右键变色存值
                if e.buttons() == Qt.RightButton:
                    self.colorFlag(True)
                    # self.color_palte.show()

    def release(self, e: QtGui.QMouseEvent) -> None:
        self._drag_position = None

    def move(self, e: QtGui.QMouseEvent) -> None:
        # 终止器位置判定
        if (self._drag_position or self._drag_position == 0) and self.isGradientStopArea(e):
            #
            stop = (e.x() - self.x()) / self.width()
            stop_v, color = self.gradientStopColor[self._drag_position]
            self.gradientStopColor[self._drag_position] = stop, color
            self.updateGradientStops()


class GradientDialog(GenericMainWindow):
    gradientChange = pyqtSignal(str)

    # 控件的位置,大小
    CONTROL_POS = 40, 40
    # 鼠标右键列表
    Right_Key_LIST = ['删除', '颜色']
    # 渐变类型按钮样式
    BTN_TYPE_QSS = [
        "qlineargradient(spread:pad,x1:0.289,y1:0.51,x2:1.03,y2:0.5,stop:0.002 rgba(39, 178, 199, 255),stop:0.983 rgba(255, 248, 249, 255));",
        "qradialgradient(spread:pad,cx:0.472,cy:0.463,radius:0.285,fx:0.462,fy:0.517,stop:0.006 rgba(242, 248, 250, 255),stop:0.983 rgba(44, 198, 241, 255));",
        "qconicalgradient(cx:0.48, cy:0.54, angle:42 stop:0.009 rgba(37, 236, 246, 255),stop:1.0 rgba(250, 251, 251, 255));"]
    # 按钮直径的间隔
    BTN_INTERVAL = 10
    # 渐变方式按钮列表
    BTN_WAY_LIST = ["pad", "repeat", "reflect"]
    # 渐变方式按钮样式
    BTN_WAY_QSS = [
        "qlineargradient(spread:pad,x1:0.0,y1:0.5,x2:0.942,y2:0.577,stop:0.0 rgba(0, 0, 255, 255),stop:0.967 rgba(250, 250, 250, 255));",
        "qlineargradient(spread:repeat,x1:0.439,y1:0.157,x2:0.752,y2:0.157,stop:0.0 rgba(0, 22, 192, 255),stop:0.977 rgba(247, 247, 250, 255));",
        "qlineargradient(spread:reflect,x1:0.573,y1:0.56,x2:0.745,y2:0.56,stop:0.0 rgba(0, 0, 255, 255),stop:0.984 rgba(248, 247, 247, 255));"]

    def __init__(self, *args, **kwargs):
        super(GradientDialog, self).__init__(*args, **kwargs)
        self.resize(500, 500)
        self._line = Line(x=20, y=50, w=self.width(), h=300)
        self._r = Repeat(x=20, y=50, w=self.width(), h=300)
        self._a = Reflect(x=20, y=50, w=self.width(), h=300)

        # 当前操作的渐变对象
        self._obj = self._line
        # 按钮控件类型的初始位置
        self._control_type_start_pos = self._line.x()

        # 渐变终止器对象
        self._g = GradientStop(x=self._line.x(), y=40 + self._line.height() + 25, w=self._line.width())

        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.init()
        self.myEvent()

    def init(self):
        # 添加按钮控件
        self.addControl()
        self._g.createGradientStops()
        self.createMenu()

    # 创建 鼠标右键菜单
    def createMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contextMenu = QMenu(self)
        for text in self.Right_Key_LIST:
            obj = self.contextMenu.addAction(text)
            obj.triggered.connect(lambda triggered: self.myMenu())

    def myEvent(self):
        self._g.color_palte.rgbaChange[tuple].connect(self.colorChange)
        self.customContextMenuRequested.connect(self.showMenu)

    # 菜单事件
    def myMenu(self):
        text = self.sender().text()
        if text == "删除":
            n = self._g.getOldDragPosition()
            self._g.gradientStopColor.removeStopAtPosition(n)
            self.gradientObj().updateGradient()  # 提交更新渐变区域
            self._g.updateGradientStops()  # 提交更新渐变终止器
            self.update()  # 更新
        if text == "颜色":
            if self._g.colorFlag():
                self._g.color_palte.show()
                self._g.colorFlag(False)

    def showMenu(self, pos):
        # pos 鼠标位置
        # 菜单显示前,将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    # 渐变终止器事件
    def colorChange(self, rgba: tuple):
        if self._g._old_drag_position or self._g._old_drag_position == 0:
            stop_v, color = self._g.gradientStopColor[self._g._old_drag_position]
            self._g.gradientStopColor[self._g._old_drag_position] = round(stop_v, 3), QColor(*rgba)
            self._g.updateGradientStops()
            self.update()
            self.gradientChange.emit(self.gradientObj().QSS(True))

    def addControl(self):
        for gradientObj, qss in zip([self._line, self._r, self._a], self.BTN_TYPE_QSS):
            btn = QPushButton(self)
            btn.resize(*self.CONTROL_POS)
            btn.setStyleSheet("background-color:" + qss)
            btn.move(self._control_type_start_pos, 0)
            self._control_type_start_pos += self.CONTROL_POS[0] + self.BTN_INTERVAL
            btn.clicked.connect(lambda checked, obj=gradientObj: self._changeType(obj))

        self._control_type_start_pos = self._control_type_start_pos + 20

        # 创建渐变方式控件
        for text, qss in zip(self.BTN_WAY_LIST, self.BTN_WAY_QSS):
            btn = QPushButton(self)
            btn.resize(*self.CONTROL_POS)
            btn.setStyleSheet("background-color:" + qss)
            btn.move(self._control_type_start_pos, 0)
            self._control_type_start_pos += self.CONTROL_POS[0] + self.BTN_INTERVAL
            btn.clicked.connect(lambda checked, t=text: self._changeWay(t))

    def _changeType(self, obj: None):
        if obj:
            self._obj = obj
        self.gradientObj().updateGradient()
        self.update()
        self.gradientChange.emit(self.gradientObj().QSS(True))

    # 切换渐变方式事件
    def _changeWay(self, way: str):
        self.gradientObj().spread(way)
        self.gradientObj().updateGradient()
        self.update()
        self.gradientChange.emit(self.gradientObj().QSS(True))

    # 当前操作的渐变对象
    def gradientObj(self) -> [QLinearGradient, QRadialGradient, QConicalGradient]:
        return self._obj

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)  # 启用抗锯齿
        # 渐变区域
        painter.setPen(Qt.white)
        painter.drawPixmap(self.gradientObj().x(), self.gradientObj().y(), self.gradientObj().pix())

        self.gradientObj().handle(painter)
        self.gradientObj().updateGradient()

        # 渐变终止器
        painter.drawPixmap(self._g.x(), self._g.y(), self._g.pix())
        self._g.handle(painter)
        self._g.updateGradientStops()

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        self._g.doubleClick(e)
        self.update()
        self.gradientChange.emit(self.gradientObj().QSS(True))

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        self.gradientObj().move(e)
        self._g.move(e)
        self.update()
        self.gradientChange.emit(self.gradientObj().QSS(True))

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.gradientObj().pressed(e)
        self._g.pressed(e)
        self.update()
        self.gradientChange.emit(self.gradientObj().QSS(True))

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        self.gradientObj().release(e)
        self._g.release(e)
        self.update()
        self.gradientChange.emit(self.gradientObj().QSS(True))

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        w = e.size().width() - 30
        self.gradientObj().width(w)
        self._g.width(w)
        self.update()

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == 81:
            self.close()
        super(GradientDialog, self).keyPressEvent(e)


# -----测试
class Test(GenericMainWindow):
    def __init__(self):
        super(Test, self).__init__()
        self.setWindowTitle("das")
        self.resize(500, 500)
        self.myEvent()

    def setUI(self):
        self.c = GradientDialog(self)
        self.c.show()

    def myEvent(self):
        self.c.gradientChange[str].connect(self.test)

    def test(self, g: str):
        # print(g)
        self.setStyleSheet("background-color:" + g)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    sys.exit(app.exec_())

