from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QPushButton
)
from PyQtGuiLib.core.widgets2 import WidgetABC

'''
    新无边框窗口
'''

class BorderlessWidget(WidgetABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.btn = QPushButton("test",self)
        self.btn.move(30,30)
        self.btn.clicked.connect(self.t_event)

    def t_event(self):
        self.c = WidgetABC()
        # 无边框模态
        self.c.setWinModality(True)
        self.c.show()
        win.setStyleSheet('''
        WidgetABC{
        qproperty-border:"3 dot rgba(100,100,255,255)";
        }
        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BorderlessWidget()
    win.setStyleSheet('''
WidgetABC{
qproperty-radius:7;
qproperty-backgroundColor: rgba(165, 138, 255,150);
qproperty-border:"1 solid rgba(100,100,255,255)";
}
''')
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())