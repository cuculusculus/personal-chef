# components/footer_nav.py
import streamlit as st
from config.constants import PAGE_RECIPE, PAGE_STOCK, PAGE_FAVORITE, PAGE_HISTORY

def render_footer_nav():
    """URL(クエリ)を使わず、セッションだけで動くクリーンなフッターナビ"""
    current_page = st.session_state.get("page", PAGE_RECIPE)

    nav_config = [
        {"page": PAGE_RECIPE, "icon": "restaurant"},
        {"page": PAGE_STOCK, "icon": "kitchen"},
        {"page": PAGE_FAVORITE, "icon": "bookmark_star"},
        {"page": PAGE_HISTORY, "icon": "history"},
    ]

    # HTMLで枠だけ作り、ボタンのクリックイベントはStreamlitの通常の仕組みで処理します
    with st.container():
        # スマホでも絶対に縦に崩れないように gap を small に指定
        cols = st.columns([1, 1, 1, 1], gap="small")
        
        for col, item in zip(cols, nav_config):
            with col:
                # 現在のページならオレンジ、それ以外はグレー
                btn_type = "primary" if current_page == item["page"] else "secondary"
                
                # アイコン付きの等幅ボタン
                if st.button("", icon=f":material/{item['icon']}:", type=btn_type, use_container_width=True, key=f"foot_btn_{item['page']}"):
                    if st.session_state.page != item["page"]:
                        st.session_state.page = item["page"]
                        st.rerun()
