import streamlit as st
import os

# Configuration de la page
st.set_page_config(
    page_title="Cortex – QG Intelligent",
    page_icon="🧠",
    layout="wide"
)

# En-tête
st.title("🧠 Cortex – Ton Quartier Général Personnel")
st.subheader("Bienvenue dans ton espace d'organisation et de productivité.")

# Sidebar de navigation
st.sidebar.title("Navigation 🗺️")
page = st.sidebar.selectbox("Aller vers :", ("Dashboard", "Objectifs Hebdomadaires"))

# Pages dynamiques
if page == "Dashboard":
    st.header("📊 Vue d'ensemble")
    st.write("Cette section affichera bientôt ton agenda, ton niveau d’énergie et tes stats principales.")

    st.info("Module en construction. 🚧")

elif page == "Objectifs Hebdomadaires":
    # Redirection vers le module Objectifs
    from pages import objectifs
    objectifs.main()

# Footer simple
st.sidebar.markdown("---")
st.sidebar.caption("Version MVP – Cortex 2025")
