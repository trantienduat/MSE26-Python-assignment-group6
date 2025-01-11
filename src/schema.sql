CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    seat_quantity TEXT NOT NULL,
    depature_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INTEGER PRIMARY KEY,
    trip_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    seat_number INTEGER NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips (trip_id),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    year_of_birth TEXT NOT NULL,
    phone_number TEXT NOT NULL
);

INSERT INTO customers 
    (first_name, last_name, year_of_birth, phone_number)
VALUES 
    ('Duat', 'Tran', '1998', '0337779773'),
    ('Van A', 'Nguyen', '2002', '0987676554'),
    ('Thi No', 'Nguyen', '1998', '0989232441');