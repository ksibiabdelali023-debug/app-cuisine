"""Composants d'interface réutilisables : visuel, pastilles, carte recette, fiche détaillée."""
import streamlit as st

import etat
from calculs import cout, format_prix, ligne_ingredient, prix_minimum
from donnees import CAT, DEGRADES, EMOJIS, FICHES


def visuel(r, hauteur=170):
    """Photo (si disponible) posée sur un visuel de secours. Le bloc a une alternative textuelle."""
    base = r["base"]
    if r["image"]:
        alt = "Photo du plat : " + base
        photo = '<div class="photo" style="background-image:url(\'' + r["image"] + '\')"></div>'
    else:
        alt = "Illustration du plat : " + base
        photo = ""
    return ('<div class="visuel" role="img" aria-label="' + alt + '" style="height:' + str(hauteur)
            + 'px;background:' + DEGRADES[r["categorie"]] + '"><span class="emo" aria-hidden="true">'
            + EMOJIS[base] + "</span>" + photo + "</div>")


def pastilles(r):
    cat = r["categorie"]
    return ('<span class="chip halal"><span aria-hidden="true">✔ </span>Halal</span>'
            f'<span class="chip c-{CAT[cat]}">{cat}</span>'
            f'<span class="chip tps">Temps : {r["temps"]}</span>'
            f'<span class="chip dif">Difficulté : {r["difficulte"]}</span>')


def annonce_html():
    texte = st.session_state.get("annonce", "")
    return f'<div class="sr-only" role="status" aria-live="polite">{texte}</div>'


def bouton_panier(r, cle, dialogue=False):
    rid, nom = r["id"], r["nom"]
    if rid in st.session_state.selection:
        st.button(f"Retirer du panier : {nom}", key=cle, on_click=etat.basculer, args=(rid, nom))
    else:
        st.button(f"Ajouter au panier : {nom}", key=cle, type="primary",
                  on_click=etat.basculer, args=(rid, nom))


def carte_recette(r, contexte):
    rid, nom = r["id"], r["nom"]
    with st.container(border=True):
        if contexte == "panier":
            c = etat.coef(rid)
            prix = (f'<span class="prix">Pour {etat.personnes(rid)} pers. : Leclerc '
                    f'{format_prix(cout(r["ingredients"], "leclerc", c))} · Lidl '
                    f'{format_prix(cout(r["ingredients"], "lidl", c))}</span>')
        else:
            prix = f'<span class="prix">À partir de {format_prix(prix_minimum(r))} pour 2 personnes</span>'
        st.markdown(visuel(r) + f'<h3 class="titre">{nom}</h3>' + pastilles(r) + "<br>" + prix,
                    unsafe_allow_html=True)
        if contexte == "panier":
            etat.champ_personnes(rid, "pn_", f"Nombre de personnes pour {nom}")
        if st.button(f"Voir la recette : {nom}", key=f"voir_{contexte}_{rid}"):
            ouvrir_fiche(r)
        bouton_panier(r, f"pan_{contexte}_{rid}")


def _corps_fiche(r):
    rid = r["id"]
    f = FICHES[r["base"]]
    st.markdown(visuel(r, 220), unsafe_allow_html=True)
    if r["image"]:
        st.caption("Photo : Wikipédia / Wikimedia Commons")
    st.markdown(pastilles(r), unsafe_allow_html=True)

    etat.champ_personnes(rid, "pers_", "Nombre de personnes")
    c = etat.coef(rid)

    st.subheader("Ingrédients")
    st.markdown("\n".join(f"- {ligne_ingredient(q * c, u, n)}" for q, u, n, _, _ in r["ingredients"]))
    st.caption("Sel, poivre et épices de base à compléter selon votre placard.")

    st.subheader("Préparation")
    st.markdown("\n".join(f"{i}. {e}" for i, e in enumerate(f["etapes"], 1)))
    st.markdown(f'<div class="astuce"><b>Astuce du chef :</b> {f["astuce"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="halalbox"><b>Conseil halal :</b> {f["halal"]}</div>', unsafe_allow_html=True)

    st.markdown(f"**Budget estimé pour {etat.personnes(rid)} personnes :** "
                f"Leclerc {format_prix(cout(r['ingredients'], 'leclerc', c))}, "
                f"Lidl {format_prix(cout(r['ingredients'], 'lidl', c))}.")

    bouton_panier(r, f"dlg_{rid}")
    if st.button("Fermer la fiche et actualiser la page", key=f"fer_{rid}"):
        st.rerun()
    st.markdown(annonce_html(), unsafe_allow_html=True)


def ouvrir_fiche(r):
    @st.dialog(r["nom"], width="large")
    def _fiche():
        _corps_fiche(r)
    _fiche()
