import os

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write('''import streamlit as st
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header

load_dotenv()
st.set_page_config(
    page_title="Smart Loan Risk System",
    layout="wide",
    initial_sidebar_state="expanded"
)
render_sidebar()

# Custom CSS for fintech styling
custom_css = """
<style>
/* Base Styles */
.stApp { background-color: #F8FAFC; color: #0F172A; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
.stAppViewBlockContainer { padding-top: 0rem !important; }

/* Typography */
h1, h2, h3, h4, h5, h6, p, div { color: #0F172A; }
.text-slate-500 { color: #64748B; }
.text-slate-600 { color: #475569; }
.text-blue-600 { color: #2563EB; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }

/* Buttons */
.btn-primary { background-color: #2563EB; color: white !important; padding: 10px 24px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 14px; transition: background-color 0.2s; display: inline-block; border: 1px solid #2563EB; }
.btn-primary:hover { background-color: #1D4ED8; }
.btn-secondary { background-color: white; color: #2563EB !important; padding: 10px 24px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 14px; border: 1px solid #BFDBFE; transition: background-color 0.2s, border-color 0.2s; display: inline-block; }
.btn-secondary:hover { background-color: #F8FAFC; border-color: #93C5FD; }

/* Layout & Containers */
.section-container { margin-bottom: 64px; }
.card { background-color: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; }
.card-header { font-size: 18px; font-weight: 700; margin-bottom: 12px; color: #0F172A; }
.card-body { font-size: 14px; color: #64748B; line-height: 1.5; flex-grow: 1; margin-bottom: 20px; }

/* Hero Section */
.hero-wrapper { display: flex; gap: 48px; align-items: center; margin-bottom: 72px; padding: 40px 0; }
.hero-content { flex: 1; }
.hero-eyebrow { font-size: 12px; font-weight: 700; color: #2563EB; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }
.hero-title { font-size: 42px; font-weight: 800; line-height: 1.1; margin-bottom: 24px; color: #0B1B33; }
.hero-subtitle { font-size: 16px; color: #475569; line-height: 1.6; margin-bottom: 32px; max-width: 500px; }
.hero-visual { flex: 1; background: white; border-radius: 16px; padding: 32px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); position: relative; }
.visual-label { position: absolute; top: -12px; left: 24px; background: white; padding: 0 12px; font-size: 12px; font-weight: 600; color: #64748B; border: 1px solid #E2E8F0; border-radius: 12px; }

/* Status Badges */
.status-badge { display: inline-flex; align-items: center; justify-content: center; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 600; margin-bottom: 16px; }
.status-success { background-color: #DCFCE7; color: #16A34A; }

/* How It Works Steps */
.step-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.step-item { position: relative; }
.step-number { font-size: 12px; font-weight: 700; color: #2563EB; margin-bottom: 8px; }
.step-title { font-size: 16px; font-weight: 700; margin-bottom: 8px; color: #0F172A; }
.step-desc { font-size: 14px; color: #64748B; line-height: 1.5; }

/* Responsive adjustments for Streamlit's container */
@media (max-width: 768px) {
    .hero-wrapper { flex-direction: column; padding: 24px 0; }
    .step-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: 32px; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Top Header (Search, Notifications, etc.)
render_header()

# State awareness
dataset_name = st.session_state.get('current_dataset_name')
active_model = st.session_state.get('active_model_name')

# 1. HERO SECTION
hero_html = """
<div class="hero-wrapper">
    <div class="hero-content">
        <div class="hero-eyebrow">AI-POWERED LOAN ANALYSIS</div>
        <h1 class="hero-title">Smart Loan Risk &<br><span class="text-blue-600">Approval System</span></h1>
        <p class="hero-subtitle">Predict loan risk, analyze applicant data, and make smarter decisions with Machine Learning and Explainable AI.</p>
        <div style="display: flex; gap: 16px;">
            <a href="Data_Upload" target="_self" class="btn-primary">Upload Dataset &rarr;</a>
            <a href="New_Applicant" target="_self" class="btn-secondary">New Applicant &rarr;</a>
        </div>
    </div>
    
    <div class="hero-visual">
        <div class="visual-label">Illustrative Example</div>
        <div style="border-bottom: 1px solid #F1F5F9; padding-bottom: 16px; margin-bottom: 16px;">
            <div style="font-size: 12px; color: #64748B; font-weight: 600; margin-bottom: 4px;">Risk Level</div>
            <div style="font-size: 24px; font-weight: 800; color: #16A34A; margin-bottom: 4px;">LOW RISK</div>
            <div style="font-size: 14px; color: #64748B;">87% Confidence</div>
        </div>
        
        <div style="border-bottom: 1px solid #F1F5F9; padding-bottom: 16px; margin-bottom: 16px;">
            <div style="font-size: 12px; color: #64748B; font-weight: 600; margin-bottom: 4px;">Decision</div>
            <div style="font-size: 18px; font-weight: 700; color: #0F172A;">&#10003; APPROVED</div>
        </div>
        
        <div>
            <div style="font-size: 12px; color: #64748B; font-weight: 600; margin-bottom: 8px;">AI Insights</div>
            <div style="font-size: 14px; color: #475569; display: flex; flex-direction: column; gap: 6px;">
                <div><span style="color: #16A34A;">&#10003;</span> Income Verified</div>
                <div><span style="color: #16A34A;">&#10003;</span> Low Default Risk</div>
                <div><span style="color: #16A34A;">&#10003;</span> Stable Employment</div>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# 2. QUICK ACTIONS
st.markdown("""
<div class="section-container">
    <h2 style="font-size: 24px; font-weight: 700; margin-bottom: 8px;">Quick Actions</h2>
    <p class="text-slate-500" style="margin-bottom: 24px;">Start exploring the Smart Loan Risk & Approval System.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="card">
        <div class="card-header">Upload Dataset</div>
        <div class="card-body">Import applicant data from CSV or supported data sources.</div>
        <div><a href="Data_Upload" target="_self" class="btn-secondary" style="width: 100%; text-align: center;">Open Data Upload &rarr;</a></div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="card">
        <div class="card-header">Analyze Data</div>
        <div class="card-body">Explore applicant data, data quality, distributions, and important patterns.</div>
        <div><a href="Data_Analysis" target="_self" class="btn-secondary" style="width: 100%; text-align: center;">Open Data Analysis &rarr;</a></div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="card">
        <div class="card-header">Train Models</div>
        <div class="card-body">Train and compare machine-learning models using the uploaded dataset.</div>
        <div><a href="Model_Training" target="_self" class="btn-secondary" style="width: 100%; text-align: center;">Open Model Training &rarr;</a></div>
    </div>
    """, unsafe_allow_html=True)

# Spacer
st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

# 3. HOW IT WORKS
st.markdown("""
<div class="section-container">
    <h2 style="font-size: 24px; font-weight: 700; margin-bottom: 8px;">How It Works</h2>
    <p class="text-slate-500" style="margin-bottom: 32px;">From applicant data to explainable loan decisions.</p>
    
    <div class="step-grid">
        <div class="step-item">
            <div class="step-number">STEP 01</div>
            <div class="step-title">Upload Data</div>
            <div class="step-desc">Import applicant information from CSV or supported sources.</div>
        </div>
        <div class="step-item">
            <div class="step-number">STEP 02</div>
            <div class="step-title">Analyze Data</div>
            <div class="step-desc">Understand data quality, patterns, and important features.</div>
        </div>
        <div class="step-item">
            <div class="step-number">STEP 03</div>
            <div class="step-title">Train Models</div>
            <div class="step-desc">Train and compare machine-learning models using the prepared data.</div>
        </div>
        <div class="step-item">
            <div class="step-number">STEP 04</div>
            <div class="step-title">Predict & Explain</div>
            <div class="step-desc">Generate applicant predictions and understand important risk factors.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Spacer
st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# 4. PLATFORM CAPABILITIES
st.markdown("""
<div class="section-container">
    <h2 style="font-size: 24px; font-weight: 700; margin-bottom: 24px;">Platform Capabilities</h2>
</div>
""", unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)
with p1:
    st.markdown("""<div class="card" style="padding: 20px;"><div class="card-header" style="font-size: 16px;">Data Analysis</div><div class="card-body" style="margin-bottom:0; font-size: 13px;">Analyze applicant data and identify patterns, trends, and data-quality issues.</div></div>""", unsafe_allow_html=True)
with p2:
    st.markdown("""<div class="card" style="padding: 20px;"><div class="card-header" style="font-size: 16px;">Machine Learning</div><div class="card-body" style="margin-bottom:0; font-size: 13px;">Train multiple classification models for loan-risk prediction (Logistic Regression, Random Forest, XGBoost).</div></div>""", unsafe_allow_html=True)
with p3:
    st.markdown("""<div class="card" style="padding: 20px;"><div class="card-header" style="font-size: 16px;">Model Comparison</div><div class="card-body" style="margin-bottom:0; font-size: 13px;">Compare models using supported metrics: Accuracy, Precision, Recall, F1 Score, and ROC-AUC.</div></div>""", unsafe_allow_html=True)
with p4:
    st.markdown("""<div class="card" style="padding: 20px;"><div class="card-header" style="font-size: 16px;">Explainable AI</div><div class="card-body" style="margin-bottom:0; font-size: 13px;">Understand which applicant features influence model predictions.</div></div>""", unsafe_allow_html=True)

# Spacer
st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

# 5. SYSTEM STATUS
st.markdown("""<div class="section-container"><h2 style="font-size: 24px; font-weight: 700; margin-bottom: 24px;">System Status</h2></div>""", unsafe_allow_html=True)

s1, s2 = st.columns(2)

with s1:
    if dataset_name:
        status_html = f"""
        <div class="card" style="border-top: 4px solid #2563EB;">
            <div class="card-header">Dataset Status</div>
            <div class="status-badge status-success">Dataset Available</div>
            <div class="card-body" style="margin-bottom: 0;"><b>Loaded:</b> {dataset_name}</div>
        </div>
        """
    else:
        status_html = """
        <div class="card">
            <div class="card-header">Dataset Status</div>
            <div class="card-body"><b>No dataset uploaded yet.</b><br>Upload a dataset to begin analysis and model training.</div>
            <div><a href="Data_Upload" target="_self" class="btn-primary" style="padding: 8px 16px;">Upload Dataset &rarr;</a></div>
        </div>
        """
    st.markdown(status_html, unsafe_allow_html=True)

with s2:
    if active_model:
        model_html = f"""
        <div class="card" style="border-top: 4px solid #16A34A;">
            <div class="card-header">Model Status</div>
            <div class="status-badge status-success">Active Model</div>
            <div class="card-body" style="margin-bottom: 0;"><b>{active_model}</b> is ready for predictions.</div>
        </div>
        """
    elif st.session_state.get('training_results'):
        model_html = """
        <div class="card">
            <div class="card-header">Model Status</div>
            <div class="card-body"><b>Models trained.</b><br>Select an active model from Model Training & Comparison.</div>
            <div><a href="Model_Training" target="_self" class="btn-primary" style="padding: 8px 16px;">Go to Model Training &rarr;</a></div>
        </div>
        """
    else:
        model_html = """
        <div class="card">
            <div class="card-header">Model Status</div>
            <div class="card-body"><b>No active model selected.</b><br>Train a model and select an active model from Model Training & Comparison.</div>
            <div><a href="Model_Training" target="_self" class="btn-primary" style="padding: 8px 16px;">Go to Model Training &rarr;</a></div>
        </div>
        """
    st.markdown(model_html, unsafe_allow_html=True)

# Spacer
st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

# 6. GET STARTED
st.markdown("""
<div style="background-color: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 40px; text-align: center; margin-bottom: 24px;">
    <h2 style="font-size: 24px; font-weight: 700; margin-bottom: 16px;">Ready to Get Started?</h2>
    <p class="text-slate-500" style="max-width: 600px; margin: 0 auto 32px auto; line-height: 1.6;">Upload your loan dataset and begin analyzing applicant data, training risk models, and generating explainable predictions.</p>
    <a href="Data_Upload" target="_self" class="btn-primary" style="font-size: 16px; padding: 14px 32px;">Upload Dataset &rarr;</a>
</div>
""", unsafe_allow_html=True)

# 7. RESPONSIBLE AI NOTICE
st.markdown("""
<div style="text-align: center; max-width: 700px; margin: 0 auto 48px auto;">
    <p style="font-size: 12px; color: #94A3B8; line-height: 1.6; font-weight: 500;">
        <b>Decision Support Notice</b><br>
        Predictions generated by this system are intended to support analysis and review. Final lending decisions should consider appropriate human review, organizational policies, and applicable requirements.
    </p>
</div>
""", unsafe_allow_html=True)

''')
print("01_Home.py rewritten successfully.")
