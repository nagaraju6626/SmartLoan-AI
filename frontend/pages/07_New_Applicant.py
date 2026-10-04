import streamlit as st
import httpx
import os
import pandas as pd
import json
import uuid
import sys
import numpy as np
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="New Applicant", page_icon="👤", layout="wide")

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header


# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def apply_custom_css():
    st.markdown("""
    <style>
    .result-card {
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .low-risk { background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border: 2px solid #10B981; }
    .medium-risk { background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border: 2px solid #F59E0B; }
    .high-risk { background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); border: 2px solid #EF4444; }
    
    .risk-title { font-size: 1.2rem; font-weight: 600; color: #475569; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.5rem; }
    .risk-level { font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; }
    .low-text { color: #059669; }
    .medium-text { color: #D97706; }
    .high-text { color: #DC2626; }
    
    .risk-conf { font-size: 1.5rem; font-weight: 700; color: #1E293B; margin-bottom: 1rem; }
    .risk-msg { font-size: 1.1rem; color: #475569; font-weight: 500; }
    
    .info-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def load_sample(dataset_path, features):
    if dataset_path and os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)
        sample = df.sample(1).iloc[0]
        for f in features:
            if f in sample and not pd.isna(sample[f]):
                st.session_state[f] = sample[f]
        st.session_state.pop('prediction_result', None)
        st.session_state.pop('submitted_prediction_inputs', None)
        st.session_state.pop('prediction_submitted', None)
        return True
    return False

def reset_form(features):
    for f in features:
        if f in st.session_state:
            del st.session_state[f]
    st.session_state.pop('prediction_result', None)
    st.session_state.pop('submitted_prediction_inputs', None)
    st.session_state.pop('prediction_submitted', None)

def get_feature_metadata(dataset_path, features):
    meta = {}
    if not dataset_path or not os.path.exists(dataset_path):
        return meta
        
    df = pd.read_csv(dataset_path)
    for f in features:
        if f in df.columns:
            if pd.api.types.is_numeric_dtype(df[f]):
                # Sensible numerical bounds
                meta[f] = {
                    "type": "numeric",
                    "min": float(df[f].min()),
                    "max": float(df[f].max()),
                    "default": float(df[f].median())
                }
            else:
                # Categorical options
                opts = df[f].dropna().unique().tolist()
                meta[f] = {
                    "type": "categorical",
                    "options": opts,
                    "default": opts[0] if opts else ""
                }
    return meta

def render_field(f, feature_meta):
    label = f.replace("_", " ")
    if f not in feature_meta:
        # Fallback if no dataset available
        if f not in st.session_state:
            st.session_state[f] = ""
        st.text_input(label, key=f)
        return
        
    f_meta = feature_meta[f]
    
    if f_meta["type"] == "numeric":
        min_v = f_meta["min"]
        max_v = f_meta["max"]
        range_v = max_v - min_v
        step = 1.0
        if range_v > 1000: step = 100.0
        elif range_v > 100: step = 10.0
        elif range_v <= 1: step = 0.01
        
        if f not in st.session_state:
            st.session_state[f] = float(f_meta["default"])
        st.number_input(label, min_value=min_v, step=step, key=f)
        
    elif f_meta["type"] == "categorical":
        opts = f_meta["options"]
        if f not in st.session_state:
            val = f_meta["default"]
            st.session_state[f] = val if val in opts else opts[0]
        st.selectbox(label, options=opts, key=f)

def main():
    apply_custom_css()
    st.title("New Applicant")
    st.markdown("Enter a new applicant's information to assess loan risk using the active ML model.")
    st.markdown("---")

    if 'active_model_version' not in st.session_state:
        st.warning("Please train and select an active model from the Model Training page first.")
        return

    active_version = st.session_state['active_model_version']
    
    # Try to load model metadata
    metadata_path = os.path.join("models", "metadata", f"{active_version}.json")
    model_alg = "Unknown"
    dataset_path = None
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            meta = json.load(f)
            model_alg = meta.get("algorithm", "").replace("_", " ").title()
            dataset_path = meta.get("dataset_path")

    # Fetch features from backend API (to ensure exactly what the endpoint expects)
    try:
        res = httpx.get(f"{API_BASE_URL}/api/predict/features/{active_version}")
        if res.status_code != 200:
            st.error("Failed to load model features from backend.")
            return
        features = res.json()["features"]
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return

    # Extract dynamic metadata from training dataset
    feature_meta = get_feature_metadata(dataset_path, features)

    # ---------------------------------------------------------
    # INFO & THRESHOLDS
    # ---------------------------------------------------------
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown(f"""
        <div class="info-card">
            <h4 style="margin-top:0; color:#0F172A;">🧠 Active Model</h4>
            <b>Model:</b> {model_alg}<br>
            <b>Version:</b> <code>{active_version}</code><br>
            <b>Type:</b> Loan Risk Classification
        </div>
        """, unsafe_allow_html=True)
        
    with col_info2:
        st.markdown("""
        <div class="info-card">
            <h4 style="margin-top:0; color:#0F172A;">⚙️ Risk Thresholds</h4>
            <small style="color:#64748B;">These thresholds are application-defined settings used to interpret model probabilities. They are not official banking standards.</small>
        </div>
        """, unsafe_allow_html=True)
        if "low_risk_thresh" not in st.session_state:
            st.session_state["low_risk_thresh"] = 0.75
        if "medium_risk_thresh" not in st.session_state:
            st.session_state["medium_risk_thresh"] = 0.50
            
        t1, t2 = st.columns(2)
        with t1: low_risk_thresh = st.slider("Low Risk Min Probability", 0.5, 1.0, key="low_risk_thresh", step=0.01)
        with t2: medium_risk_thresh = st.slider("Medium Risk Min Probability", 0.1, 0.9, key="medium_risk_thresh", step=0.01)

    st.markdown("---")

    # ---------------------------------------------------------
    # TOP CONTROLS (Load / Reset)
    # ---------------------------------------------------------
    ctrl1, ctrl2, _ = st.columns([1, 1, 2])
    with ctrl1:
        if st.button("✨ Load Sample Applicant", use_container_width=True):
            if load_sample(dataset_path, features):
                st.success("Loaded random applicant!")
            else:
                st.error("Failed to load sample dataset.")
    with ctrl2:
        if st.button("↻ Reset Form", use_container_width=True):
            reset_form(features)
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # DYNAMIC FORM
    # ---------------------------------------------------------
    # Group features logically by sections if their names match known keywords
    section_map = {
        "Applicant Profile": ["age", "gender", "married", "dependent", "education"],
        "Employment & Income": ["employ", "income", "salary", "self"],
        "Loan Information": ["loan_amount", "term", "purpose", "duration"],
        "Credit & Financial Profile": ["cibil", "credit", "dti", "existing"],
        "Assets & Property": ["asset", "property", "area"]
    }
    
    grouped_features = {k: [] for k in section_map.keys()}
    grouped_features["Additional Fields"] = []
    
    for f in features:
        if f == 'Applicant_ID': continue
        
        f_lower = f.lower()
        placed = False
        for sec, keywords in section_map.items():
            if any(kw in f_lower for kw in keywords):
                grouped_features[sec].append(f)
                placed = True
                break
                
        if not placed:
            grouped_features["Additional Fields"].append(f)

    with st.form("predict_form"):
        
        icons = ["👤", "💼", "🏦", "📊", "🏡", "📝"]
        icon_idx = 0
        
        for sec, feats in grouped_features.items():
            if not feats: continue
            
            st.markdown(f"#### {icons[icon_idx%len(icons)]} SECTION: {sec}")
            icon_idx += 1
            
            cols = st.columns(3)
            for idx, f in enumerate(feats):
                with cols[idx % 3]:
                    render_field(f, feature_meta)
                    
            st.markdown("<br>", unsafe_allow_html=True)

        submit = st.form_submit_button("🔍 Predict Loan Risk", type="primary", use_container_width=True)

    if submit:
        # Build Payload
        input_data = {}
        for f in features:
            if f == 'Applicant_ID':
                input_data[f] = f"APP-{str(uuid.uuid4())[:8]}"
            else:
                input_data[f] = st.session_state.get(f)

        # Send Prediction
        with st.spinner("Analyzing applicant risk securely..."):
            payload = {
                "version": active_version,
                "features": input_data
            }
            try:
                pred_res = httpx.post(f"{API_BASE_URL}/api/predict/", json=payload, timeout=10.0)
                if pred_res.status_code == 200:
                    res = pred_res.json()
                    prob = res['probability']
                    if prob >= low_risk_thresh:
                        risk_level, decision = "LOW RISK", "APPROVE"
                    elif prob >= medium_risk_thresh:
                        risk_level, decision = "MEDIUM RISK", "REVIEW"
                    else:
                        risk_level, decision = "HIGH RISK", "REJECT"
                    
                    res['risk_level'] = risk_level
                    res['decision'] = decision
                    
                    st.session_state['prediction_result'] = res
                    st.session_state['submitted_prediction_inputs'] = input_data
                    st.session_state['prediction_submitted'] = True
                else:
                    st.error(f"Prediction failed: {pred_res.json().get('detail')}")
            except Exception as e:
                st.error(f"Prediction failed to reach backend: {e}")

    # ---------------------------------------------------------
    # RESULT SECTION
    # ---------------------------------------------------------
    if 'prediction_result' in st.session_state:
        res = st.session_state['prediction_result']
        
        # Verify prediction result matches current active model
        if res.get('model_version') != active_version:
            st.error("Active model changed. Please refresh the prediction.")
            return
            
        prob = res['probability'] # Probability of approval
        
        # Calculate Risk and Decision
        if prob >= low_risk_thresh:
            risk_level = "LOW RISK"
            css_class = "low-risk"
            text_class = "low-text"
            msg = "✓ Loan profile appears highly suitable."
            decision = "APPROVE"
        elif prob >= medium_risk_thresh:
            risk_level = "MEDIUM RISK"
            css_class = "medium-risk"
            text_class = "medium-text"
            msg = "⚠️ Loan profile requires manual review."
            decision = "REVIEW"
        else:
            risk_level = "HIGH RISK"
            css_class = "high-risk"
            text_class = "high-text"
            msg = "❌ Loan profile does not meet minimum criteria."
            decision = "REJECT"
            
        st.markdown(f"""
        <div class="result-card {css_class}">
            <div class="risk-title">LOAN RISK ASSESSMENT</div>
            <div class="risk-level {text_class}">{risk_level}</div>
            <div class="risk-conf">Model Confidence: {max(prob, 1-prob)*100:.1f}%</div>
            <div class="risk-msg">{msg}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Probability & Decision")
        c1, c2, c3 = st.columns([1, 1, 1])
        c1.metric("Approval Probability", f"{prob*100:.1f}%")
        c2.metric("Risk Probability", f"{(1-prob)*100:.1f}%")
        c3.metric("AI-Assisted Decision", decision)
        
        # Horizontal Probability Bar
        st.markdown(f"""
        <div style="width: 100%; height: 24px; background-color: #FEE2E2; border-radius: 12px; overflow: hidden; display: flex; margin-bottom: 2rem; border: 1px solid #E2E8F0;">
            <div style="width: {prob*100}%; height: 100%; background-color: #10B981; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; color: white; font-weight: bold; font-size: 0.8rem; transition: width 0.5s ease;">
                {prob*100:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Key Applicant Factors")
        
        # Dynamically display top 6 available features as metrics
        metrics_to_show = []
        for f in ["Cibil_Score", "Annual_Income", "Loan_Amount", "DTI_Ratio", "Employment_Years", "Existing_Loans"]:
            if f in features: metrics_to_show.append(f)
            
        if not metrics_to_show:
            metrics_to_show = [f for f in features if f != 'Applicant_ID'][:6]
            
        m_cols = st.columns(max(len(metrics_to_show), 1))
        for idx, mf in enumerate(metrics_to_show):
            val = st.session_state.get(mf, "-")
            if isinstance(val, (int, float)) and "income" in mf.lower() or "amount" in mf.lower():
                m_cols[idx].metric(mf.replace("_", " "), f"₹{val:,.0f}")
            elif isinstance(val, float):
                m_cols[idx].metric(mf.replace("_", " "), f"{val:.2f}")
            else:
                m_cols[idx].metric(mf.replace("_", " "), str(val))
        
        st.markdown("### Risk Explanation")
        cibil = float(st.session_state.get("Cibil_Score", 0)) if "Cibil_Score" in features else None
        dti = float(st.session_state.get("DTI_Ratio", 0)) if "DTI_Ratio" in features else None
        emp_years = float(st.session_state.get("Employment_Years", 0)) if "Employment_Years" in features else None
        loan_amt = float(st.session_state.get("Loan_Amount", 0)) if "Loan_Amount" in features else None
        income = float(st.session_state.get("Annual_Income", 0)) if "Annual_Income" in features else None
        
        positives = []
        negatives = []
        
        if cibil is not None:
            if cibil >= 750: positives.append(f"CIBIL score of {int(cibil)} is excellent.")
            elif cibil < 600: negatives.append(f"CIBIL score of {int(cibil)} is poor.")
        
        if emp_years is not None:
            if emp_years >= 5: positives.append(f"Stable employment history ({int(emp_years)} years).")
            elif emp_years < 1: negatives.append("Limited employment history (less than 1 year).")
        
        if dti is not None:
            if dti < 0.3: positives.append(f"Healthy DTI ratio ({dti:.2f}).")
            elif dti > 0.5: negatives.append(f"Elevated DTI ratio ({dti:.2f}).")
        
        if income is not None and loan_amt is not None:
            if income > 0 and (loan_amt / income) > 3: negatives.append("Loan amount is relatively high compared to annual income.")
        
        if len(positives) > 0:
            st.success("**Positive indicators:** " + " ".join(positives))
        if len(negatives) > 0:
            st.error("**Risk indicators:** " + " ".join(negatives))
        if len(positives) == 0 and len(negatives) == 0:
            st.info("The model evaluated the applicant based on standard criteria without triggering major extreme indicators.")
            
        # Metadata and Disclaimer
        st.markdown("---")
        st.markdown(f"<div style='font-size:0.85rem; color:#64748B;'><b>Active Model:</b> {model_alg} &nbsp;|&nbsp; <b>Model Version:</b> <code>{active_version}</code> &nbsp;|&nbsp; <b>Prediction Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.75rem; color:#94A3B8; margin-top: 4px;'>AI-assisted prediction for demonstration purposes. This result is not an official banking or financial decision.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
