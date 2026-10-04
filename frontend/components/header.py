import streamlit as st

import os

import pandas as pd

from pathlib import Path

from frontend.components.theme import apply_theme

from frontend.components.navigation import toggle_sidebar



@st.cache_data(ttl=300, max_entries=20, show_spinner=False)

def perform_global_search(query, dataset_id):

    query = query.lower().strip()

    if not query:

        return []

    

    results = []

    

    # 1. Search Pages/Modules

    pages = {

        "home": ("pages/01_Home.py", "🏠 Home Dashboard"),

        "dashboard": ("pages/01_Home.py", "🏠 Dashboard"),

        "upload": ("pages/02_Data_Upload.py", "📂 Data Upload"),

        "data": ("pages/02_Data_Upload.py", "📂 Data Management"),

        "dataset": ("pages/02_Data_Upload.py", "📂 Dataset Settings"),

        "analysis": ("pages/04_Data_Analysis.py", "📈 Data Analysis"),

        "analytics": ("pages/04_Data_Analysis.py", "📈 Analytics & Charts"),

        "model": ("pages/05_Model_Training.py", "🤖 Model Training & Comparison"),

        "train": ("pages/05_Model_Training.py", "🤖 Train Models"),

        "compare": ("pages/05_Model_Training.py", "🤖 Compare Models"),

        "predict": ("pages/07_New_Applicant.py", "👤 New Applicant Prediction"),

        "new applicant": ("pages/07_New_Applicant.py", "👤 New Applicant Profile"),

        "explain": ("pages/08_Explainability.py", "💡 Explainability (SHAP)"),

        "shap": ("pages/08_Explainability.py", "💡 SHAP Values"),

        "report": ("pages/10_Reports.py", "📄 Reports Generation"),

        "export": ("pages/10_Reports.py", "📄 Export PDF/CSV"),

        "risk": ("pages/07_New_Applicant.py", "👤 Risk Assessment"),

        "approval": ("pages/07_New_Applicant.py", "👤 Loan Approval Prediction")

    }

    

    seen_pages = set()

    for kw, (page_path, title) in pages.items():

        if query in kw or kw in query:

            if page_path not in seen_pages:

                results.append({"type": "page", "path": page_path, "title": title, "desc": "Navigate to module"})

                seen_pages.add(page_path)

                

    # Direct match for general terms

    general_terms = ["loan", "risk", "cibil", "income", "amount", "dependents"]

    if any(gt in query for gt in general_terms) and "pages/04_Data_Analysis.py" not in seen_pages:

        results.append({"type": "page", "path": "pages/04_Data_Analysis.py", "title": "📈 Data Analysis", "desc": "Explore general loan, risk, and financial trends"})

        seen_pages.add("pages/04_Data_Analysis.py")

            

    # 2. Search Dataset (if available)

    if dataset_id:

        try:

            PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

            UPLOAD_DIR = os.path.join(PROJECT_ROOT, "data", "uploads")

            raw_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(dataset_id)]

            if raw_files:

                df = pd.read_csv(os.path.join(UPLOAD_DIR, raw_files[0]))

                

                # Check Applicant_ID first

                if "Applicant_ID" in df.columns:

                    matches = df[df["Applicant_ID"].astype(str).str.lower().str.contains(query, na=False)]

                    for _, row in matches.head(10).iterrows():

                        app_id = row["Applicant_ID"]

                        amount = row.get("Loan_Amount", "N/A")

                        status = row.get("Loan_Status", "Unknown")

                        results.append({

                            "type": "applicant",

                            "id": app_id,

                            "title": f"👤 Applicant: {app_id}",

                            "desc": f"Loan Amount: {amount} | Status: {status}",

                            "raw_data": row.to_dict()

                        })

                

                # Keyword matching across entire rows if few results

                if len(results) < 15:

                    cols_to_search = [c for c in ["Loan_Purpose", "Loan_Status", "Education", "Gender", "Property_Area", "Applicant_ID"] if c in df.columns]

                    mask = pd.Series([False] * len(df))

                    for c in cols_to_search:

                        mask = mask | df[c].astype(str).str.lower().str.contains(query, na=False)

                    

                    # Numeric search

                    if query.isdigit():

                        if "Cibil_Score" in df.columns:

                            mask = mask | (df["Cibil_Score"].astype(str).str.contains(query, na=False))

                        if "Loan_Amount" in df.columns:

                            mask = mask | (df["Loan_Amount"].astype(str).str.contains(query, na=False))

                        if "Annual_Income" in df.columns:

                            mask = mask | (df["Annual_Income"].astype(str).str.contains(query, na=False))

                            

                    matches = df[mask].head(15)

                    for _, row in matches.iterrows():

                        app_id = row.get("Applicant_ID", "Unknown")

                        if not any(r.get("id") == app_id for r in results):

                            amount = row.get("Loan_Amount", "N/A")

                            status = row.get("Loan_Status", "Unknown")

                            cibil = row.get("Cibil_Score", "N/A")

                            income = row.get("Annual_Income", "N/A")

                            desc = f"Amount: {amount} | CIBIL: {cibil} | Income: {income} | Status: {status}"

                            results.append({

                                "type": "data",

                                "id": app_id,

                                "title": f"📄 Record: {app_id}",

                                "desc": desc,

                                "raw_data": row.to_dict()

                            })

        except Exception:

            pass

            

    return results[:15]



def go_to_analysis(app_id):

    st.session_state["search_selected_id"] = app_id

    st.switch_page("pages/04_Data_Analysis.py")



def render_header():

    apply_theme()

    

    col1, col2 = st.columns([6.5, 1.5], vertical_alignment="center")

    

    

        

    with col1:

        search_query = st.text_input("Search", placeholder="🔍 Search applicants, loans, reports...", label_visibility="collapsed")

        

        # We put the search results panel directly below the search bar, inside col1

        if search_query:

            dataset_id = st.session_state.get('current_dataset_id')

            results = perform_global_search(search_query, dataset_id)

            

            with st.container(border=True):

                if not results:

                    st.info("No results found. Try Applicant ID, loan amount, CIBIL score, risk, approval, reports, or another keyword.")

                else:

                    for res in results:

                        if res["type"] == "page":

                            st.page_link(res["path"], label=f"**{res['title']}** - {res['desc']}")

                        else:

                            with st.expander(f"{res['title']} | {res['desc']}"):

                                raw = res.get("raw_data", {})

                                # Filter out some keys if needed, but showing all is fine since it's an expander

                                for k, v in list(raw.items())[:8]:

                                    st.write(f"- **{k}**: {v}")

                                st.button("View in Analysis", key=f"nav_{res['id']}_{res['type']}", on_click=go_to_analysis, args=(res['id'],))

    

    with col2:

        # User profile

        username = st.session_state.get("username", "User")
        with st.popover(f"👤 {username} ▾", use_container_width=True):

            st.page_link("pages/14_Profile.py", label="Profile", icon="👤")

            st.page_link("pages/13_Settings.py", label="Settings", icon="⚙️")

            if st.button("🚪 Logout", use_container_width=True):

                # Safe logout flow

                for key in list(st.session_state.keys()):

                    del st.session_state[key]

                st.session_state["logged_out"] = True

                st.switch_page("pages/00_Login.py")

