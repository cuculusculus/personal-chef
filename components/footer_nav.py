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

    /* 下固定バー */
    div[data-testid="stHorizontalBlock"] {
        position: fixed !important;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: white;
        border-top: 1px solid #ddd;
        z-index: 999999;
    }

    /* ボタン均等化 */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        border: none !important;
        background: transparent !important;
        font-size: 22px !important;
    }

    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏠"):
            st.session_state.page = PAGE_RECIPE
            st.rerun()

    with col2:
        if st.button("🥬"):
            st.session_state.page = PAGE_STOCK
            st.rerun()

    with col3:
        if st.button("⭐"):
            st.session_state.page = PAGE_FAVORITE
            st.rerun()

    with col4:
        if st.button("🕒"):
            st.session_state.page = PAGE_HISTORY
            st.rerun()
