import sqlite3
import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_table():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False
    c.execute("INSERT INTO users VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()
    conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    data = c.fetchone()
    conn.close()
    return bool(data)
