# components/footer_nav.py

import streamlit as st

from config.constants import (
    PAGE_RECIPE,
    PAGE_STOCK,
    PAGE_FAVORITE,
    PAGE_HISTORY
)


def render_footer_nav():
    # 画面最下部に固定するためのCSS（スマホ対応）
    st.markdown(
        """
        <style>
        /* フッターコンテナを最下部に固定 */
        div[data-testid="stElementContainer"]:has(div[id="footer_nav"]) {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: var(--background-color, #ffffff);
            padding: 10px 20px 20px 20px;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
            z-index: 999999;
        }
        
        /* メインコンテンツがフッターに被らないように下部に余白を作る */
        .main .block-container {
            padding-bottom: 80px !important;
        }

        /* スマホ向けにボタン内の余白を微調整 */
        div[id="footer_nav"] button {
            padding: 6px !important;
            height: 45px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # keyに "footer_nav" を指定することで上記CSSと紐付けます
    with st.container(key="footer_nav"):
        cols = st.columns([1, 1, 1, 1], gap="small")
        
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
                    key=f"btn_{config['page']}" # キーの一意性を担保
                ):
                    if st.session_state.page != config["page"]:
                        st.session_state.page = config["page"]
                        st.rerun()
