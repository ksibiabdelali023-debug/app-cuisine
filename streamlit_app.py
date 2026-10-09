import streamlit as st
import etat
import ressources
from donnees import BASE

st.set_page_config(
    page_title="MiamMiam - Recettes Halal & Comparateur",
    page_icon="🍳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "selection" not in st.session_state:
    st.session_state.selection = []
if "planning" not in st.session_state:
    st.session_state.planning = {}
if "semaine_debut" not in st.session_state:
    import datetime
    st.session_state.semaine_debut = datetime.date.today()
if "filtre_precedent" not in st.session_state:
    st.session_state.filtre_precedent = (None, None, None, None)
if "nb_affiche" not in st.session_state:
    st.session_state.nb_affiche = 8
if "confirmer_vidage" not in st.session_state:
    st.session_state.confirmer_vidage = False

st.markdown("""
    <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 24px; border-radius: 16px; text-align: center; margin-bottom: 24px;">
        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 800;">MiamMiam 🍳</h1>
        <p style="color: #E0F2FE; margin: 8px 0 0 0; font-size: 14px;">Recettes 100% Halal • Comparez Leclerc et Lidl</p>
    </div>
""", unsafe_allow_html=True)

recettes_structurees = []
recettes_par_id = {}

for idx, item in enumerate(BASE):
    if isinstance(item, tuple):
        nom, categorie, temps, diff = item
        from donnees import FICHES
        fiche = FICHES.get(nom, {"ingredients": [], "etapes": [], "astuce": "", "halal": ""})
        r_dict = {
            "id": str(idx), "nom": nom, "base": nom, "categorie": categorie,
            "temps": temps, "difficulte": diff, "ingredients": fiche["ingredients"],
            "etapes": fiche["etapes"], "astuce": fiche["astuce"], "halal": fiche["halal"]
        }
    else:
        r_dict = item
        if "id" not in r_dict:
            r_dict["id"] = str(idx)
            
    recettes_structurees.append(r_dict)
    recettes_par_id[r_dict["id"]] = r_dict

nb_panier = len(st.session_state.selection)
label_panier = f"🛒 Panier ({nb_panier})" if nb_panier > 0 else "🛒 Panier"

o_recettes, o_planning, o_panier, o_courses = st.tabs([
    "🥗 Recettes", "📅 Planning", label_panier, "📝 Liste de Courses"
])

# Importation dynamique sécurisée pour contourner le problème d'indentation du haut de fichier
import importlib
p = importlib.import_module("pages")

with o_recettes:
    p.page_recettes(recettes_structurees)

with o_planning:
    p.page_planning(recettes_structurees, recettes_par_id)

with o_panier:
    p.page_panier(recettes_par_id)

with o_courses:
    p.page_courses(recettes_par_id)
