# Credit Scoring Production API MLOPs

## Présentation du projet

Ce projet consiste à mettre en production un modèle de **scoring crédit** permettant d'estimer la probabilité de défaut d'un client et de fournir une décision automatique d'acceptation ou de refus.

L'objectif est d'appliquer une démarche MLOps par transformation d'un modèle de Machine Learning développé en environnement d'analyse en une solution complète de production comprenant :

- une API REST de prédiction avec **FastAPI**
- une validation robuste des données entrantes avec **Pydantic**
- un stockage des prédictions et logs dans l'espace cloud **Neon PostgreSQL**
- un système de monitoring du modèle
- une détection de dérive des données (**Data Drift**) avec **Evidently**
- un dashboard opérationnel avec **Streamlit**
- une chaîne CI/CD automatisée avec **GitHub Actions**
- une conteneurisation Docker
- un déploiement de l'API conteneurisée dans l'espace cloud RENDER

---

# Objectifs métier

L'application permet à un organisme financier de :

- analyser automatiquement une demande de crédit
- estimer le risque de défaut d'un client
- fournir une décision rapide et reproductible
- surveiller la stabilité du modèle après mise en production


Les sorties principales du modèle sont :

- probabilité de défaut
- seuil de décision
- décision finale :

```
0 : crédit accepté
1 : risque élevé / défaut probable
```


---

# Architecture générale

L'architecture du projet suit une approche production ML.


```
Utilisateur
    |
    |
    v

API FastAPI
    |
    |
    +----------------+
    |                |
    v                v

Validation       Modèle ML
Pydantic             |
                     |
                     v

              Prédiction risque


                     |
                     v

              Neon PostgreSQL

                     |
          +----------+-----------+
          |                      |
          v                      v

 Monitoring Drift          Logs API
 Evidently                 Santé système


                     |
                     v

              Dashboard Streamlit

```


---

# Structure du projet


```
credit_scoring_prod/

│
├── app/
│   │
│   ├── main.py
│   │
│   ├── schemas.py
│   │
│   ├── predictor.py
│   │
│   ├── dashboard/
│   │      └── streamlit_app.py
│   │
│   ├── models/
│   │      ├── api_log.py
│   │      └── system_health_log.py
│   │
│   ├── database/
│   │      └── session.py
│   │
│   ├── utils/
│   │      └── feature_validation.py
│   │
│   └── feature_limits.json
│
│
├── data/
│   ├── X_train_ml.parquet
│   ├── sample_request_client_ok.json
│   └── sample_request_client_risk.json
│
│
├── tests/
│   ├── test_health.py
│   ├── test_model.py
│   ├── test_predict.py
│   └── test_pydantic_validation.py
│
│
├── scripts/
│   └── feature_limits.py
│
│
├── reports/
│   └── evidently_drift_report.html
│
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── .github/
    └── workflows/
        └── ci.yml

```


---

# Modèle Machine Learning

Le modèle utilise les données historiques de crédit afin de prédire le risque de défaut.

Les données ont subi :

- nettoyage
- traitement des valeurs manquantes
- encodage des variables catégorielles
- feature engineering
- création de variables métier


Exemples de features créées :

- CREDIT_INCOME_RATIO
- AGE_YEARS
- EMPLOYMENT_YEARS
- INCOME_PER_PERSON
- DAYS_EMPLOYED_ANOM
- variables issues des historiques crédit


Le modèle final utilise :

```
250 features finales
```

Ces features correspondent exactement aux données utilisées en production.


---

# API FastAPI


## Installation


Créer l'environnement :

```bash
uv sync
```


Activer l'environnement :

```bash
source .venv/bin/activate
```


---

## Lancement API


```bash
uv run uvicorn app.main:app --reload
```


API disponible :

```
http://localhost:8000
```


Documentation Swagger :

```
http://localhost:8000/docs
```


---

# Endpoints API


## Health Check


```
GET /health
```


Réponse :

```json
{
  "status":"ok"
}
```


---

## Prediction


```
POST /predict
```


Exemple :

```json
{
 "features":{
    "SK_ID_CURR":100001,
    "CNT_CHILDREN":0,
    "AMT_ANNUITY":24700
 }
}
```


Réponse :

```json
{
 "client_id":100001,
 "probability_default":0.23,
 "threshold":0.5,
 "decision":0
}
```


---

# Validation Pydantic


Avant toute prédiction, les données entrantes sont contrôlées.


La validation vérifie :

- présence des features
- type numérique
- respect des bornes min/max


