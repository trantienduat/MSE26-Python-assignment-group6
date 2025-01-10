class TripController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_trip(self, name, seat_quantity, schedule):
        print(f"the connection: {self.db_connection}")
        query = "INSERT INTO trips (name, seat_quantity, schedule) VALUES (?, ?, ?)"
        self.db_connection.execute_query(query, (name, seat_quantity, schedule))

    def update_trip(self, trip_id, origin, destination, departure_time):
        query = "UPDATE trips SET origin = ?, destination = ?, departure_time = ? WHERE trip_id = ?"
        self.db_connection.execute_query(query, (origin, destination, departure_time, trip_id))

    def delete_trip(self, trip_id):
        query = "DELETE FROM trips WHERE trip_id = ?"
        self.db_connection.execute_query(query, (trip_id,))

    def get_trip(self, trip_id):
        query = "SELECT * FROM trips WHERE trip_id = ?"
        return self.db_connection.fetch_one(query, (trip_id))

    def get_all_trips(self):
        query = "SELECT * FROM trips"
        return self.db_connection.fetch_all(query)
    
    # def create_trip(self, origin, destination, departure_time):
    #     print(f"Create a trip from {origin} to {destination} at {departure_time}")
