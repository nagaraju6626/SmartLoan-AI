from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from backend.ml.preprocessing import detect_columns

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
PROCESSED_DIR = "data/processed"
UPLOAD_DIR = "data/uploads"

@router.get("/{dataset_id}/dashboard")
async def get_dashboard_data(dataset_id: str):
    # Try to load cleaned data, if not exist, load raw
    file_path = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
    if not os.path.exists(file_path):
        # Look for raw
        raw_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(dataset_id)]
        if not raw_files:
            raise HTTPException(status_code=404, detail="Dataset not found. Please upload and clean first.")
        file_path = os.path.join(UPLOAD_DIR, raw_files[0])
        
    df = pd.read_csv(file_path)
    mapping = detect_columns(df)
    
    kpis = {
        "Total Applicants": len(df),
    }
    
    charts = {}
    
    if "target" in mapping:
        target_col = mapping["target"]
        val_counts = df[target_col].value_counts().to_dict()
        kpis["Approved Applications"] = int(val_counts.get('Y', val_counts.get(1, val_counts.get('Approved', list(val_counts.values())[0] if val_counts else 0))))
        kpis["Rejected Applications"] = int(val_counts.get('N', val_counts.get(0, val_counts.get('Rejected', 0))))
        if kpis["Total Applicants"] > 0:
            kpis["Approval Rate"] = f"{(kpis['Approved Applications'] / kpis['Total Applicants']) * 100:.1f}%"
            
        charts["loan_status_dist"] = {
            "x": list(val_counts.keys()),
            "y": list(val_counts.values()),
            "type": "bar",
            "title": "Loan Status Distribution"
        }
            
    if "loan_amount" in mapping:
        amount_col = mapping["loan_amount"]
        # Convert to numeric if not already, coercing errors
        df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')
        kpis["Average Loan Amount"] = float(df[amount_col].mean())
        
        # We can send bin data for histogram
        hist, bin_edges = pd.cut(df[amount_col].dropna(), bins=10, retbins=True)
        charts["loan_amount_dist"] = {
            "x": [str(interval) for interval in hist.value_counts().sort_index().index],
            "y": hist.value_counts().sort_index().tolist(),
            "type": "bar",
            "title": "Loan Amount Distribution"
        }
        
    if "income" in mapping:
        income_col = mapping["income"]
        df[income_col] = pd.to_numeric(df[income_col], errors='coerce')
        kpis["Average Income"] = float(df[income_col].mean())
        
        if "loan_amount" in mapping:
            # Scatter plot data
            scatter_df = df.dropna(subset=[income_col, mapping["loan_amount"]]).sample(min(1000, len(df)))
            charts["income_vs_amount"] = {
                "x": scatter_df[income_col].tolist(),
                "y": scatter_df[mapping["loan_amount"]].tolist(),
                "type": "scatter",
                "title": "Applicant Income vs Loan Amount"
            }

    if "credit_history" in mapping:
        credit_col = mapping["credit_history"]
        df[credit_col] = pd.to_numeric(df[credit_col], errors='coerce')
        kpis["Average Credit Score"] = float(df[credit_col].mean())

    if "education" in mapping and "target" in mapping:
        edu_col = mapping["education"]
        target_col = mapping["target"]
        grouped = df.groupby(edu_col)[target_col].value_counts().unstack().fillna(0)
        charts["approval_by_education"] = {
            "x": grouped.index.tolist(),
            "y_approved": grouped.get('Y', grouped.get(1, [])).tolist() if 'Y' in grouped.columns or 1 in grouped.columns else [],
            "y_rejected": grouped.get('N', grouped.get(0, [])).tolist() if 'N' in grouped.columns or 0 in grouped.columns else [],
            "type": "grouped_bar",
            "title": "Approval by Education"
        }
        
    return {
        "kpis": kpis,
        "charts": charts
    }
