import re
import statistics
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests
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
# RECETTES 100 % HALAL (sans porc, sans alcool, sans gélatine animale)
# Ingrédients pour 2 personnes : (quantité, unité, nom, prix Leclerc, prix Lidl)
# Les prix sont indicatifs et correspondent à la quantité utilisée.
# Le sel, le poivre et les épices de base ne sont pas comptés.
# =====================================================================
FICHES = {
    "Salade Caprese": {
        "ingredients": [
            (3, "", "tomates mûres", 1.20, 1.40),
            (125, "g", "mozzarella à présure végétale", 1.50, 1.30),
            (1, "pot", "basilic frais", 1.10, 0.99),
            (2, "c. à soupe", "huile d'olive", 0.35, 0.30)],
        "etapes": ["Lavez les tomates et coupez-les en rondelles de 5 mm.",
                   "Égouttez la mozzarella et coupez-la en tranches de même épaisseur.",
                   "Alternez tomates et mozzarella en les faisant se chevaucher sur une assiette.",
                   "Glissez les feuilles de basilic entre les tranches.",
                   "Arrosez d'huile d'olive, salez, poivrez et servez frais."],
        "astuce": "Sortez les tomates du frigo 30 minutes avant : elles auront bien plus de goût.",
        "halal": "Choisissez une mozzarella à présure végétale (ou certifiée halal)."},
    "Avocat au Thon": {
        "ingredients": [
            (2, "", "avocats mûrs", 1.80, 1.95),
            (1, "boîte", "thon au naturel (160 g)", 2.10, 1.90),
            (2, "c. à soupe", "mayonnaise", 0.30, 0.35),
            (1, "", "citron", 0.60, 0.50),
            (1, "pot", "ciboulette", 0.90, 0.85)],
        "etapes": ["Coupez les avocats en deux et retirez le noyau.",
                   "Égouttez le thon et émiettez-le dans un bol.",
                   "Mélangez le thon avec la mayonnaise, un filet de jus de citron et la ciboulette.",
                   "Garnissez les moitiés d'avocat avec la préparation.",
                   "Servez bien frais avec un trait de citron."],
        "astuce": "Arrosez la chair d'avocat de citron pour éviter qu'elle noircisse.",
        "halal": "Lisez l'étiquette de la mayonnaise : sans alcool ni additif d'origine animale douteuse."},
    "Velouté de Potimarron": {
        "ingredients": [
            (600, "g", "potimarron", 2.50, 2.20),
            (1, "", "oignon", 0.25, 0.20),
            (500, "ml", "bouillon de légumes", 0.40, 0.35),
            (10, "cl", "crème fraîche", 1.10, 1.25),
            (1, "noix", "beurre", 0.15, 0.14)],
        "etapes": ["Lavez le potimarron (la peau se mange), retirez les graines et coupez-le en cubes.",
                   "Faites revenir l'oignon émincé dans le beurre 3 minutes.",
                   "Ajoutez le potimarron et le bouillon chaud, puis cuisez 20 minutes à frémissement.",
                   "Mixez finement en ajoutant la crème fraîche.",
                   "Rectifiez l'assaisonnement et servez chaud."],
        "astuce": "Une pincée de noix de muscade et quelques graines de courge torréfiées pour la finition.",
        "halal": "Vérifiez que le bouillon est 100 % végétal (sans arôme d'origine porcine)."},
    "Crevettes Mayo": {
        "ingredients": [
            (250, "g", "crevettes décortiquées cuites", 4.50, 4.20),
            (3, "c. à soupe", "mayonnaise", 1.30, 1.45),
            (1, "c. à café", "moutarde", 0.15, 0.12),
            (1, "", "citron", 0.60, 0.50),
            (1, "", "salade (cœur de laitue)", 0.90, 0.80)],
        "etapes": ["Décongelez les crevettes si besoin et épongez-les avec du papier absorbant.",
                   "Mélangez mayonnaise, moutarde et un peu de jus de citron.",
                   "Ajoutez les crevettes et enrobez-les délicatement.",
                   "Dressez sur un lit de salade et servez bien frais."],
        "astuce": "Ajoutez une pointe de paprika ou de piment d'Espelette dans la sauce.",
        "halal": "Les crevettes sont admises par la plupart des écoles juridiques : référez-vous à la vôtre."},
    "Poulet au Curry et Riz": {
        "ingredients": [
            (300, "g", "blanc de poulet halal", 6.50, 5.90),
            (150, "g", "riz basmati", 1.40, 1.20),
            (1, "", "oignon", 0.25, 0.20),
            (2, "c. à café", "curry en poudre", 0.60, 0.55),
            (20, "cl", "crème liquide", 1.20, 1.10),
            (1, "c. à soupe", "huile", 0.15, 0.12)],
        "etapes": ["Coupez le poulet en dés et l'oignon en lamelles.",
                   "Faites dorer le poulet dans l'huile 5 minutes, réservez.",
                   "Faites revenir l'oignon, ajoutez le curry et mélangez 1 minute.",
                   "Remettez le poulet, versez la crème et laissez mijoter 15 minutes.",
                   "Pendant ce temps, cuisez le riz 10 à 12 minutes dans l'eau bouillante salée.",
                   "Servez le poulet sur le riz égoutté."],
        "astuce": "Rincez le riz basmati avant cuisson pour des grains bien séparés.",
        "halal": "Poulet certifié halal (abattage rituel) : rayon halal ou boucherie halal."},
    "Pavé de Saumon Aneth": {
        "ingredients": [
            (2, "", "pavés de saumon", 8.90, 8.40),
            (1, "bouquet", "aneth", 1.20, 0.99),
            (1, "", "citron", 0.60, 0.50),
            (1, "c. à soupe", "huile d'olive", 0.20, 0.18)],
        "etapes": ["Préchauffez le four à 180 °C.",
                   "Posez les pavés sur une feuille de papier cuisson, huilez, salez et poivrez.",
                   "Recouvrez d'aneth ciselé et de rondelles de citron.",
                   "Fermez la papillote et enfournez 12 à 15 minutes.",
                   "Servez avec du riz ou des légumes vapeur."],
        "astuce": "Le saumon est cuit quand il se détache en pétales mais reste nacré au centre.",
        "halal": "Poisson : aucune contrainte particulière."},
    "Spaghetti Bolognaise": {
        "ingredients": [
            (200, "g", "spaghetti", 0.80, 0.75),
            (250, "g", "bœuf haché halal", 5.20, 5.50),
            (1, "", "oignon", 0.25, 0.20),
            (1, "", "carotte", 0.20, 0.18),
            (400, "g", "tomates concassées", 0.95, 0.85),
            (1, "gousse", "ail", 0.15, 0.15)],
        "etapes": ["Hachez finement l'oignon, la carotte et l'ail.",
                   "Faites-les revenir 5 minutes dans un filet d'huile.",
                   "Ajoutez la viande et faites-la dorer en l'émiettant.",
                   "Versez les tomates, salez, poivrez et laissez mijoter 25 minutes.",
                   "Cuisez les spaghetti dans l'eau bouillante salée selon le temps indiqué.",
                   "Mélangez les pâtes à la sauce et servez avec du fromage râpé."],
        "astuce": "Gardez un peu d'eau de cuisson des pâtes pour lier la sauce.",
        "halal": "Bœuf haché certifié halal ; ni vin rouge ni lardons dans la sauce."},
    "Gratin Dauphinois": {
        "ingredients": [
            (800, "g", "pommes de terre", 2.10, 1.90),
            (25, "cl", "crème liquide", 1.30, 1.20),
            (25, "cl", "lait", 0.30, 0.28),
            (1, "gousse", "ail", 0.15, 0.15),
            (60, "g", "emmental râpé à présure végétale", 1.80, 1.60),
            (1, "noix", "beurre", 0.15, 0.14)],
        "etapes": ["Préchauffez le four à 160 °C et frottez un plat avec l'ail, puis beurrez-le.",
                   "Épluchez et coupez les pommes de terre en fines rondelles (sans les rincer).",
                   "Portez à frémissement lait et crème avec sel, poivre et muscade, puis plongez-y les pommes de terre 5 minutes.",
                   "Versez le tout dans le plat et parsemez d'emmental.",
                   "Enfournez 1 heure, jusqu'à ce que le dessus soit bien doré."],
        "astuce": "Ne rincez pas les pommes de terre : leur amidon rend le gratin onctueux.",
        "halal": "Emmental à présure végétale ; pas de lardons ni de jambon."},
    "Fondant au Chocolat": {
        "ingredients": [
            (200, "g", "chocolat noir", 1.40, 1.20),
            (100, "g", "beurre", 1.90, 1.75),
            (100, "g", "sucre", 0.15, 0.13),
            (3, "", "œufs", 0.90, 0.95),
            (40, "g", "farine", 0.05, 0.05)],
        "etapes": ["Préchauffez le four à 180 °C et beurrez un moule.",
                   "Faites fondre chocolat et beurre au bain-marie, puis laissez tiédir.",
                   "Fouettez les œufs avec le sucre, puis incorporez le chocolat.",
                   "Ajoutez la farine et mélangez jusqu'à obtenir une pâte lisse.",
                   "Versez dans le moule et enfournez 20 minutes (le centre doit rester coulant).",
                   "Laissez reposer 5 minutes avant de démouler."],
        "astuce": "Ne dépassez pas 20 minutes de cuisson pour garder un cœur fondant.",
        "halal": "Chocolat sans alcool ni liqueur (pas de rhum ni de Grand Marnier)."},
    "Tarte aux Pommes": {
        "ingredients": [
            (1, "", "pâte brisée pur beurre", 1.10, 0.95),
            (4, "", "pommes", 2.30, 2.10),
            (30, "g", "sucre", 0.05, 0.05),
            (1, "c. à soupe", "compote de pommes", 0.20, 0.18),
            (1, "noix", "beurre", 0.15, 0.14)],
        "etapes": ["Préchauffez le four à 180 °C et étalez la pâte dans un moule piqué à la fourchette.",
                   "Étalez la compote sur le fond.",
                   "Épluchez et coupez les pommes en fines lamelles.",
                   "Disposez-les en rosace, saupoudrez de sucre et ajoutez quelques noisettes de beurre.",
                   "Enfournez 35 à 40 minutes jusqu'à ce que les bords soient dorés."],
        "astuce": "Badigeonnez les pommes de confiture tiède à la sortie du four pour un effet brillant.",
        "halal": "Pâte brisée pur beurre (certaines contiennent du saindoux) ; pas de calvados."},
    "Mousse au Chocolat": {
        "ingredients": [
            (150, "g", "chocolat pâtissier", 1.40, 1.20),
            (4, "", "œufs", 2.10, 2.30),
            (20, "g", "sucre", 0.03, 0.03)],
        "etapes": ["Faites fondre le chocolat au bain-marie ou au micro-ondes, puis laissez tiédir.",
                   "Séparez les blancs des jaunes et incorporez les jaunes au chocolat.",
                   "Montez les blancs en neige ferme avec une pincée de sel, en ajoutant le sucre à la fin.",
                   "Incorporez les blancs au chocolat en 3 fois, délicatement.",
                   "Répartissez en verrines et réfrigérez au moins 4 heures."],
        "astuce": "Mélangez avec une spatule en soulevant la masse pour garder la mousse aérienne.",
        "halal": "Chocolat sans alcool ; aucune gélatine animale."},
    "Tiramisu Café": {
        "ingredients": [
            (250, "g", "mascarpone à présure végétale", 2.80, 2.50),
            (2, "", "œufs", 0.90, 1.00),
            (50, "g", "sucre", 0.08, 0.07),
            (12, "", "biscuits boudoirs", 1.50, 1.35),
            (15, "cl", "café fort", 0.20, 0.18),
            (1, "c. à soupe", "cacao en poudre", 0.15, 0.14)],
        "etapes": ["Séparez les blancs des jaunes. Fouettez les jaunes avec le sucre jusqu'à blanchiment.",
                   "Ajoutez le mascarpone et mélangez jusqu'à obtenir une crème lisse.",
                   "Montez les blancs en neige et incorporez-les délicatement.",
                   "Trempez rapidement les boudoirs dans le café froid et tapissez-en le fond d'un plat.",
                   "Étalez la moitié de la crème, ajoutez une couche de boudoirs, puis le reste de crème.",
                   "Réfrigérez 6 heures et saupoudrez de cacao avant de servir."],
        "astuce": "Préparez-le la veille : le goût n'en sera que meilleur.",
        "halal": "Pas de marsala ni d'amaretto : café seul. Boudoirs sans gélatine ni alcool."},
}

