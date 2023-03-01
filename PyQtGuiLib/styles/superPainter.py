'''


'''

from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QPainter,
    QPainterPath,
    QColor,
    QRect,
    QPoint,
    QSize,
    QFont,
    QBrush,
    QWidget,
    QPaintEvent,
    QPen,
    qt,
    Qt,
    QPushButton,
    QGraphicsDropShadowEffect,
    QPolygon,
    QImage,
    QLine,
    QPicture,
    QPixmap,
    QPolygonF,
    QPointF
)


import math

'''
    超级画师(绘制+交互)
'''


class SuperPainter:
    def __init__(self,parent:QWidget=None):
        '''
            创建画师和画师路径对象
            op:QPen() 对象
            brush:QBrush() 对象
            font: QFont() 对象

        '''
        self.__painter = QPainter()
        self.__painterPath = QPainterPath()

        self.__op = None
        self.__brush = None
        self.__font = None

        self.__parent = parent  # type:QWidget

        if parent:
            self.begin()
            self.painter().setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform)

        # 默认画笔
        op = QPen()
        op.setColor(qt.black)
        self.setPen(op)

    def painter(self) -> QPainter:
        return self.__painter

    def painterPath(self) -> QPainterPath:
        return self.__painterPath

    def begin(self,parent=None):
        if parent:
            self.__painter.begin(parent)
        else:
            self.__painter.begin(self.__parent)

    def end(self):
        self.__painter.end()

    def setPen(self, op:QPen):
        self.__op = op
        self.painter().setPen(op)

    def setBrush(self, brush:QBrush):
        self.__brush = brush
        self.painter().setBrush(brush)

    def setFont(self, font:QFont):
        self.__font = font
        self.painter().setFont(font)

    def setRenderHints(self,*args):
        self.painter().setRenderHints(*args)

    def open(self) -> QPen:
        return self.__op

    def brush(self) -> QBrush:
        return self.__brush

    def font(self) -> QFont:
        return self.__font

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
    def __privateAttr(self, openAttr:dict,brushAttr:dict):
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

    # 阴影(暂时不需要阴影)
    def __shadowRect(self, x,y, w, h,r=10, imageCall=None, shadowAttr:dict = dict()):
        x+=5
        y+=5
        w-=8
        h-=8
        shadow_color = shadowAttr.get("color") or shadowAttr.get("c")  # 阴影颜色
        shadow_radius = shadowAttr.get("radius", 0) or shadowAttr.get("r", 0)
        shadow_x = shadowAttr.get("offx",0) or shadowAttr.get("x",0)
        shadow_y = shadowAttr.get("offy",0) or shadowAttr.get("y",0)

        if shadow_color:
            self.painter().setPen(qt.NoPen)
            self.painter().setBrush(QBrush(shadow_color, Qt.SolidPattern))
            # imageCall(x,y,w,h,r,r)
        if shadow_radius:
            for i in range(0, r):  # 循环绘制多个圆形
                opacity = int(255 * pow(0.75, i))  # 计算当前圆形的 alpha 值
                shadow_color.setAlpha(opacity)  # 设置当前圆形的阴影颜色
                self.painter().setBrush(QBrush(shadow_color, Qt.SolidPattern))  # 设置当前圆形的画刷
                imageCall(x+shadow_x-i, y+shadow_y-i, w + i*2, h + i*2,r,r)  # 绘制当前圆形

    # 画矩形
    def drawRect(self, x=0,y=0, w=50, h=50, openAttr:dict = dict(), brushAttr:dict = dict(),
                 shadowAttr:dict = dict()):
        '''
            openAttr,brushAttr: 是私人样式,不与其他的图像共享
            shadowAttr: 阴影属性
        '''
        # --
        rect = QRect(x, y, w, h)

        self.__shadowRect(x,y,w,h,imageCall=self.painter().drawRoundedRect,shadowAttr=shadowAttr)

        self.__privateAttr(openAttr,brushAttr)

        self.painter().drawRect(rect)

        self.__restorePrivateAttr(openAttr,brushAttr)

    def drawRoundedRect(self,x=0,y=0, w=50, h=50,r=3,mode=Qt.AbsoluteSize,openAttr:dict = dict(), brushAttr:dict = dict(),shadowAttr:dict = dict()):
        '''

        :param mode:
            Qt.AbsoluteSize
            Qt.RelativeSize
        :return:
        '''
        rect = QRect(x, y, w, h)

        self.__shadowRect(x,y,w,h,imageCall=self.painter().drawRoundedRect,shadowAttr=shadowAttr)

        self.__privateAttr(openAttr, brushAttr)

        self.painter().drawRoundedRect(rect,r,r,mode=mode)

        self.__restorePrivateAttr(openAttr, brushAttr)

    # 画直线
    def drawLine(self,x=None,y=None, w=None, h=None, openAttr:dict = dict(), brushAttr:dict = dict()):
        '''
            参数形式
                x,y,w,h
                x,y,w
                x,y,h
        '''
        self.__privateAttr(openAttr,brushAttr)

        if [x,y,w,h].count(None) == 4:
            if x is None:
                x = 0
            if y is None:
                y = 0
            if w is None:
                w = 50
            if h is None:
                h = 0
        elif [x,y,w,h].count(None) ==0:
            pass
        elif x and y and w:
            h = y
        elif x and y and h:
            w = x
        else:
            raise ValueError("parameter error!")

        self.painter().drawLine(x,y,w,h)

        self.__restorePrivateAttr(openAttr,brushAttr)

    # 画文字
    def drawText(self,x=0,y=0, w=100, h=50,text:str="hello wrold", openAttr:dict = dict(), brushAttr:dict = dict(),flags=Qt.AlignLeft):
        '''
            flags:参数
                Qt.AlignLeft: 左对齐
                Qt.AlignRight: 右对齐
                Qt.AlignHCenter: 水平居中对齐
                Qt.AlignTop: 顶部对齐
                Qt.AlignBottom: 底部对齐
                Qt.AlignVCenter: 垂直居中对齐
                Qt.AlignCenter: 居中对齐（水平和垂直居中
        '''

        rect = QRect(x, y, w, h)
        self.__privateAttr(openAttr,brushAttr)

        self.painter().drawText(rect, flags, text)

        self.__restorePrivateAttr(openAttr,brushAttr)

    # 画弧
    def drawArc(self,x=0,y=0, w=100, h=50,startAngle:int=30,spanAngle:int=180,openAttr:dict = dict(), brushAttr:dict = dict()):
        '''
            这个两个参数默认都会*16
        :param startAngle:
        :param spanAngle:

        :return:
        '''

        startAngle *= 16
        spanAngle *= 16

        rect = QRect(x, y, w, h)

        self.__privateAttr(openAttr, brushAttr)

        self.painter().drawArc(rect,spanAngle,spanAngle)

        self.__restorePrivateAttr(openAttr, brushAttr)

    # 画和弦
    def drawChord(self,x=0,y=0, w=100, h=50,startAngle:int=30,spanAngle:int=180,openAttr:dict = dict(), brushAttr:dict = dict()):
        '''
            这个两个参数默认都会*16
        :param startAngle:
        :param spanAngle:

        :return:
        '''

        startAngle *= 16
        spanAngle *= 16

        rect = QRect(x, y, w, h)

        self.__privateAttr(openAttr, brushAttr)

        self.painter().drawChord(rect,spanAngle,spanAngle)

        self.__restorePrivateAttr(openAttr, brushAttr)

    # 画圆
    def drawEllipse(self,x=0,y=0, w=None, h=None,rx:int=None,ry:int=None,openAttr:dict = dict(), brushAttr:dict = dict()):

        '''
            传参方式:
                x,y,rx=x,ry=x
                x,y,w,h
                x,y,w,h,rx,ry
        '''
        self.__privateAttr(openAttr, brushAttr)
        if (ry and ry) is None and (x and y and w and h):
            self.painter().drawEllipse(x,y,w,h)
        elif x and y and rx and ry:
            self.painter().drawEllipse(QPoint(x,y),rx,ry)
        else:
            self.painter().drawEllipse(x,y,w,h,rx,rx)

        self.__restorePrivateAttr(openAttr, brushAttr)

    # 画多边形
    def drawConvexPolygon(self,points:list,openAttr:dict = dict(), brushAttr:dict = dict()):

        self.__privateAttr(openAttr, brushAttr)
        polygon = QPolygon()
        for i in points:
            polygon.append(i)
        self.painter().drawConvexPolygon(polygon)

        self.__restorePrivateAttr(openAttr, brushAttr)

    # image
    def drawImage(self,x=0,y=0, w=100, h=50,path:str=None,openAttr:dict = dict(), brushAttr:dict = dict()):

        if path is None:
            raise Exception("No image path!")

        rect = QRect(x, y, w, h)

        self.__privateAttr(openAttr, brushAttr)

        self.painter().drawImage(rect,QImage(path))

        self.__restorePrivateAttr(openAttr, brushAttr)

    def drawPath(self,ppath:QPainterPath,openAttr:dict = dict(), brushAttr:dict = dict()):
        self.__privateAttr(openAttr, brushAttr)
        self.painter().drawPath(ppath)
        self.__restorePrivateAttr(openAttr, brushAttr)

    def drawPicture(self,x=0,y=0,picture:QPicture=None,openAttr:dict = dict(), brushAttr:dict = dict()):
        if picture is None:
            raise Exception("QPicture cannot be None !")

        self.__privateAttr(openAttr, brushAttr)
        self.painter().drawPicture(x,y,picture)
        self.__restorePrivateAttr(openAttr, brushAttr)

    # 画扇形
    def drawPie(self,x=0,y=0, w=100, h=50,startAngle:int=30,spanAngle:int=180,openAttr:dict = dict(), brushAttr:dict = dict()):
        startAngle *= 16
        spanAngle *= 16

        rect = QRect(x, y, w, h)

        self.__privateAttr(openAttr, brushAttr)

        self.painter().drawPie(rect, spanAngle, spanAngle)

        self.__restorePrivateAttr(openAttr, brushAttr)

    def drawPixmap(self, x=0, y=0, w=100, h=50,pixmap:QPixmap=None, openAttr: dict = dict(),brushAttr: dict = dict()):
        if pixmap is None:
            raise Exception("QPixmap cannot be None!")

        self.__privateAttr(openAttr, brushAttr)
        self.painter().drawPixmap(x, y,w,h,pixmap)
        self.__restorePrivateAttr(openAttr, brushAttr)

    # 画点
    def drawPoint(self,x=0, y=0, openAttr: dict = dict(),brushAttr: dict = dict()):
        self.__privateAttr(openAttr, brushAttr)
        self.painter().drawPoint(x, y)
        self.__restorePrivateAttr(openAttr, brushAttr)

    def drawPoints(self,points:list,openAttr:dict = dict(), brushAttr:dict = dict()):
        self.__privateAttr(openAttr, brushAttr)
        polygon = QPolygon()
        for i in points:
            polygon.append(i)
        self.painter().drawPoints(polygon)
        self.__restorePrivateAttr(openAttr, brushAttr)

    # 画多边形
    def drawPolygon(self,points:list,fillRule=Qt.OddEvenFill,openAttr:dict = dict(), brushAttr:dict = dict()):
        '''

        :param fillRule:
            Qt.OddEvenFill
            Qt.WindingFill
        :return:
        '''
        self.__privateAttr(openAttr, brushAttr)
        polygon = QPolygon()
        for i in points:
            polygon.append(i)
        self.painter().drawPolygon(polygon,fillRule=fillRule)

        self.__restorePrivateAttr(openAttr, brushAttr)

    def drawPolyline(self,points:list,openAttr:dict = dict(), brushAttr:dict = dict()):
        '''

        :param fillRule:
            Qt.OddEvenFill
            Qt.WindingFill
        :return:
        '''
        self.__privateAttr(openAttr, brushAttr)
        polygon = QPolygon()
        for i in points:
            polygon.append(i)
        self.painter().drawPolyline(polygon)

        self.__restorePrivateAttr(openAttr, brushAttr)

    # 擦除区域
    def eraseRect(self,x=0,y=0,w=50,h=50):
        self.painter().eraseRect(x,y,w,h)

    def fillPath(self,x,y,w,h,ppath:QPainterPath,color):
        '''

        :param ppath:
        :param color: QColor or QBrush
        :return:
        '''
        if ppath:
            self.painter().fillPath(ppath,color)
        else:
            self.painter().fillPath(x,y,w,h, color)

    # ------下面是自定义图像

    def drawRoundedRectText(self,x=0,y=0, w=100, h=50,r=2,text:str="hello wrold", openAttr:dict = dict(), brushAttr:dict = dict()):
        self.__privateAttr(openAttr,brushAttr)

        self.drawRoundedRect(x,y,w,h,r,openAttr=openAttr,brushAttr=brushAttr)
        self.drawText(x,y,w,h,text=text,openAttr=openAttr,brushAttr=brushAttr,flags=Qt.AlignCenter)

        self.__restorePrivateAttr(openAttr,brushAttr)

    # 绘制菱形
    def drawRhombus(self,x=0,y=0, w=100, h=50,openAttr:dict = dict(), brushAttr:dict = dict()):
        self.__privateAttr(openAttr, brushAttr)
        polys = QPolygonF([
            QPointF(x,y+h//2),QPointF(x+w//2,y),QPointF(x+w,y+h//2),QPointF(x+w//2,y+h)
        ])
        self.painterPath().addPolygon(polys)
        self.painterPath().closeSubpath()

        self.painter().drawPath(self.painterPath())

        self.__restorePrivateAttr(openAttr, brushAttr)

    # 绘制五角星
    def drawFiveStar(self,x=0,y=0, w=100, h=50,openAttr:dict = dict(), brushAttr:dict = dict()):
        self.__privateAttr(openAttr, brushAttr)

        a = 90
        print(x*math.cos(a)-y*math.sin(a))
        print((y+h//2)*math.sin(a)+y*math.cos(a))
        # polys = []
        # for i in range(5):
        #     sx = (x+w) * math.cos((2 * math.pi / 5) * i + math.pi / 2)
        #     sy = (y+h) * math.sin((2 * math.pi / 5) * i + math.pi / 2)
        #     # sx+=x
        #     # sy+=y
        #     polys.append(QPointF(sx,sy))
        # print(polys)
        # self.painterPath().addPolygon(QPolygonF(polys))

        self.__restorePrivateAttr(openAttr, brushAttr)


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600,600)
        self.setObjectName("win")

    def paintEvent(self, event:QPaintEvent) -> None:
        # -------
        painter = SuperPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        # painter.drawPolygon([QPoint(10,80),QPoint(20,10),QPoint(80,30),QPoint(90,70)],brushAttr={"c":QColor(0,25,45)})
        # op = QPen()
        # op.setColor(QColor(0,255,0))
        # painter.setPen(op)

        # bru = QBrush(QColor(0,0,33))
        # painter.setBrush(bru)

        # painter.drawRect(20,50,openAttr={"c":QColor(0,0,255)},
        #                  brushAttr={"c":QColor(0,255,0)},
        #                  shadowAttr={"color":QColor(234, 234, 234, 100),"r":10})
        #
        # painter.drawRoundedRect(100,300,150,150,r=10,openAttr={"color":QColor(33,123,200),"w":1},
        #                         brushAttr={"c":QColor(33,120,10)},
        #                         shadowAttr={"c":QColor(33,123,200,100),"r":30})
        #
        # painter.drawRect(100, 50, openAttr={"c": QColor(255, 0, 255)})
        #
        # painter.drawRoundedRectText(50,130,openAttr={"c":QColor(111,55,44),"w":3})
        #
        # painter.drawLine(10,110,h=90)

        # painter.drawRhombus(50,50,100,100,openAttr={"color":QColor(33,123,200),"w":3},brushAttr={"c":QColor(33,120,10)})
        painter.drawFiveStar(50,50,100,100)
        #
        painter.end()


'''
drawRect().hover()
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())