from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    Signal,
    qt,
    QPaintEvent,
    QPainter,
    QColor,
    QPixmap,
    QLinearGradient,
    QMouseEvent,
    QSlider,
    QLabel,
    QSpinBox,
    QFormLayout,
    QLineEdit,
    QPushButton
)

'''
    调色版
'''

from PyQtGuiLib.core.palettes.colorHsv import ColorHsv


# 中间色块
class ColorLump(QWidget):
    rgbaChange = Signal(tuple)
    moveed = Signal(int,int,int,int) # 鼠标移动信信号

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # h 色调值  s  v
        self.tonal_value = 350
        self.s_value = 255
        self.v_value = 255
        # 图像位置
        self._pPos_x = 0
        self._pPos_y = 0

        # 移动圆圈的大小
        self._mouse_X = 0
        self._mouse_Y = 0
        self.ellipse_r = 8  # 半径
        self._mouse_color = qt.white  # 圆圈颜色

        # 透明度
        self._alpha = 255

        # 当前颜色值
        self._RGBA = [255, 255, 255, 255]
        # 颜色的十六进制
        self._colorHex = "#ffffff"

        self.pix2 = QPixmap(256, 256)
        self.pix2.fill(qt.transparent)

        # --
        self.preview()
        self.createSVPixmap()
        self.updatePreview()

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        # 下面这两句的位置不能换
        painter.drawPixmap(self._pPos_x, self._pPos_y, self.pix2)
        painter.drawPixmap(self._pPos_x, self._pPos_y, self.pix)

        painter.setPen(self._mouse_color)
        painter.drawEllipse(self._mouse_X + self._pPos_x, self._mouse_Y + self._pPos_y,
                            self.ellipse_r * 2, self.ellipse_r * 2)

    def preview(self):
        self.pix = QPixmap(256,256)
        self.pix.fill(qt.transparent)

        painter = QPainter(self.pix)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)

        gradient = QLinearGradient(0,0,0,360)
        gradient.setColorAt(0,QColor(0,0,0,0))
        gradient.setColorAt(1,QColor(0,0,0,255))

        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0,0,256,256)

    def _setSV(self, s: int, v: int) -> None:
        self.s_value = s
        self.v_value = v

        # hsv转成rgba

    def hsvToRgba(self, h: int, s: int, v: int) -> tuple:
        color = QColor()
        color.setHsv(h, s, v)
        # print(color.name())
        # 设置十六进制
        self._colorHex = color.name()
        self._setSV(s, v)
        self._RGBA = list(color.getRgb())
        self._RGBA[3] = self._alpha
        return tuple(self._RGBA)

    def _setMousePos(self, e: QMouseEvent):
        '''
            检查鼠标是否点击在图像上,并设置鼠标位置
        :param e:
        :return:
        '''
        if (e.x() >= -5 + self._pPos_x and
                e.x() <= self._pPos_x + 255 - self.ellipse_r * 2 and
                e.y() >= -5 + self._pPos_y and
                e.y() <= self._pPos_y + 255 - self.ellipse_r * 2
        ):
            self._mouse_X = e.x() - self._pPos_x
            self._mouse_Y = e.y() - self._pPos_y
            self.update()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._setMousePos(e)
        # print()
        rgba = self.hsvToRgba(self.tonal_value, e.x(), e.y())
        self._RGBA[0] = rgba[0]
        self._RGBA[1] = rgba[1]
        self._RGBA[2] = rgba[2]
        self._RGBA[3] = rgba[3]
        self.moveed.emit(*rgba)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        self._setMousePos(e)
        # 这里y需要减一个255,将颜色矫正,不然是反的
        x = e.pos().x() - self._pPos_x
        y = 255 - e.pos().y() + self._pPos_y
        if x >= 0 and x <= 255 and y >= 0 and y <= 255:
            rgba = self.hsvToRgba(self.tonal_value, x, y)
            self._RGBA[0]=rgba[0]
            self._RGBA[1]=rgba[1]
            self._RGBA[2]=rgba[2]
            self._RGBA[3]=rgba[3]
            self.moveed.emit(*rgba)
            self.update()

    def createSVPixmap(self):
        self.pix2 = QPixmap(256, 256)
        self.pix2.fill(qt.transparent)

    def updatePreview(self):
        color = QColor()
        color.setHsv(self.tonal_value, 255, 255, self._alpha)

        painter = QPainter(self.pix2)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(0, 0, 360, 0)
        gradient.setColorAt(1, color)
        gradient.setColorAt(0, QColor("#ffffff"))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, 256, 256)


