# -*- coding:utf-8 -*-
# @time:2023/2/1810:31
# @author:LX
# @file:controlType.py
# @software:PyCharm

__all__ = ["getStyleLists","getStyleCommentLists"]

STYLE_LIB = {
    ("QPushButton",):{"QPushButton":"/*按钮*/",
                       "QPushButton:hover":"/*鼠标放在按钮上时的样式*/",
                       "QPushButton:pressed":"/*按钮按下时的样式*/",
                       "QPushButton::menu-indicator":"/*菜单指示器子控件(在菜单栏时的样式)*/",
                       "QPushButton:open":"/*按钮在菜单打开时的样式*/"},
    ("QLabel",): {"QLabel": "/*标签*/",
                  "QLabel:hover": "/*鼠标放在标签上时的样式*/"
               },
    ("QLineEdit",):{
        "QLineEdit":"/**/",
        "QLineEdit:read-only":"/*只读时读样式*/"
    },
    ("QComboBox",): {"QComboBox": "/*下拉框*/",
                  "QComboBox:!editable": "/*编辑框样式*/",
                  "QComboBox:editable": "/*编辑框样式(需要将editable设置为真才生效,内容可编辑)*/",
                  "QComboBox::drop-down": "/*下拉按钮样式*/",
                  "QComboBox::drop-down:editable": "/*下拉按钮样式(需要将editable设置为真才生效,内容可编辑)*/",
                  "QComboBox:!editable:on": "/*拉下列表展开时,编辑框样式*/",
                  "QComboBox::drop-down:!editable:on": "/*拉下列表展开时,下拉按钮样式*/",
                  "QComboBox:on": "/*拉下列表展开时,文本的样式*/",
                  "QComboBox::down-arrow": "按钮里的图标样式",
                  "QComboBox::down-arrow:on": "/*拉下列表展开时，移动箭头*/"
                  },
    ("QCheckBox",): {"QCheckBox": "/*复选框,将tristate设置为真时有三种状态(选中,未选中,待选中)*/",
                  "QCheckBox::indicator": "/*文本旁边的标志样式*/",
                  "QCheckBox::indicator:unchecked": "/*文本旁边的标志没有选中时的样式*/",
                  "QCheckBox::indicator:unchecked:hover": "/*文本旁边的标志没有选中时的鼠标放上去时的样式*/",
                  "QCheckBox::indicator:unchecked:pressed": "/*文本旁边的标志没有选中按下时一瞬间的样式*/",
                  "QCheckBox::indicator:checked": "/*文本旁边的标志选中时的样式*/",
                  "QCheckBox::indicator:checked:hover": "/*文本旁边的标志选中时的鼠标放上去时的样式*/",
                  "QCheckBox::indicator:checked:pressed": "/*文本旁边的标志选中按下时一瞬间的样式*/",
                  "QCheckBox::indicator:indeterminate:hover": "/*文本旁边的标志待选中时的鼠标放上去时的样式(需要将tristate设置为真才生效)*/",
                  "QCheckBox::indicator:indeterminate:pressed": "/*文本旁边的标志待选中按下时一瞬间的样式(需要将tristate设置为真才生效)*/"},
    ("QGroupBox",): {"QGroupBox": "/*组合框(与QCheckBox样式相似)*/",
                  "QGroupBox::title": "/*标题样式*/",
                  "QGroupBox::indicator": "/*标题旁边控件样式(需要将checkable)设置为真才生效*/",
                  "QGroupBox::indicator:unchecked": "/*标题旁边控件没有选中时的样式(需要将checkable)设置为真才生效)*/"
                  },
    ("QListView",): {"QListView": "/*列表视图*/",
                  "QListView::item:alternate": "/**/",
                  "QListView::item:selected": "/**/",
                  "QListView::item:selected:!active": "/**/",
                  "QListView::item:selected:active": "/**/",
                  "QListView::item:hover": "/**/"
                  },
    ("QListWidget",): {"QListWidget": "/*列表视图*/",
                       "QListWidget::item:alternate": "/**/",
                       "QListWidget::item:selected": "/**/",
                       "QListWidget::item:selected:!active": "/**/",
                       "QListWidget::item:selected:active": "/**/",
                       "QListWidget::item:hover": "/**/"
                       },
    ("QProgressBar",): {"QProgressBar": "/*进度条*/",
                     "QProgressBar::chunk": "进度条中间颜色区域样式"},
    ("QScrollBar",): {"QScrollBar": '''
            /*滚动条样式
            QScrollBar 指所有滚动条样式
            QScrollBar:horizontal 水平
            QScrollBar:vertical  垂直
            */
            ''',
                   "QScrollBar:horizontal": "/*水平滚动条样式*/",
                   "QScrollBar::handle:horizontal": "/*水平滚动条中手柄的样式*/",
                   "QScrollBar::add-line:horizontal": "/*水平滚动条最右边按钮样式*/",
                   "QScrollBar::sub-line:horizontal": "/*水平滚动条最左边按钮样式*/",
                   "QScrollBar:vertical": "/**/",
                   "QScrollBar::handle:vertical": "/**/",
                   "QScrollBar::add-line:vertical": "/**/",
                   "QScrollBar::sub-line:vertical": "/**/"},
    ("QSlider",):{"QSlider":
                    '''
                    /*
                    滑动条
                    QSlider 指所有滑动条
                    还有 horizontal vertical
                    */
                    ''',
                   "QSlider::groove:horizontal":"/*水平凹槽样式*/",
                   "QSlider::handle:horizontal":"/*水平手柄样式*/",
                   "QSlider::add-page:horizontal":"/*更改手柄前后滑块部分的样式*/",
                   "QSlider::sub-page:horizontal":"/*更改手柄前后滑块部分的样式*/",
                   "QSlider::groove:vertical": "/**/",
                   "QSlider::handle:vertical": "/**/",
                   "QSlider::add-page:vertical": "/**/",
                   "QSlider::sub-page:vertical": "/**/"
                   },
    ("QSpinBox",):{"QSpinBox":"/*微调框*/",
                    "QSpinBox::up-button":"/*上按钮样式*/",
                    "QSpinBox::up-button:hover":"鼠标放在上按钮时的样式",
                    "QSpinBox::up-button:pressed":"鼠标按下 下按钮时的样式",
                    "QSpinBox::up-arrow":"上按钮里小箭头样式",
                    "QSpinBox::down-button":"/*下按钮样式*/",
                    },
    ("QTabWidget",):{"QTabWidget":
                        '''
                        /*
                        标签窗口
                        好用的属性设置
                        documentMode 文档模式
                        tabsCloseable 标签按钮上出现关闭标志
                        movable 标签可移动
                        */
                        ''',
                      "QTabWidget::pane":"/*标签下面框架的样式*/",
                      "QTabBar::tab":"/*标签样式*/",
                      "QTabWidget::tab-bar":"/*标签栏样式(设置颜色无效)*/",
                      "QTabBar::tab:hover":"/*鼠标放在标签上时的样式*/",
                      "QTabBar::tab:selected":"/*标签被选择时的样式*/",
                      "QTabBar::tab:!selected":"/*标签没有被选择时的样式*/",
                      "QTabBar::close-button":"/*关闭按钮的样式(需要将tabsCloseable设置为真才生效)*/",
                      "QTabBar::close-button:hover":"/*鼠标放在关闭按钮上时的样式(需要将tabsCloseable设置为真才生效)*/"
                      },
    ("QTableView",):{"QTableView":"/*表格视图*/",
                      "QTableView QTableCornerButton::section":"/*角落部件样式*/"
                      },
    ("QTreeView",):{"QTreeView":"/*树视图*/",
                     "QTreeView::item":"/**/",
                     "QTreeView::item:hover":"/**/",
                     "QTreeView::item:selected":"/**/",
                     "QTreeView::item:selected:active":"/**/",
                     "QTreeView::item:selected:!active":"/**/",
                     "QTreeView::branch":"/*分支样式*/"},
}


def getStyles(key):
    if isinstance(key,str):
        key = key,
    return STYLE_LIB[key]


# 返回可操作的样式列表
def getStyleLists(key)->list:
    return list(getStyles(key).keys())


# 返回可操作的样式列表说明
def getStyleCommentLists(key)->list:
    return list(getStyles(key).values())


# 融合两个样式列表
def getMergeStyles(style1:list,style2:list)->list:
    return list(set(style1) | set(style2))


# print(getMergeStyles(["QPushButton"],["QPushButton","QPushButton:hover"]))
