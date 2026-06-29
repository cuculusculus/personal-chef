# config/styles.py
import streamlit as st

APP_CSS = """
<style>
/* ---------- Streamlit標準UI非表示 ---------- */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
header,
footer,
#MainMenu,
.stDeployButton,
[data-testid="stToolbar"],
div[data-testid="stDecoration"],
[data-testid="stAppHeader"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
}

/* ---------- アプリ全体レイアウト ---------- */
[data-testid="stMainBlockContainer"],
.main .block-container {
    padding-top: 0px !important;
    margin-top: 0px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 160px !important; /* フッターを避ける余白 */
    max-width: 100% !important;
}

.stApp {
    padding-top: 0px !important;
    padding-bottom: 100px;
}

/* ---------- フッターボタン内の調整 ---------- */
div[id="fixed_footer_root"] + div button {
    height: 52px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center;
}

div[id="fixed_footer_root"] + div button [data-testid="stIconMaterial"] {
    font-size: 28px !important;
}

/* ---------- 共通設定 ---------- */
.main .block-container p, 
.main .block-container div {
    word-wrap: break-word;
    overflow-wrap: break-word;
}
</style>
"""

def apply_styles():
    st.markdown("""
<link rel="stylesheet"
href="https://googleapis.com" />
""", unsafe_allow_html=True)
    st.html(APP_CSS)
