from PySide6.QtGui import QBrush, QColor, QFont, QKeyEvent, QTextCharFormat
from PySide6.QtWidgets import QApplication, QTextEdit
import sys


class TypingBox(QTextEdit):

    def __init__(self, **_):
        super().__init__()
        self.setTextToType("Test")
        self.setOverwriteMode(True)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        cursor = self.textCursor()
        pos = cursor.position()
        format = QTextCharFormat()
        format.setFontWeight(QFont().bold())
        if pos == len(self._textToType) - 1:
            self.textCursor().setPosition(0)  # Loop Back

        if e.text() == self._textToType[pos]:
            format.setForeground(QBrush(QColor("green")))
            cursor.deleteChar()
            cursor.setCharFormat(format)
            cursor.insertText(e.text())
            cursor.setPosition(pos + 1)
        elif e.text() == "":
            pass
        else:
            format.setForeground(QBrush(QColor("red")))
            cursor.deleteChar()
            cursor.setCharFormat(format)
            cursor.insertText(e.text())
            cursor.setPosition(pos + 1)

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
