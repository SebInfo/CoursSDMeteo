import pandas as pd
import folium
from folium.plugins import MarkerCluster

stations = pd.read_csv("donnees/stations_meteo.csv", sep=";")  # adapte sep si besoin
stations = stations.dropna(subset=["lat", "lon"])
m = folium.Map(location=[46.5, 2.5], zoom_start=6, tiles="OpenStreetMap")
cluster = MarkerCluster().add_to(m)

for _, r in stations.iterrows():
    folium.CircleMarker(
        location=[r["lat"], r["lon"]],
        radius=6,
        tooltip=r["name"],
        popup=r["name"]
    ).add_to(cluster)

m.save("carte_stations.html")
