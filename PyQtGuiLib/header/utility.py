import platform
from PyQtGuiLib.header import PYQT_VERSIONS,DesktopWidget,QPoint,QSize,QFontMetricsF,QFont

is_win_sys = True if platform.system() == "win32" else False

is_mac_sys = True if platform.system() == "Darwin" else False


'''
    这几个与屏幕有关的方法,只能在窗口中调用,否则报错
'''

# 获取单个桌面大小
def desktopSize() -> QSize:
    if PYQT_VERSIONS == "PyQt5":
        from PyQt5.QtWidgets import QApplication
        size = QApplication.desktop().size()
        count = QApplication.desktop().screenCount()
        return QSize(size.width()//count,size.height())
    elif PYQT_VERSIONS in ["PyQt6","PySide2","PySide6"]:
        return DesktopWidget.primaryScreen().availableGeometry().size()
    else:
        return QSize(0,0)


# 桌面居中位置
def desktopCenter() -> QPoint:
    if PYQT_VERSIONS == "PyQt5":
        return DesktopWidget().availableGeometry().center()
    elif PYQT_VERSIONS in ["PyQt6","PySide2","PySide6"]:
        return DesktopWidget.primaryScreen().availableGeometry().center()
    else:
        return QPoint(0,0)


# 获取文字大小
def textSize(font:QFont,text:str)->QSize:
    fs = QFontMetricsF(font)
    if PYQT_VERSIONS == "PyQt5":
        return QSize(int(fs.width(text)),int(fs.height()))
    elif PYQT_VERSIONS in ["PyQt6","PySide2","PySide6"]:
        return QSize(int(fs.horizontalAdvance(text)+1), int(fs.height()+1)) # +1 是为了补偿丢失的像素
    else:
        return QSize(0,0)