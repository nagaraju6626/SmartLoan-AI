import streamlit as st
import httpx
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
# Add parent to path for component imports
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header
load_dotenv()
st.set_page_config(
    page_title="Smart Loan Risk System",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Render global navigation (includes the fixed hamburger toggle)
render_sidebar()
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
def get_kpis():
    try:
        response = httpx.get(f"{API_BASE_URL}/api/analytics/kpis", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            return {
                "total": data.get("total_applications", 1248),
                "approved": data.get("approved_loans", 892),
                "rejected": data.get("rejected_loans", 356),
                "amount": data.get("total_value", "12.4 Cr")
            }
    except:
        pass
    return {"total": 1248, "approved": 892, "rejected": 356, "amount": "12.4 Cr"}
kpis = get_kpis()
import base64
def get_base64_image():
    try:
        # Resolve absolute path to the project root assets folder
        img_path = Path(__file__).resolve().parent.parent.parent / "assets" / "hero_visual.jpg"
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        return ""
hero_img_b64 = get_base64_image()
custom_css = """<style>
/* Base Page Setup */
.stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
.stAppViewBlockContainer { padding-top: 0rem !important; }
/* HERO SECTION */
.hero-section { background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-radius: 20px; padding: 48px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #BFDBFE; }
.hero-left { flex: 1; max-width: 50%; }
.hero-label { font-size: 0.85rem; font-weight: 700; color: #2563EB; letter-spacing: 1px; margin-bottom: 12px; }
.hero-title { font-size: 3rem; font-weight: 800; color: #0F172A; line-height: 1.2; margin-bottom: 16px; }
.hero-title span { color: #2563EB; }
.hero-subtitle { font-size: 1.1rem; color: #475569; line-height: 1.6; margin-bottom: 32px; }
.hero-buttons { display: flex; gap: 16px; margin-bottom: 24px; }
.btn-primary { background-color: #2563EB; color: white !important; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; box-shadow: 0 4px 6px rgba(37, 99, 235, 0.25); transition: 0.2s; }
.btn-secondary { background-color: white; color: #2563EB !important; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; border: 1px solid #BFDBFE; transition: 0.2s; }
.hero-features { display: flex; gap: 16px; font-size: 0.85rem; color: #64748B; font-weight: 600; }
/* HERO RIGHT - 3D VISUAL */
.hero-right { flex: 1; display: flex; justify-content: flex-end; position: relative; height: 400px; z-index: 1; }
.visual-core { width: 320px; height: 320px; border-radius: 24px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2; border: 3px solid #FFFFFF; box-shadow: 0 25px 50px -12px rgba(37, 99, 235, 0.3), 0 0 40px rgba(37, 99, 235, 0.2); }
.float-card { position: absolute; background: white; padding: 16px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); border: 1px solid #F1F5F9; z-index: 3; }
.fc-1 { top: 0; left: 0; width: 180px; }
.fc-2 { bottom: 20px; right: -20px; width: 160px; }
.fc-3 { bottom: 20px; left: 0px; width: 190px; }
.fc-4 { top: 20px; right: 20px; width: 140px; }
.fc-title { font-size: 0.8rem; color: #64748B; font-weight: 600; margin-bottom: 8px; }
.fc-value { font-size: 1.2rem; font-weight: 800; color: #0F172A; }
.fc-value.success { color: #22C55E; }
.fc-sub { font-size: 0.75rem; color: #94A3B8; margin-top: 4px; }
.fc-list { font-size: 0.75rem; color: #475569; line-height: 1.6; }
.fc-list i { color: #22C55E; margin-right: 4px; }
/* KPI CARDS */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 32px; }
.kpi-card { background: white; padding: 24px; border-radius: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; }
.kpi-title { font-size: 0.85rem; color: #64748B; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.kpi-val { font-size: 2rem; font-weight: 800; color: #0F172A; margin: 12px 0 8px 0; }
.kpi-trend { font-size: 0.8rem; font-weight: 600; }
.trend-up { color: #22C55E; }
.trend-down { color: #EF4444; }
/* HOW IT WORKS */
.section-title { font-size: 1.5rem; font-weight: 800; color: #0F172A; margin-bottom: 8px; }
.section-sub { font-size: 1rem; color: #64748B; margin-bottom: 24px; }
.hiw-grid { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 32px; }
.hiw-card { background: white; padding: 24px; border-radius: 16px; border: 1px solid #E2E8F0; flex: 1; position: relative; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
.hiw-num { width: 32px; height: 32px; background: #EFF6FF; color: #2563EB; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; margin-bottom: 16px; }
.hiw-title { font-weight: 700; color: #0F172A; font-size: 1.05rem; margin-bottom: 8px; }
.hiw-desc { color: #64748B; font-size: 0.85rem; line-height: 1.5; }
.hiw-arrow { color: #CBD5E1; font-size: 1.5rem; }
/* BOTTOM BAR */
.bottom-features { background: #EFF6FF; border-radius: 16px; padding: 32px; display: flex; justify-content: space-between; border: 1px solid #BFDBFE; }
.bf-col { flex: 1; text-align: center; padding: 0 20px; border-right: 1px solid #DBEAFE; }
.bf-col:last-child { border-right: none; }
.bf-title { font-weight: 700; color: #0F172A; margin-bottom: 8px; font-size: 1.1rem; }
.bf-desc { color: #64748B; font-size: 0.9rem; }
.bf-icon { font-size: 1.5rem; margin-bottom: 12px; }
</style>"""
st.markdown(custom_css, unsafe_allow_html=True)
# TOP HEADER
render_header()
# HERO SECTION
st.markdown(f"""<div class="hero-section"><div class="hero-left"><div class="hero-label">AI-POWERED LOAN ANALYSIS</div><div class="hero-title">Smart Loan Risk &<br><span>Approval System</span></div><div class="hero-subtitle">Predict loan risk, analyze applicant data, and make smarter decisions<br>with Machine Learning and Explainable AI.</div><div class="hero-buttons"><a href="Data_Upload" target="_self" class="btn-primary">🚀 Get Started</a><a href="Dashboard" target="_self" class="btn-secondary">▶ View Demo</a></div><div class="hero-features"><span>🧠 AI Powered</span><span>🎯 High Accuracy</span><span>🛡️ Explainable AI</span><span>⚡ New Applicant</span></div></div><div class="hero-right"><div class="visual-core" style="background-image: url('data:image/jpeg;base64,{hero_img_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; background-color: transparent; border: none; box-shadow: none;"></div><div class="float-card fc-1"><div class="fc-title">Risk Prediction</div><div class="fc-value success">LOW RISK</div><div class="fc-sub">87% Confidence</div></div><div class="float-card fc-2"><div class="fc-title">Approval Chance</div><div class="fc-value success">92%</div><div class="fc-sub">High Probability</div></div><div class="float-card fc-3"><div class="fc-title">AI Analysis</div><div class="fc-list"><div>✓ Income Verified</div><div>✓ Low Default Risk</div><div>✓ Good Credit Profile</div></div></div><div class="float-card fc-4"><div class="fc-title">Decision</div><div class="fc-value success">✓ APPROVED</div></div></div></div>""", unsafe_allow_html=True)
# KPI SECTION
st.markdown(f"""<div class="kpi-grid"><div class="kpi-card"><div class="kpi-title">👥 Total Applications</div><div class="kpi-val">{kpis["total"]:,}</div><div class="kpi-trend trend-up">↑ 12% from last month</div></div><div class="kpi-card"><div class="kpi-title">🟢 Approved Loans</div><div class="kpi-val">{kpis["approved"]:,}</div><div class="kpi-trend trend-up">↑ 18% from last month</div></div><div class="kpi-card"><div class="kpi-title">🔴 Rejected Loans</div><div class="kpi-val">{kpis["rejected"]:,}</div><div class="kpi-trend trend-down">↓ 5% from last month</div></div><div class="kpi-card"><div class="kpi-title">₹ Total Loan Amount</div><div class="kpi-val">₹{kpis["amount"]}</div><div class="kpi-trend trend-up">↑ 22% from last month</div></div></div>""", unsafe_allow_html=True)
# HOW IT WORKS
st.markdown("""<div class="section-title">How It Works</div><div class="section-sub">From data to decision in four simple steps</div><div class="hiw-grid"><div class="hiw-card"><div class="hiw-num">01</div><div class="hiw-title">📤 Upload Data</div><div class="hiw-desc">Import applicant data from CSV or database</div></div><div class="hiw-arrow">→</div><div class="hiw-card"><div class="hiw-num">02</div><div class="hiw-title">🧠 AI Analysis</div><div class="hiw-desc">Machine learning models analyze risk factors</div></div><div class="hiw-arrow">→</div><div class="hiw-card"><div class="hiw-num">03</div><div class="hiw-title">📊 Get Insights</div><div class="hiw-desc">View predictions with explainable AI</div></div><div class="hiw-arrow">→</div><div class="hiw-card"><div class="hiw-num">04</div><div class="hiw-title">📄 Make Decisions</div><div class="hiw-desc">Approve or reject with confidence</div></div></div>""", unsafe_allow_html=True)
# BOTTOM FEATURES
st.markdown("""<div class="bottom-features"><div class="bf-col"><div class="bf-icon">🎯</div><div class="bf-title">High Accuracy</div><div class="bf-desc">Advanced ML models for reliable predictions</div></div><div class="bf-col"><div class="bf-icon">🛡️</div><div class="bf-title">Explainable AI</div><div class="bf-desc">Understand why decisions are made</div></div><div class="bf-col"><div class="bf-icon">⚡</div><div class="bf-title">Real-time Processing</div><div class="bf-desc">Instant predictions and insights</div></div></div>""", unsafe_allow_html=True)
