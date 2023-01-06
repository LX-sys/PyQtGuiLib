from random import randint,choice
'''

    皮肤 抽象类
'''

class SkinABC:

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

    # 返回所有边的样式
    @staticmethod
    def getAllBorderStyle()->list:
        return [SkinABC.BorderSolid,SkinABC.BordeOutset,SkinABC.BorderInset,SkinABC.BorderDashed,SkinABC.BorderDot_Dash,
                SkinABC.BorderDot_Dot_Dash,SkinABC.BorderDotted,SkinABC.BorderDouble,SkinABC.BorderGroove,SkinABC.BorderRidge,
                SkinABC.BorderNone]

    # 返回所有字体风格
    @staticmethod
    def getAllFontStyle() -> list:
        return [SkinABC.FontNormal,SkinABC.FontItalic,SkinABC.FontOblique]

    # 通用主样式
    @staticmethod
    def style(objectName:str=None,
              backgroundColor:str=None,
              color:str=None,
              radius:str=None,
              border_width:str=None,
              border_style:str=None,
              border_color:str=None,
              font_size:str="18px",
              font_style:str=None,
              font_family:str="Heiti SC",**kwargs) -> str:

        style_dict = {
            "background-color": backgroundColor,
            "color": color,
            "border-radius": radius,
            "border-width": border_width,
            "border-style": border_style,
            "border-color": border_color,
            "font-size": font_size,
            "font-style": font_style,
            "font-family": font_family
        }

        if kwargs:
            style_dict.update(kwargs)

        style_list = []
        for k, v in style_dict.items():
            style_list.append("{}:{};".format(k, v))

        if objectName is None:
            return "\n".join(style_list)
        else:
            style_str = "#" + objectName + "{\n"
            style_str += "\n".join(style_list)
            style_str += "\n}"
            return style_str

    # 伪状态 - 控件激活样式
    @staticmethod
    def active_() -> str:
        pass

    # 伪状态 - 控件聚焦样式  (多数用于带输入的地方)
    @staticmethod
    def focus_() -> str:
        pass

    # 伪状态 - 控件悬停样式
    @staticmethod
    def hover_() -> str:
        pass

    # 伪状态 - 控件按下时样式
    @staticmethod
    def pressed_() -> str:
        pass

    # 伪状态 - 控件只读时样式
    @staticmethod
    def readOnly_() -> str:
        ''' read-only '''
        pass

    # 伪状态 - 控件被选中时的样式 (多数用于 可以被选中的样式)
    @staticmethod
    def checked_():
        pass

    # 伪状态 - 控件未被选中时的样式 (多数用于 可以被选中的样式)
    @staticmethod
    def unchecked_():
        pass

    # 伪状态 - 控件状态不确定时的样式 (多数用于 可以被选中的样式)
    @staticmethod
    def indeterminate_():
        pass

    # 伪状态 - 控件收起(关闭)时的样式 (例如:QTreeView 子项收起时)
    @staticmethod
    def closed_() -> str:
        pass

    # 伪状态 - 控件展开时的样式 (例如:QTreeView 子项收起时)
    @staticmethod
    def open_() -> str:
        pass

    # 伪状态 - 控件可编辑时样式
    @staticmethod
    def editable_() -> str:
        pass

    # 伪状态 - 控件处于扁平时的样式  (当控件具有setFlat(True)时,才能生效)
    @staticmethod
    def flat_() -> str:
        pass

    # 随机样式
    @staticmethod
    def randomStyle(objectName:str=None,
              backgroundColor:str=None,
              color:str=None,
              radius:str=None,
              border_width:str=None,
              border_style:str=None,
              border_color:str=None,
              font_size:str="18px",
              font_style:str=None,
              font_family:str="Heiti SC",**kwargs):

        color_format = "rgba({},{},{},{})"
        style_dict = {
            "background-color": backgroundColor if backgroundColor else color_format.format(randint(0,256),randint(0,256),randint(0,256),randint(0,256)),
            "color": color if color else color_format.format(randint(0,256),randint(0,256),randint(0,256),randint(0,256)),
            "border-radius": radius if radius else "{}%".format(randint(1,31)),
            "border-width": border_width if border_width else "{}px".format(randint(0,3)),
            "border-style": border_style if border_style else choice(SkinABC.getAllBorderStyle()),
            "border-color": border_color if border_color else color_format.format(randint(0,256),randint(0,256),randint(0,256),randint(0,256)),
            "font-size": font_size if font_size else "px".format(10,20),
            "font-style": font_style if font_style else choice(SkinABC.getAllFontStyle()),
            "font-family": font_family
        }

        if kwargs:
            style_dict.update(kwargs)

        style_list = []
        for k, v in style_dict.items():
            style_list.append("{}:{};".format(k, v))

        if objectName is None:
            return "\n".join(style_list)
        else:
            style_str = "#" + objectName + "{\n"
            style_str += "\n".join(style_list)
            style_str += "\n}"
            return style_str

