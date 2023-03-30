# -*- coding:utf-8 -*-
# @time:2023/3/2914:11
# @author:LX
# @file:qssDrak.py
# @software:PyCharm

#
QSSDrak ='''

*{
background-color: rgb(50, 50, 50);
color:rgb(220, 220, 220);
font: 12pt "黑体";
}


QScrollBar:horizontal{
padding:0px;
max-height:12px;
padding:2px;
}
QScrollBar:vertical{
padding:0px;
max-width:12px;
padding:2px;
}
QScrollBar::handle{
background-color: rgb(39, 39, 39);
border-radius:4%;
}
QScrollBar::handle:hover{
background-color: rgb(72, 72, 72);
border:1px solid rgb(149, 149, 149);
}
QScrollBar::add-page,QScrollBar::sub-page {
background:rgb(57, 57, 57);
}
QScrollBar::sub-line,QScrollBar::add-line {
background:none;
}

QPushButton{
background-color: rgb(8, 8, 8);
border:2px solid rgb(230, 230, 230);
color:rgb(220, 220, 220);
border-radius:6%;
}
QPushButton:hover{
background-color: rgb(0, 0, 0);
}
QPushButton:pressed{
background-color:rgb(50, 50, 50);
}


QToolButton {
border-radius:6%;
background-color: #1E1E1E; 
color: #FFFFFF; 
border: 1px solid #2F2F2F; 
padding: 5px;
}
QToolButton:hover {
background-color: rgb(18, 18, 18);
}
QToolButton:pressed {
background-color:#1E1E1E; 
}


QCommandLinkButton{
background-color: rgb(8, 8, 8);
border:1px solid rgb(0, 120, 215);
color:rgb(220, 220, 220);
border-radius:6%;
}
QCommandLinkButton:hover{
background-color: rgb(0, 0, 0);
}
QCommandLinkButton:pressed{
background-color:rgb(50, 50, 50);
}


QListView {
outline: 0px;
background-color: rgb(2, 2, 2);
color: #FFFFFF;
border: 1px solid #666666;
}
QListView::item:hover{
padding:0px 0px 0px 15px;
color:rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0.5625, x2:0.994318, y2:0.614, stop:0 rgba(0, 0, 0, 255), stop:0.909091 rgba(73, 73, 73, 255));
}
QListView::item {
background-color: rgb(2, 2, 2);
color: rgb(143, 143, 143);
padding: 5px;
border-bottom: 1px solid #666666;
}
QListView::item:selected {
padding:0px 0px 0px 15px;
color:rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0.5625, x2:0.994318, y2:0.614, stop:0 rgba(0, 0, 0, 255), stop:0.909091 rgba(73, 73, 73, 255));
}



QTableView{
outline: 0px;
background-color:rgb(33, 33, 33);
gridline-color:rgb(125, 125, 125);
}
QTableView QHeaderView,QTableView QHeaderView::section, QTableView QTableCornerButton::section {
background-color:rgb(0, 0, 0);
color:rgb(175, 175, 175);
}
QTableView QHeaderView::section::pressed{
color:rgb(207, 207, 103);
}
QTableView QTableCornerButton::section{
background-color: rgb(0, 0, 0);
}
QHeaderView::section, QTableCornerButton:section {
padding: 3px;
margin: 0px;
border: 1px solid gray;
border-left-width: 0px;
border-right-width: 1px;
border-top-width: 0px;
border-bottom-width: 1px;
}
QTableView::indicator{
background-color: rgb(255, 170, 0);
}
QTableView::indicator:checked{
background-color:rgb(33, 33, 33);
}
QTableView::item{
padding:0px;
border:0px;
}
QTableView::item:selected{
background-color:#000;
}
QTableView::item:hover{
background-color: rgb(86, 86, 86);
}



QTreeView{
background-color: rgb(33, 33, 33);
color:rgb(188, 188, 188);
}
QTreeView QHeaderView,QTreeView QHeaderView::section{
background-color: rgb(0, 0, 0);
color:rgb(175, 175, 175);
}
QTreeView::item:hover{
background-color:transparent;
}
QTreeView::item:selected{
background-color:rgb(121, 121, 121);
color: rgb(255, 255, 255);
}
QTreeView::branch:selected{
background-color:rgb(121, 121, 121);
}


QGroupBox {
border:2px solid rgb(118, 118, 118);
border-radius:5px;
background-color: rgb(26, 26, 26);
}


QToolBox::tab {
background-color: rgb(90, 90, 90);
border-radius:3%;
padding:5px;
}
QToolBox::tab:selected{
font: italic;
color: white;
}



QTabWidget::pane {
}
QTabWidget QWidget{
background-color: rgb(20, 20, 20);
}
QTabWidget QTabBar::tab{
background-color: rgb(20, 20, 20);
min-width: 20ex;
padding: 5px;
}
QTabBar::tab:selected{
color: rgb(180, 239, 255);
}

QTabBar::tab:!selected{
background-color: rgb(65, 65, 65);
}



QComboBox {
background-color: rgb(0, 0, 0);
border:1px solid rgb(255, 255, 255);
border-bottom:none;
border-left:none;
border-right:none;
color: rgb(182, 182, 182);
border-radius: 1px;
padding: 1px 18px 1px 3px;
min-width: 6em;
}
QComboBox:editable{
}
QComboBox::drop-down{
}
QComboBox QAbstractItemView{
background-color: rgb(0, 0, 0);
border:none;
outline: 0px;
selection-background-color:rgb(0, 0, 0);
selection-color:rgb(0, 255, 255);
}


QFontComboBox{
border:2px solid rgb(103, 103, 103);
border-radius: 5px;
padding: 1px 18px 1px 3px;
min-width: 6em;
}
QFontComboBox QAbstractItemView{
outline: 0px;
selection-background-color: rgb(90, 90, 90);
}



QLineEdit{
border:2px solid rgb(0, 0, 0);
border-top:none;
border-left:none;
border-right:none;
}
QLineEdit:hover{
border:2px solid qlineargradient(spread:pad, x1:0.012, y1:0.556818, x2:1, y2:0.573864, stop:0 rgba(110, 203, 205, 255), stop:0.965909 rgba(67, 91, 95, 255));
border-top:none;
border-left:none;
border-right:none;
}



QTextEdit{
border:1px solid rgb(0, 0, 0);
border-radius: 3px;
}
QTextEdit:hover{
border:1px solid rgb(0, 85, 255);
}


QPlainTextEdit{
border:1px solid rgb(0, 0, 0);
border-radius: 4%;
background-color: rgb(66, 66, 66);
}
QPlainTextEdit:hover{
border:1px solid rgb(109, 109, 109);
}



QProgressBar {
border: 2px solid rgb(0, 0, 0);
border-radius: 5px;
}
QProgressBar::chunk {
border: 2px solid rgb(72, 72, 72);
width: 20px;
}
'''

