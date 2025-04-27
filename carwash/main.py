#!/usr/bin/python3

from ads import AdvertisingWindow
from PyQt5.QtWidgets import QApplication, QFrame, QGraphicsScene
from PyQt5.QtCore import QTimer, Qt
import sys
from process import ProcessWindow
from database import DataBase
from splash import SplashWindow

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screen = self.app.primaryScreen()
        self.screen_size = self.screen.size()
        self.db = DataBase()  # Ma'lumotlar bazasini yaratish yoki ulanish
        
        # QFrame (asosiy oyna)
        # self.mainWindow = QFrame()
        # self.mainWindow.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        # self.mainWindow.setWindowTitle("Car Wash")
        
        # Advertising Window (birinchi oyna)
        # self.advertisingWindow = AdvertisingWindow()
        # self.advertisingWindow.setupUi(self.mainWindow)

        # Proccess Window (ikkinchi oyna)
        self.process = ProcessWindow()
        self.process.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.process.setWindowTitle("Process Screen")
        
        # Splash Window
        self.splash = SplashWindow()
        self.splash.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.splash.setWindowTitle("Splash Screen")
        self.splash.showFullScreen()
        self.splash.setNextWindow(self.process)
        QTimer.singleShot(10000, self.splash.start_main_app)
        
        # Asosiy oynani ko'rsatish
        # self.mainWindow.showFullScreen()
        # self.process.showFullScreen()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = MainApp()
    app.run()
