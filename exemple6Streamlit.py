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

# -------------------------
# Dictionnaire événements
# -------------------------
WW_EVENTS = {
    "Temps clair / sec": [0, 1, 2, 3],
    "Brume": [5],
    "Brouillard": [10],
    "Pluie / bruine": list(range(20, 60)),
    "Neige / grésil": list(range(60, 80)),
    "Averses": [80, 81, 82],
    "Orage": [95, 96, 99],
}

# -------------------------
# Widgets
# -------------------------
st.subheader("Choix de l'événement")

event_label = st.selectbox(
    "Événement météo",
    list(WW_EVENTS.keys())
)

codes_ww = WW_EVENTS[event_label]

tmp = df[df["ww"].isin(codes_ww)].copy()
tmp["validity_time"] = tmp["validity_time"].dt.tz_convert("Europe/Paris")
tmp["day"] = tmp["validity_time"].dt.floor("D")
tmp["year"] = tmp["day"].dt.year

counts = (
    tmp.drop_duplicates(["day"])
       .groupby("year")
       .size()
       .sort_index()
)

# -------------------------
# Résultats
# -------------------------
st.subheader("Occurrences par année")

fig, ax = plt.subplots(figsize=(4, 2), dpi=120)

if counts.empty:
    ax.text(0.5, 0.5, "Aucune donnée pour cet événement",
            ha="center", va="center")
    ax.set_axis_off()
else:

    years = counts.index.to_list()

    ax.bar(years, counts.values)

    ax.set_title(f"{event_label} – jours par année", fontsize=10)
    ax.set_xlabel("Année", fontsize=9)
    ax.set_ylabel("Nombre de jours", fontsize=9)

    # 👉 afficher TOUTES les années
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45, fontsize=7)

    ax.tick_params(axis="y", labelsize=8)

    fig.tight_layout()

st.pyplot(fig)

with st.expander("Afficher le tableau des valeurs"):
    st.dataframe(counts.rename("nombre").to_frame(),
                 use_container_width=True)




