import pandas as pd
import sqlite3
import os
import re

def normalize_column_names(df):
    # Basic normalization: strip, lower, replace special chars
    def clean_name(name):
        if not isinstance(name, str):
            return name
        name = name.strip().lower()
        # Replace multiple non-alphanumeric chars with a single underscore
        name = re.sub(r'[^a-z0-9_]+', '_', name)
        return name

    df.columns = [clean_name(col) for col in df.columns]

    # More specific mapping to handle variations
    column_mapping = {
        'órgão_entidade': 'orgao_entidade',
        'vínculo': 'vinculo_orgao_entidade',
        'vínculo_órgão_entidade': 'vinculo_orgao_entidade',
        'cargos': 'cargo',
        'cargo': 'cargo',
        'escolaridade': 'escolaridade',
        'esc_': 'escolaridade',
        'vagas': 'vagas',
        'ato_oficial': 'ato_oficial',
        'norma_jurídica': 'ato_oficial',
        'publicação_diário_oficial_da_união_dou': 'ato_oficial',
        'link_da_publicação_no_d_o_u_': 'link_publicacao_dou',
        'link_dou': 'link_publicacao_dou',
        'área_de_atuação_governamental': 'area_atuacao_governamental',
        'setor': 'area_atuacao_governamental',
        'tipo_de_autorização': 'tipo_autorizacao',
        'data_provimento': 'data_provimento',
        'd_o_u': 'data_publicacao_dou',
        'ano_da_publicação': 'ano_publicacao',
        'port_do_concurso': 'portaria_concurso',
        'dou_port_do_concurso_': 'data_publicacao_portaria_concurso',
        'unnamed_12': 'unnamed_12',
        'obs_': 'observacao'
    }
    
    df = df.rename(columns=column_mapping)
    return df

def process_data():
    # Define paths relative to the project root
    raw_data_dir = 'data/raw'
    processed_data_dir = 'data/processed'
    db_file = os.path.join(processed_data_dir, 'autorizacoes.db')
    csv_file = os.path.join(processed_data_dir, 'autorizacoes.csv')

    # Ensure processed data directory exists
    os.makedirs(processed_data_dir, exist_ok=True)
    os.makedirs(raw_data_dir, exist_ok=True)


    all_data = []

    # Loop through all files in the raw data directory
    for filename in os.listdir(raw_data_dir):
        if filename.endswith(('.xlsx', '.xls')):
            excel_path = os.path.join(raw_data_dir, filename)
            print(f"Processing {filename}...")

            # Dynamically find the header row
            header_row = 0
            try:
                for i in range(10):
                    df_peek = pd.read_excel(excel_path, header=i, nrows=1)
                    # A more robust check for header
                    if any('ÓRGÃO' in str(col).upper() for col in df_peek.columns):
                        header_row = i
                        break
            except Exception as e:
                print(f"  Could not automatically find header for {filename}. Skipping. Error: {e}")
                continue
            
            # Read the excel file with the found header
            try:
                df = pd.read_excel(excel_path, header=header_row)
                df = normalize_column_names(df)
                all_data.append(df)
            except Exception as e:
                print(f"  Error reading {filename}: {e}")


    # Combine all dataframes
    if not all_data:
        print("No data to process.")
        return "No data to process."

    combined_df = pd.concat(all_data, ignore_index=True)

    # Clean data
    for col in combined_df.columns:
        if combined_df[col].dtype == 'object':
            try:
                combined_df[col] = combined_df[col].str.strip()
            except:
                pass

    # Map escolaridade
    if 'escolaridade' in combined_df.columns:
        escolaridade_map = {
            'NI': 'Nível Intermediário',
            'NS': 'Nível Superior'
        }
        combined_df['escolaridade'] = combined_df['escolaridade'].replace(escolaridade_map)

    # Remove duplicate columns before saving
    combined_df = combined_df.loc[:,~combined_df.columns.duplicated()]


    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file)

    # Insert the data into the database
    combined_df.to_sql('autorizacoes', conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()

    # Save to CSV
    combined_df.to_csv(csv_file, index=False, encoding='utf-8')

    return f"Banco de dados '{db_file}' e arquivo CSV '{csv_file}' atualizados com sucesso com os dados de todos os arquivos."

if __name__ == '__main__':
    process_data()
