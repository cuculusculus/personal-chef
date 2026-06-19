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
    Streamlitの自動縦並び化を完全に回避する、純粋なHTML/CSS製フッターナビ。
    """
    current_page = st.session_state.get("page", PAGE_RECIPE)

    query_params = st.query_params
    if "page" in query_params and query_params["page"] != current_page:
        st.session_state.page = query_params["page"]
        st.rerun()

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
        height: 60px !important; /* 少し高さをスリムに */
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

    /* 各ボタンの領域（4等分・縮小を許可） */
    .custom-sticky-footer .nav-item {{
        flex: 1 1 25% !important; /* 25%をベースに伸縮可能にする */
        min-width: 0 !important;    /* はみ出し防止に必須の設定 */
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        color: #5f6368 !important;
    }}

    .custom-sticky-footer .nav-item:active {{
        background-color: #f1f3f4 !important;
    }}

    .custom-sticky-footer .nav-item.active {{
        color: #ff4b4b !important;
    }}

    /* アイコンのサイズを30pxから24pxに縮小（一般的なモバイルアプリのサイズ） */
    .custom-sticky-footer .nav-item span {{
        font-size: 24px !important;
        display: block !important;
        width: 24px !important;
        height: 24px !important;
        text-align: center !important;
    }}
    </style>
    """)
