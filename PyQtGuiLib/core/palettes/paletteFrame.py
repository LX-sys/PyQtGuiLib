from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QSlider,
    qt,
    Signal,
    QColor
)

'''
    调色板框架
'''

from PyQtGuiLib.core.palettes.colorHsv import ColorRect,ColorWheel


class PaletteFrame(QWidget):
    rgbaChange = Signal(tuple)
    # hsvChange = Signal(tuple)
    nameChange = Signal(str)
    clickColor = Signal(tuple)

    Rect = "ColorRect"
    Wheel = "ColorWheel"


    def __init__(self,*args,shape="ColorRect",**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(480,340)

        # 占位窗口
        self.placeholderWidget = QWidget()
        self.placeholderWidget.setStyleSheet('''
background-color: rgb(19, 19, 19);
        ''')

        # 色块窗口
        if shape == PaletteFrame.Wheel:
            self.colorLumpWidget = ColorWheel()
        else:
            self.colorLumpWidget = ColorRect()

        self.Init()
        self.myEvent()


    def Init(self):
        self.hboxLayout = QHBoxLayout(self)
        self.hboxLayout.setSpacing(2)
        self.hboxLayout.setContentsMargins(0,0,0,0)

        self.leftWidget = QWidget(self)
        self.rightWidget = QWidget(self)
        self.leftWidget.setObjectName("leftWidget")
        self.rightWidget.setObjectName("rightWidget")
        self.hboxLayout.addWidget(self.leftWidget)
        self.hboxLayout.addWidget(self.rightWidget)
        
        # ----
        self.vboxLayout = QVBoxLayout(self.leftWidget)
        self.vboxLayout.setSpacing(2)
        self.vboxLayout.setContentsMargins(0,0,0,0)

        self.lucency = QWidget()  # 设置透明滚动条的窗口
        self.lucency.setObjectName("lucency")
        if self.isColorLump():
            self.placeholderWidget = self.colorLumpWidget
        self.vboxLayout.addWidget(self.placeholderWidget)
        self.vboxLayout.addWidget(self.lucency)

        # --------------

        self.label_r,self.label_g,self.label_b,self.label_a,self.label_bin = [
            QLabel("红(R)"),
            QLabel("绿(G)"),
            QLabel("蓝(B)"),
            QLabel("透(A)"),
            QLabel("十六"),
        ]
        self.lineedit_r, self.lineedit_g, self.lineedit_b, self.lineedit_a,self.lineedit_bin = [
            QSpinBox(),QSpinBox(),
            QSpinBox(),QSpinBox(),QLineEdit()
        ]
        for line in [self.lineedit_r,self.lineedit_g,self.lineedit_b,self.lineedit_a]:
            line.setMaximum(255)
            line.setEnabled(False)
        self.lineedit_a.setValue(255)
        self.formLayout = QFormLayout(self.rightWidget)
        self.formLayout.addRow(self.label_r,self.lineedit_r)
        self.formLayout.addRow(self.label_g,self.lineedit_g)
        self.formLayout.addRow(self.label_b,self.lineedit_b)
        self.formLayout.addRow(self.label_a,self.lineedit_a)
        self.formLayout.addRow(self.label_bin,self.lineedit_bin)
        self.colorButton = QPushButton("获取颜色")
        self.formLayout.setWidget(self.formLayout.rowCount(),QFormLayout.SpanningRole,self.colorButton)

        # ----
        self.lucencyHLayout = QHBoxLayout(self.lucency)
        self.lucencyHLayout.setSpacing(1)
        self.t = QLabel("透明")
        self.slider = QSlider()
        self.slider.setMaximum(255)
        self.slider.setOrientation(qt.Horizontal)
        self.s_num = QSpinBox()
        self.s_num.setMaximum(255)
        self.slider.setValue(255)
        self.s_num.setValue(255)
        self.lucencyHLayout.addWidget(self.t)
        self.lucencyHLayout.addWidget(self.slider)
        self.lucencyHLayout.addWidget(self.s_num)

    def updateSize(self):
        r_w = 130
        l_w = self.width()-r_w
        self.leftWidget.setMaximumWidth(l_w)
        self.rightWidget.setMaximumWidth(r_w)

        d_h = 80
        u_h = self.height() - d_h
        self.placeholderWidget.setMaximumHeight(u_h)
        self.lucency.setMaximumHeight(d_h)

    def isColorLump(self)->bool:
        if self.colorLumpWidget:
            return True
        return False

    # 事件
    def myEvent(self):
        self.slider.valueChanged.connect(lambda v:self.slider_event(v,"QSpinBox"))
        self.s_num.valueChanged.connect(lambda v:self.slider_event(v,"QSlider"))
        #
        if self.isColorLump():
            self.placeholderWidget.rgbaChange.connect(self.spbox_event)
            self.placeholderWidget.nameChange.connect(self.lineedit_edit_event)
            self.colorButton.clicked.connect(self.click_color_event)

    # 点击获取颜色
    def click_color_event(self):
        self.clickColor.emit(self.getRGBA())

    def getRGBA(self)->tuple:
        r = self.lineedit_r.text()
        g = self.lineedit_g.text()
        b = self.lineedit_b.text()
        a = self.lineedit_a.text()
        rgba = r,g,b,a
        return rgba

    # 发送 十六进制 颜色
    def lineedit_edit_event(self,color_name):
        self.lineedit_bin.setText(color_name)
        self.nameChange.emit(color_name)

    # 元祖 转 QColor
    def tupleToQColor(self,arga:tuple):
        return QColor(*arga)

    # spbox事件
    def spbox_event(self,rgba):
        r,g,b,a = rgba
        self.lineedit_r.setValue(r)
        self.lineedit_g.setValue(g)
        self.lineedit_b.setValue(b)
        # 发送信号
        self.rgbaChange.emit(rgba)

    # 滚动条事件
    def slider_event(self,v:int,obj_str:str):
        if obj_str == "QSpinBox":
            self.s_num.setValue(v)

        if obj_str == "QSlider":
            self.slider.setValue(v)

        if self.isColorLump():
            self.placeholderWidget.setAlpha(v)
            self.lineedit_a.setValue(v)
            r = self.lineedit_r.text()
            g = self.lineedit_g.text()
            b = self.lineedit_b.text()
            rgba = r,g,b,v
            self.rgbaChange.emit(rgba)
            self.update()

    def resizeEvent(self, event) -> None:
        self.updateSize()
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PaletteFrame(shape=PaletteFrame.Rect)
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())