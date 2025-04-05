import sys
from PySide6.QtGui import QFont, QIcon, QAction, QPainter, QColor
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QDialog, QSlider, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import QFile, QIODevice, QTextStream, Qt, QTimer

from typingBox import TypingBox

default_button_bg = "4caf50"  # hex value


class SliderWindow(QDialog):
    def __init__(self, parent=None, value_range=(0, 100), value=50, text="", onChanged=None):
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


class MainWindow(QMainWindow):
    def __init__(self):
        backgroundColour = "#080E4B"
        super().__init__()
        self.setWindowTitle("Error 404")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f'QMainWindow {{background: {backgroundColour}}}')


        # saves the current page
        self.current_widget_page = None
        self.enter_home()

        # settings
        self.volume = 50
        self.text_size = 15

        # menu bar
        self.create_menu()

    def enter_typing(self):
        text_edit = TypingBox(self.timeout)

        self.setCentralWidget(text_edit)
        self.current_widget_page = text_edit

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
        home_screen = QWidget()
        home_screen.setLayout(home_layout)

        self.setCentralWidget(home_screen)
        self.current_widget_page = home_screen

    def timeout(self):
        print("timeout")

    def set_volume(self, value):
        print("set volume to", value)
        self.volume = value

    def set_text_size(self, value):
        print("set text size to", value)
        self.text_size = value
        font = QFont("Times", value)
        self.timer.setFont(font)
        self.text_edit.setFont(font)

    def restart(self):
        self.timer.restart()
        self.text_edit.reset()
        print("restart?")

    def add_file_menu(self, menu_bar):
        file_menu = menu_bar.addMenu(QIcon("assets/menu_icon.png"), "File")

        restart_action = QAction(QIcon("assets/restart_icon.png"), "Restart", self)
        restart_action.triggered.connect(self.restart)
        file_menu.addAction(restart_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def show_volume(self):
        volume_window = SliderWindow(self, (1, 100), self.volume, "Volume", self.set_volume)
        volume_window.show()

    def show_text_size(self):
        text_window = SliderWindow(self, (10, 18), self.text_size, "Text Size", self.set_text_size)
        text_window.show()

    def toggle_mistake_highlight(self):
        self.text_edit.toggle_mistake_override()

    def add_settings_menu(self, menu_bar):
        settings_menu = menu_bar.addMenu(QIcon("assets/settings_icon.png"), "Settings")

        volume_action = QAction(QIcon("assets/volume_icon"), "Volume", self)
        volume_action.triggered.connect(self.show_volume)
        settings_menu.addAction(volume_action)

        text_action = QAction(QIcon("assets/font_icon.png"), "Font Size", self)
        text_action.triggered.connect(self.show_text_size)
        settings_menu.addAction(text_action)

        mistake_action = QAction(QIcon("assets/error_icon.png"), "Toggle mistake highlight", self)
        mistake_action.triggered.connect(self.toggle_mistake_highlight)
        settings_menu.addAction(mistake_action)

    def create_menu(self):
        menu_bar = self.menuBar()

        home_action = QAction(QIcon("assets/home_icon.png"), "Home", self)
        home_action.triggered.connect(self.enter_home)
        menu_bar.addAction(home_action)

        self.add_file_menu(menu_bar)
        self.add_settings_menu(menu_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MainWindow()
    editor.show()
    sys.exit(app.exec())
