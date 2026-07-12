# ==================================
# Base image Python
# ==================================

FROM python:3.11-slim

# ==================================
# Librairie système nécessaire LightGBM
# ==================================


RUN apt-get update \
    && apt-get install -y libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# ==================================
# Variables Python
# ==================================

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# ==================================
# Installation de uv
# ==================================

RUN pip install uv


# ==================================
# Dossier de travail
# ==================================

WORKDIR /app


# ==================================
# Installation dépendances
# ==================================

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev


# ==================================
# Copie du projet
# ==================================

COPY app ./app
COPY src ./src
COPY artifacts ./artifacts


# ==================================
# Port API
# ==================================

EXPOSE 8000


# ==================================
# Lancement FastAPI
# ==================================

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
