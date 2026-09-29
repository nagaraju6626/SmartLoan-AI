from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import os
import shutil
from typing import List
from uuid import uuid4
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["data"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DatasetInfo(BaseModel):
    id: str
    filename: str
    rows: int
    columns: int
    size_bytes: int

@router.post("/upload", response_model=DatasetInfo)
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    
    dataset_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{dataset_id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Validate CSV and get metadata
        df = pd.read_csv(file_path)
        
        return DatasetInfo(
            id=dataset_id,
            filename=file.filename,
            rows=len(df),
            columns=len(df.columns),
            size_bytes=os.path.getsize(file_path)
        )
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process dataset: {str(e)}")

@router.get("/datasets", response_model=List[DatasetInfo])
async def list_datasets():
    datasets = []
    for f in os.listdir(UPLOAD_DIR):
        if f.endswith(".csv"):
            file_path = os.path.join(UPLOAD_DIR, f)
            try:
                # We can cache this in a real DB, but for now we read it
                df = pd.read_csv(file_path, nrows=0) # Just to get columns
                # get accurate row count (could be slow for huge files, but okay for this app)
                # Actually, reading just for metadata might be slow if many files. 
                # Let's just return basic info
                dataset_id = f.split("_", 1)[0]
                filename = f.split("_", 1)[1] if "_" in f else f
                datasets.append(DatasetInfo(
                    id=dataset_id,
                    filename=filename,
                    rows=sum(1 for _ in open(file_path)) - 1, # fast line count
                    columns=len(df.columns),
                    size_bytes=os.path.getsize(file_path)
                ))
            except Exception:
                pass
    return datasets

@router.get("/datasets/{dataset_id}")
async def get_dataset_preview(dataset_id: str, rows: int = 10):
    for f in os.listdir(UPLOAD_DIR):
        if f.startswith(dataset_id):
            file_path = os.path.join(UPLOAD_DIR, f)
            try:
                import math
                import numpy as np
                df = pd.read_csv(file_path, nrows=rows)
                records = df.to_dict(orient="records")
                # Safely convert all NaNs/Infs and numpy types to native Python types
                for row in records:
                    for k, v in row.items():
                        if pd.isna(v):
                            row[k] = None
                        elif isinstance(v, (np.integer, int)):
                            row[k] = int(v)
                        elif isinstance(v, (np.floating, float)):
                            if math.isnan(v) or math.isinf(v):
                                row[k] = None
                            else:
                                row[k] = float(v)
                        elif isinstance(v, (np.bool_, bool)):
                            row[k] = bool(v)
                return records
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail="Dataset not found")

from backend.ml.preprocessing import detect_columns, clean_dataset

@router.get("/analysis/{dataset_id}")
async def get_analysis(dataset_id: str):
    file_path = None
    for f in os.listdir(UPLOAD_DIR):
        if f.startswith(dataset_id):
            file_path = os.path.join(UPLOAD_DIR, f)
            break
            
    if not file_path:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    df = pd.read_csv(file_path)
    
    analysis = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "columns": df.columns.tolist(),
        "detected_mapping": detect_columns(df)
    }
    return analysis

@router.post("/clean/{dataset_id}")
async def clean_data(dataset_id: str):
    file_path = None
    for f in os.listdir(UPLOAD_DIR):
        if f.startswith(dataset_id):
            file_path = os.path.join(UPLOAD_DIR, f)
            break
            
    if not file_path:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    df = pd.read_csv(file_path)
    cleaned_df = clean_dataset(df)
    
    PROCESSED_DIR = "data/processed"
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    cleaned_path = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
    cleaned_df.to_csv(cleaned_path, index=False)
    
    return {"message": "Data cleaned successfully", "cleaned_rows": len(cleaned_df)}
