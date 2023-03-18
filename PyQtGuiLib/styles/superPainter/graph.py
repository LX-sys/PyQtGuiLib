# -*- coding:utf-8 -*-
# @time:2023/3/1815:50
# @author:LX
# @file:graph.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QWidget,
    QObject,
    QRect,
    QSize,
    QPainter,
    QPoint,
    QPen,
    QBrush,
    QFont,
    qt,
    Qt,
    QColor,
    QPaintEvent
)


class GraphABC(QObject):
    def __init__(self,painter=None,*args,**kwargs):
        super().__init__()

        self.__painter = None # type:QPainter
        self.__op = None  # type:QPen
        self.__brush = None # type: QBrush
        self.__font = None  # type: QFont

        # 参数
        self.__argc = args
        self.__kwargs = kwargs
        if args:
            self.__argc = args
        if kwargs:
            self.__kwargs = kwargs

        if painter:
            self.setPainter(painter)

    def setPainter(self,painter:QPainter):
        self.__painter = painter

    def painter(self)->QPainter:
        return self.__painter

    def setPen(self, op:QPen):
        self.__op = op
        self.painter().setPen(op)

    def setBrush(self, brush:QBrush):
        self.__brush = brush
        self.painter().setBrush(brush)

    def open(self) -> QPen:
        return self.__op

    def brush(self) -> QBrush:
        return self.__brush

    def font(self) -> QFont:
        return self.__font

    def setFont(self, font:QFont):
        self.__font = font
        self.painter().setFont(font)

    def argc(self):
        return self.__argc

    def kwargc(self):
        return self.__kwargs

    def isAgrc(self) -> bool:
        return True if self.__argc else False

    def isKWargc(self) -> bool:
        return True if self.__kwargs else False

    def isOpen(self) -> bool:
        return True if self.__op else False

    def isBrush(self) -> bool:
        return True if self.__brush else False

    def isFont(self) -> bool:
        return True if self.__font else False

    def clearOpen(self):
        if self.isOpen():
            self.painter().setPen(qt.NoPen)

    def clearBrush(self):
        if self.isBrush():
            self.painter().setBrush(qt.NoBrush)

    # 私有属性
    def __privateAttr(self, openAttr:dict=None,brushAttr:dict=None):
        if openAttr is None:
            openAttr = dict()

        if brushAttr is None:
            brushAttr = dict()

        op = QPen()
        open_color = openAttr.get("color") or openAttr.get("c")
        open_width = openAttr.get("width") or openAttr.get("w")
        open_style = openAttr.get("style")
        open_brush = openAttr.get("brush")
        open_capStyle = openAttr.get("cap") or openAttr.get("capStyle")
        open_cosmetic = openAttr.get("cos") or openAttr.get("cosmetic")
        open_joinStyle = openAttr.get("join") or openAttr.get("joinStyle")
        open_miterLimit = openAttr.get("miter") or openAttr.get("miterLimit")
        open_dashOffset = openAttr.get("dashOffset") or openAttr.get("off")
        open_dashPattern = openAttr.get("dashPattern") or openAttr.get("pattern")

        brush = QBrush(Qt.SolidPattern)
        brush_color = brushAttr.get("color") or brushAttr.get("c")
        brush_style = brushAttr.get("style")
        brush_matrix = brushAttr.get("matrix")
        brush_texture = brushAttr.get("texture") or brushAttr.get("tte")
        brush_transform = brushAttr.get("transform") or brushAttr.get("trans")
        brush_textureImage = brushAttr.get("textureImage") or brushAttr.get("image")

        if open_color:
            op.setColor(open_color)
        if open_width:
            op.setWidth(open_width)
        if open_style:
            op.setStyle(open_style)
        if open_brush:
            op.setBrush(open_brush)
        if open_capStyle:
            op.setCapStyle(open_capStyle)
        if open_cosmetic:
            op.setCosmetic(open_cosmetic)
        if open_joinStyle:
            op.setJoinStyle(open_joinStyle)
        if open_miterLimit:
            op.setMiterLimit(open_miterLimit)
        if open_dashOffset:
            op.setDashOffset(open_dashOffset)
        if open_dashPattern:
            op.setDashPattern(open_dashPattern)

        if brush_color:
            brush.setColor(brush_color)
        if brush_style:
            brush.setStyle(brush_style)
        if brush_matrix:
            brush.setMatrix(brush_matrix)
        if brush_texture:
            brush.setTexture(brush_texture)
        if brush_transform:
            brush.setTransform(brush_transform)
        if brush_textureImage:
            brush.setTextureImage(brush_textureImage)

        if openAttr:
            self.painter().setPen(op)

        if brushAttr:
            self.painter().setBrush(brush)

    def __restorePrivateAttr(self, openAttr, brushAttr):
        if openAttr and self.isOpen():
            self.setPen(self.open())

        if brushAttr:
            if self.isBrush() is False:
                self.painter().setBrush(Qt.NoBrush)
            else:
                self.setBrush(self.brush())

    # 需要重写的函数
    def _draw_(self,*args,**kwargs):
        pass

    # 实际调用的函数
    def draw(self,*args,**kwargs):
        openAttr = kwargs.get("openAttr",None)
        brushAttr = kwargs.get("brushAttr",None)
        self.__privateAttr(openAttr,brushAttr)
        if args:
            self._draw_(*args,**kwargs)
        elif self.isAgrc():
            self._draw_(*self.argc(),**self.kwargc())
        else:
            raise Exception("parameter error!")
        print(self.parent().pos())
        self.__restorePrivateAttr(openAttr,brushAttr)


class Rect(GraphABC):
    def __init__(self, painter=None,*args,**kwargs):
        super().__init__(painter,*args,**kwargs)

    def _draw_(self,*args,**kwargs):
        self.painter().drawRect(*args,**kwargs)


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.setMouseTracking(True)

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        c = Rect(painter,QRect(10,10,100,100))
        c.setParent(self)
        c.setPen(QColor(255, 0, 0))
        c.draw()
        c.draw(QRect(100,150,100,100))
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()

    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
