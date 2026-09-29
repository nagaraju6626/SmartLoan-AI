import pytest
import pandas as pd
import os
from backend.ml.preprocessing import detect_columns, clean_dataset
from backend.ml.training import train_model

def test_dynamic_column_detection():
    # Test dataset 1: Standard naming
    df1 = pd.DataFrame(columns=["ApplicantIncome", "LoanAmount", "Credit_History", "Loan_Status"])
    mapping1 = detect_columns(df1)
    
    assert mapping1["income"] == "ApplicantIncome"
    assert mapping1["loan_amount"] == "LoanAmount"
    assert mapping1["target"] == "Loan_Status"
    
    # Test dataset 2: Alternative naming
    df2 = pd.DataFrame(columns=["monthly_income", "requested_amount", "approved"])
    mapping2 = detect_columns(df2)
    
    assert mapping2["income"] == "monthly_income"
    assert mapping2["loan_amount"] == "requested_amount"
    assert mapping2["target"] == "approved"

def test_data_cleaning():
    df = pd.DataFrame({
        "income": [5000, None, 4000, 5000],
        "gender": ["Male", "Female", None, "Male"]
    })
    
    cleaned = clean_dataset(df)
    
    # Should fill numeric with median (4500)
    assert cleaned["income"].isnull().sum() == 0
    assert cleaned.loc[1, "income"] == 4500
    
    # Should drop complete duplicates
    assert len(cleaned) == 3 # Last row is duplicate of first
    
def test_model_training_pipeline():
    # Create dummy dataset
    test_file = "test_train_data.csv"
    df = pd.DataFrame({
        "income": [5000, 4000, 6000, 2000, 8000, 1000, 7000, 3000, 5500, 4500],
        "loan_amount": [150, 100, 200, 50, 300, 20, 250, 80, 180, 120],
        "status": ["Y", "Y", "Y", "N", "Y", "N", "Y", "N", "Y", "Y"]
    })
    df.to_csv(test_file, index=False)
    
    try:
        # Train Logistic Regression
        meta = train_model(test_file, "status", "logistic_regression")
        
        assert meta["algorithm"] == "logistic_regression"
        assert "accuracy" in meta["metrics"]
        assert meta["target"] == "status"
        assert len(meta["features"]) == 2
        
        # Train Random Forest
        meta_rf = train_model(test_file, "status", "random_forest")
        assert meta_rf["algorithm"] == "random_forest"
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
