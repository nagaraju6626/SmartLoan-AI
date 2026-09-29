from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import json
import joblib
import os
from typing import Dict, Any

from backend.explainability.shap_engine import generate_shap_explanation

router = APIRouter(prefix="/api/predict", tags=["predictions"])

MODELS_DIR = "models/versions"
META_DIR = "models/metadata"

class PredictionRequest(BaseModel):
    version: str
    features: Dict[str, Any]

@router.post("/")
async def predict(req: PredictionRequest):
    model_path = os.path.join(MODELS_DIR, f"model_{req.version}.pkl")
    meta_path = os.path.join(META_DIR, f"{req.version}.json")
    
    if not os.path.exists(model_path) or not os.path.exists(meta_path):
        raise HTTPException(status_code=404, detail="Model version not found.")
        
    with open(meta_path, "r") as f:
        meta = json.load(f)
        
    pipeline = joblib.load(model_path)
    
    # Create DataFrame from features
    input_df = pd.DataFrame([req.features])
    
    # Check if all required features are present
    required_features = meta["features"]
    missing = [f for f in required_features if f not in input_df.columns]
    if missing:
        # Fill missing with None/NaN so preprocessor can handle them if imputer is present
        for f in missing:
            input_df[f] = None
            
    # Keep only required features
    input_df = input_df[required_features]
    
    try:
        prediction = pipeline.predict(input_df)[0]
        
        if hasattr(pipeline, "predict_proba"):
            probability = float(pipeline.predict_proba(input_df)[0][1]) # Prob of positive class
        else:
            probability = 1.0 if prediction == 1 else 0.0
            
        target_mapping = meta.get("target_mapping")
        pred_label = target_mapping[str(prediction)] if target_mapping and str(prediction) in target_mapping else str(prediction)
        
        # Risk classification
        if probability >= 0.75:
            risk_level = "Low Risk"
        elif probability >= 0.50:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"
            
        return {
            "prediction_raw": int(prediction),
            "prediction_label": pred_label,
            "probability": probability,
            "risk_level": risk_level,
            "model_version": req.version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain")
async def explain_prediction(req: PredictionRequest):
    try:
        input_df = pd.DataFrame([req.features])
        meta_path = os.path.join(META_DIR, f"{req.version}.json")
        with open(meta_path, "r") as f:
            meta = json.load(f)
            
        required_features = meta["features"]
        for f in required_features:
            if f not in input_df.columns:
                input_df[f] = None
        input_df = input_df[required_features]
        
        explanation = generate_shap_explanation(req.version, input_df)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/features/{version}")
async def get_model_features(version: str):
    meta_path = os.path.join(META_DIR, f"{version}.json")
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=404, detail="Model metadata not found.")
    
    with open(meta_path, "r") as f:
        meta = json.load(f)
        
    return {"features": meta["features"]}
