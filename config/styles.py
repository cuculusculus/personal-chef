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

.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;

    height: 70px;
    display: flex;
    width: 100%;

    background: white;
    border-top: 1px solid #ddd;
}

/* ★ここが最重要 */
.bottom-nav button {
    flex: 1 !important;
    min-width: 0 !important;   /* ←これ必須 */

    border: none !important;
    background: transparent !important;

    display: flex;
    flex-direction: column;

    align-items: center;
    justify-content: center;
}

/* Streamlit内部span対策 */
.bottom-nav button * {
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
