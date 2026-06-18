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

    st.markdown("""
    <style>
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 64px;
        background: #ffffff;
        border-top: 1px solid #e6e6e6;
        display: flex;
        z-index: 999999;
    }

    .nav-btn {
        flex: 1;
        border: none;
        background: transparent;
        font-size: 24px;
        padding: 6px 0;
        transition: all 0.2s ease;
    }

    .nav-btn.active {
        color: #ff4b4b;
        transform: translateY(-2px);
    }

    .nav-btn:active {
        transform: scale(0.92);
    }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(4)

    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    for i, (page, icon) in enumerate(nav):
        with cols[i]:
            is_active = (current == page)

            btn_style = "primary" if is_active else "secondary"

            if st.button(
                icon,
                key=f"nav_{page}",
                type=btn_style,
                use_container_width=True
            ):
                st.session_state.page = page
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
