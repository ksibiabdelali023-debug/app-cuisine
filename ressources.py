"""Ressources mises en cache (Streamlit) : photos, prix réels, liste des recettes."""
import streamlit as st

from . import donnees, services


@st.cache_data(ttl=3600, show_spinner=False)
def photos_plats():
    return services.photos_pour(donnees.ARTICLES_WIKI)


@st.cache_data(ttl=86400, show_spinner=False)
def prix_paquet(code, magasin):
    return services.prix_paquet_reel(code, magasin)


@st.cache_data(ttl=3600, show_spinner="Chargement des recettes…")
def charger_recettes():
    photos = photos_plats()
    recettes, rid = [], 1
    for i in range(donnees.NB_VARIANTES):
        for nom, cat, temps, diff in donnees.BASE:
            suffixe = "" if i == 0 else (" maison" if i % 2 == 0 else " du Chef") + f" (variante {i + 1})"
            recettes.append({
                "id": rid, "nom": nom + suffixe, "base": nom, "categorie": cat,
                "image": donnees.PHOTOS_PERSO.get(nom) or photos.get(nom, ""),
                "temps": temps, "difficulte": diff,
                "ingredients": services.ingredients_a_jour(
                    donnees.FICHES[nom]["ingredients"], donnees.CODES_BARRES, prix_paquet),
            })
            rid += 1
    return recettes
