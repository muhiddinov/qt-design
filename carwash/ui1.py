import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QFileDialog, QStyle
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Video Player")
        self.setGeometry(100, 100, 800, 600)

        # Media player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Video widget
        self.videoWidget = QVideoWidget()

        # Play button
        self.playButton = QPushButton("Play/Pause")
        self.playButton.clicked.connect(self.toggle_play)

        # Open file button
        self.openButton = QPushButton("Open Video")
        self.openButton.clicked.connect(self.open_file)

        # Layout
        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.openButton)
        layout.addWidget(self.playButton)
        widget.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.mediaPlayer.play()

    def toggle_play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
