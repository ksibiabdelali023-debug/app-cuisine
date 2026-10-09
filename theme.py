"""Thèmes accessibles (sans Streamlit). Chaque paire fond/texte respecte le rapport de
contraste WCAG AA (4,5:1 minimum). Le mode « contraste élevé » est noir sur blanc (AAA)."""
from string import Template

TAILLES = {"Normale": 100, "Grande": 125, "Très grande": 150}

NORMAL = {
    "fond_page": "#FFFBF5", "carte": "#FFFFFF", "texte": "#1F2937", "texte_doux": "#374151",
    "contour": "#FDBA74", "focus": "#1D4ED8",
    "accent": "#7C2D12", "accent_txt": "#FFFFFF",
    "prim_bg": "#C2410C", "prim_txt": "#FFFFFF",
    "sec_bg": "#FFFFFF", "sec_txt": "#7C2D12", "sec_bord": "#7C2D12",
    "hero_bg1": "#7C2D12", "hero_bg2": "#B91C1C", "hero_txt": "#FFFFFF",
    "chip_bord": "transparent",
    "chip_entree_bg": "#D1FAE5", "chip_entree_txt": "#065F46",
    "chip_plat_bg": "#FFEDD5", "chip_plat_txt": "#9A3412",
    "chip_dessert_bg": "#FCE7F3", "chip_dessert_txt": "#9D174D",
    "chip_tps_bg": "#E0F2FE", "chip_tps_txt": "#075985",
    "chip_dif_bg": "#EDE9FE", "chip_dif_txt": "#5B21B6",
    "chip_pers_bg": "#FEF3C7", "chip_pers_txt": "#92400E",
    "chip_halal_bg": "#DCFCE7", "chip_halal_txt": "#166534",
    "prix_bg": "#166534", "prix_txt": "#FFFFFF",
    "leclerc_bg": "#1E3A8A", "leclerc_txt": "#FFFFFF",
    "lidl_bg": "#FDE047", "lidl_txt": "#422006",
    "gagnant_bg": "#14532D", "gagnant_txt": "#FFFFFF",
    "astuce_bg": "#FFF3C4", "halalbox_bg": "#E8F7EC",
}

ELEVE = {k: "#FFFFFF" for k in NORMAL}
ELEVE.update({
    "texte": "#000000", "texte_doux": "#000000", "contour": "#000000", "focus": "#000000",
    "accent": "#000000", "prim_bg": "#000000", "sec_txt": "#000000", "sec_bord": "#000000",
    "hero_bg1": "#000000", "hero_bg2": "#000000", "chip_bord": "#000000",
    "prix_bg": "#000000", "leclerc_bg": "#000000", "gagnant_bg": "#000000",
    "lidl_txt": "#000000",
})
for _nom in ("entree", "plat", "dessert", "tps", "dif", "pers", "halal"):
    ELEVE[f"chip_{_nom}_txt"] = "#000000"

PAIRES = [("fond_page", "texte"), ("carte", "texte"), ("carte", "texte_doux"), ("fond_page", "texte_doux"),
          ("accent", "accent_txt"), ("prim_bg", "prim_txt"), ("sec_bg", "sec_txt"),
          ("hero_bg1", "hero_txt"), ("hero_bg2", "hero_txt"),
          ("prix_bg", "prix_txt"), ("leclerc_bg", "leclerc_txt"), ("lidl_bg", "lidl_txt"),
          ("gagnant_bg", "gagnant_txt"), ("astuce_bg", "texte"), ("halalbox_bg", "texte")] + [
    (f"chip_{n}_bg", f"chip_{n}_txt") for n in ("entree", "plat", "dessert", "tps", "dif", "pers", "halal")]


