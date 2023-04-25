from PyQtGuiLib.header import (
    QWidget,
    QMessageBox
)

from PyQtGuiLib.core.comboBox.comboCheckBox.py_style import PyStyle


class Py_Message_box(QMessageBox):
    def __init__(self,
                 parent: QWidget = None,
                 obj_name=None,
                 title=None,
                 icon=None,
                 width=390,
                 height=120,
                 style=None,
                 message_txt=None,
                 yes_txt=None,
                 no_txt=None,
                 type=None,
                 is_frame=True,
                 ):
        super(Py_Message_box, self).__init__()

        self._parent=parent
        self._obj_name=obj_name
        self._title=title
        self._icon =icon
        self._width =width
        self._height=height
        self._style=style
        self._message_txt=message_txt
        self._yes_txt=yes_txt
        self._no_txt=no_txt
        self._type=type
        self._isFrame = is_frame

        # 设置名称
        if self._obj_name is not None:
            self.setObjectName(self._obj_name)

        # 设置标题
        if self._title is not None:
            self.setWindowTitle(self._title)
        # 设置按钮的尺寸范围
        if self._width is None:
            if self._height is None:
                pass
            else:
                self.setMinimumHeight(self._height)
                self.setMaximumHeight(self._height)
        else:
            if self._height is None:
                self.setMinimumWidth(self._width)
                self.setMaximumWidth(self._width)
            else:
                self.setFixedSize(self._width, self._height)
        if type=='information':
            self.informat(self._message_txt)

        self.set_styleSheet(self._style)
        self.exec_()
        self.set_styleSheet(self._style)


    def set_styleSheet(self, style=None):
        """设置样式"""
        if style is not None:
            self.setStyleSheet(style)
        else:
            self.setStyleSheet(PyStyle.messagebox)

    def informat(self,txt):
        self.setText(txt)
        self.setStandardButtons(QMessageBox.Yes)

        buttonY = self.button(QMessageBox.Yes)
        buttonY.setText('确 定')


