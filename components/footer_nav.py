# components/footer_nav.py

import streamlit as st

from config.constants import (
    PAGE_RECIPE,
    PAGE_STOCK,
    PAGE_FAVORITE,
    PAGE_HISTORY
)

def render_footer_nav():

    st.divider()

    cols = st.columns([1,1,1,1])

    pages = [
        PAGE_RECIPE,
        PAGE_STOCK,
        PAGE_FAVORITE,
        PAGE_HISTORY
    ]

    labels = [
        "🍳",
        "🥬",
        "⭐",
        "🕒"
    ]

    for col, page, label in zip(cols, pages, labels):
        with col:
            if st.button(
                label,
                use_container_width=True,
                key=f"nav_{page}"
            ):
                st.session_state.page = page
                st.rerun()
