# components/footer_nav.py
import streamlit as st

from config.constants import (
    PAGE_RECIPE,
    PAGE_STOCK,
    PAGE_FAVORITE,
    PAGE_HISTORY
)
st.write(st.__version__)
def render_footer_nav():

    with st.container(key="footer_nav"):

        cols = st.columns(4)

        nav_config = [
            {"page": PAGE_RECIPE, "icon": ":material/restaurant:"},
            {"page": PAGE_STOCK, "icon": ":material/kitchen:"},
            {"page": PAGE_FAVORITE, "icon": ":material/bookmark_star:"},
            {"page": PAGE_HISTORY, "icon": ":material/history:"}
        ]

        for col, config in zip(cols, nav_config):
            with col:

                btn_type = (
                    "primary"
                    if st.session_state.page == config["page"]
                    else "secondary"
                )

                if st.button(
                    "R",
                    key=f"nav_{config['page']}"
                ):
                    st.session_state.page = config["page"]
                    st.rerun()
