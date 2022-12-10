from PyQtGuiLib.header.Qt.qtWidgets import *
from PyQtGuiLib.header.Qt.qtGui import *
from PyQtGuiLib.header.Qt.qtCore import *
from PyQtGuiLib.header.py.common import *

from PyQtGuiLib.header.versions import PYQT_VERSIONS


# 处理mac下无法运行的情况
if sys.platform == "darwin" and PYQT_VERSIONS in ["PySide2","PySide6"]:
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
