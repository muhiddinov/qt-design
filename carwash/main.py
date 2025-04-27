#!/usr/bin/python3

from MainWindow import Ui_mainui
from PyQt5.QtWidgets import QApplication, QFrame, QGraphicsScene
from PyQt5.QtCore import QTimer, Qt
import sys
from process import ProcessWindow
from database import DataBase

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screen = self.app.primaryScreen()
        self.screen_size = self.screen.size()
        self.db = DataBase()  # Ma'lumotlar bazasini yaratish yoki ulanish
        # QFrame (asosiy oyna)
        self.mainWindow = QFrame()
        self.mainWindow.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.mainWindow.setWindowTitle("Car Wash")
        self.ui = Ui_mainui()
        self.ui.setupUi(self.mainWindow)

        # Proccess Window (ikkinchi oyna)
        self.process = ProcessWindow()
        self.process.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.process.setWindowTitle("Pixel Clock")

        # Klaviatura hodisasi uchun signal
        self.mainWindow.keyPressEvent = self.keyPressEvent

        # Asosiy oynani ko'rsatish
        self.mainWindow.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:  # Agar 'w' tugmasi bosilsa
            self.showProccessWindow()

    def showProccessWindow(self):
        # PixelClockWindow-ni ko'rsatish
        self.process.showFullScreen()
        self.mainWindow.hide()

        # 30 soniyadan keyin QFrame-ni qayta ko'rsatish
        QTimer.singleShot(30000, self.showMainFrame)

    def showMainFrame(self):
        # QFrame-ni qayta ko'rsatish
        self.mainWindow.showFullScreen()
        self.process.hide()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = MainApp()
    app.run()
