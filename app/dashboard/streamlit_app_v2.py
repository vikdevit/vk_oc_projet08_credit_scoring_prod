import streamlit as st
import pandas as pd
import plotly.express as px

from app.dashboard.queries import (
    load_table,
    load_predictions,
    load_api_logs,
    load_system_health_logs
)

# ==========================================================
# CONFIGURATION STREAMLIT
# ==========================================================

st.set_page_config(
    page_title="Credit Scoring Monitoring",
    layout="wide"
)

st.title("📊 Credit Scoring - Monitoring Production")

st.write(
    "Dashboard de supervision du modèle de scoring en production"
)

# ==========================================================
# CHARGEMENT DES DONNÉES
# ==========================================================

drift = load_table("drift_monitoring")

reference_stats = load_table("reference_stats")

predictions = load_predictions()

api_logs = load_api_logs()

health_logs = load_system_health_logs()

# ==========================================================
# CONVERSION DES DATES
# ==========================================================

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

# ==========================================================
# CAMPAGNES DISPONIBLES
# (uniquement pour Predictions/API/System Health)
# ==========================================================

available_campaigns = sorted(
    predictions["created_at"].dt.date.unique(),
    reverse=True
)

selected_day = st.selectbox(
    "📅 Sélectionner une campagne",
    available_campaigns
)

# ==========================================================
# FILTRAGE PAR DATE
# ==========================================================

predictions_selected = predictions[
    predictions["created_at"].dt.date == selected_day
].copy()

api_logs_selected = api_logs[
    api_logs["created_at"].dt.date == selected_day
].copy()

health_logs_selected = health_logs[
    health_logs["created_at"].dt.date == selected_day
].copy()

# ==========================================================
# LE DRIFT RESTE SUR LES 21 000 OBSERVATIONS
# ==========================================================

drift_selected = drift.copy()

# ==========================================================
# BANDEAU
# ==========================================================

st.info(
    f"""
📅 Campagne sélectionnée : {selected_day}

📉 Variables de drift : {len(drift_selected)}

🤖 Prédictions : {len(predictions_selected)}

⚡ Logs API : {len(api_logs_selected)}

🖥️ Logs système : {len(health_logs_selected)}
"""
)

# ==========================================================
# KPI GLOBAUX
# ==========================================================

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

# ==========================================================
# DATA DRIFT
# ==========================================================

st.header("📉 Data Drift Monitoring")

st.write(
    """
Analyse des variables d'entrée du modèle.

Le monitoring du drift est calculé sur
l'ensemble des 21 000 observations disponibles.
"""
)

drift_display = drift_selected.sort_values(
    "psi",
    ascending=False
)

st.subheader("Top variables")

st.dataframe(
    drift_display.head(20),
    use_container_width=True
)

st.subheader("Table complète")

st.dataframe(
    drift_display,
    use_container_width=True
)

# ==========================================================
# TOP PSI
# ==========================================================

top_psi = (
    drift_selected
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
    title="Top variables selon le PSI"
)

fig_psi.update_layout(
    yaxis_title="Feature",
    xaxis_title="PSI"
)

st.plotly_chart(
    fig_psi,
    use_container_width=True
)

# ==========================================================
# TOP KS
# ==========================================================

top_ks = (
    drift_selected
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
    title="Top variables selon le KS"
)

fig_ks.update_layout(
    yaxis_title="Feature",
    xaxis_title="KS"
)

st.plotly_chart(
    fig_ks,
    use_container_width=True
)

# ==========================================================
# KPI DRIFT
# ==========================================================

important = (
    drift_selected["status"] == "Drift important"
).sum()

moderate = (
    drift_selected["status"] == "Drift modéré"
).sum()

stable = (
    drift_selected["status"] == "Stable"
).sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Drift important",
        important
    )

with col2:
    st.metric(
        "Drift modéré",
        moderate
    )

with col3:
    st.metric(
        "Stable",
        stable
    )

# ==========================================================
# REFERENCE
# ==========================================================

st.subheader("Référence historique")

st.info(
    f"""
Variables historiques : {reference_stats.shape[0]}

Jeu d'entraînement :
{reference_stats['sample_size'].iloc[0]}
observations
"""
)

st.divider()

# ======================================================
# PREDICTION MONITORING
# ======================================================

st.header("🤖 Prediction Monitoring")

st.write(
    """
Analyse des sorties du modèle.

Indicateurs :
- volume de prédictions
- taux positif
- score moyen
- distribution des scores
"""
)

if len(predictions_selected) > 0:

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

    threshold = (
        predictions_selected["threshold"]
        .iloc[0]

    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Nombre de prédictions",
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
            "Score maximum",
            f"{score_max:.3f}"
        )

    # ==========================
    # Distribution des scores
    # ==========================

    fig_score = px.histogram(
        predictions_selected,
        x="score",
        nbins=20,
        title="Distribution des scores du modèle"
    )

    fig_score.add_vline(
        x=threshold,
        line_dash="dash",
        annotation_text=f"Seuil : {threshold:.3f}"
    )

    fig_score.update_layout(
        xaxis_title="Probabilité de défaut",
        yaxis_title="Nombre"
    )

    st.plotly_chart(
        fig_score,
        use_container_width=True
    )

    # ==========================
    # Répartition des classes
    # ==========================

    prediction_counts = (
        predictions_selected["prediction"]
        .value_counts()
        .rename_axis("prediction")
        .reset_index(name="count")
    )

    fig_pred = px.pie(
        prediction_counts,
        names="prediction",
        values="count",
        title="Répartition des prédictions"
    )

    st.plotly_chart(
        fig_pred,
        use_container_width=True
    )

