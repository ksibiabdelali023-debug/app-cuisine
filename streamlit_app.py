"""Point d'entrée : streamlit run streamlit_app.py"""
import streamlit as st

st.set_page_config(page_title="MiamMiam", page_icon="🍳", layout="centered")

import etat, pages, ressources, theme  # noqa: E402
from calculs import format_prix, totaux  # noqa: E402
from ui import annonce_html  # noqa: E402

etat.init()
recettes = ressources.charger_recettes()
par_id = {r["id"]: r for r in recettes}

st.markdown(
    '<div class="hero"><div class="ligne"><span class="logo" aria-hidden="true">🍳</span><div>'
    "<h1>MiamMiam</h1><p>Recettes 100 % halal · comparez Leclerc et Lidl</p></div></div></div>",
    unsafe_allow_html=True)

with st.expander("⚙️ Affichage : taille du texte et contraste"):
    taille = st.radio("Taille du texte", list(theme.TAILLES), horizontal=True, key="taille")
    st.checkbox("Contraste élevé (noir sur blanc)", key="contraste")

palette = theme.ELEVE if st.session_state.get("contraste") else theme.NORMAL
st.markdown(theme.css(palette, theme.TAILLES[taille]), unsafe_allow_html=True)
st.markdown(annonce_html(), unsafe_allow_html=True)

sel = [par_id[i] for i in st.session_state.selection]
n = len(sel)
if n:
    lec, lid = totaux(sel, etat.coef)
    st.markdown(f'<div class="resume">🛒 Panier : {n} recette{"s" if n > 1 else ""} · Leclerc {format_prix(lec)} '
                f'· Lidl {format_prix(lid)}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="resume">🛒 Panier vide · ajoutez des recettes pour comparer les prix</div>',
                unsafe_allow_html=True)

onglet_recettes, onglet_planning, onglet_panier, onglet_courses = st.tabs(
    ["🍽️ Recettes", "📅 Planning", f"🛒 Panier ({n})", "🧾 Courses"])
with onglet_recettes:
    pages.page_recettes(recettes)
with onglet_planning:
    pages.page_planning(recettes, par_id)
with onglet_panier:
    pages.page_panier(par_id)
with onglet_courses:
    pages.page_courses(par_id)
