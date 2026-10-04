# MiamMiam

Recettes halal et comparateur de courses Leclerc / Lidl (Streamlit).

    pip install -r requirements.txt
    streamlit run app.py
    python tests/test_miammiam.py

## Organisation
- `app.py` : point d'entrée (en-tête, accessibilité, onglets)
- `miammiam/donnees.py` : recettes, ingrédients, prix estimés, photos, rayons (à modifier ici)
- `miammiam/calculs.py` : prix, quantités, listes de courses (sans Streamlit, testé)
- `miammiam/services.py` : photos Wikipédia et prix Open Prices (sans Streamlit, testé)
- `miammiam/theme.py` : couleurs, contrastes WCAG, CSS (sans Streamlit, testé)
- `miammiam/etat.py`, `ressources.py`, `ui.py`, `pages.py` : partie Streamlit
- `.streamlit/config.toml` : thème clair (à garder à côté de app.py)
