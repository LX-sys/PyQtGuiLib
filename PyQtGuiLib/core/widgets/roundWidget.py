from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    Qt,
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

        # 背景透明,去掉窗口边框,去掉边框
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.builtin_widget = '''
#widget{
background-color:gray;
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
        self.__widget.setObjectName(name)

    def setStyleSheet(self, styleSheet:str) -> None:
        self.__widget.setStyleSheet(styleSheet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RoundWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())