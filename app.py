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
    page_title="Personal Chef", 
    page_icon="👨‍🍳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.write("APP開始")
# 1. セッションの初期化
initialize_session()
st.write("初期化後")
apply_styles()
st.write("スタイル後")

st.write("現在ページ:", st.session_state.page)

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
st.write("画面描画後")
# 4. 完全固定の下部ナビゲーション
render_footer_nav()
