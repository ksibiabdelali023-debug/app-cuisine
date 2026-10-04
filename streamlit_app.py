import streamlit as st

st.set_page_config(page_title="MiamMiam", page_icon="🍳", layout="centered")

# =====================================================================
# IMAGES : photo par-dessus un visuel de secours (dégradé + emoji).
# Pour vos propres photos, collez une URL directe d'image ici :
# =====================================================================
PHOTOS_PERSO = {
    # "Salade Caprese": "https://.../ma-photo.jpg",
}
EMOJIS = {
    "Salade Caprese": "🍅", "Avocat au Thon": "🥑", "Velouté de Potimarron": "🎃",
    "Crevettes Mayo": "🍤", "Poulet au Curry et Riz": "🍛", "Pavé de Saumon Aneth": "🐟",
    "Spaghetti Bolognaise": "🍝", "Gratin Dauphinois": "🥔", "Fondant au Chocolat": "🍫",
    "Tarte aux Pommes": "🥧", "Mousse au Chocolat": "🍮", "Tiramisu Café": "☕",
}
DEGRADES = {
    "Entrée": "linear-gradient(135deg,#34D399,#A7F3D0)",
    "Plat": "linear-gradient(135deg,#FB923C,#FDBA74)",
    "Dessert": "linear-gradient(135deg,#F472B6,#FBCFE8)",
}
ICONES = {"Entrée": "🥗", "Plat": "🍝", "Dessert": "🍰"}

