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


class GroupBoxABC:
    def __init__(self,styleLinker,parent):
        self.__title = ""
        self.__styleLinker = styleLinker
        self.__parent = parent

    def setTitle(self,title:str):
        self.__title = title

    def title(self)->str:
        return self.__title

    def styleLinker(self):
        return self.__styleLinker

    def parent(self):
        return self.__parent

    # 返回当前操作的选择器
    def selector(self):
        return self.styleLinker().global_var.selector(self.styleLinker().global_select)

    # 通用打开调色版
    def openPaletteFrame(self,title,callfun,argc=None):
        p = PaletteFrame()  # 创建颜色版
        p.setWindowTitle(title)
        p.show()

        if argc:
            p.rgbaChange.connect(lambda rgba:callfun(rgba,argc))
        else:
            p.rgbaChange.connect(lambda rgba: callfun(rgba))

    # 通用修改属性的方法
    def updateAttr_(self, key, value):
        '''

        :param self: StyleLinker 对象
        :param key: 样式属性
        :param value: 样式值
        :return:
        '''
        if self.styleLinker().global_select is None:
            head = self.styleLinker().global_var.header()[0]
        else:
            head = self.styleLinker().global_select
        self.styleLinker().global_var.selector(head).updateAttr(key, value)
        self.styleLinker().showStyleBrowserCode(self.styleLinker().global_var.toStr())

    # 创建通用 外框
    def getGroupBox_(self, size=None):
        groupBox = QGroupBox()
        self.parent().addGroupBox(groupBox)
        groupBox.setTitle(self.title())
        if size:
            groupBox.setFixedSize(size)
        else:
            groupBox.setFixedSize(PUBLIC_GROUPBOX_SIZE)
        return groupBox

    # 子类实现具体的功能
    def module(self):
        pass


