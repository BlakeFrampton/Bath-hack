from PySide6.QtGui import QKeyEvent, QTextCursor
from PySide6.QtWidgets import QApplication, QTextEdit
import sys


class TypingBox(QTextEdit):

    def __init__(self, **_):
        super().__init__()
        self.setTextToType("Test")
        self.setOverwriteMode(True)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        textToType = self.textToType()
        pos = self.textCursor().position()
        if pos == len(textToType) - 1:
            self.textCursor().setPosition(0)  # Loop Back

        if e.text() == textToType[pos]:
            self.textCursor().setPosition(pos + 1)
            return super().keyPressEvent(e)

    def insertFromMimeData(self, _) -> None:
        pass  # Disable Pasting

    def textToType(self) -> str:
        return self.toPlainText()

    def setTextToType(self, message: str) -> None:
        return self.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingBox()
    window.show()
    sys.exit(app.exec())
