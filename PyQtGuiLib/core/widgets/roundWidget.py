from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QHBoxLayout
)
from PyQtGuiLib.core.widgets import BorderlessWidget



'''
    该窗口一定要通过qss样式,设置背景
    窗口的圆角也需要通过qss来实现,例如: border-radius:50px;
                                
'''
# 圆角窗口
class RoundWidget(BorderlessWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        self.__builtin_RoundWidget ='''
#RoundWidget{
background-color: rgba(0, 0, 0, 0);
}
        '''
        self.builtin_widget = '''
#widget{
background-color:#fff;
border-radius:50px;
}
        '''
        self.__builtin_style = ""

        self.__hlay = QHBoxLayout(self)
        self.__hlay.setContentsMargins(0,0,0,0)
        self.__hlay.setSpacing(0)

        self.__widget = QWidget()
        self.__hlay.addWidget(self.__widget)

        self.setObjectName("widget")
        self.setStyleSheet(self.builtin_widget)

    def setObjectName(self, name:str) -> None:
        '''
            RoundWidget 该名称为内置对象名称,不能被外部使用
        '''
        if name == "RoundWidget":
            raise NameError("The current name is already in use.")
        self.__widget.setObjectName(name)
        super().setObjectName("RoundWidget")

    def setStyleSheet(self, styleSheet:str) -> None:
        self.__widget.setStyleSheet(styleSheet)
        super().setStyleSheet(self.__builtin_RoundWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RoundWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())