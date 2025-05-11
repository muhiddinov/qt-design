import sqlite3

class DataBase():
    def __init__(self, db_path: str = "assets/carwash.db") -> None:
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_tables()
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("select * from optoins")
        if cursor.fetchall() == None:
            self.insert_default_data_options()
        cursor.execute("select * from carwash")
        if cursor.fetchall() == None:
            self.insert_default_data_carwash()
        self.connection.close()
        
    def get_carwash(self) -> dict:
        carwash = None
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("select username, password, device_id, url_config, url_cash, pause_time, penalty_cost, currency, currency_rate from carwash")
            data = cursor.fetchall()
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
    
    def update_option(self, optoin: dict) -> dict:
        self.connect()
        name = optoin["name"]
        btn_port = optoin["btn_port"]
        relay_port = optoin["relay_port"]
        status = optoin["status"]
        on_time = optoin["on_time"]
        off_time = optoin["off_time"]
        price = optoin["price"]
        cursor = self.connection.cursor()
        cursor.execute(
            """
            update options
            set name = ?, relay_port = ?, btn_port = ?, status = ?, on_time = ?, off_time = ?, price = ?
            where port = ?
            """,
            (name, relay_port, btn_port, status, on_time, off_time, price, relay_port)
        )
        self.connection.commit()
        cursor.execute(f"select name, relay_port, btn_port, status, on_time, off_time, price from relays where port = {relay_port}")
        data = cursor.fetchone()
        response = {
            "name":         data[0],
            "relay_port":   data[1],
            "btn_port":     data[2],
            "status":       data[3],
            "on_time":      data[5],
            "off_time":     data[5],
            "price":        data[6]
        }   
        self.connection.close()
        return response

    def connect(self) -> None:
        try:
            self.connection = sqlite3.connect(self.db_path)
        except:
            pass

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
            CREATE TABLE IF NOT EXISTS optoins (
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
        cursor.execute('''INSERT INTO carwash 
                       (username, password, device_id, url_config, url_cash, pause_time, penalty_cost, currency, currency_rate) 
                       VALUES ('deviceuser', 'supersecret123', 'qOMVzYh0JfXlfHkIWxq6VOO8dqIZ05Zy4fL6fqmPrY3dUHXAKK3mCckl5wyFJIAI'
                       'https://masofaviy-monitoring.uz/api/CarWashDevice/Resources/',
                       'https://masofaviy-monitoring.uz/api/CarWashDevice/PaymentUpload',
                       180, 1500, 'so'm', 500)''')
        self.connection.commit()
        self.connection.close()
    
    def insert_default_data_options(self) -> None:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 1',  27,  2,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 2',  22,  3,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 3',  10,  18, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 4',  9,   23, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 5',  11,  24, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 6',  5,   25, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 7',  6,   8,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 8',  13,  7,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 9',  19,  12, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 10', 26,  16, 0, 800, 200, 3000.0)")
        self.connection.commit()
        self.connection.close()
        
if __name__ == "__main__":
    db = DataBase()
    options = db.get_options()
    print(options)