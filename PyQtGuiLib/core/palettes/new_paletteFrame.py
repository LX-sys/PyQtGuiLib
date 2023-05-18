# -*- coding:utf-8 -*-
# @time:2023/5/1111:00
# @author:LX
# @file:new_paletteFrame.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    Qt,
    QSizePolicy,
    QSpacerItem,
    QLineEdit,
    QFrame,
    QSlider,
    QSpinBox,
    QFormLayout,
    QPixmap,
    qt,
    QPainter,
    QLinearGradient,
    QRadialGradient,
    QConicalGradient,
    QColor,
    QRect,
    Signal,
    QFont,
    QStackedWidget,
    QCursor,
    QTimer,
    desktopAllSize,
    QPoint,
    QMouseEvent,
    QMenu,
    QAction,
    QColorDialog,
    QPen,
    QResizeEvent
)

from random import randint

from PyQtGuiLib.styles.superPainter.superPainter import SuperPainter,VirtualObject


class ColorHsv(QFrame):
    rgbaChange = Signal(QColor)
    def __init__(self):
        super().__init__()
        self.resize(300,50)

        self.suppainter = SuperPainter()

    # 创建HSV颜色条
    def createHuePixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)  # 抗锯齿
        gradient = QLinearGradient(self.width(), 0, 0, 0)

        i = 0.0
        gradient.setColorAt(0, QColor.fromHsvF(0, 1, 1, 1))
        while i < 1.0:
            gradient.setColorAt(i, QColor.fromHsvF(i, 1, 1, 1))
            i += 1.0 / 16.0
        gradient.setColorAt(1, QColor.fromHsvF(0, 1, 1, 1))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(),0,0)

    def mouseMoveEvent(self, e) -> None:
        x = e.pos().x()
        cursor = self.suppainter.virtualObj("cursor")  # 获取虚拟对象
        y = cursor.getVirtualArgs()[1]
        w = cursor.getVirtualArgs()[2]
        if 0 <= x and x <= self.width() - w:
            cursor.move(x,y)
            self.update()
            color = self.pix.toImage().pixelColor(x, y)
            self.rgbaChange.emit(color)
        super().mouseMoveEvent(e)

    def resizeEvent(self, e) -> None:
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createHuePixmap()
        if self.suppainter.isVirtualObj("cursor"):
            height = e.size().height()
            cursor = self.suppainter.virtualObj("cursor")
            old_rect = list(cursor.getVirtualArgs())
            old_rect[-1] = height
            cursor.updateArgs(*old_rect)
        super().resizeEvent(e)

    def setColor(self, color:QColor):
        # 计算颜色在颜色条中的位置
        h, s, v, a = color.getHsv()
        x = h / 360 * self.width()
        y = self.suppainter.virtualObj("cursor").getVirtualArgs()[1]
        self.suppainter.virtualObj("cursor").move(x, y)
        self.update()

    def mousePressEvent(self, e) -> None:
        cursor = self.suppainter.virtualObj("cursor")  # 获取虚拟对象
        y = cursor.getVirtualArgs()[1]
        cursor.move(e.pos().x(), y)
        cursor.updateIndexToArgs(2,4)
        self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        cursor = self.suppainter.virtualObj("cursor")
        cursor.updateIndexToArgs(2, 1)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        # 创建出游标,并设置虚拟对象
        self.suppainter.drawPixmap(e.rect(),self.pix)
        self.suppainter.drawRect(0, 0, 1, self.height(), openAttr={"color": "white", "width": 1},
                                 virtualObjectName="cursor")

        self.suppainter.end()


class MaskWidget(QWidget):
    def __init__(self,timer):
        super().__init__()
        self.setWindowFlags(qt.FramelessWindowHint)
        self.setWindowOpacity(0.01)
        self.__timer = timer
        self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, e) -> None:
        self.__timer.stop()
        self.close()
        super().mousePressEvent(e)