else:

    st.warning(
        "Aucune prédiction disponible pour cette campagne."
    )

st.divider()

# ======================================================
# API MONITORING
# ======================================================

st.header("⚡ API Monitoring")

st.write(
    """
Surveillance opérationnelle de l'API de scoring.

Indicateurs :
- volume des requêtes
- taux d'erreur HTTP
- latence moyenne
- latence P95
"""
)

if len(api_logs_selected) > 0:

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

    # Distribution des temps de réponse

    fig_latency = px.histogram(
        api_logs_selected,
        x="response_time",
        nbins=30,
        title="Distribution des temps de réponse API"
    )

    fig_latency.update_layout(
        xaxis_title="Temps de réponse (ms)",
        yaxis_title="Nombre de requêtes"
    )

    st.plotly_chart(
        fig_latency,
        use_container_width=True
    )

    # Evolution de la latence

    api_time = (
        api_logs_selected
        .sort_values("created_at")
    )

    fig_time = px.line(
        api_time,
        x="created_at",
        y="response_time",
        title="Evolution de la latence API"
    )

    fig_time.update_layout(
        xaxis_title="Temps",
        yaxis_title="Temps de réponse (ms)"
    )

    st.plotly_chart(
        fig_time,
        use_container_width=True
    )

else:

    st.warning(
        "Aucun log API disponible pour cette campagne."
    )

st.divider()

# ======================================================
# SYSTEM HEALTH MONITORING
# ======================================================

st.header("🖥️ System Health Monitoring")

st.write(
    """
Surveillance de l'infrastructure.

Indicateurs :
- utilisation CPU
- utilisation mémoire
- évolution temporelle
"""
)

if len(health_logs_selected) > 0:

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

    # Evolution CPU / mémoire

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

else:

    st.warning(
        "Aucun log système disponible pour cette campagne."
    )

st.divider()

# ======================================================
# RESUME GLOBAL
# ======================================================

st.header("📋 Résumé global monitoring")

important_drift = (
    drift_selected["status"]
    ==
    "Drift important"
).sum()

moderate_drift = (
    drift_selected["status"]
    ==
    "Drift modéré"
).sum()


# ==========================
# Indicateurs prédictions
# ==========================

if len(predictions_selected) > 0:

    positive_rate = (
        predictions_selected["prediction"]
        .mean()
    )

else:

    positive_rate = 0


# ==========================
# Indicateurs API
# ==========================

if len(api_logs_selected) > 0:

    api_error_rate = (
        api_logs_selected["status_code"]
        .ne(200)
        .mean()
    )

    api_p95 = (
        api_logs_selected["response_time"]
        .quantile(0.95)
    )

else:

    api_error_rate = 0
    api_p95 = 0


# ==========================
# Indicateurs système
# ==========================

if len(health_logs_selected) > 0:

    cpu_alert = (
        health_logs_selected["cpu_usage"]
        .max()
    )

    memory_alert = (
        health_logs_selected["memory_usage"]
        .max()
    )

else:

    cpu_alert = 0
    memory_alert = 0


# ==========================
# KPIs résumé
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Drift important",
        important_drift
    )

with col2:

    st.metric(
        "Drift modéré",
        moderate_drift
    )

with col3:

    st.metric(
        "Taux positif",
        f"{positive_rate:.2%}"
    )

with col4:

    st.metric(
        "Erreur API",
        f"{api_error_rate:.2%}"
    )


# ==========================
# Etat global
# ==========================

if important_drift > 0:

    monitoring_status = (
        "⚠️ Surveillance drift requise"
    )

elif api_error_rate > 0:

    monitoring_status = (
        "⚠️ Problème API détecté"
    )

elif cpu_alert > 90:

    monitoring_status = (
        "⚠️ Charge CPU élevée"
    )

else:

    monitoring_status = (
        "✅ Système nominal"
    )


st.subheader("État global")

st.info(
    monitoring_status
)


# ==========================
# Points de vigilance
# ==========================

st.subheader("Points de vigilance")

st.markdown(
"""
### 📉 Data Drift
- Surveiller les variables présentant un PSI ou un KS élevé.
- Une dérive persistante peut traduire une évolution de la population en production.

### 🤖 Modèle
- Vérifier la stabilité du taux de prédictions positives.
- Contrôler la distribution des scores.

### ⚡ API
- Suivre la latence P95.
- Vérifier le taux d'erreurs HTTP.

### 🖥️ Infrastructure
- Surveiller les pics CPU.
- Contrôler la consommation mémoire.
"""
)


