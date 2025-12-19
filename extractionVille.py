import pandas as pd

# Identifiant OMM de Montpellier-Aéroport
WMO_MONTPELLIER = "07643"

df = pd.read_csv(
    "donnees/synop_2014.csv",
    sep=";",
    dtype={"geo_id_wmo": str},
    low_memory=False
)

df_montpellier = df[df["geo_id_wmo"] == WMO_MONTPELLIER]

print(df_montpellier.head())
print("Nombre de lignes :", len(df_montpellier))
# On supprimes les colonnes pour lesquels c'est toujours vide
df_montpellier = df_montpellier.dropna(axis=1, how="all")
df_montpellier.to_csv("meteoMontpellier.csv", sep=";", index=False)
