# app.py
import streamlit as st
from services.session_initializer import initialize_session
from config.styles import apply_styles
from config.constants import *
from components.footer_nav import render_footer_nav
from views.recipe_view import render_recipe_page
from views.stock_view import render_stock_page_fragment
from views.history_view import render_favorite_page, render_history_page, render_recipe_detail_fullscreen

# ページ設定
st.set_page_config(
    page_title="Smart Fridge Chef", 
    page_icon="👨‍🍳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. セッションの初期化
initialize_session()

# フッターのページ切り替えURL監視
current_page = st.session_state.get("page", PAGE_RECIPE)
query_params = st.query_params

if "page" in query_params and query_params["page"] != current_page:
    st.session_state.page = query_params["page"]
    st.session_state["selected_recipe"] = None
    st.session_state["selected_recipe_mode"] = None
    st.session_state["selected_recipe_idx"] = None
    st.session_state["selected_recipe_is_fav"] = False
    st.rerun()

# 2. スタイルの適用
apply_styles()

# ⭕ ルーティングに「詳細ページ」を正式なページとして追加登録
ROUTES = {
    PAGE_RECIPE: render_recipe_page,
    PAGE_STOCK: render_stock_page_fragment,
    PAGE_FAVORITE: render_favorite_page,
    PAGE_HISTORY: render_history_page,
    PAGE_DETAIL: render_recipe_detail_fullscreen, # 追加
}

# 3. メインコンテンツの描画（ページ切り替えにより古いキャッシュは100%消滅します）
ROUTES.get(
    st.session_state.page,
    render_recipe_page
)()

# 4. 完全固定の下部ナビゲーション
render_footer_nav()
