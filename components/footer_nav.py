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
    スマホでの絶対横並び・最下部固定デザインを維持したまま、
    昔のセッション書き換えロジック（URLを汚さない安全方式）を完全復活させた決定版。
    """
    current_page = st.session_state.get("page", PAGE_RECIPE)

    nav_config = [
        {"page": PAGE_RECIPE, "icon": "restaurant"},
        {"page": PAGE_STOCK, "icon": "kitchen"},
        {"page": PAGE_FAVORITE, "icon": "bookmark_star"},
        {"page": PAGE_HISTORY, "icon": "history"},
    ]

    # 1. 4つのカスタムボタン（HTML）を出力
    # ※ hrefを使ったURLジャンプを廃止し、クリックされたらStreamlit側にイベントを飛ばす特殊ボタンにします
    links_html = ""
    for item in nav_config:
        is_active = "active" if current_page == item["page"] else ""
        links_html += f"""
        <button onclick="window.parent.postMessage({{type: 'nav_click', page: '{item['page']}'}}, '*')" class="nav-item {is_active}">
            <span class="stIconMaterial">{item['icon']}</span>
        </button>
        """

    # 2. ページ最下部から55px浮かせた位置に固定するCSS（デザインはそのまま）
    st.html(f"""
    <div class="custom-sticky-footer">
        {links_html}
    </div>
    <script>
    // HTMLボタンがクリックされたら、Streamlitの隠しボタン（下のPythonロジック）を代わりにクリックさせる仕掛け
    window.addEventListener('message', function(e) {{
        if (e.data.type === 'nav_click') {{
            var btn = window.parent.document.getElementById('hidden_btn_' + e.data.page);
            if (btn) btn.click();
        }}
    }});
    </script>
    <style>
    .custom-sticky-footer, .custom-sticky-footer * {{ box-sizing: border-box !important; }}
    .custom-sticky-footer {{
        position: fixed !important;
        bottom: 55px !important; /* バッジを避けて浮かせる */
        left: 0 !important;
        width: 100% !important;
        height: 60px !important;
        background-color: #ffffff !important;
        border-top: 1px solid #e0e0e0 !important;
        border-bottom: 1px solid #e0e0e0 !important;
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
    /* HTMLボタンの見た目をStreamlit標準のボタン風に調整 */
    .custom-sticky-footer .nav-item {{
        flex: 1 1 25% !important;
        min-width: 0 !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: none !important;
        background: none !important;
        cursor: pointer !important;
        color: #757575 !important;
        transition: background-color 0.2s, color 0.2s;
    }}
    .custom-sticky-footer .nav-item:active {{ background-color: #f1f3f4 !important; }}
    .custom-sticky-footer .nav-item.active {{
        color: #f2b544 !important; /* config.tomlのオレンジに同期 */
        border-bottom: 3px solid #f2b544 !important;
        background-color: #fdfaf9 !important;
    }}
    .custom-sticky-footer .stIconMaterial {{
        font-size: 26px !important;
        font-family: "Material Symbols Outlined", sans-serif !important;
    }}
    </style>
    """)

    # 3. 昔のコードと100%同じ、安全なセッション書き換えPythonロジック（画面には表示されません）
    # この隠し要素のおかげで、HTMLの見た目を保ちつつ、昔のセッション遷移がそのまま機能します。
    cols = st.columns(4)
    for col, item in zip(cols, nav_config):
        with col:
            # CSSで画面外（非表示）に隠した、クリック受け取り用の本物のStreamlitボタン
            if st.button(" ", key=f"hidden_btn_{item['page']}", use_container_width=True, help="hidden"):
                if st.session_state.page != item["page"]:
                    st.session_state.page = item["page"]
                    st.rerun()
    
    # 隠しボタンを画面から完全に消し去るための透明化CSS
    st.html("<style>div:has(> button[aria-help=\"hidden\"]) { display: none !important; }</style>")
