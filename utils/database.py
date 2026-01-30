import sqlite3
import hashlib
import pandas as pd
import os

DB_NAME = "supply_chain.db"

def init_db():
    """Initialize the SQLite database with users table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # User Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized.")

def register_user(username, password):
    """Registers a new user. Returns True if successful, False if username exists."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
        
    conn.close()
    return success

def login_user(username, password):
    """Verifies user credentials. Returns True if correct."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    data = c.fetchall()
    
    conn.close()
    return len(data) > 0

def load_data_to_db():
    """Optional: Loads CSV data into SQLite for querying."""
    conn = sqlite3.connect(DB_NAME)
    
    if os.path.exists("demand_history.csv"):
        df_demand = pd.read_csv("demand_history.csv")
        df_demand.to_sql("demand_history", conn, if_exists="replace", index=False)
        
    if os.path.exists("transport_logs.csv"):
        df_transport = pd.read_csv("transport_logs.csv")
        df_transport.to_sql("transport_logs", conn, if_exists="replace", index=False)
        
    conn.close()
    print("Data loaded to DB.")

if __name__ == "__main__":
    init_db()
    load_data_to_db()
