# components/footer_nav.py
from streamlit_option_menu import option_menu
import streamlit as st

def render_footer_nav():

    st.markdown("""
<style>

/* option_menu本体 */

ul.nav.nav-pills.mb-auto.nav-justified {

    position: fixed !important;

    bottom: 0 !important;
    left: 0 !important;

    width: 100vw !important;

    background: red !important;
    border-top: 1px solid #ddd !important;

    z-index: 999999 !important;

    margin: 0 !important;
    padding: 0 !important;
}

/* 4分割 */

ul.nav.nav-pills.mb-auto.nav-justified > li {
    flex: 1 !important;
    text-align: center !important;
}

</style>
""", unsafe_allow_html=True)

    option_menu(
        None,
        ["Home", "Stock", "Fav", "History"],
        icons=[
            "house-fill",
            "basket",
            "bookmark-star",
            "clock-history"
        ],
        orientation="horizontal"
    )
