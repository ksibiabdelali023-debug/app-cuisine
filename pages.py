import re
from datetime import date
import streamlit as st
import etat
import planning
import ressources
from calculs import (agreger, correspond_filtre, format_prix, grouper_par_rayon, ligne_ingredient, meilleur_mixte,
                      meilleure_enseigne, minutes, cout, prix_minimum, texte_liste, totaux)
from donnees import CATEGORIES, CODES_BARRES, FILTRES, ICONES_CATEGORIES
from ui import carte_recette

def injecter_style_premium():
    st.markdown("""
        <style>
        .mcard {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            margin-bottom: 12px;
        }
        .mcard span {
            display: block;
            font-size: 14px;
            color: #6B7280;
            margin-bottom: 4px;
        }
        .mcard b {
            font-size: 22px;
            color: #111827;
        }
        .gagnant {
            background-color: #ECFDF5;
            border: 1px solid #10B981;
            color: #065F46;
            padding: 14px;
            border-radius: 12px;
            margin: 16px 0;
            font-size: 15px;
        }
        .titre-rayon {
            font-size: 18px;
            font-weight: 600;
            color: #374151;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 2px solid #E5E7EB;
            padding-bottom: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

def _pills(libelle, options, defaut, cle, format_func=str):
    choix = st.pills(libelle, options, selection_mode="single", default=defaut, key=cle, format_func=format_func)
    return choix or defaut

def page_recettes(recettes):
    injecter_style_premium()
    recherche = st.text_input("Rechercher une recette", placeholder="Poulet, chocolat, salade…")
    trouvees = [r for r in recettes if recherche.lower() in r["nom"].lower()]
    compteurs = {lib: sum(1 for r in trouvees if cat is None or r["categorie"] == cat) for lib, cat in CATEGORIES.items()}
    choix = _pills("Catégorie", list(CATEGORIES), "Toutes", "pills_categorie", lambda k: f"{ICONES_CATEGORIES[k]} {k} ({compteurs[k]})")
    filtre = _pills("Type de plat", list(FILTRES), "Tous", "pills_type")
    tri = st.selectbox("Trier par", ["Ordre habituel", "Prix croissant", "Plus rapides"])
    signature = (recherche, choix, filtre, tri)
    if signature != st.session_state.filtre_precedent:
        st.session_state.nb_affiche = 8
        st.session_state.filtre_precedent = signature
    cat = CATEGORIES[choix]
    resultats = [r for r in trouvees if (cat is None or r["categorie"] == cat) and correspond_filtre(r, filtre)]
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
    injecter_style_premium()
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
    injecter_style_premium()
    st.header("Mes courses")
    sel = [par_id[i] for i in st.session_state.selection]
    if not sel:
        st.info("Ajoutez des recettes au panier pour comparer les prix.")
        return
    tot_lec, tot_lid = totaux(sel, etat.coef)
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="mcard"><span>Total Leclerc</span><b>{format_prix(tot_lec)}</b></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="mcard"><span>Total Lidl</span><b>{format_prix(tot_lid)}</b></div>', unsafe_allow_html=True)
    gagnant, ecart = meilleure_enseigne(tot_lec, tot_lid)
    if gagnant:
        st.markdown(f'<div class="gagnant" role="status"><b>✨ L\'enseigne la moins chère : {gagnant}</b><br>Vous économisez {format_prix(ecart)} en faisant toutes vos courses dans ce magasin.</div>', unsafe_allow_html=True)
    else:
        st.info("Les prix globaux sont identiques dans les deux enseignes.")
    agg = agreger(sel, etat.coef)
    mixte = meilleur_mixte(agg)
    gain = min(tot_lec, tot_lid) - mixte
    if gain > 0.005:
        st.success(f"💡 **Optimisation** : En achetant chaque ingrédient individuellement là où il est le moins cher, votre total descend à **{format_prix(mixte)}** (soit **{format_prix(gain)}** d'économie supplémentaire).")
    st.caption(f"Prix : {len(CODES_BARRES)} ingrédient(s) liés à Open Prices (relevés réels mis à jour toutes les 24h) ; les autres sont des estimations basées sur le marché moyen.")
    st.button("🔄 Actualiser les prix maintenant", on_click=st.cache_data.clear)
    with st.expander("⚙️ Changer le nombre de personnes global"):
        st.number_input("Nombre de personnes", 1, 12, 2, key="global_pers")
        st.button("Appliquer à toutes les recettes", on_click=etat.appliquer_a_toutes)
    groupes = grouper_par_rayon(agg)
    nb_articles = sum(len(lignes) for _, lignes in groupes)
    st.subheader(f"📋 Liste de courses ({nb_articles} articles)")
    cles = []
    for rayon, lignes in groupes:
        st.markdown(f'<div class="titre-rayon">{rayon}</div>', unsafe_allow_html=True)
        for nom, unite, q, p_lec, p_lid in lignes:
            cle = "coche_" + re.sub(r"\W+", "_", f"{nom}_{unite}")
            cles.append(cle)
            mag = "Leclerc" if p_lec <= p_lid else "Lidl"
            st.checkbox(f"{ligne_ingredient(q, unite, nom)} (Leclerc: {format_prix(p_lec)} | Lidl: {format_prix(p_lid)}) • Moins cher chez : {mag}", key=cle)
    coches = sum(1 for k in cles if st.session_state.get(k))
    st.progress(coches / len(cles) if cles else 0.0, text=f"{coches} sur {len(cles)} articles cochés")
    st.download_button("💾 Télécharger la liste (.txt)", texte_liste(groupes), file_name="liste_courses.txt", mime="text/plain")
    st.subheader("🔍 Détail par recette")
    for r in sel:
        rid = r["id"]
        with st.expander(f"{r['nom']} ({r.get('base', '')}) : {etat.personnes(rid)} personnes"):
            st.number_input("Ajuster les parts", 1, 12, value=int(etat.personnes(rid)), key=f"c_{rid}")
            c = etat.coef(rid)
            for q, u, n, p_lec, p_lid in r["ingredients"]:
                st.write(f"• {ligne_ingredient(q * c, u, n)} : Leclerc {format_prix(p_lec * c)} | Lidl {format_prix(p_lid * c)}")

def page_planning(recettes, par_id):
    injecter_style_premium()
    st.header("Planning des repas")
    debut = st.session_state.semaine_debut
    jours = planning.semaine(debut)
    plan = st.session_state.planning
    n1, n2, n3 = st.columns(3)
    n1.button("◀ Précédente", on_click=etat.changer_semaine, args=(-7,), key="sem_prec")
    n2.button("Aujourd'hui", on_click=etat.changer_semaine, args=(0,), key="sem_auj")
    n3.button("Suivante ▶", on_click=etat.changer_semaine, args=(7,), key="sem_suiv")
    st.markdown(f'<h3 style="text-align:center; color:#374151;">Semaine du {planning.libelle_jour(jours)} au {planning.libelle_jour(jours[-1])}</h3>', unsafe_allow_html=True)
    ids_sem = planning.ids_semaine(plan, debut)
    if ids_sem:
        lec, lid = totaux([par_id[i] for i in ids_sem], etat.coef)
        st.caption(f"📊 {len(ids_sem)} recette(s) planifiée(s). Estimation : Leclerc {format_prix(lec)} • Lidl {format_prix(lid)}")
        st.button("🛒 Transférer le planning dans le panier", type="primary", on_click=etat.planning_vers_panier, key="plan_vers_panier")
    else:
        st.info("Aucune recette planifiée. Cliquez sur un jour ci-dessous pour composer vos repas.")
    options = {r["id"]: r for r in recettes if r["nom"] == r["base"]}
    for rid in st.session_state.selection:
        options.setdefault(rid, par_id[rid])
    aujourdhui = date.today()
    for jour in jours:
        iso = jour.isoformat()
        prefixe_titre = "📅 " + planning.libelle_jour(jour)
        if jour == aujourdhui:
            prefixe_titre += " (Aujourd'hui)"
        with st.expander(prefixe_titre):
            repas_du_jour = planning.ids_du_jour(plan, iso)
            st.write(f"Recettes planifiées : {len(repas_du_jour)}")
            for rid in repas_du_jour:
                if rid in par_id:
                    col_txt, col_btn = st.columns(2)
                    col_txt.write(f"🍽️ {par_id[rid]['nom']}")
                    if col_btn.button("Retirer", key=f"del_{iso}_{rid}"):
                        if iso in st.session_state.planning:
                            st.session_state.planning[iso].remove(rid)
                            st.rerun()
            liste_noms = ["-- Ajouter un repas --"] + [options[rid]["nom"] for rid in options]
            selection_repas = st.selectbox("Choisir une recette à ajouter", options=liste_noms, key=f"add_select_{iso}")
            if selection_repas != "-- Ajouter un repas --":
                for rid, r_info in options.items():
                    if r_info["nom"] == selection_repas:
