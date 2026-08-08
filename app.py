import streamlit as st
import os
import uuid
import pandas as pd
from database import init_database, get_connection, save_order, save_consultation

# Initialize Database Architecture
init_database()

st.set_page_config(page_title="Chishtia Medical Store", page_icon="💊", layout="wide")

# Session State for Page Navigation & Admin Session
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home Pharmacy"
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# Premium Mobile-First Styling (No Sidebar Needed)
st.markdown("""
    <style>
    /* Hide default Streamlit sidebar elements permanently */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    .stButton>button { width: 100% !important; border-radius: 8px !important; height: 48px; font-weight: bold; }
    
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
    
    /* Order History Styling */
    .status-badge { padding: 4px 10px; border-radius: 50px; font-size: 0.85rem; font-weight: bold; display: inline-block; }
    .status-pending { background-color: #fef3c7; color: #d97706; }
    .status-preparing { background-color: #e0f2fe; color: #0369a1; }
    .status-confirmed { background-color: #dcfce7; color: #15803d; }
    .status-delivered { background-color: #dcfce7; color: #166534; border: 1px solid #16a34a; }
    .status-cancelled { background-color: #fee2e2; color: #991b1b; }
    </style>
""", unsafe_allow_html=True)

# Premium Branding Header
st.markdown("""
    <div class="main-header">
        <h1>CHISHTIA MEDICAL STORE</h1>
        <p>Your Trusted Digital Healthcare Partner / Aap Ka Ehtemaad Shuda Digital Pharmacy</p>
        <div class="management-info">🏥 Owned & Managed by Babar Aziz and Sabir Aziz</div>
    </div>
""", unsafe_allow_html=True)

# URL Check for Secret Admin Gateway (?page=admin)
query_params = st.query_params
is_admin_url = query_params.get("page") == "admin" or query_params.get("page", [""])[0] == "admin"

if is_admin_url:
    st.session_state.current_page = "Secret Admin Dashboard"
else:
    # Premium Top Grid Navigation Menu for Mobiles (5 Buttons Total)
    st.markdown("### 📱 Select Service / Koi bhi aik service chunein:")
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    nav_col4, nav_col5, nav_col6 = st.columns(3)
    
    if nav_col1.button("🏡 Home Pharmacy\n(Main Page)", key="btn_home"):
        st.session_state.current_page = "Home Pharmacy"
    if nav_col2.button("🛒 Order Medicines\n(Dawaai Likhein)", key="btn_order"):
        st.session_state.current_page = "Order Medicines"
    if nav_col3.button("📋 Upload Prescription\n(Parchi Bhejein)", key="btn_presc"):
        st.session_state.current_page = "Upload Prescription"
    if nav_col4.button("👨‍⚕️ Digital Clinic (Rs.300)\n(Doctor Se Baat)", key="btn_clinic"):
        st.session_state.current_page = "Digital Clinic (Rs.300)"
    if nav_col5.button("🔍 Track My Order\n(Order Ka Status)", key="btn_track"):
        st.session_state.current_page = "Track My Order"
        
    st.markdown(f"**Current Section / Aap is page par hain:** `{st.session_state.current_page}`")
    st.markdown("---")

# 1. HOME PHARMACY
if st.session_state.current_page == "Home Pharmacy":
    st.markdown("### 🌟 Welcome to Chishtia Medical Store / KhushAamdeed")
    st.write("Aap ghar baithe asani se apni medicines ka order likh kar bhej sakte hain ya doctor ki parchi (prescription) upload kar sakte hain. Apna order track karne ke liye 'Track My Order' par click karein.")
    st.write("*(Aap ghar baithe aasaani se apni dawaion ka order likh kar bhejin ya doctor ki parchi upload karein. Apna order check karne ke liye Track My Order button dabayein).*")
    
    st.markdown("---")
    st.markdown("### 💡 Daily Health Tip / Sehat Ki Baat")
    st.info("💡 **Stay Hydrated!** Drinking 8-10 glasses of water daily helps flush toxins out of your kidneys and improves your overall metabolic health.\n\n*(Rozana 8 se 10 glass paani peene se gurde saaf rehte hain aur sehat behtar hoti hai).*")
