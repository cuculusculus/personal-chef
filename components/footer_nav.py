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

    /* 完全固定フッター */
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

    /* ボタン強制横並び */
    .bottom-nav button {
        flex: 1 !important;
        border: none !important;
        background: transparent !important;
        font-size: 24px !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # ここ重要（HTMLコンテナで囲う）
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    if st.button("🏠", key="nav_home"):
        st.session_state.page = PAGE_RECIPE
        st.rerun()

    if st.button("🥬", key="nav_stock"):
        st.session_state.page = PAGE_STOCK
        st.rerun()

    if st.button("⭐", key="nav_fav"):
        st.session_state.page = PAGE_FAVORITE
        st.rerun()

    if st.button("🕒", key="nav_history"):
        st.session_state.page = PAGE_HISTORY
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
