import sqlite3

def connect():
    return sqlite3.connect("db/inventory.db")

def create_tables():
    conn = connect()
    cur = conn.cursor()

    # Added 'date_added' column to products
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        quantity INTEGER,
        date_added TEXT
    )
    """)

    # Created new table to keep track of bills and their timestamps
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        date_generated TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_product(name, price, quantity, date_added):
    conn = connect()
    cur = conn.cursor()
    # Notice we added date_added here and a 4th "?" in the VALUES
    cur.execute("INSERT INTO products(name, price, quantity, date_added) VALUES(?,?,?,?)",
                (name, price, quantity, date_added))
    conn.commit()
    conn.close()

def get_products():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_product(pid, name, price, quantity):
    conn = connect()
    cur = conn.cursor()
    # We do not update date_added here so it retains the original creation time
    cur.execute("UPDATE products SET name=?, price=?, quantity=? WHERE id=?",
                (name, price, quantity, pid))
    conn.commit()
    conn.close()

def delete_product(pid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()

# -------- NEW BILLING FUNCTIONS --------

def save_bill(total, date_generated):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO bills(total, date_generated) VALUES(?,?)",
                (total, date_generated))
    conn.commit()
    conn.close()

def get_bills():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bills")
    rows = cur.fetchall()
    conn.close()
    return rows