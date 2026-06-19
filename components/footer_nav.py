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
    スマホでの縦並びを回避し、マテリアルアイコンを確実に読み込んで表示する
    完全固定のフッターナビゲーション。
    """
    current_page = st.session_state.get("page", PAGE_RECIPE)

    query_params = st.query_params
    if "page" in query_params and query_params["page"] != current_page:
        st.session_state.page = query_params["page"]
        st.rerun()

    # マテリアルアイコンの名前を指定
    nav_items = [
        {"page": PAGE_RECIPE, "icon": "restaurant"},
        {"page": PAGE_STOCK, "icon": "kitchen"},
        {"page": PAGE_FAVORITE, "icon": "bookmark_star"},
        {"page": PAGE_HISTORY, "icon": "history"},
    ]

    links_html = ""
    for item in nav_items:
        is_active = "active" if current_page == item["page"] else ""
        links_html += f"""
        <a href="?page={item['page']}" target="_self" class="nav-item {is_active}">
            <span class="material-symbols-outlined">{item['icon']}</span>
        </a>
        """

    # 1. 確実にアイコンを効かせるため、このコンポーネント内で直接フォントを読み込む
    st.markdown("""
    <link rel="stylesheet" href="https://googleapis.com" />
    """, unsafe_allow_html=True)

    # 2. HTMLとCSSを出力
    st.html(f"""
    <div class="custom-sticky-footer">
        {links_html}
    </div>
    <style>
    /* 全ての要素でパディングが横幅を突き破らないように設定 */
    .custom-sticky-footer, .custom-sticky-footer * {{
        box-sizing: border-box !important;
    }}

    /* フッターコンテナの絶対最下部固定 */
    .custom-sticky-footer {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 60px !important;
        background-color: #ffffff !important;
        border-top: 1px solid #e0e0e0 !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-around !important;
        z-index: 999999 !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
        padding-bottom: env(safe-area-inset-bottom, 0px) !important;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.08) !important;
    }}

    /* 各ボタンの領域（4等分） */
    .custom-sticky-footer .nav-item {{
        flex: 1 1 25% !important;
        min-width: 0 !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        color: #757575 !important; /* 通常時（非選択）のグレー */
        transition: background-color 0.2s, color 0.2s;
    }}

    /* タップ時の視覚効果 */
    .custom-sticky-footer .nav-item:active {{
        background-color: #f1f3f4 !important;
    }}

    /* アクティブ（現在選択中）のボタンのスタイル */
    .custom-sticky-footer .nav-item.active {{
        color: #ff4b4b !important; /* 選択中のStreamlitレッド */
        border-bottom: 3px solid #ff4b4b !important; /* 下線をつけて強調 */
    }}

    /* マテリアルアイコンがテキスト化してはみ出るのを防ぐ設定 */
    .custom-sticky-footer .material-symbols-outlined {{
        font-size: 26px !important;
        font-family: 'Material Symbols Outlined' !important;
        font-weight: normal !important;
        font-style: normal !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
    }}
    </style>
    """)
