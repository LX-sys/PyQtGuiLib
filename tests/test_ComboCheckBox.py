# -*- coding:utf-8 -*-
# @time:2023/4/2516:11
# @author:LX
# @file:test_ComboCheckBox.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
)

from PyQtGuiLib.core import ComboCheckBox


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.combox = ComboCheckBox(
            self,
            obj_name='extendCCBox',
            spacing=0,
            width=500,
            items=[]
        )
        lst = ['齐辉0', '齐辉1', '齐辉2', '齐辉3', '悯农', '骆宾王', '凡士林', '孙悟空', '李逵', '迈阿密', '黑龙江', '石油',
               '前十', '酱油', '狐狸', '寒冰', '开户行', '天行健君子以自强不息', '业精于勤荒于嬉行成于思毁于随']

        self.combox.add_items(lst)
        self.combox.only_text('齐辉0')

        self.combox.linSignal[object].connect(lambda x: print(x))
        print(self.combox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())