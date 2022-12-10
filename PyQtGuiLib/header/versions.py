# 当前python qt使用的版本
PYQT_VERSIONS = None

try:
    import PyQt5
    PYQT_VERSIONS = "PyQt5"
except:
    pass

try:
    import PyQt6
    PYQT_VERSIONS = "PyQt6"
except:
    pass

try:
    import PySide2
    PYQT_VERSIONS = "PySide2"
except:
    pass

try:
    import PySide6
    PYQT_VERSIONS = "PySide6"
except:
    pass
