from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QPushButton
)
'''
    新无边框窗口主窗口
'''
from PyQtGuiLib.core.widgets2 import WidgetABC
from PyQtGuiLib.core.widgets2.titleBar import TitleBar
from PyQtGuiLib.core.widgets.statusBar import StatusBar
from PyQt5.sip import delete

class BorderlessMainWindow(WidgetABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.crbtn = QPushButton("创建",self)
        self.crbtn.move(40,40)
        self.crbtn.clicked.connect(self.createTitleBar)

        self.delbtn = QPushButton("删除",self)
        self.delbtn.move(100,100)
        self.delbtn.clicked.connect(self.removeTitleBar)

        self.__title_style = TitleBar.MacStyle

    def setTitleBtnStyle(self,style="mac"):
        if style.lower() == "win":
            self.__title_style = TitleBar.WinStyle
        else:
            self.__title_style = TitleBar.MacStyle

    # 返回标题风格
    def titleStyle(self) -> str:
        return self.__title_style

    # 创建标题栏
    def createTitleBar(self):
        if not hasattr(self,"titlebar"):
            print(self.get_backgroundColor().getRgb()) # 准备设计颜色变化
            self.titlebar = TitleBar(self)
            self.titlebar.setBtnStyle(self.titleStyle())
            self.titlebar.setStyleSheet('''
            TitleBar{
            qproperty-borderWidth:0;
            qproperty-backgroundColor: rgba(217, 217, 217,255);
            }
            ''')
            self.titlebar.show()

    # 返回标题对象
    def titleObj(self)->TitleBar:
        if hasattr(self, "titlebar"):
            return self.titlebar
        else:
            return None

    # 移除标题栏
    def removeTitleBar(self):
        if hasattr(self,"titlebar"):
            self.titlebar.deleteLater()
            delete(self.titlebar)
            del self.titlebar




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BorderlessMainWindow()
    win.setStyleSheet('''
qproperty-radius:7;
    ''')
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())