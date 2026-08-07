import sqlite3
import os
from datetime import datetime

DATABASE_FILE = "chishtia_healthcare.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initializes the database schema and sample data."""
    if not os.path.exists("uploads"):
        os.makedirs("uploads/prescriptions", exist_ok=True)
        os.makedirs("uploads/payments", exist_ok=True)
        os.makedirs("uploads/consultations", exist_ok=True)

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

    # 2. Orders Table (Browsed + Manual Orders)
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

    # 3. Consultation Booking & Communication Table
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

    # Injecting High-Quality Premium Sample Inventory
    cursor.execute("SELECT COUNT(*) FROM medicines")
    if cursor.fetchone() == 0:
        sample_meds = [
            ('Panadol 500mg (Tablet)', 'Fever & Pain', 30.0, 'Effective for relief of fever and mild to moderate pain.', 500, 1),
            ('Augmentin 625mg (Coated)', 'Antibiotics', 450.0, 'Broad-spectrum antibiotic for bacterial infections.', 120, 1),
            ('Surbex-Z (Nutritional)', 'Vitamins', 380.0, 'High potency vitamin zinc therapeutic supplement.', 200, 1),
            ('Amoxil 250mg (Capsule)', 'Antibiotics', 180.0, 'Treatment of bacterial infections of upper respiratory tract.', 300, 0),
            ('Brufen 400mg (Analgesic)', 'Fever & Pain', 90.0, 'Reduces hormones that cause inflammation and pain.', 400, 0),
            ('Softin 10mg (Allergy)', 'Antihistamine', 220.0, 'Provides 24-hour relief from allergy symptoms and hay fever.', 250, 1)
        ]
        cursor.executemany("INSERT INTO medicines (name, category, price, description, stock, is_featured) VALUES (?, ?, ?, ?, ?, ?)", sample_meds)
    
    conn.commit()
    conn.close()

def save_order(order_id, name, mobile, address, city, order_type, details, prescription_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (order_id, customer_name, mobile, address, city, order_type, order_details, prescription_path, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_id, name, mobile, address, city, order_type, details, prescription_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def save_consultation(c_id, name, mobile, screenshot, symptoms, f_path, v_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO consultations (consultation_id, patient_name, mobile, payment_screenshot, symptoms, file_path, voice_path, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (c_id, name, mobile, screenshot, symptoms, f_path, v_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

