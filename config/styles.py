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
    padding-bottom: 160px !important;
    max-width: 100% !important;
}

.stApp {
    padding-top: 0px !important;
    padding-bottom: 100px;
}

/* ---------- 【新設】ダイアログの位置を最上部に強制固定 ---------- */
/* 
   ダイアログの背景マスク全体の位置をリセットし、
   どんなスクロール位置から開いても必ず画面の最上部（top: 10px）にダイアログを配置します。
*/
div[data-testid="stModal"] {
    top: 10px !important;
    bottom: auto !important;
    align-items: flex-start !important;
    max-height: 85vh !important; /* スマホフッターを隠さない高さ */
}

/* ダイアログ内のスクロールを上端（0）から強制スタートさせるための設定 */
div[data-testid="stModal"] > div {
    margin-top: 0 !important;
    top: 0 !important;
}

/* ---------- タイトル・見出しの画面サイズ最適化 ---------- */
.main .block-container [data-testid="stHeadingWithIcon"],
.main .block-container [data-testid="stHeaderBlockContainer"],
.main .block-container [data-testid="element-container"]:has(h1, h2, h3) {
    max-width: 100% !important;
    width: 100% !important;
    min-width: 0 !important;
    overflow: hidden !important;
}

.main .block-container h1,
.main .block-container h1 span,
.main .block-container [data-testid="stHeadingWithIcon"] h1 p {
    font-size: max(1.2rem, 5.2vw) !important;
    line-height: 1.2 !important;
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
