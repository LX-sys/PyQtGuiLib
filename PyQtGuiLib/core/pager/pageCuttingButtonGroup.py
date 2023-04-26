from PyQtGuiLib.header import (
    QWidget,
    QPushButton,
    QButtonGroup,
    QHBoxLayout,
    QStackedWidget,
    QLayout,
    QLabel,
    QVBoxLayout,
    qt,
    QSize,
    QCursor,
    Signal,
    QSizePolicy
)
from typing import List


class PageCuttingButtonGroup(QWidget):
    currentPageChanged = Signal(int)

    def __init__(self, totalPages, buttonCount, *args, **kwargs):
        super(PageCuttingButtonGroup, self).__init__(*args, **kwargs)
        self._totalPages = totalPages
        if self._totalPages < 2:
            return

        self._buttonCount = max(5, buttonCount)
        self._currentPageIndex = -1
        self.__initializeWidget()
        self.setCurrentPageIndex(0)

        self.__personalInformation = {
            "author":"PyQt5学习爱好群-讨厌自己",
            "contribution time":"2023.4.25"
        }

        self.defaultStyle()

    def author(self) -> str:
        return self.__personalInformation

    def bingStackedWidget(self,st:QStackedWidget):
        self.currentPageChanged.connect(st.setCurrentIndex)

    def setSpacing(self, a0: int) -> None:
        if self._totalPages < 2:
            return

        self._hBox.setSpacing(a0)

    def setCurrentPageButtonFixedSize(self, size: QSize) -> None:
        if self._totalPages < 2:
            return

        for i, button in enumerate(self._group.buttons()):
            button.setFixedSize(size)

    def setPreviousNextPageButtonFixedSize(self, size: QSize) -> None:
        if self._totalPages < 2:
            return

        self._previousPageButton.setFixedSize(size)
        self._nextPageButton.setFixedSize(size)

    def currentPageIndex(self) -> int:
        return self._currentPageIndex

    def setCurrentPageIndex(self, index: int) -> None:
        if self._totalPages < 2 or self._totalPages <= index or index < 0:
            return
        self.__clickedOnTheJudgmentButton(currentPageIndex=index)

    def __previousOrNextPageButtonClicked(self, text):
        if text == "下一页" and self._currentPageIndex < self._totalPages - 1:
            currentPageIndex = self._currentPageIndex + 1
        elif text == "上一页" and self._currentPageIndex > 0:
            currentPageIndex = self._currentPageIndex - 1
        else:
            return
        self.__clickedOnTheJudgmentButton(currentPageIndex=currentPageIndex)

    @staticmethod
    def assignValues(middleValue, lst: List[QPushButton], pos: list):
        length = len(lst)
        middleIndex = length // 2
        lst[middleIndex].setText(str(middleValue))
        for i in range(1, middleIndex):
            lst[i].setText("...") if i in pos else lst[i].setText(str(middleValue - (middleIndex - i)))
        for i in range(middleIndex + 1, length - 1):
            lst[i].setText("...") if i in pos else lst[i].setText(str(middleValue + (i - middleIndex)))

        return lst

    def __clickedOnTheJudgmentButton(self, currentPageIndex: int):
        if currentPageIndex == self._currentPageIndex:
            return

        centre = self._buttonCount // 2 + 1
        if self._totalPages > self._buttonCount:
            if currentPageIndex < centre:
                self.assignValues(middleValue=centre, lst=self._group.buttons(), pos=[self._buttonCount - 2])
            elif centre <= currentPageIndex < self._totalPages - centre:
                self.assignValues(middleValue=currentPageIndex + 1, lst=self._group.buttons(),
                                  pos=[1, self._buttonCount - 2])
            elif currentPageIndex >= self._totalPages - centre:
                self.assignValues(middleValue=self._totalPages - centre + 1, lst=self._group.buttons(), pos=[1])
        self._currentPageIndex = currentPageIndex
        self.currentPageChanged.emit(currentPageIndex)

        for i, button in enumerate(self._group.buttons()):
            if button.text() == str(currentPageIndex + 1):
                button.setCheckable(True)
                button.setChecked(True)
            else:
                button.setCheckable(False)
                button.update()
            button.setEnabled(False) if button.text() == "..." else button.setEnabled(True)

        self.__setButtonEnabled(self._previousPageButton, False) if self._currentPageIndex == 0 \
            else self.__setButtonEnabled(self._previousPageButton, True)
        self.__setButtonEnabled(self._nextPageButton, False) if self._currentPageIndex == self._totalPages - 1 \
            else self.__setButtonEnabled(self._nextPageButton, True)

    def __initializeWidget(self):
        self._group = QButtonGroup(parent=self)
        self._group.buttonClicked.connect(
            lambda button: self.__clickedOnTheJudgmentButton(currentPageIndex=int(button.text()) - 1))
        self._hBox = QHBoxLayout(self)
        self._hBox.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self._previousPageButton = self.__registerButton("上一页", False)
        self._previousPageButton.clicked.connect(lambda: self.__previousOrNextPageButtonClicked(text="上一页"))
        self._nextPageButton = self.__registerButton("下一页", False)
        self._nextPageButton.clicked.connect(lambda: self.__previousOrNextPageButtonClicked(text="下一页"))
        self._hBox.addWidget(self._previousPageButton)
        if self._totalPages <= self._buttonCount:
            for i in range(self._totalPages):
                button = self.__registerButton("{}".format(i+1), True)
                self._hBox.addWidget(button)
                self._group.addButton(button, id=i)
        else:
            for i in range(self._buttonCount):
                if i == self._buttonCount - 1:
                    button = self.__registerButton(str(self._totalPages), True)
                else:
                    button = self.__registerButton(str(i + 1), True)
                self._hBox.addWidget(button)
                self._group.addButton(button, id=i)
        self._hBox.addWidget(self._nextPageButton)

    def __setButtonEnabled(self, button: QPushButton, enabled: bool):
        if enabled:
            button.setCursor(QCursor(qt.PointingHandCursor))
            button.setStyleSheet("")
        else:
            button.setCursor(QCursor(qt.ForbiddenCursor))
            button.setStyleSheet("""
                QPushButton{
                    border: 1px solid rgba(241, 242, 243, 255);
                    color: rgb(203, 206, 210);
                }
                QPushButton:hover{
                    background-color:none;
                }
            """)

        return button

    def __registerButton(self, text: str, checkAble: bool):
        button = QPushButton(text, parent=self)
        button.setCheckable(True) if checkAble else None
        button.setCursor(QCursor(qt.PointingHandCursor))
        button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        return button

    def defaultStyle(self):
        self.setStyleSheet('''
            QWidget{
                background-color: transparent;
            }
            QPushButton{
                font: 14px "黑体";
                color: rgba(84, 87, 87, 255);
                border:1px solid rgba(227, 229, 231, 255);
                border-radius:6px;
            }
            QPushButton:hover{
                background-color: rgba(227, 229, 231, 255);
            }
            QPushButton:checked{
                background-color: rgba(255, 102, 153, 255);
                color: rgba(255, 255, 255, 255);
                border:1px solid rgba(255, 102, 153, 255);
            }
            QPushButton:disabled{
                border:none;
                background-color:transparent;
            }
        ''')