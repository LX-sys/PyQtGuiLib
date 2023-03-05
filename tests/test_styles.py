from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QPushButton,
    QWidget
)

from PyQtGuiLib.styles import ButtonStyle
from PyQtGuiLib.core import FlowLayout

class TestStyle(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800, 500)

        self.flow = FlowLayout(self)


        for i in range(50):
            btn = QPushButton("test_{}".format(str(i)), self)
            btn.setFixedSize(130,60)
            # btn.setStyleSheet(ButtonStyle.contrastStyle())  # 互补色样式
            # btn.setStyleSheet(ButtonStyle.randomStyle()) # 随机样式
            btn.setStyleSheet(ButtonStyle.homologyStyle())  # 同色调样式
            self.flow.addWidget(btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestStyle()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())