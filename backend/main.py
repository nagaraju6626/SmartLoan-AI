from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Smart Loan Risk & Approval System API",
    description="Backend API for Loan Risk Assessment platform using Machine Learning and Explainable AI.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # In production, specify the exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

from backend.api import data, analytics, models, predictions, reports, database

# We will include routers from the api package here as we build them
app.include_router(data.router)
app.include_router(analytics.router)
app.include_router(models.router)
app.include_router(predictions.router)
app.include_router(reports.router)
app.include_router(database.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
