import importlib

# The current version of python qt used
PYQT_VERSIONS = None

VERSIONS = ["PyQt5","PySide2","PySide6","PyQt6"]

for module in VERSIONS:
    try:
        importlib.import_module(module)
        PYQT_VERSIONS = module
        break
    except:
        pass

if PYQT_VERSIONS is None:
    raise ModuleNotFoundError("Module not found,support:PyQt5,PyQt6,PySide2,PySide6")
