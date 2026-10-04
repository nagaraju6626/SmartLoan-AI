import re

with open('backend/api/reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update ReportRequest
old_req = '''class ReportRequest(BaseModel):
    dataset_id: str
    format: str = "pdf"
    active_model_version: Optional[str] = None
    prediction_result: Optional[Dict[str, Any]] = None
    prediction_inputs: Optional[Dict[str, Any]] = None'''

new_req = '''class ReportRequest(BaseModel):
    dataset_id: str
    format: str = "pdf"
    active_model_version: Optional[str] = None
    prediction_result: Optional[Dict[str, Any]] = None
    prediction_inputs: Optional[Dict[str, Any]] = None
    csv_data: Optional[str] = None'''

content = content.replace(old_req, new_req)

# 2. Update dataframe loading logic in generate_report
old_load = '''    try:
        file_path = os.path.join(PROCESSED_DATA_DIR, f"{req.dataset_id}_cleaned.csv")
        if not os.path.exists(file_path):
            # Fallback for older versions if they didn't use _cleaned
            file_path = os.path.join(PROCESSED_DATA_DIR, f"{req.dataset_id}.csv")
            
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Processed dataset not found.")
            
        df = pd.read_csv(file_path)'''

new_load = '''    try:
        import io
        if req.csv_data:
            df = pd.read_csv(io.StringIO(req.csv_data))
        else:
            file_path = os.path.join(PROCESSED_DATA_DIR, f"{req.dataset_id}_cleaned.csv")
            if not os.path.exists(file_path):
                # Fallback for older versions if they didn't use _cleaned
                file_path = os.path.join(PROCESSED_DATA_DIR, f"{req.dataset_id}.csv")
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail="Processed dataset not found.")
            df = pd.read_csv(file_path)'''

content = content.replace(old_load, new_load)

# 3. Update the return value
old_return = '''        c.save()
        return {"message": "Report generated", "download_url": f"/api/reports/download/{report_file_name}"}'''

new_return = '''        c.save()
        from fastapi.responses import FileResponse
        return FileResponse(path=report_path, media_type="application/pdf", filename=report_file_name)'''

content = content.replace(old_return, new_return)

with open('backend/api/reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
