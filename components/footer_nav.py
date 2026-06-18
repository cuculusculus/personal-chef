# components/footer_nav.py
from streamlit_option_menu import option_menu
import streamlit as st

def render_footer_nav():

    selected = option_menu(
        menu_title=None,
        options=["Home", "Stock", "Fav", "History"],
        icons=[
            "house-fill",
            "basket",
            "bookmark-star",
            "clock-history"
        ],
        orientation="horizontal",
        styles={
            "container": {
                "position": "fixed",
                "bottom": "0",
                "left": "0",
                "width": "100%",
                "background-color": "red",
                "z-index": "999999"
            }
        }
    )
