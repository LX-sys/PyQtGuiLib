# -*- coding:utf-8 -*-
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
    QPaintEvent,
    QPushButton
)
import typing


# 虚拟图形对象类
class VirtualObject:
    def __init__(self):
        # 虚拟对象字典
        self.__virtualObjects = dict()  # type:typing.Dict[str:typing.List]

    def isVirtualObject(self, vobj_name: str)->bool:
        return True if self.__virtualObjects.get(vobj_name,None) else False

    def appendVirtualObject(self, vobj_name: str, **kwargs):
        if not self.isVirtualObject(vobj_name):
            self.__virtualObjects[vobj_name] = kwargs

    def getVirtualObjectAttr(self,vobj_name: str):
        if self.isVirtualObject(vobj_name):
            return self.__virtualObjects[vobj_name]

    def getVirtualObjectAttrValue(self,vobj_name: str,key:str):
        if self.isVirtualObject(vobj_name):
            return self.__virtualObjects[vobj_name][key]

    def getVirtualFunc(self,vobj_name:str)->typing.Callable:
        return self.__virtualObjects[vobj_name]["func"]

    def getVirtualArgs(self,vobj_name:str)->tuple:
        return self.__virtualObjects[vobj_name]["args"]

    def getVirtualOpenAttr(self,vobj_name:str)->dict:
        return self.__virtualObjects[vobj_name]["openAttr"]

    def getVirtualBrushAttr(self,vobj_name:str)->dict:
        return self.__virtualObjects[vobj_name]["brushAttr"]

    def updateArgs(self,vobj_name:str,*args):
        if args:
            self.__virtualObjects[vobj_name]["args"] = args

    def updateOpenAttr(self,vobj_name:str,openAttr:dict):
        if openAttr:
            self.__virtualObjects[vobj_name]["openAttr"] = openAttr

    def updateBrushAttr(self,vobj_name:str,brushAttr:dict):
        if brushAttr:
            self.__virtualObjects[vobj_name]["brushAttr"] = brushAttr

    def updateDraw(self,vobj_name:str,*args,**kwargs):
        self.updateArgs(vobj_name,*args)
        openAttr = kwargs.get("openAttr", None)
        brushAttr = kwargs.get("brushAttr", None)
        self.updateOpenAttr(vobj_name,openAttr)
        self.updateBrushAttr(vobj_name,brushAttr)