# =====================================================================
# PRIX RÉELS (Open Prices / Open Food Facts : base ouverte, prix relevés par la communauté)
# Leclerc et Lidl ne proposent pas d'API publique de prix : on passe par Open Prices.
# Pour chaque ingrédient, indiquez le code-barres du produit dans chaque enseigne et la
# taille du paquet (dans la même unité que la recette). Sans code, le prix estimé est gardé.
# Exemple :
#   "blanc de poulet halal": {"leclerc": ("3000000000000", 600), "lidl": ("4000000000000", 600)},
# Les codes-barres sont à trouver sur prices.openfoodfacts.org ou sur l'emballage.
# =====================================================================
CODES_BARRES = {}
API_PRIX = "https://prices.openfoodfacts.org/api/v1/prices"


@st.cache_data(ttl=86400, show_spinner=False)
def prix_paquet_reel(code, magasin):
    """Médiane des 10 derniers prix en euros relevés dans l'enseigne pour ce code-barres."""
    try:
        rep = requests.get(API_PRIX, params={"product_code": code, "order_by": "-date", "size": 50},
                           timeout=8)
        rep.raise_for_status()
        valeurs = []
        for p in rep.json().get("items", []):
            lieu = p.get("location") or {}
            nom_lieu = f"{lieu.get('osm_name', '')} {lieu.get('osm_brand', '')}".lower()
            if p.get("currency") == "EUR" and p.get("price") and magasin in nom_lieu:
                valeurs.append(float(p["price"]))
        return round(statistics.median(valeurs[:10]), 2) if valeurs else None
    except Exception:
        return None  # réseau ou format inattendu : on garde le prix estimé


