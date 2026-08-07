import streamlit as st
import os
import uuid
import pandas as pd
from database import init_database, get_connection, save_order, save_consultation

# Initialize Database Architecture
init_database()

st.set_page_config(page_title="Chishtia Medical Store", page_icon="💊", layout="wide")

# Session State for Admin Login Check
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# Premium Mobile-Responsive Styling & Typography
st.markdown("""
    <style>
    /* Global Mobile Optimizations */
    [data-testid="stSidebar"] { padding: 10px 5px; }
    .stButton>button { width: 100% !important; border-radius: 8px !important; height: 45px; font-weight: bold; }
    
    .main-header {
        background: linear-gradient(135deg, #0f4c81, #1d8a99);
        padding: 1.5rem 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 { font-weight: 700; font-size: 1.8rem; margin-bottom: 5px; color: white !important; }
    .main-header p { font-size: 1rem; font-style: italic; opacity: 0.95; }
    .management-info { font-size: 0.85rem; margin-top: 10px; font-weight: 500; background: rgba(255,255,255,0.15); display: inline-block; padding: 6px 15px; border-radius: 50px; width: 90%; }
    
    .footer { text-align: center; padding: 1.5rem 1rem; color: #555; font-size: 0.85rem; border-top: 1px solid #e0e0e0; margin-top: 3rem; background-color: #f9f9f9; border-radius: 8px; }
    .footer strong { color: #0f4c81; }
    
    /* Payment Box Mobile Design */
    .payment-box { background: #f0fdf4; border: 1px dashed #16a34a; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 15px; }
    .payment-number { font-size: 1.4rem; font-weight: bold; color: #16a34a; background: #ffffff; padding: 5px; border-radius: 5px; border: 1px solid #bbf7d0; display: inline-block; margin-top: 5px; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# Premium Branding Header
st.markdown("""
    <div class="main-header">
        <h1>CHISHTIA MEDICAL STORE</h1>
        <p>Your Trusted Digital Healthcare Partner</p>
        <div class="management-info">🏥 Owned & Managed by Babar Aziz and Sabir Aziz</div>
    </div>
""", unsafe_allow_html=True)

# URL Check for Hidden Admin Link (?page=admin)
query_params = st.query_params
is_admin_url = query_params.get("page") == "admin"

if is_admin_url:
    menu_choice = "Secret Admin Dashboard"
else:
    st.sidebar.markdown("### Navigational Portal")
    menu_choice = st.sidebar.radio("Go to:", ["Home Pharmacy", "Order Medicines", "Upload Prescription", "Digital Clinic (Rs.300)"])

# 1. HOME PHARMACY
if menu_choice == "Home Pharmacy":
    st.markdown("### 🌟 Welcome to Chishtia Medical Store")
    st.write("Aap ghar baithe asani se apni medicines ka order likh kar bhej sakte hain ya doctor ki parchi (prescription) upload kar sakte hain.")
    
    st.markdown("---")
    st.markdown("### 💡 Daily Health Tip")
    st.info("💡 **Stay Hydrated!** Drinking 8-10 glasses of water daily helps flush toxins out of your kidneys and improves your overall metabolic health.")

# 2. ORDER MEDICINES (Direct Manual Written Order Only)
elif menu_choice == "Order Medicines":
    st.markdown("## 🛒 Medicine Ordering System")
    st.write("Apni matlooba medicines ki list niche box mein likhein aur apni details darj karke order submit karein.")
    
    st.markdown("### 👤 Step 1: Provide Delivery Information")
    cust_name = st.text_input("Full Name *")
    cust_mobile = st.text_input("Mobile Number *")
    cust_city = st.selectbox("City *", ["Sahiwal", "Lahore", "Karachi", "Islamabad", "Faisalabad", "Multan"])
    cust_address = st.text_area("Complete Residential Address *")
    
    st.markdown("### 📝 Step 2: Write Your Medicine Requirements")
    written_order = st.text_area("List your required medicines & amounts *:", placeholder="Example:\nPanadol 500mg - 2 Packs\nAugmentin 625mg - 1 Strip")
    instructions = st.text_input("Special Instructions (Optional)", placeholder="e.g. Please deliver after 5:00 PM")
    
    if st.button("🚀 Submit Written Order", type="primary"):
        if not cust_name or not cust_mobile or not cust_address or not written_order:
            st.error("⚠️ Verification Failed! Ensure details and medicine requirement script are filled.")
        else:
            o_id = str(uuid.uuid4())[:8].upper()
            full_details = f"Order Script:\n{written_order}\n\nInstructions: {instructions}"
            save_order(o_id, cust_name, cust_mobile, cust_address, cust_city, "Manual Written Script", full_details, None)
            st.success(f"🎉 Hand-written custom order successfully filed as Order ID: #{o_id}")
# 3. UPLOAD PRESCRIPTION
elif menu_choice == "Upload Prescription":
    st.markdown("## 📋 Upload Doctor Prescription")
    st.write("Upload a photo or PDF of your doctor's handwritten slip. Our pharmacist will read it and call you.")
    
    st.markdown("### 👤 Patient & Delivery Details")
    p_name = st.text_input("Full Patient Name *")
    p_mobile = st.text_input("Mobile Number *")
    p_city = st.selectbox("City Delivery Destination *", ["Sahiwal", "Lahore", "Karachi", "Islamabad", "Faisalabad", "Multan"])
    p_address = st.text_area("Complete Address *")
    
    uploaded_file = st.file_uploader("Choose Prescription File (Image/PDF) *", type=["png", "jpg", "jpeg", "pdf"])
    p_notes = st.text_area("Additional Notes (Optional)")
    
    if st.button("📤 Upload and Dispatch Order", type="primary"):
        if not p_name or not p_mobile or not p_address or not uploaded_file:
            st.error("⚠️ Ensure patient details and prescription file are uploaded.")
        else:
            o_id = str(uuid.uuid4())[:8].upper()
            file_ext = os.path.splitext(uploaded_file.name)[1]
            saved_filename = f"uploads/prescriptions/{o_id}{file_ext}"
            with open(saved_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            save_order(o_id, p_name, p_mobile, p_address, p_city, "Prescription Upload", f"Notes: {p_notes}", saved_filename)
            st.success(f"✅ Prescription submitted. Assigned ID: #{o_id}")

# 4. DIGITAL CLINIC (Rs.300)
elif menu_choice == "Digital Clinic (Rs.300)":
    st.markdown("## 👨‍⚕️ Remote Doctor Consultation Portal")
    st.info("💰 **Consultation Fee: Rs. 300**")
    
    st.markdown("#### 💳 Step 1: Send Fee to Babar Aziz (JazzCash/EasyPaisa)")
    st.markdown("""
    <div class="payment-box">
        <p style="margin:0; font-weight:bold; color:#15803d;">📱 JazzCash & EasyPaisa Number</p>
        <div class="payment-number">03009609625</div>
        <p style="margin-top:5px; margin-bottom:0; font-size:0.9rem; color:#166534;">Account Title: <strong>BABAR AZIZ</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📝 Step 2: Fill Case Profile & Upload Proof")
    pat_name = st.text_input("Patient Full Name *")
    pat_mob = st.text_input("Mobile / Contact Info *")
    symptoms_text = st.text_area("Describe Symptoms / Current Problems *", placeholder="Fever for last 2 days...")
    
    st.markdown("##### 📱 Mobile Voice Feature & Assets Manager")
    voice_note = st.file_uploader("🎤 Send Voice Note / Audio Recording", type=["mp3", "wav", "m4a", "ogg"])
    med_report = st.file_uploader("📎 Upload Medical Report", type=["pdf", "png", "jpg", "jpeg"])
    pay_ss = st.file_uploader("💵 Upload Payment Receipt Screenshot *", type=["png", "jpg", "jpeg"])
    
    if st.button("Submit Case to Doctor Panel", type="primary"):
        if not pat_name or not pat_mob or not symptoms_text or not pay_ss:
            st.error("⚠️ You must provide identity, symptoms, and payment screenshot.")
        else:
            c_id = "CON-" + str(uuid.uuid4())[:6].upper()
            
            file_ext_ss = os.path.splitext(pay_ss.name)[1]
            ss_path = f"uploads/payments/{c_id}_payment{file_ext_ss}"
            with open(ss_path, "wb") as f: 
                f.write(pay_ss.getbuffer())
                
            f_path = None
            if med_report:
                file_ext_rep = os.path.splitext(med_report.name)[1]
                f_path = f"uploads/consultations/{c_id}_report{file_ext_rep}"
                with open(f_path, "wb") as f: 
                    f.write(med_report.getbuffer())
                    
            v_path = None
            if voice_note:
                file_ext_v = os.path.splitext(voice_note.name)[1]
                v_path = f"uploads/consultations/{c_id}_audio{file_ext_v}"
                with open(v_path, "wb") as f: 
                    f.write(voice_note.getbuffer())
                    
            save_consultation(c_id, pat_name, pat_mob, ss_path, symptoms_text, f_path, v_path)
            st.success(f"🚀 Consultation Registered perfectly. Tracking ID: {c_id}") 
            st.info("Medical team will check the payment receipt and activate your chat dashboard via phone/SMS shortly.")

# 5. SECRET ALONE ADMIN DASHBOARD
elif menu_choice == "Secret Admin Dashboard":
    st.markdown("## 🔐 Strategic Operational Dashboard")
    
    if not st.session_state.admin_logged_in:
        admin_pass = st.text_input("Input Secure Dashboard Password", type="password")
        if st.button("Verify Authentication"):
            if admin_pass == "chishtia786":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Authentication Denied!")
                
    if st.session_state.admin_logged_in:
        st.success("Access Granted. Welcome back Babar & Sabir Aziz.")
        if st.button("🚪 Logout Admin Session"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        adm_tabs = st.tabs(["📦 Orders Ledger", "🩺 Clinic Consultations"])
        
        with adm_tabs[0]:
            st.markdown("### Active Customer Orders")
            conn = get_connection()
            orders_df = pd.read_sql_query("SELECT * FROM orders ORDER BY timestamp DESC", conn)
            conn.close()
            
            if not orders_df.empty:
                for index, row in orders_df.iterrows():
                    with st.expander(f"Order {row['order_id']} - {row['customer_name']} [{row['status']}]"):
                        st.write(f"**Contact:** {row['mobile']} | **Location:** {row['city']}, {row['address']}")
                        st.info(f"**Contents:** {row['order_details']}")
                        if row['prescription_path']:
                            st.image(row['prescription_path'], width=300)
                            
                        new_status = st.selectbox("Update Status", ["Pending", "Confirmed", "Preparing", "Delivered", "Cancelled"], key=f"status_{row['order_id']}", index=["Pending", "Confirmed", "Preparing", "Delivered", "Cancelled"].index(row['status']))
                        if st.button("Update Status", key=f"up_{row['order_id']}"):
                            conn = get_connection()
                            conn.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, row['order_id']))
                            conn.commit()
                            conn.close()
                            st.success("Status updated!")
                            st.rerun()
            else:
                st.write("No incoming product orders recorded yet.")
                
        with adm_tabs[1]:
            st.markdown("### Telemedicine Clinical Requests")
            conn = get_connection()
            cons_df = pd.read_sql_query("SELECT * FROM consultations ORDER BY timestamp DESC", conn)
            conn.close()
            
            if not cons_df.empty:
                for idx, row in cons_df.iterrows():
                    with st.expander(f"Consultation {row['consultation_id']} - {row['patient_name']} [{row['status']}]"):
                        st.write(f"**Contact:** {row['mobile']}")
                        st.warning(f"**Symptoms:** {row['symptoms']}")
                        st.image(row['payment_screenshot'], width=250)
                        
                        if row['file_path']: st.image(row['file_path'], width=250)
                        if row['voice_path']: st.audio(row['voice_path'])
                            
                        new_c_status = st.selectbox("Action Payment Status", ["Pending Verification", "Approved", "Rejected"], key=f"c_stat_{row['consultation_id']}", index=["Pending Verification", "Approved", "Rejected"].index(row['status']))
                        dr_txt = st.text_area("Doctor Reply Input", value=row['doctor_reply'] if row['doctor_reply'] else "", key=f"dr_txt_{row['consultation_id']}")
                        
                        if st.button("Apply Operational Decision", key=f"c_btn_{row['consultation_id']}"):
                            conn = get_connection()
                            conn.execute("UPDATE consultations SET status = ?, doctor_reply = ? WHERE consultation_id = ?", (new_c_status, dr_txt, row['consultation_id']))
                            conn.commit()
                            conn.close()
                            st.success("Case updated!")
                            st.rerun()
            else:
                st.write("No premium consultation clinical bookings registered yet.")

# Universal Corporate Footer Branding
st.markdown("""
    <div class="footer">
        <p>© 2026 <strong>Chishtia Medical Store</strong>. All Strategic Rights Reserved.</p>
        <p style="font-size: 0.85rem; letter-spacing: 1px; color:#555;">Managed by <strong>Babar Aziz & Sabir Aziz</strong> | System Design & Framework <strong>Developed by Abdul Rehman</strong></p>
    </div>
""", unsafe_allow_html=True)
