"""Chishtia Medical Store — Multinational E-Pharmacy Web Application."""

import html
from pathlib import Path

import streamlit as st

import backend as db

# ── Configuration ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
CSS_PATH = BASE_DIR / "styles.css"
ADMIN_PASSWORD = "chishtia123"

db.init_db()

SUBSTITUTE_DB = {
    "panadol": "Calpol / Paracetamol Molecule",
    "paracetamol": "Panadol / Calpol Molecule",
    "calpol": "Paracetamol / Panadol Molecule",
    "augmentin": "Amoxiclav / Curam Molecule",
    "omeprazole": "Risek / Omez Molecule",
    "metformin": "Glucophage / Diabex Molecule",
    "brufen": "Ibuprofen Generic Molecule",
}

ASCLEPIUS_SVG = """
<svg class="asclepius-logo" width="56" height="56" viewBox="0 0 56 56" fill="none"
     xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="28" cy="28" r="26" fill="url(#rodGlow)" stroke="#00a896" stroke-width="1.5"/>
  <defs>
    <radialGradient id="rodGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ecfdf5"/>
      <stop offset="100%" stop-color="#d1fae5"/>
    </radialGradient>
    <linearGradient id="goldRod" x1="28" y1="8" x2="28" y2="48">
      <stop offset="0%" stop-color="#fbbf24"/>
      <stop offset="50%" stop-color="#d97706"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
  </defs>
  <rect x="26.5" y="10" width="3" height="36" rx="1.5" fill="url(#goldRod)"/>
  <circle cx="28" cy="9" r="3.5" fill="#fbbf24" stroke="#d97706" stroke-width="0.8"/>
  <path d="M32 16 C42 18, 44 26, 38 32 C34 36, 30 34, 28 30 C26 34, 22 36, 18 32
           C12 26, 14 18, 24 16 C26 20, 30 20, 32 16 Z"
        fill="none" stroke="#059669" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M30 22 C34 24, 35 28, 32 31 C30 33, 27 31, 26 28 C25 31, 22 33, 20 31
           C17 28, 18 24, 22 22"
        fill="none" stroke="#10b981" stroke-width="1.4" stroke-linecap="round" opacity="0.7"/>
  <circle cx="36" cy="30" r="2" fill="#047857"/>
</svg>
"""


# ── Bootstrap ─────────────────────────────────────────────────────────────────
def load_css() -> None:
    if CSS_PATH.exists():
        st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)


