from PyQtGuiLib.header import (
    pyqtProperty,
    QColor
)

'''
    公共自定义样式
'''


class CustomStyle:
    def __init__(self):
        self._radius = 0
        self._backgroundColor = QColor(234, 234, 234)
        self._color = QColor(0,0,0)
        self._fontSize = 15
        self._fontStyle = "Heiti SC"
        self._font = "15, Heiti SC"
        self._borderWidth = 1
        self._borderStyle = "solid"
        self._borderColor = QColor(234,234,234)
        self._border = "1, solid, QColor(234,234,234)"

        # ----
        # 内边距
        self._margin = 2

    def __set_radius(self,r:int):
        print(r)
        self._radius = r

    def get_radius(self)->int:
        return self._radius

    def __set_backgroundColor(self,bgcolor:QColor):
        self._backgroundColor = QColor(*bgcolor.getRgb())

    def get_backgroundColor(self)->QColor:
        return self._backgroundColor

    def __set_color(self,color:QColor):
        self._color = color

    def get_color(self)->QColor:
        return self._color

    def __set_fontSize(self,size:int):
        self._fontSize = size

    def get_fontSize(self)->int:
        return self._fontSize

    def __set_fontStyle(self,style:str):
        self._fontStyle = style

    def get_fontStyle(self)->str:
        return self._fontStyle

    def __set_font(self,fontstr:str):
        size,style = fontstr.split(",")
        self.__set_fontSize(int(size))
        self.__set_fontStyle(style)

    def get_font(self)->str:
        return "{},{}".format(self.get_fontSize(),self.get_fontStyle())

    def __set_borderWidth(self,width:int):
        self._borderWidth = width

    def get_borderWidth(self)->int:
        return self._borderWidth

    def __set_borderStyle(self,style:str):
        self._borderStyle = style

    def get_borderStyle(self) -> str:
        return self._borderStyle

    def __set_borderColor(self,color:QColor):
        self._borderColor = color

    def get_borderColor(self)->QColor:
        return self._borderColor

    def __set_border(self,borderstr:str):
        width,style,color = borderstr.split(",")
        self.__set_borderWidth(int(width))
        self.__set_borderStyle(style)
        self.__set_borderColor(color)

    def get_border(self) -> str:
        return "{},{},{}".format(self.get_borderWidth(),self.get_borderStyle(),self.get_borderColor())

    def __set_margin(self,v:int):
        self._margin =v

    def get_margin(self)->int:
        return self._margin

    radius = pyqtProperty(int,fset=__set_radius,fget=get_radius)
    color = pyqtProperty(QColor, fset=__set_color, fget=get_color)
    backgroundColor = pyqtProperty(QColor, fset=__set_backgroundColor, fget=get_backgroundColor)
    fontSize = pyqtProperty(int, fset=__set_fontSize, fget=get_fontSize)
    fontStyle = pyqtProperty(str,fset=__set_fontStyle,fget=get_fontStyle)
    font = pyqtProperty(str,fset=__set_font,fget=get_font)
    borderWidth = pyqtProperty(int,fset=__set_borderWidth,fget=get_borderWidth)
    borderStyle = pyqtProperty(int,fset=__set_borderStyle,fget=get_borderStyle)
    borderColor = pyqtProperty(QColor, fset=__set_borderColor, fget=get_borderColor)
    border = pyqtProperty(str, fset=__set_border, fget=get_border)
    margin = pyqtProperty(int,fset=__set_margin,fget=get_margin)