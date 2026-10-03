import streamlit as st
import httpx
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import joblib

st.set_page_config(
    page_title="Explainability",
    layout="wide"
)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header

render_sidebar()
render_header()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def apply_custom_css():
    st.markdown("""
    <style>
    .info-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .result-card {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border: 1px solid #E2E8F0;
        margin-bottom: 2rem;
    }
    .metric-value { font-size: 2rem; font-weight: 800; color: #0F172A; }
    .metric-label { font-size: 0.9rem; font-weight: 600; color: #64748B; text-transform: uppercase; }
    
    .low-risk { color: #10B981; }
    .medium-risk { color: #F59E0B; }
    .high-risk { color: #EF4444; }
    </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()
    st.title("Explainability")
    st.markdown("Understand why the model made a loan risk prediction.")
    st.markdown("---")

    if 'active_model_version' not in st.session_state:
        st.warning("Please train and select an active model from the Model Training page first.")
        return
        
    if 'prediction_result' not in st.session_state:
        st.warning("No applicant prediction is available yet. Submit an applicant from the New Applicant page to view explainability.")
        return

    active_version = st.session_state['active_model_version']
    res = st.session_state['prediction_result']
    
    # ---------------------------------------------------------
    # SECTION 1 - ACTIVE MODEL
    # ---------------------------------------------------------
    st.markdown("### SECTION 1 — Active Model")
    
    metadata_path = os.path.join("models", "metadata", f"{active_version}.json")
    model_alg = "Unknown"
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            meta = json.load(f)
            model_alg = meta.get("algorithm", "").replace("_", " ").title()
            
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="info-card"><div class="metric-label">Active Model Name</div><div style="font-size:1.2rem;font-weight:700;">{model_alg}</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="info-card"><div class="metric-label">Model Version</div><div style="font-size:1.2rem;font-weight:700;"><code>{active_version}</code></div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="info-card"><div class="metric-label">Model Type</div><div style="font-size:1.2rem;font-weight:700;">Loan Risk Classification</div></div>""", unsafe_allow_html=True)
        
    # ---------------------------------------------------------
    # SECTION 2 - PREDICTION SUMMARY
    # ---------------------------------------------------------
    st.markdown("### SECTION 2 — Prediction Summary")
    
    prob = res['probability']
    risk_level = res['risk_level']
    conf = max(prob, 1-prob) * 100
    
    if risk_level == "Low Risk" or risk_level == "LOW RISK": color = "low-risk"
    elif risk_level == "Medium Risk" or risk_level == "MEDIUM RISK": color = "medium-risk"
    else: color = "high-risk"
    
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""<div class="result-card"><div class="metric-label">Prediction Result</div><div class="metric-value {color}">{risk_level.upper()}</div></div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""<div class="result-card"><div class="metric-label">Approval Probability</div><div class="metric-value">{prob*100:.1f}%</div></div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""<div class="result-card"><div class="metric-label">Risk Probability</div><div class="metric-value">{(1-prob)*100:.1f}%</div></div>""", unsafe_allow_html=True)
    with r4:
        st.markdown(f"""<div class="result-card"><div class="metric-label">Model Confidence</div><div class="metric-value">{conf:.1f}%</div></div>""", unsafe_allow_html=True)

    # Reconstruct input features
    input_data = st.session_state.get('submitted_prediction_inputs', {})
    
    # Check if we successfully got input_data, if not we fallback
    if not input_data:
        try:
            f_res = httpx.get(f"{API_BASE_URL}/api/predict/features/{active_version}")
            if f_res.status_code == 200:
                features = f_res.json()["features"]
                for f in features:
                    if f != 'Applicant_ID':
                        input_data[f] = st.session_state.get(f)
        except Exception:
            pass

    # ---------------------------------------------------------
    # SECTION 3 - KEY FACTORS
    # ---------------------------------------------------------
    st.markdown("### SECTION 3 — Key Factors")
    st.markdown("Applicant features that contributed to the prediction:")
    
    kf1, kf2, kf3, kf4, kf5, kf6 = st.columns(6)
    kf1.metric("CIBIL Score", input_data.get("Cibil_Score", "-"))
    
    income = input_data.get('Annual_Income', "-")
    if isinstance(income, (int, float)): income = f"₹{income:,.0f}"
    kf2.metric("Annual Income", income)
    
    loan_amt = input_data.get('Loan_Amount', "-")
    if isinstance(loan_amt, (int, float)): loan_amt = f"₹{loan_amt:,.0f}"
    kf3.metric("Loan Amount", loan_amt)
    
    dti = input_data.get('DTI_Ratio', "-")
    if isinstance(dti, (int, float)): dti = f"{dti:.2f}"
    kf4.metric("DTI Ratio", dti)
    
    kf5.metric("Emp. Years", input_data.get("Employment_Years", "-"))
    kf6.metric("Existing Loans", input_data.get("Existing_Loans", "-"))

    # ---------------------------------------------------------
    # SECTION 4 & 5 - EXPLANATION & CONTRIBUTIONS
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### SECTION 4 — Feature Contribution")
    
    with st.spinner("Extracting explanation values..."):
        has_local_exp = False
        features_exp = []
        
        cache_key = f"explanation_v2_{active_version}_{res.get('probability')}"
        if cache_key in st.session_state:
            features_exp = st.session_state[cache_key]["features_exp"]
            has_local_exp = st.session_state[cache_key]["has_local_exp"]
        else:
            # Try SHAP first
            if input_data:
                try:
                    payload = {"version": active_version, "features": input_data}
                    shap_res = httpx.post(f"{API_BASE_URL}/api/predict/explain", json=payload, timeout=10.0)
                    if shap_res.status_code == 200:
                        explanation = shap_res.json()
                        features_exp = explanation.get("features", [])
                        if features_exp: has_local_exp = True
                except Exception as e:
                    pass
                    
            # Fallback to Global Feature Importances
            if not has_local_exp:
                try:
                    model_path = os.path.join("models", "versions", f"model_{active_version}.pkl")
                    if os.path.exists(model_path):
                        pipeline = joblib.load(model_path)
                        classifier = pipeline.named_steps.get("classifier") or pipeline.steps[-1][1]
                        
                        # Extract feature names if possible
                        feature_names = []
                        try:
                            preprocessor = pipeline.named_steps.get('preprocessor')
                            if preprocessor:
                                num_features = preprocessor.transformers_[0][2]
                                feature_names.extend(num_features)
                                cat_features = preprocessor.transformers_[1][2]
                                onehot_encoder = preprocessor.transformers_[1][1].named_steps['onehot']
                                feature_names.extend(onehot_encoder.get_feature_names_out(cat_features))
                        except Exception:
                            pass
                            
                        if hasattr(classifier, "feature_importances_"):
                            imp = classifier.feature_importances_
                            if not feature_names or len(feature_names) != len(imp):
                                feature_names = [list(input_data.keys())[i] if i < len(input_data) else f"Feature_{i}" for i in range(len(imp))]
                            
                            for i, f_name in enumerate(feature_names):
                                if i < len(imp):
                                    features_exp.append({"feature": f_name, "shap_value": imp[i]})
                            has_local_exp = True
                        elif hasattr(classifier, "coef_"):
                            coefs = classifier.coef_[0]
                            if not feature_names or len(feature_names) != len(coefs):
                                feature_names = [list(input_data.keys())[i] if i < len(input_data) else f"Feature_{i}" for i in range(len(coefs))]
                                
                            for i, f_name in enumerate(feature_names):
                                if i < len(coefs):
                                    features_exp.append({"feature": f_name, "shap_value": coefs[i]})
                            has_local_exp = True
                except Exception as e:
                    pass
            
            st.session_state[cache_key] = {"features_exp": features_exp, "has_local_exp": has_local_exp}

        if has_local_exp and features_exp:
            df_exp = pd.DataFrame(features_exp)
            
            # Validate and filter
            has_valid_data = False
            if 'feature' in df_exp.columns and 'shap_value' in df_exp.columns:
                df_exp['shap_value'] = pd.to_numeric(df_exp['shap_value'], errors='coerce')
                df_exp = df_exp.dropna(subset=['feature', 'shap_value'])
                df_exp = df_exp[~np.isinf(df_exp['shap_value'])]
                df_exp['feature'] = df_exp['feature'].astype(str).str.strip()
                df_exp = df_exp[df_exp['feature'] != '']
                if len(df_exp) > 0:
                    has_valid_data = True
                    
            if has_valid_data:
                # Sort by absolute magnitude
                df_exp['abs_shap'] = df_exp['shap_value'].abs()
                df_exp = df_exp.sort_values(by='abs_shap', ascending=True).tail(10)
                
                df_exp['Impact'] = df_exp['shap_value'].apply(lambda x: 'Supports Approval (Positive)' if x > 0 else 'Supports Risk (Negative)')
                
                fig = px.bar(df_exp, x="shap_value", y="feature", orientation='h', 
                             color='Impact', 
                             color_discrete_map={'Supports Approval (Positive)': '#10B981', 'Supports Risk (Negative)': '#EF4444'},
                             title="Top Feature Contributions to this Prediction",
                             labels={"shap_value": "Contribution Value", "feature": "Feature"},
                             text_auto='.3f')
                
                from frontend.components.theme import apply_chart_style
                fig = apply_chart_style(fig)
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Dynamic textual explanation
                st.markdown("### SECTION 5 — Explanation")
                
                top_positive = df_exp[df_exp['shap_value'] > 0].sort_values(by='abs_shap', ascending=False)
                top_negative = df_exp[df_exp['shap_value'] < 0].sort_values(by='abs_shap', ascending=False)
                
                prob_percent = prob * 100
                
                exp_text = f"The applicant is classified as **{risk_level}** with an approval probability of **{prob_percent:.1f}%**. "
                
                top_features = [f.replace("_", " ") for f in df_exp.sort_values(by='abs_shap', ascending=False).head(4)['feature'].tolist()]
                if top_features:
                    exp_text += f"The strongest factors influencing this prediction include the applicant's {', '.join(top_features)}. "
                
                if not top_positive.empty:
                    pos_feats = [f.replace("_", " ") for f in top_positive.head(2)['feature'].tolist()]
                    exp_text += f"\n\n- **{', '.join(pos_feats)}** contributed positively to the prediction (supported lower risk)."
                    
                if not top_negative.empty:
                    neg_feats = [f.replace("_", " ") for f in top_negative.head(2)['feature'].tolist()]
                    exp_text += f"\n- Conversely, **{', '.join(neg_feats)}** increased the estimated risk."
                    
                st.info(exp_text, icon="ℹ️")
            else:
                st.info("Feature contribution data is not available for this prediction.")
                
        else:
            st.info("Feature contribution data is not available for this prediction.")

    st.markdown("### SECTION 6 — Important Notice")
    st.markdown("<div style='font-size:0.85rem; color:#64748B; padding:1rem; border:1px solid #E2E8F0; border-radius:8px; background:#F8FAFC;'>This explanation is for understanding the model prediction and should not be treated as an official financial decision.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

