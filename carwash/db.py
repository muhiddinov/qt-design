import sqlite3
import json

class DataBase():
    def __init__(self, db_path: str = "assets/carwash.db") -> None:
        self.db_path = db_path
        self.connection = None
        self.create_tables()
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("select * from options")
        if len(cursor.fetchall()) == 0:
            self.insert_default_data_options()
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("select * from carwash")
        if len(cursor.fetchall()) == 0:
            self.insert_default_data_carwash()
        self.connection.close()
        
    def get_last_cash(self) -> int:
        cash = 0
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("select price from last")
            data = cursor.fetchone()[0]
            if data is not None:
                cash = int(data)
            self.connection.close()
        except Exception as e:
            return None
        return cash
    
    def put_last_cash(self, cash: int = 0) -> int:
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("select price from last")
            data = cursor.fetchone()
            if data == None:
                cursor.execute("insert into last(id, price) values(?, ?)", (1, cash))
            else:
                cursor.execute("update last set price = ? where id = 1", (cash,))
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            return None
        return cash
    
    def update_carwash(self, carwash: dict) -> dict | None:
        try:
            self.connect()
            username = carwash["username"]
            password = carwash["password"]
            device_id = carwash["device_id"]
            url_config = carwash["url_config"]
            url_cash = carwash["url_cash"]
            pause_time = carwash["pause_time"]
            penalty_cost = carwash["penalty_cost"]
            currency = carwash["currency"]
            currency_rate = carwash["currency_rate"]
            cursor = self.connection.cursor()
            cursor.execute(
                """
                update carwash
                set username = ?, password = ?, device_id = ?, url_config = ?, url_cash = ?, 
                pause_time = ?, penalty_cost = ?, currency = ?, currency_rate = ?
                where username = ?
                """,
                (username, password, device_id, url_config, url_cash, pause_time, penalty_cost, currency, currency_rate, username)
            )
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print(e)
            return None
        return carwash
    
    
    def get_carwash(self) -> dict | None:
        carwash = None
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("select username, password, device_id, url_config, url_cash, pause_time, penalty_cost, currency, currency_rate from carwash")
            data = cursor.fetchone()
            carwash = {
                'username':         data[0],
                'password':         data[1],
                'device_id':        data[2],
                'url_config':       data[3],
                'url_cash':         data[4],
                'pause_time':       data[5],
                'penalty_cost':     data[6],
                'currency':         data[7],
                'currency_rate':    data[8],
                
            }
            self.connection.close()
        except:
            return None
        return carwash

    def get_options(self) -> dict:
        options = None
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("select name, relay_port, btn_port, status, on_time, off_time, price from options")
            data = cursor.fetchall()
            options = []
            for optoin in data:
                optoin_dict = {
                    "name":         optoin[0],
                    "relay_port":   optoin[1],
                    "btn_port":     optoin[2],
                    "status":       optoin[3],
                    "on_time":      optoin[4],
                    "off_time":     optoin[5],
                    "price":        optoin[6],
                }
                options.append(optoin_dict)
            self.connection.close()
        except:
            return None
        return options

    def update_option(self, option: dict) -> dict:
        try:
            self.connect()
            name = option["name"]
            btn_port = option["btn_port"]
            relay_port = option["relay_port"]
            status = option["status"]
            on_time = option["on_time"]
            off_time = option["off_time"]
            price = option["price"]
            cursor = self.connection.cursor()
            cursor.execute(
                """
                update options
                set name = ?, relay_port = ?, btn_port = ?, status = ?, on_time = ?, off_time = ?, price = ?
                where relay_port = ?
                """,
                (name, relay_port, btn_port, status, on_time, off_time, price, relay_port)
            )
            self.connection.commit()
            self.connection.close()
        except:
            return None
        return option

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
        except Exception as e:
            print(e)

    def create_tables(self) -> None:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carwash (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                device_id TEXT,
                url_config TEXT,
                url_cash TEXT,
                pause_time INTEGER,
                penalty_cost INTEGER,
                currency TEXT,
                currency_rate INTEGER
            )
        ''')
        self.connection.commit()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                relay_port INTEGER,
                btn_port INTEGER,
                status BOOLEAN,
                on_time INTEGER,
                off_time INTEGER,
                price REAL
            )
        ''')
        self.connection.commit()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS last (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price INTEGER
            )
        ''')
        self.connection.commit()
        self.connection.close()
        
    
    def insert_default_data_carwash(self) -> None:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO carwash (
                            username, 
                            password, 
                            device_id, 
                            url_config, 
                            url_cash, 
                            pause_time, 
                            penalty_cost, 
                            currency, 
                            currency_rate
                        ) VALUES (
                           'deviceuser', 
                           'supersecret123', 
                           'vAJxKKExTEKyzYiZOCvctlt9TzqyiqQIKlj0fcBcpO0rFUmWO5qzF0S1KRRMc3G4',
                           'https://masofaviy-monitoring.uz/api/CarWashDevice/Resources/',
                           'https://masofaviy-monitoring.uz/api/CarWashDevice/PaymentUpload/',
                           180, 
                           1500, 
                           "so'm", 
                           500
                        )
                        ''')
        self.connection.commit()
        self.connection.close()
    
    def insert_default_data_options(self) -> None:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 1',  27,  2,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 2',  22,  3,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 3',  10,  18, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 4',  9,   23, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 5',  11,  24, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 6',  5,   25, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 7',  6,   8,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 8',  13,  7,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 9',  19,  12, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO options (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 10', 26,  16, 0, 800, 200, 3000.0)")
        self.connection.commit()
        self.connection.close()
        
if __name__ == "__main__":
    db = DataBase()
    options = db.get_options()
    carwash = db.get_carwash()
    resp = db.put_last_cash(3000)
    if resp != None:
        print("updated cash", db.get_last_cash())
    carwash['options'] = options
    carwash['pause_time'] = 200
    resp = db.update_carwash(carwash=carwash)
    if resp == None:
        print("Error on update_carwash")
    else:
        print("Succes!", resp)
    config = json.dumps(carwash, indent=4)