def _luminance(hexa):
    h = hexa.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(fond, texte):
    a, b = sorted((_luminance(fond), _luminance(texte)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def paires_insuffisantes(palette, minimum=4.5):
    return [(f, t, round(contraste(palette[f], palette[t]), 2)) for f, t in PAIRES
            if contraste(palette[f], palette[t]) < minimum]


_CSS = Template("""
<style>
    html {font-size: ${pct}%;}
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: ${fond_page};}
    .block-container {padding-top: 1rem; padding-bottom: 5rem; max-width: 760px;}
    *:focus-visible {outline: 3px solid ${focus} !important; outline-offset: 2px !important;}

    /* Textes Streamlit à faible contraste par défaut */
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {color: ${texte_doux} !important; opacity: 1 !important;}
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {color: ${texte} !important;}
    input::placeholder, textarea::placeholder {color: ${texte_doux} !important; opacity: 1 !important;}
    input, textarea, [data-baseweb="select"] > div {border: 2px solid ${sec_bord} !important; border-radius: 12px !important;}

    /* Force le rendu clair même si le téléphone est en mode sombre */
    :root, .stApp {color-scheme: light !important;}
    input, textarea, [data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {
        background: ${carte} !important; color: ${texte} !important; -webkit-text-fill-color: ${texte} !important;}
    [data-baseweb="select"] *, [data-baseweb="select"] svg {color: ${texte} !important; fill: ${texte} !important;}
    [data-baseweb="popover"] ul, [data-baseweb="popover"] li, [data-baseweb="menu"] {
        background: ${carte} !important; color: ${texte} !important;}
    [data-testid="stRadio"] label, [data-testid="stRadio"] label * {color: ${texte} !important; opacity: 1 !important;}
    [data-testid="stRadio"] [role="radio"] > div:first-child, [data-testid="stRadio"] label > div:first-child {
        background: ${carte} !important; border-color: ${sec_bord} !important;}
    [data-testid="stCheckbox"] label, [data-testid="stCheckbox"] label *,
    [data-testid="stToggle"] label, [data-testid="stToggle"] label * {color: ${texte} !important;}
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {color: ${texte} !important;}
    [data-testid="stSidebar"] {background: ${carte} !important;}

    .sr-only {position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap;}

    .hero {background: linear-gradient(120deg, ${hero_bg1}, ${hero_bg2}); border: 3px solid ${contour};
           border-radius: 22px; padding: 24px 20px; margin-bottom: 14px;}
    .hero h1, .hero p {color: ${hero_txt} !important; margin: 0; padding: 0;}
    .hero h1 {font-size: 2rem;}
    .hero p {margin-top: 6px; font-size: 1.05rem;}
    .resume {background: ${accent}; color: ${accent_txt}; border-radius: 14px; padding: 12px 16px;
             font-weight: 700; margin-bottom: 14px;}

    .stTabs [data-baseweb="tab-list"] {gap: 6px; background: ${carte}; padding: 6px; border-radius: 18px;
           border: 2px solid ${contour};}
    .stTabs [data-baseweb="tab"] {flex: 1; justify-content: center; min-height: 48px; border-radius: 12px;
           font-weight: 700; font-size: 1rem; background: transparent;}
    .stTabs [data-baseweb="tab"] * {color: ${texte} !important;}
    .stTabs [aria-selected="true"] {background: ${accent} !important;}
    .stTabs [aria-selected="true"] * {color: ${accent_txt} !important;}
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display: none;}

    div[data-testid="stVerticalBlockBorderWrapper"] {background: ${carte}; border: 2px solid ${contour};
           border-radius: 18px;}

    .visuel {position: relative; overflow: hidden; border-radius: 14px; display: flex;
             align-items: center; justify-content: center; border: 2px solid ${contour};}
    .visuel .emo {font-size: 56px;}
    .visuel .photo {position: absolute; inset: 0; background-size: cover; background-position: center;}

    .titre {font-weight: 800; font-size: 1.2rem; margin: 12px 0 8px 0; line-height: 1.3; color: ${texte} !important;}

    .chip {display: inline-block; border: 2px solid ${chip_bord}; border-radius: 20px; padding: 4px 12px;
           font-size: 0.9rem; font-weight: 700; margin: 0 6px 6px 0;}
    .chip.c-entree {background: ${chip_entree_bg}; color: ${chip_entree_txt};}
    .chip.c-plat {background: ${chip_plat_bg}; color: ${chip_plat_txt};}
    .chip.c-dessert {background: ${chip_dessert_bg}; color: ${chip_dessert_txt};}
    .chip.tps {background: ${chip_tps_bg}; color: ${chip_tps_txt};}
    .chip.dif {background: ${chip_dif_bg}; color: ${chip_dif_txt};}
    .chip.pers {background: ${chip_pers_bg}; color: ${chip_pers_txt};}
    .chip.halal {background: ${chip_halal_bg}; color: ${chip_halal_txt};}
    .chip.typ {background: ${chip_pers_bg}; color: ${chip_pers_txt};}
    .prix {display: inline-block; background: ${prix_bg}; color: ${prix_txt}; font-weight: 800;
           padding: 6px 14px; border-radius: 20px; margin: 4px 0 10px;}

    /* Filtres Catégorie / Type de plat (st.pills) */
    [data-testid="stButtonGroup"] {gap: 8px; flex-wrap: wrap;}
    [data-testid="stButtonGroup"] button, button[data-testid^="stBaseButton-pills"] {
        min-height: 44px; padding: 6px 16px; border: 2px solid ${sec_bord} !important; border-radius: 22px !important;
        background: ${carte} !important; font-weight: 700;}
    [data-testid="stButtonGroup"] button *, button[data-testid^="stBaseButton-pills"] * {
        color: ${texte} !important; opacity: 1 !important;}
    [data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[aria-pressed="true"],
    button[data-testid="stBaseButton-pillsActive"] {background: ${accent} !important; border-color: ${accent} !important;}
    [data-testid="stButtonGroup"] button[aria-checked="true"] *, [data-testid="stButtonGroup"] button[aria-pressed="true"] *,
    button[data-testid="stBaseButton-pillsActive"] * {color: ${accent_txt} !important;}

    /* Boutons des cartes recette : « Voir la recette » / « Ajouter » côte à côte */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] {gap: 10px;}
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
        min-height: 52px; font-size: 1.05rem; box-shadow: 0 2px 0 ${sec_bord}; white-space: normal;}
    .stButton > button, .stDownloadButton > button {min-height: 48px; width: 100%; border-radius: 14px;
           font-weight: 700; font-size: 1rem; border: 2px solid ${sec_bord}; background: ${sec_bg};}
    .stButton > button *, .stDownloadButton > button * {color: ${sec_txt} !important;}
    .stButton > button[kind="primary"], button[data-testid="stBaseButton-primary"] {background: ${prim_bg}; border-color: ${prim_bg};}
    .stButton > button[kind="primary"] *, button[data-testid="stBaseButton-primary"] * {color: ${prim_txt} !important;}

    .mcard {border-radius: 16px; padding: 14px 16px; font-weight: 600; display: flex;
            flex-direction: column; gap: 2px; border: 3px solid ${contour};}
    .mcard b {font-size: 1.7rem;}
    .mcard.leclerc {background: ${leclerc_bg}; color: ${leclerc_txt};}
    .mcard.lidl {background: ${lidl_bg}; color: ${lidl_txt};}
    .gagnant {background: ${gagnant_bg}; color: ${gagnant_txt}; border-radius: 16px; padding: 16px;
              font-size: 1.1rem; margin: 12px 0; text-align: center;}
    .astuce {background: ${astuce_bg}; color: ${texte}; border-left: 6px solid ${accent}; border-radius: 12px;
             padding: 12px 14px; margin-top: 14px;}
    .halalbox {background: ${halalbox_bg}; color: ${texte}; border-left: 6px solid ${accent}; border-radius: 12px;
               padding: 12px 14px; margin-top: 10px;}
</style>
""")


def css(palette, pourcentage=100):
    return _CSS.safe_substitute(pct=pourcentage, **palette)