# Color plate
class ColorBar(QFrame):
    rgbaChange = Signal(QColor)
    def __init__(self):
        super().__init__()
        self.__bgcolor = QColor(0, 255, 0, 255)

        self.is_half = False

        # 当前位置
        self.__cur_pos = (20,20)

        self.suppainter = SuperPainter()

    def setAlpha(self,a:int):
        self.__bgcolor.setAlpha(a)
        self.colorLayer()

    def setBgColor(self,color:QColor):
        self.__bgcolor = color
        self.colorLayer()

    def bgColor(self) -> QColor:
        return self.__bgcolor

    # 灰色图层
    def grayLayer(self):
        self.gray_pix = QPixmap(self.size())
        self.gray_pix.fill(qt.transparent)
        self.createGrayPixmap()

    # 彩色图层
    def colorLayer(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createPixmap()

    def createGrayPixmap(self):
        painter = QPainter(self.gray_pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor("#000"))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(),2,2)

    def createPixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#fff"))

        gradient.setColorAt(1, self.bgColor())

        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(),2,2)

    def __updateCursorPos(self,pos):
        cursor = self.suppainter.virtualObj("cursor")
        x, y = pos.x()-10, pos.y()-10
        self.__cur_pos = (x,y)
        cursor.move(x, y)
        pixmap = self.grab()
        color = pixmap.toImage().pixelColor(pos)
        self.rgbaChange.emit(color)
        if y >= self.height()//2:
            cursor.updateOpenAttr({"color":"white","w":2})
        else:
            cursor.updateOpenAttr({"color": "black", "w": 2})
        self.update()

    def mouseMoveEvent(self, e):
        self.__updateCursorPos(e.pos())
        super().mouseMoveEvent(e)

    def curColor(self)->QColor:
        return self.pix.toImage().pixelColor(*self.__cur_pos)

    def mousePressEvent(self, e):
        cursor = self.suppainter.virtualObj("cursor")
        cursor.updateIndexToArgs(2,20)
        cursor.updateIndexToArgs(3,20)
        cursor.updateIndexToArgs(4,10)
        cursor.updateIndexToArgs(5,10)
        self.__updateCursorPos(e.pos())
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        cursor = self.suppainter.virtualObj("cursor")
        cursor.updateIndexToArgs(2,10)
        cursor.updateIndexToArgs(3,10)
        cursor.updateIndexToArgs(4,5)
        cursor.updateIndexToArgs(5,5)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing)
        rect = e.rect()
        self.suppainter.drawPixmap(rect,self.pix)
        self.suppainter.drawPixmap(rect,self.gray_pix)
        self.suppainter.drawRoundedRect(20,20,10,10,5,5,openAttr={"color":"black","w":2},virtualObjectName="cursor")
        self.suppainter.end()

    def resizeEvent(self, e) -> None:
        self.grayLayer()
        self.colorLayer()
        super().resizeEvent(e)


# 颜色句柄
class Handle:
    def __init__(self,x,y,w,h,r=10,lh=8):
        '''

        :param x:
        :param y:
        :param w:
        :param h:
        :param r: 圆角半径
        :param lh: 游标线长
        '''
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.lh = lh

    def rect(self) -> QRect:
        return QRect(self.x,self.y,self.w,self.h)

    def getRect(self)->tuple:
        return self.x,self.y,self.w,self.h,

    def radius(self)->int:
        return self.r

    def lineH(self)->int:
        return self.lh


