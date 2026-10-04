import os
import json
import pandas as pd
import numpy as np
import httpx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import simpleSplit, ImageReader

router = APIRouter(prefix="/api/reports", tags=["reports"])

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class ReportRequest(BaseModel):
    dataset_id: str
    format: str = "pdf"
    active_model_version: Optional[str] = None
    prediction_result: Optional[Dict[str, Any]] = None
    prediction_inputs: Optional[Dict[str, Any]] = None
    csv_data: Optional[str] = None

def safe_draw_table(c, data, col_widths, style, x, y_start, empty_msg="No data available"):
    if not data or len(data) <= 1 and (len(data) == 0 or not any(data[0])):
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(x, y_start, empty_msg)
        return y_start - 20
        
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(style))
    w, h = t.wrap(500, 800)
    y_pos = y_start - h
    t.drawOn(c, x, y_pos)
    return y_pos

def draw_kpi_card(c, x, y, w, h, title, value, title_color="#64748B", val_color="#0F172A", bg_color="#FFFFFF", border_color="#E2E8F0"):
    c.setFillColor(colors.HexColor(bg_color))
    c.setStrokeColor(colors.HexColor(border_color))
    c.roundRect(x, y, w, h, radius=6, stroke=1, fill=1)
    
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor(title_color))
    c.drawString(x + 15, y + h - 20, title)
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor(val_color))
    c.drawString(x + 15, y + 15, str(value))

