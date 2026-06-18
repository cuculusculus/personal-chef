# components/footer_nav.py
import streamlit as st
from config.constants import *

def render_footer_nav():

    nav = [
        (PAGE_RECIPE, "🍳"),
        (PAGE_STOCK, "🧊"),
        (PAGE_FAVORITE, "⭐"),
        (PAGE_HISTORY, "📁"),
    ]

    st.markdown("""
    <style>
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 64px;
        background: white;
        border-top: 1px solid #ddd;
        display: flex;
        z-index: 999999;
    }

    .bottom-nav button {
        flex: 1;
        border: none;
        background: transparent;
        font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    cols = st.columns(4)

    for i, (page, icon) in enumerate(nav):
        with cols[i]:
            if st.button(icon, key=f"nav_{i}"):
                st.session_state.page = page
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
