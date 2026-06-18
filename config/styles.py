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
    right: 0 !important;
    background: white !important;
    border-top: 1px solid #ddd !important;
    z-index: 9999 !important;
}

/* columnsコンテナ */
div.st-key-footer_nav [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-wrap: nowrap !important;
}

/* 各列 */
div.st-key-footer_nav [data-testid="column"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
}

/* ボタン */
div.st-key-footer_nav button {
    width: 100% !important;
    min-width: 0 !important;
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
