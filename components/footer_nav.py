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

    current = st.session_state.page

    # CSSで完全固定フッター
    st.markdown("""
    <style>
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 64px;
        background: #fff;
        border-top: 1px solid #e6e6e6;
        display: flex;
        z-index: 999999;
    }

    .nav-item {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .nav-item button {
        width: 100%;
        height: 64px;
        background: transparent;
        border: none;
        font-size: 24px;
    }

    .active {
        color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

    # フッター開始
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    cols = st.columns(4)

    for i, (page, icon) in enumerate(nav):
        with cols[i]:
            is_active = (current == page)

            if st.button(
                icon,
                key=f"nav_{page}",
                use_container_width=True
            ):
                st.session_state.page = page
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
