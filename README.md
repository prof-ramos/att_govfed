# Projeto de Processamento de Dados de Autorizações Governamentais

Este projeto foi desenvolvido para consolidar e normalizar dados sobre autorizações e provimentos governamentais a partir de diversos arquivos Excel. O objetivo é criar um dataset único e limpo, disponível nos formatos SQLite e CSV, para facilitar a análise e consulta.

## Estrutura de Diretórios

A organização do projeto segue a seguinte estrutura:

```
.venv/
├── data/
│   ├── raw/         # Contém os arquivos Excel brutos (.xlsx, .xls)
│   └── processed/   # Contém os dados processados (autorizacoes.db e autorizacoes.csv)
├── docs/
│   └── dicionario.md # Documentação e dicionário de dados
├── scripts/
│   └── process_data.py # Script principal para o processo de ETL
└── requirements.txt    # Lista de dependências Python
```

## Requisitos e Instalação

Para executar este projeto, você precisará do Python 3 instalado.

1.  **Crie um Ambiente Virtual:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Instale as Dependências:**
    As dependências estão listadas no arquivo `requirements.txt` e podem ser instaladas com o seguinte comando:
    ```sh
    pip install -r requirements.txt
    ```

## Como Usar

Para processar os dados, siga os passos abaixo:

1.  **Adicione os Dados Brutos:**
    Certifique-se de que todos os arquivos Excel a serem processados estejam na pasta `data/raw/`.

2.  **Execute o Script de Processamento:**
    A partir do diretório raiz do projeto, execute o script principal:
    ```sh
    python scripts/process_data.py
    ```
    O script irá ler todos os arquivos da pasta `data/raw`, consolidar os dados, normalizar os nomes das colunas, limpar as informações e salvar os resultados.

## Saídas do Processamento

Após a execução bem-sucedida do script, os seguintes arquivos serão gerados na pasta `data/processed/`:

*   `autorizacoes.db`: Um banco de dados SQLite contendo uma tabela chamada `autorizacoes` com todos os dados consolidados.
*   `autorizacoes.csv`: Um arquivo CSV com os mesmos dados consolidados, ideal para importação em outras ferramentas de análise.
