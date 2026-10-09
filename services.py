"""Accès réseau (sans Streamlit) : photos Wikipédia et prix Open Prices.
Toutes les fonctions renvoient une valeur de repli au lieu de lever une erreur."""
import re
import statistics
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests

UA = {"User-Agent": "MiamMiam/1.0 (appli de recettes)"}
API_PRIX = "https://prices.openfoodfacts.org/api/v1/prices"


def photo_wikipedia(lang, titre):
    try:
        rep = requests.get(f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(titre)}",
                           headers=UA, timeout=5)
        rep.raise_for_status()
        src = (rep.json().get("thumbnail") or {}).get("source", "")
        return re.sub(r"/\d+px-", "/500px-", src) if src else ""
    except Exception:
        return ""


def photos_pour(articles, recuperer=photo_wikipedia):
    with ThreadPoolExecutor(max_workers=6) as pool:
        resultats = pool.map(lambda kv: (kv[0], recuperer(*kv[1])), articles.items())
        return dict(resultats)


def prix_paquet_reel(code, magasin):
    """Médiane des 10 derniers prix en euros relevés dans l'enseigne pour ce code-barres."""
    try:
        rep = requests.get(API_PRIX, params={"product_code": code, "order_by": "-date", "size": 50},
                           headers=UA, timeout=8)
        rep.raise_for_status()
        valeurs = []
        for p in rep.json().get("items", []):
            lieu = p.get("location") or {}
            nom_lieu = f"{lieu.get('osm_name', '')} {lieu.get('osm_brand', '')}".lower()
            if p.get("currency") == "EUR" and p.get("price") and magasin in nom_lieu:
                valeurs.append(float(p["price"]))
        return round(statistics.median(valeurs[:10]), 2) if valeurs else None
    except Exception:
        return None


def ingredients_a_jour(ingredients, codes, prix_fn=prix_paquet_reel):
    """Remplace les prix estimés par les prix réels quand un code-barres est renseigné."""
    resultat = []
    for qte, unite, nom, p_lec, p_lid in ingredients:
        liens = codes.get(nom, {})
        prix = []
        for magasin, estime in (("leclerc", p_lec), ("lidl", p_lid)):
            if magasin in liens:
                code, taille_paquet = liens[magasin]
                paquet = prix_fn(code, magasin)
                if paquet:
                    estime = round(paquet * qte / taille_paquet, 2)
            prix.append(estime)
        resultat.append((qte, unite, nom, prix[0], prix[1]))
    return resultat
