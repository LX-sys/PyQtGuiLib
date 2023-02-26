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
)


'''
    超级画师
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

    # 阴影
    def __shadowRect(self, x,y, w, h,r=10, imageCall=None, shadowAttr:dict = dict()):
        shadow_color = shadowAttr.get("color") or shadowAttr.get("c")  # 阴影颜色
        shadow_radius = shadowAttr.get("radius", 0) or shadowAttr.get("r", 0)
        shadow_x = shadowAttr.get("offx",0) or shadowAttr.get("x",0)
        shadow_y = shadowAttr.get("offy",0) or shadowAttr.get("y",0)

        if shadow_color:
            self.painter().setPen(qt.NoPen)
            self.painter().setBrush(QBrush(shadow_color, Qt.SolidPattern))
            # imageCall(x,y,w,h,r,r)
        if shadow_radius:
            for i in range(0, 20):  # 循环绘制多个圆形
                opacity = int(255 * pow(0.75, i))  # 计算当前圆形的 alpha 值
                shadow_color.setAlpha(opacity)  # 设置当前圆形的阴影颜色
                self.painter().setBrush(QBrush(shadow_color, Qt.SolidPattern))  # 设置当前圆形的画刷
                # print(x,shadow_x)
                # imageCall(x+shadow_x-i, y+shadow_y-i,80+i,80+i,r,r)
                print(x+shadow_x-i, y+shadow_y-i, w + i*2, h + i*2)
                # imageCall(x+shadow_x-i, y+shadow_y-i, w + i*2, h + i*2,r,r)  # 绘制当前圆形


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

    def drawRoundedRect(self,x=0,y=0, w=50, h=50,r=3, openAttr:dict = dict(), brushAttr:dict = dict(),shadowAttr:dict = dict()):

        rect = QRect(x, y, w, h)

        self.__shadowRect(x,y,w,h,imageCall=self.painter().drawRoundedRect,shadowAttr=shadowAttr)

        self.__privateAttr(openAttr, brushAttr)

        self.painter().drawRoundedRect(rect,r,r)

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

    # ------下面是自定义图像

    def drawRoundedRectText(self,x=0,y=0, w=100, h=50,r=2,text:str="hello wrold", openAttr:dict = dict(), brushAttr:dict = dict()):

        rect = QRect(x, y, w, h)
        self.__privateAttr(openAttr,brushAttr)

        self.drawRoundedRect(x,y,w,h,r,openAttr,brushAttr)
        self.drawText(x,y,w,h,text=text,openAttr=openAttr,brushAttr=brushAttr,flags=Qt.AlignCenter)

        self.__restorePrivateAttr(openAttr,brushAttr)


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600,600)
        self.setObjectName("win")
        # self.setStyleSheet('''
        # #win{
        # background-color: rgb(0, 0, 0);
        # }
        # ''')

        self.btn = QPushButton("",self)
        self.btn.setStyleSheet('''
        border:1px solid rgb(33,123,200);
        background-color: rgb(33,120,10);
        border-radius:10px;
        ''')
        self.btn.resize(80,80)
        self.btn.move(250,150)

        self.sh  = QGraphicsDropShadowEffect()
        self.sh.setOffset(100,0)
        self.sh.setColor(QColor(33,123,200))
        self.sh.setBlurRadius(25)

        self.btn.setGraphicsEffect(self.sh)

    def paintEvent(self, event:QPaintEvent) -> None:
        p = QPainter(self)
        # p.drawLine()
        # p.end()
        # -------
        painter = SuperPainter(self)
        # op = QPen()
        # op.setColor(QColor(0,255,0))
        # painter.setPen(op)

        # bru = QBrush(QColor(0,0,33))
        # painter.setBrush(bru)

        # painter.drawRect(20,50,openAttr={"c":QColor(0,0,255)},
        #                  brushAttr={"c":QColor(0,255,0)},
        #                  shadowAttr={"color":QColor(234, 234, 234, 100),"r":10})

        painter.drawRoundedRect(100,300,80,80,r=10,openAttr={"color":QColor(33,123,200),"w":1},
                                brushAttr={"c":QColor(33,120,10)},
                                shadowAttr={"c":QColor(33,123,200,100),"r":20,"x":100})

        # painter.drawRect(100, 50, openAttr={"c": QColor(255, 0, 255)})

        # painter.drawRoundedRectText(50,130,openAttr={"c":QColor(111,55,44),"w":3},)

        painter.drawLine(10,110,h=90)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())