# =====================================================================
# FICHES DE PRÉPARATION (quantités pour 2 personnes)
# ingrédients : (quantité, unité, nom)
# =====================================================================
FICHES = {
    "Salade Caprese": {
        "ingredients": [(3, "", "tomates mûres"), (125, "g", "mozzarella"), (6, "", "feuilles de basilic"),
                        (2, "c. à soupe", "huile d'olive"), (1, "pincée", "sel et poivre")],
        "etapes": ["Lavez les tomates et coupez-les en rondelles de 5 mm.",
                   "Égouttez la mozzarella et coupez-la en tranches de même épaisseur.",
                   "Alternez tomates et mozzarella en les faisant se chevaucher sur une assiette.",
                   "Glissez les feuilles de basilic entre les tranches.",
                   "Arrosez d'huile d'olive, salez, poivrez et servez frais."],
        "astuce": "Sortez les tomates du frigo 30 minutes avant : elles auront bien plus de goût."},
    "Avocat au Thon": {
        "ingredients": [(2, "", "avocats mûrs"), (1, "boîte", "thon au naturel (160 g)"),
                        (2, "c. à soupe", "mayonnaise"), (1, "", "citron"), (1, "c. à café", "ciboulette")],
        "etapes": ["Coupez les avocats en deux et retirez le noyau.",
                   "Égouttez le thon et émiettez-le dans un bol.",
                   "Mélangez le thon avec la mayonnaise, un filet de jus de citron et la ciboulette.",
                   "Garnissez les moitiés d'avocat avec la préparation.",
                   "Servez bien frais avec un trait de citron."],
        "astuce": "Arrosez la chair d'avocat de citron pour éviter qu'elle noircisse."},
    "Velouté de Potimarron": {
        "ingredients": [(600, "g", "potimarron"), (1, "", "oignon"), (500, "ml", "bouillon de légumes"),
                        (10, "cl", "crème fraîche"), (1, "noix", "beurre")],
        "etapes": ["Lavez le potimarron (la peau se mange), retirez les graines et coupez-le en cubes.",
                   "Faites revenir l'oignon émincé dans le beurre 3 minutes.",
                   "Ajoutez le potimarron et le bouillon chaud, puis cuisez 20 minutes à frémissement.",
                   "Mixez finement en ajoutant la crème fraîche.",
                   "Rectifiez l'assaisonnement et servez chaud."],
        "astuce": "Une pincée de noix de muscade et quelques graines de courge torréfiées pour la finition."},
    "Crevettes Mayo": {
        "ingredients": [(250, "g", "crevettes décortiquées cuites"), (3, "c. à soupe", "mayonnaise"),
                        (1, "c. à café", "moutarde"), (0.5, "", "citron"), (4, "", "feuilles de salade")],
        "etapes": ["Décongelez les crevettes si besoin et épongez-les avec du papier absorbant.",
                   "Mélangez mayonnaise, moutarde et un peu de jus de citron.",
                   "Ajoutez les crevettes et enrobez-les délicatement.",
                   "Dressez sur un lit de salade et servez bien frais."],
        "astuce": "Ajoutez une pointe de paprika ou de piment d'Espelette dans la sauce."},
    "Poulet au Curry et Riz": {
        "ingredients": [(300, "g", "blanc de poulet"), (150, "g", "riz basmati"), (1, "", "oignon"),
                        (2, "c. à café", "curry en poudre"), (20, "cl", "crème ou lait de coco"),
                        (1, "c. à soupe", "huile")],
        "etapes": ["Coupez le poulet en dés et l'oignon en lamelles.",
                   "Faites dorer le poulet dans l'huile 5 minutes, réservez.",
                   "Faites revenir l'oignon, ajoutez le curry et mélangez 1 minute.",
                   "Remettez le poulet, versez la crème et laissez mijoter 15 minutes.",
                   "Pendant ce temps, cuisez le riz 10 à 12 minutes dans l'eau bouillante salée.",
                   "Servez le poulet sur le riz égoutté."],
        "astuce": "Rincez le riz basmati avant cuisson pour des grains bien séparés."},
    "Pavé de Saumon Aneth": {
        "ingredients": [(2, "", "pavés de saumon"), (1, "bouquet", "aneth"), (1, "", "citron"),
                        (1, "c. à soupe", "huile d'olive"), (1, "pincée", "sel et poivre")],
        "etapes": ["Préchauffez le four à 180 °C.",
                   "Posez les pavés sur une feuille de papier cuisson, huilez, salez et poivrez.",
                   "Recouvrez d'aneth ciselé et de rondelles de citron.",
                   "Fermez la papillote et enfournez 12 à 15 minutes.",
                   "Servez avec du riz ou des légumes vapeur."],
        "astuce": "Le saumon est cuit quand il se détache en pétales mais reste nacré au centre."},
    "Spaghetti Bolognaise": {
        "ingredients": [(200, "g", "spaghetti"), (250, "g", "bœuf haché"), (1, "", "oignon"),
                        (1, "", "carotte"), (400, "g", "tomates concassées"), (1, "gousse", "d'ail")],
        "etapes": ["Hachez finement l'oignon, la carotte et l'ail.",
                   "Faites-les revenir 5 minutes dans un filet d'huile.",
                   "Ajoutez la viande et faites-la dorer en l'émiettant.",
                   "Versez les tomates, salez, poivrez et laissez mijoter 25 minutes.",
                   "Cuisez les spaghetti dans l'eau bouillante salée selon le temps indiqué.",
                   "Mélangez les pâtes à la sauce et servez avec du fromage râpé."],
        "astuce": "Gardez un peu d'eau de cuisson des pâtes pour lier la sauce."},
    "Gratin Dauphinois": {
        "ingredients": [(800, "g", "pommes de terre"), (25, "cl", "crème liquide"), (25, "cl", "lait"),
                        (1, "gousse", "d'ail"), (60, "g", "emmental râpé"), (1, "noix", "beurre")],
        "etapes": ["Préchauffez le four à 160 °C et frottez un plat avec l'ail, puis beurrez-le.",
                   "Épluchez et coupez les pommes de terre en fines rondelles (sans les rincer).",
                   "Portez à frémissement lait et crème avec sel, poivre et muscade, puis plongez-y les pommes de terre 5 minutes.",
                   "Versez le tout dans le plat et parsemez d'emmental.",
                   "Enfournez 1 heure, jusqu'à ce que le dessus soit bien doré."],
        "astuce": "Ne rincez pas les pommes de terre : leur amidon rend le gratin onctueux."},
    "Fondant au Chocolat": {
        "ingredients": [(200, "g", "chocolat noir"), (100, "g", "beurre"), (100, "g", "sucre"),
                        (3, "", "œufs"), (40, "g", "farine")],
        "etapes": ["Préchauffez le four à 180 °C et beurrez un moule.",
                   "Faites fondre chocolat et beurre au bain-marie, puis laissez tiédir.",
                   "Fouettez les œufs avec le sucre, puis incorporez le chocolat.",
                   "Ajoutez la farine et mélangez jusqu'à obtenir une pâte lisse.",
                   "Versez dans le moule et enfournez 20 minutes (le centre doit rester coulant).",
                   "Laissez reposer 5 minutes avant de démouler."],
        "astuce": "Ne dépassez pas 20 minutes de cuisson pour garder un cœur fondant."},
    "Tarte aux Pommes": {
        "ingredients": [(1, "", "pâte brisée"), (4, "", "pommes"), (30, "g", "sucre"),
                        (1, "c. à soupe", "compote ou confiture"), (1, "noix", "beurre")],
        "etapes": ["Préchauffez le four à 180 °C et étalez la pâte dans un moule piqué à la fourchette.",
                   "Étalez la compote sur le fond.",
                   "Épluchez et coupez les pommes en fines lamelles.",
                   "Disposez-les en rosace, saupoudrez de sucre et ajoutez quelques noisettes de beurre.",
                   "Enfournez 35 à 40 minutes jusqu'à ce que les bords soient dorés."],
        "astuce": "Badigeonnez les pommes de confiture tiède à la sortie du four pour un effet brillant."},
    "Mousse au Chocolat": {
        "ingredients": [(150, "g", "chocolat pâtissier"), (4, "", "œufs"), (20, "g", "sucre"),
                        (1, "pincée", "de sel")],
        "etapes": ["Faites fondre le chocolat au bain-marie ou au micro-ondes, puis laissez tiédir.",
                   "Séparez les blancs des jaunes et incorporez les jaunes au chocolat.",
                   "Montez les blancs en neige ferme avec le sel, en ajoutant le sucre à la fin.",
                   "Incorporez les blancs au chocolat en 3 fois, délicatement.",
                   "Répartissez en verrines et réfrigérez au moins 4 heures."],
        "astuce": "Mélangez avec une spatule en soulevant la masse pour garder la mousse aérienne."},
    "Tiramisu Café": {
        "ingredients": [(250, "g", "mascarpone"), (2, "", "œufs"), (50, "g", "sucre"),
                        (12, "", "biscuits boudoirs"), (15, "cl", "café fort froid"), (1, "c. à soupe", "cacao en poudre")],
        "etapes": ["Séparez les blancs des jaunes. Fouettez les jaunes avec le sucre jusqu'à blanchiment.",
                   "Ajoutez le mascarpone et mélangez jusqu'à obtenir une crème lisse.",
                   "Montez les blancs en neige et incorporez-les délicatement.",
                   "Trempez rapidement les boudoirs dans le café et tapissez-en le fond d'un plat.",
                   "Étalez la moitié de la crème, ajoutez une couche de boudoirs, puis le reste de crème.",
                   "Réfrigérez 6 heures et saupoudrez de cacao avant de servir."],
        "astuce": "Préparez-le la veille : le goût n'en sera que meilleur."},
}

