"""Tests des parties sans Streamlit. Lancer : python tests/test_miammiam.py (ou pytest)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import calculs, donnees, services, theme  # noqa: E402


def test_contrastes_wcag():
    assert theme.paires_insuffisantes(theme.NORMAL) == []
    assert theme.paires_insuffisantes(theme.ELEVE, 7.0) == []


def test_css_sans_variable_non_remplacee():
    for palette in (theme.NORMAL, theme.ELEVE):
        assert "${" not in theme.css(palette, 125)


def test_format_prix_et_ingredients():
    assert calculs.format_prix(12.4) == "12,40 €"
    assert calculs.ligne_ingredient(125, "g", "mozzarella") == "125 g de mozzarella"
    assert calculs.ligne_ingredient(2, "c. à soupe", "huile d'olive") == "2 c. à soupe d'huile d'olive"
    assert calculs.ligne_ingredient(3, "", "tomates mûres") == "Tomates mûres × 3"
    assert calculs.ligne_ingredient(1.5, "gousse", "ail") == "1,5 gousse d'ail"


def test_minutes():
    assert calculs.minutes("10 min") == 10
    assert calculs.minutes("1 h 15") == 75


def test_rayons():
    assert calculs.rayon_de("tomates concassées") == "Épicerie"
    assert calculs.rayon_de("tomates mûres") == "Fruits et légumes"
    assert calculs.rayon_de("blanc de poulet halal") == "Viandes et poissons"
    assert calculs.rayon_de("pâte brisée pur beurre") == "Épicerie"
    assert calculs.rayon_de("ail") == "Fruits et légumes"
    assert calculs.rayon_de("œufs") == "Crèmerie et œufs"


def _recettes():
    return [{"id": i, "ingredients": donnees.FICHES[n]["ingredients"]}
            for i, (n, *_r) in enumerate(donnees.BASE, 1)]


def test_toutes_les_recettes_completes():
    for nom, *_ in donnees.BASE:
        f = donnees.FICHES[nom]
        assert f["ingredients"] and f["etapes"] and f["astuce"] and f["halal"], nom
        assert all(len(i) == 5 and i[3] > 0 and i[4] > 0 for i in f["ingredients"]), nom
        assert nom in donnees.EMOJIS and nom in donnees.ARTICLES_WIKI, nom


def test_agregation_et_totaux():
    recettes = _recettes()
    agg = calculs.agreger(recettes, lambda rid: 1.0)
    # l'oignon sert dans 3 recettes : une seule ligne, quantité 3
    assert agg[("oignon", "")][0] == 3
    lec, lid = calculs.totaux(recettes, lambda rid: 1.0)
    assert abs(lec - sum(v[1] for v in agg.values())) < 1e-6
    assert abs(lid - sum(v[2] for v in agg.values())) < 1e-6
    # 4 personnes = prix doublés
    lec4, _ = calculs.totaux(recettes, lambda rid: 2.0)
    assert abs(lec4 - 2 * lec) < 1e-6


def test_chaque_article_a_un_rayon_et_la_liste_est_complete():
    groupes = calculs.grouper_par_rayon(calculs.agreger(_recettes(), lambda rid: 1.0))
    total = sum(len(lignes) for _, lignes in groupes)
    assert total == len(calculs.agreger(_recettes(), lambda rid: 1.0))
    assert "Total :" in calculs.texte_liste(groupes)


def test_meilleure_enseigne():
    assert calculs.meilleure_enseigne(10, 12)[0].startswith("Leclerc")
    assert calculs.meilleure_enseigne(12, 10) == ("Lidl", 2)
    assert calculs.meilleure_enseigne(10, 10) == (None, 0.0)


def test_prix_reels_remplacent_les_estimations():
    ingr = [(300, "g", "blanc de poulet halal", 6.5, 5.9)]
    codes = {"blanc de poulet halal": {"lidl": ("123", 600)}}
    res = services.ingredients_a_jour(ingr, codes, prix_fn=lambda code, mag: 10.0)
    assert res == [(300, "g", "blanc de poulet halal", 6.5, 5.0)]      # Lidl : 10 € / 600 g × 300 g
    # sans réponse du réseau : on garde l'estimation
    assert services.ingredients_a_jour(ingr, codes, prix_fn=lambda c, m: None) == ingr


def test_photos_tolerent_les_pannes():
    def panne(lang, titre):
        return ""
    res = services.photos_pour({"A": ("en", "x"), "B": ("fr", "y")}, recuperer=panne)
    assert res == {"A": "", "B": ""}


if __name__ == "__main__":
    for nom, fonction in sorted(globals().items()):
        if nom.startswith("test_"):
            fonction()
            print("OK", nom)
