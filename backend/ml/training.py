import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import joblib
import os
import json
from datetime import datetime
from uuid import uuid4

MODELS_DIR = "models/versions"
META_DIR = "models/metadata"
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

def encode_loan_status(y):
    mapping = {
        "Rejected": 0,
        "Approved": 1,
        "rejected": 0,
        "approved": 1,
        0: 0,
        1: 1,
        "0": 0,
        "1": 1
    }
    encoded = y.map(mapping)
    if encoded.isna().any():
        invalid = y[encoded.isna()].unique().tolist()
        raise ValueError(f"Invalid Loan_Status values: {invalid}. Expected 'Approved' or 'Rejected'.")
    
    reverse_mapping = {0: "Rejected", 1: "Approved"}
    return encoded.astype(int), reverse_mapping

def train_model(dataset_path: str, target_col: str, model_type: str):
    df = pd.read_csv(dataset_path)
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")
        
    # Drop rows where target is missing
    df = df.dropna(subset=[target_col])
    
    X = df.drop(columns=[target_col])
    
    # Exclude ID columns
    id_cols = [c for c in X.columns if c.lower().endswith('_id') or c.lower() == 'id']
    X = X.drop(columns=id_cols)
    
    y = df[target_col]
    
    # Ensure target is cleanly encoded
    y, target_mapping = encode_loan_status(y)
    
    if y.nunique() < 2:
        raise ValueError("Training requires both Approved and Rejected loan records.")
            
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Prevent Data Leakage: Split first
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
    if model_type == "logistic_regression":
        classifier = LogisticRegression(random_state=42, max_iter=1000)
    elif model_type == "random_forest":
        classifier = RandomForestClassifier(random_state=42)
    elif model_type == "xgboost":
        classifier = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
    else:
        raise ValueError(f"Unknown model type: {model_type}")
        
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])
    
    start_time = datetime.now()
    pipeline.fit(X_train, y_train)
    train_time = (datetime.now() - start_time).total_seconds()
    
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
    
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else y_pred
    
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    try:
        roc_auc = float(roc_auc_score(y_test, y_prob))
    except ValueError:
        roc_auc = "N/A"

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": roc_auc,
        "confusion_matrix": cm,
        "training_time_sec": train_time
    }
    
    version = f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"
    model_path = os.path.join(MODELS_DIR, f"model_{version}.pkl")
    
    joblib.dump(pipeline, model_path)    # Extract feature importance
    feature_importance_list = []
    try:
        classifier_step = pipeline.named_steps['classifier']
        preprocessor_step = pipeline.named_steps['preprocessor']
        
        if hasattr(preprocessor_step, 'get_feature_names_out'):
            feature_names = list(preprocessor_step.get_feature_names_out())
            feature_names = [f.split("__", 1)[-1] if "__" in f else f for f in feature_names]
        else:
            feature_names = numeric_features + categorical_features
            
        importances = None
        if hasattr(classifier_step, 'feature_importances_'):
            importances = classifier_step.feature_importances_
        elif hasattr(classifier_step, 'coef_'):
            importances = np.abs(classifier_step.coef_[0])
            
        if importances is not None and len(importances) == len(feature_names):
            total = np.sum(importances)
            if total > 0:
                importances = importances / total
                
            fi_data = [{"feature": f, "importance": float(i)} for f, i in zip(feature_names, importances)]
            feature_importance_list = sorted(fi_data, key=lambda x: x["importance"], reverse=True)[:10]
    except Exception:
        pass
        

    
    metadata = {
        "version": version,
        "algorithm": model_type,
        "dataset_path": dataset_path,
        "training_date": datetime.now().isoformat(),
        "features": numeric_features + categorical_features,
        "target": target_col,
        "target_mapping": target_mapping,
        "metrics": metrics,
        "feature_importance": feature_importance_list,
        "status": "Active" # Can be updated later
    }
    
    with open(os.path.join(META_DIR, f"{version}.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
    return metadata
