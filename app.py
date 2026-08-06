"""Chishtia Medical Store — Multinational E-Pharmacy Web Application."""
import streamlit as st
import os
import sqlite3
from datetime import datetime
from style_utils import inject_multinational_styles

# 1. Premium Configurations
st.set_page_config(page_title="Chishtia Medical Store", page_icon="💊", layout="centered")

# Inject professional responsive styles from our style_utils file
try:
    inject_multinational_styles()
except Exception:
    pass

# Integrated SQLite Database Initialization Logic
def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id TEXT PRIMARY KEY, name TEXT, phone TEXT, address TEXT, medicines TEXT, image_path TEXT, status TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS reminders 
                 (name TEXT, phone TEXT)''')
    conn.commit()
    conn.close()

init_db()

if not os.path.exists("prescriptions"):
    os.makedirs("prescriptions")

# URL Query Routing Logic (?view=admin)
query_params = st.query_params

if query_params.get("view") == "admin":
    # ==========================================
    # INTERNAL SECURE ADMIN VIEW
    # ==========================================
    st.markdown("<div style='background:linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%); padding:20px; border-radius:12px; text-align:center; color:white; margin-bottom:25px;'><h2 style='margin:0;'>🛡️ CHISHTIA MANAGEMENT DESK</h2><p style='margin:5px 0 0 0; opacity:0.8; font-size:13px;'>Internal Store Management System</p></div>", unsafe_allow_html=True)
    
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        
    if not st.session_state['authenticated']:
        st.subheader("Security Verification")
        admin_password = st.text_input("Yahan Admin Password Likhein:", type="password")
        if st.button("Unlock Dashboard Systems"):
            if admin_password.strip() == "chishtia123":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Ghalat Password!")
    else:
        if st.sidebar.button("Logout"):
            st.session_state['authenticated'] = False
            st.rerun()
            
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        all_orders = c.execute("SELECT * FROM orders ORDER BY timestamp DESC").fetchall()
        
        st.metric("Total Received Orders", len(all_orders))
        st.write("---")
        
        for order in all_orders:
            o_id, o_name, o_phone, o_address, o_meds, o_img, o_status, o_time = order
            with st.container():
                st.markdown(f'<div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom:15px;"><h4>📦 Order ID: {o_id}</h4><p><b>Client:</b> {o_name} | <b>Phone:</b> {o_phone}</p><p><b>Address:</b> {o_address}</p><p style="background:#f8fafc; padding:10px; border-radius:8px;"><b>Medicines:</b><br>{o_meds if o_meds else "Parchi Uploaded"}</p><p><b>Status:</b> {o_status}</p></div>', unsafe_allow_html=True)
                if o_img and os.path.exists(o_img):
                    st.image(o_img, width=280)
                if o_status != "Delivered":
                    if st.button(f"Mark Delivered ({o_id})", key=o_id):
                        c.execute("UPDATE orders SET status='Delivered' WHERE id=?", (o_id,))
                        conn.commit()
                        st.rerun()
        conn.close()
else:
    # ==========================================
    # GLOBAL MULTINATIONAL CUSTOMER VIEW
    # ==========================================
    st.markdown("""
    <div class="premium-container">
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px;">
            <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://w3.org">
                <path d="M12 2V22" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
                <path d="M12 2C13.5 2 14.5 3 14.5 4.5C14.5 6 12 7.5 12 7.5" stroke="#f59e0b" stroke-width="2" stroke-linecap="round"/>
                <path d="M12 22C6.5 19 6.5 14 9.5 12.5C12.5 11 11.5 9 14.5 8C17.5 7 17.5 4.5 15 3.5" stroke="#0ea5e9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="2" r="1.25" fill="#f59e0b"/>
            </svg>
            <h1 style="margin: 0; font-size: 26px; font-weight: 800; color: #0f172a;">CHISHTIA MEDICAL STORE</h1>
        </div>
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); padding: 18px; border-radius: 12px; text-align: center; color: white;">
            <div style="font-size: 13px; font-weight: 600; letter-spacing: 2px;">MULTINATIONAL E-PHARMACY GATEWAY</div>
            <div style="font-size: 11px; opacity: 0.7; margin-top: 4px;">⚡ Free 30-Minute Home Delivery Within 3KM Operations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_selection = st.radio("Order Ka Tarika Chunein:", ["📸 Upload Digital Prescription (Parchi)", "✍️ Enter Medicine Text Grid (Naam Likhein)"])

    with st.form(key="pharmacy_dispatch_form"):
        st.markdown('<div class="field-tag">Apna Name (Full Name) *</div>', unsafe_allow_html=True)
        cust_name = st.text_input("", placeholder="Abdul Rehman", key="cust_name", label_visibility="collapsed")
        st.markdown('<div class="field-tag">WhatsApp Contact Number *</div>', unsafe_allow_html=True)
        cust_phone = st.text_input("", placeholder="03009609625", key="cust_phone", label_visibility="collapsed")
        st.markdown('<div class="field-tag">Delivery Destination Address *</div>', unsafe_allow_html=True)
        cust_address = st.text_area("", placeholder="Complete address details", key="cust_address", label_visibility="collapsed")
        
        mounted_file, typed_meds = None, ""
        if "Upload Digital Prescription" in tab_selection:
            mounted_file = st.file_uploader("Upload Parchi Image", type=["jpg", "jpeg", "png"])
        else:
            typed_meds = st.text_area("Type Medicines Here")
            
        if st.form_submit_button(label="🚀 TRANSMIT DISPATCH ORDER"):
            if not cust_name or not cust_phone or not cust_address:
                st.error("Fields missing!")
            else:
                stamp_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                final_id = f"CMS-LOGIX-{stamp_id}"
                img_save_route = ""
                if mounted_file is not None:
                    img_save_route = f"prescriptions/{final_id}.png"
                    with open(img_save_route, "wb") as f:
                        f.write(mounted_file.getbuffer())
                
                conn = sqlite3.connect('orders.db')
                c = conn.cursor()
                c.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (final_id, cust_name, cust_phone, cust_address, typed_meds, img_save_route, "Pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                conn.close()
                st.success(f"Order Transmitted Successfully! ID: {final_id}")

    st.write("---")
    st.markdown('<div class="executive-footer"><div class="owner-classical-title">Babar Aziz & Sabir Aziz</div><div class="owner-subtitle">Executive Corporate Directorate</div><div class="dev-signature-banner">DEVELOPED BY ABDUL REHMAN</div><div class="system-subtext">© 2026 CHISHTIA MEDICAL STORE • POWERED BY SMART-PWA</div></div>', unsafe_allow_html=True)