Les bornes sont calculées automatiquement depuis :

```
X_train_ml.parquet
```


Script de génération :

```bash
PYTHONPATH=. uv run python scripts/feature_limits.py
```


Résultat :

```
feature_limits.json
```


Contient :

```json
{
 "AMT_CREDIT":{
    "min":10000,
    "max":5000000
 }
}
```


---

# Tests automatisés


Les tests couvrent :


## API

- health check
- chargement modèle
- prédiction client accepté
- prédiction client risque
- gestion des features manquantes


## Validation Pydantic

Tests sur les 250 features finales :

- valeur valide entre min et max
- rejet valeur inférieure au minimum
- rejet valeur supérieure au maximum


Commande :

```bash
PYTHONPATH=. uv run pytest tests -v
```


Résultat attendu :

```
8 passed
```


---

# Couverture des tests


Génération du rapport HTML :

```bash
PYTHONPATH=. uv run pytest \
--cov=app \
--cov-report=html
```


Le rapport est disponible :

```
htmlcov/index.html
```


---

# Data Drift Monitoring


Le projet intègre un monitoring du comportement des données de production.


Outil utilisé :

```
Evidently
```


Les métriques suivies :

## PSI

Population Stability Index

Permet d'identifier un changement de distribution entre :

- données historiques
- données production


## KS Test

Kolmogorov-Smirnov

Compare les distributions statistiques.


---

Exemple de features surveillées :

| Feature | PSI | Drift |
|-|-|-|
| MONTHS_BALANCE_count_mean | 1.17 | Drift important |
| MONTHS_BALANCE_min_min | 1.16 | Drift important |
| HAS_LATE_max_max | 0.40 | Drift important |
| FLAG_EMAIL | 0.12 | Drift modéré |


---

# Rapport Evidently


Génération :

```python
report.run(
    reference_data=X_train,
    current_data=production_data
)
```


Export :

```
reports/evidently_drift_report.html
```


---

# Dashboard Streamlit


Le dashboard permet de suivre :

## Data Drift

- PSI
- KS
- features les plus dérivées
- statut drift


## Prediction Monitoring

- nombre de prédictions
- taux positif
- score moyen
- distribution des scores


## API Monitoring

- volume requêtes
- erreurs HTTP
- latence moyenne
- P95 latency


## System Monitoring

- CPU
- mémoire
- évolution temporelle


---

Lancement :

```bash
uv run streamlit run app/dashboard/streamlit_app.py
```


---

# Base de données


La base utilisée est :

```
Neon PostgreSQL
```


Tables principales :


## Predictions

Stockage :

- client
- score
- décision
- timestamp


## API Logs

Stockage :

- endpoint
- status HTTP
- temps réponse


## System Health Logs

Stockage :

- CPU
- mémoire
- latence


---

# Docker


Construction image :

```bash
docker build -t credit-scoring-api .
```


Lancement :

```bash
docker run -p 8000:8000 credit-scoring-api
```


---

# CI/CD GitHub Actions


Le pipeline automatique réalise :


## Job Tests

- installation dépendances
- lancement pytest


## Job Build Test

- construction image Docker


## Job Build Production

- construction image production


## Déploiement

Le déploiement est exécuté uniquement après validation complète :

```
tests
   ↓
docker build test
   ↓
docker build production
   ↓
deploy
```


avec gestion des dépendances :

```yaml
needs:
  - tests
  - docker_build_test
  - docker_build_prod
```


---

# Technologies utilisées


| Domaine | Technologie |
|-|-|
| API | FastAPI |
| Validation | Pydantic V2 |
| ML | Scikit-learn |
| Base | Neon PostgreSQL |
| ORM | SQLAlchemy |
| Monitoring | Evidently |
| Dashboard | Streamlit |
| Tests | Pytest |
| Packaging | uv |
| Conteneurisation | Docker |
| CI/CD | GitHub Actions |


---

# Etat du projet


Fonctionnalités réalisées :

✔ API de prédiction  
✔ Validation des entrées  
✔ Feature engineering intégré  
✔ Stockage PostgreSQL  
✔ Monitoring production  
✔ Data drift monitoring  
✔ Dashboard Streamlit  
✔ Tests automatisés  
✔ Pipeline CI/CD  


---

## Historique du projet

Voir :
docs/commits_history.md

---

# Améliorations possibles


- ajout authentification API
- ajout alertes automatiques drift
- monitoring modèle avec métriques métier
- déploiement Kubernetes
- ajout tracking MLflow


---

# Auteur

 Viken KHATCHERIAN

