#!/usr/bin/python3

from PyQt5.QtWidgets import QApplication, QFrame, QGraphicsScene
from PyQt5.QtCore import QTimer, Qt
import sys
from process import ProcessWindow
from splash import SplashWindow

"""
import subprocess
import time

# Start the browser
browser_process = subprocess.Popen([
        'chromium-browser',
        '--kiosk',
        '--noerrdialogs',
        '--disable-session-crashed-bubble',
        '--start-fullscreen',
        '--incognito',
        'http://localhost'])

# Wait for 20 seconds before closing (simulate viewing time)
time.sleep(20)

# Close the browser
browser_process.terminate()

"""


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screen = self.app.primaryScreen()
        self.screen_size = self.screen.size()

        self.process = ProcessWindow()
        self.process.setWindowSize(self.screen_size)
        self.process.setWindowTitle("Process Screen")
        self.process.setCursor(Qt.BlankCursor)
        self.process.showFullScreen()
        
        # self.splash = SplashWindow()
        # self.splash.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        # self.splash.setWindowTitle("Splash Screen")
        # self.splash.showFullScreen()
        # self.splash.setNextWindow(self.process)
        # self.splash.setCursor(Qt.BlankCursor)
        # QTimer.singleShot(5000, self.splash.start_main_app)

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = MainApp()
    app.run()
