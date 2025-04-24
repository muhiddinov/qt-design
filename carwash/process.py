import sys
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt, QTimer, QTime

class PixelClockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LED Matrix Style Clock")
        self.setGeometry(100, 100, 1000, 600)

        # GPIO sozlamalari
        GPIO.setmode(GPIO.BCM)
        self.output_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # Relay uchun chiquvchi pinlar
        self.input_pins = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]  # Tugmalar uchun kiruvchi pinlar
        self.interrupt_pin = 22  # Interrupt uchun kiruvchi pin
        self.pulse_count = 0  # Pulslar soni
        self.summa = 0  # Umumiy summa

        # Chiquvchi pinlarni sozlash
        for pin in self.output_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        # Kiruvchi pinlarni sozlash
        for pin in self.input_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Interrupt pinni sozlash
        GPIO.setup(self.interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.interrupt_pin, GPIO.FALLING, callback=self.handle_interrupt, bouncetime=200)

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

    def handle_interrupt(self, channel):
        # Interrupt pin orqali pulslarni hisoblash
        self.pulse_count += 1
        self.summa += 1000  # Har bir puls uchun 1000 qo'shiladi
        self.lbl_value.setText(f"Summa: {self.summa}")

        # Agar summa > 0 bo'lsa, tugmalarni tekshirish
        if self.summa > 0:
            for i, pin in enumerate(self.input_pins):
                if GPIO.input(pin) == GPIO.HIGH:
                    self.execute_task(i)

    def execute_task(self, task_index):
        # Tugma bosilganda bajariladigan vazifalar
        print(f"Tugma {task_index + 1} bosildi. Vazifa bajarilmoqda...")
        GPIO.output(self.output_pins[task_index], GPIO.HIGH)
        QTimer.singleShot(1000, lambda: GPIO.output(self.output_pins[task_index], GPIO.LOW))  # 1 soniyadan keyin o'chirish

    def closeEvent(self, event):
        # Dastur yopilganda GPIO tozalash
        GPIO.cleanup()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PixelClockWindow()
    window.show()
    sys.exit(app.exec_())