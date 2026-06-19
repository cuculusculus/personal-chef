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

initialize_session()
# =========================================================
# 【超重要：新規追加（最外層ディフェンス）】
# もし詳細画面を開くフラグが立っていたら、通常ページ（一覧）は1行も動かさず、
# ここで詳細画面だけを完全ピンポイントで描画して終了します。
# =========================================================
if st.session_state.get("selected_recipe") is not None:
    render_recipe_detail_fullscreen()
    render_footer_nav()
    st.stop() # 以降の通常ルーティングへの突入を完全に物理ブロック
# =========================================================
apply_styles()

# ルーティング
ROUTES = {
    PAGE_RECIPE: render_recipe_page,
    PAGE_STOCK: render_stock_page_fragment,
    PAGE_FAVORITE: render_favorite_page,
    PAGE_HISTORY: render_history_page,
}

# 描画
ROUTES.get(
    st.session_state.page,
    render_recipe_page
)()

# --- 完全固定の下部ナビゲーション（HTML版） ---
render_footer_nav()
