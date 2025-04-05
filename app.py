import sys
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QDialog, QSlider, QVBoxLayout, QLabel, QInputDialog, QLineEdit
from PySide6.QtCore import Qt

from typingBox import TypingBox
from Timer import Timer

default_button_bg = "4caf50"  # hex value


class SliderWindow(QDialog):
    def __init__(self, parent=None, value_range=(0, 100),
                 value=50, text="", onChanged=None):
        super().__init__(parent)
        self.setWindowTitle(text)
        self.setFixedSize(250, 120)

        self.parent_window = parent

        layout = QVBoxLayout(self)

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
        backgroundColour = "#080E4B"
        super().__init__()
        self.setWindowTitle("Error 404")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f'QMainWindow {{background: {backgroundColour}}}')

        # saves the current page
        self.timer = Timer(parent=self, runtime_seconds=30, position=(200, 0), timeout=self.timeout)
        self.timer.pause()
        self.timer.hide()

        self.current_widget_page = None
        self.enter_home()

        # settings
        self.volume = 50
        self.text_size = 15

        # text generation settings
        self.word_count = 50
        self.generation_type = "theme"
        self.generation_type_content = "typing"

        # menu bar
        self.create_menu()

    def enter_typing(self):
        text_edit = TypingBox(
                              self.word_count,
                              self.generation_type,
                              self.generation_type_content,
                              self.timeout)
        self.setCentralWidget(text_edit)

        self.timer.show()
        self.timer.unpause()
        self.timer.restart()

        self.current_widget_page = text_edit

    def get_statistics(self):
        mistakes = self.current_widget_page.get_mistakes()
        text_to_type = self.current_widget_page.get_text_to_type()
        num_chars = len(text_to_type)
        minutes_taken = self.timer.elapsed_time / 60

        accuracy = (1 - mistakes / num_chars) * 100
        accuracy = max(accuracy, 0)  # Ensure accuracy doesn't go below 0%
        final_accuracy = round(accuracy, 1)

        wpm = (num_chars / 6) * (accuracy / 100) / minutes_taken
        final_wpm = round(wpm)

        print("Final accuracy: " + str(final_accuracy))
        print("Final wpm: " + str(final_wpm))

        return final_accuracy, final_wpm

    def timeout(self):
        # calculate statistics
        accuracy, wpm = self.get_statistics()

        # go back to the home screen
        self.enter_home()
        print("timeout")

    def enter_home(self):
        # home screen
        home_layout = QVBoxLayout()
        # title
        title_text = QLabel("Typesmith", self)
        title_text.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(title_text)
        # typing game
        typing_button = QPushButton("Typing Frenzy", self)
        typing_button.clicked.connect(self.enter_typing)
        home_layout.addWidget(typing_button)
        # create home screen
        home_screen = HomeWidget()  # basically a QWidget
        # , just with some extra functions
        home_screen.setLayout(home_layout)

        self.setCentralWidget(home_screen)
        self.current_widget_page = home_screen

        self.timer.pause()
        self.timer.hide()

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
        print("restart?")

    def add_file_menu(self, menu_bar):
        file_menu = menu_bar.addMenu(QIcon("assets/menu_icon.png"), "File")

        restart_action = QAction(QIcon("assets/restart_icon.png"),
                                 "Restart", self)
        restart_action.triggered.connect(self.restart)
        file_menu.addAction(restart_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def show_volume(self):
        volume_window = SliderWindow(self, (1, 100),
                                     self.volume, "Volume", self.set_volume)
        volume_window.show()

    def show_text_size(self):
        text_window = SliderWindow(self, (10, 18), self.text_size,
                                   "Text Size", self.set_text_size)
        text_window.show()
    
    def show_word_count(self):
        text_window = SliderWindow(self, (40, 200), self.word_count,
                                   "Word Count", self.set_word_count)
        text_window.show()

    def toggle_mistake_highlight(self):
        self.current_widget_page.toggle_mistake_override()

    def add_settings_menu(self, menu_bar):
        settings_menu = menu_bar.addMenu(QIcon("assets/settings_icon.png"),
                                         "Settings")

        volume_action = QAction(QIcon("assets/volume_icon"), "Volume", self)
        volume_action.triggered.connect(self.show_volume)
        settings_menu.addAction(volume_action)

        text_action = QAction(QIcon("assets/font_icon.png"), "Font Size", self)
        text_action.triggered.connect(self.show_text_size)
        settings_menu.addAction(text_action)

        word_count_action = QAction(QIcon("assets/font_icon.png"),
                                    "Word Count", self)
        word_count_action.triggered.connect(self.show_word_count)
        settings_menu.addAction(word_count_action)

    def add_text_theme_menu(self, menu_bar):
        text_theme_menu = menu_bar.addMenu(QIcon("assets/generation_icon.png"),
                                           "Settings")

        def make_action(label):
            action = QAction(QIcon(f"assets/{label}_icon.png"), label.capitalize(), self)
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
        dialog.setWindowIcon(QIcon(f"assets/{style_type}_icon.png"))

        if dialog.exec():  # Show dialogue
            user_input = dialog.textValue()
            if user_input:
                print(f"{style_type.capitalize()} set to: {user_input}")
                self.generation_type = style_type
                self.generation_type_content = user_input
            else:
                print(f"No {style_type} entered.")

    def create_menu(self):
        menu_bar = self.menuBar()

        home_action = QAction(QIcon("assets/home_icon.png"), "Home", self)
        home_action.triggered.connect(self.enter_home)
        menu_bar.addAction(home_action)

        self.add_file_menu(menu_bar)
        self.add_settings_menu(menu_bar)
        self.add_text_theme_menu(menu_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MainWindow()
    editor.show()
    sys.exit(app.exec())
