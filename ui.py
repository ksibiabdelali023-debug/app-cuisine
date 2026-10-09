"""Composants d'interface réutilisables : visuel, pastilles, carte recette, fiche détaillée."""
from datetime import date

import streamlit as st

import etat, planning
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
    type_ = f'<span class="chip typ">{r["type"]}</span>' if r.get("type") else ""
    return ('<span class="chip halal"><span aria-hidden="true">✔ </span>Halal</span>'
            f'<span class="chip c-{CAT[cat]}">{cat}</span>' + type_ +
            f'<span class="chip tps">Temps : {r["temps"]}</span>'
            f'<span class="chip dif">Difficulté : {r["difficulte"]}</span>')


def annonce_html():
    texte = st.session_state.get("annonce", "")
    return f'<div class="sr-only" role="status" aria-live="polite">{texte}</div>'


def bouton_panier(r, cle, court=False):
    """court=True : libellé compact pour les cartes (le nom du plat est dans l'infobulle)."""
    rid, nom = r["id"], r["nom"]
    if rid in st.session_state.selection:
        st.button("✖ Retirer" if court else f"Retirer du panier : {nom}", key=cle,
                  help=f"Retirer du panier : {nom}", on_click=etat.basculer, args=(rid, nom))
    else:
        st.button("🛒 Ajouter" if court else f"Ajouter au panier : {nom}", key=cle, type="primary",
                  help=f"Ajouter au panier : {nom}", on_click=etat.basculer, args=(rid, nom))


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
        b1, b2 = st.columns(2)
        with b1:
            if st.button("📖 Voir la recette", key=f"voir_{contexte}_{rid}", help=f"Voir la recette : {nom}"):
                ouvrir_fiche(r)
        with b2:
            bouton_panier(r, f"pan_{contexte}_{rid}", court=True)


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
    st.subheader("Planifier ce plat")
    st.date_input("Jour", value=date.today(), format="DD/MM/YYYY", key=f"plan_jour_{rid}")
    st.selectbox("Repas", planning.REPAS, key=f"plan_repas_{rid}")
    st.button("📅 Ajouter au planning", key=f"plan_ajout_{rid}", on_click=etat.planifier_depuis_fiche,
              args=(rid, r["nom"]))
    if st.button("Fermer la fiche et actualiser la page", key=f"fer_{rid}"):
        st.rerun()
    st.markdown(annonce_html(), unsafe_allow_html=True)


def ouvrir_fiche(r):
    @st.dialog(r["nom"], width="large")
    def _fiche():
        _corps_fiche(r)
    _fiche()
