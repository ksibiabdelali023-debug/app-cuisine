"""Point d'entrée principal de l'application MiamMiam."""
import streamlit as st

# Alignement strict à gauche pour éviter toute IndentationError
import etat
import pages
import ressources
from donnees import BASE

# 1. Configuration de la page Streamlit (Style Application Mobile)
st.set_page_config(
    page_title="MiamMiam - Recettes Halal & Comparateur",
    page_icon="🍳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Initialisation de l'état global de la session (si non déjà fait dans etat.py)
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

# 3. En-tête de l'application (Hero Banner Moderne et Épurée)
st.markdown("""
    <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 24px; border-radius: 16px; text-align: center; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 800;">MiamMiam 🍳</h1>
        <p style="color: #E0F2FE; margin: 8px 0 0 0; font-size: 14px;">Recettes 100% Halal • Comparez Leclerc et Lidl pour économiser</p>
    </div>
""", unsafe_allow_html=True)

# 4. Préparation du dictionnaire de recettes indexées par identifiant unique
# Transformation de la liste BASE en dictionnaires structurés et indexation
recettes_structurees = []
recettes_par_id = {}

for idx, item in enumerate(BASE):
    # Gestion de la structure selon le format importé (tuple ou dict)
    if isinstance(item, tuple):
        nom, categorie, temps, diff = item
        # Récupération des ingrédients, étapes, etc. depuis les fiches de donnees
        from donnees import FICHES
        fiche = FICHES.get(nom, {"ingredients": [], "etapes": [], "astuce": "", "halal": ""})
        r_dict = {
            "id": str(idx),
            "nom": nom,
            "base": nom,
            "categorie": categorie,
            "temps": temps,
            "difficulte": diff,
            "ingredients": fiche["ingredients"],
            "etapes": fiche["etapes"],
            "astuce": fiche["astuce"],
            "halal": fiche["halal"]
        }
    else:
        r_dict = item
        if "id" not in r_dict:
            r_dict["id"] = str(idx)
            
    recettes_structurees.append(r_dict)
    recettes_par_id[r_dict["id"]] = r_dict

# 5. Système de Navigation par Onglets (Modernisé)
nb_panier = len(st.session_state.selection)
label_panier = f"🛒 Panier ({nb_panier})" if nb_panier > 0 else "🛒 Panier"

onglet_recettes, onglet_planning, onglet_panier, onglet_courses = st.tabs([
    "🥗 Recettes", 
    "📅 Planning", 
    label_panier, 
    "📝 Liste de Courses"
])

# 6. Routage vers les différentes vues du module 'pages'
with onglet_recettes:
    pages.page_recettes(recettes_structurees)

with onglet_planning:
    pages.page_planning(recettes_structurees, recettes_par_id)

with onglet_panier:
    pages.page_panier(recettes_par_id)

with onglet_courses:
    pages.page_courses(recettes_par_id)
