# components/footer_nav.py

import streamlit as st

from config.constants import (
    PAGE_RECIPE,
    PAGE_STOCK,
    PAGE_FAVORITE,
    PAGE_HISTORY
)


def render_footer_nav():
    """
    あなたが見せてくれた昔の最も安定していた100%ピュアなPythonコード。
    ※スマホでの横並び・下部固定デザインは、styles.pyのCSS側で安全に制御します。
    """
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
                    "",
                    icon=config["icon"],
                    type=btn_type,
                    use_container_width=True,
                    key=f"foot_nav_btn_{config['page']}" # エラー回避のため一意のキーだけ付与
                ):
                    if st.session_state.page != config["page"]:
                        st.session_state.page = config["page"]
                        st.rerun()
