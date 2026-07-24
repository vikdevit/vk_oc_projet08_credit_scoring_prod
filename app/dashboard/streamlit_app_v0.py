import pandas as pd
import streamlit as st
import plotly.express as px

from app.dashboard.queries import (
    load_predictions,
    load_api_logs,
    load_system_health_logs,
    load_table
)


st.set_page_config(
    page_title="Credit Scoring Monitoring",
    layout="wide"
)


st.title("📊 Credit Scoring - Monitoring Production")


st.write(
    "Dashboard de supervision du modèle de scoring en production"
)


# ==========================
# Chargement données
# ==========================

drift = load_table("drift_monitoring")
reference_stats = load_table("reference_stats")

predictions = load_predictions()
api_logs = load_api_logs()
health_logs = load_system_health_logs()


# ==========================
# Conversion dates
# ==========================

drift["created_at"] = pd.to_datetime(
    drift["created_at"]
)

predictions["created_at"] = pd.to_datetime(
    predictions["created_at"]
)

api_logs["created_at"] = pd.to_datetime(
    api_logs["created_at"]
)

health_logs["created_at"] = pd.to_datetime(
    health_logs["created_at"]
)


# ==========================
# Sélection campagne drift
# ==========================

drift_dates = (
    drift["created_at"]
    .sort_values(ascending=False)
    .unique()
)


selected_date = st.selectbox(
    "Sélectionner une analyse drift",
    drift_dates
)


selected_datetime = pd.to_datetime(
    selected_date
)


selected_day = selected_datetime.date()


# ==========================
# Filtrage campagne sélectionnée
# ==========================

drift_selected = drift[
    drift["created_at"] == selected_datetime
].copy()


predictions_selected = predictions[
    predictions["created_at"].dt.date == selected_day
].copy()


api_logs_selected = api_logs[
    api_logs["created_at"].dt.date == selected_day
].copy()


health_logs_selected = health_logs[
    health_logs["created_at"].dt.date == selected_day
].copy()


# ==========================
# Contrôle affichage
# ==========================

st.info(
    f"""
Campagne sélectionnée :
{selected_day}

Features drift :
{len(drift_selected)}

Prédictions :
{len(predictions_selected)}
"""
)


st.subheader("Connexion Neon OK")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Features surveillées",
        len(drift_selected)
    )


with col2:
    st.metric(
        "Prédictions",
        len(predictions_selected)
    )


with col3:
    st.metric(
        "Requêtes API",
        len(api_logs_selected)
    )


with col4:
    st.metric(
        "Logs système",
        len(health_logs_selected)
    )

st.divider()

st.header("📉 Data Drift Monitoring")


st.write(
    """
    Analyse de dérive des variables d'entrée du modèle.

    Les indicateurs utilisés :
    - PSI (Population Stability Index)
    - KS (Kolmogorov-Smirnov)

    Référence : données historiques d'entraînement.
    Production : données reçues par l'API.
    """
)


# Tri des variables les plus dérivées

drift_display = (
    drift
    .sort_values(
        "psi",
        ascending=False
    )
)


st.subheader("Top variables avec dérive")


st.dataframe(
    drift_display.head(20),
    use_container_width=True
)

st.subheader(
    "Détail complet du monitoring drift"
)


st.dataframe(
    drift,
    use_container_width=True
)

st.subheader(
    "Top variables selon PSI"
)


top_psi = (
    drift
    .sort_values(
        "psi",
        ascending=False
    )
    .head(15)
)


fig_psi = px.bar(
    top_psi,
    x="psi",
    y="feature_name",
    orientation="h",
    title="Variables avec plus forte dérive PSI"
)


fig_psi.update_layout(
    yaxis_title="Feature",
    xaxis_title="PSI"
)


st.plotly_chart(
    fig_psi,
    use_container_width=True
)

st.subheader(
    "Top variables selon KS"
)


top_ks = (
    drift
    .sort_values(
        "ks",
        ascending=False
    )
    .head(15)
)


fig_ks = px.bar(
    top_ks,
    x="ks",
    y="feature_name",
    orientation="h",
    title="Variables avec plus forte divergence KS"
)


fig_ks.update_layout(
    yaxis_title="Feature",
    xaxis_title="KS"
)


st.plotly_chart(
    fig_ks,
    use_container_width=True
)



