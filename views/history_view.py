# views/history_view.py
import streamlit as st
from services.data_service import toggle_favorite, delete_favorite, prepare_recipe_for_cooking
from views.recipe_helpers import render_saved_recipe_detail

def render_recipe_detail_fullscreen():
    """st.dialogを使わず、画面全体を使って最上部から100%表示するレシピ詳細画面。"""
    recipe = st.session_state.get("selected_recipe")
    mode = st.session_state.get("selected_recipe_mode")
    idx = st.session_state.get("selected_recipe_idx")
    is_fav = st.session_state.get("selected_recipe_is_fav", False)

    if not recipe:
        return

    # 「← 戻る」ボタンを押したら、詳細表示用のセッションをすべてクリアして全体リロード
    if st.button("← 戻る", type="secondary", use_container_width=True):
        st.session_state["selected_recipe"] = None
        st.session_state["selected_recipe_mode"] = None
        st.session_state["selected_recipe_idx"] = None
        st.session_state["selected_recipe_is_fav"] = False
        st.rerun(scope="app")
        
    st.subheader(":material/kitchen: レシピ詳細")
    st.markdown("---")

    render_saved_recipe_detail(recipe, recipe.get("servings", 2), show_buttons=False)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 操作ボタン群
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" 調理する", icon=":material/fork_spoon:", use_container_width=True):
            prepare_recipe_for_cooking(recipe)
            st.session_state["selected_recipe"] = None
            st.rerun(scope="app")
            
    with col2:
        if mode == "favorite":
            if st.button("解除", icon=":material/bookmark_remove:", type="secondary", use_container_width=True):
                delete_favorite(idx)
                st.session_state["selected_recipe"] = None
                st.rerun(scope="app")
        elif mode == "history":
            btn_label = "お気に入り解除" if is_fav else "お気に入り登録"
            btn_icon = ":material/bookmark_remove:" if is_fav else ":material/bookmark_add:"
            btn_type = "primary" if is_fav else "secondary"
            if st.button(btn_label, icon=btn_icon, type=btn_type, use_container_width=True):
                toggle_favorite(recipe)
                st.session_state["selected_recipe"] = None
                st.rerun(scope="app")


def render_favorite_page():
    # 【超重要：完全分離】詳細モード中か、一覧モード中かを if-else で完全に分けます
    if st.session_state.get("selected_recipe") is not None and st.session_state.get("selected_recipe_mode") == "favorite":
        render_recipe_detail_fullscreen()
    else:
        # 詳細が閉じていれば、お気に入り一覧だけをきれいに描画
        st.subheader(":material/menu_book_2: お気に入りレシピ")
        if not st.session_state.favorite_recipes:
            st.info("お気に入りに登録されたレシピはまだありません。")
            return

        for idx, recipe in enumerate(st.session_state.favorite_recipes):
            if st.button(f"{recipe['title']}", icon=":material/star:", key=f"fav_btn_{idx}", use_container_width=True):
                st.session_state["selected_recipe"] = recipe
                st.session_state["selected_recipe_mode"] = "favorite"
                st.session_state["selected_recipe_idx"] = idx
                st.rerun(scope="app")


def render_history_page():
    # 【超重要：完全分離】詳細モード中か、一覧モード中かを if-else で完全に分けます
    if st.session_state.get("selected_recipe") is not None and st.session_state.get("selected_recipe_mode") == "history":
        render_recipe_detail_fullscreen()
    else:
        # 詳細が閉じていれば、過去の履歴一覧だけをきれいに描画
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
                st.session_state["selected_recipe"] = recipe
                st.session_state["selected_recipe_mode"] = "history"
                st.session_state["selected_recipe_is_fav"] = is_fav
                st.rerun(scope="app")
