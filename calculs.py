"""Calculs purs (sans Streamlit) : prix, quantités, listes de courses."""
import re

from donnees import RAYONS_ORDRE, REGLES_RAYONS

ENSEIGNES = {"leclerc": "Leclerc (Marque Repère)", "lidl": "Lidl"}


def format_prix(x):
    return f"{x:.2f}".replace(".", ",") + " €"


def format_qte(q):
    return f"{q:g}".replace(".", ",")


def ligne_ingredient(q, unite, nom):
    qs = format_qte(q)
    if not unite:
        return f"{nom.capitalize()} × {qs}"
    de = "d'" if nom[0].lower() in "aeiouyhéèêœ" else "de "
    return f"{qs} {unite} {de}{nom}"


def minutes(temps):
    nombres = [int(n) for n in re.findall(r"\d+", temps)]
    if "h" in temps:
        return nombres[0] * 60 + (nombres[1] if len(nombres) > 1 else 0)
    return nombres[0]


def cout(ingredients, magasin, coef=1.0):
    idx = 3 if magasin == "leclerc" else 4
    return sum(i[idx] for i in ingredients) * coef


def prix_minimum(recette):
    return min(cout(recette["ingredients"], "leclerc"), cout(recette["ingredients"], "lidl"))


def rayon_de(nom):
    bas = nom.lower()
    for rayon, mots in REGLES_RAYONS:
        if any(re.search(rf"\b{re.escape(m)}\b", bas) for m in mots):
            return rayon
    return "Épicerie"


def totaux(recettes, coef_de):
    lec = sum(cout(r["ingredients"], "leclerc", coef_de(r["id"])) for r in recettes)
    lid = sum(cout(r["ingredients"], "lidl", coef_de(r["id"])) for r in recettes)
    return lec, lid


def agreger(recettes, coef_de):
    """Fusionne les ingrédients identiques : {(nom, unité): [quantité, prix Leclerc, prix Lidl]}."""
    agg = {}
    for r in recettes:
        c = coef_de(r["id"])
        for qte, unite, nom, p_lec, p_lid in r["ingredients"]:
            a = agg.setdefault((nom, unite), [0.0, 0.0, 0.0])
            a[0] += qte * c
            a[1] += p_lec * c
            a[2] += p_lid * c
    return agg


def grouper_par_rayon(agg):
    """[(rayon, [(nom, unité, quantité, prix Leclerc, prix Lidl), ...]), ...] dans l'ordre du magasin."""
    groupes = {rayon: [] for rayon in RAYONS_ORDRE}
    for (nom, unite), (q, p_lec, p_lid) in sorted(agg.items()):
        groupes[rayon_de(nom)].append((nom, unite, q, p_lec, p_lid))
    return [(rayon, lignes) for rayon, lignes in groupes.items() if lignes]


def meilleure_enseigne(tot_lec, tot_lid):
    """(nom de l'enseigne, économie) ou (None, 0) si les prix sont égaux."""
    ecart = abs(tot_lec - tot_lid)
    if ecart < 0.005:
        return None, 0.0
    return (ENSEIGNES["leclerc"] if tot_lec < tot_lid else ENSEIGNES["lidl"]), ecart


def meilleur_mixte(agg):
    """Total si chaque article est acheté dans l'enseigne la moins chère."""
    return sum(min(p_lec, p_lid) for _, p_lec, p_lid in agg.values())


def texte_liste(groupes):
    """Liste de courses au format texte, par rayon, avec l'enseigne la moins chère."""
    sortie, total = [], 0.0
    for rayon, lignes in groupes:
        sortie.append(rayon.upper())
        for nom, unite, q, p_lec, p_lid in lignes:
            prix, mag = (p_lec, "Leclerc") if p_lec <= p_lid else (p_lid, "Lidl")
            total += prix
            sortie.append(f"[ ] {ligne_ingredient(q, unite, nom)} - {mag} - {format_prix(prix)}")
        sortie.append("")
    sortie.append(f"Total : {format_prix(total)}")
    return "\n".join(sortie)
