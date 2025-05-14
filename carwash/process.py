import sys
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QTime
import time
from utils import Config
import threading
import asyncio
import subprocess


class ProcessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Process")
        self.setGeometry(100, 100, 1000, 600)
        
        self.input_pins = []
        self.output_pins = []
        self.process_data = []
        self.cash_sum = 0
        self.cash_sum_discount = 0
        self.pause_time = 0
        self.option_time :float = 0.0
        self.timer_counter = 0
        self.toggle_clock = False
        self.in_option = False
        self.pause_clicked = False
        self.cash_data_post = False
        self.cash_data_sended = False
        self.penalty_time_cost = 2000
        self.vip_client = False
        
        # Config faylidan ma'lumotlarni yuklash
        self.config = Config()
        self.config.setCallback(self.update_config)
        self.process_data = self.config.config_data["options"]
        self.output_pins = self.config.relay_pins
        self.input_pins = self.config.button_pins
        self.cash_pin = self.config.cash_pin
        self.pause_pin = self.config.pause_pin
        self.out_pwr_en = self.config.out_pwr_en
        self.pause_time = float(self.config.pause_time)
        self.cash_sum = self.config.cash_sum
        self.last_option = self.process_data[0]
        self.penalty_time_cost = self.config.penalty_cost
        self.last_save_counter = 0

        if self.cash_sum > 100:
            self.pause_clicked = True

        # GPIO sozlamalari
        GPIO.setmode(GPIO.BCM)
                
        GPIO.setup(self.out_pwr_en, GPIO.OUT)
        GPIO.output(self.out_pwr_en, GPIO.HIGH)
        
        # Chiquvchi pinlarni sozlash
        for pin in self.output_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        # Kiruvchi pinlarni sozlash
        for pin in self.input_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.execute_option, bouncetime=1000)

        # Interrupt pinni sozlash
        GPIO.setup(self.pause_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pause_pin, GPIO.FALLING, callback=self.pause_callback, bouncetime=1000)
        
        GPIO.setup(self.cash_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.cash_pin, GPIO.RISING, callback=self.cash_callback, bouncetime=50)
        
        # fontlarni yuklash
        self.font = QFont("FreeSerif")
        self.font.setPixelSize(400)

        # Label yaratish
        self.lbl_timer = QLabel(self)
        self.lbl_timer.setFont(self.font)
        self.lbl_timer.setStyleSheet("color: red; background-color: black;")
        self.lbl_timer.setAlignment(Qt.AlignCenter)
        self.lbl_timer_str = "--:--"
        self.lbl_timer.setText(self.lbl_timer_str)

        self.font.setPixelSize(130)
        self.lbl_value = QLabel(self)
        self.lbl_value.setFont(self.font)
        self.lbl_value.setStyleSheet("color: red; background-color: black;")
        self.lbl_value.setAlignment(Qt.AlignCenter)
        self.lbl_value_str = "0 so'm"
        self.lbl_value.setText(self.lbl_value_str)
        
        self.lbl_func = QLabel(self)
        self.lbl_func.setFont(self.font)
        self.lbl_func.setStyleSheet("color: red; background-color: black;")
        self.lbl_func.setAlignment(Qt.AlignCenter)
        self.lbl_func_str = "PUL KIRITING!"
        self.lbl_func.setText(self.lbl_func_str)
        
        # Layout yaratish
        layout_hor = QVBoxLayout()
        layout_hor.addWidget(self.lbl_func)
        layout_hor.addWidget(self.lbl_value)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_timer)
        layout.addLayout(layout_hor)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer_intervent = 100
        self.timer.start(self.timer_intervent)
        
        self.httptimer = QTimer(self)
        self.httptimer.timeout.connect(self.fetch_config_data)
        self.httptimer.start(24 * 3600 * 1000) # 24 soat#
        self.penalty_process = False
        self.timer_ads = 0.0
        self.browser_process = None
        self.browser_opened = False

    def update_config(self):
        self.process_data = self.config.config_data["options"]
        self.pause_time = float(self.config.pause_time)
        self.penalty_time_cost = self.config.penalty_cost

    def fetch_config_data(self):
        if self.in_option or self.pause_clicked or self.vip_client:
            return
        asyncio.run(self.config.fetch_config_data())
        
    def setWindowSize(self, size):
        self.setGeometry(0, 0, size.width(), size.height())
        self.lbl_timer.setGeometry(0, 0, size.width(), size.height() // 2)
        self.lbl_value.setGeometry(0, size.height() // 2, size.width(), size.height() // 2)
            
    
    def seconds_to_str(self, seconds, format_str="%H:%M:%S"):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = format_str.replace("%H", f"{hours:02}")
        time_str = time_str.replace("%M", f"{minutes:02}")
        time_str = time_str.replace("%S", f"{seconds:02}")
        return time_str
    
    def update_time(self):
        lbl_value_text = ""
        lbl_func_text = ""
        lbl_timer_text = ""
        self.timer_counter += 1
        if self.timer_counter >= 5:
            self.timer_counter = 0
            self.toggle_clock = not self.toggle_clock
            
        if self.in_option == False and self.pause_clicked == False:
            self.timer_ads += 0.1
            if self.timer_ads >= 10.0 and self.browser_opened == False:
                self.browser_process = subprocess.Popen([
                    'chromium-browser',
                    '--noerrdialogs',
                    '--disable-session-crashed-bubble',
                    '--start-fullscreen',
                    '--incognito',
                    '--kiosk',
                    'http://127.0.0.1'])
                # self.hide()
                self.browser_opened = True
            
        if self.in_option == False:
            if self.pause_clicked:
                if self.cash_sum <= 0:
                    self.pause_clicked = False
                    return
                else:
                    if self.pause_time <= 0:
                        self.in_option = True
                        self.option_time = self.cash_sum * 60 / self.penalty_time_cost
                        self.cash_sum_discount = self.cash_sum / self.penalty_time_cost / 10
                        self.pause_clicked = False
                        self.penalty_process =True
                        return
                lbl_func_text = "KUTISH"
                self.pause_time -= 0.1
                if self.pause_time <= 0:
                    self.pause_time = 0
                lbl_timer_text = self.seconds_to_str(int(self.pause_time), "%M:%S") if self.toggle_clock else self.seconds_to_str(int(self.pause_time), "%M %S")
            else:
                if self.cash_sum <= 0:
                    self.cash_data_post = False
                self.pause_time = self.config.pause_time
                self.penalty_process = False
                lbl_func_text = "PUL KIRITING!" if self.cash_sum <= 0 else "PUL KIRITILDI!"
                lbl_timer_text = QTime.currentTime().toString("hh:mm") if self.toggle_clock else QTime.currentTime().toString("hh mm")
        else:
            self.option_time -= 0.1
            self.cash_sum -= self.cash_sum_discount
            if self.option_time <= 0:
                self.in_option = False
                self.pause_clicked = True
                self.option_time = 0.0
                self.cash_sum = 0
            else:
                lbl_func_text = f"{self.last_option['name']}"
                if self.penalty_process == True:
                    lbl_func_text = "PULLIK KUTISH"
                lbl_timer_text = self.seconds_to_str(int(self.option_time), "%M:%S") if self.toggle_clock else self.seconds_to_str(int(self.option_time), "%M %S")
        lbl_value_text = f"{int(self.cash_sum)} {self.config.currency}"
        if lbl_timer_text != "":
            self.lbl_timer.setText(lbl_timer_text)
        if lbl_func_text != "":
            self.lbl_func.setText(lbl_func_text)
        if lbl_value_text != "":
            self.lbl_value.setText(lbl_value_text)
        self.last_save_counter += 1
        if self.last_save_counter >= 10:
            self.last_save_counter = 0
            self.config.save_last_cash(int(self.cash_sum))
    
    def pause_callback(self, pin):
        if self.browser_process != None:
            self.browser_process.terminate()
            self.timer_ads = 0.0
            self.browser_opened = False
            self.showFullScreen()
        if self.pause_time > 0 or self.cash_sum > 0:
            self.pause_clicked = True
            self.in_option = False
        press_and_hold = False
        start_time = time.time()
        while GPIO.input(pin) == GPIO.LOW:
            if time.time() - start_time >= 7:
                press_and_hold = True
                break
        if press_and_hold:
            self.in_option = False
            self.cash_sum = 0
            self.pause_clicked = False
        
    def cash_callback(self, pin):
        if self.browser_process != None:
            self.browser_process.terminate()
            self.timer_ads = 0.0
            self.browser_opened = False
            self.showFullScreen()
        self.cash_data_post = True
        self.cash_sum += self.config.currency_rate
        self.option_time = int(self.cash_sum * 60 / self.last_option['price'])
        self.lbl_value.setText(f"{int(self.cash_sum)} {self.config.currency}")

    def execute_option(self, pin):
        if self.browser_process != None:
            self.browser_process.terminate()
            self.browser_opened = False
            self.timer_ads = 0.0
            self.showFullScreen()
        option = None
        for data in self.process_data:
            if data['btn_port'] == pin:
                option = data
                break
        if option is None:
            return
        if self.cash_sum > 0.0:
            self.penalty_process = False
            self.in_option = False
            self.last_option = option
            self.pause_clicked = True
            if self.cash_data_sended == False and self.cash_data_post == True:
                self.cash_data_sended = True
                asyncio.run(self.config.cash_data_post(self.cash_sum))
            time.sleep(2)
            execute_thread = threading.Thread(target=self.execute, args=(option,))
            execute_thread.start()

    def execute(self, option):
        self.pause_clicked = False
        self.in_option = True
        self.option_time = self.cash_sum * 60 / option['price']
        self.cash_sum_discount = self.cash_sum / self.option_time / 10
        print(option)
        while True:
            if option['status']:
                thread_relay = threading.Thread(target=self.control_relay, args=(option['relay_port'], option['on_time'], option['off_time']))
                thread_relay.start()
            else:
                GPIO.output(option['relay_port'], GPIO.HIGH)
            time.sleep((option['on_time'] + option['off_time']) / 1000)
            if self.last_option['name'] != option['name']:
                break
            if self.pause_clicked:
                break
            if self.cash_sum <= 0:
                break
        GPIO.output(option['relay_port'], GPIO.LOW)
        self.in_option = False
        self.stop_threads = False
        
    def control_relay(self, relay_pin, on_time, off_time):
        GPIO.output(relay_pin, GPIO.HIGH)
        time.sleep(on_time / 1000)
        GPIO.output(relay_pin, GPIO.LOW)
        if off_time > 1:
            time.sleep(off_time / 1000)
    
    def closeEvent(self, event):
        GPIO.cleanup()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