class SuperPainterAttr(QPainter):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.__op = QPen(QColor(0,0,0))  # type:QPen
        self.__brush = QBrush(QColor(0,0,0)) # type: QBrush
        self.__font = None  # type: QFont
        self.__virtualObject = VirtualObject()

    def virtualObj(self)->VirtualObject:
        return self.__virtualObject

    def setPen(self, op:QPen):
        if not isinstance(op,QPen):
            op = QPen(op)
        self.__op = op
        super().setPen(op)

    def setBrush(self, brush:QBrush):
        if not isinstance(brush,QBrush):
            brush = QBrush(brush)
        self.__brush = brush
        super().setBrush(brush)

    def open_(self) -> QPen:
        return self.__op

    def setFont(self, font:QFont):
        self.__font = font
        super().setFont(font)

    def isOpen(self) -> bool:
        return True if self.__op else False

    def isBrush(self) -> bool:
        return True if self.__brush else False

    def isFont(self) -> bool:
        return True if self.__font else False

    def clearOpen(self):
        if self.isOpen():
            self.setPen(qt.NoPen)

    def clearBrush(self):
        if self.isBrush():
            self.setBrush(qt.NoBrush)

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
        open_joinStyle = openAttr.get("j_style") or openAttr.get("joinStyle")
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
            op.setColor(QColor(open_color))
        if open_width:
            op.setWidth(open_width)
        if open_style:
            op.setStyle(open_style)
        if open_brush:
            if isinstance(open_brush,str):
                open_brush = QColor(open_color)
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
            brush.setColor(QColor(brush_color))
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
            self.setPen(op)

        if brushAttr:
            self.setBrush(brush)

    def __restorePrivateAttr(self, op:QPen, brush:QBrush):
        if op:
            self.setPen(op)

        if brush:
            self.setBrush(brush)

    def decorator_to_all_draw_methods(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                op = self.open_()
                brush = self.brush()

                openAttr = kwargs.get("openAttr", None)
                brushAttr = kwargs.get("brushAttr", None)
                virtual_object_name = kwargs.get("virtualObjectName",None) or kwargs.get("vobj",None)
                if virtual_object_name:
                    self.__virtualObject.appendVirtualObject(virtual_object_name,func=func,args=args,kwargs=kwargs,
                                                             openAttr=openAttr,brushAttr=brushAttr)

                    args = self.virtualObj().getVirtualArgs(virtual_object_name)
                    if openAttr:
                        openAttr = self.virtualObj().getVirtualOpenAttr(virtual_object_name)
                    if brushAttr:
                        brushAttr = self.virtualObj().getVirtualBrushAttr(virtual_object_name)
                self.__privateAttr(openAttr, brushAttr)
                if openAttr:del kwargs["openAttr"]
                if brushAttr:del kwargs["brushAttr"]
                if virtual_object_name: del kwargs["virtualObjectName"]
                value = func(*args,**kwargs)
                self.__restorePrivateAttr(op,brush)
                return value
            return wrapper

        self.drawRect = decorator(self.drawRect)
        self.drawRoundedRect = decorator(self.drawRoundedRect)
        self.drawLine = decorator(self.drawLine)
        self.drawLines = decorator(self.drawLines)
        self.drawArc = decorator(self.drawArc)
        self.drawEllipse = decorator(self.drawEllipse)
        self.drawPoint = decorator(self.drawPoint)
        self.drawPoints = decorator(self.drawPoints)
        self.drawText = decorator(self.drawText)
        self.drawStaticText = decorator(self.drawStaticText)
        self.drawPolygon = decorator(self.drawPolygon)
        self.drawPie = decorator(self.drawPie)
        self.drawPicture = decorator(self.drawPicture)
        self.drawChord = decorator(self.drawChord)
        self.drawRects = decorator(self.drawRects)
        self.drawPolyline = decorator(self.drawPolyline)
        self.drawPath = decorator(self.drawPath)
        self.drawConvexPolygon = decorator(self.drawConvexPolygon)
        self.drawGlyphRun = decorator(self.drawGlyphRun)
        self.drawPixmap = decorator(self.drawPixmap)
        self.drawImage = decorator(self.drawImage)
        self.drawPixmapFragments = decorator(self.drawPixmapFragments)
        self.drawTiledPixmap = decorator(self.drawTiledPixmap)


class SuperPainter(SuperPainterAttr):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.decorator_to_all_draw_methods()


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        self.painter = SuperPainter()
        self.btn = QPushButton("更新图像",self)
        self.btn.move(300,50)
        self.btn.clicked.connect(lambda :self.test_update())

    def test_update(self):
        print(self.painter.virtualObj().getVirtualObjectAttr("rect_tt"))
        self.painter.virtualObj().updateDraw("rect_tt",20,20,70,70,openAttr={"color":"blue"},brushAttr={"color":"yellow"})
        self.update()
        print(self.painter.virtualObj().getVirtualObjectAttr("rect_tt"))

    def paintEvent(self, e:QPaintEvent) -> None:
        self.painter.begin(self)
        self.painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        self.painter.setPen(QColor(52,44,120))

        self.painter.drawRect(20, 20, 50, 50, openAttr={"color": "red", "brush": "#9bff7d"},brushAttr={"color":"green"},
                              virtualObjectName="rect_tt")

        self.painter.drawLine(70, 70, 200, 200)
        self.painter.drawRect(200, 200, 50, 50,openAttr={"color":"yellow"},brushAttr={"color":"#9bff7d"})

        self.painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()

    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
