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
    スマホ画面でも絶対に横並びを崩さない、最下部固定の4等分フッターナビゲーション。
    ※実際のレイアウトと固定スタイルは styles.py の CSS で制御されます。
    """
    # 1. コンテナの key を styles.py の CSS と完全一致させる
    with st.container(key="footer_nav"):
        
        # 2. スマホでも等幅を維持するため明示的に [1, 1, 1, 1] と gap="small" を指定
        cols = st.columns([1, 1, 1, 1], gap="small")
        
        nav_config = [
            {"page": PAGE_RECIPE, "icon": ":material/restaurant:"},
            {"page": PAGE_STOCK, "icon": ":material/kitchen:"},
            {"page": PAGE_FAVORITE, "icon": ":material/bookmark_star:"},
            {"page": PAGE_HISTORY, "icon": ":material/history:"}
        ]

        # 3. 各カラムにボタンを配置
        for col, config in zip(cols, nav_config):
            with col:
                btn_type = (
                    "primary"
                    if st.session_state.page == config["page"]
                    else "secondary"
                )

                if st.button(
                    "",  # アイコン特化のためテキストは空
                    icon=config["icon"],
                    type=btn_type,
                    use_container_width=True,
                    key=f"btn_{config['page']}"  # 画面遷移時の重複エラーを防ぐためキーを一意にする
                ):
                    if st.session_state.page != config["page"]:
                        st.session_state.page = config["page"]
                        st.rerun()
