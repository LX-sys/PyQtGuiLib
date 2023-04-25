# -*- coding: utf-8 -*-

class PyStyle:
    """样式集合"""

    windowQFStyle = """
        #windowQF {{
            background-color: {_bg_color};
            network-radius: {_border_radius};
            network: {_border_size}px solid {_border_color};
        }}
        QFrame {{ 
            color: {_text_color};
            font: {_text_font};
        }}
    """
    TEBgQF = """
        #TEBgQF {{
            background-color: {_bg_color};
            network-radius: {_border_radius};
            network: {_border_size}px solid {_border_color};
        }}
        QFrame {{ 
            color: {_text_color};
            font: {_text_font};
        }}
    """
    toolTipStyle = """ 
        QLabel {{		
            background-color: {_dark_one};	
            color: {_text_foreground};
            padding-left: 10px;
            padding-right: 10px;
            network-radius: 17px;
            network: 0px solid transparent;
            network-left: 3px solid {_context_color};
            network-right: 3px solid {_context_color};
            font: 800 9pt "Segoe UI";
        }}
        """

    messagebox = """
                QMessageBox {
                background-color: #272c36; 
            
                font-size: 16pt;
                border-radius: 50px;
                }
               QMessageBox QLabel#qt_msgbox_label { /* textLabel */
                color: #298DFF;
                background-color: transparent;
                min-width: 390px; /* textLabel设置最小宽度可以相应的改变QMessageBox的最小宽度 */
                min-height: 60px; /* textLabel和iconLabel高度保持一致 */
                max-height:60px;
            }
            QMessageBox QLabel#qt_msgboxex_icon_label { /* iconLabel */
                width: 40px;
                height: 60px; /* textLabel和iconLabel高度保持一致 */
            }

            QMessageBox QPushButton {
                border: 1px solid #298DFF;
                border-radius: 10px;
                background-color: #F2F2F2;
                color: #272c36;
                text-align:center;
                font-family: "Microsoft YaHei";
                font-size: 15pt;
                min-width: 70px;
                min-height: 0px;
                margin-right: 30px;
                margin-top: 0px;
            }
            QMessageBox QPushButton:hover {
                background-color: #298DFF;
                color: #F2F2F2;
            }
            QMessageBox QPushButton:pressed {
                background-color: #257FE6;
            }
            /*QMessageBox QDialogButtonBox#qt_msgbox_buttonbox { /* buttonBox */
            button-layout: 0;  }*/

        """
    messagebox1 = {"""
    
            QMessageBox {
            background-color: #F2F2F2; /* QMessageBox背景颜色 */
            }
            
           QMessageBox QLabel#qt_msgbox_label { /* textLabel */
                color: #298DFF;
                background-color: transparent;
                min-width: 240px; /* textLabel设置最小宽度可以相应的改变QMessageBox的最小宽度 */
                min-height: 40px; /* textLabel和iconLabel高度保持一致 */
            }
            
            /*QMessageBox QLabel#qt_msgboxex_icon_label { /* iconLabel */
                width: 40px;
                height: 40px; /* textLabel和iconLabel高度保持一致 */
            }
            */
            QMessageBox QPushButton { /* QMessageBox中的QPushButton样式 */
                border: 1px solid #298DFF;
                border-radius: 3px;
                background-color: #F2F2F2;
                color: #298DFF;
                font-family: "Microsoft YaHei";
                font-size: 10pt;
                min-width: 70px;
                min-height: 25px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #298DFF;
                color: #F2F2F2;
            }
            
            QMessageBox QPushButton:pressed {
                background-color: #257FE6;
            }
            
            /*QMessageBox QDialogButtonBox#qt_msgbox_buttonbox { /* buttonBox */
                button-layout: 0; /* 设置QPushButton布局好像没啥作用 *//* 
    
    """
                  }
    ComBoStyle = """
        QComboBox {
            color:rgb(255, 255, 255);
            background-color: rgb(27, 29, 35);
            border-radius: 5px;
            border: 1px solid rgb(33, 37, 43);
            padding: 5px;
            padding-left: 10px;
            border-radius: 8px;
           
            
            
        }
        QComboBox:hover{ border: 2px solid rgb(86, 138, 242);
        }
        QComboBox::drop-down {
            background-color:rgba(13,61,101,10);
            subcontrol-origin: padding;
            subcontrol-position: top right;
            border-left-width: 1px;
            border-left-color: rgba(60, 60, 54, 250);
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
            background-position: center;
            background-repeat: no-reperat; 
         }
         
         
         QCheckBox {color: rgb(200, 200, 200);font: 19pt;}
         QCheckBox::indicator:checked{
         background: #556B2F;
          }
          /*
         QComboBox::model:checked{
         background: rgb(255,71,209);
          }*/
               
         
         QComboBox QAbstractItemView {
            color: rgb(86,138,242);
            background-color: rgb(33, 37, 43);
            padding: 2px;
            selection-background-color: rgb(39, 44, 54);
            font: 19pt;
        }
        #xitongmingchengBox QAbstractItemView {
            color: rgb(86,138,242);
            background-color: rgb(33, 37, 43);
            padding: 2px;
            selection-background-color: rgb(39, 44, 54);
            font: 9pt;
        }
        
         QComboBox QAbstractItemView::item {
             height:28px;
             padding: 0px;
             margin: 0px;
             color: rgb(200, 200, 180);
              selection-color:rgb(33, 37, 43);
              selection-background-color: rgb(39, 44, 54);
            }
            
            
            
        QComboBox QAbstractItemView::item:selected {
            color: rgb(0,0,0);
            background: rgb(13,61,101);
        }
        /*
        QComboBox QAbstractItemView :checked {
            color: rgb(255,0,0);
            background: rgb(255,61,101);
        }*/
        
                                       
        QComboBox  QToolTip{
        color: rgb(0, 0, 0);
        font: 11pt;
        background:  rgb(129,118, 42);
        
        width: 800px;
        border-radius: 50px;
        border-bottom-left-radius: 20px;
        border-bottom-right-radius: 20px;

        }  
         

        QComboBox QAbstractScrollArea QScrollBar:vertical {
            border: none;
            background: rgb(52,59,72);
            width: 10px;
            border-radius: 2px;
        }
        QComboBox QAbstractScrollArea QScrollBar::handle:vertical {
            background: #568af2;
            min-height: 25px;
            border-radius: 4px;
          
        }
        QComboBox QAbstractScrollArea QScrollBar::add-line:vertical {
            background: #343b48;
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
           
        }
        QComboBox QAbstractScrollArea QScrollBar::sub-line:vertical {
            border: none;
            background: #343b48;
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
           
        }
        QComboBox QAbstractScrollArea QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
           
        }
        QComboBox QAbstractScrollArea QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none; 
        }
        """
    ComBoStyle1 = """
            QComboBox {
                color:rgb(255, 255, 255);
                background-color: rgb(27, 50, 50);
                border-radius: 5px;
                border: 1px solid rgb(33, 37, 43);
                padding: 5px;
                padding-left: 10px;
                border-radius: 8px;



            }
            QComboBox:hover{ border: 2px solid rgb(86, 138, 242);
            }
            QComboBox::drop-down {
                background-color:rgba(13,61,101,10);
                subcontrol-origin: padding;
                subcontrol-position: top right;
                border-left-width: 1px;
                border-left-color: rgba(60, 60, 54, 250);
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-position: center;
                background-repeat: no-reperat; 
             }


             QCheckBox {color: rgb(200, 200, 200);font: 19pt;}
             QCheckBox::indicator:checked{
             background: #556B2F;
              }
              /*
             QComboBox::model:checked{
             background: rgb(255,71,209);
              }*/


             QComboBox QAbstractItemView {
                color: rgb(86,138,242);
                background-color: rgb(33, 37, 43);
                padding: 2px;
                selection-background-color: rgb(39, 44, 54);
                font: 19pt;
            }
            #xitongmingchengBox QAbstractItemView {
                color: rgb(86,138,242);
                background-color: rgb(33, 37, 43);
                padding: 2px;
                selection-background-color: rgb(39, 44, 54);
                font: 9pt;
            }

             QComboBox QAbstractItemView::item {
                 height:28px;
                 padding: 0px;
                 margin: 0px;
                 color: rgb(200, 200, 180);
                  selection-color:rgb(33, 37, 43);
                  selection-background-color: rgb(39, 44, 54);
                }



            QComboBox QAbstractItemView::item:selected {
                color: rgb(0,0,0);
                background: rgb(13,61,101);
            }
            /*
            QComboBox QAbstractItemView :checked {
                color: rgb(255,0,0);
                background: rgb(255,61,101);
            }*/


            QComboBox  QToolTip{
            color: rgb(0, 0, 0);
            font: 11pt;
            background:  rgb(129,118, 42);

            width: 800px;
            border-radius: 50px;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;

            }  


            QComboBox QAbstractScrollArea QScrollBar:vertical {
                border: none;
                background: rgb(52,59,72);
                width: 10px;
                border-radius: 2px;
            }
            QComboBox QAbstractScrollArea QScrollBar::handle:vertical {
                background: #568af2;
                min-height: 25px;
                border-radius: 4px;

            }
            QComboBox QAbstractScrollArea QScrollBar::add-line:vertical {
                background: #343b48;
                height: 20px;
                border-bottom-left-radius: 4px;
                border-bottom-right-radius: 4px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;

            }
            QComboBox QAbstractScrollArea QScrollBar::sub-line:vertical {
                border: none;
                background: #343b48;
                height: 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                subcontrol-position: top;
                subcontrol-origin: margin;

            }
            QComboBox QAbstractScrollArea QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;

            }
            QComboBox QAbstractScrollArea QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none; 
            }
            """
    ComBoStylecankao = """
        QComboBox {
    /* 边框宽度,线条样式,颜色 */
    border:3px solid red;

    /* 倒角 */
    border-radius:8px;

    /* 内边框 */
    padding:1px 18px 1px 3px;

    min-width:100px;
}

QComboBox:editable {
    background:green;
}

/* 渐变色:从左到右,黑白渐变 */
QComboBox:!editable,QComboBox::drop-down:editable {
    background:qlineargradient(x1:0, y1:0, x2:1, y2:0,
                               stop:0 rgb(0,0,0), stop:1 rgb(255,255,255));
}

/* 当下拉框打开时,背景颜色渐变 */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                stop: 0.5 #DDDDDD, stop: 1.0 #BBBBBB);
}

/* 当下拉框打开时, 移动显示框文本位置*/
QComboBox:on {
    padding-top: 3px;
    padding-left: 4px;
}

/* 下拉按钮 */
QComboBox::drop-down {
    subcontrol-origin: padding;

    /* 按钮位置,右上角 */
    subcontrol-position: top right;

    /* 按钮宽度 */
    width: 25px;

    /* 一条边框线控制 */
    border-left-width: 3px;
    border-left-color: red;
    border-left-style: solid;

    /* 倒角 */
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}

/* 下拉按钮图片 */
QComboBox::down-arrow {
    border-image: url(:/gui/image/png_icons/xiaolog.png);
}

/* 下拉按钮位移 */
QComboBox::down-arrow:on {
    top: 1px;
    left: 1px;
}

/* 下拉列表里的颜色 */
QComboBox QAbstractItemView {
    border: 2px solid darkgray;
    selection-background-color: green;
}

        """
    ComBoTEWrong = """
        QComboBox {
            background-color: rgb(27, 29, 35);
            border-radius: 5px;
            border: 2px solid rgb(33, 37, 43);
            padding: 5px;
            padding-left: 10px;
            border-radius: 8px;
        }
        QComboBox:editable{ color: rgb(189, 147, 249); 
        }
        QComboBox:hover{ border: 2px solid rgb(189, 147, 249);
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            border-left-width: 3px;
            border-left-color: rgba(39, 44, 54, 150);
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
            background-position: center;
            background-repeat: no-reperat;
         }
        QComboBox QAbstractItemView {
            color: rgb(86,138,242);
            background-color: rgb(33, 37, 43);
            padding: 10px;
            selection-background-color: rgb(39, 44, 54);
        }
        QComboBox QAbstractScrollArea QScrollBar:vertical {
            border: none;
            background: rgb(52,59,72);
            width: 10px;
            border-radius: 0px;
        }
        QComboBox QAbstractScrollArea QScrollBar::handle:vertical {
            background: #568af2;
            min-height: 25px;
            border-radius: 4px;
        }
        QComboBox QAbstractScrollArea QScrollBar::add-line:vertical {
            background: #343b48;
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QComboBox QAbstractScrollArea QScrollBar::sub-line:vertical {
            border: none;
            background: #343b48;
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QComboBox QAbstractScrollArea QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QComboBox QAbstractScrollArea QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """
    # combo红色版保留样式
    ComBo1 = """
        QComboBox {
            background-color: rgb(27, 29, 35);
            network-radius: 5px;
            network: 2px solid rgb(33, 37, 43);
            padding: 5px;
            padding-left: 10px;
            network-radius: 8px;
        }
        QComboBox:editable{ color: rgb(189, 147, 249); 
        }
        QComboBox:hover{ border: 2px solid rgb(86, 138, 242);
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            network-left-width: 3px;
            network-left-color: rgba(39, 44, 54, 150);
            network-left-style: solid;
            network-top-right-radius: 3px;
            network-bottom-right-radius: 3px;
            background-position: center;
            background-repeat: no-reperat;
         }
        QComboBox QAbstractItemView {
            color: rgb(86,138,242);
            background-color: rgb(33, 37, 43);
            padding: 10px;
            selection-background-color: rgb(39, 44, 54);
        }
        
                                                
                                                

        QComboBox QAbstractScrollArea QScrollBar:vertical {
            border: none;
            background: rgb(52,59,72);
            width: 10px;
            border-radius: 0px;
        }
        QComboBox QAbstractScrollArea QScrollBar::handle:vertical {
            background: #568af2;
            min-height: 25px;
            border-radius: 4px;
        }
        QComboBox QAbstractScrollArea QScrollBar::add-line:vertical {
            background: #343b48;
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QComboBox QAbstractScrollArea QScrollBar::sub-line:vertical {
            border: none;
            background: #343b48;
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QComboBox QAbstractScrollArea QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QComboBox QAbstractScrollArea QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """
    TableStyle = '''
        QTableWidget {{	
            background-color: {_bg_color};
            padding: 2px;
            border-radius: {_radius}px;
            gridline-color: {_grid_line_color};
            color: rgb(0,0,0);
            font: 13pt;

        }}
        QTableWidget::item{{
            border-color: none;
            padding-left: 2px;
            padding-right: 2px;
            gridline-color: rgb(44, 49, 60);
            border-bottom: 1px solid {_bottom_line_color};
        }}
        QTableWidget::item:selected{{
            background-color: {_selection_color};
            color: rgb(160,160,160);
        }}
        QHeaderView::section{{
            background-color: rgb(86,138,242);
            max-width: 30px;
            border: 1px solid rgb(44, 49, 58);
            border-style: none;
            border-bottom: 1px solid rgb(44, 49, 60);
            border-right: 1px solid rgb(44, 49, 60);
        }}
        QHeaderView::section:hover{{color: rgb(86,138,242);}}
        QTableWidget::horizontalHeader {{	
            background-color: rgb(33, 37, 43);
        }}
        QTableWidget QTableCornerButton::section {{
            border: none;
            background-color: {_header_horizontal_color};
            padding: 3px;
            border-top-left-radius: {_radius}px;
        }}
        QHeaderView::section:horizontal
        {{
            border: none;
            background-color: {_header_horizontal_color};
            padding: 3px;
            font: 14pt;
        }}
        QHeaderView::section:vertical
        {{
            border: none;
            background-color: {_header_vertical_color};
            padding-left: 5px;
            padding-right: 5px;
            border-bottom: 1px solid {_bottom_line_color};
            margin-bottom: 1px;
        }}
        QScrollBar:horizontal {{
            border: none;
            background: {_scroll_bar_bg_color};
            height: 10px;
            margin: 0px 21px 0px 21px;
            border-radius: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {_context_color};
            min-width: 25px;
            border-radius: 4px
        }}
        QScrollBar::add-line:horizontal {{
            border: none;
            background: {_scroll_bar_btn_color};
            width: 20px;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:horizontal {{
            border: none;
            background: {_scroll_bar_btn_color};
            width: 20px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }}
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
        {{
             background: none;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
        {{
             background: none;
        }}
        QScrollBar:vertical {{
            border: none;
            background: {_scroll_bar_bg_color};
            width: 10px;
            margin: 21px 0px 21px 0px;
            border-radius: 0px;
        }}
        QScrollBar::handle:vertical {{	
            background: {_context_color};
            min-height: 25px;
            border-radius: 4px
        }}
        QScrollBar::add-line:vertical {{
            border: none;
            background: {_scroll_bar_btn_color};
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:vertical {{
            border: none;
            background: {_scroll_bar_btn_color};
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
             background: none;
        }}

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
             background: none;
        }}
    '''
    MenuStyle = '''
        QMenu{
            background-color: rgb(27, 29, 35);
            network-radius: 8px;
            network: 1px solid rgb(33, 37, 43);
            padding-left: 3px;
            width: 190px;
        }
        QMenu::item {
            color: rgb(195,204,223);
            background-color: rgb(33, 37, 43);
            padding: 10px;
            selection-background-color: rgb(39, 44, 54);
            network: 1px solid rgb(27, 29, 352);
            width: 160px;
            font: 13pt;
        }
        QMenu::item:selected{
            color: rgb(86, 138, 242);
        }
    '''
    # TODO 样式优化一下
    TabStyle = '''
        QTabWidget::pane {
            background-color: transparent;
            padding: 2px;
            border-radius: 5px;
            border-bottom: 1px solid rgb(44, 49, 60);
        }
        QTabBar::tab {
            background-color: rgb(33, 37, 43);
            width: 150;
            border-radius: 3px;
        }
        QTabBar::tab:hover{color: rgb(86,138,242);}
        QTabBar::tab:selected {
            border-bottom: 2px solid #568af2;
            color: rgb(86,138,242);
        }
    '''
    RadioBtnStyle = '''
        QRadioButton::indicator{
            network: 3px solid rgb(52, 59, 72);
            width: 15px;
            height: 15px;
            network-radius: 10px;
            background: rgb(44, 49, 60);
        }
        QRadioButton::indicator:hover{ network: 3px solid rgb(86, 138, 242);}
        QRadioButton::indicator:checked{
            background: 3px solid rgb(108,153,244);
            network: 3px solid rgb(52, 59, 72);
        }
    '''
    SAVerticalStyle = '''
        QScrollBar:vertical {
            border: none;
            background: rgb(52,59,72);
            width: 12px;
            border-radius: 0px;
        }
        QScrollBar::handle:vertical {
            background: #568af2;
            min-height: 25px;
            border-radius: 4px;
        }
        QScrollBar::add-line:vertical {
            background: #343b48;
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            border: none;
            background: #343b48;
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }  
    '''
    SAHorizontalStyle = '''
        QScrollBar:horizontal {
            border: none;
            background: rgb(52,59,72);
            height: 12px;
            border-radius: 0px;
        }
        QScrollBar::handle:horizontal {
            background: #568af2;
            min-width: 25px;
            border-radius: 4px;
        }
        QScrollBar::add-line:horizontal {
            background: #343b48;
            width: 20px;
            border-right-top-radius: 4px;
            border-right-bottom-radius: 4px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:horizontal {
            border: none;
            background: #343b48;
            width: 20px;
            border-left-top-radius: 4px;
            border-left-bottom-radius: 4px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background: none;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
    '''
    LabelStyle = '''
        QToolTip{
            font-size:10px;
        }
    '''
