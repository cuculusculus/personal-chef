# components/footer_nav.py
from streamlit_option_menu import option_menu
import streamlit as st

from config.constants import *

def render_footer_nav():

    pages = [
        PAGE_RECIPE,
        PAGE_STOCK,
        PAGE_FAVORITE,
        PAGE_HISTORY
    ]

    current_idx = pages.index(st.session_state.page)

    selected = option_menu(
        menu_title=None,
        options=[" ", "  ", "   ", "    "],
        icons=[
            "house-fill",
            "basket",
            "bookmark-star",
            "clock-history"
        ],
        default_index=current_idx,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "margin": "0!important",
                "background-color": "#ffffff",
                "border-top": "1px solid #ddd",
                "position": "fixed",
                "bottom": "0",
                "left": "0",
                "width": "100%",
                "z-index": "999999"
            },
            "nav-link": {
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#f5f5f5"
            },
            "icon": {
                "font-size": "22px"
            }
        }
    )

    idx = [" ", "  ", "   ", "    "].index(selected)

    target = pages[idx]

    if target != st.session_state.page:
        st.session_state.page = target
        st.rerun()
