# API para Processamento de Dados de Autorizações Governamentais

Este projeto foi desenvolvido para consolidar e normalizar dados sobre autorizações e provimentos governamentais a partir de diversos arquivos Excel. O objetivo é criar um dataset único e limpo, disponível através de uma API, e também nos formatos SQLite e CSV.

## Estrutura de Diretórios

A organização do projeto segue a seguinte estrutura:

```
.
├── app/
│   ├── __init__.py
│   ├── main.py         # Lógica da API FastAPI
│   └── processing.py   # Lógica de processamento dos dados
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── scripts/
├── .gitignore
├── README.md
└── requirements.txt
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

## Como Executar a API

Para iniciar a API, execute o seguinte comando a partir do diretório raiz do projeto:

```sh
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

## Endpoints da API

A API fornece os seguintes endpoints:

*   `POST /process`: Inicia o processamento dos dados em background.
*   `GET /data`: Retorna os dados processados do banco de dados com paginação.
*   `GET /download`: Faz o download dos dados processados em um arquivo CSV.

## Como Usar a API

1.  **Adicione os Dados Brutos:**
    Certifique-se de que todos os arquivos Excel a serem processados estejam na pasta `data/raw/`.

2.  **Inicie o Processamento:**
    Envie uma requisição POST para o endpoint `/process` para iniciar o processamento dos dados.
    ```sh
    curl -X POST http://127.0.0.1:8000/process
    ```

3.  **Consulte os Dados:**
    Após o processamento, você pode consultar os dados via o endpoint `/data`.
    ```sh
    curl http://127.0.0.1:8000/data?skip=0&limit=10
    ```

4.  **Faça o Download dos Dados:**
    Para baixar o dataset completo em CSV, acesse o endpoint `/download` em seu navegador ou use o `curl`:
    ```sh
    curl -o autorizacoes.csv http://127.0.0.1:8000/download
    ```