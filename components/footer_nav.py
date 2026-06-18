# components/footer_nav.py

from streamlit_option_menu import option_menu
import streamlit as st

from config.constants import *

def render_footer_nav():

    st.error("footer loaded")

    pages = [
        PAGE_RECIPE,
        PAGE_STOCK,
        PAGE_FAVORITE,
        PAGE_HISTORY
    ]

    current_idx = pages.index(st.session_state.page)

    selected = option_menu(
    menu_title=None,
    options=["Home", "Stock", "Fav", "History"],
    icons=[
        "house-fill",
        "basket",
        "bookmark-star",
        "clock-history"
    ],
    default_index=current_idx,
    orientation="horizontal"
)

st.markdown("""
<style>
.nav-pills{
    position:fixed !important;
    bottom:0 !important;
    left:0 !important;
    width:100% !important;
    background:white !important;
    z-index:999999 !important;
}
</style>
""", unsafe_allow_html=True)
    st.write("selected =", selected)
