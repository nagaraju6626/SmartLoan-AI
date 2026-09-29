import streamlit as st

def load_css():
    if "sidebar_collapsed" not in st.session_state:
        st.session_state["sidebar_collapsed"] = False
    collapsed = st.session_state["sidebar_collapsed"]
    
    css = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
    /* Main typography and background */
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif !important; }}
    .stApp {{ background-color: #F8FAFC; }}
    
    /* Remove default Streamlit top padding to fix the huge blank space */
    .block-container {{ padding-top: 0rem !important; padding-left: 48px !important; padding-right: 48px !important; max-width: 1400px; margin-top: 0px !important; }}
    header[data-testid="stHeader"] {{ display: none !important; }}
    
    /* Completely hide markdown containers that only have <style> tags to remove their phantom gap */
    div[data-testid="stMarkdownContainer"]:has(> style:only-child) {{ display: none !important; }}
    div[data-testid="stVerticalBlock"] > div:has(style:only-child) {{ display: none !important; }}
    /* Specific targeted rule for element containers that hold our CSS blocks */
    div[data-testid="stElementContainer"]:has(> div[data-testid="stMarkdownContainer"] > style:only-child) {{ display: none !important; height: 0 !important; margin: 0 !important; padding: 0 !important; }}

    
    /* Hide native sidebar toggle and scrollbar */
    [data-testid="collapsedControl"] {{ display: none !important; }}
    [data-testid="stSidebar"] ::-webkit-scrollbar {{ display: none !important; }}
    
    /* Control sidebar width */
    [data-testid="stSidebar"] {{ 
        width: {'0px' if collapsed else '290px'} !important; 
        min-width: {'0px' if collapsed else '290px'} !important; 
        max-width: {'0px' if collapsed else '290px'} !important; 
        background-color: #0B172A !important; 
        transition: width 0.3s ease; 
        overflow-x: hidden; 
        {'padding: 0 !important;' if collapsed else ''}
        {'border-right: none !important;' if collapsed else ''}
    }}
    
    /* Set text colors */
    [data-testid="stSidebar"] * {{ 
        color: #E2E8F0 !important; 
        {'display: none !important;' if collapsed else ''}
    }}
    
    /* Adjust main content left margin */
    [data-testid="stSidebar"] + section {{ 
        margin-left: {'0px' if collapsed else '290px'} !important; 
        transition: margin-left 0.3s ease; 
    }}
    
    /* Hide native default multipage nav */
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    
    /* Hide text when collapsed */
    {'[data-testid="stSidebar"] p { display: none !important; }' if collapsed else ''}
    {'[data-testid="stSidebar"] .st-emotion-cache-1wivap2 { display: none !important; }' if collapsed else ''}
    
    /* Custom Navigation Container */
    .custom-nav-container {{ display: flex; flex-direction: column; gap: 4px; margin-top: -10px; padding-bottom: 80px; }}
    
    /* Override st.page_link styles for sidebar */
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {{ 
        background-color: transparent; 
        color: #E2E8F0 !important; 
        border-radius: 8px; 
        margin: 2px 12px; 
        padding: 8px 12px; 
    }}
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p {{
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }}
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {{ background-color: rgba(255,255,255,0.05); }}
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][data-active="true"], 
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {{ 
        background-color: #1E3A8A !important; 
        font-weight: 600; 
    }}
    
    /* Logo */
    .custom-logo {{ display: flex; align-items: center; gap: 12px; padding: {'0px' if collapsed else '44px 20px 24px 20px'}; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 1.1rem; font-weight: 800; color: white; white-space: nowrap; }}
    .custom-logo-text {{ {'display: none;' if collapsed else 'display: block; line-height: 1.3;'} }}
    
    /* Bottom User Section */
    .sidebar-bottom {{ position: fixed; bottom: 0; left: 0; width: {'0px' if collapsed else '290px'}; padding: {'0px' if collapsed else '16px 20px'}; background-color: #0B172A; border-top: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center; color: #94A3B8; z-index: 100; transition: width 0.3s ease; }}
    .user-info {{ display: flex; align-items: center; gap: 10px; font-size: 0.95rem; }}
    .user-info span {{ {'display: none;' if collapsed else 'display: block; white-space: nowrap;'} }}
    .settings-icon {{ {'display: none;' if collapsed else 'display: block;'} }}
    
    /* Top Header */
    .top-header {{ display: flex; justify-content: space-between; align-items: center; height: 80px; padding: 0 24px; background-color: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; margin-bottom: 32px; }}
    .search-bar {{ display: flex; align-items: center; background: #F1F5F9; padding: 10px 16px; border-radius: 20px; width: 280px; color: #64748B; font-size: 0.9rem; gap: 8px; }}
    .header-icons {{ display: flex; align-items: center; gap: 1.5rem; font-size: 1.1rem; color: #64748B; }}
    .avatar-circle {{ background: #2563EB; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: bold; }}
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
