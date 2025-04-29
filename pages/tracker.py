import streamlit as st
import json
from pathlib import Path
from datetime import datetime, date, timedelta

# === CONFIGURATION ===

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "tracking.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_sessions():
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        save_sessions([])
        return []

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        save_sessions([])
        return []


def save_sessions(sessions):
    with open(DATA_FILE, "w") as f:
        json.dump(sessions, f, indent=2)


def main():
    st.title("⏱️ Tracker de Temps")

    if "tache_active" not in st.session_state:
        st.session_state.tache_active = None

    with st.form("form_tache"):
        nom = st.text_input("Nom de la tâche")
        categorie = st.selectbox("Catégorie", ["Deep Work", "admin", "pause", "perso"])
        submit = st.form_submit_button("▶️ Lancer la tâche")

        if submit:
            if st.session_state.tache_active:
                st.warning("Une tâche est déjà en cours")
            elif nom:
                st.session_state.tache_active = {
                    "nom": nom,
                    "categorie": categorie,
                    "debut": datetime.now().isoformat()
                }
                st.success(f"Tâche '{nom}' lancée.")

    if st.session_state.tache_active:
        tache = st.session_state.tache_active
        debut = datetime.fromisoformat(tache["debut"])
        maintenant = datetime.now()
        delta = maintenant - debut

        # Format hh:mm:ss
        def format_timedelta(td):
            total_seconds = int(td.total_seconds())
            return str(timedelta(seconds=total_seconds))

        duree_affichee = format_timedelta(delta)

        st.info(f"⏳ Tâche en cours : **{tache['nom']}** ({tache['categorie']}) — Durée : `{duree_affichee}`")

        col1, col2 = st.columns([1, 1])
        if col1.button("🔄 Actualiser"):
            st.rerun()

        if col2.button("⏹️ Arrêter la tâche"):
            fin = datetime.now()
            duree_minutes = round((fin - debut).total_seconds() / 60, 2)

            nouvelle_session = {
                "nom": tache["nom"],
                "categorie": tache["categorie"],
                "debut": debut.isoformat(),
                "fin": fin.isoformat(),
                "duree_minutes": duree_minutes,
            }

            sessions = load_sessions()
            sessions.append(nouvelle_session)
            save_sessions(sessions)

            st.session_state.tache_active = None
            st.success(f"Tâche arrêtée. Durée : {duree_minutes} minutes.")

    # Historique du jour
    st.subheader("📅 Historique du jour")

    sessions = load_sessions()
    sessions_du_jour = [
        s for s in sessions
        if datetime.fromisoformat(s["debut"]).date() == date.today()
    ]

    if sessions_du_jour:
        for s in sessions_du_jour:
            st.write(f"- **{s['nom']}** ({s['categorie']}) : {s['duree_minutes']} min")
    else:
        st.write("Aucune session enregistrée aujourd'hui.")


# Exécuter si lancé directement
if __name__ == "__main__":
    main()
