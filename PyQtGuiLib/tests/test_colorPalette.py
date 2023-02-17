from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QVBoxLayout
)

'''
   调色板 测试用例
'''

from PyQtGuiLib.core import PaletteFrame

class Test_ColorPalette(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

#         self.setStyleSheet('''
# background-color: rgb(25, 25, 25);
#         ''')
        self.vboy = QVBoxLayout(self)

        self.pcolor = PaletteFrame(self,shape=PaletteFrame.Rect)
        self.pcolor.resize(500,300)
        self.pcolor.move(10,10)
        # self.pcolor.rgbaChange.connect(self.test)
        # self.pcolor.nameChange.connect(self.test_name)
        self.pcolor.clickColor.connect(self.test_click)

        # 测试按钮
        self.btn = QPushButton("test",self)
        self.btn.move(50,400)
        self.btn.resize(80,80)

        self.vboy.addWidget(self.pcolor)
        self.vboy.addWidget(self.btn)


    def test(self,rgba:tuple):
        print("-->",rgba)
        self.btn.setStyleSheet('''
background-color: rgba(%s, %s, %s,%s);
        '''%(rgba))

    def test_name(self,name):
        print(name)
        self.btn.setStyleSheet('''
        background-color: %s;
                ''' % (name))

    def test_click(self,rgba:tuple):
        print("-->",rgba)
        self.btn.setStyleSheet('''
background-color: rgba(%s, %s, %s,%s);
        '''%(rgba))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test_ColorPalette()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())