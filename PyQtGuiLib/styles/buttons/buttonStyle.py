from PyQtGuiLib.styles import SkinABC

class ButtonStyle(SkinABC):

    def style(objectName: str = None, backgroundColor: str = None, color: str = None, radius: str = None,
              border_width: str = None, border_style: str = None, border_color: str = None, font_size: str = "18px",
              font_style: str = None, font_family: str = "Heiti SC", **kwargs):

        style_dict = {
            "background-color":backgroundColor,
            "color":color,
            "border-radius":radius,
            "border-width":border_width,
            "border-style":border_style,
            "border-color":border_color,
            "font-size":font_size,
            "font-style":font_style,
            "font-family":font_family
        }

        if kwargs:
            style_dict.update(kwargs)

        style_list = []
        for k, v in style_dict.items():
            style_list.append("{}:{};".format(k, v))

        if objectName is None:
            return "\n".join(style_list)
        else:
            style_str = "#"+objectName+"{\n"
            style_str += "\n".join(style_list)
            style_str+="\n}"
            return style_str

    # 偏平风格
    @staticmethod
    def flatStyle(objectName: str = None,**kwargs):
        return ButtonStyle.style(objectName,border_width="0px",backgroundColor="rgb(193, 191, 194)",
                                 color="rgb(254, 252, 255)",**kwargs)

    # 描边风格
    @staticmethod
    def outlineStyle(self,objectName: str = None,**kwargs):
        return ButtonStyle.style(objectName, border_width="1px",border_style=ButtonStyle.BorderSolid,
                                 border_color="rgb(50, 96, 239)",**kwargs)

    def randomStyle(**kwargs):
        pass


# print(ButtonStyle.outlineStyle(None))

