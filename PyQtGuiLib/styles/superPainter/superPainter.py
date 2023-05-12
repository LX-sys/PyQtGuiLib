# -*- coding:utf-8 -*-
from PyQtGuiLib.header import (
    QPainter,
    QPen,
    QBrush,
    QFont,
    qt,
    Qt,
    QColor,
    QPoint,
    QRect,
)
import typing

'''
        drawRect 有(x,y)
        drawRoundedRect  有(x,y)
        drawLine 有(x,y)
        drawLines  
        drawArc  有(x,y)
        drawEllipse  有(x,y)
        drawPoint  有(x,y)
        drawPoints 
        drawText 有(x,y)
        drawStaticText 
        drawPolygon 
        drawPie 有(x,y)
        drawPicture 有(x,y)
        drawChord 有(x,y)
        drawRects 
        drawPolyline 
        drawPath 
        drawConvexPolygon 
        drawGlyphRun 
        drawPixmap 有(x,y)
        drawImage 有(x,y)
        drawPixmapFragments 
        drawTiledPixmap 有(x,y)
'''
RECT_TYPES = ["drawRect","drawRoundedRect","drawLine","drawArc","drawEllipse","drawPoint",
                "drawText","drawPie","drawPicture","drawChord","drawPixmap","drawImage","drawTiledPixmap"]


# 图形分类函数
def patternClassification(name:str):
    '''
        返回参数含义:
            Rect 表示前两个参数是x,y,可以直接进行移动操作

    :param name:
    :return:
    '''
    if name in RECT_TYPES:
        return "Rect"


class VirtualObject:
    def __init__(self,vobj_name:str,**kwargs):
        self.__vobj_name = vobj_name
        self.__vir_attr = kwargs # 虚拟属性

        self.__isHide = False

    def setHide(self,b:bool):
        self.__isHide = b

    def isHide(self)->bool:
        return self.__isHide

    def type(self)->str:
        return self.getVirtualFunc().__name__

    def virName(self) -> str:
        return self.__vobj_name

    def getVirtualObjectAttr(self) -> dict:
        return self.__vir_attr

    def getVirtualObjectAttrValue(self, key: str):
        return self.getVirtualObjectAttr()[key]

    def getVirtualFunc(self) -> typing.Callable:
        return self.getVirtualObjectAttr()["func"]

    def getVirtualArgs(self) -> tuple:
        return self.getVirtualObjectAttr()["args"]

    def getVirtualOpenAttr(self) -> dict:
        return self.getVirtualObjectAttr()["openAttr"]

    def getVirtualBrushAttr(self)->dict:
        return self.getVirtualObjectAttr()["brushAttr"]

    def updateArgs(self,*args):
        if args:
            self.getVirtualObjectAttr()["args"] = args

    def updateOpenAttr(self,openAttr:dict):
        if openAttr:
            self.getVirtualObjectAttr()["openAttr"] = openAttr

    def updateBrushAttr(self,brushAttr:dict):
        if brushAttr:
            self.getVirtualObjectAttr()["brushAttr"] = brushAttr

    def updateDraw(self,*args,**kwargs):
        self.updateArgs(self.virtualObjName(),*args)
        openAttr = kwargs.get("openAttr", None)
        brushAttr = kwargs.get("brushAttr", None)
        self.updateOpenAttr(self.virtualObjName(),openAttr)
        self.updateBrushAttr(self.virtualObjName(),brushAttr)

    def __getRect(self)->QRect:
        return QRect(*self.getVirtualArgs())

    # 根据下标索引来修改
    def updateIndexToArgs(self,i:int,value):
        args = list(self.getVirtualArgs())
        args[i] = value
        self.updateArgs(*args)

    # 移动
    def move(self,x,y):
        if patternClassification(self.type()) == "Rect":
            args = self.getVirtualArgs()[2:]
            self.updateArgs(x,y,*args)

    # 缩放
    def scale(self,proportion:float):
        if patternClassification(self.type()) == "Rect":
            x, y, w, h = self.getVirtualArgs()
            w,h = int(w*proportion),int(h*proportion)
            self.updateArgs(x,y,w,h)

    # 检测鼠标是否点在图形上
    def isClick(self,pos:QPoint)->bool:
        if patternClassification(self.type()) == "Rect":
            x,y,w,h = self.getVirtualArgs()
            cx,cy = pos.x(),pos.y()

            if cx >= x and cx <= x+w and cy >= y and cy <= y+h:
                return True
            return False


