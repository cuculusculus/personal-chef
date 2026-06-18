#styles.py
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
div[data-testid="stDecoration"] {
    display: none !important;
}

/* ---------- アプリ全体レイアウト ---------- */

.block-container {
    padding-top: 0.2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 110px !important;
    max-width: 100% !important;
}

.stApp {
    padding-bottom: 100px;
}

/* ---------- フッター固定 ---------- */

div.st-key-footer_nav {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 75px !important;
    background-color: #ffffff !important;
    border-top: 1px solid #e0e0e0 !important;
    z-index: 999999 !important;
    padding: 10px !important;
    box-shadow: 0 -4px 12px rgba(0,0,0,0.05) !important;
}

/* ---------- フッターボタン ---------- */

div.st-key-footer_nav [data-testid="column"] {
    width: 25% !important;
    flex: 1 1 25% !important;
    min-width: 25% !important;
}

div.st-key-footer_nav button {
    height: 55px !important;
    padding: 0 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
/* ---------- フッターアイコン ---------- */
/* ボタン内のアイコンサイズ */
div.st-key-footer_nav button span {
    font-size: 36px !important;
}
/* ボタン内のラベルサイズ */
div.st-key-footer_nav button p {
    font-size: 12px !important;
    font-weight: 600 !important;
    margin: 0 !important;
}
/* ---------- 共通設定 ---------- */
/* 全体文字折返し */
* {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}

</style>
"""


def apply_styles():

    st.markdown("""
<link rel="stylesheet"
href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
""", unsafe_allow_html=True)

    st.markdown(APP_CSS, unsafe_allow_html=True)