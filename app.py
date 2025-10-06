from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn


# ----------- DATABASE SETUP -----------
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Product table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create Location table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Location (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create ProductMovement table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductMovement (
            movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            from_location INTEGER,
            to_location INTEGER,
            product_id INTEGER,
            qty INTEGER,
            FOREIGN KEY(product_id) REFERENCES Product(product_id),
            FOREIGN KEY(from_location) REFERENCES Location(location_id),
            FOREIGN KEY(to_location) REFERENCES Location(location_id)
        )
    ''')

    conn.commit()
    conn.close()


# ----------- ROUTES -----------

@app.route('/')
def index():
    return render_template('index.html')


# ---------- PRODUCTS ----------
@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM Product').fetchall()
    conn.close()
    return render_template('products.html', products=products)


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('INSERT INTO Product (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))


# ---------- LOCATIONS ----------
@app.route('/locations')
def locations():
    conn = get_db_connection()
    locations = conn.execute('SELECT * FROM Location').fetchall()
    conn.close()
    return render_template('locations.html', locations=locations)


@app.route('/add_location', methods=['POST'])
def add_location():
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('INSERT INTO Location (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('locations'))


# ---------- PRODUCT MOVEMENTS ----------
@app.route('/movements')
def movements():
    conn = get_db_connection()
    movements = conn.execute('SELECT * FROM ProductMovement').fetchall()
    products = conn.execute('SELECT * FROM Product').fetchall()
    locations = conn.execute('SELECT * FROM Location').fetchall()
    conn.close()
    return render_template('movements.html', movements=movements, products=products, locations=locations)


@app.route('/add_movement', methods=['POST'])
def add_movement():
    product_id = request.form['product_id']
    from_location = request.form.get('from_location')
    to_location = request.form.get('to_location')
    qty = request.form['qty']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO ProductMovement (timestamp, from_location, to_location, product_id, qty)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, from_location or None, to_location or None, product_id, qty))
    conn.commit()
    conn.close()
    return redirect(url_for('movements'))


# ---------- REPORT ----------
@app.route('/report')
def report():
    conn = get_db_connection()
    # Calculate product balance at each location
    query = '''
        SELECT p.name AS product, l.name AS location,
        IFNULL(SUM(CASE WHEN pm.to_location = l.location_id THEN pm.qty ELSE 0 END), 0)
        - IFNULL(SUM(CASE WHEN pm.from_location = l.location_id THEN pm.qty ELSE 0 END), 0) AS qty
        FROM Product p
        CROSS JOIN Location l
        LEFT JOIN ProductMovement pm ON p.product_id = pm.product_id
        GROUP BY p.product_id, l.location_id
    '''
    report_data = conn.execute(query).fetchall()
    conn.close()
    return render_template('report.html', report_data=report_data)


if __name__ == '__main__':
    init_db()  # Create tables when the app starts
    app.run(debug=True)
