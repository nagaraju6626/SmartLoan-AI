import streamlit as st

def initialize_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

def toggle_theme():
    initialize_theme()
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

def apply_theme():
    initialize_theme()
    theme = st.session_state.theme
    
    # Base CSS that applies to the theme (structural, shadows, radiuses)
    base_css = """
    <style>
    /* Search Bar Base Styling */
    div[data-testid="stTextInput"] > div > div > input {
        border-radius: 20px !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    
    /* Buttons Base Styling */
    div[data-testid="column"] > div > div > div > div > button {
        height: 44px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    div[data-testid="column"] > div > div > div > div[data-testid="stPopover"] > button {
        height: 44px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)
    
    if theme == "light":
        light_css = """
        <style>
        :root {
            --primary-color: #2563EB !important;
            --background-color: #F8FAFC !important;
            --secondary-background-color: #FFFFFF !important;
            --text-color: #0F172A !important;
        }
        .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
        
        /* Search Bar & Header Controls (Light) */
        div[data-testid="stTextInput"] > div > div > input {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #334155 !important;
        }
        div[data-testid="stTextInput"] > div > div > input::placeholder {
            color: #64748B !important;
        }
        div[data-testid="column"] > div > div > div > div > button {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #334155 !important;
        }
        div[data-testid="column"] > div > div > div > div[data-testid="stPopover"] > button {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #1E293B !important;
        }
        
        /* Force Hamburger Toggle Icon Visibility in ALL states */
        div[data-testid="column"]:nth-of-type(1) button p,
        div[data-testid="column"]:nth-of-type(1) button span,
        div[data-testid="column"]:nth-of-type(1) button svg {
            color: #334155 !important;
            fill: #334155 !important;
            stroke: #334155 !important;
            visibility: visible !important;
            opacity: 1 !important;
            display: block !important;
            text-indent: 0 !important;
        }
        </style>
        """
        st.markdown(light_css, unsafe_allow_html=True)
    else:
        dark_css = """
        <style>
        :root {
            --primary-color: #3B82F6 !important;
            --background-color: #0F172A !important;
            --secondary-background-color: #1E293B !important;
            --text-color: #F1F5F9 !important;
        }
        
        /* Main Backgrounds */
        .stApp, .main, .block-container, header { 
            background-color: #0F172A !important; 
            color: #F1F5F9 !important; 
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1E293B !important;
            border-right: 1px solid #334155 !important;
        }
        
        /* Text overrides (be careful not to override button text that should be white) */
        h1, h2, h3, h4, h5, h6, label, p:not(button p):not(.result-card p) {
            color: #F1F5F9 !important;
        }
        small, .metric-label, .fc-sub, .fc-title {
            color: #94A3B8 !important;
        }
        
        /* Override specifically hardcoded light colors in inline styles */
        div[style*="background-color: #F8FAFC"], 
        div[style*="background: #F8FAFC"],
        div[style*="background:#F8FAFC"],
        div[style*="background:#F8FAFC;"] {
            background-color: #1E293B !important;
            border-color: #334155 !important;
            color: #F1F5F9 !important;
        }
        div[style*="background-color: #FEE2E2"] {
            background-color: #450a0a !important;
            border-color: #7f1d1d !important;
        }
        div[style*="color: #334155"], div[style*="color:#334155"], 
        span[style*="color: #334155"], span[style*="color:#334155"],
        div[style*="color: #0F172A"], div[style*="color:#0F172A"],
        span[style*="color: #0F172A"], span[style*="color:#0F172A"],
        div[style*="color: #475569"], div[style*="color:#475569"],
        div[style*="color: #64748B"], div[style*="color:#64748B"],
        small[style*="color:#64748B"] {
            color: #F1F5F9 !important;
        }
        
        /* Info / Result Cards from specific pages */
        .info-card {
            background-color: #1E293B !important;
            border: 1px solid #334155 !important;
        }
        .info-card h4, .info-card p, .info-card b, .info-card span {
            color: #F1F5F9 !important;
        }
        
        /* Dataframes & Tables */
        div[data-testid="stDataFrame"] * {
            color: #F1F5F9 !important;
        }
        
        /* Inputs: Text, Number, Selectbox, Textarea */
        div[data-testid="stTextInput"] > div > div > input,
        div[data-testid="stNumberInput"] > div > div > input,
        div[data-testid="stSelectbox"] > div > div,
        div[data-testid="stTextArea"] > div > textarea {
            background-color: #1E293B !important;
            border: 1px solid #334155 !important;
            color: #F1F5F9 !important;
        }
        div[data-testid="stTextInput"] > div > div > input::placeholder {
            color: #94A3B8 !important;
        }
        
        /* Header Search Bar & Theme Button */
        div[data-testid="column"] > div > div > div > div > button:not([kind="primary"]) {
            background-color: #1E293B !important;
            border: 1px solid #334155 !important;
            color: #F1F5F9 !important;
        }
        div[data-testid="column"] > div > div > div > div[data-testid="stPopover"] > button {
            background-color: #1E293B !important;
            border: 1px solid #334155 !important;
            color: #F1F5F9 !important;
        }
        
        /* Hamburger / SVG */
        div[data-testid="column"]:nth-of-type(1) button p,
        div[data-testid="column"]:nth-of-type(1) button span,
        div[data-testid="column"]:nth-of-type(1) button svg,
        header svg {
            color: #F1F5F9 !important;
            fill: #F1F5F9 !important;
            stroke: #F1F5F9 !important;
        }
        
        /* Home Page Specific Overrides */
        .hero-section {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
            border-color: #334155 !important;
        }
        .hero-title, .hero-subtitle, .fc-value, .fc-list {
            color: #F1F5F9 !important;
        }
        .float-card, .btn-secondary {
            background-color: #1E293B !important;
            border-color: #334155 !important;
            color: #F1F5F9 !important;
        }
        .visual-core {
            border-color: #1E293B !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Metrics */
        div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] {
            color: #F1F5F9 !important;
        }
        
        /* New Applicant / Result Cards */
        .low-risk { background: linear-gradient(135deg, #064E3B 0%, #065F46 100%) !important; border-color: #10B981 !important; }
        .medium-risk { background: linear-gradient(135deg, #78350F 0%, #92400E 100%) !important; border-color: #F59E0B !important; }
        .high-risk { background: linear-gradient(135deg, #7F1D1D 0%, #991B1B 100%) !important; border-color: #EF4444 !important; }
        .risk-title, .risk-conf, .risk-msg { color: #F1F5F9 !important; }
        .low-text { color: #34D399 !important; }
        .medium-text { color: #FBBF24 !important; }
        .high-text { color: #F87171 !important; }
        </style>
        """
        st.markdown(dark_css, unsafe_allow_html=True)

def apply_chart_style(fig):
    theme = st.session_state.get("theme", "light")
    if theme == "dark":
        fig.update_layout(
            plot_bgcolor="#0F172A",
            paper_bgcolor="#0F172A",
            margin=dict(t=40, l=20, r=20, b=20),
            font=dict(color="#F1F5F9"),
            title_font=dict(color="#F1F5F9", size=16),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_xaxes(showgrid=False, linecolor="#334155", gridcolor="#334155")
        fig.update_yaxes(showgrid=True, gridcolor="#1E293B", linecolor="#334155")
    else:
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=40, l=20, r=20, b=20),
            font=dict(color="#334155"),
            title_font=dict(color="#0F172A", size=16),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_xaxes(showgrid=False, linecolor="#E2E8F0", gridcolor="#E2E8F0")
        fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", linecolor="#E2E8F0")
    return fig
