import sqlite3
from flask import Flask, render_template, g, request, jsonify

app = Flask(__name__)

DATABASE = 'trip_system.db'

# reference: https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



# ======== Routing =========================================================== #

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# -------- CUSTOMER ---------------------------------------------------------- #
@app.route('/customers', methods = ["GET", "POST"])
def customers():
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST': 
        data = request.get_json()
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        date_of_bitrh = data.get('dateOfBirth')
        phone_number = data.get('phoneNumber')
        cur.execute("INSERT INTO customers (first_name, last_name, date_of_bitrh, phone_number) VALUES (?, ?, ?, ?)",
                    (first_name, last_name, date_of_bitrh, phone_number))
        db.commit()
    data = cur.execute("SELECT * FROM customers").fetchall()
    return render_template('customer.html', data=data)

@app.route('/customers/<customer_id>', methods = ["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    date_of_bitrh = data.get('dateOfBirth')
    phone_number = data.get('phoneNumber')

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE customers
        SET first_name = ?, last_name = ?, date_of_bitrh = ?, phone_number = ?
        WHERE customer_id = ?
    """, (first_name, last_name, date_of_bitrh, phone_number, customer_id))
    db.commit()
    return jsonify({"message": "Customer updated successfully"}), 200

@app.route('/customers/<customer_id>', methods = ["DELETE"])
def delete_customer(customer_id):
    db = get_db()
    cur = db.cursor()
    request.args.get("customer_id")
    cur.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
    db.commit()
    return '', 204


# -------- TRIP ---------------------------------------------------------- #
@app.route('/trips', methods=["GET", "POST"])
def trips():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST': 
        data = request.get_json()
        origin = data.get('origin')
        destination = data.get('destination')
        cur.execute("INSERT INTO trips (origin, destination) VALUES (?, ?)",
                    (origin, destination))
        db.commit()
    data = cur.execute("SELECT * FROM trips").fetchall()
    return render_template('trip.html', data=data)

@app.route('/trips/<trip_id>/schedules')
def schedules_by_trip_id(trip_id):
    db = get_db()
    cur = db.cursor()
    data = cur.execute("""
        SELECT * FROM schedules 
        WHERE trip_id = ?
    """, (trip_id)).fetchall()
    return jsonify(data), 200

# -------- SCHEDULE ---------------------------------------------------------- #
@app.route('/schedules/<schedule_id>')
def available_seat_quantity_by_schedule_id(schedule_id):
    db = get_db()
    cur = db.cursor()
    data = cur.execute("""
    SELECT
        (SELECT seat_quantity FROM schedules WHERE schedule_id = ?) -
        (SELECT SUM(seat_quantity) FROM tickets WHERE schedule_id = ?);
    """, (schedule_id, schedule_id)).fetchall()
    return jsonify(data), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False) 