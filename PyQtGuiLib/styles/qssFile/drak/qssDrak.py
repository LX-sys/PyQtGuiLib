# -*- coding:utf-8 -*-
# @time:2023/3/2914:11
# @author:LX
# @file:qssDrak.py
# @software:PyCharm

#
Drak ='''
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

QTableView{
outline: 0px;
background-color: rgb(0, 0, 0);
}
QTableView QHeaderView{
background-color: rgb(0, 0, 0);
color:rgb(85, 255, 127);
}
QTableView QHeaderView::section{
}
QTableView QTableCornerButton::section{
background-color: rgb(0, 0, 0);
color: rgb(255, 255, 0);
}
QTableView::indicator:checked{
background-color: rgb(255, 255, 127);
}
QTableView::item{
border:1px solid gray;
border-left:none;
border-top:none;
}
QTableView::item:hover{
background-color: rgb(86, 86, 86);
}


'''
