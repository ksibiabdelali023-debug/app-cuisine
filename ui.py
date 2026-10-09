"""Composants d'interface réutilisables : visuel, pastilles, carte recette, fiche détaillée."""
from datetime import date

import streamlit as st

import etat, planning
from calculs import cout, format_prix, ligne_ingredient, prix_minimum
from donnees import CAT, DEGRADES, EMOJIS, FICHES


def injecter_style_ui():
    """Injecte les styles CSS haut de gamme pour les cartes et les badges."""
    st.markdown("""
        <style>
        /* Conteneur global de la carte recette */
        .recette-card {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 0px;
            margin-bottom: 8px;
            overflow: hidden;
        }
        
        /* Conteneur de l'image ou du dégradé de secours */
        .visuel-container {
            width: 100%;
            position: relative;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 12px;
        }
        
        .photo-bloc {
            width: 100%;
            background-size: cover;
            background-position: center;
            transition: transform 0.3s ease;
        }
        .visuel-container:hover .photo-bloc {
            transform: scale(1.03);
        }
        
        /* Emojis géants centrés en fond */
        .emoji-secours {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 48px;
            z-index: 1;
        }
        
        /* Style des titres de recettes */
        .recette-titre {
            font-size: 20px;
            font-weight: 700;
            color: #1F2937;
            margin: 8px 0 6px 0;
            line-height: 1.2;
        }
        
        /* Flexbox pour l'alignement des badges */
        .badges-wrapper {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin: 6px 0 12px 0;
        }
        
        /* Badges génériques arrondis */
        .badge-premium {
            padding: 4px 10px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
        }
        
        /* Déclinaisons colorimétriques des badges */
        .badge-premium.halal { background-color: #E6F4EA; color: #137333; }
        .badge-premium.c-entree { background-color: #E6F4EA; color: #059669; }
        .badge-premium.c-plat { background-color: #FFEDD5; color: #D97706; }
        .badge-premium.c-dessert { background-color: #FCE7F3; color: #DB2777; }
        .badge-premium.typ { background-color: #F3F4F6; color: #4B5563; }
        .badge-premium.tps { background-color: #E0F2FE; color: #0284C7; }
        .badge-premium.dif { background-color: #F3E8FF; color: #7C3AED; }
        
        /* Affichage de la tarification */
        .prix-premium-box {
            background-color: #ECFDF5;
            color: #065F46;
            font-weight: 700;
            font-size: 14.5px;
            padding: 8px 14px;
            border-radius: 10px;
            display: inline-block;
            margin-bottom: 14px;
            border: 1px dashed #A7F3D0;
        }
        
        /* Encarts informatifs de la fiche détaillée */
        .astuce-box {
            background-color: #F0FDF4;
            border-left: 4px solid #16A34A;
            padding: 12px;
            border-radius: 4px 12px 12px 4px;
            margin: 12px 0;
            color: #166534;
        }
        .halal-box {
            background-color: #EFF6FF;
            border-left: 4px solid #2563EB;
            padding: 12px;
            border-radius: 4px 12px 12px 4px;
            margin: 12px 0;
            color: #1E40AF;
        }
        
        /* Forcer le bouton Streamlit primaire à être vert émeraude */
        div.stButton > button[kind="primary"] {
            background-color: #10B981 !important;
            border-color: #10B981 !important;
            color: white !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #059669 !important;
            border-color: #059669 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def visuel(r, hauteur=170):
    """Photo posée sur un visuel de secours dégradé avec effet de zoom au survol."""
    base = r["base"]
    photo_html = ""
    alt_text = f"Illustration du plat : {base}"
    
    if r.get("image"):
        alt_text = f"Photo du plat : {base}"
        photo_html = f'<div class="photo-bloc" style="height:{hauteur}px; background-image:url(\'{r["image"]}\'); position:relative; z-index:2;"></div>'
        
    return f"""
    <div class="visuel-container" role="img" aria-label="{alt_text}" style="height:{hauteur}px; background:{DEGRADES[r["categorie"]]};">
        <span class="emoji-secours" aria-hidden="true">{EMOJIS[base]}</span>
        {photo_html}
    </div>
    """


def pastilles(r):
    """Génère la structure HTML des badges sous forme de liste épurée."""
    cat = r["categorie"]
    type_html = f'<span class="badge-premium typ">{r["type"]}</span>' if r.get("type") else ""
    
    return f"""
    <div class="badges-wrapper">
        <span class="badge-premium halal"><span aria-hidden="true">✔ </span>Halal</span>
        <span class="badge-premium c-{CAT[cat]}">{cat}</span>
        {type_html}
        <span class="badge-premium tps">⏱ {r["temps"]}</span>
        <span class="badge-premium dif">📊 {r["difficulte"]}</span>
    </div>
    """


def annonce_html():
    texte = st.session_state.get("annonce", "")
    return f'<div class="sr-only" role="status" aria-live="polite">{texte}</div>'


def bouton_panier(r, cle, court=False):
    rid, nom = r["id"], r["nom"]
    if rid in st.session_state.selection:
        st.button("✖ Retirer" if court else f"Retirer du panier : {nom}", key=cle,
                  help=f"Retirer du panier : {nom}", on_click=etat.basculer, args=(rid, nom))
    else:
        st.button("🛒 Ajouter" if court else f"Ajouter au panier : {nom}", key=cle, type="primary",
                  help=f"Ajouter au panier : {nom}", on_click=etat.basculer, args=(rid, nom))


def carte_recette(r, contexte):
    injecter_style_ui()
    rid, nom = r["id"], r["nom"]
    
    with st.container(border=True):
        if contexte == "panier":
            c = etat.coef(rid)
            prix_html = (f'<div class="prix-premium-box">Pour {etat.personnes(rid)} pers. : Leclerc '
                         f'{format_prix(cout(r["ingredients"], "leclerc", c))} · Lidl '
                         f'{format_prix(cout(r["ingredients"], "lidl", c))}</div>')
        else:
            prix_html = f'<div class="prix-premium-box">🏷️ À partir de {format_prix(prix_minimum(r))} pour 2 personnes</div>'
            
        # Affichage structuré sans les blocs marron natifs
        st.markdown(
            f'<div class="recette-card">'
            f'{visuel(r)}'
            f'<div class="recette-titre">{nom}</div>'
            f'{pastilles(r)}'
            f'{prix_html}'
            f'</div>',
            unsafe_allow_html=True
        )
        
        if contexte == "panier":
            etat.champ_personnes(rid, "pn_", f"Nombre de personnes pour {nom}")
            
        b1, b2 = st.columns(2)
        with b1:
            st.button("📖 Voir la recette", key=f"voir_{contexte}_{rid}", help=f"Voir la recette : {nom}", on_click=ouvrir_fiche, args=(r,))
        with b2:
            bouton_panier(r, f"pan_{contexte}_{rid}", court=True)


def _corps_fiche(r):
    injecter_style_ui()
    rid = r["id"]
    f = FICHES[r["base"]]
    
    st.markdown(visuel(r, 220), unsafe_allow_html=True)
    if r.get("image"):
        st.caption("📷 Source photo : Wikipédia / Wikimedia Commons")
    st.markdown(pastilles(r), unsafe_allow_html=True)

    etat.champ_personnes(rid, "pers_", "Nombre de parts (personnes) :")
    c = etat.coef(rid)

    st.subheader("📋 Ingrédients requis")
    st.markdown("\n".join(f"- {ligne_ingredient(q * c, u, n)}" for q, u, n, _, _ in r["ingredients"]))
    st.caption("💡 Le sel, le poivre et les huiles de cuisson de base sont supposés présents dans votre placard.")

    st.subheader("🍳 Étapes de préparation")
    st.markdown("\n".join(f"**{i}.** {e}" for i, e in enumerate(f["etapes"], 1)))
    
    st.markdown(f'<div class="astuce-box">💡 <b>Astuce du chef :</b> {f["astuce"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="halal-box">🛡️ <b>Conseil Halal :</b> {f["halal"]}</div>', unsafe_allow_html=True)

    st.success(f"💰 **Budget total pour {etat.personnes(rid)} personnes :** "
               f"Leclerc **{format_prix(cout(r['ingredients'], 'leclerc', c))}** | "
               f"Lidl **{format_prix(cout(r['ingredients'], 'lidl', c))}**")

    bouton_panier(r, f"dlg_{rid}")
    
    st.subheader("📅 Planifier ce repas")
    col_d, col_r = st.columns(2)
    with col_d:
        st.date_input("Choisir le jour", value=date.today(), format="DD/MM/YYYY", key=f"plan_jour_{rid}")
    with col_r:
        st.selectbox("Choisir le moment", planning.REPAS, key=f"plan_repas_{rid}")
        
    st.button("✨ Ajouter au planning de la semaine", key=f"plan_ajout_{rid}", on_click=etat.planifier_depuis_fiche,
              args=(rid, r["nom"]), type="primary")
              
    if st.button("Fermer la fiche", key=f"fer_{rid}"):
        st.rerun()
        
    st.markdown(annonce_html(), unsafe_allow_html=True)


def ouvrir_fiche(r):
    @st.dialog(r["nom"], width="large")
    def _fiche():
        _corps_fiche(r)
    _fiche()
