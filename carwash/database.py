import sqlite3
import os

class DataBase():
    def __init__(self, db_path: str = "assets/carwash.db") -> None:
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        if not os.path.exists(self.db_path):
            self.create_tables()
            self.insert_default_data()
        else:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * from relays")
            if cursor.fetchone() is None:
                self.create_tables()
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

    def connect(self) -> None:
        if not os.path.exists(self.db_path):
            self.create_tables()
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                port integer,
                status boolean,
                on_time integer,
                off_time integer,
                price REAL
            )
        ''')
        self.connection.commit()
        self.connection.close()
        
    def insert_default_data(self) -> None:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 1', 27, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 2', 22, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 3', 10, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 4', 9, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 5', 11, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 6', 5, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 7', 6, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 8', 13, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 9', 19, 0, 800, 200, 2000.0)")
        cursor.execute("INSERT INTO relays (name, port, status, on_time, off_time, price) VALUES ('Relay 10', 26, 0, 800, 200, 2000.0)")
        self.connection.commit()
        self.connection.close()
    
    def get_database(self):
        return self.connection

    def close(self):
        self.connection.close()
