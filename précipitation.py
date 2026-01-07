import pandas as pd

df = pd.read_csv(
    "meteoMontpellier.csv",
    sep=";",
    parse_dates=["validity_time"]
)

# Sécurité
print(df["validity_time"].dt.year.min(),
      df["validity_time"].dt.year.max())

# Pluie élémentaire NON CHEVAUCHANTE
df["rr3"] = pd.to_numeric(df["rr3"], errors="coerce").fillna(0)

# Année / mois
df["annee"] = df["validity_time"].dt.year
df["mois"] = df["validity_time"].dt.month

# Cumul mensuel CORRECT
pluie_mensuelle = (
    df.groupby(["annee", "mois"])["rr3"]
    .sum()
    .reset_index()
    .sort_values(["annee", "mois"])
)

print(pluie_mensuelle.head(24))

import matplotlib.pyplot as plt

pluie_annuelle = (
    pluie_mensuelle
    .groupby("annee")["rr3"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 5))

plt.bar(
    pluie_annuelle["annee"],
    pluie_annuelle["rr3"]
)

plt.xlabel("Année")
plt.ylabel("Pluviométrie annuelle (mm)")
plt.title("Pluviométrie annuelle à Montpellier")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