def init_session_state() -> None:
    for key, default in {
        "admin_logged_in": False,
        "order_confirmed": False,
        "confirmed_order_id": "",
        "medicine_text": "",
        "order_mode": "prescription",
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default


def is_admin_route() -> bool:
    return st.query_params.get("view", "").lower() == "admin"


def show_message(text: str, kind: str = "info") -> None:
    css = {"error": "msg-error", "info": "msg-info", "success": "msg-success"}.get(
        kind, "msg-info"
    )
    st.markdown(f'<div class="msg-box {css}">{html.escape(text)}</div>', unsafe_allow_html=True)


def dual_label(en: str, ur: str) -> None:
    st.markdown(
        f'<div class="dual-label">'
        f'<span class="label-en">{html.escape(en)}</span>'
        f'<span class="label-ur">{html.escape(ur)}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )


def find_substitute(query: str) -> str | None:
    q = query.strip().lower()
    for key, value in SUBSTITUTE_DB.items():
        if key in q or q in key:
            return value
    return None


def whatsapp_href(phone: str) -> str:
    clean = phone.replace(" ", "").replace("-", "").lstrip("+")
    if clean.startswith("0"):
        clean = "92" + clean[1:]
    return f"https://wa.me/{clean}"


# ── Shared UI blocks ──────────────────────────────────────────────────────────
def render_brand_header(admin: bool = False) -> None:
    admin_note = (
        '<span class="brand-admin-note">Secure Admin Desk</span>' if admin else ""
    )
    st.markdown(
        f'<div class="brand-header{" admin" if admin else ""}">'
        f"{ASCLEPIUS_SVG}"
        f'<div class="brand-text-block">'
        f'<span class="brand-title">CHISHTIA MEDICAL STORE</span>'
        f"{admin_note}"
        f"</div></div>",
        unsafe_allow_html=True,
    )


def render_welcome_banner() -> None:
    st.markdown(
        '<div class="welcome-banner">'
        '<p class="welcome-title">CHISHTIA MEDICAL STORE • MULTINATIONAL E-PHARMACY GATEWAY</p>'
        '<p class="welcome-sub">⚡ Free 30-Minute Home Delivery Within 3KM Operations</p>'
        "</div>",
        unsafe_allow_html=True,
    )


def render_executive_footer() -> None:
    st.markdown(
        '<div class="executive-footer">'
        '<div class="footer-owners-wrap">'
        '<p class="footer-directorate">Executive Corporate Directorate</p>'
        '<p class="footer-owners">OWNERS: BABAR AZIZ &amp; SABIR AZIZ</p>'
        "</div>"
        '<p class="footer-developer">DEVELOPED BY ABDUL REHMAN</p>'
        '<p class="footer-legal">'
        "© 2026 CHISHTIA MEDICAL STORE • ENGINE INFRASTRUCTURE POWERED BY SMART-PWA DEPLOYMENT NODES"
        "</p></div>",
        unsafe_allow_html=True,
    )


def render_confirmation(token: str) -> None:
    st.markdown(
        f'<div class="confirm-box">'
        f'<div class="confirm-icon">✓</div>'
        f'<p class="confirm-title">Dispatch Order Transmitted</p>'
        f'<p class="confirm-note">Your order has been securely logged in our fulfillment network.</p>'
        f'<div class="confirm-token">{html.escape(token)}</div>'
        f'<p class="confirm-note">Save this Tracking ID. Our team will contact you via WhatsApp shortly.</p>'
        f"</div>",
        unsafe_allow_html=True,
    )


# ── Customer view ─────────────────────────────────────────────────────────────
def render_method_tabs() -> None:
    st.markdown(
        '<p class="section-title">Order Transmission Method</p>'
        '<p class="section-desc">Select how you wish to submit your pharmaceutical request</p>',
        unsafe_allow_html=True,
    )

    mode = st.session_state.order_mode
    st.markdown('<div class="method-grid">', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        css = "method-active" if mode == "prescription" else ""
        st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
        if st.button(
            "📸 Upload Digital Prescription\n(Parchi Upload)",
            key="btn_prescription",
            use_container_width=True,
        ):
            st.session_state.order_mode = "prescription"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        css = "method-active" if mode == "text" else ""
        st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
        if st.button(
            "✍️ Enter Medicine Text Grid\n(Naam Likhein)",
            key="btn_text",
            use_container_width=True,
        ):
            st.session_state.order_mode = "text"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_order_collector():
    prescription_file = None

    if st.session_state.order_mode == "prescription":
        st.markdown(
            '<div class="utility-panel">'
            '<p class="section-title">📸 Digital Prescription Upload</p>'
            '<p class="section-desc">Upload JPG, JPEG, or PNG format prescription document</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        prescription_file = st.file_uploader(
            "prescription_upload",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="rx_uploader",
        )
        if prescription_file:
            st.image(prescription_file, caption="Prescription Preview", use_container_width=True)
    else:
        st.markdown(
            '<div class="utility-panel">'
            '<p class="section-title">✍️ Medicine Text Grid</p>'
            '<p class="section-desc">Enter each medicine on a separate line</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        text = st.text_area(
            "medicine_grid",
            value=st.session_state.medicine_text,
            placeholder="Panadol 500mg\nAugmentin 625mg\nORS Sachets",
            height=130,
            label_visibility="collapsed",
            key="medicine_area",
        )
        st.session_state.medicine_text = text

    return prescription_file


def render_customer_form() -> None:
    dual_label(
        "Apna Name (Full Name) *",
        "Yahan apna naam likhein",
    )
    name = st.text_input("name_field", placeholder="Ahmed Khan", label_visibility="collapsed")

    dual_label(
        "WhatsApp Contact Number *",
        "Dawaiyon ki detail ke liye mobile number",
    )
    phone = st.text_input("phone_field", placeholder="03XX XXXXXXX", label_visibility="collapsed")

    dual_label(
        "Ghar ka Pata (Delivery Address) *",
        "Ghar ka mukammal pata likhein",
    )
    address = st.text_area(
        "address_field",
        placeholder="House #, Street, Area, City",
        height=90,
        label_visibility="collapsed",
    )

    return name, phone, address


def submit_order(name: str, phone: str, address: str, prescription_file) -> None:
    errors = []
    if not name.strip():
        errors.append("Please enter your full name / Apna naam likhein")
    if not phone.strip():
        errors.append("Please enter WhatsApp number / Mobile number darj karein")
    if not address.strip():
        errors.append("Please enter delivery address / Pata likhein")

    mode = st.session_state.order_mode
    if mode == "prescription" and not prescription_file:
        errors.append("Please upload prescription / Parchi upload karein")
    if mode == "text" and not st.session_state.medicine_text.strip():
        errors.append("Please enter medicines / Dawai ka naam likhein")

    if errors:
        for err in errors:
            show_message(err, "error")
        return

    image_path = None
    medicines = st.session_state.medicine_text.strip() or None

    if prescription_file:
        image_path = db.save_prescription_file(prescription_file)

    order_id = db.create_order(
        name=name.strip(),
        phone=phone.strip(),
        address=address.strip(),
        medicines=medicines,
        image_path=image_path,
    )

    st.session_state.order_confirmed = True
    st.session_state.confirmed_order_id = order_id
    st.session_state.medicine_text = ""
    st.rerun()


def render_utility_tools() -> None:
    st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

    st.markdown(
        '<div class="utility-panel">'
        '<p class="section-title">🔄 Formula Substitute Database</p>'
        '<p class="section-desc">Query bio-equivalent alternatives for optimized pricing</p>'
        "</div>",
        unsafe_allow_html=True,
    )
    query = st.text_input(
        "substitute_query",
        placeholder="Panadol, Augmentin, Omeprazole…",
        label_visibility="collapsed",
        key="sub_search",
    )
    if query.strip():
        alt = find_substitute(query)
        if alt:
            st.markdown(
                f'<div class="substitute-alert">'
                f"💡 <strong>Verified Bio-Equivalent Substitution:</strong> "
                f"{html.escape(alt)} "
                f"<em>(Identical Quality, Optimized Lower Price Matrix)</em>"
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            show_message(
                "Try: Panadol, Augmentin, Omeprazole, Metformin, Brufen",
                "info",
            )

    st.markdown(
        '<div class="utility-panel">'
        '<p class="section-title">⏰ Chronic Logistics Auto-Refill</p>'
        '<p class="section-desc">Register for automated monthly drug delivery refills</p>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="refill-card">', unsafe_allow_html=True)
    with st.form("refill_registry", clear_on_submit=True):
        dual_label("Registry Name", "Mareez ka poora naam")
        r_name = st.text_input("refill_name", label_visibility="collapsed")

        dual_label("WhatsApp Number", "Monthly reminder ke liye number")
        r_phone = st.text_input("refill_phone", label_visibility="collapsed")

        st.markdown('<div class="refill-btn">', unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🔔 Activate Auto-Refill Registry",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not r_name.strip() or not r_phone.strip():
                show_message("Name and phone are required / Naam aur number zaroori hain", "error")
            else:
                db.add_reminder(r_name.strip(), r_phone.strip())
                show_message(
                    "✓ Auto-Refill Registry activated. Monthly reminders will be scheduled.",
                    "success",
                )
    st.markdown("</div>", unsafe_allow_html=True)


def render_customer_view() -> None:
    render_welcome_banner()

    if st.session_state.order_confirmed:
        render_confirmation(st.session_state.confirmed_order_id)
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("Submit Another Order", use_container_width=True):
            st.session_state.order_confirmed = False
            st.session_state.confirmed_order_id = ""
            st.session_state.order_mode = "prescription"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        render_utility_tools()
        render_executive_footer()
        return

    st.markdown(
        '<div class="utility-panel">'
        '<p class="section-title">Pharmaceutical Dispatch Request</p>'
        '<p class="section-desc">Complete the compliance form below to initiate your order</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    render_method_tabs()
    rx_file = render_order_collector()
    name, phone, address = render_customer_form()

    st.markdown('<div class="dispatch-btn">', unsafe_allow_html=True)
    if st.button("🚀 TRANSMIT DISPATCH ORDER", use_container_width=True):
        submit_order(name, phone, address, rx_file)
    st.markdown("</div>", unsafe_allow_html=True)

    render_utility_tools()
    render_executive_footer()


# ── Admin desk ────────────────────────────────────────────────────────────────
def render_admin_login() -> None:
    st.markdown(
        '<div class="admin-login-box">'
        '<div class="admin-lock">🔐</div>'
        '<p class="admin-login-title">Admin Desk Access</p>'
        '<p class="admin-login-sub">Chishtia Medical Store — Authorized Personnel Only</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 2, 1])
    with center:
        password = st.text_input(
            "admin_password",
            type="password",
            placeholder="Enter access password",
            label_visibility="collapsed",
        )
        st.markdown('<div class="admin-signin">', unsafe_allow_html=True)
        if st.button("Authenticate & Enter", use_container_width=True):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                show_message("Access denied. Invalid credentials.", "error")
        st.markdown("</div>", unsafe_allow_html=True)


def render_order_node(order: dict) -> None:
    status = order["status"]
    badge_cls = "badge-delivered" if status == "Delivered" else "badge-pending"
    safe_id = html.escape(order["id"])
    safe_time = html.escape(order["timestamp"])
    safe_name = html.escape(order["name"])
    safe_phone = html.escape(order["phone"])
    safe_address = html.escape(order["address"])
    wa = whatsapp_href(order["phone"])

    st.markdown(
        f'<div class="order-node">'
        f'<div class="order-node-head">'
        f'<div><p class="order-id-text">{safe_id}</p>'
        f'<p class="order-time-text">{safe_time}</p></div>'
        f'<span class="status-badge {badge_cls}">{html.escape(status)}</span>'
        f"</div></div>",
        unsafe_allow_html=True,
    )

    col_info, col_rx = st.columns([1.1, 1])

    with col_info:
        st.markdown(
            f'<p class="field-label-sm">Client</p>'
            f'<p class="info-text"><strong>{safe_name}</strong></p>'
            f'<p class="field-label-sm">WhatsApp</p>'
            f'<p class="info-text"><a href="{wa}" target="_blank">{safe_phone}</a></p>'
            f'<p class="field-label-sm">Route Data</p>'
            f'<p class="info-text">{safe_address}</p>',
            unsafe_allow_html=True,
        )
        if order["medicines"]:
            meds = html.escape(order["medicines"])
            st.markdown(
                f'<p class="field-label-sm">Text Grid Medicines</p>'
                f'<div class="medicine-grid-box">{meds}</div>',
                unsafe_allow_html=True,
            )

    with col_rx:
        st.markdown('<p class="field-label-sm">Prescription Document</p>', unsafe_allow_html=True)
        path = order.get("image_path")
        if path and Path(path).exists():
            st.markdown('<div class="rx-preview-frame">', unsafe_allow_html=True)
            st.image(path, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="rx-empty">No prescription document attached</div>',
                unsafe_allow_html=True,
            )

    is_pending = status != db.STATUS_DELIVERED
    btn_wrap = "fulfill-btn" if is_pending else "fulfill-btn done"
    btn_label = "Authorize Fulfilled State" if is_pending else "✓ Fulfillment Complete"

    st.markdown(f'<div class="{btn_wrap}">', unsafe_allow_html=True)
    if st.button(btn_label, key=f"fulfill_{order['id']}", use_container_width=True):
        if is_pending:
            db.update_order_status(order["id"], db.STATUS_DELIVERED)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)


def render_admin_dashboard() -> None:
    head_l, head_r = st.columns([4, 1])
    with head_l:
        st.markdown(
            '<p class="admin-heading">Chishtia <span>Admin Desk</span></p>',
            unsafe_allow_html=True,
        )
    with head_r:
        st.markdown('<div class="admin-logout">', unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    metrics = db.get_metrics()
    st.markdown(
        f'<div class="metric-grid">'
        f'<div class="metric-card"><p class="metric-value">{metrics["total"]}</p>'
        f'<p class="metric-label">Gross Received</p></div>'
        f'<div class="metric-card await"><p class="metric-value">{metrics["pending"]}</p>'
        f'<p class="metric-label">Awaiting Dispatch</p></div>'
        f'<div class="metric-card done"><p class="metric-value">{metrics["completed"]}</p>'
        f'<p class="metric-label">Fulfillment Complete</p></div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<p class="feed-title">Dynamic Order Feed — Newest First</p>', unsafe_allow_html=True)
    orders = db.get_all_orders()

    if not orders:
        st.markdown(
            '<div class="empty-feed">No active orders. Incoming dispatch requests will appear here.</div>',
            unsafe_allow_html=True,
        )
        return

    for order in orders:
        render_order_node(order)


def render_admin_view() -> None:
    if st.session_state.admin_logged_in:
        render_admin_dashboard()
    else:
        render_admin_login()


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    st.set_page_config(
        page_title="Chishtia Medical Store",
        page_icon="💊",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    load_css()
    init_session_state()

    render_brand_header(admin=is_admin_route())

    if is_admin_route():
        render_admin_view()
    else:
        render_customer_view()


if __name__ == "__main__":
    main()
