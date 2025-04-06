import sys
from PySide6.QtGui import QBrush, QFont, QIcon, QAction, QColor, QPixmap
from PySide6.QtWidgets import QMenu, QWidget, QToolBar, QApplication, QMainWindow, QPushButton, QDialog, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QInputDialog, QLineEdit
from PySide6.QtCore import Qt, QTimer, QSize

from typingBox import TypingBox
from Timer import Timer
from Animation import ConfettiOverlay, FireworkOverlay

default_button_bg = "4caf50"  # hex value


class SliderWindow(QDialog):
    def __init__(self, parent=None, value_range=(0, 100),
                 value=50, text="", onChanged=None, icon=None):
        super().__init__(parent)
        self.setWindowTitle(text)
        self.setFixedSize(250, 120)
        print("intit")

        self.parent_window = parent

        layout = QVBoxLayout(self)

        defaultFontColour = "#A7F1CE"
        self.setStyleSheet(f"color: {'000000'}; background-color: {default_button_bg}")
        # self.setTextColor(QColor(defaultFontColour))  #Default font color
        self.setWindowIcon(icon)

        self.text = text

        self.label = QLabel(text+": "+str(value))
        layout.addWidget(self.label)

        if onChanged is None:
            onChanged = lambda x: x
        self.onChanged = onChanged

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(value_range[0], value_range[1])
        self.slider.setValue(value)
        layout.addWidget(self.slider)

        self.slider.valueChanged.connect(self.change_value)

    def change_value(self, value):
        self.label.setText(self.text+": "+str(value))
        self.onChanged(value)


class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

    def reset(self):
        return

    def toggle_mistake_override(self):
        return


