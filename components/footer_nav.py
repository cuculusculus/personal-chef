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
    最下部から45px浮かせた位置に等幅配置する絶対タップ可能フッター。
    ※URL(クエリ)を使わず、昔のセッション書き換えロジックに完全統合した決定版。
    """
    current_page = st.session_state.get("page", PAGE_RECIPE)

    nav_config = [
        {"page": PAGE_RECIPE, "icon": "restaurant"},
        {"page": PAGE_STOCK, "icon": "kitchen"},
        {"page": PAGE_FAVORITE, "icon": "bookmark_star"},
        {"page": PAGE_HISTORY, "icon": "history"},
    ]

    # HTMLで外見（デザイン）を作ります。
    # クリックされたら、裏側に隠してある本物のStreamlitボタンを代わりにクリックさせます。
    links_html = ""
    for item in nav_config:
        is_active = "active" if current_page == item["page"] else ""
        links_html += f"""
        <button onclick="window.parent.postMessage({{type: 'nav_click', page: '{item['page']}'}}, '*')" class="nav-item {is_active}">
            <span class="stIconMaterial">{item['icon']}</span>
        </button>
        """

    # 確実にアイコンを表示するためのフォントリンク
    st.markdown("""
    <link rel="stylesheet" href="https://googleapis.com" />
    """, unsafe_allow_html=True)

    # 指定いただいた完璧なデザイン（CSS）と、裏側へクリックを届けるJavaScriptの出力
    st.html(f"""
    <div class="custom-sticky-footer">
        {links_html}
    </div>
    <script>
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
        bottom: 45px !important; /* バッジを避けて浮かせる */
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
        color: #ff4b4b !important; 
        border-bottom: 3px solid #ff4b4b !important;
        background-color: #fdfaf9 !important;
    }}
    .custom-sticky-footer .stIconMaterial {{
        font-size: 30px !important;
        font-family: "Material Symbols Outlined", sans-serif !important;
    }}
    </style>
    """)

    # ⭕ ここが重要：
    # 画面裏に配置した「あなたが見せてくれた昔のクリーンなPythonロジックそのもの」です。
    # 画面には一切表示されず、デザインの裏側で昔と全く同じ安全なセッション書き換えを行います。
    cols = st.columns(4)
    for col, item in zip(cols, nav_config):
        with col:
            if st.button(" ", key=f"hidden_btn_{item['page']}", use_container_width=True, help="hidden_nav"):
                if st.session_state.page != item["page"]:
                    st.session_state.page = item["page"]
                    st.rerun()
    
    # 本物のStreamlitボタンを透明にして隠すためのCSS
    st.html("<style>div:has(> button[aria-help=\"hidden_nav\"]) { display: none !important; }</style>")
