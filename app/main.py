"""FastAPI service exposing the data processing pipeline."""
from __future__ import annotations

import sqlite3
from typing import List

import pandas as pd
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.processing import CSV_FILE, DB_FILE, process_data

app = FastAPI(title="Autorizações Governamentais API")


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """Lightweight endpoint used by container health checks."""
    return {"status": "ok"}


@app.post("/process")
async def trigger_processing(background_tasks: BackgroundTasks) -> dict[str, str]:
    """Enfileira o processamento em segundo plano para não bloquear requisições."""
    background_tasks.add_task(process_data)
    return {"message": "Processamento iniciado em segundo plano."}


@app.get("/data")
async def get_data(skip: int = 0, limit: int = 100) -> List[dict[str, object]]:
    """Consulta os dados processados com paginação simples."""
    if not DB_FILE.exists():
        raise HTTPException(status_code=404, detail="Banco de dados não encontrado. Execute /process primeiro.")

    conn = sqlite3.connect(DB_FILE.as_posix())
    try:
        df = pd.read_sql_query(
            "SELECT * FROM autorizacoes LIMIT ? OFFSET ?",
            conn,
            params=(limit, skip),
        )
    finally:
        conn.close()

    return df.to_dict(orient="records")


@app.get("/download")
async def download_csv() -> FileResponse:
    """Disponibiliza o dataset consolidado em formato CSV."""
    if not CSV_FILE.exists():
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado. Execute /process primeiro.")

    return FileResponse(path=CSV_FILE.as_posix(), filename=CSV_FILE.name, media_type="text/csv")
