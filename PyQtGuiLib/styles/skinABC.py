from abc import ABCMeta,abstractmethod

'''

    皮肤 抽象类
'''

class SkinABC(metaclass=ABCMeta):

    # 边的风格
    BorderSolid = "solid"
    BordeOutset = "outset"
    BorderInset = "inset"
    BorderDashed = "dashed"
    BorderDot_Dash = "dot-dash"
    BorderDot_Dot_Dash ="dot-dot-dash"
    BorderDotted = "dotted"
    BorderDouble = "double"
    BorderGroove = "groove"
    BorderRidge = "ridge"
    BorderNone = "none"

    # 字体风格
    FontItalic = "italic"
    FontOblique = "oblique"
    FontNormal = "normal"

    # 通用主样式
    @staticmethod
    @abstractmethod
    def style(objectName:str=None,
              backgroundColor:str=None,
              color:str=None,
              radius:str=None,
              border_width:str=None,
              border_style:str=None,
              border_color:str=None,
              font_size:str="18px",
              font_style:str=None,
              font_family:str="Heiti SC",**kwargs):
        pass

    @staticmethod
    @abstractmethod
    def randomStyle(**kwargs):
        pass
