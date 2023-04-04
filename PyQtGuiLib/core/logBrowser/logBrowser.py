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


# 日志缓存
class LogCache(QObject):
    finish = Signal()

    def __init__(self):
        super().__init__()
        self.__logs = {
            "logs":[],
            "max":2,
            "value":0
        }

    def isEmpty(self)->bool:
        return False if self.__logs["logs"] else True

    def allLogs(self)->list:
        return self.__logs["logs"]

    def setMaxValue(self,v:int):
        self.__logs["max"] = v

    def pushLog(self,log:str):
        self.__logs["logs"].append(log)
        self.addValue()
        '''
            当缓存的日志到达最大值,会触发一个信号,通知需要同步到本地文本/服务器,
        '''
        if self.isMax():
            self.finish.emit()

    def isMax(self) -> bool:
        return True if self.value() == self.maxValue() else False

    def addValue(self):
        self.__logs["value"]+=1

    def resetLog(self):
        self.__logs["logs"].clear()
        self.__logs["value"] = 0

    def maxValue(self)->int:
        return self.__logs["max"]

    def value(self)->int:
        return self.__logs["value"]



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
        self.__logs = LogCache()
        self.__mutex = QMutex()

        # 本地日志路径
        self.__localLogPath = "."
        self.myEvents()

    def setMemoryLogMax(self,v:int):
        self.__logs.setMaxValue(v)

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
        self.__logs.pushLog(log+"\n")
        super().append(log)

    # 将日志一次性存入本地
    def saveLocalLog(self):
        if not self.__logs.isEmpty():
            self.__mutex.lock()  # 保证多线程的安全
            with open(self.localLogPath(),"a+") as f:
                f.write("".join(self.__logs.allLogs()))
            self.__logs.resetLog() # 这里需要调用一下重置
            self.__mutex.unlock()

    def closeEvent(self, a) -> None:
        self.saveLocalLog()
        super().closeEvent(a)

    def myEvents(self):
        self.__logs.finish.connect(lambda :self.saveLocalLog())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = LogBrowser()
    win.show()
    win.setLocalLogPath(r"D:\code\PyQtGuiLib\PyQtGuiLib\core\logBrowser\test.log")


    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())