# 线性渐变板
class GradientWidget(QFrame):
    Handle_Linear = "linear"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setStyleSheet("border:1px solid yellow;")

        self.suppainter = SuperPainter()

        self.grab_type = "linear"
        self.grab_mode = ""

        self.colors = {
            "linear":[{
              "colorScope":0,
              "color":qt.red
            },
                {
                    "colorScope": 1,
                    "color": qt.blue
                }
            ]
        }

        self.linear = QLinearGradient(0,self.height()//2,self.width(),self.height()//2)

        self.createLinearPix()
        self.createHandle()

    def setGrabType(self,g_type:str):
        pass

    def setGrabMode(self,mode:str):
        pass

    def createLinearPix(self):
        if not hasattr(self,"linear_pix"):
            self.linear_pix = QPixmap(self.size())
        else:
            self.linear_pix = self.linear_pix.scaled(self.size())
        self.linear_pix.fill(qt.transparent)

        s = self.linear.start()
        e = self.linear.spread()

        # self.linear = QLinearGradient()
        # self.linear.setStart(s)
        # self.linear.setSpread(e)

        for c in self.colors["linear"]:
            self.linear.setColorAt(c["colorScope"],c["color"])

        if not hasattr("self", "linear_pix"):
            painter = QPainter(self.linear_pix)
            painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

            painter.setPen(qt.NoPen)
            painter.setBrush(self.linear)
            # painter.drawRoundedRect(self.rect(),5,5)
            painter.drawRect(self.rect())

    def createRadialPix(self):
        if not hasattr(self,"radia_pix"):
            self.radia_pix = QPixmap(self.size())
        else:
            self.radia_pix = self.pix.scaled(self.size())
        self.radia_pix.fill(qt.transparent)

    def createConicalPix(self):
        if not hasattr(self,"conical_pix"):
            self.conical_pix = QPixmap(self.size())
        else:
            self.conical_pix = self.pix.scaled(self.size())
        self.radia_pix.fill(qt.transparent)


    def createHandle(self):
        if self.grab_type == GradientWidget.Handle_Linear:
            self.handles =[
                {
                    "vobj": "linear_1",
                    "handle": Handle(5, 5, 16, 16, 8, 40),
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.red},
                },
                {
                    "vobj": "linear_2",
                    "handle": Handle(335, 5, 16, 16, 8, 40),
                    "openAttr": {"c": "#000", "w": 2},
                    "brushAttr": {"c": qt.blue},
                }
            ]
            self.cur_checked_hand = None

    def updateLinearPos(self,index,color_scope):
        self.colors["linear"][index]["colorScope"] =color_scope
        self.createLinearPix()
        self.update()

    def newLinearColor(self,colorScope,color):
        self.colors["linear"].append(
            {
                "colorScope": colorScope,
                "color": color
            }
        )
        self.createLinearPix()
        self.update()

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        if self.grab_type == GradientWidget.Handle_Linear and self.cur_checked_hand:
            hand = self.cur_checked_hand # type:VirtualObject
            x,y = e.x(),e.y()
            hand.move(x-8,y-8)
            if hand.virName() == "linear_1":
                self.linear.setStart(e.pos())
            elif hand.virName() == "linear_2":
                self.linear.setFinalStop(e.pos())
            self.createLinearPix()
            self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            if self.grab_type == GradientWidget.Handle_Linear:
                for hand in self.handles:
                    c_hand = self.suppainter.virtualObj(hand["vobj"])
                    if c_hand.isClick(e):
                        c_hand.updateOpenAttr({"c": "#fff", "w": 3})
                        self.update()
                        self.cur_checked_hand = c_hand
                        break
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        if self.grab_type == GradientWidget.Handle_Linear:
            for hand in self.handles:
                c_hand = self.suppainter.virtualObj(hand["vobj"])
                c_hand.updateOpenAttr({"c": "#000", "w": 2})
            self.update()
            self.cur_checked_hand = None
        super().mouseReleaseEvent(e)


    def paintEvent(self, e):
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)
        self.suppainter.drawPixmap(e.rect(),self.linear_pix)

        if self.grab_type == GradientWidget.Handle_Linear:
            for hand in self.handles:
                r = hand["handle"].radius()
                self.suppainter.drawRoundedRect(*hand["handle"].getRect(),
                                                r,r,
                                                openAttr=hand["openAttr"],
                                                brushAttr=hand["brushAttr"],
                                                virtualObjectName=hand["vobj"]
                                                )

        self.suppainter.end()

# -----------------------------


