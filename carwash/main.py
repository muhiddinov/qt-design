from ui import Ui_mainui
from PyQt5.QtWidgets import QApplication, QFrame, QGraphicsScene
from PyQt5.QtCore import QTimer, Qt
import sys
from process import PixelClockWindow

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screen = self.app.primaryScreen()
        self.screen_size = self.screen.size()

        # QFrame (asosiy oyna)
        self.Frame = QFrame()
        self.Frame.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.Frame.setWindowTitle("Car Wash")
        self.ui = Ui_mainui()
        self.ui.setupUi(self.Frame)

        # PixelClockWindow (ikkinchi oyna)
        self.ui2 = PixelClockWindow()
        self.ui2.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.ui2.setWindowTitle("Pixel Clock")

        # Klaviatura hodisasi uchun signal
        self.Frame.keyPressEvent = self.keyPressEvent

        # Asosiy oynani ko'rsatish
        self.Frame.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:  # Agar 'w' tugmasi bosilsa
            self.showPixelClockWindow()

    def showPixelClockWindow(self):
        # PixelClockWindow-ni ko'rsatish
        self.ui2.showFullScreen()
        self.Frame.hide()

        # 30 soniyadan keyin QFrame-ni qayta ko'rsatish
        QTimer.singleShot(30000, self.showMainFrame)

    def showMainFrame(self):
        # QFrame-ni qayta ko'rsatish
        self.Frame.showFullScreen()
        self.ui2.hide()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = MainApp()
    app.run()