import sqlite3
import os
from datetime import datetime, timedelta, timezone

DATABASE_FILE = "chishtia_healthcare.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_pakistan_time():
    """Returns the current precise date and time forced inside Pakistan Standard Time (PKT)."""
    # Pakistan is exactly GMT+5 hours ahead of universal server time
    pkt_zone = timezone(timedelta(hours=5))
    return datetime.now(pkt_zone).strftime("%Y-%m-%d %I:%M:%S %p")

def init_database():
    """Initializes the database schema and automatically repairs mismatch columns."""
    if not os.path.exists("uploads"):
        os.makedirs("uploads/prescriptions", exist_ok=True)
        os.makedirs("uploads/payments", exist_ok=True)
        os.makedirs("uploads/consultations", exist_ok=True)
        os.makedirs("uploads/doctor_replies", exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # 1. Medicines Inventory Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        category TEXT NOT NULL,
        price REAL NOT NULL, 
        description TEXT, 
        stock INTEGER NOT NULL, 
        is_featured INTEGER DEFAULT 0
    )""")

    # 2. Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY, 
        customer_name TEXT NOT NULL, 
        mobile TEXT NOT NULL,
        address TEXT NOT NULL, 
        city TEXT NOT NULL, 
        order_type TEXT NOT NULL, 
        order_details TEXT, 
        prescription_path TEXT, 
        status TEXT DEFAULT 'Pending', 
        timestamp TEXT NOT NULL
    )""")

    # 3. Consultation Booking & Telemedicine Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultations (
        consultation_id TEXT PRIMARY KEY, 
        patient_name TEXT NOT NULL, 
        mobile TEXT NOT NULL,
        payment_screenshot TEXT, 
        symptoms TEXT, 
        file_path TEXT, 
        voice_path TEXT,
        status TEXT DEFAULT 'Pending Verification', 
        doctor_reply TEXT, 
        timestamp TEXT NOT NULL
    )""")
    conn.commit()

    # --- AUTOMATIC SCHEMA REPAIR MIGRATOR ---
    try:
        cursor.execute("SELECT doctor_voice_reply FROM consultations LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE consultations ADD COLUMN doctor_voice_reply TEXT DEFAULT ''")
        conn.commit()

    conn.close()

def save_order(order_id, name, mobile, address, city, order_type, details, prescription_path):
    conn = get_connection()
    conn.execute("""
        INSERT INTO orders (order_id, customer_name, mobile, address, city, order_type, order_details, prescription_path, status, timestamp) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_id, name, mobile, address, city, order_type, details, prescription_path, 'Pending', get_pakistan_time()))
    conn.commit()
    conn.close()

def save_consultation(c_id, name, mobile, screenshot, symptoms, f_path, v_path):
    conn = get_connection()
    conn.execute("""
        INSERT INTO consultations (consultation_id, patient_name, mobile, payment_screenshot, symptoms, file_path, voice_path, status, doctor_reply, doctor_voice_reply, timestamp) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (c_id, name, mobile, screenshot, symptoms, f_path, v_path, 'Pending Verification', '', '', get_pakistan_time()))
    conn.commit()
    conn.close()
