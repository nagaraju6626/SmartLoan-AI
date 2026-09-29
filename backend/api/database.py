from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/api/database", tags=["database"])

class DBConnectRequest(BaseModel):
    db_type: str
    host: str
    port: int
    database: str
    username: str
    password: str

@router.post("/connect")
async def test_connection(req: DBConnectRequest):
    try:
        if req.db_type.lower() == 'mysql':
            url = f"mysql+mysqlconnector://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
        elif req.db_type.lower() == 'postgresql':
            url = f"postgresql+psycopg2://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
        else:
            raise HTTPException(status_code=400, detail="Unsupported database type")
            
        engine = create_engine(url)
        with engine.connect() as connection:
            pass # just checking if it connects
            
        return {"status": "success", "message": "Successfully connected to the database."}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Database connection failed: {str(e)}")

class DBQueryRequest(BaseModel):
    db_type: str
    host: str
    port: int
    database: str
    username: str
    password: str
    query: str

@router.post("/query")
async def execute_query(req: DBQueryRequest):
    # SQL SAFETY Check
    dangerous_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "create", "grant", "revoke"]
    query_lower = req.query.lower()
    
    for kw in dangerous_keywords:
        if kw in query_lower.split():
            raise HTTPException(status_code=403, detail=f"Query blocked: {kw.upper()} operations are not allowed.")
            
    try:
        if req.db_type.lower() == 'mysql':
            url = f"mysql+mysqlconnector://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
        elif req.db_type.lower() == 'postgresql':
            url = f"postgresql+psycopg2://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
        else:
            raise HTTPException(status_code=400, detail="Unsupported database type")
            
        engine = create_engine(url)
        with engine.connect() as connection:
            result = connection.execute(text(req.query))
            keys = result.keys()
            data = [dict(zip(keys, row)) for row in result.fetchmany(100)] # Limit to 100
            
        return {"columns": list(keys), "data": data}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {str(e)}")

@router.post("/tables")
async def list_tables(req: DBConnectRequest):
    try:
        if req.db_type.lower() == 'mysql':
            url = f"mysql+mysqlconnector://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
        elif req.db_type.lower() == 'postgresql':
            url = f"postgresql+psycopg2://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
        else:
            raise HTTPException(status_code=400, detail="Unsupported database type")
            
        engine = create_engine(url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {"tables": tables}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch tables: {str(e)}")
