import pandas as pd
import numpy as np
from typing import Dict, List, Any

# Common synonyms for dynamic column detection
COLUMN_MAPPINGS = {
    "income": ["income", "applicant_income", "salary", "monthly_income", "annual_income", "applicantincome"],
    "coapplicant_income": ["coapplicant_income", "coapplicantincome", "co_income", "spouse_income"],
    "loan_amount": ["loan_amount", "loan", "requested_amount", "amount", "loanamount"],
    "loan_term": ["loan_term", "loan_amount_term", "term", "duration", "loan_term_years", "loanterm"],
    "credit_history": ["credit_history", "credit_score", "credit_rating", "credit", "credithistory", "cibil_score", "cibil", "creditscore"],
    "target": ["loan_status", "approved", "approval", "status", "target"],
    "gender": ["gender", "sex"],
    "married": ["married", "marital_status"],
    "dependents": ["dependents", "children", "num_dependents"],
    "education": ["education", "degree"],
    "self_employed": ["self_employed", "selfemployed", "business_owner"],
    "property_area": ["property_area", "area", "region", "location"]
}

def detect_columns(df: pd.DataFrame) -> Dict[str, str]:
    """
    Tries to map the dataframe columns to standard internal names.
    Returns a dictionary of standard_name -> dataframe_column_name.
    """
    detected_mapping = {}
    df_cols_lower = {col.lower(): col for col in df.columns}
    
    for standard_name, synonyms in COLUMN_MAPPINGS.items():
        for syn in synonyms:
            if syn in df_cols_lower:
                detected_mapping[standard_name] = df_cols_lower[syn]
                break # Found the mapping, move to next standard_name
                
    return detected_mapping

def clean_dataset(df: pd.DataFrame, mapping: Dict[str, str] = None) -> pd.DataFrame:
    """
    Cleans the dataset by handling missing values, duplicates, and invalid types.
    Does NOT modify the original df in place.
    """
    cleaned_df = df.copy()
    
    # Remove complete duplicates
    cleaned_df.drop_duplicates(inplace=True)
    
    # We shouldn't blindly fill NA for everything, but let's do a basic standard fill
    numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
    categorical_cols = cleaned_df.select_dtypes(exclude=[np.number]).columns
    
    # Fill numeric missing values with median
    for col in numeric_cols:
        cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
        
    # Fill categorical missing values with mode
    for col in categorical_cols:
        if not cleaned_df[col].mode().empty:
            cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mode()[0])
        else:
            cleaned_df[col] = cleaned_df[col].fillna("Unknown")
            
    # In a real scenario we'd do more specific cleaning based on the mappings,
    # e.g., mapping "Y"/"N" to 1/0 for target, but we can do that at ML pipeline stage.
    
    return cleaned_df
