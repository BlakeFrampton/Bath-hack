from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QTimer, Qt, QPointF
from PySide6.QtGui import QColor
import random, math

class ConfettiItem(QGraphicsRectItem):
    def __init__(self, scene_width):
        size = random.randint(5, 12)
        super().__init__(0, 0, size, size)
        self.setBrush(QColor(
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        ))
        self.setPos(random.randint(0, scene_width), random.randint(-100, 0))
        self.velocity = random.uniform(1.5, 3.5)

    def fall(self):
        self.moveBy(0, self.velocity)

    def is_off_screen(self, screen_height):
        return self.y() > screen_height


class ConfettiOverlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(parent.rect())
        self.scene_width = self.width()
        self.scene_height = self.height()

        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(self.rect())
        self.view.setStyleSheet("background: transparent; border: none;")
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QGraphicsView.NoFrame)

        self.confetti_items = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_confetti)

    def start_confetti(self):
        self.scene.clear()
        self.confetti_items = [ConfettiItem(self.scene_width) for _ in range(60)]
        for item in self.confetti_items:
            self.scene.addItem(item)
        self.show()
        self.raise_()
        self.timer.start(30)

    def update_confetti(self):
        all_below = True
        for item in self.confetti_items:
            if not item.is_off_screen(self.scene_height):
                item.fall()
                all_below = False

        if all_below:
            self.timer.stop()
            for item in self.confetti_items:
                self.scene.removeItem(item)
            self.confetti_items.clear()
            self.hide()  # Hide when done


class FireworkConfetti(QGraphicsRectItem):
    def __init__(self, origin_x, origin_y):
        size = random.randint(5, 10)
        super().__init__(-size/2, -size/2, size, size)
        self.setBrush(QColor(
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        ))
        self.setPos(origin_x, origin_y)

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.velocity = QPointF(math.cos(angle) * speed, math.sin(angle) * speed)
        self.gravity = 0.15

    def update_motion(self):
        self.setPos(self.pos() + self.velocity)
        self.velocity.setY(self.velocity.y() + self.gravity)

    def is_off_screen(self, scene_height):
        return self.pos().y() > scene_height + 50

class FireworkOverlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(parent.rect())
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(self.rect())
        self.view.setStyleSheet("background: transparent; border: none;")
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QGraphicsView.NoFrame)

        self.confetti_items = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_confetti)

    def start_firework(self, x=None, y=None):
        self.scene.clear()
        self.confetti_items.clear()

        center_x = x if x is not None else self.width() // 2
        center_y = y if y is not None else self.height() // 2

        for _ in range(80):
            confetti = FireworkConfetti(center_x, center_y)
            self.scene.addItem(confetti)
            self.confetti_items.append(confetti)

        self.show()
        self.raise_()
        self.timer.start(30)

    def update_confetti(self):
        all_done = True
        for item in self.confetti_items:
            if not item.is_off_screen(self.height()):
                item.update_motion()
                all_done = False

        if all_done:
            self.timer.stop()
            for item in self.confetti_items:
                self.scene.removeItem(item)
            self.confetti_items.clear()
            self.hide()