def ingredients_a_jour(nom_recette):
    """Ingrédients de la fiche, avec les prix réels quand un code-barres est renseigné."""
    resultat = []
    for qte, unite, nom, p_lec, p_lid in FICHES[nom_recette]["ingredients"]:
        codes = CODES_BARRES.get(nom, {})
        prix = []
        for magasin, estime in (("leclerc", p_lec), ("lidl", p_lid)):
            if magasin in codes:
                code, taille_paquet = codes[magasin]
                paquet = prix_paquet_reel(code, magasin)
                if paquet:
                    estime = round(paquet * qte / taille_paquet, 2)
            prix.append(estime)
        resultat.append((qte, unite, nom, prix[0], prix[1]))
    return resultat


CAT = {"Entrée": "entree", "Plat": "plat", "Dessert": "dessert"}
COUL = {"Entrée": "#10B981", "Plat": "#F97316", "Dessert": "#EC4899"}

# =====================================================================
# PHOTOS DES PLATS : récupérées automatiquement sur Wikipédia (images libres, Wikimedia Commons).
# (langue, titre de l'article) pour chaque plat. Si une photo n'est pas trouvée, le visuel de
# secours (dégradé + emoji) s'affiche. Pour imposer votre propre photo : PHOTOS_PERSO.
# =====================================================================
ARTICLES_WIKI = {
    "Salade Caprese": ("en", "Caprese salad"),
    "Avocat au Thon": ("en", "Avocado"),
    "Velouté de Potimarron": ("en", "Pumpkin soup"),
    "Crevettes Mayo": ("en", "Prawn cocktail"),
    "Poulet au Curry et Riz": ("en", "Chicken curry"),
    "Pavé de Saumon Aneth": ("en", "Salmon as food"),
    "Spaghetti Bolognaise": ("en", "Bolognese sauce"),
    "Gratin Dauphinois": ("fr", "Gratin dauphinois"),
    "Fondant au Chocolat": ("en", "Molten chocolate cake"),
    "Tarte aux Pommes": ("en", "Apple pie"),
    "Mousse au Chocolat": ("en", "Chocolate mousse"),
    "Tiramisu Café": ("en", "Tiramisu"),
}


