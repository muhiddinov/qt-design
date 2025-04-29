import sys
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt, QTimer, QTime
import time
import json
import os

class ProcessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Process")
        self.setGeometry(100, 100, 1000, 600)
        
        self.pause_clicked = False
        self.pause_time = 3 * 60 # 3 daqiqa
        self.work_time_in_second = 0
        self.active_pin = 0
        self.discounting = 0
        self.current_time = QTime.currentTime().toString("hh:mm")
        
        self.relays = []
        with open('config.a', '+r') as config_file:
            config_data = config_file.readlines()
            self.relays.clear()
            self.relays = json.loads(config_data[0])
        
        # GPIO sozlamalari
        GPIO.setmode(GPIO.BCM)
        self.output_pins = [relay["port"] for relay in self.relays]
        self.input_pins = [2, 3, 18, 23, 24, 25, 8, 7, 12, 16]
        self.cash_interrupt_pin = 21  # Interrupt uchun kiruvchi pin
        self.summa = 0  # Umumiy summa
        if os.path.exists('last.a'):
            with open('last.a', 'r') as last:
                self.summa = int(last.read())
            
        self.out_pwr_en = 17
        self.pause_interrupt_pin = 20
        
        GPIO.setup(self.out_pwr_en, GPIO.OUT)
        GPIO.output(self.out_pwr_en, GPIO.HIGH)
        
        # Chiquvchi pinlarni sozlash
        for pin in self.output_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        # Kiruvchi pinlarni sozlash
        for pin in self.input_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=self.execute_task, bouncetime=200)

        # Interrupt pinni sozlash
        GPIO.setup(self.pause_interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pause_interrupt_pin, GPIO.FALLING, callback=self.pause_callback, bouncetime=200)
        GPIO.setup(self.cash_interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.cash_interrupt_pin, GPIO.FALLING, callback=self.handle_interrupt, bouncetime=50)

        font = QFont("FreeSerif")
        font.setPixelSize(400)

        # Label yaratish
        self.lbl_timer = QLabel(self)
        self.lbl_timer.setFont(font)
        self.lbl_timer.setStyleSheet("color: red; background-color: black;")
        self.lbl_timer.setAlignment(Qt.AlignCenter)

        font.setPixelSize(200)
        self.lbl_value = QLabel(self)
        self.lbl_value.setFont(font)
        self.lbl_value.setStyleSheet("color: red; background-color: black;")
        self.lbl_value.setAlignment(Qt.AlignCenter)
        self.lbl_value.setText("----")
        
        font.setPixelSize(200)
        self.lbl_func = QLabel(self)
        self.lbl_func.setFont(font)
        self.lbl_func.setStyleSheet("color: red; background-color: black;")
        self.lbl_func.setAlignment(Qt.AlignCenter)
        self.lbl_func.setText("----")

        # Layout yaratish
        layout_hor = QVBoxLayout()
        layout_hor.addWidget(self.lbl_func)
        layout_hor.addWidget(self.lbl_value)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_timer)
        layout.addLayout(layout_hor)
        self.setLayout(layout)

        self.callback_function = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.toggle_clock = False
        self.ads_window_time = time.process_time()
        self.ads_window_show = False
        self.update_time()
        
    def setWindowSize(self, size):
        self.setGeometry(0, 0, size.width(), size.height())
        self.lbl_timer.setGeometry(0, 0, size.width(), size.height() // 2)
        self.lbl_value.setGeometry(0, size.height() // 2, size.width(), size.height() // 2)
            
    def pause_callback(self, index):
        print(f"Pause Callback: {index}")
        if self.work_time_in_second > 0:
            self.pause_clicked = True
            self.lbl_func.setText("PAUSE")
            for pin in self.output_pins:
                GPIO.output(pin, GPIO.LOW)
            
    def update_time(self):
        minute = int(self.work_time_in_second / 60)
        second = int(self.work_time_in_second % 60)
        if self.pause_clicked ==True:
            minute = int(self.pause_time / 60)
            second = int(self.pause_time % 60)
            if self.pause_time > 0:
                self.pause_time -= 1
        else:
            minute = int(self.work_time_in_second / 60)
            second = int(self.work_time_in_second % 60)
            if self.work_time_in_second > 0:
                self.work_time_in_second -= 1
                if self.active_pin > 0:
                    GPIO.output(self.active_pin, GPIO.LOW)
                    if self.summa > 0:
                        self.summa -= self.discounting
                        if self.summa < 0:
                            self.summa = 0
                        self.lbl_value.setText(str(self.summa) + " so'm")
                        with open('last.a', 'w') as last_file:
                            last_file.write(str(self.summa))
            else:
                self.summa = 0
                self.work_time_in_second = 0
                self.lbl_func.setText("----")
                if self.summa <= 0:
                    self.lbl_value.setText("----")
                
                    
        if minute > 0 or second > 0:
            self.current_time = str(f"{minute:02}:{second:02}")
        else:
            self.current_time = QTime.currentTime().toString("hh:mm")
            self.lbl_func.setText("----")
        if self.toggle_clock:
            self.current_time  = self.current_time.replace(":", " ")
        self.toggle_clock = not self.toggle_clock
        self.lbl_timer.setText(self.current_time)
        
    def handle_interrupt(self, channel):
        self.summa += 1000
        self.
        self.lbl_value.setText(f"{self.summa} so'm")

    def execute_task(self, task_index):
        self.pause_clicked = False
        if self.summa > 0:
            for pin in self.output_pins:
                GPIO.output(pin, GPIO.LOW)
            print(f"Tugma {task_index} bosildi. Vazifa bajarilmoqda...")
            input_index = self.input_pins.index(task_index)
            self.active_pin = self.output_pins[input_index]
            GPIO.output(self.active_pin, GPIO.HIGH)
            price = self.relays[input_index]["price"]
            funk_name = self.relays[input_index]["desc"]
            self.lbl_func.setText(funk_name)
            self.work_time_in_second = self.summa * 60 / price
            self.discounting = int(price / 60)
        else:
            self.active_pin = 0
            self.lbl_value.setText("Pul yetarli emas")
            QTimer.singleShot(2000, lambda: self.lbl_value.setText("----"))
        
        
    def closeEvent(self, event):
        for pin in self.output_pins:
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessWindow()
    window.showFullScreen()
    sys.exit(app.exec_())