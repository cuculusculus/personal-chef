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
    スマホでの縦並びやフォント読み込みエラーを100%回避する、
    絵文字ベースの絶対横並びフッターナビ。
    """
    current_page = st.session_state.get("page", PAGE_RECIPE)

    query_params = st.query_params
    if "page" in query_params and query_params["page"] != current_page:
        st.session_state.page = query_params["page"]
        st.rerun()

    # 【修正】Material Iconsをやめ、スマホ共通の「絵文字」に変更
    # これによりフォントが読み込めずにテキストとしてはみ出る現象を完全に防ぎます
    nav_items = [
        {"page": PAGE_RECIPE, "icon": "🍳"},      # レシピ
        {"page": PAGE_STOCK, "icon": "🫙"},       # 在庫 (冷蔵庫)
        {"page": PAGE_FAVORITE, "icon": "⭐"},    # お気に入り
        {"page": PAGE_HISTORY, "icon": "⏱️"},     # 履歴
    ]

    links_html = ""
    for item in nav_items:
        is_active = "active" if current_page == item["page"] else ""
        links_html += f"""
        <a href="?page={item['page']}" target="_self" class="nav-item {is_active}">
            <div class="icon-wrapper">{item['icon']}</div>
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

    /* フッターコンテナの絶対最下部固定（横並び強制） */
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

    /* 各ボタンの領域（4等分・縮小を許可） */
    .custom-sticky-footer .nav-item {{
        flex: 1 1 25% !important;
        min-width: 0 !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        transition: background-color 0.2s;
        opacity: 0.4; /* 通常時は少し薄くする */
    }}

    /* タップ時の視覚効果 */
    .custom-sticky-footer .nav-item:active {{
        background-color: #f1f3f4 !important;
    }}

    /* アクティブ（現在選択中）のボタンのスタイル */
    .custom-sticky-footer .nav-item.active {{
        opacity: 1.0 !important; /* アクティブ時はくっきり表示 */
        background-color: #fcf8f8 !important; /* 選択中の背景をほんのり変更 */
        border-bottom: 3px solid #ff4b4b !important; /* 下線をつけて強調 */
    }}

    /* アイコン（絵文字）のサイズと配置 */
    .custom-sticky-footer .icon-wrapper {{
        font-size: 26px !important; /* スマホで最適なサイズ */
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    </style>
    """)
