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
    page_title="Aplikasi Professional",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# GLOBAL STYLE
# =========================
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    :root {
        --primary-color: #2563eb;
        --secondary-color: #1e40af;
        --success-color: #16a34a;
        --danger-color: #dc2626;
        --dark-color: #1f2937;
        --light-color: #f3f4f6;
        --border-color: #e5e7eb;
    }

    body, html {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stApp {
        background: transparent !important;
    }

    /* HEADER */
    .header-main {
        background: white;
        padding: 1.5rem 2rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .logo-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #2563eb, #1e40af);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.5rem;
    }

    .logo-text h1 {
        margin: 0;
        color: #1f2937;
        font-size: 1.8rem;
        font-weight: 700;
    }

    .logo-text p {
        margin: 0;
        color: #6b7280;
        font-size: 0.85rem;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: #1f2937;
    }

    /* AUTH CONTAINER */
    .auth-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
        padding: 2rem;
    }

    .auth-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
        padding: 3rem;
        max-width: 450px;
        width: 100%;
        animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .auth-card .logo-section {
        justify-content: center;
        margin-bottom: 2rem;
    }

    .auth-card h2 {
        text-align: center;
        color: #1f2937;
        margin-bottom: 2rem;
        font-size: 1.75rem;
        font-weight: 700;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: #1f2937;
    }

    /* TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: #f3f4f6;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
        color: #6b7280;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        color: white !important;
    }

    /* FOOTER */
    .footer-main {
        background: #1f2937;
        color: white;
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
        border-radius: 12px 12px 0 0;
    }

    .footer-main p {
        margin: 0;
        color: #d1d5db;
    }

    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }

    .footer-links a {
        color: #9ca3af;
        text-decoration: none;
        transition: color 0.3s;
    }

    .footer-links a:hover {
        color: white;
    }

    /* BUTTONS */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
    }

    /* FORM INPUTS */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 2px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }

    /* ALERTS */
    .stAlert {
        border-radius: 8px !important;
        animation: slideIn 0.3s ease-out !important;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* LINK STYLING */
    .auth-link {
        text-align: center;
        margin-top: 1.5rem;
        color: #6b7280;
    }

    .auth-link a {
        color: #2563eb;
        text-decoration: none;
        font-weight: 600;
    }

    .auth-link a:hover {
        text-decoration: underline;
    }

    /* RESPONSIVE */
    @media (max-width: 768px) {
        .header-main {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
        }

        .auth-card {
            padding: 1.5rem;
        }

        .logo-text h1 {
            font-size: 1.3rem;
        }
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

if "page" not in st.session_state:
    st.session_state.page = "login"

# =========================
# HEADER
# =========================
def show_header():
    """Tampilkan header"""
    st.markdown("""
    <div class="header-main">
        <div class="logo-section">
            <div class="logo-icon">📊</div>
            <div class="logo-text">
                <h1>Aplikasi Professional</h1>
                <p>Sistem Manajemen Data Profesional</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.markdown(f"""
        <div class="user-info">
            <span>Selamat datang, <strong>{st.session_state.user_name}</strong></span>
        </div>
    </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
def show_footer():
    """Tampilkan footer"""
    st.markdown("""
    <div class="footer-main">
        <p><strong>Aplikasi Professional</strong> - Sistem Manajemen Data Terpadu</p>
        <div class="footer-links">
            <a href="#">Tentang Kami</a>
            <a href="#">Hubungi Kami</a>
            <a href="#">Kebijakan Privasi</a>
            <a href="#">Syarat Layanan</a>
        </div>
        <p>© 2026 Aplikasi Professional. Semua hak dilindungi.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# LOGIN PAGE
# =========================
def login_page():
    """Halaman Login"""
    pass

# =========================
# REGISTER PAGE
# =========================
def register_page():
    """Halaman Register"""
    pass

# =========================
# DASHBOARD PAGE
# =========================
def dashboard_page():
    """Halaman Dashboard"""
    show_header()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 📊 Dashboard")
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.session_state.page = "login"
            st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Total Users", 42)
    with col2:
        st.metric("📊 Data Points", 1250)
    with col3:
        st.metric("📈 Growth", "12.5%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart
    chart_data = pd.DataFrame({
        'Minggu': ['Minggu 1', 'Minggu 2', 'Minggu 3', 'Minggu 4'],
        'Data A': [20, 35, 30, 50],
        'Data B': [25, 30, 45, 40]
    })
    
    st.bar_chart(chart_data.set_index('Minggu'))
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    show_footer()

# =========================
# MAIN APP
# =========================
if st.session_state.logged_in:
    dashboard_page()
else:
    # HEADER
    show_header()
    
    # AUTH CONTAINER - CENTER
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="auth-card">
        <div class="logo-section" style="justify-content: center; margin-bottom: 2rem;">
            <div class="logo-icon">🏫</div>
        </div>
        <h2 style="text-align: center; margin-bottom: 0.5rem;">SMKN 1 Denpasar</h2>
        <p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Sistem Informasi Sekolah</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔓 Masuk", "📝 Daftar"])
        
        # LOGIN TAB
        with tab1:
            email = st.text_input("📧 Email", placeholder="masukkan@email.com", key="login_email")
            password = st.text_input("🔒 Password", type="password", placeholder="Masukkan password", key="login_password")
            
            if st.button("Masuk", use_container_width=True, key="login_btn"):
                if not email or not password:
                    st.error("❌ Email dan password harus diisi!")
                else:
                    users = load_users()
                    if email in users and verify_password(password, users[email]['password']):
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.user_name = users[email]['name']
                        st.session_state.page = "dashboard"
                        st.success("✅ Login berhasil!")
                        st.rerun()
                    else:
                        st.error("❌ Email atau password salah!")
            
            st.markdown("""
            <div class="auth-link">
                Belum punya akun? Buat akun di tab <strong>Daftar</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # REGISTER TAB
        with tab2:
            name = st.text_input("👤 Nama Lengkap", placeholder="Masukkan nama Anda", key="register_name")
            email = st.text_input("📧 Email", placeholder="masukkan@email.com", key="register_email")
            password = st.text_input("🔒 Password", type="password", placeholder="Min 6 karakter", key="register_password")
            confirm_password = st.text_input("✓ Konfirmasi Password", type="password", placeholder="Ulangi password", key="register_confirm")
            
            if st.button("Daftar", use_container_width=True, key="register_btn"):
                if not name or not email or not password or not confirm_password:
                    st.error("❌ Semua field harus diisi!")
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
            
            st.markdown("""
            <div class="auth-link">
                Sudah punya akun? Masuk di tab <strong>Masuk</strong>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # FOOTER
    show_footer()