class ColorPalette(QWidget):
    # 信号
    rgbaChange = Signal(tuple)
    colorNamed = Signal(str) # 只返回十六进制名称
    clicked = Signal(tuple,str) # 点击事件

    # 风格
    Style_Black = "black"
    Style_White = "white"
    Style_None = "none"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setFixedSize(255+120+2,300)
        self.setWindowTitle("调色版")

        # 风格
        self.styleMode = ColorPalette.Style_None
        self.setStyleMode(self.styleMode)

        self.Init()
        self.myEvent()

    def Init(self):
        # 左右布局
        self.rl_lay = QHBoxLayout(self)
        self.rl_lay.setContentsMargins(1,1,1,1)
        self.rl_lay.setSpacing(2)
        self.left_widget = QWidget()
        self.rigth_widget = QWidget()
        self.left_widget.setFixedWidth(255)
        self.rigth_widget.setFixedWidth(120)
        self.rl_lay.addWidget(self.left_widget)
        self.rl_lay.addWidget(self.rigth_widget)

        # 左布局
        self.tb_lay = QVBoxLayout(self.left_widget)
        self.tb_lay.setContentsMargins(1, 1, 1, 1)
        self.tb_lay.setSpacing(2)
        self.upper_widget = QWidget()
        self.color_lump = ColorLump()
        self.lower_widget = QWidget()
        self.chsv = ColorHsv(self.upper_widget)
        self.upper_widget.setFixedHeight(30)
        self.lower_widget.setFixedHeight(40)
        self.tb_lay.addWidget(self.upper_widget)
        self.tb_lay.addWidget(self.color_lump)
        self.tb_lay.addWidget(self.lower_widget)

        # 下面滑动条
        self.s_lay = QHBoxLayout(self.lower_widget)
        self.l_transparency_text = QLabel("不透明度")
        self.slider = QSlider()
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.setOrientation(qt.Horizontal)
        self.l_transparency = QLabel("100%")
        self.s_lay.addWidget(self.l_transparency_text)
        self.s_lay.addWidget(self.slider)
        self.s_lay.addWidget(self.l_transparency)

        # 右边布局
        self.f_lay = QFormLayout(self.rigth_widget)
        self.f_lay.setContentsMargins(1,5,3,1)
        self.red_label = QLabel("红(R)")
        self.green_label = QLabel("绿(G)")
        self.blue_label = QLabel("蓝(B)")
        self.a_label = QLabel("透(A)")
        self.er_label = QLabel("十六")
        self.red_sp = QSpinBox()
        self.green_sp = QSpinBox()
        self.blue_sp = QSpinBox()
        self.a_sp = QSpinBox()
        self.er_line = QLineEdit()
        # 获取颜色按钮
        self.colorBtn = QPushButton("获取颜色")
        self.colorBtn.setObjectName("colorBtn")
        self.colorBtn.setFixedHeight(30)

        self.red_sp.setMaximum(255)
        self.green_sp.setMaximum(255)
        self.blue_sp.setMaximum(255)
        self.a_sp.setMaximum(255)
        self.red_sp.setEnabled(False)
        self.green_sp.setEnabled(False)
        self.blue_sp.setEnabled(False)
        self.a_sp.setEnabled(False)

        self.f_lay.addRow(self.red_label,self.red_sp)
        self.f_lay.addRow(self.green_label, self.green_sp)
        self.f_lay.addRow(self.blue_label,self.blue_sp)
        self.f_lay.addRow(self.a_label, self.a_sp)
        self.f_lay.addRow(self.er_label,self.er_line)
        self.f_lay.setWidget(self.f_lay.rowCount(),QFormLayout.SpanningRole,self.colorBtn)

    def setStyleMode(self,mode:str):
        self.styleMode = mode
        self.updateStyle()

    # 更新风格
    def updateStyle(self):
        if self.styleMode == ColorPalette.Style_Black:
            self.setStyleSheet('''
            *{
            font: 11pt "黑体";
            background-color: rgb(0, 0, 0);
            color:rgb(255, 255, 255);
            }
            #colorBtn:hover{
            border:1px solid rgb(255, 255, 255);
            font-size:10pt;
            }
            #colorBtn,#colorBtn:pressed{
            border:2px solid rgb(255, 255, 255);
            font-size:11pt;
            }

                    ''')
        elif self.styleMode == ColorPalette.Style_White:
            self.setStyleSheet('''
            *{
            font: 11pt "黑体";
            background-color: rgb(255, 255, 255);
            color:rgb(0, 0, 0);
            }
            #colorBtn:hover{
            border:1px solid rgb(0, 0, 0);
            font-size:10pt;
            }
            #colorBtn,#colorBtn:pressed{
            border:2px solid rgb(0, 0, 0);
            font-size:11pt;
            }
                    ''')

    def myEvent(self):
        self.chsv.hsvChange.connect(self.hsv_event)
        self.slider.valueChanged.connect(self.slider_event)
        self.color_lump.moveed.connect(self.updateRGBSP)
        self.colorBtn.clicked.connect(lambda :self.clicked.emit(tuple(self.color_lump._RGBA),self.color_lump._colorHex))

    # 发送信号
    def sendSignl(self):
        self.rgbaChange.emit(tuple(self.color_lump._RGBA))
        self.colorNamed.emit(self.color_lump._colorHex)

    def updateRGBSP(self,r,g,b,a):
        self.red_sp.setValue(r)
        self.green_sp.setValue(g)
        self.blue_sp.setValue(b)
        self.a_sp.setValue(a)
        self.er_line.setText(self.color_lump._colorHex)
        # 发送信号
        self.sendSignl()

    def hsv_event(self,hsv):
        self.color_lump.tonal_value = hsv
        # 更新图像
        self.color_lump.updatePreview()
        temp = (self.color_lump.tonal_value, self.color_lump.s_value, self.color_lump.v_value)
        rgba = self.color_lump.hsvToRgba(*temp)
        self.updateRGBSP(*rgba)
        self.update()
        # 发送信号
        self.sendSignl()

    # 返回当前十六进制颜色
    def getHexName(self) -> str:
        return self.color_lump._colorHex

    # 返回当前RGBA颜色
    def getRGBA(self) -> tuple:
        return tuple(self.color_lump._RGBA.copy())

    # 滑块事件
    def slider_event(self,v):
        self.l_transparency.setText(str(v)+"%")
        self.color_lump._alpha = int(v // (100 / 255))
        self.a_sp.setValue(self.color_lump._alpha)
        self.color_lump._RGBA[3]=self.color_lump._alpha
        # 发送信号
        self.rgbaChange.emit(tuple(self.color_lump._RGBA))
        # 更新图像
        self.color_lump.updatePreview()
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ColorPalette()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())