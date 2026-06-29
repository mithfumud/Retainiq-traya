import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from churn import calculate_churn_score, get_risk_label
from data import df

st.set_page_config(
    page_title="RetainIQ · Traya",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def build_scored_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    out = raw_df.copy()
    out["churn_score"] = out.apply(calculate_churn_score, axis=1)
    out["risk_label"]  = out["churn_score"].apply(get_risk_label)
    return out

df        = build_scored_df(df)
df_active = df[df["status"] == "active"].copy()

# ── Aggregates (needed before sidebar renders) ────────────────────────────────
N         = len(df)
active_n  = int((df["status"] == "active").sum())
m3_pct    = round((df["months_active"] >= 3).sum() / N * 100, 1)
hi        = int((df_active["risk_label"] == "High").sum())
med       = int((df_active["risk_label"] == "Medium").sum())
lo        = int((df_active["risk_label"] == "Low").sum())
total_mrr = int(df_active["mrr"].sum())

# ════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"] {
    background: #F8FAFC !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}

#MainMenu, footer { display: none !important; }
header[data-testid="stHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    display: none !important;
    visibility: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
}
[data-testid="stDecoration"] { display: none !important; }

[data-testid="stMainBlockContainer"],
.main .block-container {
    padding: 0 20px 0 24px !important;
    margin-top: 0 !important;
    max-width: 100% !important;
    background: #F8FAFC !important;
}
section.main {
    padding-top: 0 !important;
}
[data-testid="stAppViewContainer"] > .main {
    padding-top: 0 !important;
}
[data-testid="stMarkdownContainer"] {
    margin: 0 !important;
    padding: 0 !important;
}

/* ── Hide sidebar collapse chrome ── */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
[data-testid="stSidebarResizer"] { display: none !important; }

/* ════════════════════════════════
   SIDEBAR
════════════════════════════════ */
section[data-testid="stSidebar"] {
    width: 210px !important;
    min-width: 210px !important;
    max-width: 210px !important;
    background: linear-gradient(180deg, #166534 0%, #15803D 100%) !important;
    border-right: 1px solid #14532D !important;
    display: flex !important;
    flex-direction: column !important;
    transform: none !important;
    visibility: visible !important;
    top: 0 !important;
    margin-top: 0 !important;
    height: 100vh !important;
    z-index: 2 !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    display: none !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    width: 210px !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    background: linear-gradient(180deg, #166534 0%, #15803D 100%) !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
    padding-top: 0 !important;
    background: transparent !important;
}
section[data-testid="stSidebar"] .block-container > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdown"]:first-of-type,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:first-of-type {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* ── Brand ── */
.sb-brand {
    padding: 14px 12px 12px 12px;
    margin: 0;
    border-bottom: 1px solid rgba(255,255,255,0.15);
}
.sb-name { font-size: 1.7rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.6px; line-height: 1; }
.sb-sub  { font-size: 0.66rem; font-weight: 600; color: rgba(255,255,255,0.7); letter-spacing: 1.4px; text-transform: uppercase; margin-top: 4px; }

/* ── Section label ── */
.sb-section {
    font-size: 0.52rem; font-weight: 600; color: rgba(255,255,255,0.45);
    text-transform: uppercase; letter-spacing: 1.6px;
    padding: 10px 14px 4px;
}

/* ── Radio nav ── */
section[data-testid="stSidebar"] .stRadio > label { display: none !important; }

section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    gap: 2px !important;
    padding: 0 10px !important;
}

section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    padding: 6px 10px !important;
    border-radius: 6px !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
    transition: background 0.14s ease, border-color 0.14s ease !important;
    margin: 0 !important;
    position: relative !important;
}

/* Invisible but fully clickable radio input */
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input[type="radio"] {
    position: absolute !important;
    opacity: 0 !important;
    width: 100% !important;
    height: 100% !important;
    top: 0 !important; left: 0 !important;
    margin: 0 !important;
    cursor: pointer !important;
    z-index: 2 !important;
}

section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
    font-size: 0.74rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.75) !important;
    margin: 0 !important; padding: 0 !important;
    font-family: 'Inter', sans-serif !important;
    pointer-events: none !important;
    z-index: 1 !important; position: relative !important;
    transition: color 0.14s ease !important;
}

section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.1) !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover p {
    color: #FFFFFF !important;
}

