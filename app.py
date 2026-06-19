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
# 【超重要：新規追加】
# フッターのボタン（URLのクエリパラメータ）が押されたかを、画面を描画する前に最優先でチェックする。
# ページが切り替わる場合は、ここで他ページの詳細画面のデータを完全に真っさらにします。
# =========================================================
current_page = st.session_state.get("page", PAGE_RECIPE)
query_params = st.query_params

if "page" in query_params and query_params["page"] != current_page:
    # ページを更新
    st.session_state.page = query_params["page"]
    
    # 詳細表示用のセッションのゴミをここで確実に全消去
    st.session_state["selected_recipe"] = None
    st.session_state["selected_recipe_mode"] = None
    st.session_state["selected_recipe_idx"] = None
    st.session_state["selected_recipe_is_fav"] = False
    st.rerun()
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
