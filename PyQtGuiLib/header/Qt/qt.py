# -*- coding:utf-8 -*-
# @time:2023/1/68:49
# @author:LX
# @file:qt.py
# @software:PyCharm
from PyQtGuiLib.header.versions import PYQT_VERSIONS
from PyQtGuiLib.header import Qt,QPainter,QStyle,QSizePolicy,QEasingCurve


if PYQT_VERSIONS == "PyQt5"  :
    FramelessWindowHint = Qt.FramelessWindowHint
    Window = Qt.Window
    WindingFill = Qt.WindingFill
    WindowStaysOnTopHint = Qt.WindowStaysOnTopHint
    ArrowCursor = Qt.ArrowCursor
    SizeFDiagCursor = Qt.SizeFDiagCursor
    SizeBDiagCursor = Qt.SizeBDiagCursor
    SizeHorCursor = Qt.SizeHorCursor
    SizeVerCursor = Qt.SizeVerCursor
    LeftButton = Qt.LeftButton
    OpenHandCursor = Qt.OpenHandCursor
    WA_TranslucentBackground = Qt.WA_TranslucentBackground
    WA_DeleteOnClose = Qt.WA_DeleteOnClose
    WA_StyledBackground = Qt.WA_StyledBackground
    NoBrush = Qt.NoBrush
    NoPen = Qt.NoPen
    red = Qt.red
    blue = Qt.blue
    white = Qt.white
    black = Qt.black
    gray = Qt.gray
    transparent = Qt.transparent
    Antialiasing = QPainter.Antialiasing
    SmoothPixmapTransform = QPainter.SmoothPixmapTransform
    TextAntialiasing = QPainter.TextAntialiasing
    PE_Widget = QStyle.PE_Widget
    AlignCenter = Qt.AlignCenter
    ScrollBarAlwaysOn = Qt.ScrollBarAlwaysOn
    ScrollBarAlwaysOff = Qt.ScrollBarAlwaysOff
    ScrollBarAsNeeded = Qt.ScrollBarAsNeeded
    SolidLine = Qt.SolidLine
    DashLine = Qt.DashLine
    DotLine = Qt.DotLine
    DashDotLine = Qt.DashDotLine
    DashDotDotLine = Qt.DashDotDotLine
    CustomDashLine = Qt.CustomDashLine
    Widget = Qt.Widget
    PolicyExpanding = QSizePolicy.Expanding
    PolicyMinimum = QSizePolicy.Minimum
    PolicyPushButton = QSizePolicy.PushButton
    Horizontal = Qt.Horizontal
    Vertical = Qt.Vertical
    PM_LayoutHorizontalSpacing = QStyle.PM_LayoutHorizontalSpacing
    PM_LayoutVerticalSpacing = QStyle.PM_LayoutVerticalSpacing
    NoFocus = Qt.NoFocus
    TabFocus = Qt.TabFocus
    ClickFocus = Qt.ClickFocus
    StrongFocus = Qt.StrongFocus
    OutBounce = QEasingCurve.OutBounce
    CosineCurve = QEasingCurve.CosineCurve
    SineCurve = QEasingCurve.SineCurve
    InCurve = QEasingCurve.InCurve



if PYQT_VERSIONS in ["PyQt6","PySide2","PySide6"]:
    Window = Qt.WindowType.Window
    WindingFill = Qt.WindowType.WindingFill
    FramelessWindowHint = Qt.WindowType.FramelessWindowHint
    WindowStaysOnTopHint =Qt.WindowType.WindowStaysOnTopHint
    ArrowCursor = Qt.CursorShape.ArrowCursor
    SizeFDiagCursor = Qt.CursorShape.SizeFDiagCursor
    SizeBDiagCursor = Qt.CursorShape.SizeBDiagCursor
    SizeHorCursor = Qt.CursorShape.SizeHorCursor
    SizeVerCursor = Qt.CursorShape.SizeVerCursor
    LeftButton = Qt.MouseButton.LeftButton
    OpenHandCursor = Qt.CursorShape.OpenHandCursor
    WA_TranslucentBackground = Qt.WidgetAttribute.WA_TranslucentBackground
    WA_DeleteOnClose = Qt.WidgetAttribute.WA_DeleteOnClose
    WA_StyledBackground = Qt.WidgetAttribute.WA_StyledBackground
    NoBrush = Qt.BrushStyle.NoBrush
    NoPen = Qt.PenStyle.NoPen
    red = Qt.GlobalColor.red
    blue = Qt.GlobalColor.blue
    white = Qt.GlobalColor.white
    black = Qt.GlobalColor.black
    gray = Qt.GlobalColor.gray
    transparent = Qt.GlobalColor.transparent
    Antialiasing = QPainter.RenderHint.Antialiasing
    SmoothPixmapTransform = QPainter.RenderHint.SmoothPixmapTransform
    TextAntialiasing = QPainter.RenderHint.TextAntialiasing
    PE_Widget = QStyle.PrimitiveElement.PE_Widget
    AlignCenter = Qt.AlignmentFlag.AlignCenter
    ScrollBarAlwaysOn = Qt.ScrollBarPolicy.ScrollBarAlwaysOn
    ScrollBarAlwaysOff = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    ScrollBarAsNeeded = Qt.ScrollBarPolicy.ScrollBarAsNeeded
    SolidLine = Qt.PenStyle.SolidLine
    DashLine = Qt.PenStyle.DashLine
    DotLine = Qt.PenStyle.DotLine
    DashDotLine = Qt.PenStyle.DashDotLine
    DashDotDotLine = Qt.PenStyle.DashDotDotLine
    CustomDashLine = Qt.PenStyle.CustomDashLine
    Widget = Qt.WindowType.Widget
    PolicyExpanding = QSizePolicy.Policy.Expanding
    PolicyMinimum = QSizePolicy.Policy.Minimum
    Horizontal = Qt.Orientation.Horizontal
    Vertical = Qt.Orientation.Vertical
    PM_LayoutHorizontalSpacing = QStyle.PixelMetric.PM_LayoutHorizontalSpacing
    PM_LayoutVerticalSpacing = QStyle.PixelMetric.PM_LayoutVerticalSpacing
    NoFocus = Qt.FocusPolicy.NoFocus
    TabFocus = Qt.FocusPolicy.TabFocus
    ClickFocus = Qt.FocusPolicy.ClickFocus
    StrongFocus = Qt.FocusPolicy.StrongFocus
    OutBounce = QEasingCurve.Type.OutBounce
    CosineCurve = QEasingCurve.Type.CosineCurve
    SineCurve = QEasingCurve.Type.SineCurve
    InCurve = QEasingCurve.Type.InCurve
