import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QDialog, QSlider, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtGui import QIcon, QAction, QPainter, QColor
from PySide6.QtCore import QFile, QIODevice, QTextStream, Qt, QTimer


class PlaceholderTextEdit(QTextEdit):
    def __init__(self, placeholder_text="initial text", parent=None):
        super().__init__(parent)
        self._placeholder_text = placeholder_text
        self.textChanged.connect(self.update)

    def setPlaceholderText(self, text):
        self._placeholder_text = text
        self.update()

    def placeholderText(self):
        return self._placeholder_text

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.toPlainText() == "":
            painter = QPainter(self.viewport())
            painter.setPen(QColor(150, 150, 150))  # Light gray color
            # painter.setFont(self.font())
            margin = self.document().documentMargin()
            painter.drawText(self.viewport().rect().adjusted(margin + 2, margin, 0, 0),
                             Qt.AlignTop | Qt.AlignLeft, self._placeholder_text)


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
        super().__init__()
        self.setWindowTitle("Error 404")
        self.setGeometry(100, 100, 800, 600)

        # text thing
        self.text_edit = PlaceholderTextEdit()
        self.setCentralWidget(self.text_edit)

        # settings
        self.volume = 50
        self.text_size = 15

        # menu bar
        self.create_menu()

        # timer
        self.timer = Timer(10, self, self.timeout, False, (200, 0))

    def timeout(self):
        print("timeout")

    def set_volume(self, value):
        print("set volume to", value)
        self.volume = value

    def set_text_size(self, value):
        print("set text size to", value)
        self.text_size = value

    def restart(self):
        self.timer.restart()
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

    def home(self):
        print("Go to home screen")

    def add_settings_menu(self, menu_bar):
        settings_menu = menu_bar.addMenu(QIcon("assets/settings_icon.png"), "Settings")

        volume_action = QAction(QIcon("assets/volume_icon"), "Volume", self)
        volume_action.triggered.connect(self.show_volume)
        settings_menu.addAction(volume_action)

        text_action = QAction(QIcon("assets/font_icon.png"), "Font Size", self)
        text_action.triggered.connect(self.show_text_size)
        settings_menu.addAction(text_action)

    def create_menu(self):
        menu_bar = self.menuBar()

        home_action = QAction(QIcon("assets/home_icon.png"), "Home", self)
        home_action.triggered.connect(self.home)
        menu_bar.addAction(home_action)

        self.add_file_menu(menu_bar)
        self.add_settings_menu(menu_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MainWindow()
    editor.show()
    sys.exit(app.exec())