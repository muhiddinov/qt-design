import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation

class SplashWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Wash")
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout(self)
        self.logo_label = QLabel(self)
        self.logo_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/logo.jpg")
        scaled_pixmap = pixmap.scaled(1920, 1080, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        layout.addWidget(self.logo_label)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.logo_label.setGraphicsEffect(self.opacity_effect)

        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(2000)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()
        
    def setNextWindow(self, next_window):
        self.next_window = next_window

    def start_main_app(self):
        fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_out.setDuration(2000)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.finished.connect(self.close)
        fade_out.start()
        self.next_window.showFullScreen()
        QTimer.singleShot(10000, splash.start_main_app)
        QTimer.singleShot(2000, self.close_splash)

    def close_splash(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashWindow()
    splash.showFullScreen()
    QTimer.singleShot(10000, splash.start_main_app)
    sys.exit(app.exec_())