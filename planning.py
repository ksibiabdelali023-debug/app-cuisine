"""Planning des repas (sans Streamlit) : {date ISO: {repas: [id_recette, ...]}}."""
from datetime import date, timedelta

REPAS = ("Déjeuner", "Dîner")
ICONES_REPAS = {"Déjeuner": "☀️", "Dîner": "🌙"}
JOURS = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche")
MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre")


def lundi(d):
    return d - timedelta(days=d.weekday())


def semaine(debut):
    return [debut + timedelta(days=i) for i in range(7)]


def libelle_jour(d):
    return f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]}"


def ajouter(plan, iso, repas, rid):
    """Ajoute une recette à un repas. False si elle y est déjà ou si le repas est inconnu."""
    if repas not in REPAS:
        return False
    liste = plan.setdefault(iso, {}).setdefault(repas, [])
    if rid in liste:
        return False
    liste.append(rid)
    return True


def retirer(plan, iso, repas, rid):
    liste = plan.get(iso, {}).get(repas, [])
    if rid in liste:
        liste.remove(rid)
    if not liste:                                  # nettoie les repas / jours vides
        plan.get(iso, {}).pop(repas, None)
        if iso in plan and not plan[iso]:
            del plan[iso]


def ids_du_jour(plan, iso):
    return [rid for repas in REPAS for rid in plan.get(iso, {}).get(repas, [])]


def ids_semaine(plan, debut):
    """Recettes planifiées sur la semaine, sans doublon, dans l'ordre du calendrier."""
    vus = []
    for jour in semaine(debut):
        for rid in ids_du_jour(plan, jour.isoformat()):
            if rid not in vus:
                vus.append(rid)
    return vus


def vider_semaine(plan, debut):
    for jour in semaine(debut):
        plan.pop(jour.isoformat(), None)


def texte_planning(plan, par_id, debut):
    """Planning de la semaine au format texte (téléchargeable)."""
    lignes = []
    for jour in semaine(debut):
        iso = jour.isoformat()
        lignes.append(libelle_jour(jour).upper())
        for repas in REPAS:
            noms = [par_id[rid]["nom"] for rid in plan.get(iso, {}).get(repas, []) if rid in par_id]
            lignes.append(f"  {repas} : " + (", ".join(noms) if noms else "-"))
        lignes.append("")
    return "\n".join(lignes)