col1, col2, col3 = st.columns(3)


with col1:

    important = (
        drift["status"]
        ==
        "Drift important"
    ).sum()

    st.metric(
        "Drift important",
        important
    )


with col2:

    moderate = (
        drift["status"]
        ==
        "Drift modéré"
    ).sum()

    st.metric(
        "Drift modéré",
        moderate
    )


with col3:

    stable = (
        drift["status"]
        ==
        "Stable"
    ).sum()

    st.metric(
        "Stable",
        stable
    )

st.subheader("Référence utilisée pour le calcul du drift")


st.info(
    f"""
    Dataset de référence :
    - Nombre de variables : {reference_stats.shape[0]}
    - Taille historique : {reference_stats['sample_size'].iloc[0]} observations
    - Source : statistiques calculées sur les données d'entraînement
    """
)


st.divider()

st.header("🤖 Prediction Monitoring")


st.write(
    """
    Analyse des sorties du modèle en production.
    
    Les métriques suivies :
    - volume de prédictions
    - proportion de clients classés positifs
    - distribution des scores
    - seuil de décision utilisé
    """
)


# Statistiques prédictions

# ==========================
# Prediction Monitoring campagne sélectionnée
# ==========================

prediction_rate = (
    predictions_selected["prediction"]
    .mean()
)


score_mean = (
    predictions_selected["score"]
    .mean()
)


score_min = (
    predictions_selected["score"]
    .min()
)


score_max = (
    predictions_selected["score"]
    .max()
)

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Nombre prédictions",
        len(predictions_selected)
    )


with col2:
    st.metric(
        "Taux positif",
        f"{prediction_rate:.2%}"
    )


with col3:
    st.metric(
        "Score moyen",
        f"{score_mean:.3f}"
    )


with col4:
    st.metric(
        "Score max",
        f"{score_max:.3f}"
    )

st.subheader("Distribution des scores")


threshold = predictions_selected["threshold"].iloc[0]


fig = px.histogram(
    predictions_selected,
    x="score",
    nbins=20,
    title="Distribution des probabilités prédites de risque (classe 1)"
)


fig.add_vline(
    x=threshold,
    line_dash="dash",
    annotation_text=f"Seuil décision : {threshold:.3f}",
    annotation_position="top"
)


fig.update_layout(
    xaxis_title="Probabilité prédite classe 1",
    yaxis_title="Nombre de prédictions"
)


st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.header("⚡ API Monitoring")


st.write(
    """
    Surveillance opérationnelle de l'API de scoring.

    Indicateurs suivis :
    - volume des requêtes
    - taux d'erreur HTTP
    - latence moyenne
    - latence P95
    - évolution temporelle des temps de réponse
    """
)

total_requests = len(api_logs_selected)


error_rate = (
    api_logs_selected["status_code"]
    .ne(200)
    .mean()
)


mean_latency = (
    api_logs_selected["response_time"]
    .mean()
)


median_latency = (
    api_logs_selected["response_time"]
    .median()
)


p95_latency = (
    api_logs_selected["response_time"]
    .quantile(0.95)
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Requêtes API",
        total_requests
    )


with col2:

    st.metric(
        "Taux erreur HTTP",
        f"{error_rate:.2%}"
    )


with col3:

    st.metric(
        "Latence moyenne",
        f"{mean_latency:.0f} ms"
    )


with col4:

    st.metric(
        "Latence P95",
        f"{p95_latency:.0f} ms"
    )

st.subheader(
    "Distribution des temps de réponse"
)


fig_latency = px.histogram(
    api_logs_selected,
    x="response_time",
    nbins=30,
    title="Distribution latence API"
)


fig_latency.update_layout(
    xaxis_title="Temps de réponse (ms)",
    yaxis_title="Nombre de requêtes"
)


st.plotly_chart(
    fig_latency,
    use_container_width=True
)

st.subheader(
    "Evolution de la latence dans le temps"
)


api_time = api_logs_selected.sort_values(
    "created_at"
)


fig_time = px.line(
    api_time,
    x="created_at",
    y="response_time",
    title="Evolution du temps de réponse API"
)


fig_time.update_layout(
    xaxis_title="Temps",
    yaxis_title="Latence (ms)"
)


st.plotly_chart(
    fig_time,
    use_container_width=True
)

