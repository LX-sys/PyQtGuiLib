# -*- coding:utf-8 -*-
# @time:2023/2/209:09
# @author:LX
# @file:component.py
# @software:PyCharm
'''
    小组件
'''
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QGroupBox,
    QFormLayout,
    QPushButton,
    QSize,
    QLabel,
    QGridLayout,
    QSpinBox
)
from PyQtGuiLib.core import PaletteFrame
from PyQtGuiLib.styles import QssStyleAnalysis

# 通用 QGroupBox 大小
PUBLIC_GROUPBOX_SIZE = QSize(150,100)


# 颜色组件
# class GroupBox(QGroupBox):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)

# 通用修改属性的方法
def __updateAttr(self,key,value):
    '''

    :param self: StyleLinker 对象
    :param key: 样式属性
    :param value: 样式值
    :return:
    '''
    if self.global_select is None:
        head = self.global_var.header()[0]
    else:
        head = self.global_select
    self.global_var.selector(head).updateAttr(key,value)
    self.showStyleBrowserCode(self.global_var.toStr())


# 通用的颜色组件
def colorComponent(self,parent):
    '''

    :param self: StyleLinker 对象
    :param parent: parent 窗口对象
    :param browser:  QTextBrowser 对象
    :return:
    '''

    def open_PaletteFrame(btn,case:str):
        p = PaletteFrame()  # 创建颜色版
        p.show()

        def update(rgba,k,v):
            __updateAttr(self,k,v )
            btn.setStyleSheet('''background-color:rgba(%s, %s, %s,%s);''' % rgba)

        if case == "bg":
            p.setWindowTitle("背景色")
            p.rgbaChange.connect(lambda rgba:update(rgba,"background-color", "rgba(%s, %s, %s,%s)" % rgba))

        if case == "c":
            p.setWindowTitle("前景色")
            p.rgbaChange.connect(lambda rgba:update(rgba, "color", "rgba(%s, %s, %s,%s)" % rgba))

    groupBox = QGroupBox(parent)
    groupBox.setTitle("调色区")
    groupBox.resize(PUBLIC_GROUPBOX_SIZE)
    fboy = QFormLayout(groupBox)

    bgc = QLabel("背景颜色")
    bgc_btn = QPushButton()
    color = QLabel("前景色")
    color_btn = QPushButton()
    fboy.addRow(bgc,bgc_btn)
    fboy.addRow(color,color_btn)

    # event
    bgc_btn.clicked.connect(lambda: open_PaletteFrame(bgc_btn,"bg"))
    color_btn.clicked.connect(lambda: open_PaletteFrame(color_btn,"c"))


# 通用调节大小位置组件
def geometryComponent(self,parent):
    '''

    :param self: StyleLinker 对象
    :param parent: parent 窗口对象
    :param browser:  QTextBrowser 对象
    :return:
    '''
    def geometry_event(d,v):
        parent = self.global_var.parent()
        if d == "x":
            parent.move(v, parent.y())

        if d == "y":
            parent.move(parent.x(), v)

        if d == "w":
            parent.resize(v, parent.height())

        if d == "h":
            parent.resize(parent.width(), v)

    groupBox = QGroupBox(parent)
    groupBox.move(150,parent.y())
    groupBox.setTitle("位置大小")
    groupBox.resize(PUBLIC_GROUPBOX_SIZE)
    gboy = QGridLayout(groupBox)

    xy_l = QLabel("位置")
    x_spinbox = QSpinBox()
    y_spinbox = QSpinBox()
    x_spinbox.setMaximum(600)
    y_spinbox.setMaximum(600)
    x_spinbox.setValue(self.global_var.parent().x())
    y_spinbox.setValue(self.global_var.parent().y())

    gboy.addWidget(xy_l,0,0)
    gboy.addWidget(x_spinbox,0,1)
    gboy.addWidget(y_spinbox,0,2)

    x_spinbox.valueChanged.connect(lambda v:geometry_event("x",v))
    y_spinbox.valueChanged.connect(lambda v:geometry_event("y",v))

    size_l = QLabel("大小")
    w_spinbox = QSpinBox()
    h_spinbox = QSpinBox()
    w_spinbox.setMaximum(600)
    h_spinbox.setMaximum(600)
    w_spinbox.setValue(self.global_var.parent().width())
    h_spinbox.setValue(self.global_var.parent().height())

    gboy.addWidget(size_l, 1, 0)
    gboy.addWidget(w_spinbox, 1, 1)
    gboy.addWidget(h_spinbox, 1, 2)

    w_spinbox.valueChanged.connect(lambda v:geometry_event("w",v))
    h_spinbox.valueChanged.connect(lambda v:geometry_event("h",v))


# 通用边组件
def borderComponent(self,parent):
    '''

    :param self: StyleLinker 对象
    :param parent: parent 窗口对象
    :param browser:  QTextBrowser 对象
    :return:
    '''
    def border_event(mode,v):
        if mode == "radius":
            __updateAttr(self,"border-radius","{}px".format(v))

    groupBox = QGroupBox(parent)
    groupBox.move(300,parent.y())
    groupBox.setTitle("边设置")
    groupBox.resize(PUBLIC_GROUPBOX_SIZE)
    gboy = QGridLayout(groupBox)

    radius_l = QLabel("圆角")
    radius_spinbox = QSpinBox()

    gboy.addWidget(radius_l,0,0)
    gboy.addWidget(radius_spinbox,0,1)

    radius_spinbox.valueChanged.connect(lambda v:border_event("radius",v))


# 小控件注册器
class RegisterComponent:
    __Reg_Funs = [colorComponent,
                  geometryComponent,
                  borderComponent
                         ]

    # 返回注册项
    @staticmethod
    def getRegister():
        return RegisterComponent.__Reg_Funs