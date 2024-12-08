import sqlite3

DB_PATH = 'hotel.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY,
            name TEXT,
            floor INTEGER,
            type TEXT,
            price REAL,
            capacity INTEGER,
            amenities TEXT,
            image_url TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            rooms_booked TEXT,
            check_in_date TEXT,
            check_out_date TEXT,
            guests TEXT,
            customer_cmnd TEXT,
            customer_address TEXT,
            customer_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_rooms():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()
    conn.close()
    return rooms

def get_rooms_by_id(room_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
    room = cursor.fetchone()
    conn.close()
    return room

def search_rooms(criteria):
    query = 'SELECT * FROM rooms WHERE 1=1'
    params = []

    if criteria.get('name'):
        query += ' AND name LIKE ?'
        params.append(f"%{criteria['name']}%")
    if criteria.get('price_min'):
        query += ' AND price >= ?'
        params.append(float(criteria['price_min']))
    if criteria.get('price_max'):
        query += ' AND price <= ?'
        params.append(float(criteria['price_max']))
    if criteria.get('capacity'):
        query += ' AND capacity >= ?'
        params.append(int(criteria['capacity']))
    if criteria.get('type'):
        query += ' AND type = ?'
        params.append(criteria['type'])

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def save_booking(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (customer_name, rooms_booked, check_in_date, check_out_date, guests, 
                              customer_cmnd, customer_address, customer_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['customer_name'], data['rooms_booked'], data['check_in_date'], data['check_out_date'],
        data['guests'], data['customer_cmnd'], data['customer_address'], data['customer_type']
    ))
    conn.commit()
    conn.close()

def get_recommendations(limit=3):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms ORDER BY RANDOM() LIMIT ?', (limit,))
    recommendations = cursor.fetchall()
    conn.close()
    return recommendations
