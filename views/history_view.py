# views/history_view.py
import streamlit as st
from services.data_service import toggle_favorite, delete_favorite, prepare_recipe_for_cooking
from views.recipe_helpers import render_saved_recipe_detail

def render_recipe_detail_fullscreen():
    """詳細画面のみを独立描画する関数（戻るボタン機能付き）"""
    recipe = st.session_state.get("selected_recipe")
    if not recipe: return

    if st.button("← 戻る", type="secondary", use_container_width=True):
        st.session_state.update({"selected_recipe": None, "selected_recipe_mode": None, "selected_recipe_idx": None, "selected_recipe_is_fav": False})
        st.rerun(scope="app")
        
    st.subheader(":material/kitchen: レシピ詳細")
    st.markdown("---")
    render_saved_recipe_detail(recipe, recipe.get("servings", 2), show_buttons=False)
    # 調理・お気に入り操作ボタンのロジックは従来通り（省略）

# 以下、リスト表示用関数（詳細ロジックを分離）
def render_favorite_page():
    st.subheader(":material/menu_book_2: お気に入りレシピ")
    # 一覧表示と選択時のセッション更新のみを行う
    for idx, recipe in enumerate(st.session_state.favorite_recipes):
        if st.button(f"{recipe['title']}", key=f"fav_btn_{idx}"):
            st.session_state.update({"selected_recipe": recipe, "selected_recipe_mode": "favorite", "selected_recipe_idx": idx})
            st.rerun(scope="app")

def render_history_page():
    st.subheader(":material/history_edu: 過去の提案履歴")
    # 一覧表示と選択時のセッション更新のみを行う
    for idx, recipe in enumerate(st.session_state.recipe_history):
        if st.button(f"{recipe['title']}", key=f"hist_btn_{idx}"):
            st.session_state.update({"selected_recipe": recipe, "selected_recipe_mode": "history"})
            st.rerun(scope="app")
