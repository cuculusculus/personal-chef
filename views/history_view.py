# views/history_view.py
import streamlit as st
from services.data_service import toggle_favorite, delete_favorite, prepare_recipe_for_cooking
from views.recipe_helpers import render_saved_recipe_detail
# 定数を新しくインポート
from config.constants import PAGE_DETAIL

def render_recipe_detail_fullscreen():
    """詳細画面のみを独立描画する関数"""
    recipe = st.session_state.get("selected_recipe")
    mode = st.session_state.get("selected_recipe_mode")
    idx = st.session_state.get("selected_recipe_idx")
    is_fav = st.session_state.get("selected_recipe_is_fav", False)
    
    if not recipe: 
        return

    # 【修正】「← 戻る」ボタンを押したら、元のページIDをセッションに書き戻して遷移する
    if st.button("← 戻る", type="secondary", use_container_width=True):
        st.session_state.page = mode  # 元いた一覧ページ（favoriteかhistory）に戻す
        st.session_state.update({
            "selected_recipe": None, 
            "selected_recipe_mode": None, 
            "selected_recipe_idx": None, 
            "selected_recipe_is_fav": False
        })
        st.rerun(scope="app")
        
    st.subheader(":material/kitchen: レシピ詳細")
    st.markdown("---")
    
    render_saved_recipe_detail(recipe, recipe.get("servings", 2), show_buttons=False)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 各操作ボタン（すべて st.session_state.page = mode を戻す処理を追加）
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" 調理する", icon=":material/fork_spoon:", use_container_width=True):
            prepare_recipe_for_cooking(recipe)
            st.session_state.page = mode
            st.session_state.update({"selected_recipe": None, "selected_recipe_mode": None, "selected_recipe_idx": None, "selected_recipe_is_fav": False})
            st.rerun(scope="app")
            
    with col2:
        if mode == "favorite":
            if st.button("解除", icon=":material/bookmark_remove:", type="secondary", use_container_width=True):
                delete_favorite(idx)
                st.session_state.page = mode
                st.session_state.update({"selected_recipe": None, "selected_recipe_mode": None, "selected_recipe_idx": None, "selected_recipe_is_fav": False})
                st.rerun(scope="app")
        elif mode == "history":
            btn_label = "お気に入り解除" if is_fav else "お気に入り登録"
            btn_icon = ":material/bookmark_remove:" if is_fav else ":material/bookmark_add:"
            btn_type = "primary" if is_fav else "secondary"
            if st.button(btn_label, icon=btn_icon, type=btn_type, use_container_width=True):
                toggle_favorite(recipe)
                st.session_state.page = mode
                st.session_state.update({"selected_recipe": None, "selected_recipe_mode": None, "selected_recipe_idx": None, "selected_recipe_is_fav": False})
                st.rerun(scope="app")


def render_favorite_page():
    st.subheader(":material/menu_book_2: お気に入りレシピ")
    if not st.session_state.favorite_recipes:
        st.info("お気に入りに登録されたレシピはまだありません。")
        return

    for idx, recipe in enumerate(st.session_state.favorite_recipes):
        if st.button(f"{recipe['title']}", icon=":material/star:", key=f"fav_btn_{idx}", use_container_width=True):
            # 【修正】セッションページを正式に PAGE_DETAIL（detail）に切り替える
            st.session_state.page = PAGE_DETAIL
            st.session_state.update({
                "selected_recipe": recipe, 
                "selected_recipe_mode": "favorite", 
                "selected_recipe_idx": idx
            })
            st.rerun(scope="app")


def render_history_page():
    st.subheader(":material/history_edu: 過去の提案履歴")
    if not st.session_state.recipe_history:
        st.info("過去に提案されたレシピ履歴はありません。")
        return

    for idx, recipe in enumerate(st.session_state.recipe_history):
        recipe_id = recipe.get("id")
        is_fav = any(f.get("id") == recipe_id for f in st.session_state.favorite_recipes)
        
        label = f"{recipe['title']}"
        icon = ":material/star:" if is_fav else ":material/push_pin:"
        
        if st.button(label, icon=icon, key=f"hist_btn_{idx}", use_container_width=True):
            # 【修正】セッションページを正式に PAGE_DETAIL（detail）に切り替える
            st.session_state.page = PAGE_DETAIL
            st.session_state.update({
                "selected_recipe": recipe, 
                "selected_recipe_mode": "history", 
                "selected_recipe_is_fav": is_fav
            })
            st.rerun(scope="app")
