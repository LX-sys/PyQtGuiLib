from PyQtGuiLib.header.Qt.qtWidgets import *
from PyQtGuiLib.header.Qt.qtGui import *
from PyQtGuiLib.header.Qt.qtCore import *
from PyQtGuiLib.header.Qt.qtSip import *
from PyQtGuiLib.header.Qt import qt
from PyQtGuiLib.header.py.common import *

from PyQtGuiLib.header.versions import PYQT_VERSIONS
from PyQtGuiLib.header.utility import *
from PyQtGuiLib.header.customStyle import CustomStyle


# 处理mac下无法运行的情况
if is_mac_sys and PYQT_VERSIONS in ["PySide2","PySide6"]:
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
