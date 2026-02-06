import streamlit as st

st.title("Tableau de bord météo")

st.subheader("Contexte")
st.write(
    "Cette application permet de visualiser des données météo issues de l’Open Data. "
    "Elle a été développée avec Streamlit dans un objectif de prototypage rapide."
)

st.divider()

st.header("Sélection des paramètres")
st.markdown(
    "- Choix de la station météo\n"
    "- Choix de la période d’analyse\n"
    "- Affichage des indicateurs principaux"
)

st.divider()

st.header("Résultats")
st.write(
    "Les graphiques ci-dessous présentent l’évolution de la température "
    "en fonction de la période sélectionnée."
)