/* Active state — left accent only, no box border */
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
    background: rgba(255,255,255,0.12) !important;
    border-color: transparent !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked)::before {
    content: '';
    position: absolute;
    left: 0; top: 50%; transform: translateY(-50%);
    width: 3px; height: 60%;
    background: #FFFFFF;
    border-radius: 0 3px 3px 0;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* ── Sidebar footer ── */
.sb-footer-wrap {
    margin-top: auto;
    border-top: 1px solid rgba(255,255,255,0.15);
    padding: 10px 14px 14px;
}
.sb-live-row { display:flex; align-items:center; gap:6px; margin-bottom:6px; }
.sb-pulse {
    width: 6px; height: 6px; border-radius: 50%; background: #FFFFFF; flex-shrink: 0;
    box-shadow: 0 0 0 3px rgba(255,255,255,0.2);
    animation: pulse 2.4s ease infinite;
}
@keyframes pulse {
    0%,100% { box-shadow: 0 0 0 3px rgba(255,255,255,0.2); }
    50%      { box-shadow: 0 0 0 7px rgba(255,255,255,0.06); }
}
.sb-live-txt { font-size: 0.62rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase; letter-spacing: 1px; }
.sb-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }
.sb-stat  { background: rgba(255,255,255,0.08); border: none; border-radius: 6px; padding: 5px 7px; }
.sb-stat-val { font-size: 0.72rem; font-weight: 600; color: #FFFFFF; letter-spacing: -0.3px; font-family: 'JetBrains Mono', ui-monospace, monospace; }
.sb-stat-lbl { font-size: 0.52rem; color: rgba(255,255,255,0.65); margin-top: 1px; }

/* ════════════════════════════════
   GLOBAL TOPBAR (full-width, above content)
════════════════════════════════ */
.g-topbar {
    background: linear-gradient(90deg, #166534 0%, #15803D 100%);
    height: 38px; padding: 0 16px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid rgba(0,0,0,0.12);
    position: relative;
    margin: 0;
    z-index: 1;
}
.gt-left  { display: flex; align-items: center; gap: 10px; }
.gt-brand { font-size: 0.76rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.2px; }
.gt-divider { width: 1px; height: 14px; background: rgba(255,255,255,0.25); }
.gt-page  { font-size: 0.68rem; color: rgba(255,255,255,0.75); font-weight: 400; }
.gt-right { display: flex; align-items: center; gap: 6px; }
.badge {
    border-radius: 5px; padding: 3px 9px;
    font-size: 0.62rem; font-weight: 600; letter-spacing: 0.2px;
    display: inline-flex; align-items: center; gap: 4px;
}
.b-neutral { background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.9); border: none; }
.b-green   { background: rgba(255,255,255,0.16); color: #FFFFFF;              border: none; }

/* ── Page-level topbar (per-page subtitle / badges) ── */
.pg-bar {
    background: #fff;
    height: 32px; padding: 0 16px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: none;
    box-shadow: 0 1px 0 #F1F5F9;
    position: relative;
    margin: 0;
    z-index: 1;
}
.pg-title { font-size: 0.7rem; font-weight: 600; color: #0F172A; }
.pg-right { display: flex; align-items: center; gap: 6px; }

/* ── On-page badges (dark bg context) ── */
.pb-neutral { background: #F8FAFC; color: #64748B; border: none; border-radius: 5px; padding: 3px 9px; font-size: 0.62rem; font-weight: 600; }
.pb-green   { background: #F0FDF4; color: #15803D; border: none; border-radius: 5px; padding: 3px 9px; font-size: 0.62rem; font-weight: 600; }
.pb-red     { background: #FEF2F2; color: #DC2626; border: none; border-radius: 5px; padding: 3px 9px; font-size: 0.62rem; font-weight: 600; }

/* ════════════════════════════════
   PAGE BODY
════════════════════════════════ */
.page-body { padding: 8px 0 10px; }
.section-label {
    font-size: 0.58rem; font-weight: 700; color: #64748B;
    text-transform: uppercase; letter-spacing: 1.3px; margin: 10px 0 6px;
}

/* ════════════════════════════════
   KPI CARDS
════════════════════════════════ */
[data-testid="stMetric"],
[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 12px 8px 14px !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05) !important;
    position: relative !important;
    overflow: visible !important;
    margin-top: 0 !important;
    min-height: 62px !important;
}
[data-testid="stMetric"]::before,
[data-testid="metric-container"]::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: #16A34A;
    border-radius: 8px 0 0 8px;
    z-index: 0;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] div,
[data-testid="metric-container"] label,
[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    color: #64748B !important;
    font-family: 'Inter', sans-serif !important;
    margin: 0 0 4px 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;
    position: relative !important;
    z-index: 1 !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div,
[data-testid="metric-container"] [data-testid="stMetricValue"] div {
    display: block !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.5px !important;
    line-height: 1.15 !important;
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
    position: relative !important;
    z-index: 1 !important;
}
[data-testid="stMetricDelta"] { display: none !important; }

/* ════════════════════════════════
   CARD SHELL
════════════════════════════════ */
.card {
    background: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 10px 4px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05);
    margin-bottom: 6px;
    height: 100%;
}
.card-title { font-size: 0.72rem; font-weight: 700; color: #0F172A; letter-spacing: -0.15px; margin-bottom: 1px; }
.card-sub   { font-size: 0.58rem; color: #94A3B8; line-height: 1.3; margin-bottom: 4px; }
.card-hdr-fixed { min-height: 72px; margin-bottom: 6px; }
.chan-legend {
    display: flex; flex-wrap: wrap; gap: 3px 10px;
    margin: 4px 0 0; font-size: 0.56rem; color: #64748B;
}
.chan-legend span { display: inline-flex; align-items: center; gap: 4px; white-space: nowrap; }
.chan-legend i { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }

/* ════════════════════════════════
   RISK CARDS
════════════════════════════════ */
.risk-row { display: flex; gap: 8px; margin-bottom: 10px; }
.rc { flex: 1; border-radius: 8px; padding: 10px 12px; display: flex; align-items: center; gap: 8px; border: none; }
.rc.h { background: #FEF2F2; border-left: 3px solid #EF4444; }
.rc.m { background: #FFFBEB; border-left: 3px solid #F59E0B; }
.rc.l { background: #F0FDF4; border-left: 3px solid #16A34A; }
.rc-num   { font-size: 1.15rem; font-weight: 700; letter-spacing: -0.6px; line-height: 1; font-family: 'JetBrains Mono', ui-monospace, monospace; }
.rc-num.h { color: #DC2626; }  .rc-num.m { color: #D97706; }  .rc-num.l { color: #16A34A; }
.rc-lbl   { font-size: 0.58rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }
.rc-lbl.h { color: #DC2626; }  .rc-lbl.m { color: #D97706; }  .rc-lbl.l { color: #16A34A; }
.rc-note  { font-size: 0.63rem; color: #64748B; line-height: 1.45; margin-left: auto; text-align: right; }

/* ════════════════════════════════
   FILTER BAR
════════════════════════════════ */
.fbar {
    background: #fff;
    border: none;
    border-radius: 8px;
    padding: 8px 12px 10px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05);
}
.stSelectbox > label {
    font-size: 0.58rem !important; font-weight: 600 !important;
    color: #64748B !important; text-transform: uppercase !important; letter-spacing: 1.2px !important;
}
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #E2E8F0 !important;
    border-radius: 8px !important;
    min-height: 36px !important;
    color: #0F172A !important;
}
.stSelectbox [data-baseweb="select"] > div:hover,
.stSelectbox div[data-baseweb="select"] > div:hover {
    border-color: #CBD5E1 !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within,
.stSelectbox div[data-baseweb="select"] > div:focus-within {
    border-color: #16A34A !important;
    box-shadow: 0 0 0 1px #16A34A !important;
}
.stSelectbox svg { fill: #64748B !important; }
.stSelectbox [data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] span {
    color: #0F172A !important;
    font-size: 0.8rem !important;
    font-family: 'Inter', sans-serif !important;
}

/* ════════════════════════════════
   EXPANDER
════════════════════════════════ */
[data-testid="stExpander"] {
    background: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05) !important;
    margin-bottom: 12px !important;
}
[data-testid="stExpander"] > details > summary {
    font-size: 0.78rem !important; font-weight: 600 !important;
    color: #0F172A !important; padding: 11px 14px !important;
    border-bottom: 1px solid #F1F5F9 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ════════════════════════════════
   ALERT BANNERS
════════════════════════════════ */
.bn { border-radius: 7px; padding: 8px 12px; font-size: 0.68rem; line-height: 1.45; margin-top: 8px; border: none; }
.bn b { font-weight: 700; }
.bn.warn { background: #FFFBEB; color: #451A03; border-left: 3px solid #D97706; }
.bn.info { background: #EFF6FF; color: #1E3A5F; border-left: 3px solid #2563EB; }
.bn.red  { background: #FEF2F2; color: #7F1D1D; border-left: 3px solid #EF4444; }

/* ── Insight note (calm, analyst-style callout) ── */
.insight-note {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-left: 3px solid #16A34A;
    border-radius: 8px;
    padding: 12px 14px;
    margin-top: 10px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
}
.insight-note .in-label {
    font-size: 0.55rem; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #16A34A; margin-bottom: 5px;
}
.insight-note .in-body { font-size: 0.72rem; line-height: 1.55; color: #334155; }
.insight-note .in-body b { font-weight: 700; color: #0F172A; }
.insight-note .in-action {
    font-size: 0.7rem; line-height: 1.5; color: #475569;
    margin-top: 6px; padding-top: 6px; border-top: 1px solid #F1F5F9;
}
.insight-note .in-action b { font-weight: 700; color: #0F172A; }

/* ════════════════════════════════
   LAYOUT UTILS
════════════════════════════════ */
[data-testid="stHorizontalBlock"] { gap: 6px !important; }
div[data-testid="column"]         { padding: 0 !important; }
.stVerticalBlock                  { gap: 0 !important; }
[data-testid="element-container"] { margin: 0 !important; }
[data-testid="stPlotlyChart"]     { margin-bottom: 0 !important; }
[data-testid="stPlotlyChart"] > div { height: auto !important; }
[data-testid="stVerticalBlockBorderWrapper"] { padding: 0 !important; gap: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Keep sidebar permanently visible ─────────────────────────────────────────
components.html("""<script>
(function(){
  var d = window.parent.document;
  function fix(){
    var sb = d.querySelector('[data-testid="stSidebar"]');
    if(sb){
      sb.style.setProperty('transform','none','important');
      sb.style.setProperty('visibility','visible','important');
      sb.style.setProperty('margin-left','0','important');
    }
    var tab = d.getElementById('sb-toggle-tab');
    if(tab) tab.remove();
    ['[data-testid="stSidebarCollapseButton"]','[data-testid="collapsedControl"]',
     '[data-testid="stSidebarResizer"]'].forEach(function(sel){
      d.querySelectorAll(sel).forEach(function(el){
        el.style.setProperty('display','none','important');
      });
    });
    ['[data-testid="stSidebarUserContent"]','[data-testid="stSidebarContent"]'].forEach(function(sel){
      d.querySelectorAll(sel).forEach(function(el){
        el.style.setProperty('padding-top','0','important');
        el.style.setProperty('margin-top','0','important');
      });
    });
  }
  fix();
  new MutationObserver(fix).observe(d.body,{childList:true,subtree:true});
})();
</script>""", height=0, width=0)


# ── Chart helper ──────────────────────────────────────────────────────────────
UI_FONT  = "Inter, system-ui, sans-serif"
MONO_FONT = "JetBrains Mono, ui-monospace, monospace"
AXIS_TICK  = dict(size=10, color="#0F172A", family=MONO_FONT, weight=500)
AXIS_TITLE = dict(size=10, color="#0F172A", family=UI_FONT, weight=600)


def style_chart(fig, h=140, hbar=False):
    left_margin = 112 if hbar else 44
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=UI_FONT, color="#0F172A", size=10),
        margin=dict(l=left_margin, r=12, t=8, b=40), height=h,
        hoverlabel=dict(bgcolor="#0F172A", font_color="#F8FAFC", font_size=10, font_family=MONO_FONT),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F1F5F9", zeroline=False,
                     linecolor="#E2E8F0", tickfont=AXIS_TICK, title_font=AXIS_TITLE,
                     automargin=True)
    fig.update_yaxes(showgrid=False, zeroline=False,
                     linecolor="#E2E8F0", tickfont=AXIS_TICK, title_font=AXIS_TITLE,
                     automargin=True)
    return fig


# ════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-name">Traya</div>
      <div class="sb-sub">RetainIQ</div>
    </div>
    <div class="sb-section">Analytics</div>
    """, unsafe_allow_html=True)

    NAV       = ["Overview", "Cohorts", "Churn Risk", "Segments"]

    choice = st.radio(
        "page", NAV,
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div class="sb-footer-wrap">
      <div class="sb-live-row">
        <div class="sb-pulse"></div>
        <span class="sb-live-txt">Live Data</span>
      </div>
      <div class="sb-stats">
        <div class="sb-stat">
          <div class="sb-stat-val">{N:,}</div>
          <div class="sb-stat-lbl">Total users</div>
        </div>
        <div class="sb-stat">
          <div class="sb-stat-val">{active_n:,}</div>
          <div class="sb-stat-lbl">Active</div>
        </div>
        <div class="sb-stat">
          <div class="sb-stat-val">{m3_pct}%</div>
          <div class="sb-stat-lbl">M3 retain.</div>
        </div>
        <div class="sb-stat">
          <div class="sb-stat-val">₹{total_mrr//1000}K</div>
          <div class="sb-stat-lbl">Active MRR</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  GLOBAL TOP HEADER (renders inside main area, above per-page content)
# ════════════════════════════════════════════════════════════════════════════
PAGE_LABELS = {
    "Overview":   "Overview · Hair health retention",
    "Cohorts":    "Cohort Analysis · Jan-Jun 2025",
    "Churn Risk": "Churn Risk Engine · Active users",
    "Segments":   "User Segments · 4 dimensions",
}

st.markdown(f"""
<div class="g-topbar">
  <div class="gt-left">
    <span class="gt-brand">RetainIQ</span>
    <div class="gt-divider"></div>
    <span class="gt-page">{PAGE_LABELS[choice]}</span>
  </div>
  <div class="gt-right">
    <span class="badge b-neutral">Jun 2025</span>
    <span class="badge b-green">● Live</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if choice == "Overview":
    # Per-page sub-bar
    st.markdown(f"""
    <div class="pg-bar">
      <span class="pg-title">Overview Dashboard</span>
      <div class="pg-right">
        <span class="pb-red">{hi} High Risk</span>
        <span class="pb-neutral">{active_n:,} Active</span>
        <span class="pb-green">M3 {m3_pct}%</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='page-body'>", unsafe_allow_html=True)

    # ── KPI row ──
    st.markdown("<div class='section-label'>Key Metrics</div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5, gap="small")
    c1.metric("Total Users",       f"{N:,}")
    c2.metric("Active Users",      f"{active_n:,}")
    c3.metric("M3 Retention",      f"{m3_pct}%")
    c4.metric("Active MRR",        f"₹{total_mrr // 1000}K")
    c5.metric("High Risk Active",  f"{hi}")

    # ── Funnel + Channel retention ──
    st.markdown("<div class='section-label'>Acquisition & Funnel</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")

    fn_stages = ["Took hair test","Purchased kit","M1 active","M3 active","M6 active"]
    fn_counts = [N, 375,
                 int((df["months_active"]>=1).sum()),
                 int((df["months_active"]>=3).sum()),
                 int((df["months_active"]>=6).sum())]
    ff = px.bar(pd.DataFrame({"Stage":fn_stages,"Users":fn_counts}),
                x="Users", y="Stage", orientation="h", color="Users",
                color_continuous_scale=["#DCFCE7","#15803D"])
    ff.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Users", coloraxis_showscale=False)
    ff.update_yaxes(categoryorder="array", categoryarray=fn_stages[::-1])
    style_chart(ff, 145, hbar=True)

    ch_df = df.groupby("channel", as_index=False)["months_active"].mean().sort_values("months_active")
    cf = px.bar(ch_df, x="months_active", y="channel", orientation="h", color="months_active",
                color_continuous_scale=["#DBEAFE","#1D4ED8"])
    cf.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Avg months active", coloraxis_showscale=False)
    style_chart(cf, 145, hbar=True)

    with col1:
        st.markdown('<div class="card"><div class="card-title">Conversion Funnel</div>'
                    '<div class="card-sub">Users progressing from hair test → 6-month active retention</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(ff, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">Retention by Channel</div>'
                    '<div class="card-sub">Avg months active per acquisition channel; referral leads</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(cf, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Channel matrix + Subscription ──
    st.markdown("<div class='section-label' style='margin-top:18px;margin-bottom:10px'>Channel Quality & Behaviour</div>", unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3, gap="small")

    ch_qual = df.groupby("channel").agg(
        volume=("id","count"),
        avg_retention=("months_active","mean"),
        churn_rate=("channel_churn_prob","first"),
    ).reset_index()
    scatter = px.scatter(ch_qual, x="avg_retention", y="churn_rate",
                         size="volume", color="channel", size_max=42,
                         color_discrete_sequence=["#16A34A","#D97706","#2563EB","#EF4444","#7C3AED"])
    scatter.update_traces(text=None)
    scatter.update_layout(
        xaxis_title="Avg months retained",
        yaxis_title="Churn probability",
        showlegend=False,
    )
    style_chart(scatter, 175)
    scatter.update_layout(margin=dict(l=48, r=12, t=20, b=52))

    plan_df = df.groupby("plan", as_index=False)["months_active"].mean()
    plan_df["plan"] = pd.Categorical(plan_df["plan"], ["basic","pro","premium"], ordered=True)
    pf = px.bar(plan_df.sort_values("plan"), x="plan", y="months_active", color="plan",
                color_discrete_map={"basic":"#CBD5E1","pro":"#64748B","premium":"#0F172A"})
    pf.update_layout(showlegend=False, xaxis_title="Plan", yaxis_title="Avg months active")
    style_chart(pf, 175)
    pf.update_layout(margin=dict(l=48, r=12, t=20, b=52))

    with col3:
        st.markdown("""<div class="card"><div class="card-hdr-fixed"><div class="card-title">Channel Quality Matrix</div>
                    <div class="card-sub">Bubble = volume · X = retention · Y = churn rate</div>
                    <div class="chan-legend">
                      <span><i style="background:#16A34A"></i>google</span>
                      <span><i style="background:#D97706"></i>instagram</span>
                      <span><i style="background:#2563EB"></i>organic</span>
                      <span><i style="background:#EF4444"></i>referral</span>
                      <span><i style="background:#7C3AED"></i>youtube</span>
                    </div></div>""", unsafe_allow_html=True)
        st.plotly_chart(scatter, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card"><div class="card-hdr-fixed"><div class="card-title">Retention by Plan</div>'
                    '<div class="card-sub">Premium subscribers retain longer. Upsell lever</div></div>',
                    unsafe_allow_html=True)
        st.plotly_chart(pf, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    stress_df = df.groupby("stress_level", as_index=False)["months_active"].mean()
    stress_df["stress_level"] = pd.Categorical(stress_df["stress_level"], ["low","medium","high"], ordered=True)
    sf = px.bar(stress_df.sort_values("stress_level"), x="stress_level", y="months_active", color="stress_level",
                color_discrete_map={"low":"#16A34A","medium":"#D97706","high":"#EF4444"})
    sf.update_layout(showlegend=False, xaxis_title="Stress level", yaxis_title="Avg months active")
    style_chart(sf, 175)
    sf.update_layout(margin=dict(l=48, r=12, t=20, b=52))
    with col5:
        st.markdown('<div class="card"><div class="card-hdr-fixed"><div class="card-title">Retention by Stress</div>'
                    '<div class="card-sub">High-stress users churn faster; coach trigger</div></div>',
                    unsafe_allow_html=True)
        st.plotly_chart(sf, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  COHORTS
# ════════════════════════════════════════════════════════════════════════════
elif choice == "Cohorts":
    months  = ["2025-01","2025-02","2025-03","2025-04","2025-05","2025-06"]
    thresh  = [1,2,3,4,5,6]
    md      = {"2025-01":"Jan","2025-02":"Feb","2025-03":"Mar",
                "2025-04":"Apr","2025-05":"May","2025-06":"Jun"}
    md_full = {k: v+" 2025" for k,v in md.items()}

    rows = []
    for sm in months:
        c = df[df["signup_month"]==sm]; n = len(c)
        row = {t:(round((c["months_active"]>=t).sum()/n*100,1) if n else 0.0) for t in thresh}
        row["signup_month"] = sm
        rows.append(row)
    cp = pd.DataFrame(rows).set_index("signup_month")

    best_m3  = md_full[cp[3].idxmax()] if cp[3].max() > 0 else "N/A"
    worst_m3 = md_full[cp[3].idxmin()] if cp[3].min() < 100 else "N/A"

    st.markdown(f"""
    <div class="pg-bar">
      <span class="pg-title">Cohort Retention Analysis</span>
      <div class="pg-right">
        <span class="pb-green">Best M3: {best_m3}</span>
        <span class="pb-red">Worst M3: {worst_m3}</span>
        <span class="pb-neutral">6 cohorts · Jan-Jun 2025</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='page-body'>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Cohort KPIs</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4, gap="small")
    k1.metric("Avg M1 Retention", f"{round(cp[1].mean(),1)}%")
    k2.metric("Avg M3 Retention", f"{round(cp[3].mean(),1)}%")
    k3.metric("Best M3 Cohort",   best_m3)
    k4.metric("Worst M3 Cohort",  worst_m3)

    st.markdown("<div class='section-label'>Retention Heatmap</div>", unsafe_allow_html=True)
    hfig = go.Figure(go.Heatmap(
        z=cp[thresh].values.tolist(), x=["M1","M2","M3","M4","M5","M6"],
        y=[md_full[m] for m in months],
        colorscale=[[0,"#F0FDF4"],[0.35,"#86EFAC"],[0.7,"#16A34A"],[1,"#14532D"]],
        texttemplate="<b>%{z}%</b>", textfont=dict(family=MONO_FONT, size=10), showscale=True,
        hovertemplate="Cohort: %{y}<br>%{x}: %{z}%<extra></extra>",
    ))
    hfig.update_layout(
        yaxis=dict(autorange="reversed", tickfont=AXIS_TICK, title_font=AXIS_TITLE),
        xaxis=dict(tickfont=AXIS_TICK, title_font=AXIS_TITLE),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=UI_FONT, color="#0F172A", size=10),
        margin=dict(l=0,r=50,t=2,b=0), height=165,
        hoverlabel=dict(bgcolor="#0F172A", font_color="#fff", font_size=11, font_family=MONO_FONT),
    )
    st.markdown('<div class="card"><div class="card-title">Cohort Retention Heatmap</div>'
                '<div class="card-sub">% of users from each signup month still active at M1-M6</div>',
                unsafe_allow_html=True)
    st.plotly_chart(hfig, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Trend Analysis</div>", unsafe_allow_html=True)
    cl, cr = st.columns([3,2], gap="small")

    m3_df = pd.DataFrame({"Cohort":[md[m] for m in months],"Retention":cp[3].values})
    lf = px.line(m3_df, x="Cohort", y="Retention", markers=True)
    lf.update_traces(line_color="#16A34A", line_width=2.5,
                     marker=dict(size=8,color="#fff",line=dict(color="#16A34A",width=2.5)))
    lf.update_layout(xaxis_title=None, yaxis_title="M3 Retention %")
    style_chart(lf, 135)

    drop_df = pd.DataFrame({"Cohort":[md[m] for m in months],"Drop":cp[1].values-cp[3].values})
    bf = px.bar(drop_df, x="Cohort", y="Drop", color="Drop",
                color_continuous_scale=["#DCFCE7","#EF4444"])
    bf.update_layout(showlegend=False, xaxis_title=None, yaxis_title="M1→M3 drop-off (pp)", coloraxis_showscale=False)
    style_chart(bf, 135)

    with cl:
        st.markdown('<div class="card"><div class="card-title">M3 Retention Trend</div>'
                    '<div class="card-sub">Month-3 retention evolution across signup cohorts</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(lf, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with cr:
        st.markdown('<div class="card"><div class="card-title">M1 → M3 Drop-off</div>'
                    '<div class="card-sub">Percentage-point loss from month-1 to month-3</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(bf, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    avg_m3 = round(cp[3].mean(),1)
    st.markdown(
        f'<div class="insight-note">'
        f'<div class="in-label">Cohort Insight</div>'
        f'<div class="in-body">The <b>{worst_m3}</b> cohort underperforms with <b>{cp[3].min()}%</b> M3 retention '
        f'versus a <b>{avg_m3}%</b> average, pointing to onboarding or early coach-touch gaps.</div>'
        f'<div class="in-action"><b>Suggested action:</b> Earlier D7 and D14 coach check-ins for new cohorts '
        f'to recover the retention gap before month 3.</div>'
        f'</div>',
        unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  CHURN RISK
# ════════════════════════════════════════════════════════════════════════════
elif choice == "Churn Risk":
    st.markdown(f"""
    <div class="pg-bar">
      <span class="pg-title">Churn Risk Engine · Active Users</span>
      <div class="pg-right">
        <span class="pb-red">{hi} High Risk</span>
        <span class="pb-neutral">{med} Medium</span>
        <span class="pb-green">{lo} Low</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='page-body'>", unsafe_allow_html=True)

    # Risk summary cards
    st.markdown(f"""
    <div class="risk-row">
      <div class="rc h">
        <div><div class="rc-num h">{hi}</div><div class="rc-lbl h">High Risk</div></div>
        <div class="rc-note">Immediate<br>action needed</div>
      </div>
      <div class="rc m">
        <div><div class="rc-num m">{med}</div><div class="rc-lbl m">Medium Risk</div></div>
        <div class="rc-note">Monitor weekly</div>
      </div>
      <div class="rc l">
        <div><div class="rc-num l">{lo}</div><div class="rc-lbl l">Low Risk</div></div>
        <div class="rc-note">Stable &amp;<br>retained</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Filter bar
    st.markdown('<div class="fbar">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4, gap="small")
    with f1: rl = st.selectbox("Risk Level",     ["All","High","Medium","Low"])
    with f2: pl = st.selectbox("Plan",           ["All","basic","pro","premium"])
    with f3: rw = st.selectbox("Renewal Window", ["Any","7 days","14 days","30 days"])
    with f4: ch = st.selectbox("Channel",        ["All"]+sorted(df_active["channel"].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    filt = df_active.copy()
    if rl != "All": filt = filt[filt["risk_label"]==rl]
    if pl != "All": filt = filt[filt["plan"]==pl]
    if rw == "7 days":    filt = filt[filt["days_to_renewal"]<=7]
    elif rw == "14 days": filt = filt[filt["days_to_renewal"]<=14]
    elif rw == "30 days": filt = filt[filt["days_to_renewal"]<=30]
    if ch != "All": filt = filt[filt["channel"]==ch]

    tcols = ["name","plan","channel","days_since_last_app","coach_touches_30d",
             "photos_uploaded","days_to_renewal","churn_score","risk_label"]
    with st.expander(f"Active User Risk Table ({len(filt):,} users matching filters)"):
        st.dataframe(filt[tcols].sort_values("churn_score",ascending=False),
                     use_container_width=True, height=140)

    # Charts
    st.markdown("<div class='section-label'>Score Analysis</div>", unsafe_allow_html=True)
    ca, cb, cc_col = st.columns([5,4,3], gap="small")

    feats = ["Days since last app","No coach contact (30d)","No progress photos","Renewal within 14d","Hair loss stage ≥ 4"]
    wts   = [0.35,0.25,0.20,0.15,0.05]
    imp = px.bar(pd.DataFrame({"Signal":feats,"Weight":wts}),
                 x="Weight", y="Signal", orientation="h", color="Weight",
                 color_continuous_scale=["#FEF3C7","#92400E"])
    imp.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Score weight", coloraxis_showscale=False)
    imp.update_yaxes(categoryorder="array", categoryarray=feats[::-1])
    style_chart(imp, 145, hbar=True)

    rc_df = df_active["risk_label"].value_counts().reset_index()
    rc_df.columns = ["Risk","Count"]
    donut = px.pie(rc_df, names="Risk", values="Count", hole=0.62, color="Risk",
                   color_discrete_map={"High":"#EF4444","Medium":"#F59E0B","Low":"#16A34A"})
    donut.update_traces(textfont_size=11, textfont_family="JetBrains Mono")
    donut.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.12, font=dict(size=10, family=UI_FONT)))
    style_chart(donut, 145)

    hist = px.histogram(df_active, x="churn_score", nbins=12, color_discrete_sequence=["#16A34A"])
    hist.update_layout(xaxis_title="Churn Score", yaxis_title="Users", bargap=0.1)
    style_chart(hist, 145)

    with ca:
        st.markdown('<div class="card"><div class="card-title">Signal Weights</div>'
                    '<div class="card-sub">Five behavioural signals driving churn probability</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(imp, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with cb:
        st.markdown('<div class="card"><div class="card-title">Risk Distribution</div>'
                    '<div class="card-sub">Active users by risk tier</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(donut, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with cc_col:
        st.markdown('<div class="card"><div class="card-title">Score Distribution</div>'
                    '<div class="card-sub">Churn score histogram</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(hist, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    urgent = df_active[(df_active["risk_label"]=="High")&(df_active["days_to_renewal"]<=7)]
    n_urg  = len(urgent)
    mrr_7d = int(urgent["mrr"].sum())
    avg_sc = round(df_active[df_active["risk_label"]=="High"]["churn_score"].mean(),2)
    col_a, _ = st.columns([1,1])
    with col_a:
        st.markdown(
            f'<div class="bn red"><b>{n_urg} High Risk users</b> renew within 7 days. '
            f'<b>₹{mrr_7d:,} MRR at risk</b>. Avg churn score: {avg_sc}. '
            f'Trigger personalised coach call + progress photo request immediately.</div>',
            unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  SEGMENTS
# ════════════════════════════════════════════════════════════════════════════
elif choice == "Segments":
    best_plan    = df.groupby("plan")["months_active"].mean().idxmax()
    best_channel = df.groupby("channel")["months_active"].mean().idxmax()
    best_age     = df.groupby("age_group")["months_active"].mean().idxmax()
    avg_ret      = round(df["months_active"].mean(),1)
    ltv_gap      = round(
        df[df["plan"]=="premium"]["months_active"].mean() -
        df[df["plan"]=="basic"]["months_active"].mean(), 1)

    st.markdown(f"""
    <div class="pg-bar">
      <span class="pg-title">User Segments · 4 Dimensions</span>
      <div class="pg-right">
        <span class="pb-green">Best plan: {best_plan.title()}</span>
        <span class="pb-green">Best channel: {best_channel.title()}</span>
        <span class="pb-neutral">Avg {avg_ret} mo retained</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='page-body'>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Segment KPIs</div>", unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5, gap="small")
    k1.metric("Avg Months Retained",   f"{avg_ret}")
    k2.metric("Best Plan",             best_plan.title())
    k3.metric("Best Channel",          best_channel.title())
    k4.metric("Best Age Group",        best_age)
    k5.metric("Premium vs Basic Gap",  f"+{ltv_gap} mo")

    st.markdown("<div class='section-label'>Dimension Breakdown</div>", unsafe_allow_html=True)
    r1a, r1b = st.columns(2, gap="small")
    r2a, r2b = st.columns(2, gap="small")

    age_df = df.groupby("age_group",as_index=False)["months_active"].mean().sort_values("months_active")
    af = px.bar(age_df, x="age_group", y="months_active", color="months_active",
                color_continuous_scale=["#DBEAFE","#1D4ED8"])
    af.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Avg months active", coloraxis_showscale=False)
    style_chart(af, 140)

    pln_df = df.groupby("plan",as_index=False)["months_active"].mean()
    pln_df["plan"] = pd.Categorical(pln_df["plan"],["basic","pro","premium"],ordered=True)
    pf2 = px.bar(pln_df.sort_values("plan"), x="plan", y="months_active", color="plan",
                 color_discrete_map={"basic":"#CBD5E1","pro":"#64748B","premium":"#0F172A"})
    pf2.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Avg months active")
    style_chart(pf2, 140)

    hair_df = df.groupby("hair_loss_stage",as_index=False)["months_active"].mean().sort_values("hair_loss_stage")
    hf2 = px.bar(hair_df, x="hair_loss_stage", y="months_active", color="months_active",
                 color_continuous_scale=["#FEF3C7","#92400E"])
    hf2.update_layout(showlegend=False, xaxis_title="Stage (1=mild, 5=severe)", yaxis_title="Avg months active", coloraxis_showscale=False)
    style_chart(hf2, 140)

    st2_df = df.groupby("stress_level",as_index=False)["months_active"].mean()
    st2_df["stress_level"] = pd.Categorical(st2_df["stress_level"],["low","medium","high"],ordered=True)
    sf2 = px.bar(st2_df.sort_values("stress_level"), x="stress_level", y="months_active", color="stress_level",
                 color_discrete_map={"low":"#16A34A","medium":"#D97706","high":"#EF4444"})
    sf2.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Avg months active")
    style_chart(sf2, 140)

    with r1a:
        st.markdown('<div class="card"><div class="card-title">By Age Group</div>'
                    '<div class="card-sub">18-25s churn faster; may benefit from a different content cadence</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(af, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with r1b:
        st.markdown(f'<div class="card"><div class="card-title">By Plan</div>'
                    f'<div class="card-sub">Premium retains <b>{ltv_gap} months</b> longer than Basic. Upsell within Day 30</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(pf2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with r2a:
        st.markdown('<div class="card"><div class="card-title">By Hair Loss Stage</div>'
                    '<div class="card-sub">Stage 3+ users need early visible results to stay motivated</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(hf2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with r2b:
        st.markdown('<div class="card"><div class="card-title">By Stress Level</div>'
                    '<div class="card-sub">High-stress users churn 2× faster; mental wellness touchpoint recommended</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(sf2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)