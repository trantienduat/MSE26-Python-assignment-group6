import sqlite3
from flask import Flask, render_template, g, request, jsonify
from datetime import datetime

app = Flask(__name__)

DATABASE = "trip_system.db"


# reference: https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r", encoding="utf-8") as f:
            db.cursor().executescript(f.read())
        db.commit()


# <==================== Routing =======================================================> #
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# <==================== CUSTOMER =======================================================> #
@app.route("/customers", methods=["GET", "POST"])
def customers():
    db = get_db()
    cur = db.cursor()
    if request.method == "POST":
        data = request.get_json()
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        date_of_bitrh = data.get("dateOfBirth")
        phone_number = data.get("phoneNumber")
        cur.execute(
            "INSERT INTO customers (first_name, last_name, date_of_bitrh, phone_number) VALUES (?, ?, ?, ?)",
            (first_name, last_name, date_of_bitrh, phone_number),
        )
        db.commit()
    data = cur.execute("SELECT * FROM customers").fetchall()
    return render_template("customer.html", data=data)


@app.route("/customers/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    date_of_bitrh = data.get("dateOfBirth")
    phone_number = data.get("phoneNumber")

    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        UPDATE customers
        SET first_name = ?, last_name = ?, date_of_bitrh = ?, phone_number = ?
        WHERE customer_id = ?
    """,
        (first_name, last_name, date_of_bitrh, phone_number, customer_id),
    )
    db.commit()
    return jsonify({"message": "Customer updated successfully"}), 200


@app.route("/customers/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    db = get_db()
    cur = db.cursor()
    request.args.get("customer_id")
    cur.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
    db.commit()
    return "", 204


# <====================== TRIPS =======================================================> #
@app.route("/trips", methods=["GET", "POST"])
def trips():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        data = request.get_json()
        origin = data.get("origin")
        destination = data.get("destination")
        cur.execute(
            "INSERT INTO trips (origin, destination) VALUES (?, ?)",
            (origin, destination),
        )
        db.commit()
    data = cur.execute("SELECT * FROM trips").fetchall()
    return render_template("trip.html", data=data)


@app.route("/trips/<trip_id>", methods=["DELETE", "PUT"])
def trip_actions(trip_id):
    db = get_db()
    cur = db.cursor()

    if request.method == "PUT":
        data = request.get_json()
        origin = data.get("origin")
        destination = data.get("destination")
        cur.execute(
            "UPDATE trips SET origin=:origin, destination=:destination WHERE trip_id=:id",
            {"id": trip_id, "origin": origin, "destination": destination},
        )
        db.commit()
    else:
        cur.execute("DELETE FROM trips WHERE trip_id=:id", {"id": trip_id})
        db.commit()
    data = cur.execute("SELECT * FROM trips").fetchall()
    return render_template("trip.html", data=data)


@app.route("/trips/<trip_id>/schedules")
def schedules_by_trip_id(trip_id):
    db = get_db()
    cur = db.cursor()
    data = cur.execute(
        """
        SELECT * FROM schedules 
        WHERE trip_id = ?
    """,
        (trip_id),
    ).fetchall()
    return jsonify(data), 200

# -------- SCHEDULE ---------------------------------------------------------- #
@app.route('/schedules', methods=["GET", "POST"])
def schedules():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        data = request.get_json()
        trip_id = data.get('tripId')
        departure_time = data.get('departureTime')
        arrival_time = data.get('arrivalTime')
        seat_quantity = data.get('seatQuantity')
        cur.execute("INSERT INTO schedules (trip_id, departure_time, arrival_time, seat_quantity) VALUES (?, ?, ?, ?)",
                    (trip_id, departure_time, arrival_time, seat_quantity))
        db.commit()
    data = cur.execute("SELECT * FROM schedules").fetchall()
    return jsonify(data), 201

@app.route("/schedules/<schedule_id>")
def available_seat_quantity_by_schedule_id(schedule_id):
    db = get_db()
    cur = db.cursor()
    # total quantity for each schedule - total ticket in
    data = cur.execute(
        """
    SELECT
        (SELECT seat_quantity FROM schedules WHERE schedule_id = ?) -
        (SELECT SUM(seat_quantity) FROM tickets WHERE schedule_id = ?);
    """,
        (schedule_id, schedule_id),
    ).fetchall()
    return jsonify(data), 200


# -------- Ticket ---------------------------------------------------------- #
@app.route('/ticket_cancel/<ticket_id>', methods=["PUT"])
def ticket_cancel(ticket_id):
    db = get_db()
    cur = db.cursor()
    status = cur.execute("SELECT status FROM tickets where ticket_id = ? ", (ticket_id,)).fetchone()
    if status[0] == 'BOOKED':
        cur.execute("UPDATE tickets set status = 'CANCEL' WHERE ticket_id = ?", (ticket_id,)).fetchone()
        db.commit()
        if cur.rowcount == 1:
            return jsonify({"message": "Ticket cancel success"}), 200
        else:
            return jsonify({"message": "Ticket cancel fail"}), 400


@app.route('/ticket/show_ticket/<customer_id>', methods=["get"])
def ticket(customer_id):
    db = get_db()
    cur = db.cursor()
    query = """
    SELECT 
        t.customer_id,
        trip.origin,
        trip.destination,
        t.seat_quantity,
        sch.departure_time,
        sch.arrival_time,
        t.ticket_id,
        t.departure_date,
        t.status
    FROM 
        tickets t
    JOIN 
        trips trip ON sch.trip_id = trip.trip_id
    JOIN 
        schedules sch ON t.schedule_id = sch.schedule_id
    WHERE 
        t.customer_id = ?;
    """
    data = cur.execute(query, (customer_id,)).fetchall()
    return render_template('ticket.html', data=data)


def seat_available(schedule_id, departure_date):
    db = get_db()
    cur = db.cursor()
    data = cur.execute(
        "SELECT SUM(seat_quantity) AS total_sum FROM tickets where schedule_id = ? and status = 'BOOKED' and departure_date = ?",
        (schedule_id, departure_date,)).fetchone()
    seat_quantity = cur.execute("SELECT seat_quantity FROM schedules where schedule_id = ? ", (schedule_id,)).fetchone()
    remaining_seat = data[0]
    if remaining_seat is None:
        remaining_seat = 0
    if remaining_seat < seat_quantity[0]:
        return True
    else:
        return False


@app.route('/ticket/buy_ticket', methods=["post"])
def buy_ticket():
    db = get_db()
    cur = db.cursor()
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    trip_id = data.get('trip_id')
    customer_id = data.get('customer_id')
    seat_quantity = data.get('seat_quantity')
    departure_date = datetime.strptime(data.get('departure_date'), "%Y-%m-%d")
    if datetime.now() > departure_date:
        return jsonify({"message": "Ticket buy fail"}), 400
    check = cur.execute("SELECT * FROM schedules WHERE schedule_id = ? and trip_id=?",
                        (schedule_id, trip_id)).fetchone()

    if check is not None:
        if seat_available(trip_id, departure_date):
            cur.execute(
                "INSERT INTO tickets (schedule_id,customer_id, departure_date, status,seat_quantity) VALUES ( ?, ?, ?, ?,?)",
                (schedule_id, customer_id, departure_date.strftime("%d-%m-%Y"), 'BOOKED', seat_quantity))
            db.commit()
            return jsonify({"message": "Ticket is buy success"}), 200
    return jsonify({"message": "Ticket buy fail"}), 400


@app.route('/ticket/<customer_id>', methods=["GET"])
def customers_login(customer_id):
    db = get_db()
    cur = db.cursor()
    data = cur.execute("SELECT * FROM customers WHERE customer_id = ? ", (customer_id,)).fetchone()
    trip = cur.execute("SELECT * FROM trips").fetchall()
    return render_template('buy_ticket.html', data=data, trip=trip)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)
