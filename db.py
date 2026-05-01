import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    payment_id TEXT,
    status TEXT
)
""")

conn.commit()

def add_order(user_id, payment_id):
    cursor.execute("INSERT INTO orders (user_id, payment_id, status) VALUES (?, ?, ?)",
                   (user_id, payment_id, "pending"))
    conn.commit()

def confirm_order(payment_id):
    cursor.execute("UPDATE orders SET status='paid' WHERE payment_id=?", (payment_id,))
    conn.commit()

def get_user(payment_id):
    cursor.execute("SELECT user_id FROM orders WHERE payment_id=?", (payment_id,))
    return cursor.fetchone()