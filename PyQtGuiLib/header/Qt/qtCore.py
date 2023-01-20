from PyQtGuiLib.header.versions import PYQT_VERSIONS

if PYQT_VERSIONS == "PyQt5":
    from PyQt5.QtCore import (
        Qt,
        QUrl,
        pyqtSignal as Signal,
        QSize,
        QPoint,
        QPointF,
        QUrl,
        QRectF,
        QRect,
        QPropertyAnimation,
        QThread,
        QEasingCurve,
        QByteArray,
        QSequentialAnimationGroup,
        QParallelAnimationGroup,
        QMargins,
        QModelIndex,
        pyqtProperty
    )

if PYQT_VERSIONS == "PyQt6":
    from PyQt6.QtCore import (
        Qt,
        QUrl,
        pyqtSignal as Signal,
        QSize,
        QPoint,
        QPointF,
        QUrl,
        QRectF,
        QRect,
        QPropertyAnimation,
        QThread,
        QEasingCurve,
        QByteArray,
        QSequentialAnimationGroup,
        QParallelAnimationGroup,
        QMargins,
        QModelIndex,
        pyqtProperty
    )

if PYQT_VERSIONS == "PySide2":
    from PySide2.QtCore import (
        Qt,
        QUrl,
        Signal,
        QSize,
        QPoint,
        QPointF,
        QUrl,
        QRectF,
        QRect,
        QPropertyAnimation,
        QThread,
        QEasingCurve,
        QByteArray,
        QSequentialAnimationGroup,
        QParallelAnimationGroup,
        QMargins,
        QModelIndex,
        pyqtProperty
    )
if PYQT_VERSIONS == "PySide6":
    from PySide6.QtCore import (
        Qt,
        QUrl,
        Signal,
        QSize,
        QPoint,
        QPointF,
        QUrl,
        QRectF,
        QRect,
        QPropertyAnimation,
        QThread,
        QEasingCurve,
        QByteArray,
        QSequentialAnimationGroup,
        QParallelAnimationGroup,
        QMargins,
        QModelIndex,
        pyqtProperty
    )