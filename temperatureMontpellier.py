import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
df = pd.read_csv("meteoMontpellier.csv", sep=";", low_memory=False)

# Conversion de la date
df["validity_time"] = pd.to_datetime(df["validity_time"], utc=True)
df["annee"] = df["validity_time"].dt.year
df["mois"] = df["validity_time"].dt.month

# Conversion Kelvin -> Celsius
df["temp_c"] = df["t"] - 273.15

df_mois = (
    df.groupby(["annee", "mois"])["temp_c"]
    .mean()
    .reset_index()
)

annees = sorted(df_mois["annee"].unique())

# Tracé du graphique
plt.figure(figsize=(12, 6))

for annee in annees:
    data = df_mois[df_mois["annee"] == annee]
    plt.plot(
        data["mois"],
        data["temp_c"],
        label=str(annee),
        linewidth=1.5
    )

plt.xticks(range(1, 13))
plt.xlabel("Mois")
plt.ylabel("Température moyenne (°C)")
plt.title("Température moyenne mensuelle à Montpellier – toutes les années disponibles")
plt.legend(
    ncol=3,
    fontsize=8
)
plt.grid(True)
plt.tight_layout()
plt.show()

