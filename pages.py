"""Les trois vues de l'application : Recettes, Panier, Courses."""
import re

import streamlit as st

import etat, ressources
from calculs import (agreger, correspond_filtre, format_prix, grouper_par_rayon, ligne_ingredient, meilleur_mixte,
                      meilleure_enseigne, minutes, cout, prix_minimum, texte_liste, totaux)
from donnees import CATEGORIES, CODES_BARRES, FILTRES, ICONES_CATEGORIES
from ui import carte_recette


def _pills(libelle, options, defaut, cle, format_func=str):
    """Boutons-pastilles faciles à toucher sur mobile ; revient à la valeur par défaut si on désélectionne."""
    choix = st.pills(libelle, options, selection_mode="single", default=defaut, key=cle,
                     format_func=format_func)
    return choix or defaut


def page_recettes(recettes):
    recherche = st.text_input("Rechercher une recette", placeholder="Poulet, chocolat, salade…")
    trouvees = [r for r in recettes if recherche.lower() in r["nom"].lower()]
    compteurs = {lib: sum(1 for r in trouvees if cat is None or r["categorie"] == cat)
                 for lib, cat in CATEGORIES.items()}
    choix = _pills("Catégorie", list(CATEGORIES), "Toutes", "pills_categorie",
                   lambda k: f"{ICONES_CATEGORIES[k]} {k} ({compteurs[k]})")
    filtre = _pills("Type de plat", list(FILTRES), "Tous", "pills_type")
    tri = st.selectbox("Trier par", ["Ordre habituel", "Prix croissant", "Plus rapides"])

    signature = (recherche, choix, filtre, tri)
    if signature != st.session_state.filtre_precedent:
        st.session_state.nb_affiche = 8
        st.session_state.filtre_precedent = signature

    cat = CATEGORIES[choix]
    resultats = [r for r in trouvees
                 if (cat is None or r["categorie"] == cat) and correspond_filtre(r, filtre)]
    if tri == "Prix croissant":
        resultats.sort(key=prix_minimum)
    elif tri == "Plus rapides":
        resultats.sort(key=lambda r: minutes(r["temps"]))

    if not resultats:
        st.warning("Aucune recette ne correspond à votre recherche.")
        return

    n = len(resultats)
    st.caption(f"{n} recette{'s' if n > 1 else ''} trouvée{'s' if n > 1 else ''}. Prix pour 2 personnes.")
    for r in resultats[:st.session_state.nb_affiche]:
        carte_recette(r, "liste")

    reste = n - st.session_state.nb_affiche
    if reste > 0:
        if st.button(f"Afficher {min(8, reste)} recettes de plus ({reste} restantes)"):
            st.session_state.nb_affiche += 8
            st.rerun()


def page_panier(par_id):
    st.header("Mon panier")
    sel = [par_id[i] for i in st.session_state.selection]
    if not sel:
        st.info("Votre panier est vide. Ajoutez des recettes depuis l'onglet Recettes.")
        return
    for r in sel:
        carte_recette(r, "panier")
    st.divider()
    if st.session_state.confirmer_vidage:
        st.warning("Voulez-vous vraiment vider tout le panier ?")
        st.button("Oui, vider le panier", type="primary", on_click=etat.vider_panier)
        st.button("Non, garder mon panier", on_click=etat.annuler_vidage)
    else:
        st.button("Vider le panier", on_click=etat.demander_vidage)


def page_courses(par_id):
    st.header("Mes courses")
    sel = [par_id[i] for i in st.session_state.selection]
    if not sel:
        st.info("Ajoutez des recettes au panier pour comparer les prix.")
        return

    tot_lec, tot_lid = totaux(sel, etat.coef)
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="mcard leclerc"><span>Total Leclerc</span><b>{format_prix(tot_lec)}</b></div>',
                unsafe_allow_html=True)
    c2.markdown(f'<div class="mcard lidl"><span>Total Lidl</span><b>{format_prix(tot_lid)}</b></div>',
                unsafe_allow_html=True)

    gagnant, ecart = meilleure_enseigne(tot_lec, tot_lid)
    if gagnant:
        st.markdown(f'<div class="gagnant" role="status"><b>Le moins cher : {gagnant}</b><br>'
                    f'Vous économisez {format_prix(ecart)} en achetant tout là-bas.</div>',
                    unsafe_allow_html=True)
    else:
        st.info("Les prix sont identiques dans les deux enseignes.")

    agg = agreger(sel, etat.coef)
    mixte = meilleur_mixte(agg)
    gain = min(tot_lec, tot_lid) - mixte
    if gain > 0.005:
        st.write(f"En achetant chaque article dans l'enseigne la moins chère, vous paieriez "
                 f"{format_prix(mixte)}, soit encore {format_prix(gain)} d'économie.")

    st.caption(f"Prix : {len(CODES_BARRES)} ingrédient(s) liés à Open Prices (relevés réels, mis à jour "
               "toutes les 24 h) ; les autres sont des estimations.")
    st.button("Actualiser les prix maintenant", on_click=st.cache_data.clear)

    with st.expander("Changer le nombre de personnes pour toutes les recettes"):
        st.number_input("Nombre de personnes", 1, 12, 2, key="global_pers")
        st.button("Appliquer à toutes les recettes", on_click=etat.appliquer_a_toutes)

    # Liste de courses à cocher, classée par rayon
    groupes = grouper_par_rayon(agg)
    nb_articles = sum(len(lignes) for _, lignes in groupes)
    st.subheader(f"Liste de courses : {nb_articles} articles")
    cles = []
    for rayon, lignes in groupes:
        st.markdown(f'<h3 class="titre">{rayon}</h3>', unsafe_allow_html=True)
        for nom, unite, q, p_lec, p_lid in lignes:
            cle = "coche_" + re.sub(r"\W+", "_", f"{nom}_{unite}")
            cles.append(cle)
            mag = "Leclerc" if p_lec <= p_lid else "Lidl"
            st.checkbox(f"{ligne_ingredient(q, unite, nom)} : Leclerc {format_prix(p_lec)}, "
                        f"Lidl {format_prix(p_lid)}. Moins cher : {mag}.", key=cle)
    coches = sum(1 for k in cles if st.session_state.get(k))
    st.progress(coches / len(cles) if cles else 0.0, text=f"{coches} sur {len(cles)} articles cochés")

    st.download_button("Télécharger la liste de courses (texte)", texte_liste(groupes),
                       file_name="liste_courses.txt", mime="text/plain")

    st.subheader("Détail par recette")
    for r in sel:
        rid = r["id"]
        with st.expander(f"{r['nom']} : {etat.personnes(rid)} personnes"):
            etat.champ_personnes(rid, "c_", f"Nombre de personnes pour {r['nom']}")
            c = etat.coef(rid)
            for q, u, n, p_lec, p_lid in r["ingredients"]:
                st.write(f"{ligne_ingredient(q * c, u, n)} : Leclerc {format_prix(p_lec * c)}, "
                         f"Lidl {format_prix(p_lid * c)}")
