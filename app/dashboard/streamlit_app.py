import pandas as pd
import streamlit as st
import plotly.express as px

from app.dashboard.queries import (
    load_predictions,
    load_api_logs,
    load_system_health_logs,
    load_table
)


# ==========================
# Configuration Streamlit
# ==========================

st.set_page_config(
    page_title="Credit Scoring Monitoring",
    layout="wide"
)


st.title("📊 Credit Scoring - Monitoring Production")


st.write(
    "Dashboard de supervision du modèle de scoring en production"
)


# ==========================
# Chargement données Neon DB
# ==========================

drift = load_table(
    "drift_monitoring"
)

reference_stats = load_table(
    "reference_stats"
)

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
# Création des campagnes drift
# ==========================

drift["campaign_date"] = (
    drift["created_at"]
    .dt.date
)


available_campaigns = (
    drift["campaign_date"]
    .drop_duplicates()
    .sort_values(
        ascending=False
    )
)


# ==========================
# Sélecteur campagne
# ==========================

selected_day = st.selectbox(
    "Sélectionner une campagne de monitoring",
    available_campaigns
)


# ==========================
# Filtrage cohérent
# ==========================

drift_selected = drift[
    drift["campaign_date"]
    ==
    selected_day
].copy()


predictions_selected = predictions[
    predictions["created_at"]
    .dt.date
    ==
    selected_day
].copy()


api_logs_selected = api_logs[
    api_logs["created_at"]
    .dt.date
    ==
    selected_day
].copy()


health_logs_selected = health_logs[
    health_logs["created_at"]
    .dt.date
    ==
    selected_day
].copy()


# ==========================
# Contrôle cohérence données
# ==========================

if len(predictions_selected) == 0:

    st.warning(
        "Aucune prédiction trouvée pour cette campagne"
    )


if len(api_logs_selected) == 0:

    st.warning(
        "Aucun log API trouvé pour cette campagne"
    )


if len(health_logs_selected) == 0:

    st.warning(
        "Aucun log système trouvé pour cette campagne"
    )


# ==========================
# Bandeau contrôle campagne
# ==========================

st.info(
    f"""
📅 Campagne sélectionnée : {selected_day}

📉 Features drift analysées : {len(drift_selected)}

🤖 Prédictions : {len(predictions_selected)}

⚡ Requêtes API : {len(api_logs_selected)}

🖥️ Logs système : {len(health_logs_selected)}
"""
)


# ==========================
# KPIs globaux
# ==========================

st.subheader(
    "Connexion Neon OK"
)


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

# ==========================
# DATA DRIFT MONITORING
# ==========================

st.header(
    "📉 Data Drift Monitoring"
)


st.write(
    """
    Analyse de dérive des variables d'entrée du modèle.

    Indicateurs :
    - PSI (Population Stability Index)
    - KS (Kolmogorov-Smirnov)

    Référence :
    statistiques calculées sur les données historiques d'entraînement.
    Production :
    nouvelles données reçues par l'API.
    """
)


# ==========================
# Drift sélectionné uniquement
# ==========================

drift_display = (
    drift_selected
    .sort_values(
        "psi",
        ascending=False
    )
)


st.subheader(
    "Top variables avec dérive"
)


st.dataframe(
    drift_display.head(20),
    use_container_width=True
)


st.subheader(
    "Détail complet du drift"
)


st.dataframe(
    drift_selected,
    use_container_width=True
)


# ==========================
# Graphique PSI
# ==========================

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
    title="Top variables selon PSI"
)


fig_psi.update_layout(
    yaxis_title="Feature",
    xaxis_title="PSI"
)


st.plotly_chart(
    fig_psi,
    use_container_width=True
)


# ==========================
# Graphique KS
# ==========================

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
    title="Top variables selon KS"
)


fig_ks.update_layout(
    yaxis_title="Feature",
    xaxis_title="KS"
)


st.plotly_chart(
    fig_ks,
    use_container_width=True
)



# ==========================
# Statut drift
# ==========================

col1, col2, col3 = st.columns(3)


with col1:

    important = (
        drift_selected["status"]
        ==
        "Drift important"
    ).sum()


    st.metric(
        "Drift important",
        important
    )


