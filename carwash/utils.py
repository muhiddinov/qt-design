import json
import requests
import asyncio
import aiohttp

class Config:
    def __init__(self):
        self.relay_pins = []
        self.button_pins = []
        self.cash_pin = 21
        self.pause_pin = 20
        self.out_pwr_en = 17
        self.cash_sum = 0
        self.config_file : str = 'config.a'
        self.config_data = []
        self.pause_time = 0
        self.username = 'deviceuser'
        self.password = 'supersecret123'
        self.url_cash = "https://masofaviy-monitoring.uz/api/CarWashDevice/PaymentUpload"
        self.url = 'https://masofaviy-monitoring.uz/api/CarWashDevice/Resources/'
        self.device_id = '12837192388a0sdua9hdsausdhas'
        self.penalty_cost = 2000
        
    def load_config(self, config_file :str = 'config.a') -> list:
        json_data = []
        with open(str(config_file), 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            self.config_data = json_data
            self.pause_time = json_data['pause_time']
            self.penalty_cost = json_data['penalty_cost']
            json_options = json_data['options']
            for data in json_options:
                self.relay_pins.append(data['relay_pin'])
                self.button_pins.append(data['button_pin'])
            file.close()
        return json_data
                
    def save_config(self, json_data, config_file :str = 'config.a') -> list:
        with open(config_file, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
            file.close()
        return json_data
    
    def get_last_event(self) -> dict:
        json_data = {'summa': 0, 'option': 'NONE'}
        with open('last.a', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            file.close()
        return json_data
    
    def save_last_event(self, json_data) -> dict:
        with open('last.a', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
            file.close()
        return json_data
    
    async def cash_data_post(self, url, username, password, device_id, cash_sum: float = 0.0) -> dict:
        url = url
        auth = aiohttp.BasicAuth(username, password)
        data = {
                "deviceToken": device_id,
                "paymentType": 1,
                "amount": cash_sum
                }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, auth=auth) as response:
                    if response.status == 200:
                        print("Cash data posted successfully.")
                    else:
                        print(f"Failed to post cash data. Status code: {response.status}")
        except aiohttp.ClientError as e:
            print(f"Error posting cash data: {e}")
    
    async def update_config(self, config_file: str = 'config.a'):
        await self.fetch_config_data(self.url, self.username, self.password, self.device_id, config_file)
        self.load_config(config_file)
        
    async def fetch_config_data(self, url, username, password, device_id, config_file: str = 'config.a') -> dict:
        url = url + device_id
        auth = aiohttp.BasicAuth(username, password)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, auth=auth) as response:
                    if response.status == 200:
                        config_data = await response.json()
                        myconfig = self.load_config(config_file)
                        options = myconfig['options']
                        option_config = config_data['options']
                        if option_config:
                            for item in option_config:
                                name = item['resourceName']
                                price = item['resourceMinutePrice']
                                relayPort = int(item['relayPort'])
                                relayOnTime = item['relayOnTime']
                                relayOffTime = item['relayOfTime']
                                for option in options:
                                    if option['relay_pin'] == relayPort:
                                        option['name'] = name
                                        option['price'] = price
                                        option['relay_pin'] = relayPort
                                        option['on_time'] = relayOnTime
                                        option['off_time'] = relayOffTime
                                        break
                        if config_data['pause_time'] is not None:
                            self.pause_time = config_data['pause_time']
                            if self.pause_time == 0:
                                self.pause_time = 180
                        if config_data['penalty_cost'] is not None:
                            self.penalty_cost = config_data['penalty_cost']
                            if self.penalty_cost == 0:
                                self.penalty_cost = 2000
                        myconfig['options'] = options
                        self.save_config(json_data=myconfig)
                        return myconfig
                    else:
                        print(f"Failed to fetch config data. Status code: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"Error fetching config data: {e}")
            return None
        
if __name__ == "__main__":
    config = Config()
    asyncio.run(config.update_config())
    