# ---------- STYLE ----------
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem; max-width: 760px;}

    .hero {background: linear-gradient(135deg,#FF6B35 0%,#F7931E 55%,#FFC145 100%);
           border-radius: 22px; padding: 26px 22px; color: white; margin-bottom: 18px;
           box-shadow: 0 8px 24px rgba(255,107,53,.30);}
    .hero h1 {margin:0; font-size:2rem; color:white; padding:0;}
    .hero p {margin:6px 0 0 0; opacity:.95;}

    .stTabs [data-baseweb="tab-list"] {gap:6px; background:#FFF4EC; padding:6px; border-radius:16px;}
    .stTabs [data-baseweb="tab"] {flex:1; justify-content:center; padding:10px 6px;
           border-radius:12px; font-weight:700; font-size:14px; background:transparent;}
    .stTabs [aria-selected="true"] {background:#FF6B35 !important; color:white !important;}
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display:none;}

    div[data-testid="stVerticalBlockBorderWrapper"] {border-radius:18px; border:1px solid #F1E3D8;
           box-shadow:0 4px 14px rgba(0,0,0,.06);}

    .visuel {position:relative; overflow:hidden; border-radius:14px; display:flex;
             align-items:center; justify-content:center;}
    .visuel .emo {font-size:56px;}
    .visuel .photo {position:absolute; inset:0; background-size:cover; background-position:center;}

    .chip {display:inline-block; background:#FFF4EC; color:#C2410C; border-radius:20px;
           padding:3px 10px; font-size:12px; font-weight:700; margin:0 6px 4px 0;}
    .prix {color:#16A34A; font-weight:800; font-size:15px; margin-bottom:6px;}
    .titre {font-weight:800; font-size:16px; margin:8px 0 4px 0; line-height:1.25;}

    .stButton > button {border-radius:12px; font-weight:700; width:100%; padding:10px 0;}
    .stButton > button[kind="primary"] {background:#FF6B35; border:none;}
    .stButton > button[kind="primary"]:hover {background:#E85A28;}

    .badge {padding:6px 12px; border-radius:10px; color:white; font-weight:700;
            display:inline-block; font-size:13px; margin:2px 4px 8px 0;}
    .gagnant {background:linear-gradient(135deg,#16A34A,#4ADE80); border-radius:18px;
              padding:18px; color:white; text-align:center; font-size:1.05rem; margin:12px 0;}

    .etape {display:flex; gap:12px; margin:10px 0; align-items:flex-start;}
    .etape .num {flex:0 0 32px; height:32px; border-radius:50%; background:#FF6B35; color:white;
                 font-weight:800; display:flex; align-items:center; justify-content:center;}
    .etape .txt {padding-top:4px; line-height:1.45;}
    .astuce {background:#FFF9E6; border-left:5px solid #FFC145; border-radius:10px;
             padding:12px 14px; margin-top:14px;}
</style>
""", unsafe_allow_html=True)

# ---------- ÉTAT ----------
st.session_state.setdefault("selection", [])
st.session_state.setdefault("nb_affiche", 8)
st.session_state.setdefault("filtre_precedent", None)

# ---------- DONNÉES ----------
@st.cache_data
def charger_recettes():
    # (nom, catégorie, mot-clé photo, temps, difficulté, [(ingrédient, prix Leclerc, prix Lidl)])
    base = [
        ("Salade Caprese", "Entrée", "caprese", "10 min", "Facile",
         [("Tomates Marque Repère", 1.20, 1.40), ("Mozzarella Marque Repère", 1.50, 1.30)]),
        ("Avocat au Thon", "Entrée", "avocado", "10 min", "Facile",
         [("Avocat Rose de France", 1.80, 1.95), ("Thon entier Marque Repère", 2.10, 1.90)]),
        ("Velouté de Potimarron", "Entrée", "pumpkin,soup", "30 min", "Facile",
         [("Potimarron", 2.50, 2.20), ("Crème Fraîche Marque Repère", 1.10, 1.25)]),
        ("Crevettes Mayo", "Entrée", "shrimp", "15 min", "Facile",
         [("Crevettes décortiquées", 4.50, 4.20), ("Mayonnaise Marque Repère", 1.30, 1.45)]),
        ("Poulet au Curry et Riz", "Plat", "chicken,curry", "35 min", "Moyen",
         [("Blanc de Poulet Marque Repère", 6.50, 5.90), ("Riz Basmati Marque Repère", 1.40, 1.20)]),
        ("Pavé de Saumon Aneth", "Plat", "salmon", "20 min", "Facile",
         [("Pavé de Saumon Atlantique", 8.90, 8.40), ("Citron jaune", 0.60, 0.50)]),
        ("Spaghetti Bolognaise", "Plat", "spaghetti", "40 min", "Facile",
         [("Pâtes Spaghetti Marque Repère", 0.80, 0.75), ("Bœuf Haché Marque Repère", 5.20, 5.50)]),
        ("Gratin Dauphinois", "Plat", "gratin", "1 h 15", "Moyen",
         [("Pommes de terre", 2.10, 1.90), ("Emmental râpé Marque Repère", 1.80, 1.60)]),
        ("Fondant au Chocolat", "Dessert", "chocolate,cake", "25 min", "Moyen",
         [("Chocolat Noir Marque Repère", 1.40, 1.20), ("Beurre Marque Repère", 1.90, 1.75)]),
        ("Tarte aux Pommes", "Dessert", "apple,pie", "50 min", "Moyen",
         [("Pommes", 2.30, 2.10), ("Pâte Brisée Marque Repère", 1.10, 0.95)]),
        ("Mousse au Chocolat", "Dessert", "chocolate,mousse", "20 min", "Facile",
         [("Chocolat Pâtissier Marque Repère", 1.40, 1.20), ("Œufs Marque Repère", 2.10, 2.30)]),
        ("Tiramisu Café", "Dessert", "tiramisu", "30 min", "Moyen",
         [("Mascarpone Marque Repère", 2.80, 2.50), ("Biscuits Boudoirs", 1.50, 1.35)]),
    ]
    recettes, rid = [], 1
    for i in range(85):
        for nom, cat, kw, temps, diff, ings in base:
            suffixe = "" if i == 0 else (" maison" if i % 2 == 0 else " du Chef") + f" (Variante {i + 1})"
            recettes.append({
                "id": rid, "nom": nom + suffixe, "base": nom, "categorie": cat,
                "image": PHOTOS_PERSO.get(nom, f"https://loremflickr.com/640/420/{kw},food?lock={rid}"),
                "temps": temps, "difficulte": diff, "ingredients": ings,
            })
            rid += 1
    return recettes

RECETTES = charger_recettes()
PAR_ID = {r["id"]: r for r in RECETTES}


def visuel(r, hauteur=170):
    """Photo par-dessus un dégradé + emoji : si la photo échoue, le visuel de secours reste visible."""
    return (f'<div class="visuel" style="height:{hauteur}px;background:{DEGRADES[r["categorie"]]}">'
            f'<span class="emo">{EMOJIS[r["base"]]}</span>'
            f'<div class="photo" style="background-image:url(\'{r["image"]}\')"></div></div>')


def cout(r, magasin, coef=1.0):
    idx = 1 if magasin == "leclerc" else 2
    return sum(i[idx] for i in r["ingredients"]) * coef


def basculer(rid):
    if rid in st.session_state.selection:
        st.session_state.selection.remove(rid)
    else:
        st.session_state.selection.append(rid)


# ---------- FICHE RECETTE (fenêtre) ----------
@st.dialog("Fiche recette", width="large")
def fiche(rid):
    r = PAR_ID[rid]
    f = FICHES[r["base"]]
    st.markdown(visuel(r, 200), unsafe_allow_html=True)
    st.markdown(f'<div class="titre" style="font-size:22px">{r["nom"]}</div>'
                f'<span class="chip">{ICONES[r["categorie"]]} {r["categorie"]}</span>'
                f'<span class="chip">⏱ {r["temps"]}</span>'
                f'<span class="chip">{r["difficulte"]}</span>', unsafe_allow_html=True)

    personnes = st.number_input("👥 Nombre de personnes", 1, 12, 2, key=f"pers_{rid}")
    coef = personnes / 2

    st.markdown("### 🧺 Ingrédients")
    for qte, unite, nom in f["ingredients"]:
        q = f"{qte * coef:g}"
        texte = f"{q} {unite} {nom}".replace(" ", " ").strip()
        # « g » / « ml » / « cl » collés au nom avec « de »
        if unite in ("g", "ml", "cl"):
            texte = f"{q} {unite} de {nom}" if nom[0] not in "aeiouhéèêœ" else f"{q} {unite} d'{nom}"
        st.markdown(f"- {texte}")

    st.markdown("### 👩‍🍳 Préparation")
    for n, etape in enumerate(f["etapes"], 1):
        st.markdown(f'<div class="etape"><div class="num">{n}</div><div class="txt">{etape}</div></div>',
                    unsafe_allow_html=True)
    st.markdown(f'<div class="astuce">💡 <b>Astuce du chef :</b> {f["astuce"]}</div>', unsafe_allow_html=True)

    st.markdown(f"**Budget estimé (ingrédients principaux) :** Leclerc {cout(r, 'leclerc', coef):.2f} € · "
                f"Lidl {cout(r, 'lidl', coef):.2f} €")

    if rid in st.session_state.selection:
        if st.button("✅ Dans mon panier · Retirer", key=f"dlg_{rid}"):
            basculer(rid)
            st.rerun()
    else:
        if st.button("❤️ Ajouter au panier", key=f"dlg_{rid}", type="primary"):
            basculer(rid)
            st.rerun()


# ---------- EN-TÊTE ----------
st.markdown("""
<div class="hero">
    <h1>🍳 MiamMiam</h1>
    <p>Choisissez vos recettes, comparez Leclerc et Lidl, économisez sur vos courses.</p>
</div>
""", unsafe_allow_html=True)

nb = len(st.session_state.selection)
t1, t2, t3 = st.tabs(["📖 Recettes", f"❤️ Panier ({nb})", "🛒 Courses"])

# ---------- RECETTES ----------
with t1:
    recherche = st.text_input("Recherche", placeholder="🔍 Poulet, chocolat, salade…",
                              label_visibility="collapsed")
    choix = st.radio("Catégorie", ["Tous", "🥗 Entrée", "🍝 Plat", "🍰 Dessert"],
                     horizontal=True, label_visibility="collapsed")
    cat = choix.split(" ")[-1] if choix != "Tous" else "Tous"
    tri = st.selectbox("Trier par", ["Par défaut", "Prix croissant", "Plus rapides"],
                       label_visibility="collapsed")

    signature = (recherche, cat, tri)
    if signature != st.session_state.filtre_precedent:
        st.session_state.nb_affiche = 8
        st.session_state.filtre_precedent = signature

    resultats = [r for r in RECETTES
                 if (cat == "Tous" or r["categorie"] == cat)
                 and recherche.lower() in r["nom"].lower()]
    if tri == "Prix croissant":
        resultats.sort(key=lambda r: min(cout(r, "leclerc"), cout(r, "lidl")))
    elif tri == "Plus rapides":
        resultats.sort(key=lambda r: int(r["temps"].split()[0]) * (60 if "h" in r["temps"] else 1))

    if not resultats:
        st.warning("Aucune recette ne correspond à votre recherche.")
    else:
        st.caption(f"{len(resultats)} recettes")
        visibles = resultats[:st.session_state.nb_affiche]
        for debut in range(0, len(visibles), 2):
            cols = st.columns(2)
            for col, r in zip(cols, visibles[debut:debut + 2]):
                with col, st.container(border=True):
                    st.markdown(
                        visuel(r) +
                        f'<div class="titre">{r["nom"]}</div>'
                        f'<span class="chip">{ICONES[r["categorie"]]} {r["categorie"]}</span>'
                        f'<span class="chip">⏱ {r["temps"]}</span>'
                        f'<span class="chip">{r["difficulte"]}</span>'
                        f'<div class="prix">dès {min(cout(r, "leclerc"), cout(r, "lidl")):.2f} €</div>',
                        unsafe_allow_html=True)
                    if st.button("📖 Voir la recette", key=f"fi{r['id']}"):
                        fiche(r["id"])
                    if r["id"] in st.session_state.selection:
                        st.button("✅ Ajoutée · Retirer", key=f"t{r['id']}",
                                  on_click=basculer, args=(r["id"],))
                    else:
                        st.button("❤️ Ajouter", key=f"t{r['id']}", type="primary",
                                  on_click=basculer, args=(r["id"],))

        if len(resultats) > st.session_state.nb_affiche:
            if st.button("⬇️ Voir plus de recettes"):
                st.session_state.nb_affiche += 8
                st.rerun()

# ---------- PANIER ----------
with t2:
    st.subheader("Mes recettes")
    sel = [PAR_ID[i] for i in st.session_state.selection]
    if not sel:
        st.info("Votre panier est vide. Ajoutez des recettes depuis l'onglet 📖.")
    else:
        for r in sel:
            with st.container(border=True):
                c1, c2 = st.columns([1, 2])
                c1.markdown(visuel(r, 90), unsafe_allow_html=True)
                c2.markdown(f'<div class="titre">{r["nom"]}</div>'
                            f'<span class="chip">⏱ {r["temps"]}</span>'
                            f'<span class="chip">{r["categorie"]}</span>', unsafe_allow_html=True)
                if c2.button("📖 Voir la recette", key=f"fp{r['id']}"):
                    fiche(r["id"])
                c2.button("🗑 Retirer", key=f"p{r['id']}", on_click=basculer, args=(r["id"],))
        st.button("Vider le panier", on_click=lambda: st.session_state.selection.clear())

# ---------- COURSES ----------
with t3:
    sel = [PAR_ID[i] for i in st.session_state.selection]
    if not sel:
        st.info("Sélectionnez des recettes pour comparer les prix.")
    else:
        personnes = st.number_input("👥 Nombre de personnes (prix de base : 2)", 1, 12, 2)
        coef = personnes / 2

        tot_lec = sum(cout(r, "leclerc", coef) for r in sel)
        tot_lid = sum(cout(r, "lidl", coef) for r in sel)

        m1, m2 = st.columns(2)
        m1.metric("🟦 Leclerc", f"{tot_lec:.2f} €")
        m2.metric("🟨 Lidl", f"{tot_lid:.2f} €")

        diff = abs(tot_lec - tot_lid)
        gagnant = "Leclerc (Marque Repère)" if tot_lec < tot_lid else "Lidl"
        if diff > 0.005:
            st.markdown(f'<div class="gagnant">🌟 Allez chez <b>{gagnant}</b><br>'
                        f'et économisez <b>{diff:.2f} €</b></div>', unsafe_allow_html=True)
        else:
            st.info("Prix identiques dans les deux enseignes.")

        lignes, total_mix = [], 0.0
        for r in sel:
            for ing, p_lec, p_lid in r["ingredients"]:
                meilleur, mag = (p_lec, "Leclerc") if p_lec <= p_lid else (p_lid, "Lidl")
                prix = meilleur * coef
                total_mix += prix
                lignes.append(f"[ ] {ing} — {mag} — {prix:.2f} €")
        gain_mix = min(tot_lec, tot_lid) - total_mix
        if gain_mix > 0.005:
            st.caption(f"💡 En achetant chaque article dans l'enseigne la moins chère, "
                       f"vous paieriez {total_mix:.2f} € (encore {gain_mix:.2f} € d'économie).")
        st.download_button("📥 Télécharger ma liste de courses",
                           "\n".join(lignes) + f"\n\nTotal : {total_mix:.2f} €",
                           file_name="liste_courses.txt", mime="text/plain")

        st.subheader("Détail par recette")
        for r in sel:
            with st.expander(f"{ICONES[r['categorie']]} {r['nom']}"):
                for ing, p_lec, p_lid in r["ingredients"]:
                    c_lec = "#16A34A" if p_lec <= p_lid else "#DC2626"
                    c_lid = "#16A34A" if p_lid <= p_lec else "#DC2626"
                    st.markdown(
                        f"**{ing}**<br>"
                        f'<span class="badge" style="background:{c_lec}">Leclerc {p_lec * coef:.2f} €</span>'
                        f'<span class="badge" style="background:{c_lid}">Lidl {p_lid * coef:.2f} €</span>',
                        unsafe_allow_html=True)
