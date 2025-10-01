from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import sqlite3
import pandas as pd
from app.processing import process_data

app = FastAPI()

@app.post("/process")
async def trigger_processing(background_tasks: BackgroundTasks):
    """
    Triggers the data processing background task.
    """
    background_tasks.add_task(process_data)
    return {"message": "Data processing started in the background."}

@app.get("/data")
async def get_data(skip: int = 0, limit: int = 100):
    """
    Retrieves data from the database with pagination.
    """
    db_file = 'data/processed/autorizacoes.db'
    try:
        conn = sqlite3.connect(db_file)
        df = pd.read_sql_query(f"SELECT * FROM autorizacoes LIMIT {limit} OFFSET {skip}", conn)
        conn.close()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@app.get("/download")
async def download_csv():
    """
    Downloads the processed data as a CSV file.
    """
    csv_file = 'data/processed/autorizacoes.csv'
    return FileResponse(path=csv_file, filename=csv_file, media_type='text/csv')
