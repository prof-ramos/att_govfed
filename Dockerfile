# syntax=docker/dockerfile:1.6

# Etapa de build usa python:3.12-slim em vez de Alpine porque pandas/openpyxl
# possuem wheels otimizados para glibc, evitando toolchains pesados e builds lentos.
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Dependências temporárias apenas para compilação/instalação de wheels.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

# Instala dependências em um venv dedicado para ser reaproveitado no runtime.
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ------------------------

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DATA_ROOT=/var/lib/autorizacoes \
    APP_HOME=/app

# Ferramentas mínimas necessárias em produção (curl para healthcheck HTTP).
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copia o ambiente virtual isolado da etapa de build.
COPY --from=builder /opt/venv /opt/venv

WORKDIR $APP_HOME

# Copia código-fonte e artefatos necessários.
COPY . ./

# Cria usuário não-root e diretórios de dados com as permissões corretas.
RUN useradd --create-home --home-dir /home/appuser appuser \
    && mkdir -p "$DATA_ROOT/raw" "$DATA_ROOT/processed" \
    && chown -R appuser:appuser "$APP_HOME" "$DATA_ROOT"

# Volumes permitem persistir os dados processados fora do contêiner.
VOLUME ["/var/lib/autorizacoes/raw", "/var/lib/autorizacoes/processed"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://127.0.0.1:8000/health || exit 1

USER appuser

# Uvicorn expõe a aplicação FastAPI seguindo o padrão 12-factor.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
