# app.py
import streamlit as st
from services.session_initializer import initialize_session
from config.styles import apply_styles
from config.constants import *
from components.footer_nav import render_footer_nav
from views.recipe_view import render_recipe_page
from views.stock_view import render_stock_page_fragment
from views.history_view import render_favorite_page, render_history_page

# ページ設定
st.set_page_config(
    page_title="Smart Fridge Chef", 
    page_icon="👨‍🍳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_styles()
initialize_session()

# =========================================================
# 【フッターナビ連動用アンテナ】
# =========================================================
current_page = st.session_state.get("page", PAGE_RECIPE)
query_params = st.query_params

if "page" in query_params and query_params["page"] != current_page:
    st.session_state.page = query_params["page"]
    st.rerun()

# =========================================================
# 【高速化のキモ】今必要なページ「だけ」をピンポイントで動かす
# =========================================================
# 選択されているページに応じて、該当する関数の「1つだけ」を実行します。
# これにより、裏側で他の重いページが同時に計算されるのを100%完全に防ぎ、
# タブを切り替えた瞬間に画面がサッと表示されるようになります。
target_page = st.session_state.get("page", PAGE_RECIPE)

if target_page == PAGE_STOCK:
    render_stock_page_fragment()
elif target_page == PAGE_FAVORITE:
    render_favorite_page()
elif target_page == PAGE_HISTORY:
    render_history_page()
else:
    render_recipe_page() # デフォルトはレシピ考案ページ

# --- 完全固定の下部ナビゲーション ---
render_footer_nav()