QSSDrak2 ='''
/*=============overall============*/
*{
background-color: rgb(50, 50, 50);
color:rgb(220, 220, 220);
font: 12pt "黑体";
}


QScrollBar:horizontal{
padding:0px;
max-height:12px;
padding:2px;
}
QScrollBar:vertical{
padding:0px;
max-width:12px;
padding:2px;
}
QScrollBar::handle{
background-color: rgb(39, 39, 39);
border-radius:4%;
}
QScrollBar::handle:hover{
background-color: rgb(72, 72, 72);
border:1px solid rgb(149, 149, 149);
}
QScrollBar::add-page,QScrollBar::sub-page {
background:rgb(57, 57, 57);
}
QScrollBar::sub-line,QScrollBar::add-line {
background:none;
}
/* ============== Buttons =============== */
QPushButton{
background-color: rgb(8, 8, 8);
border:2px solid rgb(230, 230, 230);
color:rgb(220, 220, 220);
border-radius:6%;
}
QPushButton:hover{
background-color: rgb(0, 0, 0);
}
QPushButton:pressed{
background-color:rgb(50, 50, 50);
}

/* QToolButton */
QToolButton {
border-radius:6%;
background-color: #1E1E1E; 
color: #FFFFFF; 
border: 1px solid #2F2F2F; 
padding: 5px;
}
QToolButton:hover {
background-color: rgb(18, 18, 18);
}
QToolButton:pressed {
background-color:#1E1E1E; 
}

/* QCommandLinkButton */
QCommandLinkButton{
background-color: rgb(8, 8, 8);
border:1px solid rgb(0, 120, 215);
color:rgb(220, 220, 220);
border-radius:6%;
}
QCommandLinkButton:hover{
background-color: rgb(0, 0, 0);
}
QCommandLinkButton:pressed{
background-color:rgb(50, 50, 50);
}

/* ============ Item Views =============== */
QListView {
outline: 0px;
background-color: rgb(2, 2, 2);
color: #FFFFFF;
border: 1px solid #666666;
}
QListView::item:hover{
padding:0px 0px 0px 15px;
color:rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0.5625, x2:0.994318, y2:0.614, stop:0 rgba(0, 0, 0, 255), stop:0.909091 rgba(73, 73, 73, 255));
}
QListView::item {
background-color: rgb(2, 2, 2);
color: rgb(143, 143, 143);
padding: 5px;
border-bottom: 1px solid #666666;
}
QListView::item:selected {
padding:0px 0px 0px 15px;
color:rgb(255, 255, 255);
background-color: qlineargradient(spread:pad, x1:0, y1:0.5625, x2:0.994318, y2:0.614, stop:0 rgba(0, 0, 0, 255), stop:0.909091 rgba(73, 73, 73, 255));
}


/* QTableView */
QTableView{
outline: 0px;
background-color:rgb(33, 33, 33);
gridline-color:rgb(125, 125, 125);
}
QTableView QHeaderView,QTableView QHeaderView::section, QTableView QTableCornerButton::section {
background-color:rgb(0, 0, 0);
color:rgb(175, 175, 175);
}
QTableView QHeaderView::section::pressed{
color:rgb(207, 207, 103);
}
QTableView QTableCornerButton::section{
background-color: rgb(0, 0, 0);
}
QHeaderView::section, QTableCornerButton:section {
padding: 3px;
margin: 0px;
border: 1px solid gray;
border-left-width: 0px;
border-right-width: 1px;
border-top-width: 0px;
border-bottom-width: 1px;
}
QTableView::indicator{
background-color: rgb(255, 170, 0);
}
QTableView::indicator:checked{
background-color:rgb(33, 33, 33);
}
QTableView::item{
padding:0px;
border:0px;
}
QTableView::item:selected{
background-color:#000;
}
QTableView::item:hover{
background-color: rgb(86, 86, 86);
}


/* QTreeView */
QTreeView{
background-color: rgb(33, 33, 33);
color:rgb(188, 188, 188);
}
QTreeView QHeaderView,QTreeView QHeaderView::section{
background-color: rgb(0, 0, 0);
color:rgb(175, 175, 175);
}
QTreeView::item:hover{
background-color:transparent;
}
QTreeView::item:selected{
background-color:rgb(121, 121, 121);
color: rgb(255, 255, 255);
}
QTreeView::branch:selected{
background-color:rgb(121, 121, 121);
}

/* ================= Containers ================= */
QGroupBox {
border:2px solid rgb(118, 118, 118);
border-radius:5px;
background-color: rgb(26, 26, 26);
}

/* QToolBox */
QToolBox::tab {
background-color: rgb(90, 90, 90);
border-radius:3%;
padding:5px;
}
QToolBox::tab:selected{
font: italic;
color: white;
}


/*  QTabWidget  */
QTabWidget::pane {
}
QTabWidget QWidget{
background-color: rgb(20, 20, 20);
}
QTabWidget QTabBar::tab{
background-color: rgb(20, 20, 20);
min-width: 20ex;
padding: 5px;
}
QTabBar::tab:selected{
color: rgb(180, 239, 255);
}

QTabBar::tab:!selected{
background-color: rgb(65, 65, 65);
}


/* =================Input Widgets ==============*/
QComboBox {
background-color: rgb(0, 0, 0);
border:1px solid rgb(255, 255, 255);
border-bottom:none;
border-left:none;
border-right:none;
color: rgb(182, 182, 182);
border-radius: 1px;
padding: 1px 18px 1px 3px;
min-width: 6em;
}
QComboBox:editable{
}
QComboBox::drop-down{
}
QComboBox QAbstractItemView{
background-color: rgb(0, 0, 0);
border:none;
outline: 0px;
selection-background-color:rgb(0, 0, 0);
selection-color:rgb(0, 255, 255);
}

/* QFontComboBox */
QFontComboBox{
border:2px solid rgb(103, 103, 103);
border-radius: 5px;
padding: 1px 18px 1px 3px;
min-width: 6em;
}
QFontComboBox QAbstractItemView{
outline: 0px;
selection-background-color: rgb(90, 90, 90);
}


/* QLineEdit */
QLineEdit{
border:2px solid rgb(0, 0, 0);
border-top:none;
border-left:none;
border-right:none;
}
QLineEdit:hover{
border:2px solid qlineargradient(spread:pad, x1:0.012, y1:0.556818, x2:1, y2:0.573864, stop:0 rgba(110, 203, 205, 255), stop:0.965909 rgba(67, 91, 95, 255));
border-top:none;
border-left:none;
border-right:none;
}


/* QTextEdit */
QTextEdit{
border:1px solid rgb(0, 0, 0);
border-radius: 3px;
}
QTextEdit:hover{
border:1px solid rgb(0, 85, 255);
}

/* QPlainTextEdit */
QPlainTextEdit{
border:1px solid rgb(0, 0, 0);
border-radius: 4%;
background-color: rgb(66, 66, 66);
}
QPlainTextEdit:hover{
border:1px solid rgb(109, 109, 109);
}


/* QProgressBar */
QProgressBar {
border: 2px solid rgb(0, 0, 0);
border-radius: 5px;
}
QProgressBar::chunk {
border: 2px solid rgb(72, 72, 72);
width: 20px;
}
'''