def _photo_wikipedia(lang, titre):
    try:
        rep = requests.get(f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(titre)}",
                           headers={"User-Agent": "MiamMiam/1.0 (appli de recettes)"}, timeout=5)
        rep.raise_for_status()
        src_img = (rep.json().get("thumbnail") or {}).get("source", "")
        return re.sub(r"/\d+px-", "/500px-", src_img) if src_img else ""
    except Exception:
        return ""


@st.cache_data(ttl=3600, show_spinner=False)
def photos_plats():
    with ThreadPoolExecutor(max_workers=6) as pool:
        resultats = pool.map(lambda kv: (kv[0], _photo_wikipedia(*kv[1])), ARTICLES_WIKI.items())
    return dict(resultats)


# ---------- STYLE ----------
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: linear-gradient(180deg,#FFF1E6 0%,#FFFBF5 280px,#FFFFFF 100%);}
    .block-container {padding-top: 1rem; padding-bottom: 5rem; max-width: 760px;}

    .hero {position:relative; overflow:hidden;
           background: linear-gradient(120deg,#FF4E50 0%,#FF6B35 40%,#F9A826 100%);
           border-radius: 24px; padding: 28px 22px 26px; color: white; margin-bottom: 18px;
           box-shadow: 0 10px 28px rgba(255,78,80,.32);}
    .hero::after {content:"🍅 🥑 🍝 🍰"; position:absolute; right:14px; bottom:6px;
                  font-size:26px; opacity:.35; letter-spacing:4px;}
    .hero h1 {margin:0; font-size:2.1rem; color:white; padding:0; text-shadow:0 2px 6px rgba(0,0,0,.18);}
    .hero p {margin:6px 0 0 0; opacity:.97; font-size:1rem;}

    .stTabs [data-baseweb="tab-list"] {gap:6px; background:#FFFFFF; padding:6px; border-radius:18px;
           box-shadow:0 3px 12px rgba(0,0,0,.07);}
    .stTabs [data-baseweb="tab"] {flex:1; justify-content:center; padding:10px 6px;
           border-radius:12px; font-weight:700; font-size:14px; background:transparent;}
    .stTabs [data-baseweb="tab"]:nth-child(1)[aria-selected="true"] {background:linear-gradient(135deg,#FF6B35,#F9A826) !important; color:white !important;}
    .stTabs [data-baseweb="tab"]:nth-child(2)[aria-selected="true"] {background:linear-gradient(135deg,#EC4899,#F43F5E) !important; color:white !important;}
    .stTabs [data-baseweb="tab"]:nth-child(3)[aria-selected="true"] {background:linear-gradient(135deg,#10B981,#34D399) !important; color:white !important;}
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display:none;}

    div[data-testid="stVerticalBlockBorderWrapper"] {border-radius:20px; border:1px solid #FFE0CC;
           background:#FFFFFF; box-shadow:0 6px 18px rgba(255,107,53,.10);}

    .visuel {position:relative; overflow:hidden; border-radius:16px; display:flex;
             align-items:center; justify-content:center; box-shadow:0 3px 10px rgba(0,0,0,.12);}
    .visuel .emo {font-size:60px;}
    .visuel .photo {position:absolute; inset:0; background-size:cover; background-position:center;}

    .chip {display:inline-block; background:#FFEDD5; color:#C2410C; border-radius:20px;
           padding:3px 10px; font-size:12px; font-weight:700; margin:0 6px 4px 0;}
    .chip.halal {background:#DCFCE7; color:#15803D;}
    .chip.c-entree {background:#D1FAE5; color:#047857;}
    .chip.c-plat {background:#FFEDD5; color:#C2410C;}
    .chip.c-dessert {background:#FCE7F3; color:#BE185D;}
    .chip.tps {background:#E0F2FE; color:#0369A1;}
    .chip.dif {background:#EDE9FE; color:#6D28D9;}
    .chip.pers {background:#FEF3C7; color:#B45309;}
    .prix {display:inline-block; background:linear-gradient(135deg,#16A34A,#4ADE80); color:white;
           font-weight:800; font-size:14px; padding:4px 12px; border-radius:20px; margin:4px 0 8px;}
    .titre {font-weight:800; font-size:16px; margin:10px 0 6px 0; line-height:1.25; color:#1F2937;}

    .stButton > button {border-radius:14px; font-weight:700; width:100%; padding:10px 0;
           border:2px solid #FFD4B8; background:#FFF7F0; color:#C2410C;}
    .stButton > button:hover {border-color:#FF6B35; color:#FF6B35;}
    .stButton > button[kind="primary"] {background:linear-gradient(135deg,#FF4E50,#FF6B35); border:none; color:white;
           box-shadow:0 4px 12px rgba(255,78,80,.30);}
    .stButton > button[kind="primary"]:hover {filter:brightness(1.08); color:white;}

    .badge {padding:4px 10px; border-radius:10px; color:white; font-weight:700;
            display:inline-block; font-size:12px; margin:2px 4px 6px 0;}
    .mcard {border-radius:18px; padding:14px 16px; color:white; font-weight:600; font-size:14px;
            display:flex; flex-direction:column; gap:2px; box-shadow:0 5px 14px rgba(0,0,0,.14);}
    .mcard b {font-size:26px;}
    .mcard.leclerc {background:linear-gradient(135deg,#1D4ED8,#38BDF8);}
    .mcard.lidl {background:linear-gradient(135deg,#F59E0B,#FDE047); color:#78350F;}
    .gagnant {background:linear-gradient(135deg,#059669,#4ADE80); border-radius:20px;
              padding:18px; color:white; text-align:center; font-size:1.05rem; margin:12px 0;
              box-shadow:0 6px 16px rgba(5,150,105,.30);}

    .etape {display:flex; gap:12px; margin:10px 0; align-items:flex-start;}
    .etape .num {flex:0 0 34px; height:34px; border-radius:50%; color:white;
                 font-weight:800; display:flex; align-items:center; justify-content:center;
                 box-shadow:0 3px 8px rgba(0,0,0,.18);}
    .etape .txt {padding-top:5px; line-height:1.45;}
    .astuce {background:#FFF9E6; border-left:5px solid #FFC145; border-radius:12px;
             padding:12px 14px; margin-top:14px;}
    .halalbox {background:#F0FDF4; border-left:5px solid #16A34A; border-radius:12px;
               padding:12px 14px; margin-top:10px;}
</style>
""", unsafe_allow_html=True)

# ---------- ÉTAT ----------
st.session_state.setdefault("selection", [])
st.session_state.setdefault("portions", {})          # {id_recette: nombre de personnes}
st.session_state.setdefault("nb_affiche", 8)
st.session_state.setdefault("filtre_precedent", None)

# ---------- DONNÉES ----------
@st.cache_data(ttl=3600, show_spinner="Chargement des recettes…")
def charger_recettes():
    # (nom, catégorie, mot-clé photo, temps, difficulté)
    base = [
        ("Salade Caprese", "Entrée", "caprese", "10 min", "Facile"),
        ("Avocat au Thon", "Entrée", "avocado", "10 min", "Facile"),
        ("Velouté de Potimarron", "Entrée", "pumpkin,soup", "30 min", "Facile"),
        ("Crevettes Mayo", "Entrée", "shrimp", "15 min", "Facile"),
        ("Poulet au Curry et Riz", "Plat", "chicken,curry", "35 min", "Moyen"),
        ("Pavé de Saumon Aneth", "Plat", "salmon", "20 min", "Facile"),
        ("Spaghetti Bolognaise", "Plat", "spaghetti", "40 min", "Facile"),
        ("Gratin Dauphinois", "Plat", "gratin", "1 h 15", "Moyen"),
        ("Fondant au Chocolat", "Dessert", "chocolate,cake", "25 min", "Moyen"),
        ("Tarte aux Pommes", "Dessert", "apple,pie", "50 min", "Moyen"),
        ("Mousse au Chocolat", "Dessert", "chocolate,mousse", "20 min", "Facile"),
        ("Tiramisu Café", "Dessert", "tiramisu", "30 min", "Moyen"),
    ]
    recettes, rid = [], 1
    photos = photos_plats()
    for i in range(85):
        for nom, cat, kw, temps, diff in base:
            suffixe = "" if i == 0 else (" maison" if i % 2 == 0 else " du Chef") + f" (Variante {i + 1})"
            recettes.append({
                "id": rid, "nom": nom + suffixe, "base": nom, "categorie": cat,
                "image": PHOTOS_PERSO.get(nom) or photos.get(nom, ""),
                "temps": temps, "difficulte": diff, "ingredients": ingredients_a_jour(nom),
            })
            rid += 1
    return recettes

RECETTES = charger_recettes()
PAR_ID = {r["id"]: r for r in RECETTES}


def visuel(r, hauteur=170):
    """Photo par-dessus un dégradé + emoji : si la photo échoue, le visuel de secours reste visible."""
    return (f'<div class="visuel" style="height:{hauteur}px;background:{DEGRADES[r["categorie"]]}">'
            f'<span class="emo">{EMOJIS[r["base"]]}</span>'
            + (f'<div class="photo" style="background-image:url(\'{r["image"]}\')"></div>' if r["image"] else "")
            + '</div>')


def personnes(rid):
    return st.session_state.portions.get(rid, 2)


def coef(rid):
    return personnes(rid) / 2


def cout(r, magasin, c=1.0):
    idx = 3 if magasin == "leclerc" else 4
    return sum(i[idx] for i in r["ingredients"]) * c


def ligne_ingredient(q, unite, nom):
    qs = f"{q:g}"
    if not unite:
        return f"{nom.capitalize()} × {qs}"
    de = "d'" if nom[0].lower() in "aeiouyhéèêœ" else "de "
    return f"{qs} {unite} {de}{nom}"


def basculer(rid):
    if rid in st.session_state.selection:
        st.session_state.selection.remove(rid)
    else:
        st.session_state.selection.append(rid)


def maj_portions(rid, cle):
    """Le nombre de personnes est mémorisé par recette et synchronisé entre la fiche et les courses."""
    n = st.session_state[cle]
    st.session_state.portions[rid] = n
    autre = f"c_{rid}" if cle.startswith("pers_") else f"pers_{rid}"
    if autre in st.session_state:
        st.session_state[autre] = n


def appliquer_a_toutes():
    n = st.session_state.global_pers
    for rid in st.session_state.selection:
        st.session_state.portions[rid] = n
        st.session_state[f"c_{rid}"] = n


# ---------- FICHE RECETTE (fenêtre) ----------
@st.dialog("Fiche recette", width="large")
def fiche(rid):
    r = PAR_ID[rid]
    f = FICHES[r["base"]]
    st.markdown(visuel(r, 220), unsafe_allow_html=True)
    if r["image"]:
        st.caption("📷 Photo : Wikipédia / Wikimedia Commons")
    st.markdown(f'<div class="titre" style="font-size:22px">{r["nom"]}</div>'
                f'<span class="chip halal">✅ Halal</span>'
                f'<span class="chip c-{CAT[r["categorie"]]}">{ICONES[r["categorie"]]} {r["categorie"]}</span>'
                f'<span class="chip tps">⏱ {r["temps"]}</span>'
                f'<span class="chip dif">{r["difficulte"]}</span>', unsafe_allow_html=True)

    cle = f"pers_{rid}"
    st.session_state[cle] = personnes(rid)
    st.number_input("👥 Nombre de personnes", 1, 12, key=cle,
                    on_change=maj_portions, args=(rid, cle))
    c = coef(rid)

    st.markdown("### 🧺 Ingrédients")
    for qte, unite, nom, _, _ in r["ingredients"]:
        st.markdown(f"- {ligne_ingredient(qte * c, unite, nom)}")
    st.caption("Sel, poivre et épices de base à compléter selon votre placard.")

    st.markdown("### 👩‍🍳 Préparation")
    for n, etape in enumerate(f["etapes"], 1):
        st.markdown(f'<div class="etape"><div class="num" style="background:{COUL[r["categorie"]]}">{n}</div><div class="txt">{etape}</div></div>',
                    unsafe_allow_html=True)
    st.markdown(f'<div class="astuce">💡 <b>Astuce du chef :</b> {f["astuce"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="halalbox">✅ <b>Conseil halal :</b> {f["halal"]}</div>', unsafe_allow_html=True)

    st.markdown(f"**Budget estimé pour {personnes(rid)} pers. :** Leclerc {cout(r, 'leclerc', c):.2f} € · "
                f"Lidl {cout(r, 'lidl', c):.2f} €")

    b1, b2 = st.columns(2)
    if rid in st.session_state.selection:
        if b1.button("✅ Dans le panier · Retirer", key=f"dlg_{rid}"):
            basculer(rid)
            st.rerun()
    else:
        if b1.button("❤️ Ajouter au panier", key=f"dlg_{rid}", type="primary"):
            basculer(rid)
            st.rerun()
    if b2.button("Fermer et actualiser", key=f"fer_{rid}"):
        st.rerun()


# ---------- EN-TÊTE ----------
st.markdown("""
<div class="hero">
    <h1>🍳 MiamMiam</h1>
    <p>Recettes 100 % halal : comparez Leclerc et Lidl, économisez sur vos courses.</p>
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
        st.caption(f"{len(resultats)} recettes · prix pour 2 personnes")
        visibles = resultats[:st.session_state.nb_affiche]
        for debut in range(0, len(visibles), 2):
            cols = st.columns(2)
            for col, r in zip(cols, visibles[debut:debut + 2]):
                with col, st.container(border=True):
                    st.markdown(
                        visuel(r) +
                        f'<div class="titre">{r["nom"]}</div>'
                        f'<span class="chip halal">✅ Halal</span>'
                        f'<span class="chip c-{CAT[r["categorie"]]}">{ICONES[r["categorie"]]} {r["categorie"]}</span>'
                        f'<span class="chip tps">⏱ {r["temps"]}</span>'
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
                            f'<span class="chip pers">👥 {personnes(r["id"])} pers.</span>'
                            f'<span class="chip tps">⏱ {r["temps"]}</span>', unsafe_allow_html=True)
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
        # Totaux : chaque recette est comptée avec SON nombre de personnes
        tot_lec = sum(cout(r, "leclerc", coef(r["id"])) for r in sel)
        tot_lid = sum(cout(r, "lidl", coef(r["id"])) for r in sel)

        m1, m2 = st.columns(2)
        m1.markdown(f'<div class="mcard leclerc">🟦 Leclerc<b>{tot_lec:.2f} €</b></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="mcard lidl">🟨 Lidl<b>{tot_lid:.2f} €</b></div>', unsafe_allow_html=True)

        diff = abs(tot_lec - tot_lid)
        gagnant = "Leclerc (Marque Repère)" if tot_lec < tot_lid else "Lidl"
        if diff > 0.005:
            st.markdown(f'<div class="gagnant">🌟 Allez chez <b>{gagnant}</b><br>'
                        f'et économisez <b>{diff:.2f} €</b></div>', unsafe_allow_html=True)
        else:
            st.info("Prix identiques dans les deux enseignes.")

        st.caption(f"💶 Prix : {len(CODES_BARRES)} ingrédient(s) liés à Open Prices (relevés réels, "
                   "mis à jour toutes les 24 h) ; les autres restent des estimations.")
        st.button("🔄 Actualiser les prix maintenant", on_click=st.cache_data.clear)

        # Nombre de personnes pour toutes les recettes d'un coup
        g1, g2 = st.columns([2, 1])
        g1.number_input("👥 Même nombre de personnes pour toutes", 1, 12, 2, key="global_pers")
        g2.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        g2.button("Appliquer", on_click=appliquer_a_toutes)

        # Liste de courses complète : tous les ingrédients, regroupés
        agg = {}
        for r in sel:
            c = coef(r["id"])
            for qte, unite, nom, p_lec, p_lid in r["ingredients"]:
                a = agg.setdefault((nom, unite), [0.0, 0.0, 0.0])
                a[0] += qte * c
                a[1] += p_lec * c
                a[2] += p_lid * c

        st.subheader(f"🧺 Liste de courses ({len(agg)} articles)")
        lignes, total_mix = [], 0.0
        for (nom, unite), (q, p_lec, p_lid) in sorted(agg.items()):
            c_lec = "#16A34A" if p_lec <= p_lid else "#DC2626"
            c_lid = "#16A34A" if p_lid <= p_lec else "#DC2626"
            libelle = ligne_ingredient(q, unite, nom)
            st.markdown(
                f"**{libelle}**<br>"
                f'<span class="badge" style="background:{c_lec}">Leclerc {p_lec:.2f} €</span>'
                f'<span class="badge" style="background:{c_lid}">Lidl {p_lid:.2f} €</span>',
                unsafe_allow_html=True)
            meilleur, mag = (p_lec, "Leclerc") if p_lec <= p_lid else (p_lid, "Lidl")
            total_mix += meilleur
            lignes.append(f"[ ] {libelle} — {mag} — {meilleur:.2f} €")

        gain_mix = min(tot_lec, tot_lid) - total_mix
        if gain_mix > 0.005:
            st.caption(f"💡 En achetant chaque article dans l'enseigne la moins chère, "
                       f"vous paieriez {total_mix:.2f} € (encore {gain_mix:.2f} € d'économie).")
        st.download_button("📥 Télécharger ma liste de courses",
                           "\n".join(lignes) + f"\n\nTotal : {total_mix:.2f} €",
                           file_name="liste_courses.txt", mime="text/plain")

        st.subheader("Détail par recette")
        for r in sel:
            rid = r["id"]
            with st.expander(f"{ICONES[r['categorie']]} {r['nom']} · {personnes(rid)} pers."):
                cle = f"c_{rid}"
                st.session_state[cle] = personnes(rid)
                st.number_input("👥 Nombre de personnes", 1, 12, key=cle,
                                on_change=maj_portions, args=(rid, cle))
                c = coef(rid)
                for qte, unite, nom, p_lec, p_lid in r["ingredients"]:
                    c_lec = "#16A34A" if p_lec <= p_lid else "#DC2626"
                    c_lid = "#16A34A" if p_lid <= p_lec else "#DC2626"
                    st.markdown(
                        f"{ligne_ingredient(qte * c, unite, nom)}<br>"
                        f'<span class="badge" style="background:{c_lec}">Leclerc {p_lec * c:.2f} €</span>'
                        f'<span class="badge" style="background:{c_lid}">Lidl {p_lid * c:.2f} €</span>',
                        unsafe_allow_html=True)

