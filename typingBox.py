from PySide6.QtGui import (QBrush, QColor, QFont, QKeyEvent,
                           QMouseEvent, QTextCharFormat, Qt)
from PySide6.QtWidgets import QApplication, QTextEdit, QLabel
from PySide6.QtCore import QTimer
import textGenerator
import sys
import os
from dotenv import load_dotenv

# by default, the text challenge will close after 5 minutes
class Timer:
    def __init__(self, runtime_seconds=300, parent=None, timeout=None, restart_on_timeout=False, position=(0, 0), dimensions=(200, 50)):
        self.timeout_function = timeout
        self.runtime_seconds = runtime_seconds
        total_minutes = self.runtime_seconds // 60
        total_seconds = self.runtime_seconds % 60

        # Create the label to display the time
        self.timer_label = QLabel(f"00:00 / {total_minutes:02}:{total_seconds:02}", parent)
        self.timer_label.setAlignment(Qt.AlignHCenter)
        self.timer_label.setStyleSheet("font-size: 24px;")
        self.timer_label.setGeometry(position[0], position[1], dimensions[0], dimensions[1])

        # Create a QTimer that updates the label every second
        self.timer = QTimer(parent)
        self.timer.timeout.connect(self.update_timer)  # connect the timeout signal to our update function
        self.timer.start(1000)  # 1000 milliseconds = 1 second

        self.elapsed_time = 0
        self.restart_on_timeout = restart_on_timeout

        self.paused = False

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def restart(self):
        total_minutes = self.runtime_seconds // 60
        total_seconds = self.runtime_seconds % 60

        self.timer.start(1000)  # 1000 milliseconds = 1 second

        self.elapsed_time = 0
        self.timer_label.setText(f"00:00 / {total_minutes:02}:{total_seconds:02}")

    def update_timer(self):
        total_minutes = self.runtime_seconds // 60
        total_seconds = self.runtime_seconds % 60

        if self.elapsed_time < self.runtime_seconds and not self.paused:
            self.elapsed_time += 1

            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60

            self.timer_label.setText(f"{minutes:02}:{seconds:02} / {total_minutes:02}:{total_seconds:02}")  # Format as MM:SS
            # check for the timer ending
            if self.elapsed_time >= self.runtime_seconds:
                self.timer_label.setText(f"{total_minutes:02}:{total_seconds:02} / {total_minutes:02}:{total_seconds:02}")  # Format as MM:SS
                self.timeout()

    def timeout(self):
        self.timeout_function()

        if self.restart_on_timeout:
            self.restart()


class TypingBox(QTextEdit):

    def __init__(self, timeout_func, word_count, generation_type, generation_type_content, **_):
        super().__init__()

        backgroundColour = "#282E78"
        self.setStyleSheet(f'background-color: {backgroundColour}')

        load_dotenv()
        self.setFont(QFont("Times", 18, QFont.Bold))
        self.streak = 0
        self.mistakes = 0
        self.correct = 0
        self.typed = ""
        textToType = self.getText(word_count, generation_type, generation_type_content)
        self.setTextToType(textToType)
        self.setFont(QFont("Times", 50, QFont.Bold))
        # self.setTextToType("""In ancient times, the invention of the catapult revolutionized warfare. This powerful siege engine could launch projectiles with incredible force, causing devastation to enemy fortifications. The sound of the catapult releasing was a loud noise that struck fear into the hearts of those under attack. Additionally, when the projectiles hit their target, clouds of smoke and dust would fill the air. The catapult's ability to hurl heavy objects over long distances made it a formidable weapon in countless battles throughout history.""")
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

        self.scroll()
        

        try:
            if e.text() == self._textToType[pos]: # If input is correct
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

    def scroll(self):
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
            return textGenerator.getTextFromTheme(generation_type_content, difficultWords, word_count)
        elif generation_type == "code":
            return textGenerator.getTextFromCode(generation_type_content, difficultWords, word_count)
        elif generation_type == "notes":
            return textGenerator.getTextFromNotes(generation_type_content, difficultWords, word_count)
        else:
            print("uh oh, that's not a valid generation type. What's going on?")


def finishedTest(typed: str, target: str, correct: int, mistakes: int):
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingBox()
    window.show()
    sys.exit(app.exec())
