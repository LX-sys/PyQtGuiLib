# -*- coding:utf-8 -*-
# @time:2023/1/68:49
# @author: PyQt5学习爱好群 - 知行合一
# @file:comboCheckBox.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QWidget,
    QComboBox,
    QLineEdit,
    QListView,
    QCompleter,
    QStyledItemDelegate,
    QLabel,
    QGraphicsDropShadowEffect,
    QStandardItemModel,
    QStandardItem,
    QMouseEvent,
    QColor,
    QFont,
    qt,
    Signal,
    QKeyEvent
)

from typing import Union
from PyQtGuiLib.core.comboBox.comboCheckBox.py_style import PyStyle
from PyQtGuiLib.core.comboBox.comboCheckBox.py_message_box import Py_Message_box


def show_text(function):
    def wrapped(self, *args, **kwargs):
        # 避免异常增加行////////////////////////////////////////////////////
        if self.vars["additem"]:
            if self.vars["listViewModel"].rowCount() - self.vars["rowcount"] == 1:
                self.vars["listViewModel"].removeRows(self.vars["rowcount"], 1)
                self.vars["lineEdit"].setFocus()
                Py_Message_box(parent=self._parent,
                               obj_name='mesBox',
                               title='提示',
                               width=200,
                               height=200,
                               message_txt='确保输入框光标在闪烁！否则无法取值。',
                               type='information')
                # 避免异常增加行、、、、、、、、、、、、、、、、、、、、、、、、、、、、、、、、、、、、、

        if self.vars["showTextLock"]:
            self.vars["showTextLock"] = False

            result = function(self, *args, **kwargs)
            items = self.get_selected()
            l = len(items)
            l_ = self.vars["listViewModel"].rowCount() - 1
            self.vars["listViewModel"].item(0).setCheckState(
                qt.Checked if l == l_ else qt.Unchecked if l == 0 else qt.PartiallyChecked)
            # 自定义 修改选中颜色
            for i in range(1, self.vars["listViewModel"].rowCount()):
                if str(self.vars["listViewModel"].item(i).checkState()) == 'CheckState.Checked':
                    self.vars["listViewModel"].item(i).setBackground(QColor(77, 42, 0, 30))
                else:
                    self.vars["listViewModel"].item(i).setBackground(QColor(39, 44, 54))
            # 自定义 修改选中颜色
            self.vars["lineEdit"].setText(
                "全选" if l == l_ else "无选择" if l == 0 else "||".join((item.text() for item in items)))
            if self.vars["lineEdit"].text() != '全选':
                self.setStyleSheet(PyStyle.ComBoStyle1)
            else:
                self.setStyleSheet(PyStyle.ComBoStyle)

            # 自定义 智能输入框
            # items_txt = self.get_items_txt()
            self.completer = QCompleter(self.get_items_txt())

            self.completer.setFilterMode(qt.MatchContains)
            self.completer.setCompletionMode(qt.PopupCompletion)
            self.vars["lineEdit"].setCompleter(self.completer)
            self.vars["lineEdit"].setFocus()

            dd=QStyledItemDelegate()
            self.completer.popup().setItemDelegate(dd)
            self.completer.popup().setStyleSheet(
            '''
            QAbstractItemView{
                background-color:rgba(44, 50, 61, 1);
                color:rgba(219, 226, 241, 1);
                border:1px solid rgba(37, 41, 48, 1);
                font: 15pt;
            }
            QAbstractItemView::item:hover{
                background-color:rgba(77, 155, 213, 1);
            }
            '''
            )
            self.completer.activated.connect(lambda x:self.only_text(x))
            self.vars["lineEdit"].setFocus()
            # 自定义 智能输入框
            self.vars["showTextLock"] = True
        else:
            result = function(self, *args, **kwargs)
        return result
    return wrapped


