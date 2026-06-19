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
    スマホでの縦並びを完全に回避し、Streamlit内蔵のフォントを利用して
    マテリアルアイコンを100%確実に表示する最下部固定フッターナビ。
    """
    current_page = st.session_state.get("page", PAGE_RECIPE)

    query_params = st.query_params
    if "page" in query_params and query_params["page"] != current_page:
        st.session_state.page = query_params["page"]
        st.rerun()

    # アイコン名を純粋な単語（小文字）で指定
    nav_config = [
        {"page": PAGE_RECIPE, "icon": "restaurant"},
        {"page": PAGE_STOCK, "icon": "kitchen"},
        {"page": PAGE_FAVORITE, "icon": "bookmark_star"},
        {"page": PAGE_HISTORY, "icon": "history"},
    ]

    links_html = ""
    for item in nav_config:
        is_active = "active" if current_page == item["page"] else ""
        # 【重要】クラス名に "stIconMaterial" を直接指定することで文字化けを100%防ぎます
        links_html += f"""
        <a href="?page={item['page']}" target="_self" class="nav-item {is_active}">
            <span class="stIconMaterial">{item['icon']}</span>
        </a>
        """

    # HTMLとCSSを画面に出力
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

    /* 各ボタンの領域（4等分・スマホでの縮小を許可） */
    .custom-sticky-footer .nav-item {{
        flex: 1 1 25% !important;
        min-width: 0 !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        color: #757575 !important; /* 通常時（非選択）の落ち着いたグレー */
        transition: background-color 0.2s, color 0.2s;
    }}

    /* タップ時の視覚効果 */
    .custom-sticky-footer .nav-item:active {{
        background-color: #f1f3f4 !important;
    }}

    /* アクティブ（現在選択中）のボタンのスタイル */
    .custom-sticky-footer .nav-item.active {{
        color: #f2b544 !important; /* 選択中のStreamlitブランドレッド */
        border-bottom: 3px solid #f2b544 !important; /* アクティブを示す下線 */
        background-color: #fdfaf9 !important;
    }}

    /* Streamlit内蔵マテリアルフォントの強制適用設定 */
    .custom-sticky-footer .stIconMaterial {{
        font-size: 26px !important;
        font-family: "Material Symbols Outlined", "Material Symbols Rounded", sans-serif !important;
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
