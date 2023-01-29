from PyQtGuiLib.header import (
    pyqtProperty,
    QColor,
    qt,
    Qt,
    QPoint,
    QRect
)
import re
import json
'''
    公共自定义样式
'''

def strRGBA_to_RGBA(rgba_str:str)->list:
    return [int(v) for v in re.findall(r"\d+",rgba_str)]


class CustomStyle:
    def __init__(self):
        self._radius = 0
        self._backgroundColor = QColor(234, 234, 234)
        self._color = QColor(0,0,0)
        self._fontSize = 15
        self._fontStyle = "Heiti SC"
        self._font = "15 'Heiti SC'"
        self._borderWidth = 1
        self._borderStyle = "solid"
        self._borderColor = QColor(234,234,234)
        self._border = "1 solid QColor(234,234,234)"

        # 线性渐变
        self._linearDirection = "LR"
        self._linearColor = "[(0.3, QColor(153, 153, 230, 60)), (1, QColor(98, 98, 147, 255))]"
        self._linear ="[0,0,0,0] [(0.3, QColor(153, 153, 230, 60)), (1, QColor(98, 98, 147, 255))]"

        # ----
        # 内边距
        self._margin = 5

    def __set_radius(self,r:int):
        self._radius = r

    def get_radius(self)->int:
        return self._radius

    def __set_backgroundColor(self,bgcolor:QColor):
        self._backgroundColor = QColor(*bgcolor.getRgb())

    def get_backgroundColor(self) -> QColor:
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
        size,style = fontstr.split(" ")
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

    def get_borderStyle(self) -> Qt.PenStyle:
        style_dict = {
            "dash": qt.DashLine,
            "dot": qt.DotLine,
            "dashdot": qt.DashDotLine,
            "solid": qt.SolidLine
        }
        if style_dict.get(self._borderStyle.lower(), None):
           return style_dict[self._borderStyle.lower()]
        else:
            return qt.SolidLine

    def __set_borderColor(self,color:QColor):
        if isinstance(color,str):
            self._borderColor = QColor(*strRGBA_to_RGBA(color))
        else:
            self._borderColor = color

    def get_borderColor(self)->QColor:
        return self._borderColor

    def __set_border(self,borderstr:str):
        width,style,color = borderstr.split(" ")
        self.__set_borderWidth(int(width))
        self.__set_borderStyle(style)
        self.__set_borderColor(color)

    def get_border(self) -> str:
        return "{},{},{}".format(self.get_borderWidth(),self.get_borderStyle(),self.get_borderColor())

    def __set_margin(self,v:int):
        self._margin = v

    def get_margin(self) -> int:
        return self._margin

    # 渐变
    def __set_linearDirection(self,direction:QRect):
        '''
            qproperty-linearDirection:LR
            qproperty-linearDirection:UD
            qproperty-linearDirection:[(0,0),(100,100)]
        :param direction:
        :return:
        '''
        self._linearDirection = direction

    def get_linearDirection(self) ->str:
        linearDirection_dict = {
            "LR":[0, self.height(),self.width(), self.height()],
            "UD":[self.width(), 0,self.width(), self.height()]
        }
        try:
            if linearDirection_dict.get(self._linearDirection,None):
                return json.dumps(linearDirection_dict[self._linearDirection])
            else:
                return self._linearDirection
        except Exception as e:
            print(e)
            return json.dumps(linearDirection_dict["LR"])

    def __set_linearColor(self,color_list_str:str):
        self._linearColor = color_list_str

    def get_linearColor(self) -> list:
        return self._linearColor

    radius = pyqtProperty(int,fset=__set_radius,fget=get_radius)
    color = pyqtProperty(QColor, fset=__set_color, fget=get_color)
    backgroundColor = pyqtProperty(QColor, fset=__set_backgroundColor, fget=get_backgroundColor)
    fontSize = pyqtProperty(int, fset=__set_fontSize, fget=get_fontSize)
    fontStyle = pyqtProperty(str,fset=__set_fontStyle,fget=get_fontStyle)
    font = pyqtProperty(str,fset=__set_font,fget=get_font)
    borderWidth = pyqtProperty(int,fset=__set_borderWidth,fget=get_borderWidth)
    borderStyle = pyqtProperty(str,fset=__set_borderStyle,fget=get_borderStyle)
    borderColor = pyqtProperty(QColor, fset=__set_borderColor, fget=get_borderColor)
    border = pyqtProperty(str, fset=__set_border, fget=get_border)
    margin = pyqtProperty(int,fset=__set_margin,fget=get_margin)
    # 线性渐变
    linearDirection = pyqtProperty(str,fset=__set_linearDirection,fget=get_linearDirection)
    linearColor = pyqtProperty(str,fset=__set_linearColor,fget=get_linearColor)
