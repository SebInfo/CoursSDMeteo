# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aide à la décision", layout="wide")
st.title("Mini outil d'aide à la décision (scoring pondéré)")

# --- Paramètres (poids) ---
st.sidebar.header("Poids des critères (somme = 1)")
w_cost = st.sidebar.slider("Poids coût", 0.0, 1.0, 0.25, 0.05)
w_delay = st.sidebar.slider("Poids délai", 0.0, 1.0, 0.25, 0.05)
w_risk = st.sidebar.slider("Poids risque", 0.0, 1.0, 0.25, 0.05)
w_value = st.sidebar.slider("Poids valeur/impact", 0.0, 1.0, 0.25, 0.05)

weights = {"Coût": w_cost, "Délai": w_delay, "Risque": w_risk, "Valeur": w_value}
sum_w = sum(weights.values())
st.sidebar.write(f"Somme des poids : **{sum_w:.2f}**")

if abs(sum_w - 1.0) > 1e-6:
    st.sidebar.warning("Ajuste les poids pour que la somme fasse 1.")

st.divider()

# --- Entrées (critères normalisés 0..1) ---
st.subheader("Entrées (0 = faible / 1 = fort)")
c1, c2 = st.columns(2)

with c1:
    # Ici: coût, délai, risque => plus c'est grand, plus c'est "mauvais"
    cost = st.slider("Coût (0..1)", 0.0, 1.0, 0.4, 0.05)
    delay = st.slider("Délai (0..1)", 0.0, 1.0, 0.3, 0.05)

with c2:
    risk = st.slider("Risque (0..1)", 0.0, 1.0, 0.2, 0.05)
    # Valeur => plus c'est grand, plus c'est "bon"
    value = st.slider("Valeur/Impact (0..1)", 0.0, 1.0, 0.7, 0.05)

# --- Modèle simple ---
# On transforme les critères "mauvais" en "bons" via (1 - x)
normalized = {
    "Coût": 1 - cost,
    "Délai": 1 - delay,
    "Risque": 1 - risk,
    "Valeur": value
}

contrib = {k: weights[k] * normalized[k] for k in normalized}
score = sum(contrib.values())

# Règles de décision (exemple)
if risk > 0.7:
    decision = "❌ À éviter (risque trop élevé)"
elif score >= 0.75:
    decision = "✅ Go"
elif score >= 0.55:
    decision = "⚠️ À discuter / améliorer"
else:
    decision = "❌ Non"

# --- Affichage ---
df = pd.DataFrame({
    "Critère": list(normalized.keys()),
    "Poids": [weights[k] for k in normalized],
    "Valeur (0..1 bon)": [normalized[k] for k in normalized],
    "Contribution": [contrib[k] for k in normalized],
}).sort_values("Contribution", ascending=False)

left, right = st.columns([1.2, 1])

with left:
    st.subheader("Détails du calcul")
    st.dataframe(df, use_container_width=True)

with right:
    st.subheader("Résultat")
    st.metric("Score global", f"{score:.2f}")
    st.write(f"**Décision : {decision}**")

    top = df.head(3)[["Critère", "Contribution"]]
    st.caption("Principaux facteurs (top 3 contributions)")
    st.table(top)

# --- Scénarios (A/B/C) ---
st.divider()
st.subheader("Scénarios (comparaison rapide)")

if "scenarios" not in st.session_state:
    st.session_state.scenarios = []

colA, colB, colC = st.columns([1, 1, 1])

with colA:
    name = st.text_input("Nom du scénario", "Scénario 1")
with colB:
    if st.button("Ajouter / sauvegarder"):
        st.session_state.scenarios.append({
            "Nom": name,
            "Score": round(score, 2),
            "Coût": cost, "Délai": delay, "Risque": risk, "Valeur": value
        })
with colC:
    if st.button("Effacer tous les scénarios"):
        st.session_state.scenarios = []

if st.session_state.scenarios:
    sdf = pd.DataFrame(st.session_state.scenarios).sort_values("Score", ascending=False)
    st.dataframe(sdf, use_container_width=True)
    st.download_button("Télécharger CSV", sdf.to_csv(index=False).encode("utf-8"), "scenarios.csv", "text/csv")
else:
    st.info("Ajoute un scénario pour comparer.")
