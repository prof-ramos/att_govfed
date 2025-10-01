# Fase 1 — Análise Integral da Codebase

## 1. Estrutura do Projeto
- `app/`: aplicação FastAPI (`main.py`) e pipeline de processamento compartilhado (`processing.py`).
- `scripts/`: utilitário CLI `process_data.py` que reutiliza `app.processing`.
- `data/`: diretórios `raw/` e `processed/` usados como armazenamento padrão (vazios por padrão).
- `docs/`: documentação complementar, incluindo dicionário de dados e este relatório.
- `requirements.txt`: dependências Python pinadas.
- `.github/workflows/`: automações do GitHub Actions.
- `.venv/` e `__pycache__/`: artefatos locais (ignorados em produção/container).

## 2. Linguagem, Framework e Dependências-Chave
- Linguagem principal: Python 3.12+.
- Framework web: FastAPI (com Uvicorn como ASGI server).
- Bibliotecas de dados: pandas, openpyxl, xlrd (suporte a Excel), numpy.
- Outras libs: pydantic, starlette, typing-extensions, etc. conforme `requirements.txt`.

## 3. Arquivos de Configuração Detectados
- `requirements.txt`: lista completa de dependências Python.
- `.gitignore`: exclusões padrão + diretórios do Gemini.
- GitHub Actions (`.github/workflows/*.yml`).
- Não há `pyproject.toml`, `package.json` ou configs de servidores web externos.

## 4. Variáveis de Ambiente
- Código atualizado para honrar `DATA_ROOT` (opcional) que define diretório base para dados.
- Nenhuma variável obrigatória adicional detectada.

## 5. Portas de Rede
- Serviço FastAPI executa via Uvicorn na porta padrão `8000` (definiremos explicitamente no contêiner).

## 6. Bancos de Dados e Serviços Externos
- Persistência local em SQLite (`autorizacoes.db`) e CSV dentro de `data/processed/`.
- Sem dependências externas (Redis, filas, serviços de terceiros) nesta etapa.

## 7. Scripts de Build e Inicialização
- `scripts/process_data.py`: executa pipeline para geração de banco/CSV.
- API exposta via `uvicorn app.main:app --reload` (documentado no README).
- GitHub Actions se concentram em automações Gemini; nenhum build adicional detectado.

## 8. Arquivos de Configuração Específicos
- Não há configs de NGINX, Apache ou proxies reversos.
- Sem Dockerfile prévio ou manifestos de infraestrutura antes deste trabalho.

## Decisões Resultantes
- Definir `DATA_ROOT` como variável padrão no contêiner para permitir volumes dedicados.
- Incluir endpoint `/health` para health check de contêiner.
- Planejar imagem baseada em Python slim para compatibilidade com bibliotecas científicas (documentado no Dockerfile).
