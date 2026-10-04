import streamlit as st

st.set_page_config(page_title="MiamMiam", page_icon="🍳", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem; max-width: 760px;}

    .hero {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 55%, #FFC145 100%);
        border-radius: 22px; padding: 26px 22px; color: white; margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(255,107,53,0.30);
    }
    .hero h1 {margin: 0; font-size: 2rem; color: white; padding: 0;}
    .hero p {margin: 6px 0 0 0; opacity: .95; font-size: 1rem;}

    .stTabs [data-baseweb="tab-list"] {gap: 6px; background: #FFF4EC; padding: 6px; border-radius: 16px;}
    .stTabs [data-baseweb="tab"] {
        flex: 1; justify-content: center; padding: 10px 6px; border-radius: 12px;
        font-weight: 700; font-size: 14px; background: transparent;
    }
    .stTabs [aria-selected="true"] {background: #FF6B35 !important; color: white !important;}
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display: none;}

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px; border: 1px solid #F1E3D8;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06); overflow: hidden;
    }
    div[data-testid="stImage"] img {border-radius: 14px; height: 170px; object-fit: cover;}

    .chip {display:inline-block; background:#FFF4EC; color:#C2410C; border-radius:20px;
           padding:3px 10px; font-size:12px; font-weight:700; margin-right:6px;}
    .prix {color:#16A34A; font-weight:800; font-size:15px;}
    .titre {font-weight:800; font-size:16px; margin:6px 0 4px 0; line-height:1.25;}

    .stButton > button {border-radius: 12px; font-weight: 700; width: 100%; padding: 10px 0;}
    .stButton > button[kind="primary"] {background: #FF6B35; border: none;}
    .stButton > button[kind="primary"]:hover {background: #E85A28;}

    .badge {padding: 6px 12px; border-radius: 10px; color: white; font-weight: 700;
            display: inline-block; font-size: 13px; margin: 2px 4px 8px 0;}
    .gagnant {background: linear-gradient(135deg,#16A34A,#4ADE80); border-radius: 18px;
              padding: 18px; color: white; text-align: center; font-size: 1.05rem; margin-top: 12px;}
</style>
""", unsafe_allow_html=True)

# ---------- ÉTAT ----------
st.session_state.setdefault("selection", [])
st.session_state.setdefault("nb_affiche", 8)

# ---------- DONNÉES ----------
@st.cache_data
def charger_recettes():
    # (nom, catégorie, mot-clé photo, temps, difficulté, [(ingrédient, prix Leclerc, prix Lidl)])
    base = [
        ("Salade Caprese", "Entrée", "caprese,salad", "10 min", "Facile",
         [("Tomates Marque Repère", 1.20, 1.40), ("Mozzarella Marque Repère", 1.50, 1.30)]),
        ("Avocat au Thon", "Entrée", "avocado,tuna", "10 min", "Facile",
         [("Avocat Rose de France", 1.80, 1.95), ("Thon entier Marque Repère", 2.10, 1.90)]),
        ("Velouté de Potimarron", "Entrée", "pumpkin,soup", "30 min", "Facile",
         [("Potimarron", 2.50, 2.20), ("Crème Fraîche Marque Repère", 1.10, 1.25)]),
        ("Crevettes Mayo", "Entrée", "shrimp,mayonnaise", "15 min", "Facile",
         [("Crevettes décortiquées", 4.50, 4.20), ("Mayonnaise Marque Repère", 1.30, 1.45)]),
        ("Poulet au Curry et Riz", "Plat", "chicken,curry", "35 min", "Moyen",
         [("Blanc de Poulet Marque Repère", 6.50, 5.90), ("Riz Basmati Marque Repère", 1.40, 1.20)]),
        ("Pavé de Saumon Aneth", "Plat", "salmon,dill", "20 min", "Facile",
         [("Pavé de Saumon Atlantique", 8.90, 8.40), ("Citron jaune", 0.60, 0.50)]),
        ("Spaghetti Bolognaise", "Plat", "spaghetti,bolognese", "40 min", "Facile",
         [("Pâtes Spaghetti Marque Repère", 0.80, 0.75), ("Bœuf Haché Marque Repère", 5.20, 5.50)]),
        ("Gratin Dauphinois", "Plat", "gratin,potatoes", "1 h 15", "Moyen",
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
                "id": rid, "nom": nom + suffixe, "categorie": cat,
                "image": f"https://loremflickr.com/640/420/{kw}?lock={rid}",
                "temps": temps, "difficulte": diff, "ingredients": ings,
            })
            rid += 1
    return recettes

RECETTES = charger_recettes()
PAR_ID = {r["id"]: r for r in RECETTES}
ICONES = {"Entrée": "🥗", "Plat": "🍝", "Dessert": "🍰"}

def cout(r, magasin):
    idx = 1 if magasin == "leclerc" else 2
    return sum(i[idx] for i in r["ingredients"])

def basculer(rid):
    if rid in st.session_state.selection:
        st.session_state.selection.remove(rid)
    else:
        st.session_state.selection.append(rid)

# ---------- EN-TÊTE ----------
st.markdown("""
<div class="hero">
    <h1>🍳 MiamMiam</h1>
    <p>Choisissez vos recettes, comparez Leclerc et Lidl, économisez sur vos courses.</p>
</div>
""", unsafe_allow_html=True)

nb = len(st.session_state.selection)
t1, t2, t3 = st.tabs(["📖 Recettes", f"❤️ Panier ({nb})", "🛒 Courses"])

# ---------- ONGLET RECETTES ----------
with t1:
    recherche = st.text_input("Recherche", placeholder="🔍 Poulet, chocolat, salade…",
                              label_visibility="collapsed")
    cat = st.radio("Catégorie", ["Tous", "🥗 Entrée", "🍝 Plat", "🍰 Dessert"],
                   horizontal=True, label_visibility="collapsed")
    cat = cat.split(" ")[-1] if cat != "Tous" else cat

    resultats = [r for r in RECETTES
                 if (cat == "Tous" or r["categorie"] == cat)
                 and recherche.lower() in r["nom"].lower()]

    if not resultats:
        st.warning("Aucune recette ne correspond à votre recherche.")
    else:
        st.caption(f"{len(resultats)} recettes")
        visibles = resultats[:st.session_state.nb_affiche]
        for ligne in range(0, len(visibles), 2):
            cols = st.columns(2)
            for col, r in zip(cols, visibles[ligne:ligne + 2]):
                with col, st.container(border=True):
                    st.image(r["image"], use_container_width=True)
                    st.markdown(
                        f'<div class="titre">{r["nom"]}</div>'
                        f'<span class="chip">{ICONES[r["categorie"]]} {r["categorie"]}</span>'
                        f'<span class="chip">⏱ {r["temps"]}</span>'
                        f'<span class="chip">{r["difficulte"]}</span>'
                        f'<div class="prix">dès {min(cout(r, "leclerc"), cout(r, "lidl")):.2f} €</div>',
                        unsafe_allow_html=True)
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

# ---------- ONGLET PANIER ----------
with t2:
    st.subheader("Mes recettes")
    sel = [PAR_ID[i] for i in st.session_state.selection]
    if not sel:
        st.info("Votre panier est vide. Ajoutez des recettes depuis l'onglet 📖.")
    else:
        for r in sel:
            with st.container(border=True):
                c1, c2 = st.columns([1, 2])
                c1.image(r["image"], use_container_width=True)
                c2.markdown(f'<div class="titre">{r["nom"]}</div>'
                            f'<span class="chip">⏱ {r["temps"]}</span>'
                            f'<span class="chip">{r["categorie"]}</span>', unsafe_allow_html=True)
                c2.button("🗑 Retirer", key=f"p{r['id']}", on_click=basculer, args=(r["id"],))
        st.button("Vider le panier", on_click=lambda: st.session_state.selection.clear())

# ---------- ONGLET COURSES ----------
with t3:
    sel = [PAR_ID[i] for i in st.session_state.selection]
    if not sel:
        st.info("Sélectionnez des recettes pour comparer les prix.")
    else:
        tot_lec = sum(cout(r, "leclerc") for r in sel)
        tot_lid = sum(cout(r, "lidl") for r in sel)

        m1, m2 = st.columns(2)
        m1.metric("🟦 Leclerc", f"{tot_lec:.2f} €")
        m2.metric("🟨 Lidl", f"{tot_lid:.2f} €")

        diff = abs(tot_lec - tot_lid)
        gagnant = "Leclerc (Marque Repère)" if tot_lec < tot_lid else "Lidl"
        if diff > 0:
            st.markdown(f'<div class="gagnant">🌟 Allez chez <b>{gagnant}</b><br>'
                        f'et économisez <b>{diff:.2f} €</b></div>', unsafe_allow_html=True)
        else:
            st.info("Prix identiques dans les deux enseignes.")

        st.subheader("Détail par recette")
        for r in sel:
            with st.expander(f"{ICONES[r['categorie']]} {r['nom']}"):
                for ing, p_lec, p_lid in r["ingredients"]:
                    c_lec = "#16A34A" if p_lec <= p_lid else "#DC2626"
                    c_lid = "#16A34A" if p_lid <= p_lec else "#DC2626"
                    st.markdown(
                        f"**{ing}**<br>"
                        f'<span class="badge" style="background:{c_lec}">Leclerc {p_lec:.2f} €</span>'
                        f'<span class="badge" style="background:{c_lid}">Lidl {p_lid:.2f} €</span>',
                        unsafe_allow_html=True)