# 虚拟图形对象管理类
class VirtualObjectManagement:
    def __init__(self):
        '''
            虚拟对象管理
        '''
        self.__virtualObjects = dict()  # type:typing.Dict[str:typing.List]

    def virtualObjName(self,vobj_name:str)->str:
        if self.isVirtualObject(vobj_name):
            return self.__virtualObjects[vobj_name]
        else:
            raise Exception("[{}] The virtual object does not exist!".format(vobj_name))

    def isVirtualObject(self,vobj_name:str)->bool:
        return True if self.__virtualObjects.get(vobj_name,None) else False

    def appendVirtualObject(self, vobj_name: str, **kwargs):
        if not self.isVirtualObject(vobj_name):
            self.__virtualObjects[vobj_name] = VirtualObject(vobj_name,**kwargs)


class SuperPainterAttr(QPainter):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.__op = QPen(QColor(0,0,0))  # type:QPen
        self.__brush = QBrush(QColor(0,0,0)) # type: QBrush
        self.__font = None  # type: QFont
        self.__virtualObject = VirtualObjectManagement() # 虚拟对象

    def virtualObj(self,vobj_name:str)->VirtualObject:
        return self.__virtualObject.virtualObjName(vobj_name)

    def isVirtualObj(self,vobj_name:str)->bool:
        return self.__virtualObject.isVirtualObject(vobj_name)

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
                    vir_obj = self.virtualObj(virtual_object_name)
                    args = vir_obj.getVirtualArgs()
                    vir_openAttr = vir_obj.getVirtualOpenAttr()
                    vir_brushAttr = vir_obj.getVirtualBrushAttr()

                    if openAttr:openAttr = vir_openAttr
                    elif vir_openAttr:
                        openAttr = vir_openAttr
                        kwargs["openAttr"] = openAttr
                    if brushAttr:brushAttr = vir_brushAttr
                    elif vir_brushAttr:
                        brushAttr = vir_brushAttr
                        kwargs["brushAttr"] = brushAttr

                self.__privateAttr(openAttr, brushAttr)
                if openAttr: del kwargs["openAttr"]
                if brushAttr: del kwargs["brushAttr"]
                if virtual_object_name: del kwargs["virtualObjectName"]

                if virtual_object_name and vir_obj.isHide() is False:
                    func(*args, **kwargs)
                else:
                    func(*args, **kwargs)
                self.__restorePrivateAttr(op, brush)
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

    # ------------下面代码是作为工具的提示代码------------

    def drawRect(self, x:int,y:int,w:int,h:int,
                 openAttr:dict=None,brushAttr:dict=None,virtualObjectName:str="") -> None:
        super().drawRect(x,y,w,h)

    def drawRoundedRect(self, x:int,y:int,w:int,h:int,r:int=5,r2:int=5,
                        openAttr:dict=None,brushAttr:dict=None,virtualObjectName:str="") -> None:
        super().drawRoundedRect(x,y,w,h,r,r2)

    def drawLine(self, x:int,y:int,x1:int,y1:int,
                 openAttr:dict=None,brushAttr:dict=None,virtualObjectName:str="") -> None:
        super().drawLine(x,y,x1,y1)

    def drawLines(self,*args,openAttr:dict=None,brushAttr:dict=None,virtualObjectName:str="")->None:
        super().drawLines(*args)

    def drawPixmap(self,rect:QRect,pix):
        super().drawPixmap(rect,pix)


class SuperPainter(SuperPainterAttr):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.decorator_to_all_draw_methods()

