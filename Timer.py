from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer
# by default, the text challenge will close after 5 minutes
class Timer:
    def __init__(self, runtime_seconds=300, parent=None, timeout=None, restart_on_timeout=False, position=(0, 0), dimensions=(200, 50)):
        self.timeout_function = timeout
        self.runtime_seconds = runtime_seconds
        total_minutes = self.runtime_seconds // 60
        total_seconds = self.runtime_seconds % 60

        # Create the label to display the time
        self.timer_label = QLabel(f"00:00 / {total_minutes:02}:{total_seconds:02}", parent)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.timer_label.setStyleSheet("font-size: 24px;")
        self.timer_label.setGeometry(position[0], position[1], dimensions[0], dimensions[1])

        # Create a QTimer that updates the label every second
        self.timer = QTimer(parent)
        self.timer.timeout.connect(self.update_timer)  # connect the timeout signal to our update function
        self.timer.start(1000)  # 1000 milliseconds = 1 second

        self.elapsed_time = 0
        self.restart_on_timeout = restart_on_timeout

        self.paused = False

    def hide(self):
        self.timer_label.hide()

    def show(self):
        self.timer_label.show()

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def setFont(self, font: QFont):
        self.timer_label.setFont(font)

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
            print("hi1")
            self.elapsed_time += 1

            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60

            self.timer_label.setText(f"{minutes:02}:{seconds:02} / {total_minutes:02}:{total_seconds:02}")  # Format as MM:SS
            # check for the timer ending
            if self.elapsed_time >= self.runtime_seconds:
                print("hi2")
                self.timer_label.setText(f"{total_minutes:02}:{total_seconds:02} / {total_minutes:02}:{total_seconds:02}")  # Format as MM:SS
                self.timeout()

    def timeout(self):
        self.timeout_function()

        if self.restart_on_timeout:
            self.restart()

