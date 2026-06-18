# components/footer_nav.py
from streamlit_option_menu import option_menu
import streamlit as st

def render_footer_nav():

    st.markdown("""
    <style>

    /* option_menuのnavを強制固定 */

    nav.navbar {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        z-index: 999999 !important;
        background: white !important;
        border-top: 1px solid #ddd !important;
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
