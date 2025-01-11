import sqlite3
from flask import Flask, render_template, g, request

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
# -------- CUSTOMER ---------------------------------------------------------- #
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/customer', methods=["GET", "POST"])
def customer():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST': 
        first_name = request.form['first_name'] 
        last_name = request.form['last_name'] 
        yob = request.form['yob'] 
        phone_number = request.form['phone_number'] 
        cur.execute("INSERT INTO customers (first_name, last_name, year_of_birth, phone_number) VALUES (?, ?, ?, ?)",
                    (first_name, last_name, yob, phone_number))
        db.commit()

    data = cur.execute("SELECT * FROM customers").fetchall()

    return render_template('customer.html', data=data)
  

@app.route('/customer/<customer_id>', methods=["DELETE"])
def delete_customer():
    pass

if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)