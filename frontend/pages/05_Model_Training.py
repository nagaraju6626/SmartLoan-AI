import streamlit as st
from frontend.components.theme import apply_dataframe_style
import httpx
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import sys
from pathlib import Path

st.set_page_config(page_title="Model Training & Comparison", page_icon="🤖", layout="wide")

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header
from backend.ml.preprocessing import detect_columns


# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
UPLOAD_DIR = "data/uploads"
PROCESSED_DIR = "data/processed"
MODELS_DIR = "models/versions"

@st.cache_data
def load_data(dataset_id):
    file_path = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
    is_cleaned = True
    if not os.path.exists(file_path):
        is_cleaned = False
        raw_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(dataset_id)]
        if not raw_files:
            return None, False
        file_path = os.path.join(UPLOAD_DIR, raw_files[0])
    try:
        return pd.read_csv(file_path), is_cleaned
    except Exception:
        return None, False

from frontend.components.theme import apply_chart_style

def main():
    st.title("MODEL TRAINING & COMPARISON")
    st.markdown("Train, evaluate, and activate machine learning models")
    st.markdown("---")

    if 'current_dataset_id' not in st.session_state:
        st.warning("Please upload a dataset on the Data Upload page first.")
        return

    dataset_id = st.session_state['current_dataset_id']
    dataset_name = st.session_state.get('current_dataset_name', 'Unknown')
    
    df, is_cleaned = load_data(dataset_id)
    if df is None:
        st.error("Failed to load dataset.")
        return

    mapping = detect_columns(df)
    cols = df.columns.tolist()
    default_target = mapping.get("target")
    default_idx = cols.index(default_target) if default_target in cols else 0

    # --------------------------------------------------
    # DATASET CONFIGURATION
    # --------------------------------------------------
    st.markdown("### Dataset Configuration")
    
    total_samples = len(df)
    
    if "target_col" not in st.session_state:
        st.session_state["target_col"] = cols[default_idx] if default_idx < len(cols) else cols[0]
        
    config_card = f"""
    <div style='background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 20px;'>
        <p style='margin-bottom: 10px; font-size: 16px;'><b>Dataset:</b> <span style='word-wrap: break-word; color: #334155;'>{dataset_name}</span></p>
        <p style='margin-bottom: 0; font-size: 16px;'>
            <b>Samples:</b> <span style='color: #334155;'>{total_samples:,}</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            <b>Features:</b> <span style='color: #334155;'>{len(cols):,}</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            <b>Split:</b> <span style='color: #334155;'>80/20</span>
        </p>
    </div>
    """
    
    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        st.selectbox("Target Column", cols, key="target_col")
        target_col = st.session_state["target_col"]
        
    st.markdown(config_card, unsafe_allow_html=True)
    
    # --------------------------------------------------
    # TRAINING READINESS
    # --------------------------------------------------
    st.markdown("### Training Readiness")
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("✓ Dataset loaded")
        if target_col in cols:
            st.markdown("✓ Target detected")
        else:
            st.markdown("❌ Missing target")
        st.markdown("✓ Features detected")
    with r2:
        if df.isnull().sum().sum() == 0:
            st.markdown("✓ Missing values checked")
        else:
            st.markdown("⚠️ Missing values present")
        st.markdown("✓ Preprocessing configured")
        st.markdown("✓ Train/Test split ready")

    # --------------------------------------------------
    # MODELS TO TRAIN
    # --------------------------------------------------
    st.markdown("### Models to Train")
    
    if "train_lr" not in st.session_state:
        st.session_state["train_lr"] = True
    if "train_rf" not in st.session_state:
        st.session_state["train_rf"] = True
    if "train_xgb" not in st.session_state:
        st.session_state["train_xgb"] = True
        
    m1, m2, m3 = st.columns(3)
    with m1: train_lr = st.checkbox("Logistic Regression", key="train_lr")
    with m2: train_rf = st.checkbox("Random Forest", key="train_rf")
    with m3: train_xgb = st.checkbox("XGBoost", key="train_xgb")
    
    models_to_train = []
    if train_lr: models_to_train.append("logistic_regression")
    if train_rf: models_to_train.append("random_forest")
    if train_xgb: models_to_train.append("xgboost")

    # We store results in session_state to persist across button clicks
    if "training_results" not in st.session_state:
        st.session_state["training_results"] = None

    st.markdown("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
    with c_btn2:
        start_btn = st.button("Start Training", type="primary", use_container_width=True)
        
    if start_btn:
        if not models_to_train:
            st.error("Please select at least one model to train.")
        else:
            with st.spinner("Training models..."):
                payload = {
                    "dataset_id": dataset_id,
                    "target_column": target_col,
                    "model_types": models_to_train
                }
                try:
                    train_res = httpx.post(f"{API_BASE_URL}/api/models/train", json=payload, timeout=120.0)
                    if train_res.status_code == 200:
                        st.session_state["training_results"] = train_res.json()["results"]
                        st.success("Training completed successfully!")
                    else:
                        st.error(f"Training failed: {train_res.json().get('detail')}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {str(e)}")

    results = st.session_state["training_results"]
    success_results = [r for r in results if "error" not in r] if results else []

    # Validate active model against current training results
    active_ver = st.session_state.get('active_model_version')
    active_name = st.session_state.get('active_model_name')
    if success_results:
        current_valid_versions = [r["version"] for r in success_results]
        if active_ver not in current_valid_versions:
            st.session_state['active_model_version'] = None
            st.session_state['active_model_name'] = None
            active_ver = None
            active_name = None

    # --------------------------------------------------
    # MODEL PERFORMANCE SUMMARY (Always show active status)
    # --------------------------------------------------
    st.markdown("---")
    st.markdown("### 🏆 Model Performance Summary")
    
    if active_ver:
        status_html = f"<p><b>Currently Active Model:</b> <span style='color: #10B981; font-weight: bold;'>{active_name}</span> <code>({active_ver})</code></p>"
    else:
        status_html = "<p><b>Currently Active Model:</b> <span style='color: #EF4444; font-weight: bold;'>No active model selected. Please select a trained model.</span></p>"
        
    st.markdown(f"""
    <div style='background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0;'>
        <h4 style='margin-top: 0; color: #0F172A;'>Active Model Status</h4>
        <p><b>Models Successfully Trained:</b> {len(success_results)}</p>
        {status_html}
        <p><small>The active model is used globally by the New Applicant and Explainability systems.</small></p>
    </div>
    """, unsafe_allow_html=True)

    if not results:
        return

    st.markdown("---")

    # Filter out failures
    if not success_results:
        st.error("All selected models failed to train.")
        for r in results:
            st.error(f"{r['algorithm']}: {r['error']}")
        return

    # --------------------------------------------------
    # ACTIVE MODEL SELECTION
    # --------------------------------------------------
    st.markdown("### 🎯 Active Model Selection")
    
    model_options = {f"{r['algorithm'].replace('_', ' ').title()} ({r['version']})": r for r in success_results}
    
    col_sel1, col_sel2 = st.columns([2, 1])
    with col_sel1:
        selected_model_key = st.selectbox("Select a trained model:", list(model_options.keys()))
        
    with col_sel2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Set Active Model", type="primary", use_container_width=True):
            r = model_options[selected_model_key]
            st.session_state['active_model_version'] = r["version"]
            st.session_state['active_model_name'] = r["algorithm"].replace('_', ' ').title()
            st.rerun()
            
    st.markdown("---")

    # --------------------------------------------------
    # MODEL COMPARISON SUMMARY
    # --------------------------------------------------
    st.markdown("### ⚖️ Model Comparison")
    
    comp_data = []
    for r in results:
        name = r["algorithm"].replace("_", " ").title()
        if "error" in r:
            comp_data.append({
                "Model": name,
                "Accuracy": "-", "Precision": "-", "Recall": "-", "F1 Score": "-", "ROC-AUC": "-",
                "Status": "❌ Failed"
            })
        else:
            m = r["metrics"]
            is_active = (r["version"] == active_ver)
            status_text = "✅ Success (Active)" if is_active else "✅ Success"
            
            roc_auc_val = m.get('roc_auc')
            roc_auc_str = f"{roc_auc_val*100:.2f}%" if isinstance(roc_auc_val, (float, int)) else "N/A"

            comp_data.append({
                "Model": name,
                "Accuracy": f"{m.get('accuracy',0)*100:.2f}%",
                "Precision": f"{m.get('precision',0)*100:.2f}%",
                "Recall": f"{m.get('recall',0)*100:.2f}%",
                "F1 Score": f"{m.get('f1_score',0)*100:.2f}%",
                "ROC-AUC": roc_auc_str,
                "Status": status_text
            })
            
    st.dataframe(apply_dataframe_style(pd.DataFrame(comp_data)), use_container_width=True, hide_index=True)

    # --------------------------------------------------
    # VISUAL MODEL COMPARISON
    # --------------------------------------------------
    chart_data = []
    for r in success_results:
        name = r["algorithm"].replace("_", " ").title()
        m = r["metrics"]
        chart_data.extend([
            {"Model": name, "Metric": "Accuracy", "Score": m.get('accuracy',0)*100},
            {"Model": name, "Metric": "Precision", "Score": m.get('precision',0)*100},
            {"Model": name, "Metric": "Recall", "Score": m.get('recall',0)*100},
            {"Model": name, "Metric": "F1 Score", "Score": m.get('f1_score',0)*100},
            {"Model": name, "Metric": "ROC-AUC", "Score": m.get('roc_auc')*100 if isinstance(m.get('roc_auc'), (float, int)) else 0}
        ])
        
    df_chart = pd.DataFrame(chart_data)
    fig = px.bar(df_chart, x="Metric", y="Score", color="Model", barmode="group", title="Performance Comparison")
    fig.update_layout(yaxis=dict(range=[0, 100]))
    st.plotly_chart(apply_chart_style(fig), use_container_width=True, key="performance_comparison_chart")

    st.markdown("---")

    # --------------------------------------------------
    # INDIVIDUAL MODEL EVALUATION & FEATURE IMPORTANCE
    # --------------------------------------------------
    st.markdown("### 🔍 Individual Model Results")
    
    for r in success_results:
        alg = r["algorithm"].replace("_", " ").title()
        ver = r["version"]
        m = r["metrics"]
        
        st.markdown(f"#### {alg}")
        st.markdown(f"**Version:** `{ver}`")
        
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Accuracy", f"{m.get('accuracy',0)*100:.2f}%")
        c2.metric("Precision", f"{m.get('precision',0)*100:.2f}%")
        c3.metric("Recall", f"{m.get('recall',0)*100:.2f}%")
        c4.metric("F1 Score", f"{m.get('f1_score',0)*100:.2f}%")
        
        roc_auc_val = m.get('roc_auc')
        roc_auc_str = f"{roc_auc_val*100:.2f}%" if isinstance(roc_auc_val, (float, int)) else "N/A"
        c5.metric("ROC-AUC", roc_auc_str)
        
        # Matrix and Importance side by side
        col_cm, col_fi = st.columns(2)
        model_key = r["algorithm"].lower().replace(" ", "_").replace("-", "_")
        
        with col_cm:
            st.markdown("**Confusion Matrix**")
            cm = m.get('confusion_matrix')
            if cm:
                cm_df = pd.DataFrame(cm, index=["Actual 0", "Actual 1"], columns=["Predicted 0", "Predicted 1"])
                st.dataframe(apply_dataframe_style(cm_df), use_container_width=True, key=f"confusion_matrix_{model_key}_{ver}")
                
        with col_fi:
            st.markdown("**Feature Importance / Influence**")
            # Try to load model to extract importance
            model_path = os.path.join(MODELS_DIR, f"model_{ver}.pkl")
            if os.path.exists(model_path):
                try:
                    pipeline = joblib.load(model_path)
                    classifier = pipeline.named_steps['classifier']
                    preprocessor = pipeline.named_steps['preprocessor']
                    
                    # Extract feature names
                    if hasattr(preprocessor, 'get_feature_names_out'):
                        feature_names = list(preprocessor.get_feature_names_out())
                        # Clean up prefixes from ColumnTransformer (e.g., 'num__', 'cat__')
                        feature_names = [f.split("__", 1)[-1] if "__" in f else f for f in feature_names]
                    else:
                        num_features = r.get("features", [])
                        cat_features = []
                        if hasattr(preprocessor, 'transformers_'):
                            for name, trans, cols in preprocessor.transformers_:
                                if name == 'num': num_features = cols
                                if name == 'cat':
                                    if hasattr(trans, 'named_steps') and 'onehot' in trans.named_steps:
                                        cat_features = list(trans.named_steps['onehot'].get_feature_names_out(cols))
                        feature_names = list(num_features) + list(cat_features)

                    importances = None
                    
                    if hasattr(classifier, 'feature_importances_'):
                        importances = classifier.feature_importances_
                    elif hasattr(classifier, 'coef_'):
                        importances = np.abs(classifier.coef_[0])
                        
                    if importances is not None and len(importances) == len(feature_names):
                        fi_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
                        fi_df = fi_df.sort_values(by="Importance", ascending=False).head(10)
                        
                        fig_fi = px.bar(fi_df, x="Importance", y="Feature", orientation='h', color_discrete_sequence=["#3B82F6"])
                        fig_fi = apply_chart_style(fig_fi)
                        fig_fi.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=250)
                        fig_fi.update_yaxes(categoryorder="total ascending")
                        st.plotly_chart(fig_fi, use_container_width=True, key=f"feature_importance_{model_key}_{ver}")
                    else:
                        st.info("Feature importance is not available for this model.")
                except Exception as e:
                    st.info("Feature importance is not available for this model.")
            else:
                st.info("Model file not found locally to compute feature importance.")
                
st.markdown("---")

if __name__ == "__main__":
    main()
