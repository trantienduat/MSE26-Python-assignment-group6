import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='bus_ticket_booking.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trips (
                trip_id INTEGER PRIMARY KEY,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                seat_quantity TEXT NOT NULL,
                depature_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY,
                trip_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                seat_number INTEGER NOT NULL,
                FOREIGN KEY (trip_id) REFERENCES trips (trip_id),
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.lastrowid

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()