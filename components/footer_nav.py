# components/footer_nav.py
import streamlit as st

from config.constants import (
    PAGE_RECIPE,
    PAGE_STOCK,
    PAGE_FAVORITE,
    PAGE_HISTORY
)

def render_footer_nav():

    st.markdown("""
    <style>

    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;

        height: 60px;
        background: white;
        border-top: 1px solid #ddd;
        z-index: 999999;

        display: flex;
    }

    .bottom-nav button {
        flex: 1 !important;
        border: none !important;
        background: transparent !important;
        font-size: 22px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    if st.button("🏠"):
        st.session_state.page = PAGE_RECIPE
        st.rerun()

    if st.button("🥬"):
        st.session_state.page = PAGE_STOCK
        st.rerun()

    if st.button("⭐"):
        st.session_state.page = PAGE_FAVORITE
        st.rerun()

    if st.button("🕒"):
        st.session_state.page = PAGE_HISTORY
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
