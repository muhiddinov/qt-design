import asyncio
import aiohttp
from .database import Database

class Config:
    def __init__(self):
        self.db = DataBase()
        options = self.db.get_options()
        carwash = self.db.get_carwash()
        carwash['options'] = options
        self.config_data = carwash
        print(self.config_data)
        self.relay_pins = [option['relay_port'] for option in options]
        self.button_pins = [option['btn_port'] for option in options]
        self.cash_pin = 21
        self.pause_pin = 20
        self.out_pwr_en = 17
        self.cash_sum = self.db.get_last_cash()
        if self.cash_sum == None:
            self.cash_sum = 0
        self.pause_time = carwash['pause_time']
        self.username = carwash['username']
        self.password = carwash['password']
        self.url_cash = carwash['url_cash']
        self.url_config = carwash['url_config']
        self.device_id = carwash['device_id']
        self.penalty_cost = carwash['penalty_cost']
        self.currency = carwash['currency']
        self.currency_rate = carwash['currency_rate']
                
    def save_config(self, config: dict) -> dict | None:
        try:
            if config != None:
                self.db.update_carwash(config)
        except Exception as e:
            print(e)
            return None
        return config
    
    def get_last_cash(self) -> int | None:
        cash = 0
        try:
            cash = self.db.get_last_cash()
        except Exception as e:
            print(e)
            return None
        return cash
    
    def save_last_cash(self, cash:int) -> int:
        try:
            self.db.put_last_cash(cash)
        except Exception as e:
            print(e)
            return None
        return cash
    
    async def cash_data_post(self, cash_sum: int = 0) -> dict:
        auth = aiohttp.BasicAuth(self.username, self.password)
        data = {
                "deviceToken": self.device_id,
                "paymentType": 1,
                "amount": cash_sum
                }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url_cash, json=data, auth=auth) as response:
                    if response.status == 200:
                        print("Cash data posted successfully.")
                    else:
                        print(f"Failed to post cash data. Status code: {response.status}")
        except aiohttp.ClientError as e:
            print(f"Error posting cash data: {e}")
            return {"Error": str(e)}
        return data
    
    async def update_config(self):
        await self.fetch_config_data()
        
    async def fetch_config_data(self) -> dict:
        url = self.url_config + self.device_id
        auth = aiohttp.BasicAuth(self.username, self.password)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, auth=auth) as response:
                    if response.status == 200:
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
                        self.save_config(json_data=myconfig)
                        self.config_data = myconfig
                        print(self.config_data)
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
    