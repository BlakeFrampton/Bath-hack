from PySide6.QtGui import (QBrush, QColor, QFont, QKeyEvent,
                           QMouseEvent, QTextCharFormat, Qt)
from PySide6.QtWidgets import QApplication, QTextEdit
import textGenerator
import sys
from dotenv import load_dotenv


class TypingBox(QTextEdit):

    def __init__(self, end_type_func, timer, word_count=1, generation_type="theme", generation_type_content="computer science hackathon", use_text="", key_function=None, **_):
        super().__init__()

        backgroundColour = "#5475A0"
        self.setStyleSheet(f'background-color: {backgroundColour}')
        self.defaultFontColour = "#A7F1CE"
        self.setTextColor(QColor(self.defaultFontColour))  #Default font color

        load_dotenv()
        self.streak = 0
        self.mistakes = 0
        self.correct = 0
        self.typed = ""

        if use_text == "":
            #textToType = self.getText(word_count,
                                      #generation_type, generation_type_content)
            #self.setTextToType(textToType)
            pass
        else:
            self.setTextToType(use_text)
        self.setFont(QFont("Times", 50, QFont.Bold))
        # self.setTextToType("""In ancient times, the invention of the catapult revolutionized warfare. This powerful siege engine could launch projectiles with incredible force, causing devastation to enemy fortifications. The sound of the catapult releasing was a loud noise that struck fear into the hearts of those under attack. Additionally, when the projectiles hit their target, clouds of smoke and dust would fill the air. The catapult's ability to hurl heavy objects over long distances made it a formidable weapon in countless battles throughout history.""")
        # self.setTextToType("Shorter text")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mistakesOverride = False

        #Creating arrays for difficult words 
        self.difficultWords = []
        self.difficultsScore = []

        # key function - activated whenever a key is pressed
        self.key_function = key_function

        # timer
        self.end_type_func = end_type_func
        self.timer = timer

        # set cursor to the start
        cursor = self.textCursor()
        cursor.setPosition(0)
        self.setTextCursor(cursor)

    def get_mistakes(self):
        return self.mistakes

    def get_text_to_type(self):
        return self._textToType

    def get_correct(self):
        return self.correct

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
        while True:
            self.backspace()
            if self.textCursor().position() <= 0:
                break

    def keyPressEvent(self, e: QKeyEvent) -> None:
        cursor = self.textCursor()
        format = QTextCharFormat()

        pos = cursor.position()

        self.smoothScroll()

        self.key_function()

        try:
            if e.text() == self._textToType[pos]:  # If input is correct
                correctFontColour = "#3EE094"
                format.setForeground(QBrush(QColor(correctFontColour)))
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
                    self.backspace()
            elif ord(e.text()) == 127:  # Ctrl-backspace
                startingSpace = False
                if self._textToType[pos - 1] == " ":  # If pressed while on a
                    # space delete from space to start of previous word
                    startingSpace = True
                while startingSpace or (pos > 0 and
                                        self._textToType[pos - 1] != " "):
                    # Backspace until start of text or word
                    startingSpace = False
                    self.backspace()
                    cursor = self.textCursor()
                    pos = cursor.position()
            elif e.key() == Qt.Key_Backtab:  # Shift + tab
                self.reset()
            else:
                #Code for when they typed a wrong character:
                current_word = ""
                #Getting characters before _textToType[pos] 
                prev = pos - 1
                startFound = False 
                start = ""
                while startFound != True:
                    if prev == 0: 
                        start =  self._textToType[prev] + start
                        startFound = True 
                    elif self._textToType[prev].isalpha():
                        prev = prev - 1
                        start = self._textToType[prev] + start
                    else:
                        startFound = True
                
                #Getting characters in the word after 
                post = pos + 1 
                endFound = False 
                end = ""
                while endFound != True:
                    if post == len(self._textToType) -1: 
                        end =  self._textToType[post] + end
                        endFound = True 
                    elif self._textToType[prev].isalpha():
                        post = post + 1
                        end = self._textToType[post] + end
                    else:
                        endFound = True
                
                current_word = start + self._textToType[pos] + end

                #Adding it to mistakes array and -3

                self.difficultWords.append(current_word)
                self.difficultsScore.append(-3)
                print(self.difficultWords)
                print(self.difficultsScore)

                

                self.mistakes += 1
                self.streak = 0
                incorrectFontColour = "#D9818A"
                format.setForeground(QBrush(QColor(incorrectFontColour)))
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
            self.end_typing()
            cursor.setPosition(0)  # Loop Back
            self.setTextCursor(cursor)
            self.streak = 0
            self.correct = 0
            self.mistakes = 0

    def smoothScroll(self):
        cursorPos = self.mapToGlobal(self.cursorRect().topLeft()).y()
        if (cursorPos > 0.6 * self.height()):
            scrollBar = self.verticalScrollBar()
            scrollBar.setValue(scrollBar.value() + 20)

    def backspace(self):
        cursor = self.textCursor()
        pos = cursor.position()
        format = QTextCharFormat()

        indx = (pos - 1) % len(self._textToType)
        cursor.setPosition(indx)
        cursor.deleteChar()
        self.typed = self.typed[:-1]
        # self.setTextColor(QColor(self.defaultFontColour)) #Default font color
        format.setForeground(QBrush(QColor(self.defaultFontColour)))
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