with col2:

    moderate = (
        drift_selected["status"]
        ==
        "Drift modéré"
    ).sum()


    st.metric(
        "Drift modéré",
        moderate
    )


with col3:

    stable = (
        drift_selected["status"]
        ==
        "Stable"
    ).sum()


    st.metric(
        "Stable",
        stable
    )



# ==========================
# Référence
# ==========================

st.subheader(
    "Référence utilisée"
)


st.info(
    f"""
Nombre de variables historiques :
{reference_stats.shape[0]}

Taille historique :
{reference_stats['sample_size'].iloc[0]}

Source :
statistiques calculées sur les données d'entraînement.
"""
)



# ======================================================
# PREDICTION MONITORING
# ======================================================


st.divider()


st.header(
    "🤖 Prediction Monitoring"
)


st.write(
    """
Analyse des sorties du modèle.

Métriques :
- volume de prédictions
- taux positif
- score moyen
- distribution des probabilités
- seuil de décision
"""
)



# Protection dataframe vide

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


    # ==========================
    # Distribution scores
    # ==========================


    threshold = (
        predictions_selected["threshold"]
        .iloc[0]
    )


    fig_score = px.histogram(
        predictions_selected,
        x="score",
        nbins=20,
        title="Distribution des scores modèle"
    )


    fig_score.add_vline(
        x=threshold,
        line_dash="dash",
        annotation_text=
        f"Seuil : {threshold:.3f}"
    )


    fig_score.update_layout(
        xaxis_title="Probabilité défaut",
        yaxis_title="Nombre"
    )


    st.plotly_chart(
        fig_score,
        use_container_width=True
    )


else:

    st.warning(
        "Pas de prédiction pour cette période"
    )


st.divider()

# ======================================================
# API MONITORING
# ======================================================

st.header(
    "⚡ API Monitoring"
)


st.write(
    """
Surveillance opérationnelle de l'API de scoring.

Indicateurs :
- volume des requêtes
- taux d'erreur HTTP
- latence moyenne
- latence P95
- évolution temporelle
"""
)



if len(api_logs_selected) > 0:


    total_requests = (
        len(api_logs_selected)
    )


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



    # Distribution latence

    fig_latency = px.histogram(
        api_logs_selected,
        x="response_time",
        nbins=30,
        title="Distribution latence API"
    )


    fig_latency.update_layout(
        xaxis_title="Temps réponse (ms)",
        yaxis_title="Nombre requêtes"
    )


    st.plotly_chart(
        fig_latency,
        use_container_width=True
    )



    # Evolution latence

    api_time = (
        api_logs_selected
        .sort_values(
            "created_at"
        )
    )


    fig_time = px.line(
        api_time,
        x="created_at",
        y="response_time",
        title="Evolution latence API"
    )


    fig_time.update_layout(
        xaxis_title="Temps",
        yaxis_title="Latence (ms)"
    )


    st.plotly_chart(
        fig_time,
        use_container_width=True
    )


else:

    st.warning(
        "Pas de logs API pour cette période"
    )



st.divider()



# ======================================================
# SYSTEM HEALTH MONITORING
# ======================================================


st.header(
    "🖥️ System Health Monitoring"
)


st.write(
    """
Surveillance infrastructure API.

Indicateurs :
- CPU
- mémoire
- pics de charge
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



    # Evolution CPU mémoire


    health_time = (
        health_logs_selected
        .sort_values(
            "created_at"
        )
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
        "Pas de logs système pour cette période"
    )



st.divider()



# ======================================================
# RESUME GLOBAL
# ======================================================


st.header(
    "📋 Résumé global monitoring"
)



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



if len(predictions_selected) > 0:


    positive_rate = (
        predictions_selected["prediction"]
        .mean()
    )


else:

    positive_rate = 0



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



# Etat global


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



st.subheader(
    "Etat global"
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
- Surveiller les variables avec PSI ou KS élevés.
- Une dérive persistante peut indiquer un changement de population.

### Modèle
- Surveiller le taux positif.
- Vérifier la stabilité des scores.

### API
- Surveiller la latence P95.
- Identifier les ralentissements.

### Infrastructure
- Vérifier les pics CPU.
- Surveiller la mémoire.
"""
)
