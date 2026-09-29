# Smart Loan Risk & Approval System

A Machine Learning and Explainable AI platform that allows users to upload loan datasets, analyze applicant information, train and compare multiple machine learning models, predict loan risk for new applicants, and understand the factors behind each prediction using SHAP. The platform provides interactive analytics, real-time prediction through FastAPI, model versioning, database connectivity, and automated PDF/Excel reports.

## Architecture

*   **Frontend**: Streamlit
*   **Backend**: FastAPI
*   **Data Processing**: Pandas, NumPy
*   **Machine Learning**: Scikit-Learn, XGBoost
*   **Explainable AI**: SHAP
*   **Reports**: ReportLab, OpenPyXL
*   **Database**: SQLAlchemy

## Setup Instructions

1.  **Clone or set up the project**
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Environment Variables**:
    Create a `.env` file based on `.env.example`.

## Running the Application

1.  **Start the Backend (FastAPI)**:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The backend will run on `http://localhost:8000`. API docs available at `http://localhost:8000/docs`.

2.  **Start the Frontend (Streamlit)**:
    Open a new terminal, activate venv, and run:
    ```bash
    streamlit run frontend/app.py
    ```
    The frontend will open in your browser (usually `http://localhost:8501`).

## Machine Learning Pipeline & Data Leakage Prevention
*   The system uses Scikit-learn's `Pipeline` and `ColumnTransformer`.
*   Data is strictly split into train and test sets *before* any imputation or scaling occurs.
*   The target column is excluded from the input features to prevent leakage.

## SHAP Explainability
*   The system uses TreeExplainer for Tree-based models (Random Forest, XGBoost) and LinearExplainer for Logistic Regression.
*   It generates waterfall and bar charts to illustrate local feature importance for individual predictions.

## Security
*   SQL injection prevention is handled via SQLAlchemy text execution and blocking destructive keywords (`INSERT`, `DROP`, etc.).
*   Passwords are not logged or stored.
