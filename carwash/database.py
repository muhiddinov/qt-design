import sqlite3

class DataBase():
    def __init__(self, db_path: str = "assets/carwash.db") -> None:
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_tables()
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("select * from relays")
        if cursor.fetchone() == None:
            self.insert_default_data()
        self.connection.close()

    def fetchAll(self, query: str) -> list:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.connection.close()
        return result

    def fetchOne(self, query: str) -> tuple:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        self.connection.close()
        return result

    def getRelays(self) -> dict:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("select name, desc, port, on_time, off_time, price from relays")
        data = cursor.fetchall()
        relays = []
        for relay in data:
            print(relay)
            relay_dict = {
                "name": relay[0],
                "desc": relay[1],
                "port": relay[2],
                "on_time": relay[3],
                "off_time": relay[4],
                "price": relay[5],
            }
            relays.append(relay_dict)
        self.connection.close()
        return relays
    
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
            UPDATE relays
            SET name = ?, status = ?, on_time = ?, off_time = ?, price = ?
            WHERE port = ?
            """,
            (name, desc, on_time, off_time, price, port)
        )
        self.connection.commit()
        cursor.execute(f"SELECT name, relay_port, btn_port, status, on_time, off_time, price FROM relays WHERE port = {port}")
        data = cursor.fetchone()
        response = {
            "name": data[0],
            "desc": data[1],
            "port": data[2],
            "on_time": data[3],
            "off_time": data[4],
            "price": data[5]
        }
        self.connection.close()
        return response

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.db_path)

    def create_tables(self) -> None:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carwash (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT,
                end_time TEXT,
                price REAL
            )
        ''')
        self.connection.commit()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optoins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                relay_port integer,
                btn_port integer,
                status boolean,
                on_time integer,
                off_time integer,
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
    
    def insert_default_data_options(self) -> None:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 1', 27,  2,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 2', 22,  3,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 3', 10,  18, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 4', 9,   23, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 5', 11,  24, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 6', 5,   25, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 7', 6,   8,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 8', 13,  7,  0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 9', 19,  12, 0, 800, 200, 3000.0)")
        cursor.execute("INSERT INTO relays (name, relay_port, btn_port, status, on_time, off_time, price) VALUES ('OPTION 10', 26, 16, 0, 800, 200, 3000.0)")
        self.connection.commit()
        self.connection.close()