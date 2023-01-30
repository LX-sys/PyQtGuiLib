import platform,math
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    DesktopWidget,
    QPoint,
    QSize,
    QFontMetricsF,
    QFont,
)

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
def desktopCenter(parent) -> QPoint:
    if PYQT_VERSIONS == "PyQt5":
        center = DesktopWidget().availableGeometry().center()
        return QPoint(center.x()-parent.width()//2,center.y()-parent.height()//2)
    elif PYQT_VERSIONS in ["PyQt6","PySide2","PySide6"]:
        center = DesktopWidget.primaryScreen().availableGeometry().center()
        return QPoint(center.x()-parent.width()//2,center.y()-parent.height()//2)
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


# RGB 转 HSV
def rgbTohsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx,mn = max(r, g, b),min(r, g, b)
    df = mx-mn
    h=0
    if mx == mn:
        h = 0
    elif mx == r:h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:h = (60 * ((r-g)/df) + 240) % 360

    s = 0 if mx ==0 else df/mx
    # if mx == 0:
    #     s = 0
    # else:
    #     s = df/mx
    v = mx
    return h, s, v


# HSV 转 RGB
def hsvTorgb(h, s, v):
    h,s,v = float(h),float(s),float(v)

    h_60 = h / 60.0
    h_60f = math.floor(h_60)
    hi = int(h_60f) % 6
    f = h_60 - h_60f

    p,q,t = v * (1 - s),v * (1 - f * s),v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0

    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b