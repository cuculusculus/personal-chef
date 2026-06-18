# components/footer_nav.py

from streamlit_option_menu import option_menu
import streamlit as st

from config.constants import *

def render_footer_nav():

    st.markdown("""
    <style>

    /* option_menu全体 */
    ul.nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;

        background: white !important;
        border-top: 1px solid #ddd !important;

        z-index: 999999 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 各ボタン均等割り */
    ul.nav li {
        flex: 1 !important;
        text-align: center !important;
    }

    </style>
    """, unsafe_allow_html=True)

    pages = [
        PAGE_RECIPE,
        PAGE_STOCK,
        PAGE_FAVORITE,
        PAGE_HISTORY
    ]

    current_idx = pages.index(st.session_state.page)
    st.markdown("""
    <style>
    
    ul {
        border: 3px solid red !important;
    }
    
    nav {
        border: 3px solid blue !important;
    }
    
    </style>
""", unsafe_allow_html=True)
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

    page_map = {
        "Home": PAGE_RECIPE,
        "Stock": PAGE_STOCK,
        "Fav": PAGE_FAVORITE,
        "History": PAGE_HISTORY
    }

    target = page_map[selected]

    if target != st.session_state.page:
        st.session_state.page = target
        st.rerun()
st.markdown("""
---
footer end
""")
