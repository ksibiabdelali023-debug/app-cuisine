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
    "ov_bg": "#111827", "ov_txt": "#FFFFFF",      # pastilles posées sur les photos
    "epais": "1px",                               # épaisseur des contours (3px en contraste élevé)
}

ELEVE = {k: "#FFFFFF" for k in NORMAL}
ELEVE.update({
    "texte": "#000000", "texte_doux": "#000000", "contour": "#000000", "focus": "#000000",
    "accent": "#000000", "prim_bg": "#000000", "sec_txt": "#000000", "sec_bord": "#000000",
    "hero_bg1": "#000000", "hero_bg2": "#000000", "chip_bord": "#000000",
    "prix_bg": "#000000", "leclerc_bg": "#000000", "gagnant_bg": "#000000",
    "lidl_txt": "#000000", "ov_bg": "#000000", "epais": "3px",
})
for _nom in ("entree", "plat", "dessert", "tps", "dif", "pers", "halal"):
    ELEVE[f"chip_{_nom}_txt"] = "#000000"

PAIRES = [("fond_page", "texte"), ("carte", "texte"), ("carte", "texte_doux"), ("fond_page", "texte_doux"),
          ("accent", "accent_txt"), ("prim_bg", "prim_txt"), ("sec_bg", "sec_txt"),
          ("hero_bg1", "hero_txt"), ("hero_bg2", "hero_txt"),
          ("prix_bg", "prix_txt"), ("leclerc_bg", "leclerc_txt"), ("lidl_bg", "lidl_txt"),
          ("gagnant_bg", "gagnant_txt"), ("ov_bg", "ov_txt"), ("astuce_bg", "texte"), ("halalbox_bg", "texte")] + [
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
    :root, .stApp {color-scheme: light !important;}
    .stApp {background: ${fond_page};}
    .block-container {padding: 0.75rem 0.9rem 7rem; max-width: 760px;}
    *:focus-visible {outline: 3px solid ${focus} !important; outline-offset: 2px !important;}
    .sr-only {position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap;}

    /* ---------- Textes natifs : toujours lisibles, même si le téléphone est en mode sombre ---------- */
    [data-testid="stMarkdownContainer"] > p, [data-testid="stMarkdownContainer"] > ul li,
    [data-testid="stMarkdownContainer"] > ol li, [data-testid="stMarkdownContainer"] > p strong {color: ${texte};}
    [data-testid="stHeading"], [data-testid="stHeading"] * {color: ${texte} !important;}
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {color: ${texte_doux} !important; opacity: 1 !important;}
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {color: ${texte} !important;}
    input::placeholder, textarea::placeholder {color: ${texte_doux} !important; opacity: 1 !important;}
    [data-testid="stAlert"] {background: ${astuce_bg} !important; border: ${epais} solid ${contour}; border-radius: 16px;}
    [data-testid="stAlert"] * {color: ${texte} !important;}
    [data-testid="stExpander"] {background: ${carte}; border: ${epais} solid ${contour}; border-radius: 16px;}
    [data-testid="stExpander"] details, [data-testid="stExpander"] summary {background: ${carte} !important; border-radius: 16px;}
    [data-testid="stExpander"] summary, [data-testid="stExpander"] summary * {color: ${texte} !important; font-weight: 700;}
    [data-testid="stExpander"] svg {fill: ${texte} !important; color: ${texte} !important;}
    div[role="dialog"], [data-testid="stDialog"] > div > div {background: ${fond_page} !important;}
    div[role="dialog"] svg {fill: ${texte} !important;}

    /* ---------- Champs de saisie, listes, cases ---------- */
    [data-testid="stTextInputRootElement"], [data-testid="stNumberInputContainer"], [data-testid="stTextAreaRootElement"] {
        background: transparent !important; border: none !important; box-shadow: none !important;}
    [data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
        background: ${carte} !important; border: 2px solid ${sec_bord} !important; border-radius: 14px !important;
        min-height: 48px;}
    [data-baseweb="base-input"] {background: transparent !important; border: none !important;}
    input, textarea {background: transparent !important; border: none !important; color: ${texte} !important;
        -webkit-text-fill-color: ${texte} !important;}
    [data-testid="stNumberInputContainer"] button {background: ${carte} !important; color: ${texte} !important;}
    [data-baseweb="select"] *, [data-baseweb="select"] svg {color: ${texte} !important; fill: ${texte} !important;}
    [data-baseweb="popover"] ul, [data-baseweb="popover"] li, [data-baseweb="menu"] {
        background: ${carte} !important; color: ${texte} !important;}
    [data-testid="stRadio"] label, [data-testid="stRadio"] label * {color: ${texte} !important; opacity: 1 !important;}
    [data-testid="stRadio"] [role="radio"] > div:first-child, [data-testid="stRadio"] label > div:first-child {
        background: ${carte} !important; border-color: ${sec_bord} !important;}
    [data-testid="stCheckbox"] label, [data-testid="stCheckbox"] label *,
    [data-testid="stToggle"] label, [data-testid="stToggle"] label * {color: ${texte} !important;}
    [data-baseweb="calendar"], [data-baseweb="datepicker"] {background: ${carte} !important;}
    [data-baseweb="calendar"] *, [data-baseweb="datepicker"] * {color: ${texte} !important;}
    [data-baseweb="calendar"] [aria-selected="true"], [data-baseweb="calendar"] [aria-selected="true"] * {
        background: ${accent} !important; color: ${accent_txt} !important;}
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {color: ${texte} !important;}
    [data-testid="stSidebar"] {background: ${carte} !important;}

    /* ---------- En-tête compact et bandeau panier ---------- */
    .hero {background: linear-gradient(120deg, ${hero_bg1}, ${hero_bg2}); border: ${epais} solid ${contour};
           border-radius: 20px; padding: 14px 16px; margin-bottom: 10px;}
    .hero .ligne {display: flex; align-items: center; gap: 12px;}
    .hero .logo {font-size: 2.1rem; line-height: 1;}
    .hero h1, .hero p {color: ${hero_txt} !important; margin: 0; padding: 0;}
    .hero h1 {font-size: 1.5rem; font-weight: 800; line-height: 1.15;}
    .hero p {margin-top: 2px; font-size: 0.9rem;}
    .resume {background: ${accent}; color: ${accent_txt}; border-radius: 14px; padding: 9px 14px;
             font-weight: 700; font-size: 0.92rem; margin-bottom: 10px;}

    /* ---------- Navigation en bas de l'écran (comme une vraie appli) ---------- */
    .stTabs [data-baseweb="tab-list"] {position: fixed; left: 0; right: 0; bottom: 0; z-index: 1000; margin: 0;
           gap: 4px; background: ${carte}; border: none; border-top: ${epais} solid ${contour}; border-radius: 0;
           padding: 6px 6px calc(6px + env(safe-area-inset-bottom, 0px)); box-shadow: 0 -6px 18px rgba(0,0,0,0.08);}
    .stTabs [data-baseweb="tab"] {flex: 1; justify-content: center; min-height: 48px; padding: 0 2px;
           border-radius: 14px; font-weight: 700; font-size: 0.78rem; background: transparent; white-space: nowrap;}
    .stTabs [data-baseweb="tab"], .stTabs [data-baseweb="tab"] * {color: ${texte} !important; opacity: 1 !important;}
    .stTabs [aria-selected="true"] {background: ${accent} !important;}
    .stTabs [aria-selected="true"] * {color: ${accent_txt} !important;}
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display: none;}

    /* ---------- Filtres horizontaux défilables (Catégorie / Type de plat) ---------- */
    [data-testid="stButtonGroup"] {gap: 8px; flex-wrap: nowrap !important; overflow-x: auto; padding: 2px 2px 8px;
           -webkit-overflow-scrolling: touch; scrollbar-width: none;}
    [data-testid="stButtonGroup"]::-webkit-scrollbar {display: none;}
    [data-testid="stButtonGroup"] button, button[data-testid^="stBaseButton-pills"] {
        flex: 0 0 auto; white-space: nowrap; min-height: 42px; padding: 4px 16px; font-weight: 700;
        border: 2px solid ${sec_bord} !important; border-radius: 22px !important; background: ${carte} !important;}
    [data-testid="stButtonGroup"] button *, button[data-testid^="stBaseButton-pills"] * {
        color: ${texte} !important; opacity: 1 !important;}
    [data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[aria-pressed="true"],
    button[data-testid="stBaseButton-pillsActive"] {background: ${accent} !important; border-color: ${accent} !important;}
    [data-testid="stButtonGroup"] button[aria-checked="true"] *, [data-testid="stButtonGroup"] button[aria-pressed="true"] *,
    button[data-testid="stBaseButton-pillsActive"] * {color: ${accent_txt} !important;}

    /* ---------- Cartes recette ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {background: ${carte}; border: ${epais} solid ${contour};
           border-radius: 22px; padding: 6px; box-shadow: 0 8px 22px rgba(124,45,18,0.10); overflow: hidden;}
    .visuel {position: relative; overflow: hidden; border-radius: 17px; display: flex;
             align-items: center; justify-content: center;}
    .visuel .emo {font-size: 56px;}
    .visuel .photo {position: absolute; inset: 0; background-size: cover; background-position: center;}
    .ov {position: absolute; z-index: 2; background: ${ov_bg}; color: ${ov_txt}; font-weight: 700; font-size: 0.82rem;
         padding: 4px 11px; border-radius: 14px; line-height: 1.3;}
    .ov.hg {left: 10px; top: 10px;} .ov.bg {left: 10px; bottom: 10px;} .ov.bd {right: 10px; bottom: 10px;}
    .titre {font-weight: 800; font-size: 1.12rem; margin: 10px 4px 2px; line-height: 1.3; color: ${texte} !important;}
    .meta {color: ${texte_doux}; font-size: 0.9rem; margin: 0 4px 6px;}
    .puces {margin: 0 4px;}

    .chip {display: inline-block; border: ${epais} solid ${chip_bord}; border-radius: 20px; padding: 3px 11px;
           font-size: 0.82rem; font-weight: 700; margin: 0 6px 6px 0;}
    .chip.c-entree {background: ${chip_entree_bg}; color: ${chip_entree_txt};}
    .chip.c-plat {background: ${chip_plat_bg}; color: ${chip_plat_txt};}
    .chip.c-dessert {background: ${chip_dessert_bg}; color: ${chip_dessert_txt};}
    .chip.tps {background: ${chip_tps_bg}; color: ${chip_tps_txt};}
    .chip.dif {background: ${chip_dif_bg}; color: ${chip_dif_txt};}
    .chip.pers {background: ${chip_pers_bg}; color: ${chip_pers_txt};}
    .chip.halal {background: ${chip_halal_bg}; color: ${chip_halal_txt};}
    .chip.typ {background: ${chip_pers_bg}; color: ${chip_pers_txt};}
    .prix {display: inline-block; background: ${prix_bg}; color: ${prix_txt} !important; font-weight: 800; font-size: 0.92rem;
           padding: 5px 13px; border-radius: 20px; margin: 4px 4px 8px;}

    /* ---------- Boutons ---------- */
    .stButton, .stDownloadButton, [data-testid="stTooltipHoverTarget"] {width: 100%;}
    .stButton button, .stDownloadButton button {min-height: 48px; width: 100%; border-radius: 14px;
           font-weight: 700; font-size: 1rem; border: 2px solid ${sec_bord}; background: ${sec_bg};}
    .stButton button *, .stDownloadButton button * {color: ${sec_txt} !important;}
    .stButton button[kind="primary"], button[data-testid="stBaseButton-primary"] {background: ${prim_bg}; border-color: ${prim_bg};}
    .stButton button[kind="primary"] *, button[data-testid="stBaseButton-primary"] * {color: ${prim_txt} !important;}
    /* Les rangées qui contiennent des boutons (ou les totaux) restent côte à côte sur téléphone */
    [data-testid="stHorizontalBlock"]:has(.stButton), [data-testid="stHorizontalBlock"]:has(.mcard) {
        flex-direction: row !important; flex-wrap: nowrap !important; gap: 8px;}
    [data-testid="stHorizontalBlock"]:has(.stButton) > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"]:has(.mcard) > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"]:has(.stButton) > div[data-testid="column"],
    [data-testid="stHorizontalBlock"]:has(.mcard) > div[data-testid="column"] {
        min-width: 0 !important; width: auto !important; flex: 1 1 0 !important;}
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton button {min-height: 50px; font-size: 1rem;}

    /* ---------- Courses ---------- */
    .mcard {border-radius: 16px; padding: 12px 14px; font-weight: 600; display: flex;
            flex-direction: column; gap: 2px; border: ${epais} solid ${contour};}
    .mcard b {font-size: 1.5rem;}
    .mcard.leclerc {background: ${leclerc_bg}; color: ${leclerc_txt} !important;}
    .mcard.lidl {background: ${lidl_bg}; color: ${lidl_txt} !important;}
    .mcard.leclerc *, .mcard.leclerc b {color: ${leclerc_txt} !important;}
    .mcard.lidl *, .mcard.lidl b {color: ${lidl_txt} !important;}
    .gagnant {background: ${gagnant_bg}; color: ${gagnant_txt}; border-radius: 16px; padding: 16px;
              font-size: 1.1rem; margin: 12px 0; text-align: center;}
    .gagnant * {color: ${gagnant_txt} !important;}
    .astuce {background: ${astuce_bg}; color: ${texte}; border-left: 6px solid ${accent}; border-radius: 12px;
             padding: 12px 14px; margin-top: 14px;}
    .halalbox {background: ${halalbox_bg}; color: ${texte}; border-left: 6px solid ${accent}; border-radius: 12px;
               padding: 12px 14px; margin-top: 10px;}
    .astuce *, .halalbox * {color: ${texte} !important;}
</style>
""")


def css(palette, pourcentage=100):
    return _CSS.safe_substitute(pct=pourcentage, **palette)