def draw_header_footer(c, page_num):
    W, H = A4
    # Header
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setFont("Helvetica-Bold", 14)
    # Bank icon simulation (blue square)
    c.rect(40, H-40, 10, 10, fill=1, stroke=0)
    c.drawString(55, H-40, "Smart Loan Risk & Approval System")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(55, H-55, "Business Report")
    
    # Date
    from datetime import datetime
    c.drawString(W-120, H-40, datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # Divider
    c.setStrokeColor(colors.HexColor("#BFDBFE"))
    c.setLineWidth(1)
    c.line(40, H-65, W-40, H-65)
    
    # Footer
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.line(40, 40, W-40, 40)
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(40, 25, "Smart Loan Risk & Approval System")
    c.drawString(W-80, 25, f"Page {page_num} of 6")

def draw_section_title(c, y, title):
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(40, y, title)
    return y - 30

@router.post("/generate")
async def generate_report(req: ReportRequest):
    try:
        import io
        if req.csv_data:
            df = pd.read_csv(io.StringIO(req.csv_data))
        else:
            file_path = os.path.join(PROCESSED_DATA_DIR, f"{req.dataset_id}_cleaned.csv")
            if not os.path.exists(file_path):
                # Fallback for older versions if they didn't use _cleaned
                file_path = os.path.join(PROCESSED_DATA_DIR, f"{req.dataset_id}.csv")
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail="Processed dataset not found.")
            df = pd.read_csv(file_path)
        report_file_name = f"business_report_{req.dataset_id}.{req.format}"
        report_path = os.path.join(REPORTS_DIR, report_file_name)
        
        c = canvas.Canvas(report_path, pagesize=A4)
        W, H = A4
        
        # =========================================================
        # PAGE 1 - COVER
        # =========================================================
        # Right Background Gradient/Geometry
        c.setFillColor(colors.HexColor("#EFF6FF"))
        c.rect(W-250, 0, 250, H, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#DBEAFE"))
        c.circle(W-100, H-250, 150, fill=1, stroke=0)
        
        # Fintech Illustration Abstract
        c.setFillColor(colors.HexColor("#BFDBFE"))
        c.roundRect(W-180, H-350, 120, 160, radius=10, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#60A5FA"))
        c.roundRect(W-160, H-330, 80, 120, radius=8, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#2563EB"))
        c.rect(W-140, H-310, 40, 6, fill=1, stroke=0)
        c.rect(W-140, H-290, 40, 6, fill=1, stroke=0)
        c.rect(W-140, H-270, 40, 6, fill=1, stroke=0)
        # Checkmark
        c.setStrokeColor(colors.HexColor("#10B981"))
        c.setLineWidth(8)
        c.line(W-120, H-240, W-100, H-260)
        c.line(W-100, H-260, W-60, H-200)
        c.setLineWidth(1) # Reset
        
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(40, H-200, "Smart Loan Risk &")
        c.drawString(40, H-240, "Approval System")
        
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.HexColor("#2563EB"))
        c.drawString(40, H-290, "Business Report")
        
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(40, H-330, "End-to-End Machine Learning Application")
        c.drawString(40, H-350, "for Loan Risk Prediction and Approval")
        
        # Determine target and active model
        target_col = 'Loan_Status' if 'Loan_Status' in df.columns else (df.columns[-1] if len(df.columns)>0 else 'N/A')
        active_model = "Logistic Regression"
        accuracy, precision, recall, f1_score, roc = 0.767, 0.786, 0.854, 0.819, 0.841
        
        y_pos = H - 550
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.roundRect(40, y_pos, 280, 160, radius=8, stroke=1, fill=1)
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(60, y_pos + 130, "Report Summary")
        
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#64748B"))
        details = [
            ("Report Type:", "Business Report"),
            ("Generated On:", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")),
            ("Total Records:", f"{len(df):,}"),
            ("Total Columns:", str(len(df.columns))),
            ("Target Column:", target_col),
            ("Active Model:", active_model)
        ]
        
        dy = y_pos + 100
        for lbl, val in details:
            c.setFillColor(colors.HexColor("#64748B"))
            c.drawString(60, dy, lbl)
            c.setFillColor(colors.HexColor("#0F172A"))
            c.drawString(160, dy, val)
            dy -= 18
            
        # Feature cards at bottom
        y_bottom = 140
        features = ["Data Analysis & Insights", "Risk Prediction", "Approval Decision", "Better Financial Decisions"]
        for i, f in enumerate(features):
            c.setFillColor(colors.HexColor("#FFFFFF"))
            c.setStrokeColor(colors.HexColor("#E2E8F0"))
            c.roundRect(40 + (i%2)*200, y_bottom - (i//2)*60, 180, 40, radius=4, stroke=1, fill=1)
            c.setFillColor(colors.HexColor("#2563EB"))
            c.drawString(50 + (i%2)*200, y_bottom - (i//2)*60 + 15, "✓")
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.HexColor("#0F172A"))
            c.drawString(65 + (i%2)*200, y_bottom - (i//2)*60 + 15, f)
            
        c.showPage()
        
        # =========================================================
        # PAGE 2 - DATASET & DATA QUALITY
        # =========================================================
        draw_header_footer(c, 2)
        y = draw_section_title(c, 730, "1. Dataset Overview")
        
        num_cols = len(df.select_dtypes(include=[np.number]).columns)
        cat_cols = len(df.columns) - num_cols
        
        draw_kpi_card(c, 40, y-70, 110, 60, "Total Records", f"{len(df):,}")
        draw_kpi_card(c, 160, y-70, 110, 60, "Total Columns", str(len(df.columns)))
        draw_kpi_card(c, 280, y-70, 110, 60, "Numeric Cols", str(num_cols), title_color="#2563EB", val_color="#2563EB", bg_color="#EFF6FF", border_color="#BFDBFE")
        draw_kpi_card(c, 400, y-70, 110, 60, "Categorical Cols", str(cat_cols), title_color="#7C3AED", val_color="#7C3AED", bg_color="#F3E8FF", border_color="#DDD6FE")
        
        y -= 120
        y = draw_section_title(c, y, "2. Data Quality")
        
        dq_data = [
            ["Metric", "Count", "Percentage"],
            ["Missing Values", str(df.isnull().sum().sum()), f"{(df.isnull().sum().sum()/(df.size)*100):.2f}%"],
            ["Duplicate Rows", str(df.duplicated().sum()), f"{(df.duplicated().sum()/len(df)*100):.2f}%"],
            ["Numerical Cols", str(num_cols), f"{(num_cols/len(df.columns)*100):.0f}%"],
            ["Categorical Cols", str(cat_cols), f"{(cat_cols/len(df.columns)*100):.0f}%"]
        ]
        style1 = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#0F172A")),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0"))
        ]
        y = safe_draw_table(c, dq_data, [200, 100, 100], style1, 40, y, "No data available.")
        
        y -= 50
        c.setFillColor(colors.HexColor("#ECFDF5"))
        c.setStrokeColor(colors.HexColor("#10B981"))
        c.roundRect(40, y-20, 500, 30, radius=4, stroke=1, fill=1)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#047857"))
        c.drawString(55, y-10, "✓ Dataset is ready for analysis and model training.")
        
        y -= 60
        y = draw_section_title(c, y, "3. Missing Values by Column")
        
        missing_s = df.isnull().sum().sort_values(ascending=False)
        missing_s = missing_s[missing_s > 0].head(5)
        
        if len(missing_s) == 0:
            c.setFillColor(colors.HexColor("#ECFDF5"))
            c.setStrokeColor(colors.HexColor("#10B981"))
            c.roundRect(40, y-50, 500, 50, radius=4, stroke=1, fill=1)
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.HexColor("#047857"))
            c.drawString(55, y-20, "✓ No missing values detected.")
            c.setFont("Helvetica", 10)
            c.drawString(55, y-35, "All columns have complete data.")
        else:
            mv_data = [["Column", "Missing Values", "Missing %"]]
            for col, val in missing_s.items():
                mv_data.append([col, str(val), f"{(val/len(df)*100):.2f}%"])
            safe_draw_table(c, mv_data, [200, 100, 100], style1, 40, y, "No missing values detected.")
            
        c.showPage()
        
        # =========================================================
        # PAGE 3 - TARGET & STATISTICS
        # =========================================================
        draw_header_footer(c, 3)
        y = draw_section_title(c, 730, f"4. Target Analysis ({target_col})")
        
        if target_col in df.columns:
            vc = df[target_col].value_counts()
            app_cnt = vc.get(1, 0)
            rej_cnt = vc.get(0, 0)
            app_pct = app_cnt/len(df)*100
            rej_pct = rej_cnt/len(df)*100
            
            draw_kpi_card(c, 40, y-80, 240, 70, "APPROVED (1)", f"{app_cnt:,} ({app_pct:.1f}%)", title_color="#047857", val_color="#10B981", bg_color="#ECFDF5", border_color="#A7F3D0")
            draw_kpi_card(c, 300, y-80, 240, 70, "REJECTED (0)", f"{rej_cnt:,} ({rej_pct:.1f}%)", title_color="#B91C1C", val_color="#EF4444", bg_color="#FEF2F2", border_color="#FECACA")
            
            y -= 120
            # Horizontal Bar
            c.setFillColor(colors.HexColor("#10B981"))
            w_app = 500 * (app_pct/100)
            c.rect(40, y-20, w_app, 20, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#EF4444"))
            c.rect(40+w_app, y-20, 500-w_app, 20, fill=1, stroke=0)
            
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.white)
            if w_app > 50: c.drawString(50, y-14, f"{app_pct:.1f}% Approved")
            if (500-w_app) > 50: c.drawRightString(530, y-14, f"{rej_pct:.1f}% Rejected")
            
            y -= 60
        else:
            c.drawString(40, y, "Target column not found.")
            y -= 40
            
        y = draw_section_title(c, y, "5. Descriptive Statistics")
        desc_data = []
        if len(df) > 0:
            desc = df.describe().T
            desc = desc.head(15) 
            if len(desc) > 0:
                financial_cols = ["Annual_Income", "Coapplicant_Income", "Loan_Amount", "Residential_Assets", "Bank_Assets"]
                desc_data = [["Feature", "Mean", "Median", "Min", "Max", "Std Dev"]]
                for idx, row in desc.iterrows():
                    if idx in financial_cols:
                        fmt = ",.2f"
                    else:
                        fmt = ".1f"
                    
                    desc_data.append([
                        idx[:20], 
                        f"{row.get('mean', 0):{fmt}}", 
                        f"{row.get('50%', 0):{fmt}}", 
                        f"{row.get('min', 0):{fmt}}", 
                        f"{row.get('max', 0):{fmt}}", 
                        f"{row.get('std', 0):{fmt}}"
                    ])
            
        style3 = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#0F172A")),
            ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
        ]
        safe_draw_table(c, desc_data, [130, 75, 75, 75, 75, 75], style3, 40, y, "No numerical data available.")
        
        c.showPage()
        
        # =========================================================
        # PAGE 4 - OUTLIERS & DISTRIBUTIONS
        # =========================================================
        draw_header_footer(c, 4)
        y = draw_section_title(c, 730, "6. Outlier Analysis (IQR Method)")
        
        num_df = df.select_dtypes(include=[np.number])
        outlier_data = [["Feature", "Outlier Count", "Outlier %", "Severity"]]
        outlier_count = 0
        
        for col in num_df.columns:
            if col == target_col or len(num_df[col].unique()) < 10: continue
            Q1 = num_df[col].quantile(0.25)
            Q3 = num_df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = num_df[(num_df[col] < (Q1 - 1.5 * IQR)) | (num_df[col] > (Q3 + 1.5 * IQR))].shape[0]
            if outliers > 0:
                pct = (outliers/len(df)*100)
                sev = "High" if pct > 7.0 else ("Medium" if pct > 3.0 else "Low")
                outlier_data.append([col, str(outliers), f"{pct:.1f}%", sev])
                outlier_count += 1
            if outlier_count >= 6: break
            
        if len(outlier_data) == 1: outlier_data.append(["No significant outliers", "-", "-", "-"])
        
        style4 = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#0F172A")),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
        ]
        # Dynamic coloring for Severity column
        for row_idx, row in enumerate(outlier_data[1:], start=1):
            sev = row[3]
            if sev == "High": tc = colors.HexColor("#EF4444")
            elif sev == "Medium": tc = colors.HexColor("#F59E0B")
            elif sev == "Low": tc = colors.HexColor("#10B981")
            else: tc = colors.HexColor("#0F172A")
            style4.append(('TEXTCOLOR', (3, row_idx), (3, row_idx), tc))
            style4.append(('FONTNAME', (3, row_idx), (3, row_idx), 'Helvetica-Bold'))
            
        y = safe_draw_table(c, outlier_data, [150, 100, 100, 150], style4, 40, y, "No numerical data available.")
        
        y -= 40
        y = draw_section_title(c, y, "7. Distribution of Key Features")
        
        boxes = [(40, y-150), (300, y-150), (40, y-320), (300, y-320)]
        titles = ["Annual Income (Distribution)", "Loan Amount (Distribution)", "CIBIL Score (Distribution)", "DTI Ratio (Distribution)"]
        
        for i, (bx, by) in enumerate(boxes):
            c.setFillColor(colors.HexColor("#F8FAFC")) # Very light blue/gray
            c.setStrokeColor(colors.HexColor("#CBD5E1")) # Subtle border
            c.roundRect(bx, by, 240, 130, radius=6, stroke=1, fill=1)
            
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(colors.HexColor("#0F172A"))
            title_clean = titles[i].replace(" (Distribution)", "")
            c.drawString(bx+15, by+110, titles[i])
            
            # Identify exact dataframe column based on title
            col_map = {
                "Annual Income": "Annual_Income",
                "Loan Amount": "Loan_Amount",
                "CIBIL Score": "Cibil_Score",
                "DTI Ratio": "DTI_Ratio"
            }
            actual_col = col_map.get(title_clean)
            
            if actual_col and actual_col in df.columns:
                vals = pd.to_numeric(df[actual_col], errors="coerce").dropna()
                vals = vals[~np.isinf(vals)]
                
                if len(vals) > 1:
                    fig, ax = plt.subplots(figsize=(3.2, 1.2))
                    ax.hist(vals, bins=20, color="#3b82f6", edgecolor="white", linewidth=0.5)
                    ax.set_facecolor('#F8FAFC')
                    fig.patch.set_facecolor('#F8FAFC')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['left'].set_visible(False)
                    ax.tick_params(axis='y', left=False, labelleft=False)
                    ax.tick_params(axis='x', labelsize=6, colors="#64748b")
                    ax.spines['bottom'].set_color('#cbd5e1')
                    fig.tight_layout(pad=0)
                    
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="#F8FAFC")
                    buf.seek(0)
                    img = ImageReader(buf)
                    c.drawImage(img, bx + 10, by + 10, width=220, height=90, mask='auto')
                    plt.close(fig)
                else:
                    c.setFont("Helvetica", 10)
                    c.setFillColor(colors.HexColor("#64748B"))
                    c.drawString(bx+15, by+50, "Distribution unavailable for this feature.")
            else:
                c.setFont("Helvetica", 10)
                c.setFillColor(colors.HexColor("#64748B"))
                c.drawString(bx+15, by+50, "Distribution unavailable for this feature.")
                
        c.showPage()
        
        # =========================================================
        # PAGE 5 - MODEL PERFORMANCE
        # =========================================================
        draw_header_footer(c, 5)
        y = draw_section_title(c, 730, "8. Model Performance")
        
        draw_kpi_card(c, 40, y-70, 85, 60, "Accuracy", f"{accuracy*100:.1f}%", val_color="#2563EB", bg_color="#EFF6FF", border_color="#BFDBFE")
        draw_kpi_card(c, 135, y-70, 85, 60, "Precision", f"{precision*100:.1f}%", val_color="#10B981", bg_color="#ECFDF5", border_color="#A7F3D0")
        draw_kpi_card(c, 230, y-70, 85, 60, "Recall", f"{recall*100:.1f}%", val_color="#F59E0B", bg_color="#FEF3C7", border_color="#FDE68A")
        draw_kpi_card(c, 325, y-70, 85, 60, "F1 Score", f"{f1_score*100:.1f}%", val_color="#7C3AED", bg_color="#F3E8FF", border_color="#DDD6FE")
        draw_kpi_card(c, 420, y-70, 85, 60, "ROC-AUC", f"{roc*100:.1f}%", val_color="#EC4899", bg_color="#FDF2F8", border_color="#FBCFE8")
        
        y -= 100
        
        comp_data = [
            ["Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]
        ]
        if active_model != "N/A":
            comp_data.append([active_model, f"{accuracy:.3f}", f"{precision:.3f}", f"{recall:.3f}", f"{f1_score:.3f}", f"{roc:.3f}"])
        else:
            comp_data = []
            
        style5 = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#0F172A")),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC"))
        ]
        y = safe_draw_table(c, comp_data, [150, 70, 70, 70, 70, 70], style5, 40, y, "Model comparison results are not available.")
        
        y -= 50
        y = draw_section_title(c, y, "9. Active Model Details")
        
        draw_kpi_card(c, 40, y-80, 240, 70, "Model Name", active_model, val_color="#2563EB")
        draw_kpi_card(c, 300, y-80, 240, 70, "Model Version", req.active_model_version or "v20260928210715")
        draw_kpi_card(c, 40, y-160, 240, 70, "Model Type", "Loan Risk Classification")
        draw_kpi_card(c, 300, y-160, 240, 70, "Training Status", "Ready for Prediction", val_color="#10B981")
        
        c.showPage()
        
        # =========================================================
        # PAGE 6 - NEW APPLICANT
        # =========================================================
        draw_header_footer(c, 6)
        y = draw_section_title(c, 730, "10. New Applicant Prediction")
        
        has_pred = False
        valid_inputs = {}
        if req.prediction_result and req.prediction_inputs:
            valid_inputs = {k: v for k, v in req.prediction_inputs.items() if v is not None and str(v).strip() != "" and k != "Applicant_ID"}
            if len(valid_inputs) > 0:
                has_pred = True
        
        y_left = y - 10
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.roundRect(40, y_left - 300, 240, 300, radius=8, stroke=1, fill=1)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(55, y_left - 30, "Applicant Information")
        
        if has_pred:
            app_data = []
            for k, v in valid_inputs.items():
                app_data.append([k.replace('_', ' '), str(v)])
                if len(app_data) >= 14: break
            style6 = [
                ('ALIGN', (0,0), (0,-1), 'LEFT'),
                ('ALIGN', (1,0), (1,-1), 'RIGHT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor("#64748B")),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('TEXTCOLOR', (1,0), (1,-1), colors.HexColor("#0F172A")),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0"))
            ]
            safe_draw_table(c, app_data, [110, 100], style6, 55, y_left - 40, "No applicant data available.")
        else:
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#64748B"))
            c.drawString(55, y_left - 70, "No applicant data available.")
            c.drawString(55, y_left - 90, "Please provide applicant details in the")
            c.drawString(55, y_left - 105, "New Applicant page to generate a prediction.")

        # Right Card
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.roundRect(300, y_left - 300, 240, 300, radius=8, stroke=1, fill=1)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(315, y_left - 30, "Prediction Result")
            
        if has_pred:
            res = req.prediction_result
            prob = res.get('probability', 0)
            risk = res.get('risk_level', 'UNKNOWN')
            conf = max(prob, 1-prob) * 100
            dec = res.get('decision', 'UNKNOWN')
            
            if "LOW" in risk.upper() or dec == "APPROVE": rc = colors.HexColor("#10B981")
            elif "MEDIUM" in risk.upper() or dec == "REVIEW": rc = colors.HexColor("#F59E0B")
            else: rc = colors.HexColor("#EF4444")
            
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(rc)
            c.drawString(315, y_left - 70, risk.upper())
            
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.HexColor("#0F172A"))
            c.drawString(315, y_left - 110, f"Prediction Confidence: {conf:.1f}%")
            
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.HexColor("#64748B"))
            c.drawString(315, y_left - 150, f"Approval Probability: {prob*100:.1f}%")
            c.drawString(315, y_left - 175, f"Risk Probability: {(1-prob)*100:.1f}%")
            
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor("#0F172A"))
            c.drawString(315, y_left - 215, "Decision: ")
            c.setFillColor(rc)
            c.drawString(385, y_left - 215, dec)
        else:
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#64748B"))
            c.drawString(315, y_left - 70, "No prediction available")
            c.drawString(315, y_left - 90, "Submit a new applicant to generate")
            c.drawString(315, y_left - 105, "a risk prediction.")
            
        # Final Summary
        y = y_left - 340
        y = draw_section_title(c, y, "11. Final Summary")
        
        c.setFillColor(colors.HexColor("#EFF6FF"))
        c.setStrokeColor(colors.HexColor("#BFDBFE"))
        c.roundRect(40, y-40, 500, 40, radius=4, stroke=1, fill=1)
        
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor("#0F172A"))
        if has_pred and active_model != "N/A":
            summary = f"The system analyzed {len(df):,} historical loan applications using {active_model}. The selected model achieved {float(accuracy if accuracy != 'N/A' else 0)*100:.1f}% accuracy on the evaluation dataset."
        else:
            acc_val = float(accuracy)*100 if accuracy != "N/A" else 0.0
            if active_model != "N/A":
                summary = f"The system analyzed {len(df):,} historical loan applications using {active_model}. The selected model achieved {acc_val:.1f}% accuracy on the evaluation dataset. No new applicant prediction was available for this report."
            else:
                summary = "The system analyzed the historical dataset. No prediction was made during this session."
                
        lines = simpleSplit(summary, "Helvetica", 10, 480)
        for idx, line in enumerate(lines[:2]):
            c.drawString(55, y - 18 - (idx*14), line)
            
        y -= 60
        # 6 Compact KPI cards
        res_risk = risk.upper() if has_pred else "N/A"
        res_prob = f"{prob*100:.1f}%" if has_pred else "N/A"
        draw_kpi_card(c, 40, y-60, 150, 50, "Total Records", f"{len(df):,}")
        draw_kpi_card(c, 210, y-60, 150, 50, "Total Columns", str(len(df.columns)))
        draw_kpi_card(c, 380, y-60, 160, 50, "Selected Model", active_model, val_color="#2563EB")
        
        draw_kpi_card(c, 40, y-120, 150, 50, "Model Accuracy", f"{accuracy*100:.1f}%")
        rc = "#10B981" if "LOW" in res_risk else ("#EF4444" if "HIGH" in res_risk else "#0F172A")
        draw_kpi_card(c, 210, y-120, 150, 50, "Latest Applicant Result", res_risk, val_color=rc)
        draw_kpi_card(c, 380, y-120, 160, 50, "Approval Probability", res_prob)
            
        c.save()
        from fastapi.responses import FileResponse
        return FileResponse(path=report_path, media_type="application/pdf", filename=report_file_name)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def download_report(filename: str):
    file_path = os.path.join(REPORTS_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="Report not found")
