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
    
    def updateRelay(self, relay: dict) -> dict:
        self.connect()
        name = relay["name"]
        desc = relay["desc"]
        port = relay["port"]
        on_time = relay["on_time"]
        off_time = relay["off_time"]
        price = relay["price"]
        
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE relays
            SET name = ?, desc = ?, on_time = ?, off_time = ?, price = ?
            WHERE port = ?
            """,
            (name, desc, on_time, off_time, price, port)
        )
        self.connection.commit()
        cursor.execute(f"SELECT name, desc, port, on_time, off_time, price FROM relays WHERE port = {port}")
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
            CREATE TABLE IF NOT EXISTS relays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                desc TEXT,
                port integer,
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
        
    def insert_default_data(self) -> None:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 1', 'Relay 1', 27, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 2', 'Relay 1', 22, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 3', 'Relay 1', 10, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 4', 'Relay 1', 9, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 5', 'Relay 1', 11, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 6', 'Relay 1', 5, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 7', 'Relay 1', 6, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 8', 'Relay 1', 13, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 9', 'Relay 1', 19, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, desc, port, status, on_time, off_time, price) VALUES ('Relay 10', 'Relay 1', 26, 0, 800, 200, 2000.0)")
        self.connection.commit()
        self.connection.close()
    
    def get_database(self):
        return self.connection

    def close(self):
        self.connection.close()
