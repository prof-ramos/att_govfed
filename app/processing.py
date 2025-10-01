"""Data processing utilities shared by the API and CLI entry points."""
from __future__ import annotations

import os
import re
import sqlite3
from pathlib import Path
from typing import Dict, List

import pandas as pd

# Configure where raw and processed data will live; defaults match the repo layout.
DATA_ROOT = Path(os.getenv("DATA_ROOT", Path(__file__).resolve().parents[1] / "data")).resolve()
RAW_DIR = DATA_ROOT / "raw"
PROCESSED_DIR = DATA_ROOT / "processed"
DB_FILE = PROCESSED_DIR / "autorizacoes.db"
CSV_FILE = PROCESSED_DIR / "autorizacoes.csv"


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise column names by stripping, lowercasing and mapping aliases."""

    def clean_name(name: str) -> str:
        if not isinstance(name, str):
            return name
        name = name.strip().lower()
        # Replace multiple non-alphanumeric chars with a single underscore
        name = re.sub(r"[^a-z0-9_]+", "_", name)
        return name

    df.columns = [clean_name(col) for col in df.columns]

    column_mapping: Dict[str, str] = {
        "órgão_entidade": "orgao_entidade",
        "vínculo": "vinculo_orgao_entidade",
        "vínculo_órgão_entidade": "vinculo_orgao_entidade",
        "cargos": "cargo",
        "cargo": "cargo",
        "escolaridade": "escolaridade",
        "esc_": "escolaridade",
        "vagas": "vagas",
        "ato_oficial": "ato_oficial",
        "norma_jurídica": "ato_oficial",
        "publicação_diário_oficial_da_união_dou": "ato_oficial",
        "link_da_publicação_no_d_o_u_": "link_publicacao_dou",
        "link_dou": "link_publicacao_dou",
        "área_de_atuação_governamental": "area_atuacao_governamental",
        "setor": "area_atuacao_governamental",
        "tipo_de_autorização": "tipo_autorizacao",
        "data_provimento": "data_provimento",
        "d_o_u": "data_publicacao_dou",
        "ano_da_publicação": "ano_publicacao",
        "port_do_concurso": "portaria_concurso",
        "dou_port_do_concurso_": "data_publicacao_portaria_concurso",
        "unnamed_12": "unnamed_12",
        "obs_": "observacao",
    }

    df = df.rename(columns=column_mapping)
    return df


def _ensure_directories() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def process_data() -> str:
    _ensure_directories()

    all_data: List[pd.DataFrame] = []

    # Loop through all spreadsheet files under the raw directory
    for entry in RAW_DIR.iterdir():
        if entry.suffix.lower() not in {".xlsx", ".xls"}:
            continue

        excel_path = entry.as_posix()
        print(f"Processing {entry.name}...")

        # Dynamically find the header row
        header_row = 0
        try:
            for i in range(10):
                df_peek = pd.read_excel(excel_path, header=i, nrows=1)
                if any("ÓRGÃO" in str(col).upper() for col in df_peek.columns):
                    header_row = i
                    break
        except Exception as exc:
            print(
                f"  Could not automatically find header for {entry.name}. Skipping. Error: {exc}"
            )
            continue

        try:
            df = pd.read_excel(excel_path, header=header_row)
            df = normalize_column_names(df)
            all_data.append(df)
        except Exception as exc:
            print(f"  Error reading {entry.name}: {exc}")

    if not all_data:
        message = "No data to process."
        print(message)
        return message

    combined_df = pd.concat(all_data, ignore_index=True)

    for col in combined_df.columns:
        if combined_df[col].dtype == "object":
            try:
                combined_df[col] = combined_df[col].str.strip()
            except Exception:
                pass

    if "escolaridade" in combined_df.columns:
        escolaridade_map = {
            "NI": "Nível Intermediário",
            "NS": "Nível Superior",
        }
        combined_df["escolaridade"] = combined_df["escolaridade"].replace(escolaridade_map)

    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    conn = sqlite3.connect(DB_FILE.as_posix())
    combined_df.to_sql("autorizacoes", conn, if_exists="replace", index=False)
    conn.close()

    combined_df.to_csv(CSV_FILE.as_posix(), index=False, encoding="utf-8")

    return (
        "Banco de dados '"
        + DB_FILE.as_posix()
        + "' e arquivo CSV '"
        + CSV_FILE.as_posix()
        + "' atualizados com sucesso com os dados de todos os arquivos."
    )


if __name__ == "__main__":
    process_data()
