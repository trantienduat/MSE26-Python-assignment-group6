CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_bitrh TEXT NOT NULL,
    phone_number TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schedules (
    schedule_id INTEGER PRIMARY KEY,
    trip_id INTEGER NOT NULL,
    seat_quantity INTEGER NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips (trip_id)
);

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INTEGER PRIMARY KEY,
    schedule_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    seat_quantity INTEGER NOT NULL,
    departure_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (schedule_id) REFERENCES schedules (schedule_id),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);



INSERT INTO customers 
    (first_name, last_name, date_of_bitrh, phone_number)
VALUES 
    ('Duat', 'Tran', '1998', '0337779773'),
    ('Van A', 'Nguyen', '2002', '0987676554'),
    ('Thi No', 'Nguyen', '1998', '0989232441');


INSERT INTO trips 
    (origin, destination)
VALUES 
    ('Hồ Chí Minh', 'Đồng Nai'),    --ID: 1
    ('Hồ Chí Minh', 'Biên Hoà'),    --ID: 2
    ('Hồ Chí Minh', 'Tây Ninh'),    --ID: 3
    ('Hồ Chí Minh', 'Hà Nội'),      --ID: 4
    ('Hồ Chí Minh', 'Kiên Giang'),  --ID: 5
    ('Hồ Chí Minh', 'Khánh Hoà');   --ID: 6

INSERT INTO schedules 
    (trip_id, seat_quantity, departure_time, arrival_time)
VALUES 
    (1, 30, '7:00', '10:00'),
    (1, 20, '10:00', '13:30'),
    (1, 25, '14:00','17:00'),
    (2, 30, '8:00','10:00'),
    (2, 30, '16:00','18:00'),
    (3, 50, '09:00','12:00'),
    (3, 50, '15:00','18:00');

INSERT INTO tickets
    (schedule_id, customer_id, seat_quantity, departure_date, status)
VALUES
    (1, 1, 2, '01/01/2025', 'BOOKED'),
    (1, 2, 2, '01/01/2025', 'BOOKED'),
    (2, 3, 2, '01/01/2025', 'BOOKED'),
    (2, 1, 2, '02/01/2025', 'BOOKED');