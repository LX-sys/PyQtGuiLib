from PyQtGuiLib.header.versions import PYQT_VERSIONS

if PYQT_VERSIONS == "PyQt5":
    from PyQt5.QtGui import (
        QCursor,
        QPainter,
        QResizeEvent,
        QMouseEvent,
        QPaintEvent,
        QColor,
        QPen,
        QPainterPath,
        QPolygon,
        QPolygonF,
        QFont,
        QLinearGradient,
        QRadialGradient,
        QConicalGradient,
        QFontMetricsF,
        QCloseEvent,
        QBrush,
        QPalette
    )

if PYQT_VERSIONS == "PyQt6":
    from PyQt6.QtGui import (
        QCursor,
        QPainter,
        QResizeEvent,
        QMouseEvent,
        QPaintEvent,
        QColor,
        QPen,
        QPainterPath,
        QPolygon,
        QPolygonF,
        QFont,
        QLinearGradient,
        QRadialGradient,
        QConicalGradient,
        QFontMetricsF,
        QCloseEvent,
        QBrush,
        QPalette
    )

if PYQT_VERSIONS == "PySide2":
    from PySide2.QtGui import (
        QCursor,
        QPainter,
        QResizeEvent,
        QMouseEvent,
        QPaintEvent,
        QColor,
        QPen,
        QPainterPath,
        QPolygon,
        QPolygonF,
        QFont,
        QLinearGradient,
        QRadialGradient,
        QConicalGradient,
        QFontMetricsF,
        QCloseEvent,
        QBrush,
        QPalette
    )


if PYQT_VERSIONS == "PySide6":
    from PySide6.QtGui import (
        QCursor,
        QPainter,
        QResizeEvent,
        QMouseEvent,
        QPaintEvent,
        QColor,
        QPen,
        QPainterPath,
        QPolygon,
        QPolygonF,
        QFont,
        QLinearGradient,
        QRadialGradient,
        QConicalGradient,
        QFontMetricsF,
        QCloseEvent,
        QBrush,
        QPalette
    )