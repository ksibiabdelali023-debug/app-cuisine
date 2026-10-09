# MiamMiam

Recettes halal et comparateur de courses Leclerc / Lidl (Streamlit).

## Lancer en local
    pip install -r requirements.txt
    streamlit run streamlit_app.py

## Déployer sur Render (Web Service)
- Build Command : `pip install -r requirements.txt`
- Start Command : `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
- Variable d'environnement : `PYTHON_VERSION` = `3.12.3`
- (ou « New + > Blueprint » : Render lit `render.yaml`)

## Fichiers
- `streamlit_app.py` : point d'entrée
- `donnees.py` : recettes, ingrédients, prix estimés, photos, rayons (à modifier ici)
- `calculs.py`, `services.py`, `theme.py` : logique sans Streamlit (testée par `test_miammiam.py`)
- `etat.py`, `ressources.py`, `ui.py`, `pages.py` : partie Streamlit
- `.streamlit/config.toml` : thème clair
