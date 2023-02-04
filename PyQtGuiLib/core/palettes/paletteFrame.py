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
    qt
)

'''
    调色板框架
'''

from PyQtGuiLib.core.palettes.colorHsv import ColorHsv,ColorLump,ColorRect,ColorWheel


class PaletteFrame(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(480,340)


        # 占位窗口
        self.placeholderWidget = QWidget()
        self.placeholderWidget.setStyleSheet('''
background-color: rgb(19, 19, 19);
        ''')

        # 色块窗口
        # self.colorLumpWidget = None
        self.colorLumpWidget = ColorRect()
        # self.addColorLump(self.placeholderWidget)

        self.setStyleSheet('''
#leftWidget{
background-color: rgb(255, 255, 173);
}
#rightWidget{
background-color: rgb(164, 255, 185);
}
#lucency{
background-color: rgb(198, 217, 255);
}
        ''')
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
            QLabel("红(G)"),
            QLabel("红(B)"),
            QLabel("红(A)"),
            QLabel("十六"),
        ]
        self.lineedit_r, self.lineedit_g, self.lineedit_b, self.lineedit_a,self.lineedit_bin = [
            QSpinBox(),QSpinBox(),
            QSpinBox(),QSpinBox(),QLineEdit()
        ]
        for line in [self.lineedit_r,self.lineedit_g,self.lineedit_b,self.lineedit_a]:
            line.setMaximum(255)
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

    # 添加颜色块
    def addColorLump(self,wdiget:QWidget):
        wdiget.setParent(self)
        wdiget.move(0,0)

    # 事件
    def myEvent(self):
        self.slider.valueChanged.connect(lambda v:self.slider_event(v,"QSpinBox"))
        self.s_num.valueChanged.connect(lambda v:self.slider_event(v,"QSlider"))

    # 滚动条事件
    def slider_event(self,v:int,obj_str:str):
        if obj_str == "QSpinBox":
            self.s_num.setValue(v)

        if obj_str == "QSlider":
            self.slider.setValue(v)

    def resizeEvent(self, event) -> None:
        self.updateSize()
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PaletteFrame()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())