# 渐变通用操作台
class ColorOperation(QFrame):
    # clickCurSorColored = Signal(QColor)
    posed = Signal(int,float)
    newColored = Signal(float,QColor)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setFixedHeight(80)

        self.suppainter = SuperPainter()

        self.handles = [
            {
                "vobj":"handle_1",
                "handle":Handle(5,5,20,20,10,40),
                "openAttr":{"c":"#000","w":2},
                "brushAttr": {"c": qt.red},
                "colorScope":0,
                "color":qt.red
            },
            {
                "vobj": "handle_2",
                "handle": Handle(335,5,20,20,10,40),
                "openAttr": {"c": "#000", "w": 2},
                "brushAttr": {"c": qt.blue},
                "colorScope": 1,
                "color":qt.blue
            }
        ]

        # The id only increases and does not decrease, maintaining uniqueness
        self.max_handle_id = 2

        self.cursor_flag = ""
        self.updatePix()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_event)

    def menu_event(self):
        menu_ = QMenu(self)

        new_cursor = QAction("新建游标", self)
        del_cursor = QAction("删除游标", self)
        update_color = QAction("更新颜色",self)
        new_cursor.triggered.connect(self.createCursor_event)
        del_cursor.triggered.connect(self.delCursor_event)
        update_color.triggered.connect(self.updateCursorColor_event)
        menu_.addAction(new_cursor)
        menu_.addAction(del_cursor)
        menu_.addAction(update_color)

        menu_.popup(QCursor.pos())

    def createCursor_event(self):
        if not self._right_pressed_pos:
            return

        x = self._right_pressed_pos.x()
        self.max_handle_id+=1
        structure = {
            "vobj": "handle_{}".format(self.max_handle_id),
            "handle": Handle(x, 5, 20, 20, 10, 40),
            "openAttr": {"c": "#000", "w": 2},
        }
        col = QColorDialog.getColor()
        if col.isValid():
            structure["brushAttr"]={"c": col}
            structure["colorScope"] = 1/self.width()*x
            structure["color"]=col
            self.handles.append(structure)
            self.newColored.emit(1/self.width()*x,col)
            self.updatePix()
            self.update()
        self._right_pressed_pos = None

    def getHandle(self,vname:str):
        for info in self.handles:
            if info["vobj"] == vname:
                return info
        return None

    def delCursor_event(self):
        if not self._right_pressed_pos:
            return

        for vname in self.vObjs():
            cursor = self.suppainter.virtualObj(vname)
            if cursor.isClick(self._right_pressed_pos):
                self.handles.remove(self.getHandle(vname))
                break

        self.updatePix()
        self.update()
        self._right_pressed_pos = None

    def updateCursorColor_event(self):
        if not self._right_pressed_pos:
            return
        for vname in self.vObjs():
            cursor = self.suppainter.virtualObj(vname)
            if cursor.isClick(self._right_pressed_pos):
                col = QColorDialog.getColor()
                if col.isValid():
                    hand=self.getHandle(vname)
                    hand["brushAttr"]["c"] = col
                    hand["color"] = col
                    break

        self.updatePix()
        self.update()
        self._right_pressed_pos = None

    def vObjs(self)->list:
        return [vname["vobj"] for vname in self.handles]

    def updatePix(self):
        if not hasattr(self,"pix"):
            self.pix = QPixmap(self.size())
        else:
            self.pix = self.pix.scaled(self.size())
        self.pix.fill(qt.transparent)

        h2 = self.height()//2
        linear = QLinearGradient(0,h2,self.width(),h2)

        for cursor in self.handles:
            linear.setColorAt(cursor["colorScope"],cursor["color"])

        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)
        painter.setPen(qt.NoPen)
        painter.setBrush(linear)
        painter.drawRoundedRect(self.rect(),5,5)

    # 根据游标名称,更新colorScope
    def updateColorScope(self,cursor_name,v):
        for hand in self.handles:
            if hand["vobj"] == cursor_name:
                hand["colorScope"] = v
                break

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        if self.cursor_flag and e.buttons() == Qt.LeftButton:
            cursor = self.suppainter.virtualObj(self.cursor_flag)
            if e.x() + cursor.getWidth() // 2 >= cursor.getWidth() // 2 \
                    and e.x() <= self.width():
                cursor.updateIndexToArgs(0,e.x() - cursor.getWidth() // 2)
                self.updateColorScope(self.cursor_flag,1/self.width()*e.x())
                self.updatePix()
                # 发送 游标信息
                self.posed.emit(int(self.cursor_flag.split("_")[-1])-1,
                                1/self.width()*e.x())
            self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            for vname in self.vObjs():
                cursor = self.suppainter.virtualObj(vname)
                if cursor.isClick(e):
                    r,b,g,a =QColor(cursor.getVirtualBrushAttr()["c"]).getRgb()
                    reverse_color = QColor(255-r,255-b,255-g)
                    cursor.updateOpenAttr({"c": reverse_color, "w": 3})
                    cursor.updateIndexToArgs(5,50)
                    self.cursor_flag = vname
                    break
                else:
                    self.cursor_flag = ""
            self.update()
        elif e.buttons() == Qt.RightButton:
            self._right_pressed_pos = QPoint(e.pos().x(), e.pos().y())
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.cursor_flag = ""
        for vname in self.vObjs():
            cursor = self.suppainter.virtualObj(vname)
            cursor.updateOpenAttr({"c":"#000","w":2})
            cursor.updateIndexToArgs(5, 40)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

        self.suppainter.setPen(qt.NoPen)
        rect = QRect(0,self.height()-50,self.width(),self.height())
        self.suppainter.drawPixmap(rect,self.pix)

        # 绘制句柄
        for cursor in self.handles:
            handle_obj = cursor["handle"]
            self.suppainter.drawCursor(*handle_obj.getRect(),
                                       handle_obj.radius(),
                                       handle_obj.lineH(),
                                       openAttr=cursor["openAttr"],
                                       brushAttr = cursor["brushAttr"],
                                       virtualObjectName=cursor["vobj"]
                                       )
        self.suppainter.end()

    def resizeEvent(self, e:QResizeEvent) -> None:
        width = e.size().width()
        for hand in self.handles:
            if self.suppainter.isVirtualObj(hand["vobj"]):
                cursor = self.suppainter.virtualObj(hand["vobj"])
                new_pos = width * hand["colorScope"]
                if new_pos >= width:
                    new_pos -= 20
                cursor.updateIndexToArgs(0,new_pos)
        self.updatePix()
        super().resizeEvent(e)
# -------------------------------


# 调色对话框
class PaletteDialog(QWidget):
    clickColor = Signal(QColor)
    def __init__(self):
        super().__init__()
        self.setObjectName("widget")
        self.setWindowTitle("Palette")
        self.resize(500,400)

        # Pipette timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateColor)

        self.setUI()
        self.myEvent()

    def setUI(self):
        self.__lay = QVBoxLayout(self)

        self.__top_lay = QHBoxLayout()
        self.__top_lay.setSpacing(20)
        self.pure_color_btn = QPushButton()  # 纯色按钮
        self.line_btn = QPushButton() # 线性渐变按钮
        self.repeat_btn = QPushButton() # 径向渐变按钮
        self.reflect_btn = QPushButton() # 角度渐变按钮
        self.pure_color_btn.setObjectName("pure_color_btn")
        self.line_btn.setObjectName("line_btn")
        self.repeat_btn.setObjectName("repeat_btn")
        self.reflect_btn.setObjectName("reflect_btn")
        self.pure_color_btn.setToolTip("纯色")
        self.line_btn.setToolTip("线性渐变")
        self.repeat_btn.setToolTip("径向渐变")
        self.reflect_btn.setToolTip("角度渐变")

        self.__spacer = QSpacerItem(0,0,QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.demonstration_color_l = QLabel()

        self.demonstration_color_l.setFixedSize(24,24)
        self.color_straw_btn = QPushButton() # 吸管
        self.color_straw_btn.setObjectName("color_straw_btn")
        self.color_straw_btn.setText("吸")
        self.color_straw_btn.setFixedSize(24,24)
        self.hex_line = QLineEdit()
        self.hex_line.setFixedSize(100,24)
        self.hex_line.setText("#00ff00")

        for btn in [self.pure_color_btn,self.line_btn,self.repeat_btn,self.reflect_btn]:
            btn.setFixedSize(24,24)
            self.__top_lay.addWidget(btn,)

        self.__top_lay.addItem(self.__spacer)
        self.__top_lay.addWidget(self.demonstration_color_l)
        self.__top_lay.addWidget(self.color_straw_btn)
        self.__top_lay.addWidget(self.hex_line)

        # 中间层
        self.__middle_lay = QHBoxLayout()
        self.__middle_lay.setContentsMargins(0,0,0,0)
        self.__middle_lay.setSpacing(3)

        # ---

        # 纯色,线性渐变,径向渐变,角度渐变
        self.st = QStackedWidget()
        self.st_pure_color_wideget = QWidget()
        self.st_line_widget = QWidget()
        self.st_repeat_widget = QWidget()
        self.st_reflect_widget = QWidget()
        self.st.addWidget(self.st_pure_color_wideget)
        self.st.addWidget(self.st_line_widget)
        self.st.addWidget(self.st_repeat_widget)
        self.st.addWidget(self.st_reflect_widget)

        self.pureColorWidget()
        self.linearColorWidget()
        # -----


        self._m_r_widget = QWidget()
        self._m_r_lay = QVBoxLayout(self._m_r_widget)
        self._m_r_widget.setFixedWidth(100)

        self.label_r,self.label_g,self.label_b,self.label_a = [
            QLabel("红(R)"),
            QLabel("绿(G)"),
            QLabel("蓝(B)"),
            QLabel("透(A)"),
        ]
        self.lineedit_r, self.lineedit_g, self.lineedit_b, self.lineedit_a = [
            QLineEdit(),QLineEdit(),
            QLineEdit(),QLineEdit()
        ]
        for line in [self.lineedit_r,self.lineedit_g,self.lineedit_b,self.lineedit_a]:
            line.setText("255")
        self.lineedit_a.setText("255")
        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.label_r,self.lineedit_r)
        self.formLayout.addRow(self.label_g,self.lineedit_g)
        self.formLayout.addRow(self.label_b,self.lineedit_b)
        self.formLayout.addRow(self.label_a,self.lineedit_a)
        self.colorButton = QPushButton("获取颜色")
        self.colorButton.setFixedSize(90,30)
        self.colorButton.setObjectName("colorButton")
        self.formLayout.setWidget(self.formLayout.rowCount(),QFormLayout.SpanningRole,self.colorButton)

        self._m_r_lay.addLayout(self.formLayout)


        self.__middle_lay.addWidget(self._m_r_widget)

        self.__lay.addLayout(self.__top_lay)
        self.__lay.addLayout(self.__middle_lay)

        # 初始化演示色块
        self.setDemonstrationColor(self.color_bar.bgColor())
        self.setStyleSheet('''
#widget{
background-color:#0b4a2d;
}
#color_straw_btn{
font: 10pt "等线";
background-color: rgb(20, 134, 79);
color: rgb(232, 232, 232);
border:1px solid rgb(85, 170, 127);
border-radius:2px;
}
#color_straw_btn:pressed{
background-color:rgb(14, 95, 56)
}
#pure_color_btn,#line_btn,#repeat_btn,#reflect_btn{
border-radius:12px;
border:2px solid rgba(0,0,0,255);
}
#pure_color_btn:hover,#line_btn:hover,#repeat_btn:hover,#reflect_btn:hover{
border:3px solid rgba(0,0,0,255);
}
#pure_color_btn:pressed,#line_btn:pressed,#repeat_btn:pressed,#reflect_btn:pressed{
border:2px solid rgba(0,0,0,255);
}
#pure_color_btn{
background-color: rgb(255, 170, 0);
}
#line_btn{
background-color:qlineargradient(spread:pad,x1:0.002,y1:0.457,x2:0.957,y2:0.463,stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
#repeat_btn{
background-color:qradialgradient(spread:pad,cx:0.436,cy:0.483,radius:0.462,fx:0.47,fy:0.533,stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
#reflect_btn{
background-color:qconicalgradient(cx:0.448, cy:0.42, angle:120 stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
QLabel{
color: rgb(108, 210, 171);
font: 11pt "等线";
}
#colorButton{
border-radius:5px;
background-color: rgb(88, 142, 128);
color: rgb(255, 255, 255);
font: 11pt "等线";
}
QLineEdit{
border:none;
background-color: rgba(23, 154, 93,100);
color: rgb(209, 209, 209);
}
        ''')

    def updateColor(self):
        if hasattr(self, "maskWidget"):
            self.maskWidget.move(QCursor.pos()-QPoint(50,50))
        # straw
        pos = QCursor.pos()
        screen = QApplication.primaryScreen()
        if screen is not None:
            pixmap = screen.grabWindow(0, pos.x(), pos.y(), 1, 1)
            color = pixmap.toImage().pixelColor(0, 0)
            self.setDemonstrationColor(color)
            self.setLabelRGB(color)
            self.hex_line.setText(color.name())

    # 纯色面板
    def pureColorWidget(self):
        self.__m_v_lay = QVBoxLayout(self.st_pure_color_wideget)
        self.color_bar = ColorBar()
        self.hsv_widget = QWidget()
        self.hsv_widget.setFixedHeight(50)
        self.__hsv_lay = QVBoxLayout(self.hsv_widget)
        self.hsv = ColorHsv()
        self.hsv.setFixedHeight(15)
        self.splider = QSlider()
        self.splider.setMinimum(0)
        self.splider.setMaximum(255)
        self.splider.setValue(255)
        self.splider.setOrientation(Qt.Horizontal)
        self.__hsv_lay.addWidget(self.hsv)
        self.__hsv_lay.addWidget(self.splider)

        self.__m_v_lay.addWidget(self.color_bar)
        self.__m_v_lay.addWidget(self.hsv_widget)

        self.__middle_lay.addWidget(self.st)

    # 线性面板
    def linearColorWidget(self):
        self.__line_vlay = QVBoxLayout(self.st_line_widget)
        self.linear = GradientWidget()

        self.operation_color  = ColorOperation()
        self.operation_color.posed.connect(self.linear.updateLinearPos)
        self.operation_color.newColored.connect(self.linear.newLinearColor)

        self.__line_vlay.addWidget(self.linear)
        self.__line_vlay.addWidget(self.operation_color)

    def setLabelRGB(self,c:QColor):
        r,g,b,a = c.getRgb()
        self.lineedit_r.setText(str(r))
        self.lineedit_g.setText(str(g))
        self.lineedit_b.setText(str(b))

    def setDemonstrationColor(self,color:QColor):
        self.demonstration_color_l.setStyleSheet('''
        border-radius:3px;
        background-color:{};
        '''.format(color.name()))

    def __update_color_event(self,c):
        self.setLabelRGB(c)
        self.hex_line.setText(c.name())
        self.setDemonstrationColor(c)
        self.update()

    # 更新色块 rgb 事件
    def __update_rgb_event(self,c:QColor):
        self.color_bar.setBgColor(QColor(c))
        self.setLabelRGB(self.color_bar.curColor())
        self.setDemonstrationColor(self.color_bar.curColor())
        self.update()

    # 更新透明度
    def update_a_event(self,value:int):
        self.color_bar.setAlpha(value)
        self.lineedit_a.setText(str(value))
        self.setDemonstrationColor(self.color_bar.curColor())
        self.update()

    # emit
    def __emit_color_event(self):
        self.clickColor.emit(QColor(self.hex_line.text()))

    def straw_event(self):
        self.maskWidget = MaskWidget(self.timer)
        # size = desktopAllSize()
        # self.maskWidget.move(-size.width()//2,0)
        # self.maskWidget.resize(size)
        self.maskWidget.resize(100,100)
        self.maskWidget.show()
        self.timer.start(50)

    def myEvent(self):
        self.pure_color_btn.clicked.connect(lambda :self.st.setCurrentIndex(0))
        self.line_btn.clicked.connect(lambda :self.st.setCurrentIndex(1))
        self.repeat_btn.clicked.connect(lambda :self.st.setCurrentIndex(2))
        self.reflect_btn.clicked.connect(lambda :self.st.setCurrentIndex(3))

        self.hsv.rgbaChange.connect(self.__update_rgb_event)
        self.color_bar.rgbaChange.connect(self.__update_color_event)

        self.splider.valueChanged.connect(self.update_a_event)

        self.colorButton.clicked.connect(self.__emit_color_event)

        self.color_straw_btn.clicked.connect(self.straw_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PaletteDialog()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())