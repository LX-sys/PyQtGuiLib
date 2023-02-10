from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QPushButton,
    QPoint,
    QMouseEvent,
    QWidget,
    QVBoxLayout
)
'''
    新无边框窗口主窗口,(还没有设计完成,暂时先放下 2023.1.31)
'''
from PyQtGuiLib.core.widgets import WidgetABC
from PyQtGuiLib.core.widgets.titleBar import TitleBar
from PyQtGuiLib.core.widgets.statusBar import StatusBar
# import ctypes
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class BorderlessMainWindow(WidgetABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


        self.crbtn = QPushButton("创建",self)
        self.crbtn.move(40,40)
        self.crbtn.clicked.connect(self.createTitleBar)

        self.delbtn = QPushButton("删除",self)
        self.delbtn.move(100,100)
        self.delbtn.clicked.connect(self.removeTitleBar)

        # 标题风格
        self.__title_style = TitleBar.MacStyle

        self.createTitleBar()

        # self.coreWin = WidgetABC(self)
        # self.coreWin.setStyleSheet('''
        #  WidgetABC{
        #  qproperty-backgroundColor:rgba(0, 255, 127,255);
        #  }
        #  ''')
        # self.setCentralWidget(self.coreWin)

        # self.status = StatusBar(self)
        # self.status.setStatusPos(StatusBar.PosBottom)
        # self.status.addText("我是标签")

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
            h,s,v,a = self.get_backgroundColor().getHsv()
            v = 0 if v - 30 < 0 else v-30

            self.titlebar = TitleBar(self)
            self.titlebar.setBtnStyle(self.titleStyle())
            self.titlebar.setStyleSheet('''
            TitleBar{
            qproperty-fontSize:14;
            qproperty-borderWidth:0;
            qproperty-borderColor:hsv(%d, %d, %d,%d);
            qproperty-backgroundColor: hsv(%d, %d, %d,%d);
            }
            '''%(h,s,v,a,h,s,v,a))
            self.titlebar.show()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if hasattr(self, "titlebar"):
            h, s, v, a = self.get_backgroundColor().getHsv()
            v = 0 if v - 30 < 0 else v - 30
            self.titlebar.setStyleSheet('''
                        TitleBar{
                        qproperty-fontSize:14;
                        qproperty-borderWidth:0;
                        qproperty-borderColor:hsv(%d, %d, %d,%d);
                        qproperty-backgroundColor: hsv(%d, %d, %d,%d);
                        }
                        ''' % (h, s, v, a, h, s, v, a))


    def setCentralWidget(self,widget:QWidget):
        if hasattr(self, "titlebar"):
            widget.resize(self.width()-4,self.height()-self.titlebar.height())
            widget.move(2,self.titlebar.height()-2)
        else:
            widget.resize(self.size())

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
            del self.titlebar



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BorderlessMainWindow()
    # win.setEnableGColor(True)
    win.setStyleSheet('''
qproperty-radius:7;
qproperty-backgroundColor:rgba(255, 170, 127,255);
    ''')
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())