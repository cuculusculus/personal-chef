#styles.py
import streamlit as st

APP_CSS = """
<style>

/* Streamlit標準UI非表示 */
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

/* 本文 */
.block-container {
    padding-top: 0.2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 90px !important;
    max-width: 100% !important;
}

/* 下ナビ分の余白 */
.stApp {
    padding-bottom: 80px;
}

/* 折返し */
* {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}

</style>
"""

def apply_styles():

    st.markdown(
        APP_CSS,
        unsafe_allow_html=True
    )
