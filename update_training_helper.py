import re

with open('backend/ml/training.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the helper robust to already encoded or lowercase variants
old_helper = '''def encode_loan_status(y):
    mapping = {
        "Rejected": 0,
        "Approved": 1
    }
    encoded = y.map(mapping)
    if encoded.isna().any():
        invalid = y[encoded.isna()].unique().tolist()
        raise ValueError(f"Invalid Loan_Status values: {invalid}. Expected 'Approved' or 'Rejected'.")
    
    reverse_mapping = {0: "Rejected", 1: "Approved"}
    return encoded.astype(int), reverse_mapping'''

new_helper = '''def encode_loan_status(y):
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
    return encoded.astype(int), reverse_mapping'''

content = content.replace(old_helper, new_helper)

with open('backend/ml/training.py', 'w', encoding='utf-8') as f:
    f.write(content)
