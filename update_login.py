import textwrap

code = '''import streamlit as st
import sys
import base64
from pathlib import Path

# Setup path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

st.set_page_config(page_title="Login - Smart Loan System", layout="wide", initial_sidebar_state="collapsed")

css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stSidebarNav"], [data-testid="stHeader"] {
    display: none !important;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    margin: 0 !important;
}
[data-testid="stAppViewBlockContainer"] {
    max-width: 100% !important;
    padding: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}
.stApp {
    background: #F0F5FA !important;
    background-image: 
        radial-gradient(circle at 90% 30%, rgba(208, 227, 247, 0.8) 0%, transparent 50%),
        radial-gradient(circle at 10% 80%, rgba(208, 227, 247, 0.8) 0%, transparent 50%) !important;
}

/* Streamlit grid layout */
[data-testid="stHorizontalBlock"] {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    align-items: center;
    gap: 40px !important;
    padding: 20px;
}

/* LEFT COLUMN */
.left-content {
    padding: 10px 40px;
}
.logo-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}
.logo-icon { font-size: 28px; color: #1769E0; }
.logo-text { font-size: 22px; font-weight: 800; color: #1769E0; line-height: 1.1; }
.logo-text span { font-weight: 500; font-size: 14px; color: #64748B; display: block; }

.main-title {
    font-size: 44px;
    font-weight: 800;
    line-height: 1.15;
    color: #14213D;
    margin-bottom: 16px;
}
.main-title .blue { color: #1769E0; }
.main-desc {
    font-size: 16px;
    color: #475569;
    margin-bottom: 32px;
    line-height: 1.5;
    max-width: 90%;
}

.split-layout {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
}
.feature-list {
    flex: 1.2;
    min-width: 280px;
}
.illustration-wrapper {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}
.illustration-img {
    width: 100%;
    max-width: 320px;
    display: block;
    border-radius: 16px;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
}
.feat-icon {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.fi-1 { background: #E1EFFE; color: #1769E0; }
.fi-2 { background: #F3E8FF; color: #9333EA; }
.fi-3 { background: #DCFCE7; color: #16A34A; }
.feat-text h4 { margin: 0 0 4px 0; font-size: 15px; font-weight: 700; color: #14213D; }
.feat-text p { margin: 0; font-size: 13px; color: #64748B; line-height: 1.4; }

.bottom-benefits {
    display: flex;
    align-items: center;
    gap: 24px;
    margin-top: 20px;
    border-top: 1px solid rgba(0,0,0,0.08);
    padding-top: 20px;
}
.benefit { 
    display: flex; 
    align-items: center; 
    gap: 10px; 
    padding-right: 24px;
    border-right: 1px solid rgba(0,0,0,0.1);
}
.benefit:last-child {
    border-right: none;
    padding-right: 0;
}
.benefit i { font-size: 22px; color: #1769E0; }
.benefit-txt { font-size: 12px; font-weight: 600; color: #475569; line-height: 1.3; }
.benefit-txt span { color: #14213D; font-weight: 700; display: block; }

/* RIGHT COLUMN (CARD) */
[data-testid="stColumn"]:nth-child(2) {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 48px 40px !important;
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05), 0 0 20px rgba(0,0,0,0.02);
    border: 1px solid rgba(255,255,255,0.8);
    position: relative;
    z-index: 10;
}

.card-header { text-align: center; margin-bottom: 32px; }
.card-icon {
    width: 60px;
    height: 60px;
    background: #EFF6FF;
    color: #1769E0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    margin: 0 auto 20px auto;
}
.card-title { font-size: 26px; font-weight: 800; color: #14213D; margin-bottom: 12px; }
.card-sub { font-size: 14px; color: #64748B; line-height: 1.5; }

/* Form inputs */
[data-testid="stForm"] { background: transparent !important; border: none !important; padding: 0 !important; }
.stTextInput > div > div > input {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 14px 16px 14px 44px !important;
    font-size: 15px !important;
    color: #14213D !important;
}
.stTextInput > div > div > input:focus { border-color: #1769E0 !important; box-shadow: 0 0 0 3px rgba(23,105,224,0.1) !important; }
.stTextInput > label { font-size: 14px !important; font-weight: 600 !important; color: #1E293B !important; padding-bottom: 6px !important; }

/* Icons in inputs */
.stTextInput:nth-of-type(1) > div > div > input {
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%2394A3B8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z'></path><polyline points='22,6 12,13 2,6'></polyline></svg>") !important;
    background-repeat: no-repeat !important;
    background-position: 14px center !important;
}
.stTextInput:nth-of-type(2) > div > div > input {
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%2394A3B8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='11' width='18' height='11' rx='2' ry='2'></rect><path d='M7 11V7a5 5 0 0 1 10 0v4'></path></svg>") !important;
    background-repeat: no-repeat !important;
    background-position: 14px center !important;
}

/* Submit Button */
[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    background: #1769E0 !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 16px !important;
    border-radius: 12px !important;
    border: none !important;
    margin-top: 16px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background: #1557C0 !important;
}

.secure-footer {
    text-align: center;
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid #E2E8F0;
    font-size: 13px;
    color: #64748B;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

@media (max-width: 1100px) {
    .split-layout { flex-direction: column; align-items: flex-start; }
    .illustration-wrapper { width: 100%; margin-top: 20px; }
}
@media (max-width: 900px) {
    [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    .left-content { padding: 20px; }
    [data-testid="stColumn"]:nth-child(2) { padding: 30px 20px !important; }
    .bottom-benefits { flex-wrap: wrap; }
    .benefit { border-right: none; width: 100%; }
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

if st.session_state.get("authenticated", False):
    st.switch_page("pages/01_Home.py")

if "logged_out" in st.session_state:
    del st.session_state["logged_out"]

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

img_path = Path(__file__).resolve().parent.parent.parent / "assets" / "login_illustration.jpg"
img_b64 = get_base64_of_bin_file(img_path)

col1, col2 = st.columns([1.3, 1], gap="large")

left_html = f"""
<div class="left-content">
<div class="logo-bar">
<div class="logo-icon">🏦</div>
<div class="logo-text">Smart Loan<br><span>Risk & Approval System</span></div>
</div>
<div class="main-title"><span class="blue">Smart Loan</span><br>Risk & Approval System</div>
<div class="main-desc">Intelligent loan risk assessment and approval support powered by data analytics and machine learning.</div>
<div class="split-layout">
<div class="feature-list">
<div class="feature-item">
<div class="feat-icon fi-1">📊</div>
<div class="feat-text">
<h4>Data-Driven Risk Assessment</h4>
<p>Analyze applicant profiles with advanced analytics and insights.</p>
</div>
</div>
<div class="feature-item">
<div class="feat-icon fi-2">⚙️</div>
<div class="feat-text">
<h4>ML-Based Loan Prediction</h4>
<p>Accurate and efficient loan approval predictions using machine learning.</p>
</div>
</div>
<div class="feature-item">
<div class="feat-icon fi-3">🛡️</div>
<div class="feat-text">
<h4>Explainable Decisions</h4>
<p>Transparent and interpretable results for better decision making.</p>
</div>
</div>
</div>
<div class="illustration-wrapper">
<img src="data:image/jpeg;base64,{img_b64}" class="illustration-img" alt="Illustration" />
</div>
</div>
<div class="bottom-benefits">
<div class="benefit">
<i>👥</i>
<div class="benefit-txt">Better<br><span>Risk Analysis</span></div>
</div>
<div class="benefit">
<i>📈</i>
<div class="benefit-txt">Higher<br><span>Approval Accuracy</span></div>
</div>
<div class="benefit">
<i>🛡️</i>
<div class="benefit-txt">Smarter<br><span>Financial Decisions</span></div>
</div>
</div>
</div>
"""

with col1:
    st.markdown(left_html, unsafe_allow_html=True)

right_header = """
<div class="card-header">
<div class="card-icon">🏦</div>
<div class="card-title">Welcome Back</div>
<div class="card-sub">Sign in to continue to Smart Loan<br>Risk & Approval System</div>
</div>
"""

right_footer = """
<div class="secure-footer">
🔒 Secure access to the Smart Loan<br>Risk & Approval System
</div>
"""

with col2:
    st.markdown(right_header, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="admin@smartloan.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submit = st.form_submit_button("Sign In →", use_container_width=True)

        if submit:
            if email == "admin@smartloan.com" and password == "admin123":
                st.session_state["authenticated"] = True
                st.switch_page("pages/01_Home.py")
            else:
                st.error("Invalid credentials. Use admin@smartloan.com / admin123")
                
    st.markdown(right_footer, unsafe_allow_html=True)
'''

with open('frontend/pages/00_Login.py', 'w', encoding='utf-8') as f:
    f.write(code)
