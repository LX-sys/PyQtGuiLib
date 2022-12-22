from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    Qt,
    QWidget,
    QGridLayout,
    QLabel,
    QFont
)
'''
    亚克力窗口
'''

from windowEffect import WindowEffect

from PyQtGuiLib.core.widgets import BorderlessWidget

class AcrylicWidget(BorderlessWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        # self.setWindowFlags(Qt.FramelessWindowHint)  # make the window frameless
        self.setAttribute(Qt.WA_TranslucentBackground)  # make the window translucent
        #
        self.ui_layout = QGridLayout(self)  # create a ui layout
        self.ui_layout.setAlignment(Qt.AlignCenter)  # center the layout

        self.label = QLabel("Hello World!", self)  # create a label to display a text
        self.label.setFont(QFont("Segoe UI", 14))  # configure the text size and font
        # self.ui_layout.addWidget(self.label)  # add the label widget into the layout
        self.windowFX = WindowEffect()  # instatiate the WindowEffect class
        self.windowFX.setAcrylicEffect(self.winId())  # set the Acrylic effect by
        # self.windowFX.setAeroEffect(self.winId())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AcrylicWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())