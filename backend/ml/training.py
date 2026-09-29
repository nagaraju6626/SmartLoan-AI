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

def train_model(dataset_path: str, target_col: str, model_type: str):
    df = pd.read_csv(dataset_path)
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")
        
    # Drop rows where target is missing
    df = df.dropna(subset=[target_col])
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # If target is categorical strings, encode to 0/1
    # Very basic encoding for binary classification
    target_mapping = None
    if y.dtype == 'object' or y.dtype.name == 'category':
        classes = y.unique()
        if len(classes) == 2:
            # Try to infer positive class
            pos_class = classes[0]
            for c in classes:
                if str(c).lower() in ['y', 'yes', 'approved', '1', 'true']:
                    pos_class = c
                    break
            y = (y == pos_class).astype(int)
            target_mapping = {int(1): str(pos_class), int(0): str([c for c in classes if c != pos_class][0])}
        else:
            raise ValueError("Only binary classification is currently supported.")
            
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Prevent Data Leakage: Split first
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
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
    
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "confusion_matrix": cm,
        "training_time_sec": train_time
    }
    
    version = f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"
    model_path = os.path.join(MODELS_DIR, f"model_{version}.pkl")
    
    joblib.dump(pipeline, model_path)
    
    metadata = {
        "version": version,
        "algorithm": model_type,
        "dataset_path": dataset_path,
        "training_date": datetime.now().isoformat(),
        "features": numeric_features + categorical_features,
        "target": target_col,
        "target_mapping": target_mapping,
        "metrics": metrics,
        "status": "Active" # Can be updated later
    }
    
    with open(os.path.join(META_DIR, f"{version}.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
    return metadata
