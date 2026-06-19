# components/footer_nav.py

import streamlit as st
from config.constants import PAGE_RECIPE, PAGE_STOCK, PAGE_FAVORITE, PAGE_HISTORY

def render_footer_nav():
    """CSSを直書きしてスマホでも絶対横並び＆最下部固定を実現するフッター"""
    
    st.markdown("""
        <style>
        /* 親要素ごと画面最下部に固定し、スマホでも崩れないレイアウトに強制設定 */
        [data-testid="stVerticalBlockBorderWrapper"]:has(div[id="fixed_footer_root"]) {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100% !important;
            background-color: #ffffff !important;
            border-top: 1px solid #e0e0e0 !important;
            z-index: 999999 !important;
            padding: 10px 16px 20px 16px !important;
            box-shadow: 0 -4px 12px rgba(0,0,0,0.06) !important;
        }
        
        /* 内部の st.columns がスマホで縦積みになるのを阻止 */
        div[id="fixed_footer_root"] div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            width: 100% !important;
            gap: 8px !important;
        }
        
        /* カラムを常に4等分（25%）に維持 */
        div[id="fixed_footer_root"] div[data-testid="column"] {
            width: 25% !important;
            min-width: 0 !important;
            flex: 1 1 25% !important;
        }
        
        /* ボタンのスタイル調整 */
        div[id="fixed_footer_root"] button {
            height: 48px !important;
            padding: 0px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # 固定位置を検知するためのアンカー用HTML
    st.html('<div id="fixed_footer_root"></div>')
    
    # 既存のPythonロジックを利用してボタンをレンダリング
    with st.container():
        cols = st.columns([1, 1, 1, 1], gap="small")
        nav_config = [
            {"page": PAGE_RECIPE, "icon": ":material/restaurant:"},
            {"page": PAGE_STOCK, "icon": ":material/kitchen:"},
            {"page": PAGE_FAVORITE, "icon": ":material/bookmark_star:"},
            {"page": PAGE_HISTORY, "icon": ":material/history:"}
        ]

        for col, config in zip(cols, nav_config):
            with col:
                btn_type = "primary" if st.session_state.page == config["page"] else "secondary"
                if st.button("", icon=config["icon"], type=btn_type, use_container_width=True, key=f"btn_nav_{config['page']}"):
                    if st.session_state.page != config["page"]:
                        st.session_state.page = config["page"]
                        st.rerun()
