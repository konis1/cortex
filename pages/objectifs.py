import streamlit as st
import json
from pathlib import Path

# Définit le chemin du dossier 'data' par rapport à app.py
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "objectifs.json"

# S'assurer que le dossier data existe
DATA_DIR.mkdir(exist_ok=True)


# Chargement des objectifs existants
def load_objectifs():
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        # Fichier inexistant ou vide -> on initialise
        save_objectifs([])
        return []

    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Fichier corrompu -> on réinitialise proprement
            save_objectifs([])
            return []


# Sauvgarde des objectifs
def save_objectifs(objectifs):
    with open(DATA_FILE, "w") as f:
        json.dump(objectifs, f, indent=2)


#  Afficher les objectifs
def afficher_objectifs(objectifs):
    st.subheader("📋 Objectifs de la semaine")
    if not objectifs:
        st.write("Aucun objectif défini.")
    else:
        for i, obj in enumerate(objectifs):
            col1, col2 = st.columns([8, 1])
            col1.write(f"- {obj}")
            if col2.button("❌", key=f"delete_{i}"):
                objectifs.pop(i)
                save_objectifs(objectifs)
                st.rerun()


def main():
    st.title("🎯 Objectifs Hebdomadaires")

    objectifs = load_objectifs()

    with st.form("add_objectf"):
        new_obj = st.text_input("Nouvel Objectif")
        submitted = st.form_submit_button("Ajouter")
        if submitted and new_obj:
            objectifs.append(new_obj)
            save_objectifs(objectifs)
            st.success("Objectif ajouté avec succès")
            st.rerun()

    afficher_objectifs(objectifs)


if __name__ == "__main__":
    main()
