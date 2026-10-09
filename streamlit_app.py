import re
from datetime import date
import streamlit as st
import etat
import ressources
import planning
from calculs import (agreger, correspond_filtre, format_prix, grouper_par_rayon, ligne_ingredient, meilleur_mixte,
                      meilleure_enseigne, minutes, cout, prix_minimum, texte_liste, totaux)
from donnees import BASE, CATEGORIES, CODES_BARRES, FILTRES, ICONES_CATEGORIES, CAT, DEGRADES, EMOJIS, FICHES

# 1. Configuration de la page
st.set_page_config(
    page_title="MiamMiam - Recettes Halal & Comparateur",
    page_icon="🍳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Initialisation de l'état
if "selection" not in st.session_state: st.session_state.selection = []
if "planning" not in st.session_state: st.session_state.planning = {}
if "semaine_debut" not in st.session_state:
    import datetime
    st.session_state.semaine_debut = datetime.date.today()
if "filtre_precedent" not in st.session_state: st.session_state.filtre_precedent = (None, None, None, None)
if "nb_affiche" not in st.session_state: st.session_state.nb_affiche = 8
if "confirmer_vidage" not in st.session_state: st.session_state.confirmer_vidage = False

# 3. Injection du Design Premium (Interface Moderne)
st.markdown("""
    <style>
    .stApp { background-color: #F9FAFB; }
    .recette-card { background-color: #FFFFFF; border-radius: 16px; padding: 0px; margin-bottom: 8px; overflow: hidden; }
    .visuel-container { width: 100%; position: relative; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 12px; }
    .photo-bloc { width: 100%; background-size: cover; background-position: center; transition: transform 0.3s ease; }
    .visuel-container:hover .photo-bloc { transform: scale(1.03); }
    .emoji-secours { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 48px; z-index: 1; }
    .recette-titre { font-size: 20px; font-weight: 700; color: #1F2937; margin: 8px 0 6px 0; line-height: 1.2; }
    
    .badges-wrapper { display: flex; flex-wrap: wrap; gap: 6px; margin: 6px 0 12px 0; }
    .badge-premium { padding: 4px 10px; border-radius: 30px; font-size: 12px; font-weight: 600; display: inline-flex; align-items: center; }
    .badge-premium.halal { background-color: #E6F4EA; color: #137333; }
    .badge-premium.c-entree { background-color: #E6F4EA; color: #059669; }
    .badge-premium.c-plat { background-color: #FFEDD5; color: #D97706; }
    .badge-premium.c-dessert { background-color: #FCE7F3; color: #DB2777; }
    .badge-premium.typ { background-color: #F3F4F6; color: #4B5563; }
    .badge-premium.tps { background-color: #E0F2FE; color: #0284C7; }
    .badge-premium.dif { background-color: #F3E8FF; color: #7C3AED; }
    
    .prix-premium-box { background-color: #ECFDF5; color: #065F46; font-weight: 700; font-size: 14.5px; padding: 8px 14px; border-radius: 10px; display: inline-block; margin-bottom: 14px; border: 1px dashed #A7F3D0; }
    .mcard { background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 16px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 12px; }
    .mcard span { display: block; font-size: 14px; color: #6B7280; margin-bottom: 4px; }
    .mcard b { font-size: 22px; color: #111827; }
    .gagnant { background-color: #ECFDF5; border: 1px solid #10B981; color: #065F46; padding: 14px; border-radius: 12px; margin: 16px 0; font-size: 15px; }
    .titre-rayon { font-size: 18px; font-weight: 600; color: #374151; margin-top: 20px; margin-bottom: 10px; border-bottom: 2px solid #E5E7EB; padding-bottom: 4px; }
    .astuce-box { background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 12px; border-radius: 4px 12px 12px 4px; margin: 12px 0; color: #166534; }
    .halal-box { background-color: #EFF6FF; border-left: 4px solid #2563EB; padding: 12px; border-radius: 4px 12px 12px 4px; margin: 12px 0; color: #1E40AF; }
    
    div.stButton > button[kind="primary"] { background-color: #10B981 !important; border-color: #10B981 !important; color: white !important; border-radius: 8px !important; }
    div.stButton > button[kind="primary"]:hover { background-color: #059669 !important; border-color: #059669 !important; }
    div.stButton > button[kind="secondary"] { border-radius: 8px !important; }
    </style>
""", unsafe_allow_html=True)

# Bannière supérieure
st.markdown("""
    <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 24px; border-radius: 16px; text-align: center; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 800;">MiamMiam 🍳</h1>
        <p style="color: #E0F2FE; margin: 8px 0 0 0; font-size: 14px;">Recettes 100% Halal • Comparez Leclerc et Lidl</p>
    </div>
""", unsafe_allow_html=True)

# 4. Visuels & Cartes sécurisés (.get() pour parer aux KeyErrors)
def generer_visuel_html(r, hauteur=170):
    base = r["base"]
    # Sécurité si la catégorie ou l'emoji n'existe pas exactement
    couleur_fond = DEGRADES.get(r["categorie"], "linear-gradient(135deg, #E5E7EB, #9CA3AF)")
    emoji_plat = EMOJIS.get(base, "🍽️")
    photo_html = f'<div class="photo-bloc" style="height:{hauteur}px; background-image:url(\'{r["image"]}\'); position:relative; z-index:2;"></div>' if r.get("image") else ""
    return f'<div class="visuel-container" style="height:{hauteur}px; background:{couleur_fond};"><span class="emoji-secours">{emoji_plat}</span>{photo_html}</div>'

def generer_pastilles_html(r):
    cat = r["categorie"]
    code_cat = CAT.get(cat, "plat")
    type_html = f'<span class="badge-premium typ">{r["type"]}</span>' if r.get("type") else ""
    return f'<div class="badges-wrapper"><span class="badge-premium halal">✔ Halal</span><span class="badge-premium c-{code_cat}">{cat}</span>{type_html}<span class="badge-premium tps">⏱ {r["temps"]}</span><span class="badge-premium dif">📊 {r["difficulte"]}</span></div>'

def bouton_panier_integre(r, cle, court=False):
    rid, nom = r["id"], r["nom"]
    if rid in st.session_state.selection:
        st.button("✖ Retirer" if court else f"Retirer : {nom}", key=cle, on_click=etat.basculer, args=(rid, nom))
    else:
        st.button("🛒 Ajouter" if court else f"Ajouter : {nom}", key=cle, type="primary", on_click=etat.basculer, args=(rid, nom))

def afficher_carte_recette(r, contexte):
    rid, nom = r["id"], r["nom"]
    with st.container(border=True):
        if contexte == "panier":
            c = etat.coef(rid)
            prix_html = f'<div class="prix-premium-box">Pour {etat.personnes(rid)} pers. : Leclerc {format_prix(cout(r["ingredients"], "leclerc", c))} · Lidl {format_prix(cout(r["ingredients"], "lidl", c))}</div>'
        else:
            prix_html = f'<div class="prix-premium-box">🏷️ À partir de {format_prix(prix_minimum(r))} pour 2 personnes</div>'
            
        st.markdown(f'<div class="recette-card">{generer_visuel_html(r)}<div class="recette-titre">{nom}</div>{generer_pastilles_html(r)}{prix_html}</div>', unsafe_allow_html=True)
        
        if contexte == "panier":
            st.number_input("Nombre de personnes", 1, 12, value=int(etat.personnes(rid)), key=f"pn_{rid}")
            
        b1, b2 = st.columns(2)
        with b1:
            st.button("📖 Voir la recette", key=f"voir_{contexte}_{rid}", on_click=ouvrir_fiche_dialog, args=(r,))
        with b2:
            bouton_panier_integre(r, f"pan_{contexte}_{rid}", court=True)

def _corps_fiche_dialog(r):
    rid = r["id"]
    f = FICHES.get(r["base"], {"etapes": [], "astuce": "Aucune astuce", "halal": "Vérifier les étiquettes"})
    st.markdown(generer_visuel_html(r, 220), unsafe_allow_html=True)
    st.markdown(generer_pastilles_html(r), unsafe_allow_html=True)
    st.number_input("Nombre de parts :", 1, 12, value=int(etat.personnes(rid)), key=f"pers_{rid}")
    c = etat.coef(rid)
    st.subheader("📋 Ingrédients")
    st.markdown("\n".join(f"- {ligne_ingredient(q * c, u, n)}" for q, u, n, _, _ in r["ingredients"]))
    st.subheader("🍳 Préparation")
    st.markdown("\n".join(f"**{i}.** {e}" for i, e in enumerate(f["etapes"], 1)))
    st.markdown(f'<div class="astuce-box">💡 <b>Astuce :</b> {f["astuce"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="halal-box">🛡️ <b>Conseil Halal :</b> {f["halal"]}</div>', unsafe_allow_html=True)
    st.success(f"💰 Leclerc: **{format_prix(cout(r['ingredients'], 'leclerc', c))}** | Lidl: **{format_prix(cout(r['ingredients'], 'lidl', c))}**")
    bouton_panier_integre(r, f"dlg_{rid}")

def ouvrir_fiche_dialog(r):
    @st.dialog(r["nom"], width="large")
    def _fiche(): _corps_fiche_dialog(r)
    _fiche()

# 5. Traitement sécurisé des données initiales
recettes_structurees = []
recettes_par_id = {}
for idx, item in enumerate(BASE):
    if isinstance(item, tuple):
        nom, categorie, temps, diff = item
        fiche = FICHES.get(nom, {"ingredients": [], "etapes": [], "astuce": "", "halal": ""})
        r_dict = {"id": str(idx), "nom": nom, "base": nom, "categorie": categorie, "temps": temps, "difficulte": diff, "ingredients": fiche["ingredients"], "image": None, "type": "Plat"}
    else:
        r_dict = item
        if "id" not in r_dict: r_dict["id"] = str(idx)
        if "base" not in r_dict: r_dict["base"] = r_dict["nom"]
        if "image" not in r_dict: r_dict["image"] = None
        if "type" not in r_dict: r_dict["type"] = "Plat"
    recettes_structurees.append(r_dict)
    recettes_par_id[r_dict["id"]] = r_dict

# 6. Vues internes sécurisées
def _pills(libelle, options, defaut, cle, format_func=str):
    return st.pills(libelle, options, selection_mode="single", default=defaut, key=cle, format_func=format_func) or defaut

def vue_recettes(recettes):
    recherche = st.text_input("Rechercher une recette", placeholder="Poulet, chocolat, salade…")
    trouvees = [r for r in recettes if recherche.lower() in r["nom"].lower()]
