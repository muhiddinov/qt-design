import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt, QTimer, QTime

class PixelClockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LED Matrix Style Clock")
        self.setGeometry(100, 100, 1000, 600)

        # Pixel shriftni yuklash
        font_id = QFontDatabase.addApplicationFont("pixel_lcd_7.ttf")
        if font_id == -1:
            print("Shrift yuklanmadi. .ttf fayl mavjudligini tekshiring.")
            sys.exit(1)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family)
        font.setPixelSize(400)  # Shrfit o'lchami

        # Label yaratish
        self.lbl_timer = QLabel(self)
        self.lbl_timer.setFont(font)
        self.lbl_timer.setStyleSheet("color: red; background-color: black;")
        self.lbl_timer.setAlignment(Qt.AlignCenter)
        self.lbl_timer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
         # Label yaratish
        self.lbl_value = QLabel(self)
        font.setPixelSize(200)
        self.lbl_value.setFont(font)
        self.lbl_value.setStyleSheet("color: red; background-color: black;")
        self.lbl_value.setAlignment(Qt.AlignCenter)
        self.lbl_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_value.setText("Pixel Clock")
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_timer)
        layout.addWidget(self.lbl_value)
        self.setLayout(layout)

        # Timer — har soniyada vaqtni yangilash
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Dastlabki vaqtni yangilash
        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime().toString("mm:ss")
        self.lbl_timer.setText(current_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PixelClockWindow()
    window.show()
    sys.exit(app.exec_())
