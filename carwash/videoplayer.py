import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Video oynasi
        videoWidget = QVideoWidget()

        # Tugmalar
        self.openButton = QPushButton('Open Video')
        self.openButton.clicked.connect(self.open_file)

        self.playButton = QPushButton('Play')
        self.playButton.clicked.connect(self.play_video)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addWidget(self.openButton)
        layout.addWidget(self.playButton)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setText('Play')
        else:
            self.mediaPlayer.play()
            self.playButton.setText('Pause')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
