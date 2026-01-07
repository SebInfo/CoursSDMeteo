import pandas as pd
from glob import glob
import os

# ----------------------------
# PARAMÈTRES
# ----------------------------
WMO_MONTPELLIER = "07643"
PAS = 1
ANNEE_DEBUT = 1996
ANNEE_FIN = 2025   # incluse

DOSSIER_DONNEES = "donnees"

# ----------------------------
# SÉLECTION DES FICHIERS PAR ANNÉE
# ----------------------------
fichiers = []

for fichier in glob(f"{DOSSIER_DONNEES}/synop_*.csv"):
    annee = int(os.path.basename(fichier)[6:10])  # extrait YYYY
    if ANNEE_DEBUT <= annee <= ANNEE_FIN:
        if (
                ANNEE_DEBUT <= annee <= ANNEE_FIN
                and (annee - ANNEE_DEBUT) % PAS == 0
        ):
            fichiers.append(fichier)

fichiers = sorted(fichiers)

print("Fichiers sélectionnés :")
for f in fichiers:
    print(" -", f)

# ----------------------------
# LECTURE ET FILTRAGE
# ----------------------------
dfs = []

for fichier in fichiers:
    df = pd.read_csv(
        fichier,
        sep=";",
        dtype={"geo_id_wmo": str},
        low_memory=False
    )

    df_station = df[df["geo_id_wmo"] == WMO_MONTPELLIER].copy()

    df_station["validity_time"] = pd.to_datetime(
        df_station["validity_time"],
        utc=True,
        errors="coerce"
    )

    if not df_station.empty:
        dfs.append(df_station)

# ----------------------------
# CONCATÉNATION
# ----------------------------
if not dfs:
    raise RuntimeError("Aucune donnée trouvée pour la période demandée")

df_montpellier = pd.concat(dfs, ignore_index=True)

# ----------------------------
# NETTOYAGE
# ----------------------------
colonnes_inutiles = [
    "lat",
    "lon",
    "geo_id_wmo",
    "geo_id_wigos",
    "name"
]

df_montpellier = df_montpellier.drop(
    columns=colonnes_inutiles,
    errors="ignore"
)

df_montpellier = df_montpellier.dropna(axis=1, how="all")

# ----------------------------
# EXPORT
# ----------------------------
df_montpellier.to_csv("meteoMontpellier.csv", sep=";", index=False)

print("Export terminé")
print("Période :", ANNEE_DEBUT, "-", ANNEE_FIN)
print("Nombre de lignes :", len(df_montpellier))