class MainWindow(QMainWindow):
    def __init__(self):
        self.backgroundColour = "#2E4057"
        super().__init__()
        self.setWindowTitle("Error 404")
        # self.setGeometry(100, 100, 800, 600)
        self.showFullScreen()  # makes the window fullscreen
        self.setStyleSheet(f'QMainWindow {{background: {self.backgroundColour}}}')

        # saves the current page
        self.timer = Timer(parent=self, runtime_seconds=30, position=(600, 0), timeout=self.timeout)
        self.timer.pause()
        self.timer.hide()

        self.current_widget_page = None

        self.enter_home()

        # settings
        self.volume = 50
        self.text_size = 15
        self.runtime = 30
        self.icon_size = 60  # pixels per side - square icons

        # text generation settings
        self.word_count = 50
        self.generation_type = "theme"
        self.generation_type_content = "typing"

        # menu bar
        self.create_menu()

        self.difficultWords = []

    def enter_typing(self):
        self.difficultWords = []
        # text = "Some text about catapults text"
        text = ""
        text_edit = TypingBox(
                              self.finish_typing,
                              self.timer,
                              self.word_count,
                              self.generation_type,
                              self.generation_type_content,
                              use_text=text,
                              key_function=self.timer.unpause
                              )
        text_edit.setStyleSheet("""margin: 100px 50px 100px 50px
            ; border-radius: 20px;
            border: 2px solid black;
            background-color: palette(base)""")
        self.setCentralWidget(text_edit)

        self.timer.show()
        self.timer.timeout_function = self.timeout
        self.timer.runtime_seconds = self.runtime  # one minute to get through the test
        self.timer.restart_on_timeout = False
        self.timer.restart()
        self.timer.pause()

        self.current_widget_page = text_edit
        QTimer.singleShot(0, text_edit.setFocus) #Focuses typing test after it has loaded

    def make_icon(self, path):
        pixmap = QPixmap(path).scaled(self.icon_size, self.icon_size)
        return QIcon(pixmap)

    def get_statistics(self):
        mistakes = self.current_widget_page.get_mistakes()
        correct = self.current_widget_page.get_correct()
        minutes_taken = self.timer.elapsed_time / 60
        total_typed = mistakes + correct

        accuracy = (1 - mistakes / total_typed) * 100
        accuracy = max(accuracy, 0)  # Ensure accuracy doesn't go below 0%
        final_accuracy = round(accuracy, 1)

        wpm = (correct / 6) * (final_accuracy / 100) / minutes_taken
        score = round(wpm)

        return round(final_accuracy, 2), round(wpm), round(score, 1)

    def finish_typing(self):
        self.timeout()

    def timeout(self):
        # calculate statistics
        accuracy, wpm, score = self.get_statistics()

        print("Final accuracy: " + str(accuracy))
        print("Final wpm: " + str(wpm))
        print("Final score: " + str(score))

        # update the difficult words
        new_difficult_words = self.current_widget_page.difficultWords.copy()
        self.difficultWords = list(set(self.difficultWords + new_difficult_words))

        print(self.difficultWords)

        # go back to the home screen
        self.enter_home(accuracy, wpm, score)

    def make_type_box_title(self, home_layout):
        self.timer.pause()
        self.timer.runtime_seconds = 0.5  # 0.5 seconds before it backspaces
        self.timer.restart_on_timeout = True
        self.timer.hide()

        title_text = TypingBox(None, self.timer, key_function=self.timer.restart, use_text="Typesmith")
        # title_text.setGeometry(0, 0, self.width(), 20)

        def timeout_func():
            if title_text.textCursor().position() > 0:
                title_text.backspace()

        self.timer.timeout_function = timeout_func
        self.timer.unpause()
        self.timer.restart()

        # confetti appears when you type the game name
        # confetti = ConfettiOverlay(self)
        confetti = FireworkOverlay(self)

        def complete_title():
            # confetti.start_confetti()
            confetti.start_firework(self.width() // 2, self.height() // 2)
            title_text.reset()

        title_text.end_type_func = complete_title

        title_text.setFont(QFont("Times", 100))
        title_text.setStyleSheet(f"color: white;background-color: {self.backgroundColour}")
        title_text.setAlignment(Qt.AlignCenter)

        home_layout.addWidget(title_text)

        # focus on the title widget once it has loaded
        QTimer.singleShot(0, title_text.setFocus)

    def make_data_display_boxes(self, home_layout, accuracy=None, wpm=None, score=None):
        if accuracy is None:
            accuracy = "100"
        if wpm is None:
            wpm = "N/A"
        if score is None:
            score = "N/A"

        accuracy_text = QLabel(str(accuracy)+"%", self)
        accuracy_text.setFont(QFont("Times", 50))
        accuracy_text.setAlignment(Qt.AlignCenter)

        wpm_text = QLabel(str(wpm)+" wpm", self)
        wpm_text.setFont(QFont("Times", 50))
        wpm_text.setAlignment(Qt.AlignCenter)

        score_text = QLabel("Score: "+str(score), self)
        score_text.setFont(QFont("Times", 50))
        score_text.setAlignment(Qt.AlignCenter)

        home_layout.addWidget(accuracy_text)
        home_layout.addWidget(wpm_text)
        home_layout.addWidget(score_text)

    def enter_home(self, accuracy=None, wpm=None, score=None):
        # home screen
        home_layout = QVBoxLayout()
        # title and data displays
        self.make_type_box_title(home_layout)
        self.make_data_display_boxes(home_layout, accuracy, wpm, score)

        # typing game
        typing_button = QPushButton("Typing Frenzy", self)
        typing_button.setFont(QFont("Times", 100))
        typing_button.setStyleSheet(f"color: white; background-color: '#3F5878'")
        typing_button.clicked.connect(self.enter_typing)
        home_layout.addWidget(typing_button)
        # create home screen
        home_screen = HomeWidget()  # basically a QWidget
        # , just with some extra functions
        home_screen.setLayout(home_layout)

        self.setCentralWidget(home_screen)
        self.current_widget_page = home_screen

    def set_volume(self, value):
        print("set volume to", value)
        self.volume = value

    def set_text_size(self, value):
        print("set text size to", value)
        self.text_size = value
        font = QFont("Times", value)

        self.current_widget_page.setFont(font)

    def set_word_count(self, value):
        print("set word count to ", value)
        self.word_count = value

    def restart(self):
        self.current_widget_page.reset()
        self.timer.restart()  # restart the timer as well
        print("restart?")

    def add_file_menu(self, menu_bar):
        # layout
        layout = QVBoxLayout()

        # add menu button
        file_menu_button = QPushButton(self.make_icon("assets/menu_icon.png"), "File", self)
        file_menu = QMenu()
        file_menu_button.setMenu(file_menu)
        layout.addWidget(file_menu_button)

        # menu_bar.addWidget(file_menu_button)

        # add menu actions
        restart_action = QAction(self.make_icon("assets/restart_icon.png"),
                                 "Restart", self)
        restart_action.triggered.connect(self.restart)
        file_menu.addAction(restart_action)

        exit_action = QAction(self.make_icon("assets/exit_icon.png"), "Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def show_volume(self):
        volume_icon = self.make_icon("assets/volume_icon.png")
        volume_window = SliderWindow(self, (1, 100),
                                     self.volume, "Volume", self.set_volume,
                                     volume_icon)
        volume_window.show()

    def show_text_size(self):
        font_icon = self.make_icon("assets/font_icon.png")
        text_window = SliderWindow(self, (10, 18), self.text_size,
                                   "Text Size", self.set_text_size,
                                   font_icon)
        text_window.show()
    
    def show_word_count(self):
        text_window = SliderWindow(self, (40, 200), self.word_count,
                                   "Word Count", self.set_word_count)
        text_window.show()

    def toggle_mistake_highlight(self):
        self.current_widget_page.toggle_mistake_override()

    def add_settings_menu(self, menu_bar):
        settings_menu = menu_bar.addMenu(self.make_icon("assets/settings_icon.png"),
                                         "Settings")

        volume_action = QAction(self.make_icon("assets/volume_icon"), "Volume", self)
        volume_action.triggered.connect(self.show_volume)
        settings_menu.addAction(volume_action)

        text_action = QAction(self.make_icon("assets/font_icon.png"), "Font Size", self)
        text_action.triggered.connect(self.show_text_size)
        settings_menu.addAction(text_action)

        word_count_action = QAction(self.make_icon("assets/word_count.png"),
                                    "Word Count", self)
        word_count_action.triggered.connect(self.show_word_count)
        settings_menu.addAction(word_count_action)

    def add_text_theme_menu(self, menu_bar):
        text_theme_menu = menu_bar.addMenu(self.make_icon("assets/generation_icon.png"),
                                           "Settings")

        def make_action(label):
            action = QAction(self.make_icon(f"assets/{label}_icon.png"), label.capitalize(), self)
            action.triggered.connect(lambda: self.set_theme_from_input(label))
            return action

        for label in ["theme", "code", "notes"]:
            text_theme_menu.addAction(make_action(label))

    def set_theme_from_input(self, style_type):
        self.style = style_type
        dialog = QInputDialog(self)
        dialog.setWindowTitle(f"Enter {style_type.capitalize()}")
        if style_type == "code":
            dialog.setLabelText("Enter your coding language:")
        else:
            dialog.setLabelText(f"Enter your {style_type}:")
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setTextEchoMode(QLineEdit.Normal)
        dialog.setWindowIcon(self.make_icon(f"assets/{style_type}_icon.png"))

        if dialog.exec():  # Show dialogue
            user_input = dialog.textValue()
            if user_input:
                print(f"{style_type.capitalize()} set to: {user_input}") 
                self.generation_type = style_type
                self.generation_type_content = user_input
            else:
                print(f"No {style_type} entered.")

    def add_base_menu_items(self, menu_bar):

        home_action = QAction(self.make_icon("assets/home_icon.png"), "Home", self)
        home_action.triggered.connect(self.enter_home)
        menu_bar.addAction(home_action)

        exit_action = QAction(self.make_icon("assets/exit_icon.png"), "Exit", self)
        exit_action.triggered.connect(self.close)
        menu_bar.addAction(exit_action)

        menu_bar.addSeparator()

        volume_action = QAction(self.make_icon("assets/volume_icon"), "Volume", self)
        volume_action.triggered.connect(self.show_volume)
        menu_bar.addAction(volume_action)

        text_action = QAction(self.make_icon("assets/font_icon.png"), "Font Size", self)
        text_action.triggered.connect(self.show_text_size)
        menu_bar.addAction(text_action)

    def add_special_actions(self, menu_bar):

        word_count_action = QAction(self.make_icon("assets/word_count_icon.png"),
                                    "Word Count", self)
        word_count_action.triggered.connect(self.show_word_count)
        menu_bar.addAction(word_count_action)

        menu_bar.addSeparator()

        def make_action(label1):
            action = QAction(self.make_icon(f"assets/{label1}_icon.png"), label1.capitalize(), self)
            action.triggered.connect(lambda: self.set_theme_from_input(label1))
            return action

        for label in ["theme", "code", "notes"]:
            menu_bar.addAction(make_action(label))


    def create_menu(self):
        # icon images are 100x100 pixils
        menu_bar = QToolBar("Main Toolbar")
        menu_bar.setIconSize(QSize(self.icon_size, self.icon_size))
        self.addToolBar(menu_bar)

        # menu_bar = self.menuBar()
        menu_bar.setStyleSheet(f"QMenuBar {{background:'#3F5878'}}; QMenuBar::item {{padding-left: 6px; padding-right: 6px; height: 60px;}}")
        # menu_bar.setFixedHeight(self.icon_size)

        self.add_base_menu_items(menu_bar)
        self.add_special_actions(menu_bar)
        # self.add_file_menu(menu_bar)
        # self.add_settings_menu(menu_bar)
        # self.add_text_theme_menu(menu_bar)

        # menu_bar.frameSize()
        # menu_bar.setBaseSize(QSize(self.icon_size, self.icon_size))

        # raise the timer to the top of the widget stack
        self.timer.timer_label.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MainWindow()
    editor.show()
    sys.exit(app.exec())
