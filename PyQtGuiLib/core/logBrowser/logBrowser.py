# -*- coding:utf-8 -*-
# @time:2023/3/2717:33
# @author:LX
# @file:logBrowser.py
# @software:PyCharm
import os
import time
from datetime import datetime as dt
from PyQtGuiLib.header import (
    QApplication,
    sys,
    PYQT_VERSIONS,
    QWidget,
    QTextBrowser,
    QThread,
    Signal,
    QObject,
    QScrollBar,
    QListWidget,
    QMutex
)
from PyQtGuiLib.core.logBrowser.logSizeTh import LogSizeTh
from PyQtGuiLib.core.logBrowser.loadLogTh import LoadLocalLog



TimeFormat = str





# 日志控件
class LogBrowser(QTextBrowser):
    Debug = "Debug"
    Info = "Info"
    Warning = "Warning"
    Error = "Error"
    Critical = "Critical"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.__timeFormat = "%Y-%m-%d %H:%M:%S"
        self._start_slider_value = 0
        self._next_slider_value = 0

        '''
            将日志暂时存储在内存中,避免过渡读取磁盘
        '''
        self.__logs = []
        self.__logMax = 300
        self.__culog = 0
        self.__mutex = QMutex()

        # 本地日志路径
        self.__localLogPath = "."

        # self.ll = LoadLocalLog(limit=1000)
        # self.ll.loaded.connect(self.test)
        # self.ll.finish.connect(self.init_slider_event)
        # self.ll.start()
        # self.verticalScrollBar().sliderMoved.connect(self.info)

    def setMemoryLogMax(self,max_num):
        self.__logMax = max_num

    def setLocalLogPath(self,path):
        self.__localLogPath = path

    def localLogPath(self) -> str:
        return self.__localLogPath

    # 在第一次加载日志后,初始化滚动条
    def init_slider_event(self):
        self.verticalScrollBar().setValue(0)
        self._start_slider_value = self.verticalScrollBar().value()
        self._next_slider_value = self.verticalScrollBar().value()

    def sliderValue(self) -> int:
        return self.verticalScrollBar().value()

    def wheelEvent(self, *args, **kwargs):
        self._next_slider_value = self.sliderValue()
        print(self._start_slider_value,self._next_slider_value)
        if self._next_slider_value > self._start_slider_value:
            print("向下")
        elif self._next_slider_value < self._start_slider_value:
            print("向上")

        self._start_slider_value = self._next_slider_value
        super().wheelEvent(*args,**kwargs)

    def info(self,i):
        print(i)

    def test(self,info):
        self.append(info,LogBrowser.Debug)

    def setTimeFormat(self,format:TimeFormat):
        self.__timeFormat = format

    def timeFormat(self) -> TimeFormat:
        return self.__timeFormat

    def append(self, p_str,mode="Info"):
        '''
            每次写入的输入会存入内存,当然数据到达一定的量的时候,
            才会写入本地,避免过渡读取磁盘

        :param p_str:
        :param mode:
        :return:
        '''
        for_time = dt.strftime(dt.now(),self.timeFormat())
        log = "{mode} [{time}] > {info}".format(mode=mode,
                                            time=for_time,
                                            info=p_str.replace("\n",""))
        self.__logs.append(log+"\n")
        self.__culog += 1
        if self.__culog >= self.__logMax:
            self.saveLocalLog()
            self.__culog = 0
        super().append(log)

    # 将日志一次性存入本地
    def saveLocalLog(self):
        self.__mutex.lock() # 保证多线程的安全
        with open(self.localLogPath(),"a+") as f:
            f.write("".join(self.__logs))
        self.__mutex.unlock()

    def closeEvent(self, a) -> None:
        self.saveLog()
        super().closeEvent(a)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = LogBrowser()
    win.show()
    win.setLocalLogPath(r"D:\code\PyQtGuiLib\PyQtGuiLib\core\logBrowser\test.log")



    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())

