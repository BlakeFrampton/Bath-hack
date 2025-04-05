from PySide6.QtGui import (QBrush, QColor, QFont, QKeyEvent,
                           QMouseEvent, QTextCharFormat, Qt)
from PySide6.QtWidgets import QApplication, QTextEdit
import textGenerator
import sys
from dotenv import load_dotenv


class TypingBox(QTextEdit):

    def __init__(self, word_count, generation_type, generation_type_content, end_type_func, **_):
        super().__init__()

        backgroundColour = "#282E78"
        self.setStyleSheet(f'background-color: {backgroundColour}')

        load_dotenv()
        self.streak = 0
        self.mistakes = 0
        self.correct = 0
        self.typed = ""
        #textToType = self.getText(word_count,
                                  #generation_type, generation_type_content)
        #self.setTextToType(textToType)
        self.setFont(QFont("Times", 50, QFont.Bold))
        self.setTextToType("""In ancient times, the invention of the catapult revolutionized warfare. This powerful siege engine could launch projectiles with incredible force, causing devastation to enemy fortifications. The sound of the catapult releasing was a loud noise that struck fear into the hearts of those under attack. Additionally, when the projectiles hit their target, clouds of smoke and dust would fill the air. The catapult's ability to hurl heavy objects over long distances made it a formidable weapon in countless battles throughout history.""")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mistakesOverride = False


        # timer
        self.end_type_func = end_type_func

        # set cursor to the start
        cursor = self.textCursor()
        cursor.setPosition(0)
        self.setTextCursor(cursor)

    def get_mistakes(self):
        return self.mistakes

    def get_text_to_type(self):
        return self._textToType

    def end_typing(self):
        # self.typed, self._textToType, self.correct, self.mistakes


        # call the function for when the typing is finished
        self.end_type_func()

    def set_font(self, font):
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
                if self._textToType[pos - 1] == " ":  # If pressed while on a
                    # space delete from space to start of previous word
                    startingSpace = True
                while startingSpace or (pos > 0 and
                                        self._textToType[pos - 1] != " "):
                    # Backspace until start of text or word
                    startingSpace = False
                    self.backspace(cursor, pos, format)
                    pos = cursor.position()
            elif e.key() == Qt.Key_Backtab:  # Shift + tab
                self.reset()
            else:
                self.mistakes += 1
                self.streak = 0
                format.setForeground(QBrush(QColor("red")))
                cursor.deleteChar()
                self.typed += e.text()
                cursor.setCharFormat(format)
                if self._textToType[pos] == " ":
                    cursor.insertText("_")
                else:
                    cursor.insertText(self._textToType[pos])
                cursor.setPosition(pos + 1)
                pos += 1
        except TypeError:
            pass

        if pos == len(self._textToType):
            cursor.setPosition(0)  # Loop Back
            self.setTextCursor(cursor)
            self.end_typing()
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

    def getText(self, word_count, generation_type, generation_type_content):
        difficultWords = ["cappuccino", "spring", "crisp", "establishment"]
        if generation_type == "theme":
            return textGenerator.getTextFromTheme(generation_type_content,
                                                  difficultWords, word_count)
        elif generation_type == "code":
            return textGenerator.getTextFromCode(generation_type_content,
                                                 difficultWords, word_count)
        elif generation_type == "notes":
            return textGenerator.getTextFromNotes(generation_type_content,
                                                  difficultWords, word_count)
        else:
            print("uh oh, that's not a valid generation type. What's going on?")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingBox()
    window.show()
    sys.exit(app.exec())
