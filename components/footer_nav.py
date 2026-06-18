# components/footer_nav.py

import streamlit as st

from config.constants import (
    PAGE_RECIPE,
    PAGE_STOCK,
    PAGE_FAVORITE,
    PAGE_HISTORY
)


def render_footer_nav():

    with st.container(key="footer_nav"):

    cols = st.columns(4)

    for i, col in enumerate(cols):
        with col:
            st.write(f"列{i}")
