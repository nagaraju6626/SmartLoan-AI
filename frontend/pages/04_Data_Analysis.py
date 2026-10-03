import streamlit as st
import httpx
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

st.set_page_config(page_title="Data Analysis", page_icon="📊", layout="wide")

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header
from backend.ml.preprocessing import detect_columns

render_sidebar()
render_header()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "data", "uploads")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

@st.cache_data
def load_data(dataset_id):
    raw_df = None
    cleaned_df = None
    
    # Load Raw
    raw_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(dataset_id)]
    if raw_files:
        try:
            raw_df = pd.read_csv(os.path.join(UPLOAD_DIR, raw_files[0]))
        except Exception:
            pass
            
    # Load Cleaned
    cleaned_path = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
    if os.path.exists(cleaned_path):
        try:
            cleaned_df = pd.read_csv(cleaned_path)
        except Exception:
            pass
            
    return raw_df, cleaned_df

from frontend.components.theme import apply_chart_style

def main():
    st.title("DATA ANALYSIS")

    if 'current_dataset_id' not in st.session_state:
        st.warning("Please upload or select a dataset from the Data Upload page first.")
        return

    dataset_id = st.session_state['current_dataset_id']
    dataset_name = st.session_state.get('current_dataset_name', 'Unknown')
    
    st.markdown(f"**Analyzing dataset:** `{dataset_name}`")
    st.markdown("---")
    
    raw_df, cleaned_df = load_data(dataset_id)
    if raw_df is None:
        st.error("Failed to load original dataset.")
        return

    # --------------------------------------------
    # 📊 DATASET OVERVIEW
    # --------------------------------------------
    st.markdown("### 📊 DATASET OVERVIEW")
    raw_num_cols = len(raw_df.select_dtypes(include=[np.number]).columns)
    raw_cat_cols = len(raw_df.select_dtypes(exclude=[np.number]).columns)
    raw_missing_val = int(raw_df.isnull().sum().sum())
    raw_dup_rows = int(raw_df.duplicated().sum())
    
    o1, o2, o3 = st.columns(3)
    o1.metric("Rows", f"{len(raw_df):,}")
    o2.metric("Numeric Features", f"{raw_num_cols:,}")
    o3.metric("Missing Values", f"{raw_missing_val:,}")
    
    o4, o5, o6 = st.columns(3)
    o4.metric("Columns", f"{len(raw_df.columns):,}")
    o5.metric("Categorical Features", f"{raw_cat_cols:,}")
    o6.metric("Duplicate Rows", f"{raw_dup_rows:,}")
    
    st.markdown("---")

    # --------------------------------------------
    # 📄 RAW DATASET
    # --------------------------------------------
    st.markdown("### 📄 RAW DATASET")
    st.dataframe(raw_df.head(10), use_container_width=True)
    
    # --------------------------------------------
    # 🧹 DATA CLEANING
    # --------------------------------------------
    st.markdown("### 🧹 DATA CLEANING")
    
    raw_rows = len(raw_df)
    raw_cols = len(raw_df.columns)
    raw_missing = int(raw_df.isnull().sum().sum())
    raw_dups = int(raw_df.duplicated().sum())

    if cleaned_df is None:
        if raw_missing == 0 and raw_dups == 0:
            st.markdown("<h4 style='color: #10B981;'>🟢 No Missing or Duplicate Data Issues Detected</h4>", unsafe_allow_html=True)
            button_label = "🧹 View Cleaning Details"
        else:
            st.markdown("<h4 style='color: #EF4444;'>🟠 Data Quality Issues Detected</h4>", unsafe_allow_html=True)
            button_label = "🧹 Clean Data"
            
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Rows", f"{raw_rows:,}")
        c2.metric("Total Columns", f"{raw_cols:,}")
        c3.metric("Duplicate Rows", f"{raw_dups:,}")
        c4.metric("Total Missing Values", f"{raw_missing:,}")
        
        if st.button(button_label, use_container_width=True):
            with st.spinner("Cleaning dataset (handling missing values & duplicates)..."):
                try:
                    clean_res = httpx.post(f"{API_BASE_URL}/api/clean/{dataset_id}", timeout=60.0)
                    if clean_res.status_code == 200:
                        st.session_state['processed_dataset_id'] = dataset_id
                        st.session_state['processed_dataset_name'] = dataset_name
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Failed to clean dataset.")
                except Exception as e:
                    st.error(f"Error connecting to backend: {str(e)}")
                    
        # Active DataFrame for the rest of the page
        df = raw_df

    else:
        # Also ensure session state is set if we loaded an already cleaned dataset
        if 'processed_dataset_id' not in st.session_state:
            st.session_state['processed_dataset_id'] = dataset_id
            st.session_state['processed_dataset_name'] = dataset_name

        st.markdown("<h4 style='color: #10B981;'>🟢 Dataset Cleaned Successfully</h4>", unsafe_allow_html=True)
        
        clean_rows = len(cleaned_df)
        clean_cols = len(cleaned_df.columns)
        clean_missing = int(cleaned_df.isnull().sum().sum())
        clean_dups = int(cleaned_df.duplicated().sum())
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Original Rows", f"{raw_rows:,}")
        c2.metric("Cleaned Rows", f"{clean_rows:,}", delta=f"{clean_rows - raw_rows:,}")
        c3.metric("Duplicates Removed", f"{raw_dups - clean_dups:,}")
        c4.metric("Missing Values Handled", f"{raw_missing - clean_missing:,}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ✅ Cleaned Dataset Quality")
        q1, q2, q3 = st.columns(3)
        q1.metric("Cleaned Rows", f"{clean_rows:,}")
        q2.metric("Remaining Duplicate Rows", f"{clean_dups:,}")
        q3.metric("Remaining Missing Values", f"{clean_missing:,}")
        
        
        st.markdown("### ✨ CLEANED DATASET")
        st.dataframe(cleaned_df.head(10), use_container_width=True)
        
        # Active DataFrame for the rest of the page
        df = cleaned_df
        
    total_rows = len(df)
    total_cols = len(df.columns)
    cols = df.columns.tolist()
    total_missing = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    st.markdown("---")

    # --------------------------------------------
    # Detected Column Mapping
    # --------------------------------------------
    st.markdown("### 🔎 Detected Feature Mapping")
    mapping = detect_columns(df)
    
    # We display a clean table instead of raw JSON
    mapping_data = []
    # common standard features we want to show explicitly
    standard_features = ["income", "loan_amount", "loan_term", "credit_history", "target", "gender", "education", "property_area", "self_employed"]
    for std_feat in standard_features:
        if std_feat in mapping:
            mapping_data.append({"Standard Feature": std_feat.replace("_", " ").title(), "Detected Column": mapping[std_feat], "Status": "✅ Detected"})
        else:
            mapping_data.append({"Standard Feature": std_feat.replace("_", " ").title(), "Detected Column": "-", "Status": "❌ Missing"})
            
    st.dataframe(pd.DataFrame(mapping_data), use_container_width=True, hide_index=True)

    st.markdown("---")

    # --------------------------------------------
    # 🔍 DATA QUALITY REPORT
    # --------------------------------------------
    st.markdown("### 🔍 DATA QUALITY REPORT")
    
    dq_data = []
    for col in cols:
        missing = int(df[col].isnull().sum())
        dups = int(df[col].duplicated().sum())
        valid = total_rows - missing
        invalid = 0
        
        # Simple validation logic for known standard features if present
        if col in mapping.values():
            if col == mapping.get("credit_history") and pd.api.types.is_numeric_dtype(df[col]):
                invalid = int(((df[col] < 300) | (df[col] > 900)).sum())
            elif col in [mapping.get("income"), mapping.get("loan_amount"), mapping.get("loan_term")] and pd.api.types.is_numeric_dtype(df[col]):
                invalid = int((df[col] <= 0).sum())
            elif col == mapping.get("target"):
                invalid = int((~df[col].astype(str).str.upper().isin(["APPROVED", "REJECTED", "Y", "N", "1", "0", "YES", "NO"])).sum())
            elif col == "DTI_Ratio" and pd.api.types.is_numeric_dtype(df[col]):
                invalid = int(((df[col] < 0) | (df[col] > 1)).sum())
            
        valid = valid - invalid
        
        dq_data.append({
            "Column": col,
            "Valid Values": f"{valid:,}",
            "Invalid Values": f"{invalid:,}",
            "Missing": f"{missing:,}",
            "Repeated Values": f"{dups:,}",
            "Data Type": str(df[col].dtype)
        })
            
    st.markdown("<small><i>Repeated Values indicates repeated values within an individual column and does not mean duplicate rows.</i></small>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(dq_data), use_container_width=True, hide_index=True)

    st.markdown("---")

    # --------------------------------------------
    # 🎯 TARGET ANALYSIS
    # --------------------------------------------
    st.markdown("### 🎯 TARGET ANALYSIS")
    
    target_col = mapping.get("target", "Loan_Status")
    if target_col in cols:
        target_series = df[target_col].astype(str).str.upper()
        approved = len(target_series[target_series.isin(["APPROVED", "Y", "1", "YES"])])
        rejected = len(target_series[target_series.isin(["REJECTED", "N", "0", "NO"])])
        total_valid = approved + rejected
        
        app_pct = (approved / total_valid * 100) if total_valid > 0 else 0
        rej_pct = (rejected / total_valid * 100) if total_valid > 0 else 0
        
        # Class Balance Indicator
        balance_ratio = min(app_pct, rej_pct)
        if balance_ratio >= 40:
            balance_status = "🟢 Reasonably Balanced"
        elif balance_ratio >= 20:
            balance_status = "🟡 Moderately Imbalanced"
        else:
            balance_status = "🔴 Highly Imbalanced"
            
        st.markdown(f"**Target Column:** `{target_col}`")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Applications", f"{total_valid:,}")
        c2.metric("Approved", f"{approved:,}")
        c3.metric("Rejected", f"{rejected:,}")
        c4.markdown(f"**Target Balance:** {balance_status}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        c5, c6, c7 = st.columns([1,1,2])
        c5.metric("Approval Rate", f"{app_pct:.2f}%")
        c6.metric("Rejection Rate", f"{rej_pct:.2f}%")
        
        with c7:
            fig = px.pie(values=[approved, rejected], names=["Approved", "Rejected"], title="Approved vs Rejected", hole=0.5, color_discrete_sequence=["#10B981", "#EF4444"])
            fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), height=250)
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
    else:
        st.info(f"Target column not available in this dataset. Required for target analysis.")

    st.markdown("---")

    # --------------------------------------------
    # ⚠️ OUTLIER DETECTION
    # --------------------------------------------
    st.markdown("### ⚠️ OUTLIER DETECTION")
    st.markdown("<small><i>Outliers were checked using the IQR method. Any detected outliers can be reviewed and handled during preprocessing.</i></small>", unsafe_allow_html=True)
    
    outlier_data = []
    
    for col in cols:
        if pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            outliers = int(((df[col] < lower) | (df[col] > upper)).sum())
            if outliers > 0:
                outlier_pct = (outliers / total_rows * 100) if total_rows > 0 else 0
                
                outlier_data.append({
                    "Column": col,
                    "Outlier Count": f"{outliers:,}",
                    "Outlier %": f"{outlier_pct:.2f}%"
                })
            
    if outlier_data:
        st.dataframe(pd.DataFrame(outlier_data), use_container_width=True, hide_index=True)
    else:
        st.info("No potential outliers detected using the IQR method.")

    st.markdown("---")

    # --------------------------------------------
    # ⚙️ PREPROCESSING SUMMARY
    # --------------------------------------------
    st.markdown("### ⚙️ PREPROCESSING SUMMARY")
    st.markdown("Recommended preprocessing pipeline for model training.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("✅ **COMPLETED**")
        st.markdown("✓ Raw dataset loaded")
        st.markdown("✓ Data cleaning")
        st.markdown("✓ Duplicate handling")
        st.markdown("✓ Missing-value handling")
        st.markdown("✓ Feature detection")
        st.markdown("✓ Data quality analysis")
        st.markdown("✓ Target analysis")
        st.markdown("✓ Outlier detection")
    with c2:
        st.markdown("⏳ **PLANNED / MODEL PREPROCESSING**")
        st.markdown("⏳ Categorical encoding")
        st.markdown("⏳ Numerical scaling")
        st.markdown("⏳ Feature selection")
        st.markdown(f"⏳ Target encoding (e.g., Approved → 1, Rejected → 0)")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    pipeline_html = """
    <div style='display:flex; justify-content:space-between; align-items:center; background:#F8FAFC; padding:16px; border-radius:12px; border:1px solid #E2E8F0; font-size:0.9rem; font-weight:600; color:#334155; text-align:center;'>
        <div>Raw Dataset</div> <div>➔</div>
        <div>Data Cleaning</div> <div>➔</div>
        <div>Feature Detection</div> <div>➔</div>
        <div>Categorical Encoding</div> <div>➔</div>
        <div>Numerical Scaling</div> <div>➔</div>
        <div>Feature Selection</div> <div>➔</div>
        <div>Target Encoding</div> <div>➔</div>
        <div style='color:#2563EB;'>Model Training</div>
    </div>
    """
    st.markdown(pipeline_html, unsafe_allow_html=True)

    st.markdown("---")

    # --------------------------------------------
    # 💡 AUTOMATIC DATA INSIGHTS
    # --------------------------------------------
    st.markdown("### 💡 AUTOMATIC DATA INSIGHTS")
    insights = []
    def format_money(val):
        if val >= 100000:
            return f"₹{val/100000:.1f} lakh"
        return f"₹{val:,.0f}"

    cibil_col = mapping.get("credit_history")
    if cibil_col and cibil_col in cols and pd.api.types.is_numeric_dtype(df[cibil_col]):
        cibil_name = cibil_col.replace('_', ' ').replace('Cibil', 'CIBIL').replace('cibil', 'CIBIL')
        insights.append(f"Average {cibil_name}: {df[cibil_col].mean():.0f}")
        
    if target_col in cols:
        try:
            if app_pct > 50:
                insights.append(f"Most applications were approved")
            else:
                insights.append(f"Most applications were rejected")
        except:
            pass
            
    gender_col = mapping.get("gender")
    if gender_col and gender_col in cols:
        vc = df[gender_col].astype(str).str.upper().value_counts()
        if "MALE" in vc and "FEMALE" in vc:
            if vc["MALE"] > vc["FEMALE"]:
                insights.append("Male applicants are more than female applicants")
            elif vc["FEMALE"] > vc["MALE"]:
                insights.append("Female applicants are more than male applicants")

    edu_col = mapping.get("education")
    if edu_col and edu_col in cols:
        grads = len(df[df[edu_col].astype(str).str.upper() == "GRADUATE"])
        if (grads/total_rows) > 0.5:
            insights.append("Most applicants are graduates")
        else:
            insights.append("Many applicants are not graduates")

    income_col = mapping.get("income")
    if income_col and income_col in cols and pd.api.types.is_numeric_dtype(df[income_col]):
        val = df[income_col].mean()
        insights.append(f"Average annual income: {format_money(val)}")
        
    dti_col = [c for c in cols if "dti" in c.lower()]
    if dti_col and pd.api.types.is_numeric_dtype(df[dti_col[0]]):
        insights.append(f"Median DTI Ratio: {df[dti_col[0]].median():.2f}")
        
    loan_col = mapping.get("loan_amount")
    if loan_col and loan_col in cols and pd.api.types.is_numeric_dtype(df[loan_col]):
        val = df[loan_col].mean()
        insights.append(f"Average loan amount: {format_money(val)}")
        
    for insight in insights:
        st.markdown(f"• {insight}")
        
    if not insights:
        st.markdown("• Not enough columns to generate automatic insights.")

    st.markdown("---")

    # --------------------------------------------
    # 📌 KEY FINDINGS
    # --------------------------------------------
    st.markdown("### 📌 KEY FINDINGS")
    
    findings = []
    if cibil_col and cibil_col in cols and pd.api.types.is_numeric_dtype(df[cibil_col]):
        cibil_name = cibil_col.replace('_', ' ').replace('Cibil', 'CIBIL').replace('cibil', 'CIBIL')
        findings.append(f"- **Average {cibil_name}**: {df[cibil_col].mean():.0f}")
    if loan_col and loan_col in cols and pd.api.types.is_numeric_dtype(df[loan_col]):
        findings.append(f"- **Median {loan_col.replace('_', ' ')}**: ₹{df[loan_col].median():,.0f}")
    if target_col in cols:
        try:
            findings.append(f"- **Approval Rate**: {app_pct:.2f}%")
            findings.append(f"- **Rejection Rate**: {rej_pct:.2f}%")
        except:
            pass
    if edu_col and edu_col in cols:
        grads = len(df[df[edu_col].astype(str).str.upper() == "GRADUATE"])
        findings.append(f"- **Graduate Applicants**: {(grads/total_rows*100) if total_rows else 0:.1f}%")
        
    # Count outliers across all numeric columns
    outlier_count_total = 0
    for col in cols:
        if pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outlier_count_total += int(((df[col] < lower) | (df[col] > upper)).sum())
            
    findings.append(f"- **Potential Outlier Observations**: {outlier_count_total:,}")
    findings.append(f"- **Remaining Missing Values**: {total_missing:,}")
    
    for f in findings:
        st.markdown(f)
        
    st.markdown("<small><i>Outlier counts are calculated per numerical feature, so one observation may be counted in multiple features.</i></small>", unsafe_allow_html=True)

    st.markdown("---")

    # --------------------------------------------
    # ✅ ANALYSIS READINESS & CONTINUE
    # --------------------------------------------
    st.markdown("### ✅ ANALYSIS READINESS")
    
    ready = True
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("✓ Dataset loaded")
        if target_col in cols:
            st.markdown("✓ Target identified")
        else:
            st.markdown("❌ Target missing")
            ready = False
            
        if total_missing == 0:
            st.markdown("✓ Missing values checked")
        else:
            st.markdown("❌ Missing values present")
            ready = False
            
    with c2:
        if duplicate_rows == 0:
            st.markdown("✓ Duplicate rows checked")
        else:
            st.markdown("❌ Duplicate rows present")
            ready = False
            
        st.markdown("✓ Numerical features detected")
        st.markdown("✓ Categorical features detected")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if ready:
        st.markdown("<h4 style='color: #10B981;'>🟢 Analysis Completed — Ready for Model Preprocessing</h4>", unsafe_allow_html=True)
    else:
        st.markdown("<h4 style='color: #F59E0B;'>🟡 Please clean data before preprocessing</h4>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Continue to Model Preprocessing →", type="primary", use_container_width=True):
        st.switch_page("pages/05_Model_Training.py")

if __name__ == "__main__":
    main()