# 2. ORDER MEDICINES (Direct Manual Written Order Only)
elif st.session_state.current_page == "Order Medicines":
    st.markdown("## 🛒 Medicine Ordering System / Dawaai Ka Order")
    st.write("Apni matlooba medicines ki list niche box mein likhein aur apni details darj karke order submit karein.")
    st.write("*(Apni dawaion ki list neeche box me likhein aur apni details de kar order bhejein).*")
    
    st.markdown("### 👤 Step 1: Provide Delivery Information / Apni Details Likhein")
    cust_name = st.text_input("Full Name / Aap Ka Poora Naam *")
    cust_mobile = st.text_input("Mobile Number / Phone Number *")
    cust_city = st.selectbox("City / Shehar *", ["Sahiwal", "Lahore", "Karachi", "Islamabad", "Faisalabad", "Multan"])
    cust_address = st.text_area("Complete Residential Address / Ghar Ka Poora Pata *")
    
    st.markdown("### 📝 Step 2: Write Your Medicine Requirements / Dawaion Ki List")
    written_order = st.text_area("List your required medicines & amounts / Apni dawaai aur tonaad (quantity) likhein *:", placeholder="Example:\nPanadol 500mg - 2 Packs\nAugmentin 625mg - 1 Strip")
    instructions = st.text_input("Special Instructions / Koi zaroori baat (Optional)", placeholder="e.g. Please deliver after 5:00 PM / Shaam 5 baje ke baad bhejein")
    
    if st.button("🚀 Submit Written Order / Order Bhejein", type="primary"):
        if not cust_name or not cust_mobile or not cust_address or not written_order:
            st.error("⚠️ Verification Failed! Ensure details and medicine requirement script are filled. / Meherbani karke saari zaroori details poori likhein.")
        else:
            o_id = str(uuid.uuid4())[:8].upper()
            full_details = f"Order Script:\n{written_order}\n\nInstructions: {instructions}"
            save_order(o_id, cust_name, cust_mobile, cust_address, cust_city, "Manual Written Script", full_details, None)
            st.success(f"🎉 Hand-written custom order successfully filed! Your Order tracking ID is: **#{o_id}** (Isko note kar lein status check karne ke liye).")
            st.info(f"*(Aap ka order chalagya hai! Aap ka tracking Number **#{o_id}** hai, isay apne paas likh lein).*")

