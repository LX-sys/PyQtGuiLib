from PyQtGuiLib.styles import SkinABC

class ButtonStyle(SkinABC):

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

