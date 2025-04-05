from PySide6.QtGui import (QBrush, QColor, QFont, QKeyEvent,
                           QMouseEvent, QTextCharFormat)
from PySide6.QtWidgets import QApplication, QTextEdit
from textGenerator import getTextToType
import sys
import os
from dotenv import load_dotenv


class TypingBox(QTextEdit):

    def __init__(self, **_):
        super().__init__()

        load_dotenv()
        self.setFont(QFont("Times", 18, QFont.Bold))
        self.streak = 0
        self.mistake = 0
        self.correct = 0
        self.setTextToType("Multiple test words")
        # textToType = self.getText()
        # self.setTextToType(textToType)
        self.setOverwriteMode(True)
        self.mistakesOverride = False


    def keyPressEvent(self, e: QKeyEvent) -> None:
        cursor = self.textCursor()
        pos = cursor.position()
        format = QTextCharFormat()

        print("streak: ", self.streak)
        if e.text() == self._textToType[pos]:
            format.setForeground(QBrush(QColor("green")))
            cursor.deleteChar()
            cursor.setCharFormat(format)
            cursor.insertText(e.text())
            cursor.setPosition(pos + 1)
            pos += 1
            self.correct += 1
            self.streak += 1
        elif ord(e.text()) == 8:  # Backspace
            if pos > 0:
                self.backspace(cursor, pos, format, e)
        elif ord(e.text()) == 127: # Ctrl-backspace
            startingSpace = False
            if self._textToType[pos - 1] == " ": # If pressed while on a space, delete from space to start of previous word
                startingSpace = True
            while startingSpace or (pos > 0 and self._textToType[pos - 1] != " "): # Backspace until start of text or word
                startingSpace = False
                self.backspace(cursor, pos, format, e)
                pos = cursor.position()
        else:
            print((e.text().isprintable()))
            self.mistake += 1
            self.streak = 0
            format.setForeground(QBrush(QColor("red")))
            cursor.deleteChar()
            cursor.setCharFormat(format)
            cursor.insertText(self._textToType[pos])
            cursor.setPosition(pos + 1)
            pos += 1

        if pos == len(self._textToType):
            cursor.setPosition(0)  # Loop Back
            self.setTextCursor(cursor)
            finishedTest(self.toPlainText(), self._textToType, self.correct, self.mistakes)
            self.streak = 0
            self.correct = 0
            self.mistakes = 0

    def backspace(self, cursor, pos, format, e):
        indx = (pos - 1) % len(self._textToType)
        print(indx)
        cursor.setPosition(indx)
        cursor.deleteChar()
        cursor.setCharFormat(format)
        if self.mistakesOverride:
            cursor.insertText(e.text())
        else:
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

    def getText(self):
        targetLength = 50
        theme = "coffee"
        difficultWords = ["cappuccino", "spring", "crisp", "establishment"]
        return getTextToType(theme, difficultWords, targetLength, True, os.environ.get("OPENAI_API_KEY"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingBox()
    window.show()
    sys.exit(app.exec())
