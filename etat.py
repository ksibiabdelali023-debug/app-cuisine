"""État de la session : panier, nombre de personnes par recette, pagination."""
import streamlit as st

PREFIXES = ("pers_", "pn_", "c_")   # champs « nombre de personnes » (fiche, panier, courses)


def init():
    st.session_state.setdefault("selection", [])
    st.session_state.setdefault("portions", {})          # {id_recette: nombre de personnes}
    st.session_state.setdefault("nb_affiche", 8)
    st.session_state.setdefault("filtre_precedent", None)
    st.session_state.setdefault("annonce", "")
    st.session_state.setdefault("confirmer_vidage", False)


def personnes(rid):
    return st.session_state.portions.get(rid, 2)


def coef(rid):
    return personnes(rid) / 2


def basculer(rid, nom):
    sel = st.session_state.selection
    if rid in sel:
        sel.remove(rid)
        action = "retirée du panier"
    else:
        sel.append(rid)
        action = "ajoutée au panier"
    n = len(sel)
    st.session_state.annonce = f"{nom} {action}. {n} recette{'s' if n > 1 else ''} dans le panier."


def maj_portions(rid, cle):
    """Le nombre de personnes est mémorisé par recette et synchronisé entre tous les champs."""
    n = st.session_state[cle]
    st.session_state.portions[rid] = n
    for p in PREFIXES:
        autre = f"{p}{rid}"
        if autre in st.session_state and autre != cle:
            st.session_state[autre] = n


def champ_personnes(rid, prefixe, libelle):
    cle = f"{prefixe}{rid}"
    st.session_state[cle] = personnes(rid)
    return st.number_input(libelle, min_value=1, max_value=12, step=1, key=cle,
                           on_change=maj_portions, args=(rid, cle))


def appliquer_a_toutes():
    n = st.session_state.global_pers
    for rid in st.session_state.selection:
        st.session_state.portions[rid] = n
        for p in PREFIXES:
            if f"{p}{rid}" in st.session_state:
                st.session_state[f"{p}{rid}"] = n
    st.session_state.annonce = f"{n} personnes appliquées à toutes les recettes du panier."


def demander_vidage():
    st.session_state.confirmer_vidage = True


def annuler_vidage():
    st.session_state.confirmer_vidage = False


def vider_panier():
    st.session_state.selection.clear()
    st.session_state.confirmer_vidage = False
    st.session_state.annonce = "Panier vidé."
