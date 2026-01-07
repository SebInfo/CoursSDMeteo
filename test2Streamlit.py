import streamlit as st

st.title("Tableau de bord météo")

st.subheader("Contexte")
st.write(
    "Cette application permet de visualiser des données météo issues de l’Open Data. "
    "Elle a été développée avec Streamlit dans un objectif de prototypage rapide."
)

st.divider()

st.header("Sélection des paramètres")

st.markdown("""
### Contexte de l'application

Cette application a pour objectif de **visualiser des données météo Open Data**
dans un cadre de **prototypage rapide**.

Les données exploitées permettent :
- l'analyse de l'évolution des **températures**
- la comparaison entre **stations météo**
- l'observation de tendances **saisonnières**

---
### Fonctionnalités disponibles

- Sélection d'une **station météo**
- Choix de l'**année**
- Visualisation graphique de la température
- Affichage d'indicateurs statistiques

---
### Source des données

Les données utilisées proviennent de l'Open Data :
- [data.gouv.fr](https://www.data.gouv.fr)
- ou de jeux de données météo locaux

""")

st.divider()

st.header("Résultats")
st.write(
    "Les graphiques ci-dessous présentent l’évolution de la température "
    "en fonction de la période sélectionnée."
)