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
    QSpinBox,
    QComboBox,
    QFileDialog,
    QFontComboBox,
)
from PyQtGuiLib.core import PaletteFrame
from PyQtGuiLib.styles import QssStyleAnalysis

# 通用 QGroupBox 大小(最多3排组件)
PUBLIC_GROUPBOX_SIZE = QSize(160,100)
PUBLIC_GROUPBOX_SIZE_4 = QSize(160,130)



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

# 创建通用 外框
def __getGroupBox(parent,title:str,size=None):
    groupBox = QGroupBox()
    parent.addWidget(groupBox)
    groupBox.setTitle(title)
    if size:
        groupBox.setFixedSize(size)
    else:
        groupBox.setFixedSize(PUBLIC_GROUPBOX_SIZE)
    return groupBox

# -------------------

# 通用的颜色组件
def colorComponent(self,parent):
    '''

    :param self: StyleLinker 对象
    :param parent: parent 窗口对象
    :param browser:  QTextBrowser 对象
    :return:
    '''

    def open_PaletteFrame(btn,case:str):

        if case in ["bg","c"]:
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

        if case == "image":
            # ;;images(*.png *.jpg *.jpeg *.bmp *.gif)
            name,ty=QFileDialog.getOpenFileName(self,"选择图片","","images(*.png *.jpg *.jpeg *.bmp *.gif)")
            if name:
                __updateAttr(self,"border-image","url(%s)"%name)

    groupBox =__getGroupBox(parent,"调色区")
    fboy = QFormLayout(groupBox)

    bgc = QLabel("背景颜色")
    bgc_btn = QPushButton()
    color = QLabel("前景色")
    color_btn = QPushButton()
    image_l = QLabel("背景图片(b)")
    image_btn = QPushButton("...")
    fboy.addRow(bgc,bgc_btn)
    fboy.addRow(color,color_btn)
    fboy.addRow(image_l,image_btn)

    # event
    bgc_btn.clicked.connect(lambda: open_PaletteFrame(bgc_btn,"bg"))
    color_btn.clicked.connect(lambda: open_PaletteFrame(color_btn,"c"))
    image_btn.clicked.connect(lambda :open_PaletteFrame(image_btn,"image"))


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

    groupBox = __getGroupBox(parent,"位置大小")
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
    def border_event(mode,v,color_btn=None):
        if mode == "border_radius":
            __updateAttr(self,"border-radius","{}px".format(v))
        if mode == "border_width":
            __updateAttr(self, "border-width", "{}px".format(v))
        if mode == "border_style":
            __updateAttr(self, "border-style", "%s"%v)
        if mode == "border_color":
            p = PaletteFrame()  # 创建颜色版
            p.show()

            def update(rgba, k, v):
                __updateAttr(self, k, v)
                color_btn.setStyleSheet('''background-color:rgba(%s, %s, %s,%s);''' % rgba)

            p.rgbaChange.connect(lambda rgba: update(rgba, "border-color", "rgba(%s, %s, %s,%s)" % rgba))

    groupBox = __getGroupBox(parent,"边设置",PUBLIC_GROUPBOX_SIZE_4)
    gboy = QGridLayout(groupBox)

    radius_l = QLabel("圆角")
    radius_spinbox = QSpinBox()
    width_l = QLabel("边框宽度")
    width_spinbox = QSpinBox()
    style_l = QLabel("边框风格")
    style_combox = QComboBox()
    style_combox.addItems(["none","solid","outset","inset",
                           "dashed","dot-dash","dot-dot-dash",
                           "dotted","double","groove","ridge"])
    color_l = QLabel("边框颜色")
    color_btn = QPushButton()

    gboy.addWidget(radius_l,0,0)
    gboy.addWidget(radius_spinbox,0,1)
    gboy.addWidget(width_l,1,0)
    gboy.addWidget(width_spinbox,1,1)
    gboy.addWidget(style_l,2,0)
    gboy.addWidget(style_combox,2,1)
    gboy.addWidget(color_l,3,0)
    gboy.addWidget(color_btn,3,1)

    radius_spinbox.valueChanged.connect(lambda v:border_event("border_radius",v))
    width_spinbox.valueChanged.connect(lambda v:border_event("border_width",v))
    style_combox.currentTextChanged.connect(lambda v:border_event("border_style",v))
    color_btn.clicked.connect(lambda :border_event("border_color",0,color_btn))

# 字体类组件
def fontComponent(self,parent):

    def font_event(mode,v):
        if mode == "font_size":
            __updateAttr(self,"font-size","{}px".format(v))
        if mode == "text_decoration":
            __updateAttr(self,"text-decoration", "%s"%v)
        if mode == "font_family":
            __updateAttr(self, "font-family", "\'%s\'" % v)
        if mode == "font_style":
            __updateAttr(self, "font-style", "%s" % v)

    groupBox = __getGroupBox(parent, "文字操作", PUBLIC_GROUPBOX_SIZE_4)
    gboy = QGridLayout(groupBox)

    size_l = QLabel("文字大小")
    size_spinbox = QSpinBox()
    size_spinbox.setValue(12)
    decoration_l = QLabel("文字装饰")
    decoration_combobox = QComboBox()
    decoration_combobox.addItems(["none","underline","line-through"])
    family_l = QLabel("字体")
    family_fcombobox = QFontComboBox()
    style_l = QLabel("文字风格")
    style_combobox = QComboBox()
    style_combobox.addItems(["none","italic","oblique"])

    gboy.addWidget(size_l,0,0)
    gboy.addWidget(size_spinbox,0,1)
    gboy.addWidget(decoration_l,1,0)
    gboy.addWidget(decoration_combobox,1,1)
    gboy.addWidget(family_l,2,0)
    gboy.addWidget(family_fcombobox,2,1)
    gboy.addWidget(style_l,3,0)
    gboy.addWidget(style_combobox,3,1)

    size_spinbox.valueChanged.connect(lambda v:font_event("font_size",v))
    decoration_combobox.currentTextChanged.connect(lambda v:font_event("text_decoration",v))
    family_fcombobox.currentTextChanged.connect(lambda v:font_event("font_family",v))
    family_fcombobox.textHighlighted.connect(lambda v:font_event("font_family",v))
    style_combobox.currentTextChanged.connect(lambda v:font_event("font_style",v))


# 小控件注册器
class RegisterComponent:
    __Reg_Funs = [colorComponent,
                  geometryComponent,
                  borderComponent,
                  fontComponent
                         ]

    # 返回注册项
    @staticmethod
    def getRegister():
        return RegisterComponent.__Reg_Funs