class _ToolTip(QLabel):
    # TOOLTIP / LABEL StyleSheet
    style_tooltip = """ 
    QLabel {{		
        background-color: {_dark_one};	
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        border-right: 3px solid {_context_color};
        font: 800 9pt "Segoe UI";
    }}
    """
    def __init__(
        self,
        parent,
        tooltip,
        dark_one,
        context_color,
        text_foreground
    ):
        QLabel.__init__(self)

        # LABEL SETUP
        style = self.style_tooltip.format(
            _dark_one = dark_one,
            _context_color = context_color,
            _text_foreground = text_foreground
        )
        self.setObjectName(u"label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setOffset(0,0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)


class ComboCheckBox(QComboBox):
    linSignal = Signal(object)

    class MyListView(QListView):
        def __init__(self, parent: QWidget = None, vars=None):
            super().__init__(parent)
            self.vars = vars

        def mousePressEvent(self, event: QMouseEvent):
            self.vars["lock"] = False
            super().mousePressEvent(event)

        def mouseDoubleClickEvent(self, event: QMouseEvent):
            self.vars["lock"] = False
            super().mouseDoubleClickEvent(event)

    def __init__(self,
                 parent: QWidget = None,
                 obj_name=None,
                 width:int=200,
                 height:int=35,
                 spacing:int=0,
                 punc:str=',',
                 head_word:str='',
                 end_word:str='',
                 is_edit:bool=True,
                 is_read_only:bool=True,
                 is_fill_bg:bool=False,
                 is_frame:bool=True,
                 style:str=None,
                 rowcount:int=0,
                 items=None
                 ):
        super().__init__(parent)
        self._parent = parent
        self._objName = obj_name
        self._width = width
        self._heigh = height
        self._spacing = spacing
        self._punc = punc
        self._headWord = head_word
        self._endWord = end_word
        self._isEdit = is_edit
        self._isReadOnly = is_read_only
        self._isFillBg = is_fill_bg
        self._isFrame = is_frame
        self._isShow = False
        self._style = style
        self._items=items

        self.vars = {
            "lock":True,
            "additem":False,
            "showTextLock":True,
            "lineEdit":QLineEdit(self),
            "listViewModel":QStandardItemModel(self),
            "rowcount":rowcount+1
        }
        self.vars["listView"] = self.MyListView(self, self.vars)
        self.vars["lineEdit"].setReadOnly(False)
        self.setModel(self.vars["listViewModel"])
        self.setView(self.vars["listView"])
        self.setLineEdit(self.vars["lineEdit"])

        self.add_item("全选")
        self.activated.connect(self.__show_selected)

        self.add_items(self._items)

        # 设置父窗口
        if self._parent is not None:
            self.setParent(self._parent)
        # 设置名称
        if self._objName is not None:
            self.setObjectName(self._objName)
        # 设置按钮的尺寸范围
        if self._width is None:
            if self._heigh is None:
                pass
            else:
                self.setMinimumHeight(self._heigh)
                self.setMaximumHeight(self._heigh)
        else:
            if self._heigh is None:
                self.setMinimumWidth(self._width)
                self.setMaximumWidth(self._width)
            else:
                self.setFixedSize(self._width, self._heigh)
        # 设置背景填充
        self.setAutoFillBackground(self._isFillBg)
        # 设置边框
        self.setFrame(self._isFrame)
        # 设置下拉框的显示对象，防止combo的设置影响qss样式
        # self.setView(QListView())
        # 设置显示框编辑状态
        if self._isEdit is not None:
            self.setEditable(self._isEdit)
        self.set_styleSheet(self._style)
        self.setMaxVisibleItems(30)

        self.__personalInformation = {
            "author": "PyQt5学习爱好群-知行合一",
            "contribution time": "2023.4.25"
        }

    def author(self) -> str:
        return self.__personalInformation

    def set_styleSheet(self, style:str=None):
        """设置样式"""
        if style is not None:
            self.setStyleSheet(style)
        else:
            self.setStyleSheet(PyStyle.ComBoStyle)

    def count(self) -> int:
        # 返回子项数
        return super().count() - 1

    @show_text
    def add_item(self, text,tooltip=None):
        #
        item = QStandardItem()
        item.setText(text)
        item.setCheckable(True)

        if tooltip is None:
            tooltip = text
        item.setToolTip(tooltip)
        font = QFont("黑体")
        item.setFont(font)
        item.setCheckState(qt.Checked)
        self.vars["listViewModel"].appendRow(item)

    @show_text
    def add_items(self, texts: Union[list,tuple]):
        self.vars["rowcount"] = len(texts) + 1
        # 根据文本列表添加子项
        for text in texts:
            self.add_item(text)
        self.vars["additem"] = True

    @show_text
    def add_item_data(self, name:str,crew_number:str,part_rate:str,namesake_rate:str,class_rate:str,code:str,system:str):
        item = QStandardItem()
        item.setText(name)
        item.setCheckable(True)

        # part_rate='60%'
        # chezuh='''{2010-{'06', '02', '03', '01', '07', '04', '00'}", "2023-{'01'}", "2009-{'06', '02', '03', '01', '07', '04', '00'}", "0208-{'06', '02', '03', '01', '07', '04', '00'}", "2007-{'06', '02', '03', '01', '07', '04', '00'}", "2181-{'03', '07'}", "2187-{'06', '02', '03', '01', '07', '04'}", "2008-{'06', '02', '04'}", "2030-{'01', '07', '04'}", "2143-{'04'}", "2012-{'06', '02', '03', '01', '07', '00'}", "2058-{'02'}", "2048-{'03', '06', '01'}", "2016-{'01'}", "2047-{'00'}", "2015-{'03', '07'}'''
        item.setToolTip("<h2>故障名称：<font color=#AAAAAA;size:10px>"+name+"</font></h2>"
                        "<h2>代码：<font color=#AAAAAA;size:18px>"+code+"</font> -----系统：<font color=#AAAAAA;size:18px>"+system+"</font></h2>"
                        "<h2>更换配件率：<font color=#AAAAAA;size:18px>"+part_rate+"</font></h2>"
                        "<h2>同名属实率：<font color=#AAAAAA;size:10px>"+namesake_rate+"</font></h2>"
                        "<h2>类名属实率：<font color=#AAAAAA;size:10px>"+class_rate+"</font></h2>"
                        "<h2>故障车组号：<font color=#AA0000;font-size:10px>"+crew_number+"</font></h2>")

        # item.setBackground(QColor(200, 200, 200))
        font = QFont("黑体")
        item.setFont(font)
        item.setCheckState(qt.Checked)
        self.vars["listViewModel"].appendRow(item)

    @show_text
    def add_items_data(self, data):
        self.vars["rowcount"] = len(data) + 1
        # 根据文本列表添加子项
        for row in data.itertuples():
            sanlv=row[3].split("||")
            part_rate=sanlv[0]   #换件
            namesake_rate=sanlv[1] #属实
            class_rate=sanlv[2] #类名
            code=row[1]
            name=row[2]
            crew_number=row[4]
            system=row[5]
            self.add_item_data(name,crew_number,part_rate,namesake_rate,class_rate,code,system)
        self.vars["additem"] = True

    @show_text
    def clear_items(self):
        # 清空所有子项
        self.vars["listViewModel"].clear()
        self.add_item("全选")

    def find_index(self, index: int):
        # 根据索引查找子项
        return self.vars["listViewModel"].item(index if index < 0 else index + 1)

    def find_indexs(self, indexs:Union[list,tuple]):
        # 根据索引列表查找子项
        return [self.find_index(index) for index in indexs]

    def find_text(self, text: str):
        # 根据文本查找子项
        tempList = self.vars["listViewModel"].findItems(text)
        tempList.pop(0) if tempList and tempList[0].row() == 0 else tempList
        return tempList

    def find_texts(self, texts: Union[list,tuple]):
        # 根据文本列表查找子项
        return {text: self.find_text(text) for text in texts}

    def in_text(self, text: str):
        # 根据文本查找子项
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            if text in item.text():
                # print(text,item.text())
                self.select_text(item.text(),True)
            else:
                self.select_del(item)

    def only_text(self, text: str):
        # 根据文本查找子项
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            if text in item.text():
                self.select_text(item.text(),True)
            else:
                self.select_del(item)
        self.linSignal.emit(self)

    @show_text
    def only_texts(self,textlist):
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            if item.text() in textlist:
                item.setCheckState(qt.Checked)
            else:item.setCheckState(qt.Unchecked)

    def get_text(self, index:int):
        # 根据索引返回文本
        return self.vars["listViewModel"].item(index if index < 0 else index + 1).text()

    def get_texts(self, indexs: Union[list,tuple]):
        # 根据索引列表返回文本
        return [self.get_text(index) for index in indexs]

    def change_text(self, index: int, text: str):
        # 根据索引改变某一子项的文本
        self.vars["listViewModel"].item(index if index < 0 else index + 1).setText(text)

    @show_text
    def select_index(self, index: int, state: bool = True):
        # 根据索引选中子项，state=False时为取消选中
        self.vars["listViewModel"].item(index if index < 0 else index + 1).setCheckState(
            qt.Checked if state else qt.Unchecked)

    @show_text
    def select_indexs(self, indexs: Union[list,tuple], state: bool = True):
        # 根据索引列表选中子项，state=False时为取消选中
        for index in indexs:
            self.select_index(index, state)

    @show_text
    def select_text(self, text: str, state: bool = True):
        # 根据文本选中子项，state=False时为取消选中
        for item in self.find_text(text):
            item.setCheckState(qt.Checked if state else qt.Unchecked)

    @show_text
    def select_texts(self, texts: Union[list,tuple], state: bool = True):
        # 根据文本列表选中子项，state=False时为取消选中
        for text in texts:
            self.select_text(text, state)

    @show_text
    def select_reverse(self):
        # 反转选择
        if self.vars["listViewModel"].item(0).checkState() == qt.Unchecked:
            self.select_all()
        elif self.vars["listViewModel"].item(0).checkState() == qt.Checked:
            self.select_clear()
        else:
            for row in range(1, self.vars["listViewModel"].rowCount()):
                self.__select_reverse(row)

    def __select_reverse(self, row: int):
        item = self.vars["listViewModel"].item(row)
        item.setCheckState(qt.Unchecked if item.checkState() == qt.Checked else qt.Checked)

    @show_text
    def deselected(self, text):
        #去除选择单个
        if text:
            ele_list = self.find_text(text)
            for ele in ele_list:
              ele.setCheckState(qt.Unchecked)

    @show_text
    def select_all(self):
        # 全选
        for row in range(0, self.vars["listViewModel"].rowCount()):
            self.vars["listViewModel"].item(row).setCheckState(qt.Checked)

    @show_text
    def select_clear(self):
        # 全不选
        for row in range(0, self.vars["listViewModel"].rowCount()):
            self.vars["listViewModel"].item(row).setCheckState(qt.Unchecked)
    @show_text
    def select_del(self,item:object):
        # 不选
        item.setCheckState(qt.Unchecked)

    @show_text
    def remove_index(self, index: int):
        # 根据索引移除子项
        return self.vars["listViewModel"].takeRow(index if index < 0 else index + 1)

    @show_text
    def remove_indexs(self, indexs:Union[list,tuple]):
        # 根据索引列表移除子项
        return [self.remove_index(index) for index in sorted(indexs, reverse=True)]

    @show_text
    def remove_text(self, text: str):
        # 根据文本移除子项
        items = self.find_text(text)
        indexs = [item.row() for item in items]
        return [self.vars["listViewModel"].takeRow(index) for index in sorted(indexs, reverse=True)]

    @show_text
    def remove_texts(self, texts:Union[list,tuple]):
        # 根据文本列表移除子项
        return {text: self.remove_text(text) for text in texts}

    def get_selected(self):
        # 获取当前选择的子项
        items = list()
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            if item.checkState() == qt.Checked:
                items.append(item)
        return items

    def get_selected_txt(self):
        # 获取当前选择的子项
        items = list()
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            if item.checkState() == qt.Checked:
                items.append(item.text())
        return items

    def get_items_txt(self):
        # 获取当前选择的子项
        items = list()
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            items.append(item.text())
        return items

    def get_items(self):
        # 获取当前选择的子项
        items = list()
        for row in range(1, self.vars["listViewModel"].rowCount()):
            item = self.vars["listViewModel"].item(row)
            items.append(item)
        return items

    def is_all(self):
        # 判断是否是全选
        return True if self.vars["listViewModel"].item(0).checkState() == qt.Checked else False

    def sort(self, order=qt.AscendingOrder):
        # 排序，默认正序
        self.vars["listViewModel"].sort(0, order)

    @show_text
    def __show_selected(self, index):
        if not self.vars["lock"]:
            if index == 0:
                if self.vars["listViewModel"].item(0).checkState() == qt.Checked:
                    self.select_clear()
                else:
                    self.select_all()
            else:
                self.__select_reverse(index)

            self.vars["lock"] = True

    def hidePopup(self):
        if self.vars["lock"]:
            self.linSignal.emit(self)
            super().hidePopup()

    def keyPressEvent(self, event:QKeyEvent):
        if (event.key() != qt.Key_Enter and event.key() != qt.Key_Return) and (event.key() != qt.Key_Backspace):
            txt=self.vars["lineEdit"].text()
            n=self.vars["lineEdit"].cursorPosition()
            etxt=event.text()
            list_i = list(txt)  # str -> list
            list_i.insert(n, etxt)  # 注意不用重新赋值
            str_i = ''.join(list_i)  # list -> str
            self.vars["lineEdit"].setText(str_i)
        elif (event.key() == qt.Key_Enter) or event.key() == qt.Key_Return:
            if self.vars["lineEdit"].text() == '全选' or self.vars["lineEdit"].text().strip() == '':
                self.select_all()
            else:
                self.in_text(self.vars["lineEdit"].text())
        elif (event.key() == qt.Key_Backspace):
            if self.vars["lineEdit"].text()=='全选' or len(self.vars["lineEdit"].text())>10 or self.vars["lineEdit"].text()=='无选择':
                self.setEditText('')
            super().keyPressEvent(event)
