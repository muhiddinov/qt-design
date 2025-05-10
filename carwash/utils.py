import json
import asyncio
import aiohttp
import traceback

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
        self.url_config = 'https://masofaviy-monitoring.uz/api/CarWashDevice/Resources/'
        self.device_id = 'qOMVzYh0JfXlfHkIWxq6VOO8dqIZ05Zy4fL6fqmPrY3dUHXAKK3mCckl5wyFJIAI'
        self.penalty_cost = 2000
        self.currency = "so'm"
        self.currency_rate = 1000
        
    def load_config(self, config_file :str = 'config.a') -> list:
        json_data = []
        try:
            with open(str(config_file), 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                self.config_data = json_data
                self.pause_time = json_data['pause_time']
                self.penalty_cost = json_data['penalty_cost']
                json_options = json_data['options']
                self.url_config = json_data['url_config']
                self.url_cash = json_data['url_cash']
                self.currency = json_data['currency']
                self.currency_rate = json_data['currency_rate']
                self.device_id = json_data['device_id']
                for data in json_options:
                    self.relay_pins.append(data['relay_pin'])
                    self.button_pins.append(data['button_pin'])
                file.close()
        except:
            return None
        return json_data
                
    def save_config(self, json_data, config_file :str = 'config.a') -> list:
        with open(config_file, 'w', encoding='utf-8') as file:
            if json_data is not None:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
            file.close()
        return json_data
    
    def get_last_event(self) -> dict:
        json_data = {'summa': 0}
        try:
            with open('last.a', 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                file.close()
        except:
            pass
        return json_data
    
    def save_last_event(self, json_data) -> dict:
        try:
            with open('last.a', 'w', encoding='utf-8') as file:
                json.dump(json_data, file)
                file.close()
        except:
            return {"Message": "Save last event ERROR!"}
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
    
    async def update_config(self):
        await self.fetch_config_data(self.url_config, self.username, self.password, self.device_id)
        
    async def fetch_config_data(self, url, username, password, device_id) -> dict:
        url = url + device_id
        auth = aiohttp.BasicAuth(username, password)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, auth=auth) as response:
                    if response.status == 200:
                        try:
                            resp_data = await response.json()
                            myconfig = self.config_data
                            options = myconfig['options']
                            option_config = resp_data['resources']
                            if option_config:
                                for item in option_config:
                                    name = item['relayDescription']
                                    price = item['resourceMinutePrice']
                                    relayPort = int(item['relayPort'])
                                    relayOnTime = int(item['relayOnTime'])
                                    relayOffTime = int(item['relayOfTime'])
                                    relayState = item['relayMonitorStatus']
                                    for option in options:
                                        if option['relay_pin'] == relayPort:
                                            option['name'] = name
                                            option['price'] = price
                                            option['relay_pin'] = relayPort
                                            option['on_time'] = relayOnTime if relayOnTime else 0
                                            option['off_time'] = relayOffTime if relayOffTime else 0
                                            option['state'] = relayState
                                            break
                            if resp_data['pauseTime'] is not None:
                                self.pause_time = resp_data['pauseTime']
                                if self.pause_time == 0:
                                    self.pause_time = 180
                                self.pause_time = 60 if self.pause_time < 60 else self.pause_time                                
                            if resp_data['penaltyCost'] is not None:
                                self.penalty_cost = resp_data['penaltyCost']
                                if self.penalty_cost == 0:
                                    self.penalty_cost = 2000
                                self.penalty_cost = 500 if self.penalty_cost < 500 else self.penalty_cost
                            myconfig['options'] = options
                            myconfig['pause_time'] = self.pause_time
                            myconfig['penalty_cost'] = self.penalty_cost
                            if myconfig != None:
                                self.save_config(json_data=myconfig)
                                self.config_data = myconfig
                                # print(self.config_data)
                                return myconfig
                        except Exception:
                            print(traceback.format_exc())
                    else:
                        print(f"Failed to fetch config data. Status code: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"Error fetching config data: {e}")
            return None
        
if __name__ == "__main__":
    config = Config()
    asyncio.run(config.update_config())
    