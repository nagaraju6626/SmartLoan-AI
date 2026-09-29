import pytest
from fastapi.testclient import TestClient
import pandas as pd
import os
import shutil

from backend.main import app

client = TestClient(app)

# Helper to create a test dataset
def create_test_csv(filename, columns):
    df = pd.DataFrame([
        {cols: 1 for cols in columns},
        {cols: 0 for cols in columns}
    ])
    df.to_csv(filename, index=False)
    return filename

@pytest.fixture(scope="module")
def setup_data():
    os.makedirs("data/uploads", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    yield
    # Cleanup after tests
    # for f in os.listdir("data/uploads"): os.remove(f"data/uploads/{f}")
    # for f in os.listdir("data/processed"): os.remove(f"data/processed/{f}")

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload_and_clean_data(setup_data):
    # Create mock CSV
    test_file = "test_loan.csv"
    create_test_csv(test_file, ["Loan_ID", "ApplicantIncome", "LoanAmount", "Loan_Status"])
    
    # Test Upload
    with open(test_file, "rb") as f:
        response = client.post("/api/upload", files={"file": ("test_loan.csv", f, "text/csv")})
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    dataset_id = data["id"]
    
    # Test Analysis
    analysis_res = client.get(f"/api/analysis/{dataset_id}")
    assert analysis_res.status_code == 200
    assert "detected_mapping" in analysis_res.json()
    
    # Test Clean
    clean_res = client.post(f"/api/clean/{dataset_id}")
    assert clean_res.status_code == 200
    assert "cleaned_rows" in clean_res.json()
    
    os.remove(test_file)
