from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json
from backend.ml.training import train_model

router = APIRouter(prefix="/api/models", tags=["models"])

class TrainRequest(BaseModel):
    dataset_id: str
    target_column: str
    model_types: list[str] = ["logistic_regression"]

@router.post("/train")
async def train_models(req: TrainRequest):
    PROCESSED_DIR = "data/processed"
    file_path = os.path.join(PROCESSED_DIR, f"{req.dataset_id}_cleaned.csv")
    
    if not os.path.exists(file_path):
        UPLOAD_DIR = "data/uploads"
        raw_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(req.dataset_id)]
        if not raw_files:
            raise HTTPException(status_code=404, detail="Dataset not found")
        file_path = os.path.join(UPLOAD_DIR, raw_files[0])
        
    results = []
    for m_type in req.model_types:
        try:
            meta = train_model(file_path, req.target_column, m_type)
            results.append(meta)
        except Exception as e:
            results.append({"algorithm": m_type, "error": str(e)})
            
    return {"message": "Training completed", "results": results}

@router.get("/")
async def list_models():
    META_DIR = "models/metadata"
    if not os.path.exists(META_DIR):
        return []
        
    models = []
    for f in os.listdir(META_DIR):
        if f.endswith(".json"):
            with open(os.path.join(META_DIR, f), "r") as file:
                models.append(json.load(file))
                
    return sorted(models, key=lambda x: x.get("training_date", ""), reverse=True)
