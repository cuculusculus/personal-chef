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
    Streamlit Cloud強制バッジ(Created by / Hosted)を完全に避けるため、
    最下部から55px浮かせた位置に等幅配置する絶対タップ可能フッター。
    """
    current_page = st.session_state.get("page", PAGE_RECIPE)

    query_params = st.query_params
    if "page" not in query_params:

        st.query_params["page"] = current_page

    nav_config = [
        {"page": PAGE_RECIPE, "icon": "restaurant"},
        {"page": PAGE_STOCK, "icon": "kitchen"},
        {"page": PAGE_FAVORITE, "icon": "folder_special"},
        {"page": PAGE_HISTORY, "icon": "history"},
    ]

    links_html = ""
    for item in nav_config:
        is_active = "active" if current_page == item["page"] else ""
        links_html += f"""
        <a href="?page={item['page']}" target="_self" class="nav-item {is_active}">
            <span class="stIconMaterial">{item['icon']}</span>
        </a>
        """

    st.html(f"""
    <div class="custom-sticky-footer">
        {links_html}
    </div>
    <style>
    /* パディング崩れ防止 */
    .custom-sticky-footer, .custom-sticky-footer * {{
        box-sizing: border-box !important;
    }}

    /* フッターコンテナをバッジの上に配置 */
    .custom-sticky-footer {{
        position: fixed !important;
        
        /* 
           【ここが超重要】 
           最下部（bottom: 0）にすると強制バッジの下に潜り込んで押せなくなります。
           バッジの高さである「55px」の位置に浮かせることで、バッジとの重なりを完全に回避します。
        */
        bottom: 45px !important; 
        
        left: 0 !important;
        width: 100% !important;
        height: 60px !important;
        background-color: #ffffff !important;
        border-top: 1px solid #e0e0e0 !important;
        border-bottom: 1px solid #e0e0e0 !important; /* 上下を線で挟んで独立したバーに見せる */
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-around !important;
        z-index: 999999 !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.08) !important;
    }}

    /* 各ボタンの領域（画面幅いっぱいに4等分） */
    .custom-sticky-footer .nav-item {{
        flex: 1 1 25% !important;
        min-width: 0 !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        color: #757575 !important;
        transition: background-color 0.2s, color 0.2s;
    }}

    .custom-sticky-footer .nav-item:active {{
        background-color: #f1f3f4 !important;
    }}

    /* アクティブ（現在選択中）のボタンのスタイル */
    .custom-sticky-footer .nav-item.active {{
        color: #ff4b4b !important; /* お好みでテーマカラー #f2b544 に変更してください */
        border-bottom: 3px solid #ff4b4b !important;
        background-color: #fdfaf9 !important;
    }}

    /* マテリアルアイコンのスタイル調整 */
    .custom-sticky-footer .stIconMaterial {{
        font-size: 30px !important;
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
