import sys
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt, QTimer, QTime
from time import sleep

class ProcessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LED Matrix Style Clock")
        self.setGeometry(100, 100, 1000, 600)

        # GPIO sozlamalari
        GPIO.setmode(GPIO.BCM)
        self.output_pins = [27, 22, 10, 9, 11, 5, 6, 13, 19, 26]  # Relay uchun chiquvchi pinlar
        self.input_pins = [2, 3, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]  # Tugmalar uchun kiruvchi pinlar
        self.interrupt_pin = 21  # Interrupt uchun kiruvchi pin
        self.pulse_count = 0  # Pulslar soni
        self.summa = 0  # Umumiy summa
        self.out_pwr_en = 17
        
        GPIO.setup(self.out_pwr_en, GPIO.OUT)
        
        # Chiquvchi pinlarni sozlash
        for pin in self.output_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        # Kiruvchi pinlarni sozlash
        for pin in self.input_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Interrupt pinni sozlash
        GPIO.setup(self.interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.interrupt_pin, GPIO.FALLING, callback=self.handle_interrupt, bouncetime=50)

        # Pixel shriftni yuklash
        font_id = QFontDatabase.addApplicationFont("Pixel Emulator.otf")
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

        # callback funksiya
        self.callback_function = None
        
        # Timer — har soniyada vaqtni yangilash
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Dastlabki vaqtni yangilash
        self.update_time()
        # for pin in self.output_pins:
        #     GPIO.setup(pin, GPIO.OUT)
        #     GPIO.output(pin, GPIO.HIGH)
        #     sleep(1)
        #     GPIO.output(pin, GPIO.LOW)
            
    def set_callback(self, callback):
        self.callback_function = callback

    def update_time(self):
        current_time = QTime.currentTime().toString("mm:ss")
        self.lbl_timer.setText(current_time)

    def handle_interrupt(self, channel):
        # Interrupt pin orqali pulslarni hisoblash
        if self.callback_function:
            self.callback_function()
        self.pulse_count += 1
        self.summa += 1000  # Har bir puls uchun 1000 qo'shiladi
        self.lbl_value.setText(f"Summa: {self.summa}")

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
    window = ProcessWindow()
    window.show()
    sys.exit(app.exec_())