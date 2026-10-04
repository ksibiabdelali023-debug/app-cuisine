import streamlit as st
import random

# Configuration optimisée pour les écrans de téléphones
st.set_page_config(page_title="MiamMiam", page_icon="🍳", layout="centered")

st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 14px;
        background-color: #f0f2f6;
        border-radius: 12px;
        font-weight: bold;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] { background-color: #FF4B4B !important; color: white !important; }
    .recipe-card {
        border: 1px solid #e6e9ef;
        border-radius: 15px;
        padding: 12px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        background-color: white;
    }
    .badge { padding: 4px 8px; border-radius: 6px; color: white; font-weight: bold; display: inline-block; }
</style>
""", unsafe_allow_html=True)

if 'selection' not in st.session_state:
    st.session_state.selection = []

@st.cache_data
def charger_recettes():
    categories = ["Entrée", "Plat", "Dessert"]
    ingredients_base = {
        "Entrée": [("Tomates", 1.20, 1.40), ("Mozzarella", 1.50, 1.30), ("Salade", 0.90, 0.85), ("Avocat", 1.80, 1.95)],
        "Plat": [("Poulet", 6.50, 5.90), ("Crème Fraîche", 1.10, 1.25), ("Pâtes", 0.80, 0.75), ("Bœuf Haché", 5.20, 5.50)],
        "Dessert": [("Chocolat", 1.40, 1.20), ("Beurre", 1.90, 1.75), ("Œufs", 2.10, 2.30), ("Farine", 0.70, 0.65)]
    }
    images_pool = {
        "Entrée": ["https://unsplash.com"],
        "Plat": ["https://unsplash.com"],
        "Dessert": ["https://unsplash.com"]
    }
    
    recettes = []
    id_recette = 1
    for cat in categories:
        for i in range(1, 334 if cat != "Dessert" else 333):
            recettes.append({
                "id": id_recette,
                "nom": f"{cat} Gourmand n°{i}",
                "categorie": cat,
                "image": images_pool[cat][0],
                "ingredients": random.sample(ingredients_base[cat], k=2)
            })
            id_recette += 1
    return recettes

liste_recettes = charger_recettes()

st.title("🍳 MiamMiam App")
st.write("Comparez vos courses chez Leclerc et Lidl !")

onglet1, onglet2, onglet3 = st.tabs(["📖 Recettes", "❤️ Sélection", "🛒 Courses"])

with onglet1:
    cat_choisie = st.radio("Catégorie :", ["Tous", "Entrée", "Plat", "Dessert"], horizontal=True)
    for r in liste_recettes:
        if cat_choisie != "Tous" and r["categorie"] != cat_choisie:
            continue
        
        st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
        st.image(r["image"], use_container_width=True)
        st.subheader(r["nom"])
        
        if r["id"] in st.session_state.selection:
            if st.button("❌ Retirer du panier", key=f"del_{r['id']}"):
                st.session_state.selection.remove(r["id"])
                st.rerun()
        else:
            if st.button("❤️ Ajouter au panier", key=f"add_{r['id']}", type="primary"):
                st.session_state.selection.append(r["id"])
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with onglet2:
    st.header("Mes recettes")
    recettes_sel = [r for r in liste_recettes if r["id"] in st.session_state.selection]
    if not recettes_sel:
        st.info("Votre panier est vide.")
    else:
        for r in recettes_sel:
            st.write(f"✅ {r['nom']}")

with onglet3:
    st.header("Le moins cher ?")
    recettes_sel = [r for r in liste_recettes if r["id"] in st.session_state.selection]
    if not recettes_sel:
        st.info("Sélectionnez des recettes pour comparer les prix.")
    else:
        total_leclerc, total_lidl = 0.0, 0.0
        for r in recettes_sel:
            st.write(f"**{r['nom']} :**")
            for ing, p_lec, p_lid in r["ingredients"]:
                total_leclerc += p_lec
                total_lidl += p_lid
                c_lec = "#2ecc71" if p_lec < p_lid else "#e74c3c"
                c_lid = "#2ecc71" if p_lid < p_lec else "#e74c3c"
                
                st.write(f"• {ing}")
                st.markdown(f'<span class="badge" style="background-color:{c_lec}">Leclerc : {p_lec:.2f}€</span> <span class="badge" style="background-color:{c_lid}">Lidl : {p_lid:.2f}€</span>', unsafe_allow_html=True)
            st.divider()
        
        st.subheader("💰 Total Estimé")
        st.write(f"**Total Leclerc :** {total_leclerc:.2f} €")
        st.write(f"**Total Lidl :** {total_lidl:.2f} €")
        
        diff = abs(total_leclerc - total_lidl)
        moins_cher = "Leclerc" if total_leclerc < total_lidl else "Lidl"
        if diff > 0:
            st.success(f"🌟 Allez chez **{moins_cher}** pour économiser **{diff:.2f} €** !")

