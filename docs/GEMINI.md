# Visão Geral do Diretório

Este diretório contém um projeto de processamento de dados focado em autorizações e provimentos governamentais. O fluxo de trabalho principal envolve a extração de dados brutos de arquivos Excel, a normalização desses dados com base em um dicionário de dados e, finalmente, o carregamento dos dados processados em um banco de dados SQLite.

# Arquivos Principais

*   `autorizacoes*.xlsx`, `planilha-*.xlsx`, etc.: Arquivos de dados brutos em formato Excel que servem como entrada para o processo de ETL.
*   `dicionario.md`: Um dicionário de dados que descreve o esquema e o significado das colunas presentes nos arquivos Excel.
*   `process_data.py`: Um script Python que orquestra todo o processo de ETL. Ele lê os arquivos Excel, limpa e normaliza os dados de acordo com as regras definidas no `dicionario.md` e carrega o resultado no banco de dados.
*   `autorizacoes.db`: O banco de dados SQLite final que contém os dados normalizados e processados, prontos para análise.
*   `.venv`: Um ambiente virtual Python que contém as bibliotecas necessárias (`pandas`, `openpyxl`, `uv`) para executar o script de processamento.

# Uso

O fluxo de trabalho principal neste diretório é processar os arquivos Excel brutos em um banco de dados SQLite estruturado.

1.  **Dados Brutos:** Os dados brutos são armazenados em vários arquivos `.xlsx` e `.xls`.
2.  **Dicionário de Dados:** O arquivo `dicionario.md` fornece o esquema e a descrição dos dados.
3.  **Processamento:** O script `process_data.py` é executado para realizar o processo de ETL (Extração, Transformação e Carga).
4.  **Banco de Dados:** O arquivo `autorizacoes.db` resultante é um banco de dados SQLite pronto para uso para análise.
