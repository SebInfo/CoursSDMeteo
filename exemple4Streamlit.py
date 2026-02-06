import streamlit as st

st.title("Démo des widgets Streamlit")

# --- Bouton ---
st.subheader("Bouton")
if st.button("Actualiser"):
    st.write("✅ Bouton cliqué")

# --- Slider ---
st.subheader("Slider")
temperature = st.slider(
    "Température (°C)",
    min_value=-10,
    max_value=40,
    value=20
)
st.write("Température sélectionnée :", temperature, "°C")

# --- Liste déroulante ---
st.subheader("Liste déroulante")
station = st.selectbox(
    "Station météo",
    ["Carcassonne", "Toulouse", "Narbonne"]
)
st.write("Station sélectionnée :", station)
