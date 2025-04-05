from PySide6.QtGui import (QBrush, QColor, QFont, QKeyEvent,
                           QMouseEvent, QTextCharFormat)
from PySide6.QtWidgets import QApplication, QTextEdit
import sys


class TypingBox(QTextEdit):

    def __init__(self, **_):
        super().__init__()
        self.setFont(QFont("Times", 50, QFont.Bold))
        self.setTextToType("Test")
        self.setOverwriteMode(True)
        self.mistakesOverride = False

    def mousePressEvent(self, _: QMouseEvent, /) -> None:
        pass

    def keyPressEvent(self, e: QKeyEvent) -> None:
        cursor = self.textCursor()
        pos = cursor.position()
        format = QTextCharFormat()
        mistake = 0
        correct = 0

        if e.text() == self._textToType[pos]:
            format.setForeground(QBrush(QColor("green")))
            cursor.deleteChar()
            cursor.setCharFormat(format)
            cursor.insertText(e.text())
            cursor.setPosition(pos + 1)
            pos += 1
            correct += 1
        elif ord(e.text()) == 8:  # Backspace
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
        else:
            print((e.text().isprintable()))
            mistake += 1
            format.setForeground(QBrush(QColor("red")))
            cursor.deleteChar()
            cursor.setCharFormat(format)
            cursor.insertText(self._textToType[pos])
            cursor.setPosition(pos + 1)
            pos += 1

        if pos == len(self._textToType):
            cursor.setPosition(0)  # Loop Back
            self.setTextCursor(cursor)
            finishedTest(self.toPlainText(), self._textToType)

    def insertFromMimeData(self, _) -> None:
        pass  # Disable Pasting

    def textToType(self) -> str:
        return self.toPlainText()

    def setTextToType(self, message: str) -> None:
        self._textToType = message
        return self.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingBox()
    window.show()
    sys.exit(app.exec())
