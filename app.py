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

# 1. セッションの初期化
initialize_session()

apply_styles()
# =========================================================
# 【ここを追加】自動遷移の障害物（古いURLの文字）をクリアする
# =========================================================
# もしセッション状態のページと、URLのパラメータにズレがある場合（ボタンでページが切り替えられたとき）
if "page" in st.query_params and st.query_params["page"] != st.session_state.page:
    # URLの末尾のパラメータを現在のセッションページ（"recipe"など）に自動で書き換えます
    st.query_params["page"] = st.session_state.page
# =========================================================

# 通常のルーティング
ROUTES = {
    PAGE_RECIPE: render_recipe_page,
    PAGE_STOCK: render_stock_page_fragment,
    PAGE_FAVORITE: render_favorite_page,
    PAGE_HISTORY: render_history_page,
}

# 3. メインコンテンツの描画
ROUTES.get(
    st.session_state.page,
    render_recipe_page
)()

# 4. 完全固定の下部ナビゲーション
render_footer_nav()