st.divider()

st.header("🖥️ System Health Monitoring")


st.write(
    """
    Surveillance des ressources système utilisées par l'API.

    Indicateurs suivis :
    - utilisation CPU
    - utilisation mémoire
    - évolution temporelle
    - détection des pics de charge
    """
)

cpu_mean = (
    health_logs_selected["cpu_usage"]
    .mean()
)


cpu_max = (
    health_logs_selected["cpu_usage"]
    .max()
)


memory_mean = (
    health_logs_selected["memory_usage"]
    .mean()
)


memory_max = (
    health_logs_selected["memory_usage"]
    .max()
)


cpu_p95 = (
    health_logs_selected["cpu_usage"]
    .quantile(0.95)
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "CPU moyen",
        f"{cpu_mean:.1f}%"
    )


with col2:

    st.metric(
        "CPU maximum",
        f"{cpu_max:.1f}%"
    )


with col3:

    st.metric(
        "Mémoire moyenne",
        f"{memory_mean:.1f}%"
    )


with col4:

    st.metric(
        "Mémoire maximum",
        f"{memory_max:.1f}%"
    )

st.subheader(
    "Evolution des ressources système"
)


health_time = (
    health_logs_selected
    .sort_values("created_at")
)


fig_health = px.line(
    health_time,
    x="created_at",
    y=[
        "cpu_usage",
        "memory_usage"
    ],
    title="Evolution CPU et mémoire"
)


fig_health.update_layout(
    xaxis_title="Temps",
    yaxis_title="Utilisation (%)"
)


st.plotly_chart(
    fig_health,
    use_container_width=True
)

cpu_threshold = (
    health_logs_selected["cpu_usage"]
    .quantile(0.95)
)


cpu_peaks = (
    health_logs_selected["cpu_usage"]
    >
    cpu_threshold
).sum()


st.subheader(
    "Détection des pics CPU"
)


st.metric(
    "Nombre de pics CPU",
    cpu_peaks
)

st.subheader(
    "Corrélation ressources - latence"
)


correlation = (
    health_logs_selected[
        [
            "cpu_usage",
            "memory_usage",
            "response_time"
        ]
    ]
    .corr()
)


st.dataframe(
    correlation,
    use_container_width=True
)

st.divider()

st.header("📋 Résumé global du monitoring")

important_drift = (
    drift["status"]
    == "Drift important"
).sum()


moderate_drift = (
    drift["status"]
    == "Drift modéré"
).sum()

positive_rate = (
    predictions_selected["prediction"]
    .mean()
)


mean_score = (
    predictions_selected["score"]
    .mean()
)

api_error_rate = (
    api_logs_selected["status_code"]
    .ne(200)
    .mean()
)


api_p95 = (
    api_logs_selected["response_time"]
    .quantile(0.95)
)

cpu_alert = (
    health_logs_selected["cpu_usage"]
    .max()
)


memory_alert = (
    health_logs_selected["memory_usage"]
    .max()
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Variables en drift important",
        important_drift
    )


with col2:

    st.metric(
        "Drift modéré",
        moderate_drift
    )


with col3:

    st.metric(
        "Taux positif modèle",
        f"{positive_rate:.2%}"
    )


with col4:

    st.metric(
        "Erreur API",
        f"{api_error_rate:.2%}"
    )

if important_drift > 0:

    monitoring_status = "⚠️ Surveillance requise"

elif api_error_rate > 0:

    monitoring_status = "⚠️ Problème API détecté"

elif cpu_alert > 90:

    monitoring_status = "⚠️ Charge système élevée"

else:

    monitoring_status = "✅ Système nominal"


st.subheader(
    "Etat global du système"
)


st.info(
    monitoring_status
)

st.subheader(
    "Points de vigilance"
)


st.markdown(
"""
### Data Drift
- Les variables avec PSI ou KS élevés doivent être analysées.
- Une dérive persistante peut indiquer une évolution de la population cliente.

### Performance modèle
- Surveiller l'évolution du taux de prédictions positives.
- Vérifier la stabilité de la distribution des scores.

### API
- Surveiller la latence P95.
- Identifier les périodes de ralentissement.

### Infrastructure
- Vérifier les pics CPU.
- Surveiller l'évolution de la mémoire.
"""
)