# 3. UPLOAD PRESCRIPTION
elif st.session_state.current_page == "Upload Prescription":
    st.markdown("## 📋 Upload Doctor Prescription / Parchi Upload Karein")
    st.write("Upload a photo or PDF of your doctor's handwritten slip. Our pharmacist will read it and call you.")
    st.write("*(Doctor ki parchi ya slip ki photo ya PDF upload karein. Hamare pharmacist parchi parh kar aap ko phone karenge).*")
    
    st.markdown("### 👤 Patient & Delivery Details / Mareez Aur Delivery Ki Details")
    p_name = st.text_input("Full Patient Name / Mareez Ka Naam *")
    p_mobile = st.text_input("Mobile Number / Phone Number *")
    p_city = st.selectbox("City Delivery Destination / Shehar *", ["Sahiwal", "Lahore", "Karachi", "Islamabad", "Faisalabad", "Multan"], key="p_city_select")
    p_address = st.text_area("Complete Address / Pata *", key="p_address_text")
    
    uploaded_file = st.file_uploader("Choose Prescription File (Image/PDF) / Parchi ki Photo ya PDF chunein *", type=["png", "jpg", "jpeg", "pdf"])
    p_notes = st.text_area("Additional Notes / Koi aur baat (Optional)")
    
    if st.button("📤 Upload and Dispatch Order / Parchi Bhejein", type="primary"):
        if not p_name or not p_mobile or not p_address or not uploaded_file:
            st.error("⚠️ Ensure patient details and prescription file are uploaded. / Parchi ki file aur details upload karna zaroori hai.")
        else:
            o_id = str(uuid.uuid4())[:8].upper()
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            saved_filename = f"uploads/prescriptions/{o_id}{file_ext}"
            with open(saved_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            save_order(o_id, p_name, p_mobile, p_address, p_city, "Prescription Upload", f"Notes: {p_notes}", saved_filename)
            st.success(f"✅ Prescription submitted perfectly! Your tracking reference Token ID is: **#{o_id}**")
            st.info(f"*(Parchi successfully bhej di gayi hai. Aap ka Token ID: **#{o_id}** hai).*")
# 4. DIGITAL CLINIC (Rs.300)
elif st.session_state.current_page == "Digital Clinic (Rs.300)":
    st.markdown("## 👨‍⚕️ Remote Doctor Consultation Portal / Online Clinic")
    st.info("💰 **Consultation Fee: Rs. 300 / Doctor Ki Fees: 300 Rupee**")
    
    st.markdown("#### 💳 Step 1: Send Fee to Babar Aziz (JazzCash/EasyPaisa) / Fees Is Number Par Bhejein")
    st.markdown("""
    <div class="payment-box">
        <p style="margin:0; font-weight:bold; color:#15803d;">📱 JazzCash & EasyPaisa Number</p>
        <div class="payment-number">03009609625</div>
        <p style="margin-top:5px; margin-bottom:0; font-size:0.9rem; color:#166534;">Account Title: <strong>BABAR AZIZ</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📝 Step 2: Fill Case Profile & Upload Proof / Details Aur ScreenShot Bhejein")
    pat_name = st.text_input("Patient Full Name / Mareez Ka Poora Naam *")
    pat_mob = st.text_input("Mobile / Contact Info / Phone Number *")
    symptoms_text = st.text_area("Describe Symptoms / Bemari Ki Details Likhein *", placeholder="e.g. Fever for last 2 days / Do din se bukhar hai...")
    
    st.markdown("##### 📱 Mobile Voice Feature & Assets Manager / Voice Note Ya Reports")
    voice_note = st.file_uploader("🎤 Send Voice Note / Apni Awaaz Mein Record Karke Bhejein", type=["mp3", "wav", "m4a", "ogg"])
    med_report = st.file_uploader("📎 Upload Medical Report / Test Ki Report Upload Karein", type=["pdf", "png", "jpg", "jpeg"])
    pay_ss = st.file_uploader("💵 Upload Payment Receipt Screenshot / Fees Ka ScreenShot Bhejein *", type=["png", "jpg", "jpeg"])
    
    if st.button("Submit Case to Doctor Panel / Doctor Ko Bhejein", type="primary"):
        if not pat_name or not pat_mob or not symptoms_text or not pay_ss:
            st.error("⚠️ You must provide identity, symptoms, and payment screenshot. / Naam, bemari ki details aur fees ka screenshot lazmi hai.")
        else:
            c_id = "CON-" + str(uuid.uuid4())[:6].upper()
            
            file_ext_ss = os.path.splitext(pay_ss.name)[1].lower()
            ss_path = f"uploads/payments/{c_id}_payment{file_ext_ss}"
            with open(ss_path, "wb") as f: 
                f.write(pay_ss.getbuffer())
                
            f_path = None
            if med_report:
                file_ext_rep = os.path.splitext(med_report.name)[1].lower()
                f_path = f"uploads/consultations/{c_id}_report{file_ext_rep}"
                with open(f_path, "wb") as f: 
                    f.write(med_report.getbuffer())
                    
            v_path = None
            if voice_note:
                file_ext_v = os.path.splitext(voice_note.name)[1].lower()
                v_path = f"uploads/consultations/{c_id}_audio{file_ext_v}"
                with open(v_path, "wb") as f: 
                    f.write(voice_note.getbuffer())
                    
            save_consultation(c_id, pat_name, pat_mob, ss_path, symptoms_text, f_path, v_path)
            st.success(f"🚀 Consultation Registered perfectly! Track using ID: **{c_id}**") 
            st.info(f"*(Doctor ki clinic me aap ka case submit hogya hai. Tracking ID **{c_id}** hai. Fees verify hote hi doctor reply yahan bhej denge).*")

# 5. USER ORDER HISTORY & TRACKING PORTAL (SMART AUTO-CLEAN LOGIC)
elif st.session_state.current_page == "Track My Order":
    st.markdown("## 🔍 Personal Order History & Status Tracker / Order Check Karein")
    st.write("Apne order ka status (Pending, Preparing, Delivered) dekhne ke liye apna Mobile Number ya Order ID darj karein:")
    
    search_input = st.text_input("Enter Mobile Number or Order ID / Phone ya ID Likhein:")
    
    if search_input:
        clean_input = search_input.strip().replace("#", "").upper()
        
        conn = get_connection()
        user_orders = conn.execute("SELECT * FROM orders WHERE mobile = ? OR order_id = ? ORDER BY timestamp DESC", (search_input, clean_input)).fetchall()
        user_consults = conn.execute("SELECT * FROM consultations WHERE mobile = ? OR consultation_id = ? ORDER BY timestamp DESC", (search_input, clean_input)).fetchall()
        conn.close()
        
        st.markdown("### 📦 Aap Ke Medicine Orders / Dawaion Ke Orders:")
        if user_orders:
            for row in user_orders:
                status_class = f"status-{row['status'].lower()}"
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin-bottom: 10px; background-color: #fafafa;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b>Order ID: #{row['order_id']}</b>
                        <span class="status-badge {status_class}">{row['status']}</span>
                    </div>
                    <p style="margin: 5px 0; font-size: 0.9rem; color: #555;"><b>Date / Tareekh:</b> {row['timestamp']}</p>
                    <p style="margin: 5px 0; font-size: 0.9rem; color: #333;"><b>Order Items / Dawaai:</b><br>{row['order_details']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Is number/ID se koi medicine order nahi mila. / Is number par koi order nahi mila.")
        st.markdown("### 🩺 Aap Ki Doctor Consultations / Doctor Se Baat Cheet:")
        if user_consults:
            for row in user_consults:
                status_class = f"status-confirmed" if row['status'] == "Approved" else "status-pending"
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin-bottom: 10px; background-color: #fafafa;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b>Consultation ID: {row['consultation_id']}</b>
                        <span class="status-badge {status_class}">{row['status']}</span>
                    </div>
                    <p style="margin: 5px 0; font-size: 0.9rem; color: #555;"><b>Date / Tareekh:</b> {row['timestamp']}</p>
                    <p style="margin: 5px 0; font-size: 0.9rem; color: #333;"><b>Your Symptoms / Bemari:</b> {row['symptoms']}</p>
                    <div style="background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 10px; margin-top: 10px; border-radius: 4px;">
                        <b style="color: #15803d;">👨‍⚕️ Doctor Reply / Doctor Ka Jawab:</b><br>
                        {row['doctor_reply'] if row['doctor_reply'] else 'Babar Aziz sahib aap ki payment check karke jald doctor ka jawab yahan share karenge. Thoda intezar farmayein.'}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if row['doctor_voice_reply'] and isinstance(row['doctor_voice_reply'], str) and os.path.exists(row['doctor_voice_reply']):
                    st.write("🎤 **Doctor Audio Prescription / Jawab Ki Audio:**")
                    st.audio(row['doctor_voice_reply'])
        else:
            st.info("Is number/ID se koi consultation booking nahi mili. / Is number par koi consultation nahi mili.")

# 6. SECRET ALONE ADMIN DASHBOARD
elif st.session_state.current_page == "Secret Admin Dashboard":
    st.markdown("## 🔐 Strategic Operational Dashboard (Admin Panel)")
    
    if not st.session_state.admin_logged_in:
        admin_pass = st.text_input("Input Secure Dashboard Password", type="password")
        if st.button("Verify Authentication"):
            if admin_pass == "chishtia786":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Authentication Denied! / Galat Password.")
                
    if st.session_state.admin_logged_in:
        st.success("Access Granted. Welcome back Babar & Sabir Aziz.")
        if st.button("🚪 Logout Admin Session"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        # Correctly defined multi-tab instantiation
        adm_tabs = st.tabs(["📦 Orders Ledger", "🩺 Clinic Consultations"])
        
        with adm_tabs[0]:
            st.markdown("### Active Customer Orders Ledger")
            conn = get_connection()
            orders_df = pd.read_sql_query("SELECT * FROM orders ORDER BY timestamp DESC", conn)
            conn.close()
            
            if not orders_df.empty:
                for index, row in orders_df.iterrows():
                    with st.expander(f"Order {row['order_id']} - {row['customer_name']} [{row['status']}]"):
                        st.write(f"**Contact:** {row['mobile']} | **Location:** {row['city']}, {row['address']}")
                        st.info(f"**Contents:** {row['order_details']}")
                        
                        if row['prescription_path'] and isinstance(row['prescription_path'], str) and os.path.exists(row['prescription_path']):
                            if row['prescription_path'].lower().endswith('.pdf'):
                                with open(row['prescription_path'], "rb") as f:
                                    st.download_button("📥 Download PDF Prescription", f.read(), file_name=os.path.basename(row['prescription_path']), key=f"dl_{row['order_id']}")
                            else: 
                                st.image(row['prescription_path'], width=300)
                            
                        new_status = st.selectbox("Update Status", ["Pending", "Confirmed", "Preparing", "Delivered", "Cancelled"], key=f"status_{row['order_id']}", index=["Pending", "Confirmed", "Preparing", "Delivered", "Cancelled"].index(row['status']))
                        
                        col_up, col_del = st.columns(2)
                        if col_up.button("Update Status", key=f"up_{row['order_id']}"):
                            conn = get_connection()
                            conn.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, row['order_id']))
                            conn.commit()
                            conn.close()
                            st.success("Status modified updated!")
                            st.rerun()
                        
                        if col_del.button("🗑️ Delete Order Permanently (History Clear)", key=f"del_{row['order_id']}"):
                            conn = get_connection()
                            conn.execute("DELETE FROM orders WHERE order_id = ?", (row['order_id'],))
                            conn.commit()
                            conn.close()
                            st.warning("Order Record permanently deleted from historical logs!")
                            st.rerun()
            else: 
                st.write("No product orders recorded.")
                
        with adm_tabs[1]:
            st.markdown("### Telemedicine Clinical Requests")
            conn = get_connection()
            cons_df = pd.read_sql_query("SELECT * FROM consultations ORDER BY timestamp DESC", conn)
            conn.close()
            
            if not cons_df.empty:
                for idx, row in cons_df.iterrows():
                    with st.expander(f"Consultation {row['consultation_id']} - {row['patient_name']} [{row['status']}]"):
                        st.write(f"**Contact:** {row['mobile']} | Symptoms: {row['symptoms']}")
                        if row['payment_screenshot'] and os.path.exists(row['payment_screenshot']):
                            st.image(row['payment_screenshot'], width=250)
                        if row['voice_path'] and os.path.exists(row['voice_path']):
                            st.audio(row['voice_path'])
                            
                        new_c_status = st.selectbox("Action Payment Status", ["Pending Verification", "Approved", "Rejected"], key=f"c_stat_{row['consultation_id']}", index=["Pending Verification", "Approved", "Rejected"].index(row['status']))
                        dr_txt = st.text_area("Doctor Text Reply Input", value=row['doctor_reply'] if row['doctor_reply'] else "", key=f"dr_txt_{row['consultation_id']}")
                        
                        dr_audio_file = st.file_uploader("🎤 Doctor Optional Voice/Audio Reply Upload (.mp3/.wav)", type=["mp3", "wav"], key=f"dr_aud_{row['consultation_id']}")
                        
                        col_c_up, col_c_del = st.columns(2)
                        if col_c_up.button("Apply Operational Decision & Send Reply", key=f"c_btn_{row['consultation_id']}"):
                            v_reply_path = row['doctor_voice_reply']
                            if dr_audio_file:
                                file_ext_dr_v = os.path.splitext(dr_audio_file.name)[1].lower()
                                v_reply_path = f"uploads/doctor_replies/{row['consultation_id']}_dr_voice{file_ext_dr_v}"
                                with open(v_reply_path, "wb") as f: 
                                    f.write(dr_audio_file.getbuffer())
                            
                            conn = get_connection()
                            conn.execute("UPDATE consultations SET status = ?, doctor_reply = ?, doctor_voice_reply = ? WHERE consultation_id = ?", (new_c_status, dr_txt, v_reply_path, row['consultation_id']))
                            conn.commit()
                            conn.close()
                            st.success("Case updated with text/audio instructions!")
                            st.rerun()
                        
                        if col_c_del.button("🗑️ Delete Consultation Permanently", key=f"c_del_{row['consultation_id']}"):
                            conn = get_connection()
                            conn.execute("DELETE FROM consultations WHERE consultation_id = ?", (row['consultation_id'],))
                            conn.commit()
                            conn.close()
                            st.warning("Consultation case removed permanently!")
                            st.rerun()
            else: 
                st.write("No consultation clinical bookings.")

# Universal Corporate Footer Branding
st.markdown("""
    <div class="footer">
        <p>© 2026 <strong>Chishtia Medical Store</strong>. All Strategic Rights Reserved.</p>
        <p style="font-size: 0.85rem; letter-spacing: 1px; color:#555;">Managed by <strong>Babar Aziz & Sabir Aziz</strong> | System Design & Framework <strong>Developed by Abdul Rehman</strong></p>
    </div>
""", unsafe_allow_html=True)
