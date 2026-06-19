# views/history_view.py
import streamlit as st
from services.data_service import toggle_favorite, delete_favorite, prepare_recipe_for_cooking
from views.recipe_helpers import render_saved_recipe_detail

def render_recipe_detail_fullscreen(placeholder, recipe, mode, idx=None, is_fav=False):
    """
    st.empty()で作ったクリーンな専用エリアを1から上書きして描画する詳細画面。
    """
    # placeholder.container() を使うことで、この中身が描画される瞬間、
    # 以前そこに表示されていたお気に入りや履歴の一覧リストは文字通り「強制消去」されます。
    with placeholder.container():
        # 最上部に配置する「戻る」ボタン
        if st.button("← 戻る", type="secondary", use_container_width=True):
            # 詳細表示用のゴミをすべて消去して画面全体をガラガラポンとリフレッシュする
            st.session_state.update({
                "selected_recipe": None, 
                "selected_recipe_mode": None, 
                "selected_recipe_idx": None, 
                "selected_recipe_is_fav": False
            })
            st.rerun(scope="app")
            
        st.subheader(":material/kitchen: レシピ詳細")
        st.markdown("---")

        # 詳細本文の描画
        render_saved_recipe_detail(recipe, recipe.get("servings", 2), show_buttons=False)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 操作ボタン
        col1, col2 = st.columns(2)
        with col1:
            if st.button(" 調理する", icon=":material/fork_spoon:", use_container_width=True):
                prepare_recipe_for_cooking(recipe)
                st.session_state.update({"selected_recipe": None, "selected_recipe_mode": None, "selected_recipe_idx": None, "selected_recipe_is_fav": False})
                st.rerun(scope="app")
                
        with col2:
            if mode == "favorite":
                if st.button("解除", icon=":material/bookmark_remove:", type="secondary", use_container_width=True):
                    delete_favorite(idx)
                    st.session_state.update({"selected_recipe": None, "selected_recipe_mode": None, "selected_recipe_idx": None, "selected_recipe_is_fav": False})
                    st.rerun(scope="app")
            elif mode == "history":
                btn_label = "お気に入り解除" if is_fav else "お気に入り登録"
                btn_icon = ":material/bookmark_remove:" if is_fav else ":material/bookmark_add:"
                btn_type = "primary" if is_fav else "secondary"
                if st.button(btn_label, icon=btn_icon, type=btn_type, use_container_width=True):
                    toggle_favorite(recipe)
                    st.session_state.update({"selected_recipe": None, "selected_recipe_mode": None, "selected_recipe_idx": None, "selected_recipe_is_fav": False})
                    st.rerun(scope="app")


def render_favorite_page():
    # 1. 画面の最上部に、中身を自由に入れ替え・完全消去できる「空の箱（st.empty）」を用意します
    main_placeholder = st.empty()

    # 2. 詳細モードのフラグが立っている場合は、上の空の箱を詳細画面で「上書き」して処理を終了
    if st.session_state.get("selected_recipe") is not None and st.session_state.get("selected_recipe_mode") == "favorite":
        recipe = st.session_state["selected_recipe"]
        idx = st.session_state.get("selected_recipe_idx")
        render_recipe_detail_fullscreen(main_placeholder, recipe, mode="favorite", idx=idx)
        return

    # 3. 通常時（詳細を閉じたとき）は、空の箱の中に「お気に入り一覧」を綺麗に流し込みます
    with main_placeholder.container():
        st.subheader(":material/menu_book_2: お気に入りレシピ")
        if not st.session_state.favorite_recipes:
            st.info("お気に入りに登録されたレシピはまだありません。")
            return

        for idx, recipe in enumerate(st.session_state.favorite_recipes):
            if st.button(f"{recipe['title']}", icon=":material/star:", key=f"fav_btn_{idx}", use_container_width=True):
                st.session_state.update({
                    "selected_recipe": recipe, 
                    "selected_recipe_mode": "favorite", 
                    "selected_recipe_idx": idx
                })
                st.rerun(scope="app")


def render_history_page():
    # 1. 画面の最上部に、中身を自由に入れ替え・完全消去できる「空の箱（st.empty）」を用意します
    main_placeholder = st.empty()

    # 2. 詳細モードのフラグが立っている場合は、上の空の箱を詳細画面で「上書き」して処理を終了
    if st.session_state.get("selected_recipe") is not None and st.session_state.get("selected_recipe_mode") == "history":
        recipe = st.session_state["selected_recipe"]
        is_fav = st.session_state.get("selected_recipe_is_fav", False)
        render_recipe_detail_fullscreen(main_placeholder, recipe, mode="history", is_fav=is_fav)
        return

    # 3. 通常時（詳細を閉じたとき）は、空の箱の中に「過去の履歴一覧」を綺麗に流し込みます
    with main_placeholder.container():
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
                st.session_state.update({
                    "selected_recipe": recipe, 
                    "selected_recipe_mode": "history", 
                    "selected_recipe_is_fav": is_fav
                })
                st.rerun(scope="app")
