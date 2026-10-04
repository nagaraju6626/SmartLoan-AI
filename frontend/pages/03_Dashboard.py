import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header


# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()

PROCESSED_DIR = "data/processed"
UPLOAD_DIR = "data/uploads"

def load_dashboard_data(dataset_id):
    if 'cleaned_df' in st.session_state and st.session_state['cleaned_df'] is not None:
        return st.session_state['cleaned_df']
    elif 'raw_df' in st.session_state and st.session_state['raw_df'] is not None:
        return st.session_state['raw_df']
    return None

def main():
    st.title("SMART LOAN DASHBOARD")

    if 'current_dataset_id' not in st.session_state:
        st.warning("Please upload or select a dataset from the Data Upload page first.")
        return

    dataset_id = st.session_state['current_dataset_id']
    dataset_name = st.session_state.get('current_dataset_name', 'Unknown')
    
    df = load_dashboard_data(dataset_id)
    
    if df is None or df.empty:
        st.error("Failed to load dataset data.")
        return

    st.markdown(f"**Dataset:** `{dataset_name}`  |  <span style='color:green;font-weight:bold;'>✓ Data Loaded</span>  |  **Rows:** {len(df):,}  |  **Features:** {len(df.columns):,}", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Initialize session state for filters
    for key in ["f_status", "f_education", "f_gender", "f_purpose", "f_property", "f_employed", "f_cibil"]:
        if key not in st.session_state:
            st.session_state[key] = "All"

    # Reset filters logic
    def reset_filters():
        for key in ["f_status", "f_education", "f_gender", "f_purpose", "f_property", "f_employed", "f_cibil"]:
            st.session_state[key] = "All"

    # Define columns to check existence
    cols = df.columns.tolist()
    
    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------
    st.markdown("### FILTERS")
    
    # Cibil Score binning for filter and charts
    if "Cibil_Score" in cols:
        df["CIBIL_Range"] = pd.cut(df["Cibil_Score"], bins=[0, 549, 649, 749, 900], labels=["300-549", "550-649", "650-749", "750-900"])
        cols.append("CIBIL_Range")

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        if "Loan_Status" in cols:
            opts = ["All"] + sorted(df["Loan_Status"].dropna().unique().tolist())
            if st.session_state["f_status"] not in opts: st.session_state["f_status"] = "All"
            st.selectbox("Loan Status", opts, key="f_status")
        if "Education" in cols:
            opts = ["All"] + sorted(df["Education"].dropna().unique().tolist())
            if st.session_state["f_education"] not in opts: st.session_state["f_education"] = "All"
            st.selectbox("Education", opts, key="f_education")
            
    with f2:
        if "Gender" in cols:
            opts = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
            if st.session_state["f_gender"] not in opts: st.session_state["f_gender"] = "All"
            st.selectbox("Gender", opts, key="f_gender")
        if "Loan_Purpose" in cols:
            opts = ["All"] + sorted(df["Loan_Purpose"].dropna().unique().tolist())
            if st.session_state["f_purpose"] not in opts: st.session_state["f_purpose"] = "All"
            st.selectbox("Loan Purpose", opts, key="f_purpose")

    with f3:
        if "Property_Area" in cols:
            opts = ["All"] + sorted(df["Property_Area"].dropna().unique().tolist())
            if st.session_state["f_property"] not in opts: st.session_state["f_property"] = "All"
            st.selectbox("Property Area", opts, key="f_property")
        if "Self_Employed" in cols:
            opts = ["All"] + sorted(df["Self_Employed"].dropna().unique().tolist())
            if st.session_state["f_employed"] not in opts: st.session_state["f_employed"] = "All"
            st.selectbox("Self Employed", opts, key="f_employed")

    with f4:
        if "CIBIL_Range" in cols:
            opts = ["All", "300-549", "550-649", "650-749", "750-900"]
            if st.session_state["f_cibil"] not in opts: st.session_state["f_cibil"] = "All"
            st.selectbox("CIBIL Score Range", opts, key="f_cibil")
        
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.button("Reset Filters", on_click=reset_filters, use_container_width=True)

    # Apply Filters
    filtered_df = df.copy()
    if "Loan_Status" in cols and st.session_state.get("f_status", "All") != "All":
        filtered_df = filtered_df[filtered_df["Loan_Status"] == st.session_state["f_status"]]
    if "Education" in cols and st.session_state.get("f_education", "All") != "All":
        filtered_df = filtered_df[filtered_df["Education"] == st.session_state["f_education"]]
    if "Gender" in cols and st.session_state.get("f_gender", "All") != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == st.session_state["f_gender"]]
    if "Loan_Purpose" in cols and st.session_state.get("f_purpose", "All") != "All":
        filtered_df = filtered_df[filtered_df["Loan_Purpose"] == st.session_state["f_purpose"]]
    if "Property_Area" in cols and st.session_state.get("f_property", "All") != "All":
        filtered_df = filtered_df[filtered_df["Property_Area"] == st.session_state["f_property"]]
    if "Self_Employed" in cols and st.session_state.get("f_employed", "All") != "All":
        filtered_df = filtered_df[filtered_df["Self_Employed"] == st.session_state["f_employed"]]
    if "CIBIL_Range" in cols and st.session_state.get("f_cibil", "All") != "All":
        filtered_df = filtered_df[filtered_df["CIBIL_Range"] == st.session_state["f_cibil"]]

    st.markdown("---")

    # --------------------------------------------------
    # KPIs
    # --------------------------------------------------
    total_apps = len(filtered_df)
    
    approved = 0
    rejected = 0
    if "Loan_Status" in cols:
        approved = len(filtered_df[filtered_df["Loan_Status"].astype(str).str.upper().isin(["APPROVED", "Y", "1", "YES"])])
        rejected = len(filtered_df[filtered_df["Loan_Status"].astype(str).str.upper().isin(["REJECTED", "N", "0", "NO"])])
    
    approval_rate = (approved / total_apps * 100) if total_apps > 0 else 0
    
    avg_loan = filtered_df["Loan_Amount"].mean() if "Loan_Amount" in cols else 0
    avg_income = filtered_df["Annual_Income"].mean() if "Annual_Income" in cols else 0
    avg_cibil = filtered_df["Cibil_Score"].mean() if "Cibil_Score" in cols else 0
    avg_term = filtered_df["Loan_Term_Years"].mean() if "Loan_Term_Years" in cols else 0
    avg_dti = filtered_df["DTI_Ratio"].mean() if "DTI_Ratio" in cols else 0

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Applicants", f"{total_apps:,}")
    k2.metric("Approved", f"{approved:,}")
    k3.metric("Rejected", f"{rejected:,}")
    k4.metric("Approval Rate", f"{approval_rate:.1f}%")
    k5.metric("Avg Loan Amount", f"₹{avg_loan:,.0f}" if pd.notnull(avg_loan) else "N/A")
    k6.metric("Avg Income", f"₹{avg_income:,.0f}" if pd.notnull(avg_income) else "N/A")

    st.markdown("<br>", unsafe_allow_html=True)
    k7, k8, k9, _, _, _ = st.columns(6)
    k7.metric("Avg CIBIL Score", f"{avg_cibil:.0f}" if pd.notnull(avg_cibil) else "N/A")
    k8.metric("Avg Loan Term", f"{avg_term:.1f} Yrs" if pd.notnull(avg_term) else "N/A")
    k9.metric("Avg DTI Ratio", f"{avg_dti:.2f}" if pd.notnull(avg_dti) else "N/A")

    st.markdown("---")

    # --------------------------------------------------
    # LOAN RISK OVERVIEW
    # --------------------------------------------------
    st.markdown("### Loan Risk Overview (Analytics)")
    st.markdown("<small><i>These analytical groups are generated dynamically based on CIBIL and DTI rules, not official banking decisions.</i></small>", unsafe_allow_html=True)
    
    if "Cibil_Score" in cols and "DTI_Ratio" in cols:
        def get_risk(row):
            if row["Cibil_Score"] >= 750 and row["DTI_Ratio"] <= 0.4: return "Low Risk"
            elif row["Cibil_Score"] < 600 or row["DTI_Ratio"] > 0.6: return "High Risk"
            else: return "Medium Risk"
            
        filtered_df["Risk_Category"] = filtered_df.apply(get_risk, axis=1)
        risk_counts = filtered_df["Risk_Category"].value_counts()
        
        r1, r2, r3 = st.columns(3)
        low = risk_counts.get("Low Risk", 0)
        med = risk_counts.get("Medium Risk", 0)
        high = risk_counts.get("High Risk", 0)
        
        r1.metric("Low Risk", f"{low:,} ({(low/total_apps*100) if total_apps else 0:.1f}%)")
        r2.metric("Medium Risk", f"{med:,} ({(med/total_apps*100) if total_apps else 0:.1f}%)")
        r3.metric("High Risk", f"{high:,} ({(high/total_apps*100) if total_apps else 0:.1f}%)")
    else:
        st.info("Required columns (Cibil_Score, DTI_Ratio) not available for Risk Overview.")

    st.markdown("---")

    from frontend.components.theme import apply_chart_style

    # Row 1: CIBIL Score Distribution | Approval Rate by CIBIL Range
    c1, c2 = st.columns(2)
    with c1:
        if "CIBIL_Range" in cols:
            cibil_counts = filtered_df["CIBIL_Range"].value_counts().sort_index().reset_index()
            cibil_counts.columns = ["CIBIL Range", "Applicants"]
            fig = px.bar(cibil_counts, x="CIBIL Range", y="Applicants", title="CIBIL Score Distribution", color_discrete_sequence=["#3B82F6"])
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required column 'Cibil_Score' not available.")
            
    with c2:
        if "CIBIL_Range" in cols and "Loan_Status" in cols:
            app_rate = filtered_df.copy()
            app_rate["Approved"] = app_rate["Loan_Status"].astype(str).str.upper().isin(["APPROVED", "Y", "1", "YES"]).astype(int)
            grouped = app_rate.groupby("CIBIL_Range")["Approved"].agg(["sum", "count"]).reset_index()
            grouped["Approval Rate (%)"] = (grouped["sum"] / grouped["count"] * 100).fillna(0)
            fig = px.bar(grouped, x="CIBIL_Range", y="Approval Rate (%)", title="Approval Rate by CIBIL Range", color_discrete_sequence=["#10B981"])
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required columns for Approval Rate not available.")

    # Row 2: Loan Status Distribution | Loan Amount Distribution
    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if "Loan_Status" in cols:
            status_counts = filtered_df["Loan_Status"].value_counts().reset_index()
            status_counts.columns = ["Loan Status", "Count"]
            fig = px.pie(status_counts, names="Loan Status", values="Count", title="Loan Status Distribution", hole=0.4, color_discrete_sequence=["#10B981", "#EF4444", "#F59E0B"])
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required column 'Loan_Status' not available.")
            
    with c4:
        if "Loan_Amount" in cols:
            # Custom readable bins instead of pandas intervals
            bins = [0, 500000, 1000000, 1500000, 2000000, float('inf')]
            labels = ["₹0–5L", "₹5L–10L", "₹10L–15L", "₹15L–20L", "₹20L+"]
            filtered_df["Amount_Bin"] = pd.cut(filtered_df["Loan_Amount"], bins=bins, labels=labels)
            amt_counts = filtered_df["Amount_Bin"].value_counts().sort_index().reset_index()
            amt_counts.columns = ["Loan Amount Range", "Applicants"]
            fig = px.bar(amt_counts, x="Loan Amount Range", y="Applicants", title="Loan Amount Distribution", color_discrete_sequence=["#3B82F6"])
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required column 'Loan_Amount' not available.")

    # Row 3: Income vs Loan Amount | CIBIL vs Loan Amount
    st.markdown("<br>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if "Annual_Income" in cols and "Loan_Amount" in cols:
            color_col = "Loan_Status" if "Loan_Status" in cols else None
            scatter_df = filtered_df.dropna(subset=["Annual_Income", "Loan_Amount"]).sample(min(1000, len(filtered_df)))
            fig = px.scatter(scatter_df, x="Annual_Income", y="Loan_Amount", color=color_col, title="Applicant Income vs Loan Amount", labels={"Annual_Income": "Annual Income (₹)", "Loan_Amount": "Loan Amount (₹)"}, color_discrete_map={"Approved": "#10B981", "Rejected": "#EF4444", "Y": "#10B981", "N": "#EF4444"})
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required columns for Income vs Loan Amount not available.")
            
    with c6:
        if "Cibil_Score" in cols and "Loan_Amount" in cols:
            color_col = "Risk_Category" if "Risk_Category" in filtered_df.columns else ("Loan_Status" if "Loan_Status" in cols else None)
            scatter_df = filtered_df.dropna(subset=["Cibil_Score", "Loan_Amount"]).sample(min(1000, len(filtered_df)))
            fig = px.scatter(scatter_df, x="Cibil_Score", y="Loan_Amount", color=color_col, title="CIBIL Score vs Loan Amount", labels={"Cibil_Score": "CIBIL Score", "Loan_Amount": "Loan Amount (₹)"}, color_discrete_map={"Low Risk": "#10B981", "Medium Risk": "#F59E0B", "High Risk": "#EF4444"})
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required columns for CIBIL vs Loan Amount not available.")

    # Row 4: Approval by Education | Approval by Loan Purpose
    st.markdown("<br>", unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        if "Education" in cols and "Loan_Status" in cols:
            edu_status = filtered_df.groupby(["Education", "Loan_Status"]).size().reset_index(name="Count")
            fig = px.bar(edu_status, x="Education", y="Count", color="Loan_Status", barmode="group", title="Approval by Education", color_discrete_map={"Approved": "#10B981", "Rejected": "#EF4444", "Y": "#10B981", "N": "#EF4444"})
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required columns for Approval by Education not available.")
            
    with c8:
        if "Loan_Purpose" in cols and "Loan_Status" in cols:
            purp_status = filtered_df.groupby(["Loan_Purpose", "Loan_Status"]).size().reset_index(name="Count")
            fig = px.bar(purp_status, x="Loan_Purpose", y="Count", color="Loan_Status", barmode="stack", title="Approval by Loan Purpose", color_discrete_map={"Approved": "#10B981", "Rejected": "#EF4444", "Y": "#10B981", "N": "#EF4444"})
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required columns for Approval by Loan Purpose not available.")

    # Row 5: Approval by Employment | Approval by Property Area
    st.markdown("<br>", unsafe_allow_html=True)
    c9, c10 = st.columns(2)
    with c9:
        if "Self_Employed" in cols and "Loan_Status" in cols:
            emp_status = filtered_df.groupby(["Self_Employed", "Loan_Status"]).size().reset_index(name="Count")
            fig = px.bar(emp_status, x="Self_Employed", y="Count", color="Loan_Status", barmode="group", title="Approval by Employment Status", color_discrete_map={"Approved": "#10B981", "Rejected": "#EF4444", "Y": "#10B981", "N": "#EF4444"})
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required columns for Approval by Employment not available.")
            
    with c10:
        if "Property_Area" in cols and "Loan_Status" in cols:
            prop_status = filtered_df.groupby(["Property_Area", "Loan_Status"]).size().reset_index(name="Count")
            fig = px.bar(prop_status, x="Property_Area", y="Count", color="Loan_Status", barmode="group", title="Approval by Property Area", color_discrete_map={"Approved": "#10B981", "Rejected": "#EF4444", "Y": "#10B981", "N": "#EF4444"})
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Required columns for Approval by Property Area not available.")

    st.markdown("---")

    # --------------------------------------------------
    # KEY INSIGHTS
    # --------------------------------------------------
    st.markdown("### Key Insights")
    insights = []
    
    if total_apps > 0:
        insights.append(f"The overall approval rate for the current filtered selection is **{approval_rate:.1f}%** across {total_apps:,} applicants.")
        
    if "Cibil_Score" in cols and pd.notnull(avg_cibil):
        insights.append(f"The average CIBIL score is **{avg_cibil:.0f}**. Higher CIBIL ranges correlate strongly with improved approval rates in this dataset.")
        
    if "Loan_Purpose" in cols and "Loan_Status" in cols and total_apps > 0:
        # Find purpose with highest approval rate
        app_rate_df = filtered_df.copy()
        app_rate_df["Approved"] = app_rate_df["Loan_Status"].astype(str).str.upper().isin(["APPROVED", "Y", "1", "YES"]).astype(int)
        purp_grouped = app_rate_df.groupby("Loan_Purpose")["Approved"].agg(["sum", "count"])
        purp_grouped["rate"] = purp_grouped["sum"] / purp_grouped["count"]
        if not purp_grouped.empty:
            best_purpose = purp_grouped["rate"].idxmax()
            best_rate = purp_grouped["rate"].max() * 100
            insights.append(f"The loan purpose with the highest approval rate is **{best_purpose}** ({best_rate:.1f}% approval).")
            
    if "Loan_Amount" in cols and pd.notnull(avg_loan):
        insights.append(f"The average requested loan amount is **₹{avg_loan:,.0f}**.")
        
    for insight in insights:
        st.markdown(f"• {insight}")

    if not insights:
        st.markdown("• No insights could be generated from the available data.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------
    # Create a summary CSV
    summary_data = {
        "Metric": ["Total Applicants", "Approved", "Rejected", "Approval Rate", "Avg Loan Amount", "Avg Income", "Avg CIBIL", "Avg DTI", "Filters Applied"],
        "Value": [
            total_apps, 
            approved, 
            rejected, 
            f"{approval_rate:.1f}%", 
            f"{avg_loan:.2f}", 
            f"{avg_income:.2f}", 
            f"{avg_cibil:.2f}", 
            f"{avg_dti:.2f}",
            str({k:v for k,v in st.session_state.items() if k.startswith("f_")})
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    csv = summary_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Dashboard Report",
        data=csv,
        file_name="smart_loan_dashboard_report.csv",
        mime="text/csv",
        use_container_width=True
    )

if __name__ == "__main__":
    main()
