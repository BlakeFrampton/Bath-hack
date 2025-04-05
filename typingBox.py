from PySide6.QtGui import (QBrush, QColor, QFont, QKeyEvent,
                           QMouseEvent, QTextCharFormat, Qt)
from PySide6.QtWidgets import QApplication, QTextEdit
from Timer import Timer
import textGenerator
import sys
import os
from dotenv import load_dotenv

class TypingBox(QTextEdit):

    def __init__(self, timeout_func, **_):
        super().__init__()

        backgroundColour = "#282E78"
        self.setStyleSheet(f'background-color: {backgroundColour}')

        load_dotenv()
        self.streak = 0
        self.mistakes = 0
        self.correct = 0
        self.typed = ""
        # textToType = self.getText()
        # self.setTextToType(textToType)
        self.setFont(QFont("Times", 50, QFont.Bold))
        self.setTextToType("""In ancient times, the invention of the catapult revolutionized warfare. This powerful siege engine could launch projectiles with incredible force, causing devastation to enemy fortifications. The sound of the catapult releasing was a loud noise that struck fear into the hearts of those under attack. Additionally, when the projectiles hit their target, clouds of smoke and dust would fill the air. The catapult's ability to hurl heavy objects over long distances made it a formidable weapon in countless battles throughout history.""")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setOverwriteMode(True)
        self.mistakesOverride = False

        # timer
        self.timer = Timer(10, self, timeout_func, False, (200, 0))

    def set_font(self, font):
        self.timer.setFont(font)
        self.setFont(font)

    def toggle_mistake_override(self):
        self.set_mistake_override(not self.mistakesOverride)

    def set_mistake_override(self, value):
        self.mistakesOverride = value

    def reset(self):
        self.streak = 0
        self.mistakes = 0
        self.correct = 0

        # remove the current text
        format = QTextCharFormat()
        format.setForeground(QBrush(QColor("white")))
        cursor = self.textCursor()
        while cursor.position() > 0:
            self.backspace(cursor, cursor.position(), format)

        # reset the timer
        self.timer.restart()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        cursor = self.textCursor()
        format = QTextCharFormat()

        pos = cursor.position()

        self.smoothScroll()

        try:
            if e.text() == self._textToType[pos]:  # If input is correct
                fontColour = "#28785e"
                format.setForeground(QBrush(QColor(fontColour)))
                cursor.deleteChar()
                self.typed += e.text()
                cursor.setCharFormat(format)
                cursor.insertText(e.text())
                cursor.setPosition(pos + 1)
                pos += 1
                self.correct += 1
                self.streak += 1
            elif ord(e.text()) == 8:  # Backspace
                if pos > 0:
                    self.backspace(cursor, pos, format)
            elif ord(e.text()) == 127:  # Ctrl-backspace
                startingSpace = False
                if self._textToType[pos - 1] == " ":  # If pressed while on a space
                    # delete from space to start of previous word
                    startingSpace = True
                while startingSpace or (pos > 0 and self._textToType[pos - 1] != " "):
                    # Backspace until start of text or word
                    startingSpace = False
                    self.backspace(cursor, pos, format)
                    pos = cursor.position()
            elif e.key() == Qt.Key_Backtab: #Shift + tab
                self.reset()
            else:
                self.mistakes += 1
                self.streak = 0
                format.setForeground(QBrush(QColor("red")))
                cursor.deleteChar()
                self.typed += e.text()
                cursor.setCharFormat(format)
                cursor.insertText(self._textToType[pos])
                cursor.setPosition(pos + 1)
                pos += 1
        except TypeError:
            pass

        if pos == len(self._textToType):
            cursor.setPosition(0)  # Loop Back
            self.setTextCursor(cursor)
            finishedTest(self.typed, self._textToType, self.correct, self.mistakes)
            self.streak = 0
            self.correct = 0
            self.mistakes = 0

    def smoothScroll(self):
        cursorPos = self.mapToGlobal(self.cursorRect().topLeft()).y()
        if (cursorPos > 0.6 * self.height()):
            scrollBar = self.verticalScrollBar()
            scrollBar.setValue(scrollBar.value() + 20)

    def backspace(self, cursor, pos, format):
        indx = (pos - 1) % len(self._textToType)
        cursor.setPosition(indx)
        cursor.deleteChar()
        self.typed = self.typed[:-1]
        cursor.setCharFormat(format)
        cursor.insertText(self._textToType[indx])
        cursor.setPosition(indx)
        self.setTextCursor(cursor)

    def insertFromMimeData(self, _) -> None:
        pass  # Disable Pasting

    def textToType(self) -> str:
        return self.toPlainText()

    def setTextToType(self, message: str) -> None:
        self._textToType = message
        return self.setText(message)
    
    def mousePressEvent(self, _: QMouseEvent, /) -> None:
        pass

    def getText(self):
        targetLength = 200
        difficultWords = ["cappuccino", "spring", "crisp", "establishment"]
        return getTextToType(theme, difficultWords, targetLength,
                             True, os.environ.get("OPENAI_API_KEY"))


def finishedTest(typed: str, target: str, correct: int, mistakes: int):
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingBox()
    window.show()
    sys.exit(app.exec())
