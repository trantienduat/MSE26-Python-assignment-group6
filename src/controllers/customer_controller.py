class CustomerController:
    def __init__(self, database):
        self.database = database

    def add_customer(self, name, email, phone_number):
        query = "INSERT INTO customers (name, email, phone_number) VALUES (?, ?, ?)"
        self.database.execute_query(query, (name, email, phone_number))

    def update_customer(self, customer_id, name, email, phone_number):
        query = "UPDATE customers SET name = ?, email = ?, phone_number = ? WHERE customer_id = ?"
        self.database.execute_query(query, (name, email, phone_number, customer_id))

    def delete_customer(self, customer_id):
        query = "DELETE FROM customers WHERE customer_id = ?"
        self.database.execute_query(query, (customer_id,))

    def get_customer(self, customer_id):
        query = "SELECT * FROM customers WHERE customer_id = ?"
        return self.database.fetch_one(query, (customer_id,))

    def get_all_customers(self):
        query = "SELECT * FROM customers"
        return self.database.fetch_all(query)
    
    def show(self):
        print("Customer Controller")