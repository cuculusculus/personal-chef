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
    # 現在のセッション状態のページ情報を取得
    current_page = st.session_state.get("page", PAGE_RECIPE)

    # クエリパラメータを確認し、URLから直接アクセスされた場合やクリック後の遷移に対応
    query_params = st.query_params
    if "page" in query_params and query_params["page"] != current_page:
        st.session_state.page = query_params["page"]
        st.rerun()

    # 各ナビゲーション項目の設定
    nav_items = [
        {"page": PAGE_RECIPE, "icon": "restaurant"},
        {"page": PAGE_STOCK, "icon": "kitchen"},
        {"page": PAGE_FAVORITE, "icon": "bookmark_star"},
        {"page": PAGE_HISTORY, "icon": "history"},
    ]

    # 各項目のHTMLリンクを生成
    links_html = ""
    for item in nav_items:
        is_active = "active" if current_page == item["page"] else ""
        links_html += f"""
        <a href="?page={item['page']}" target="_self" class="nav-item {is_active}">
            <span class="material-symbols-outlined">{item['icon']}</span>
        </a>
        """

    # HTMLとCSSを同時に出力（Streamlitの枠外で完全固定）
    st.html(f"""
    <div class="custom-sticky-footer">
        {links_html}
    </div>
    <style>
    /* フッターコンテナの絶対最下部固定 */
    .custom-sticky-footer {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 65px !important;
        background-color: #ffffff !important;
        border-top: 1px solid #e0e0e0 !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-around !important;
        z-index: 999999 !important;
        padding-bottom: env(safe-area-inset-bottom, 10px) !important; /* iPhoneの底面バー対策 */
        box-shadow: 0 -4px 12px rgba(0,0,0,0.08) !important;
    }}

    /* 各ボタンの領域（4等分） */
    .custom-sticky-footer .nav-item {{
        flex: 1 !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        color: #5f6368 !important; /* 通常時のアイコン色 */
        transition: background-color 0.2s;
    }}

    /* タップ時の視覚効果 */
    .custom-sticky-footer .nav-item:active {{
        background-color: #f1f3f4 !important;
    }}

    /* アクティブ（現在選択中）のボタンのスタイル */
    .custom-sticky-footer .nav-item.active {{
        color: #ff4b4b !important; /* アクティブ時のアイコン色 */
    }}

    /* アイコンのサイズ */
    .custom-sticky-footer .nav-item span {{
        font-size: 30px !important;
    }}
    </style>
    """)
