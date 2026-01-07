import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Suivi événements météo (ww)", layout="wide")
st.title("Suivi d'événements météo (SYNOP) via le code ww")

# --- Chargement des données ---
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=";",
        parse_dates=["validity_time"],
        low_memory=False
    )

    # Nettoyage minimal
    df = df.dropna(axis=1, how="all")  # colonnes entièrement vides
    # Assurer ww numérique (certaines sources le mettent en float à cause des NaN)
    df["ww"] = pd.to_numeric(df["ww"], errors="coerce")
    df = df.dropna(subset=["ww", "validity_time"])
    df["ww"] = df["ww"].astype(int)

    return df

csv_path = st.text_input("Chemin du fichier CSV", "meteoMontpellier.csv")
df = load_data(csv_path)

# Option fuseau horaire (souvent inutile si on compte “par année” en UTC, mais utile si besoin local)
use_paris = st.checkbox("Convertir la date en Europe/Paris", value=False)
if use_paris:
    # validity_time est généralement timezone-aware (UTC)
    df["validity_time"] = df["validity_time"].dt.tz_convert("Europe/Paris")

# --- Widgets de sélection ---
st.subheader("Paramètres")

col1, col2 = st.columns([1, 2])

with col1:
    ww_values = sorted(df["ww"].unique().tolist())
    ww_choice = st.selectbox("Code ww à suivre", ww_values, index=0)

with col2:
    # Petit texte d’aide (tu peux enrichir ce dictionnaire si tu veux)
    ww_labels = {
        0: "Temps clair",
        5: "Brume",
        10: "Brouillard",
        95: "Orage",
        96: "Orage + grêle",
    }
    st.info(f"Code sélectionné : **{ww_choice}**" + (f" — {ww_labels[ww_choice]}" if ww_choice in ww_labels else ""))

# --- Calcul : occurrences par année ---
data = df[df["ww"] == ww_choice].copy()
data["year"] = data["validity_time"].dt.year

counts = data.groupby("year").size().sort_index()  # nb d'observations par année

st.subheader("Résultats")

c1, c2 = st.columns([1, 1])
with c1:
    st.metric("Nombre total d'observations", int(counts.sum()) if not counts.empty else 0)
with c2:
    st.metric("Nombre d'années concernées", int(counts.shape[0]))

# --- Graphique matplotlib : histogramme (barres) ---
fig, ax = plt.subplots()
if counts.empty:
    ax.text(0.5, 0.5, "Aucune donnée pour ce code ww", ha="center", va="center")
    ax.set_axis_off()
else:
    ax.bar(counts.index.astype(str), counts.values)
    ax.set_title(f"Nombre d'observations par année (ww = {ww_choice})")
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre d'observations")
    ax.tick_params(axis="x", rotation=45)

st.pyplot(fig)

# --- Option : tableau sous le graphique ---
with st.expander("Afficher le tableau des comptages"):
    st.dataframe(counts.rename("count").to_frame(), use_container_width=True)
