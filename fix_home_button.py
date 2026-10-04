import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First, restore the previous intercept block removal
content = re.sub(r'# Intercept query parameter.*?st\.switch_page\("pages/02_Data_Upload\.py"\)', '', content, flags=re.DOTALL)

# Re-build the Hero Section using st.columns but with PERFECT CSS wrapping
old_hero_pattern = r'st\.markdown\(f"""<div class="hero-section">.*?</div></div>""", unsafe_allow_html=True\)'

# The new python code for the hero section
new_hero = '''
st.markdown("""
<style>
/* Target the first stHorizontalBlock which contains our columns */
div[data-testid="stHorizontalBlock"]:first-of-type {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border-radius: 20px;
    padding: 48px;
    margin-bottom: 32px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    border: 1px solid #BFDBFE;
    align-items: center !important;
    gap: 0 !important;
}

/* Remove internal padding from columns */
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"] {
    padding: 0 !important;
}

/* Ensure right column can relative position its children */
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:nth-of-type(2) {
    display: flex;
    justify-content: flex-end;
    position: relative;
    min-height: 400px;
}

/* Style the native Streamlit button to match .btn-primary */
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] button {
    background-color: #2563EB !important;
    color: white !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
    margin-top: 10px;
    margin-bottom: 25px;
    transition: all 0.2s ease !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] button:hover {
    background-color: #1D4ED8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.3) !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] button p {
    color: white !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="hero-left" style="max-width: 100%; padding-right: 20px;">
        <div class="hero-label">AI-POWERED LOAN ANALYSIS</div>
        <div class="hero-title">Smart Loan Risk &<br><span>Approval System</span></div>
        <div class="hero-subtitle">Predict loan risk, analyze applicant data, and make smarter decisions<br>with Machine Learning and Explainable AI.</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("\U0001F680 Get Started", type="primary", use_container_width=False):
        st.switch_page("pages/02_Data_Upload.py")
        
    st.markdown("""
    <div class="hero-left" style="max-width: 100%;">
        <div class="hero-features">
            <span>\U0001F52E AI Powered</span>
            <span>\U0001F4C8 High Accuracy</span>
            <span>\U0001F9E0 Explainable AI</span>
            <span>\U0001F464 New Applicant</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="hero-right" style="width: 100%; min-height: 400px; position: relative;">
        <div class="visual-core" style="background-image: url('data:image/jpeg;base64,{hero_img_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; background-color: transparent; border: none; box-shadow: none;"></div>
        <div class="float-card fc-1"><div class="fc-title">Risk Prediction</div><div class="fc-value success">LOW RISK</div><div class="fc-sub">87% Confidence</div></div>
        <div class="float-card fc-2"><div class="fc-title">Approval Chance</div><div class="fc-value success">92%</div><div class="fc-sub">High Probability</div></div>
        <div class="float-card fc-3"><div class="fc-title">AI Analysis</div><div class="fc-list"><div>\u2714 Income Verified</div><div>\u2714 Low Default Risk</div><div>\u2714 Good Credit Profile</div></div></div>
        <div class="float-card fc-4"><div class="fc-title">Decision</div><div class="fc-value success">\u2714 APPROVED</div></div>
    </div>
    """, unsafe_allow_html=True)
'''

content = re.sub(old_hero_pattern, new_hero, content, flags=re.DOTALL)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