# 通用的颜色组件
class ColorComponent(GroupBoxABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setTitle("调色区")

    def open_PaletteFrame(self,btn, case: str):
        if case in ["bg", "c"]:
            p = PaletteFrame()  # 创建颜色版
            p.show()

        def update(rgba, k, v):
            self.updateAttr_(k, v)
            btn.setStyleSheet('''background-color:rgba(%s, %s, %s,%s);''' % rgba)

        if case == "bg":
            p.setWindowTitle("背景色")
            p.rgbaChange.connect(lambda rgba: update(rgba, "background-color", "rgba(%s, %s, %s,%s)" % rgba))

        if case == "c":
            p.setWindowTitle("前景色")
            p.rgbaChange.connect(lambda rgba: update(rgba, "color", "rgba(%s, %s, %s,%s)" % rgba))

        if case == "image":
            # ;;images(*.png *.jpg *.jpeg *.bmp *.gif)
            name, ty = QFileDialog.getOpenFileName(self.parent(), "选择图片", "", "images(*.png *.jpg *.jpeg *.bmp *.gif)")
            if name:
                self.updateAttr_("border-image", "url(%s)" % name)
                btn.setStyleSheet("border:2px solid green;")

    def module(self):
        groupBox = self.getGroupBox_()
        fboy = QFormLayout(groupBox)
        fboy.setContentsMargins(3, 3, 3, 3)

        '''
            这里需要重新编写结构,增加一个清除图片
        '''

        bgc = QLabel("背景颜色")
        bgc_btn = QPushButton()
        color = QLabel("前景色")
        color_btn = QPushButton()
        image_l = QLabel("背景图片(b)")
        image_btn = QPushButton("...")
        fboy.addRow(bgc, bgc_btn)
        fboy.addRow(color, color_btn)
        fboy.addRow(image_l, image_btn)

        # event
        bgc_btn.clicked.connect(lambda: self.open_PaletteFrame(bgc_btn, "bg"))
        color_btn.clicked.connect(lambda: self.open_PaletteFrame(color_btn, "c"))
        image_btn.clicked.connect(lambda: self.open_PaletteFrame(image_btn, "image"))


# 通用调节大小位置组件
class GeometryComponent(GroupBoxABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setTitle("位置大小")

    def geometry_event(self,case, v):
        parent = self.styleLinker().global_var.parent()
        if case == "x":
            parent.move(v, parent.y())

        if case == "y":
            parent.move(parent.x(), v)

        if case == "w":
            parent.resize(v, parent.height())

        if case == "h":
            parent.resize(parent.width(), v)

    def module(self):
        groupBox = self.getGroupBox_()
        gboy = QGridLayout(groupBox)
        gboy.setContentsMargins(3, 3, 3, 3)

        xy_l = QLabel("位置")
        x_spinbox = QSpinBox()
        y_spinbox = QSpinBox()
        x_spinbox.setMaximum(600)
        y_spinbox.setMaximum(600)
        x_spinbox.setValue(self.styleLinker().global_var.parent().x())
        y_spinbox.setValue(self.styleLinker().global_var.parent().y())

        gboy.addWidget(xy_l, 0, 0)
        gboy.addWidget(x_spinbox, 0, 1)
        gboy.addWidget(y_spinbox, 0, 2)

        x_spinbox.valueChanged.connect(lambda v: self.geometry_event("x", v))
        y_spinbox.valueChanged.connect(lambda v: self.geometry_event("y", v))

        size_l = QLabel("大小")
        w_spinbox = QSpinBox()
        h_spinbox = QSpinBox()
        w_spinbox.setMaximum(600)
        h_spinbox.setMaximum(600)
        w_spinbox.setValue(self.styleLinker().global_var.parent().width())
        h_spinbox.setValue(self.styleLinker().global_var.parent().height())

        gboy.addWidget(size_l, 1, 0)
        gboy.addWidget(w_spinbox, 1, 1)
        gboy.addWidget(h_spinbox, 1, 2)

        w_spinbox.valueChanged.connect(lambda v: self.geometry_event("w", v))
        h_spinbox.valueChanged.connect(lambda v: self.geometry_event("h", v))


# 通用边组件
class BorderComponent(GroupBoxABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setTitle("边设置")

    def border_event(self,case,v,color_btn=None):
        if case == "border_radius":
            self.updateAttr_("border-radius","{}px".format(v))
        if case == "border_width":
            self.updateAttr_( "border-width", "{}px".format(v))
        if case == "border_style":
            self.updateAttr_("border-style", "%s"%v)
        if case == "border_color":
            p = PaletteFrame()  # 创建颜色版
            p.show()

            def update(rgba, k, v):
                self.updateAttr_(k, v)
                color_btn.setStyleSheet('''background-color:rgba(%s, %s, %s,%s);''' % rgba)

            p.rgbaChange.connect(lambda rgba: update(rgba, "border-color", "rgba(%s, %s, %s,%s)" % rgba))

    def module(self):
        groupBox = self.getGroupBox_(PUBLIC_GROUPBOX_SIZE_4)
        gboy = QGridLayout(groupBox)
        gboy.setContentsMargins(3, 3, 3, 3)

        radius_l = QLabel("圆角")
        radius_spinbox = QSpinBox()
        width_l = QLabel("边框宽度")
        width_spinbox = QSpinBox()
        style_l = QLabel("边框风格")
        style_combox = QComboBox()
        style_combox.addItems(["none", "solid", "outset", "inset",
                               "dashed", "dot-dash", "dot-dot-dash",
                               "dotted", "double", "groove", "ridge"])
        color_l = QLabel("边框颜色")
        color_btn = QPushButton()

        gboy.addWidget(radius_l, 0, 0)
        gboy.addWidget(radius_spinbox, 0, 1)
        gboy.addWidget(width_l, 1, 0)
        gboy.addWidget(width_spinbox, 1, 1)
        gboy.addWidget(style_l, 2, 0)
        gboy.addWidget(style_combox, 2, 1)
        gboy.addWidget(color_l, 3, 0)
        gboy.addWidget(color_btn, 3, 1)

        radius_spinbox.valueChanged.connect(lambda v: self.border_event("border_radius", v))
        width_spinbox.valueChanged.connect(lambda v: self.border_event("border_width", v))
        style_combox.currentTextChanged.connect(lambda v: self.border_event("border_style", v))
        style_combox.textHighlighted.connect(lambda v: self.border_event("border_style", v))
        color_btn.clicked.connect(lambda: self.border_event("border_color", 0, color_btn))


# 通用字体类组件
class FontComponent(GroupBoxABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setTitle("文字操作")

    def font_event(self,case,v):
        if case == "font_size":
            self.updateAttr_("font-size","{}px".format(v))
        if case == "text_decoration":
            self.updateAttr_("text-decoration", "%s"%v)
        if case == "font_family":
            self.updateAttr_("font-family", "\'%s\'" % v)
        if case == "font_style":
            self.updateAttr_("font-style", "%s" % v)

    def module(self):
        groupBox = self.getGroupBox_(PUBLIC_GROUPBOX_SIZE_4)
        gboy = QGridLayout(groupBox)
        gboy.setContentsMargins(3, 3, 3, 3)

        size_l = QLabel("文字大小")
        size_spinbox = QSpinBox()
        size_spinbox.setValue(12)
        decoration_l = QLabel("文字装饰")
        decoration_combobox = QComboBox()
        decoration_combobox.addItems(["none", "underline", "line-through"])
        family_l = QLabel("字体")
        family_fcombobox = QFontComboBox()
        style_l = QLabel("文字风格")
        style_combobox = QComboBox()
        style_combobox.addItems(["none", "italic", "oblique"])

        gboy.addWidget(size_l, 0, 0)
        gboy.addWidget(size_spinbox, 0, 1)
        gboy.addWidget(decoration_l, 1, 0)
        gboy.addWidget(decoration_combobox, 1, 1)
        gboy.addWidget(family_l, 2, 0)
        gboy.addWidget(family_fcombobox, 2, 1)
        gboy.addWidget(style_l, 3, 0)
        gboy.addWidget(style_combobox, 3, 1)

        size_spinbox.valueChanged.connect(lambda v: self.font_event("font_size", v))
        decoration_combobox.currentTextChanged.connect(lambda v: self.font_event("text_decoration", v))
        decoration_combobox.textHighlighted.connect(lambda v: self.font_event("text_decoration", v))
        family_fcombobox.currentTextChanged.connect(lambda v: self.font_event("font_family", v))
        family_fcombobox.textHighlighted.connect(lambda v: self.font_event("font_family", v))
        style_combobox.currentTextChanged.connect(lambda v: self.font_event("font_style", v))
        style_combobox.textHighlighted.connect(lambda v: self.font_event("font_style", v))


# 通用边细节组件
class BorderDetailComponent(GroupBoxABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setTitle("边细节")
        self._dir = None # 方向设置

    def setDir(self,dir,w_spinbox:QSpinBox,c_btn:QPushButton,s_combobox:QComboBox):
        if dir == "none":
            '''
                如果当 border-{}-width:0px;,那么这句话前面的 border-width:10px,
                将会永久失效,所有在选择方向为 none时,删除当前 border-{}-width 这个属性,来保障,
                border-width是有效的,并重置其他控件
            '''
            temp_dir = ["top","right","bottom","left"]
            temp_attr = ["width","color","style"]
            selector = self.selector()
            for d in temp_dir:
                for a in temp_attr:
                    key = "border-{}-{}".format(d,a)
                    if selector.isAttr(key):
                        self.selector().removeAttr(key)

            # 这里顺序不能反,必须先重置方向,防止触发事件
            self._dir = None
            w_spinbox.setValue(0)
            c_btn.setStyleSheet("")
            s_combobox.setCurrentIndex(0)
            return
        self._dir = dir

    def isDir(self)->bool:
        return bool(self._dir)

    def border_event(self,case,v,btn):
        if self.isDir() and case == "b_width":
            attr = "border-{}-width".format(self._dir)
            self.updateAttr_(attr,"%s"%v)

        if self.isDir() and case == "b_color":
            attr = "border-{}-color".format(self._dir)
            def call(rgba):
                btn.setStyleSheet("background-color:rgba(%s, %s, %s,%s);"%rgba)
                self.updateAttr_(attr,"rgba(%s, %s, %s,%s)"%rgba)
            self.openPaletteFrame("[{}]颜色".format(self._dir),call)

        if self.isDir() and case == "b_style":
            attr = "border-{}-style".format(self._dir)
            self.updateAttr_(attr,"%s"%v)

    def module(self):
        groupBox = self.getGroupBox_(PUBLIC_GROUPBOX_SIZE_4)
        fboy = QFormLayout(groupBox)
        fboy.setContentsMargins(3, 3, 3, 3)

        direction_l = QLabel("方向")
        direction_combobox = QComboBox()
        direction_combobox.addItems(["none","top","right","bottom","left"])
        width_l = QLabel("边宽")
        width_spinbox = QSpinBox()
        color_l = QLabel("边颜色")
        color_btn = QPushButton()
        style_l = QLabel("边风格")
        style_combobox = QComboBox()
        style_combobox.addItems(["none", "solid", "outset", "inset",
                               "dashed", "dot-dash", "dot-dot-dash",
                               "dotted", "double", "groove", "ridge"])

        fboy.addRow(direction_l, direction_combobox)
        fboy.addRow(width_l, width_spinbox)
        fboy.addRow(color_l, color_btn)
        fboy.addRow(style_l, style_combobox)

        direction_combobox.currentTextChanged.connect(lambda text:self.setDir(text,width_spinbox,color_btn,style_combobox))
        width_spinbox.valueChanged.connect(lambda v:self.border_event("b_width",v,None))
        color_btn.clicked.connect(lambda :self.border_event("b_color",None,color_btn))
        style_combobox.currentTextChanged.connect(lambda v:self.border_event("b_style",v,None))
        style_combobox.textHighlighted.connect(lambda v:self.border_event("b_style",v,None))

# ---------------------------------------------------

# -----------------------------------
# 小控件注册器
class RegisterComponent:
    '''
        __Reg_Funs: 是由程序自动加载的组件
        __Hand_Reg_Funs: 是由用户手动的使用右键来添加的组件

    '''
    __Reg_Funs =[
        ColorComponent,
        GeometryComponent,
        BorderComponent,
        FontComponent
    ]

    __Hand_Reg_Funs = [
        BorderDetailComponent
    ]


    # 返回注册项
    @staticmethod
    def getRegister():
        return RegisterComponent.__Reg_Funs

    # 返回手动注册项
    @staticmethod
    def getHandRegister():
        return RegisterComponent.__Hand_Reg_Funs