import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# --- Chargement des données ---
df = pd.read_csv("meteo.csv", parse_dates=["date"])

st.title("Tableau de bord météo")

st.markdown("### Paramètres de visualisation")

# --- Widgets ---
station = st.selectbox(
    "Station météo",
    sorted(df["station"].unique())
)

temperature_min = st.slider(
    "Température minimale (°C)",
    min_value=-20,
    max_value=40,
    value=0
)

afficher_graphique = st.button("Actualiser l'affichage")

# --- Traitement déclenché par les widgets ---
if afficher_graphique:

    # Filtrage des données
    df_filtre = df[
        (df["station"] == station) &
        (df["temperature"] >= temperature_min)
    ]

    st.markdown("### Résultats")

    # Affichage des données filtrées
    st.write("Aperçu des données filtrées")
    st.dataframe(df_filtre)

    # Indicateurs
    st.metric(
        "Température moyenne",
        round(df_filtre["temperature"].mean(), 1)
    )

    annees = df_filtre["date"].dt.year.unique()
    annee_min = annees.min()
    annee_max = annees.max()

    if annee_min == annee_max:
        periode = str(annee_min)
    else:
        periode = f"{annee_min} - {annee_max}"

    # Graphique matplotlib
    fig, ax = plt.subplots()

    ax.plot(df_filtre["date"], df_filtre["temperature"])

    ax.set_title(f"Évolution de la température ({periode})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Température (°C)")

    # Format de la date : jour/mois
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

    fig.autofmt_xdate()  # inclinaison automatique (optionnel)

    st.pyplot(fig)

else:
    st.info("Sélectionnez les paramètres puis cliquez sur « Actualiser l'affichage ».")