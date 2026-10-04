import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First, let's extract the CSS for .hero-buttons, .btn-primary etc.
# We'll keep them in case they are used.
# But we need to replace the HERO SECTION part.

# Old Hero Section:
pattern = r'# HERO SECTION\n.*?# KPI SECTION'

# New Hero Section using Streamlit columns
new_hero = '''# HERO SECTION
st.markdown("""
<style>
/* Target the first stHorizontalBlock which will be our hero section */
div[data-testid="stHorizontalBlock"]:nth-of-type(1) {
    background: white;
    border-radius: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    padding: 40px 60px;
    align-items: center;
    margin-bottom: 32px;
}
/* Adjust internal padding for markdown blocks in the hero */
div[data-testid="stHorizontalBlock"]:nth-of-type(1) [data-testid="stMarkdownContainer"] p {
    margin-bottom: 0;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="hero-left" style="padding:0; width: 100%;">
        <div class="hero-label">AI-POWERED LOAN ANALYSIS</div>
        <div class="hero-title">Smart Loan Risk &<br><span>Approval System</span></div>
        <div class="hero-subtitle">Predict loan risk, analyze applicant data, and make smarter decisions<br>with Machine Learning and Explainable AI.</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("\U0001F680 Get Started", type="primary", use_container_width=False):
        st.switch_page("pages/02_Data_Upload.py")
        
    st.markdown("""
    <div class="hero-left" style="padding:0; width: 100%;">
        <div class="hero-features" style="margin-top: 24px;">
            <span>\U0001F9E0 AI Powered</span>
            <span>\u26A1 High Accuracy</span>
            <span>\U0001F6E1\uFE0F Explainable AI</span>
            <span>\U0001F195 New Applicant</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="hero-right" style="padding:0; width: 100%; margin:0;">
        <div class="visual-core" style="background-image: url('data:image/jpeg;base64,{hero_img_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; background-color: transparent; border: none; box-shadow: none;"></div>
        <div class="float-card fc-1"><div class="fc-title">Risk Prediction</div><div class="fc-value success">LOW RISK</div><div class="fc-sub">87% Confidence</div></div>
        <div class="float-card fc-2"><div class="fc-title">Approval Chance</div><div class="fc-value success">92%</div><div class="fc-sub">High Probability</div></div>
        <div class="float-card fc-3"><div class="fc-title">AI Analysis</div><div class="fc-list"><div>\u2714\uFE0F Income Verified</div><div>\u2714\uFE0F Low Default Risk</div><div>\u2714\uFE0F Good Credit Profile</div></div></div>
        <div class="float-card fc-4"><div class="fc-title">Decision</div><div class="fc-value success">\u2714\uFE0F APPROVED</div></div>
    </div>
    """, unsafe_allow_html=True)

# KPI SECTION'''

content = re.sub(pattern, new_hero, content, flags=re.DOTALL)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
