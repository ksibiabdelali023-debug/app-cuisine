import streamlit as st
import random

# Configuration de la page pour mobile
st.set_page_config(page_title="MiamMiam", page_icon="🍳", layout="centered")

# Style CSS personnalisé pour le look Fun & Design (Inspiré des meilleures apps)
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 15px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #FF4B4B !important; color: white !important; }
    .recipe-card {
        border: 1px solid #e6e9ef;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        background-color: white;
    }
    .price-leclerc { font-weight: bold; padding: 3px 8px; border-radius: 8px; }
    .price-lidl { font-weight: bold; padding: 3px 8px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# Initialisation de la sélection dans la session utilisateur
if 'selection' not in st.session_state:
    st.session_state.selection = []

# Générateur automatique de la base de données de 1000 recettes (Simulées par combinaisons)
@st.cache_data
def charger_recettes():
    categories = ["Entrée", "Plat", "Dessert"]
    ingredients_base = {
        "Entrée": [("Tomates", 1.20, 1.40), ("Mozzarella", 1.50, 1.30), ("Salade", 0.90, 0.85), ("Avocat", 1.80, 1.95), ("Crevettes", 4.50, 4.20)],
        "Plat": [("Poulet", 6.50, 5.90), ("Crème Fraîche", 1.10, 1.25), ("Pâtes", 0.80, 0.75), ("Bœuf Haché", 5.20, 5.50), ("Pommes de terre", 2.10, 1.90), ("Saumon", 8.90, 8.40)],
        "Dessert": [("Chocolat", 1.40, 1.20), ("Beurre", 1.90, 1.75), ("Œufs", 2.10, 2.30), ("Farine", 0.70, 0.65), ("Pommes", 2.30, 2.10)]
    }
    
    # Mots-clés d'images Unsplash de qualité culinaire
    images_pool = {
        "Entrée": ["https://unsplash.com", "https://unsplash.com"],
        "Plat": ["https://unsplash.com", "https://unsplash.com"],
        "Dessert": ["https://unsplash.com", "https://unsplash.com"]
    }
    
    recettes = []
    id_recette = 1
    
    for cat in categories:
        for i in range(1, 334 if cat != "Dessert" else 333):
            img = random.choice(images_pool[cat])
            ing_selectionnes = random.sample(ingredients_base[cat], k=min(3, len(ingredients_base[cat])))
            
            recettes.append({
                "id": id_recette,
                "nom": f"{cat} Gourmand n°{i}",
                "categorie": cat,
                "image": f"{img}&q={id_recette}",
                "ingredients": ing_selectionnes
            })
            id_recette += 1
    return recettes

liste_recettes = charger_recettes()

# Interface Principale
st.title("🍳 MiamMiam App")
st.write("L'appli fun qui compare vos courses chez Leclerc et Lidl !")

onglet1, onglet2, onglet3 = st.tabs(["📖 Les Recettes", "❤️ Ma Sélection", "🛒 Liste de Courses"])

# ONGLET 1 : Catalogue des recettes
with onglet1:
    cat_choisie = st.radio("Filtrer par catégorie :", ["Tous", "Entrée", "Plat", "Dessert"], horizontal=True)
    
    for r in liste_recettes:
        if cat_choisie != "Tous" and r["categorie"] != cat_choisie:
            continue
            
        with st.container():
            st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
            col1, col2 = st.columns(1, 2)
            with col1:
                st.image(r["image"], use_container_width=True)
            with col2:
                st.subheader(r["nom"])
                st.caption(f"Catégorie: {r['categorie']}")
                
                if r["id"] in st.session_state.selection:
                    if st.button("❌ Retirer", key=f"del_{r['id']}"):
                        st.session_state.selection.remove(r["id"])
                        st.rerun()
                else:
                    if st.button("❤️ Ajouter", key=f"add_{r['id']}"):
                        st.session_state.selection.append(r["id"])
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ONGLET 2 : Ma Sélection
with onglet2:
    st.header("Mes recettes sélectionnées")
    recettes_selectionnees = [r for r in liste_recettes if r["id"] in st.session_state.selection]
    
    if not recettes_selectionnees:
        st.info("Votre carnet est vide. Ajoutez des recettes depuis le premier onglet !")
    else:
        for r in recettes_selectionnees:
            st.markdown(f"✅ **{r['nom']}** ({r['categorie']})")

# ONGLET 3 : Liste de courses comparative
with onglet3:
    st.header("Comparateur de prix de vos courses")
    recettes_selectionnees = [r for r in liste_recettes if r["id"] in st.session_state.selection]
    
    if not recettes_selectionnees:
        st.info("Sélectionnez au moins une recette pour voir votre liste de courses.")
    else:
        total_leclerc = 0.0
        total_lidl = 0.0
        
        st.write("### Détail des ingrédients")
        for r in recettes_selectionnees:
            st.markdown(f"**Pour la recette : {r['nom']}**")
            for ing, p_leclerc, p_lidl in r["ingredients"]:
                total_leclerc += p_leclerc
                total_lidl += p_lidl
                
                c_leclerc = "#2ecc71" if p_leclerc < p_lidl else "#e74c3c"
                c_lidl = "#2ecc71" if p_lidl < p_leclerc else "#e74c3c"
                
                col_ing, col_lec, col_lid = st.columns(3)
                col_ing.write(f"• {ing}")
                col_lec.markdown(f'<span class="price-leclerc" style="background-color: {c_leclerc}; color: white;">Leclerc: {p_leclerc:.2f}€</span>', unsafe_allow_html=True)
                col_lid.markdown(f'<span class="price-lidl" style="background-color: {c_lidl}; color: white;">Lidl: {p_lidl:.2f}€</span>', unsafe_allow_html=True)
            st.divider()
            
        st.subheader("💰 Ticket de caisse Estimé")
        c_tot_lec = "green" if total_leclerc < total_lidl else "red"
        c_tot_lid = "green" if total_lidl < total_leclerc else "red"
        
        st.markdown(f"**Total chez Leclerc :** :{c_tot_lec}[{total_leclerc:.2f} €]")
        st.markdown(f"**Total chez Lidl :** :{c_tot_lid}[{total_lidl:.2f} €]")
        
        diff = abs(total_leclerc - total_lidl)
        magasin_moins_cher = "Leclerc" if total_leclerc < total_lidl else "Lidl"
        if diff > 0:
            st.success(f"🌟 En allant chez **{magasin_moins_cher}**, vous économisez **{diff:.2f} €** sur ces repas !")
