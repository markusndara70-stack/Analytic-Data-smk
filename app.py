import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from hashlib import sha256

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="SMKN 1 Denpasar",
    layout="wide"
)

# =========================
# CSS STYLING
# =========================
st.markdown("""
<style>
    /* HEADER */
    .header-box {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }

    .header-box h1 {
        margin: 0.5rem 0;
        color: #1f2937;
    }

    .header-box p {
        margin: 0;
        color: #6b7280;
        font-size: 0.9rem;
    }

    /* FORM CONTAINER */
    .form-container {
        max-width: 500px;
        margin: 0 auto;
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* TAB */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
    }

    /* BUTTON */
    .stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 6px;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
    }

    /* FOOTER */
    .footer-box {
        background: #1f2937;
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
    }

    .footer-box p {
        margin: 0.5rem 0;
        color: #d1d5db;
    }

    /* DASHBOARD LAYOUT */
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .dashboard-header h1 {
        margin: 0;
        color: #1f2937;
    }

    .user-info {
        color: #6b7280;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# USER MANAGEMENT
# =========================
USERS_FILE = "users.json"

def load_users():
    """Load users dari file JSON"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Simpan users ke file JSON"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Hash password"""
    return sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password"""
    return hash_password(password) == hashed

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_name = None

# =========================
# LOGIN & REGISTER
# =========================
if not st.session_state.logged_in:
    # HEADER
    st.markdown("""
    <div class="header-box">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏫</div>
        <h1>SMKN 1 Denpasar</h1>
        <p>Sistem Informasi Sekolah</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FORM CONTAINER
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # TAB LOGIN & DAFTAR
    tab1, tab2 = st.tabs(["📝 Login", "📋 Daftar"])
    
    with tab1:
        st.subheader("Masuk ke Akun")
        email = st.text_input("Email", placeholder="masukkan@email.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Masukkan password", key="login_password")
        
        if st.button("🔓 Masuk", use_container_width=True, key="login_btn"):
            if not email or not password:
                st.error("⚠️ Email dan password harus diisi!")
            else:
                users = load_users()
                if email in users and verify_password(password, users[email]['password']):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_name = users[email]['name']
                    st.success("✅ Login berhasil!")
                    st.rerun()
                else:
                    st.error("❌ Email atau password salah!")
    
    with tab2:
        st.subheader("Buat Akun Baru")
        name = st.text_input("Nama Lengkap", placeholder="Masukkan nama Anda", key="register_name")
        email = st.text_input("Email", placeholder="masukkan@email.com", key="register_email")
        password = st.text_input("Password", type="password", placeholder="Min 6 karakter", key="register_password")
        confirm_password = st.text_input("Konfirmasi Password", type="password", placeholder="Ulangi password", key="register_confirm")
        
        if st.button("✓ Daftar", use_container_width=True, key="register_btn"):
            if not name or not email or not password or not confirm_password:
                st.error("⚠️ Semua field harus diisi!")
            elif len(password) < 6:
                st.error("❌ Password minimal 6 karakter!")
            elif password != confirm_password:
                st.error("❌ Password tidak cocok!")
            else:
                users = load_users()
                if email in users:
                    st.error("❌ Email sudah terdaftar!")
                else:
                    users[email] = {
                        'name': name,
                        'password': hash_password(password),
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    save_users(users)
                    st.success("✅ Daftar berhasil! Silakan login")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FOOTER
    st.markdown("""
    <div class="footer-box">
        <p><strong>SMKN 1 Denpasar</strong></p>
        <p>© 2026 Sistem Informasi Sekolah. Semua hak dilindungi.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# DASHBOARD (Setelah Login)
# =========================
else:
    # HEADER DASHBOARD
    st.markdown(f"""
    <div class="dashboard-header">
        <h1>📊 Dashboard</h1>
        <div class="user-info">👤 {st.session_state.user_name}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # LOGOUT BUTTON
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.rerun()
    
    st.markdown("---")
    
    # STATS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Total Users", 42)
    with col2:
        st.metric("📊 Data Points", 1250)
    with col3:
        st.metric("📈 Growth", "12.5%")
    
    st.markdown("")
    
    # CHART
    chart_data = pd.DataFrame({
        'Minggu': ['Minggu 1', 'Minggu 2', 'Minggu 3', 'Minggu 4'],
        'Data A': [20, 35, 30, 50],
        'Data B': [25, 30, 45, 40]
    })
    
    st.bar_chart(chart_data.set_index('Minggu'))
    
    st.markdown("---")
    
    # FOOTER
    st.markdown("""
    <div class="footer-box">
        <p><strong>SMKN 1 Denpasar</strong></p>
        <p>© 2026 Sistem Informasi Sekolah. Semua hak dilindungi.</p>
    </div>
    """, unsafe_allow_html=True)
