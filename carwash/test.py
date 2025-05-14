import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QTime, pyqtSignal
from utils import Config
import asyncio


class ProcessWindow(QWidget):
    asyncFunkSignal = pyqtSignal()
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
        self.asyncFunkSignal.connect(self.fetch_config_data, Qt.QueuedConnection)
        self.asyncFunkSignal.emit()
        # Config faylidan ma'lumotlarni yuklash
        self.config = Config()
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
        asyncio.run(self.config.update_config())
        self.process_data = self.config.config_data["options"]

        if self.cash_sum > 100:
            self.pause_clicked = True
            
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
        
        # self.httptimer = QTimer(self)
        # self.httptimer.timeout.connect(self.fetch_config_data)
        # self.httptimer.start(24 * 3600 * 1000) # 24 soat#
        self.penalty_process = False
        self.timer_ads = 0.0
        self.browser_process = None
        self.browser_opened = False

    async def fetch_config_data(self):
        if self.in_option or self.pause_clicked or self.vip_client:
            return
        config = await self.config.fetch_config_data()
        self.process_data = config["options"]
        self.pause_time = float(self.config.pause_time)
        self.penalty_time_cost = self.config.penalty_cost
        print("Fetch config data successful!")
        
    def setWindowSize(self, size):
        self.setGeometry(0, 0, size.width(), size.height())
        self.lbl_timer.setGeometry(0, 0, size.width(), size.height() // 2)
        self.lbl_value.setGeometry(0, size.height() // 2, size.width(), size.height() // 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
