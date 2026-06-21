# views/history_view.py
import streamlit as st

from services.data_service import (
    toggle_favorite,
    delete_favorite,
    prepare_recipe_for_cooking
)
from views.recipe_helpers import render_saved_recipe_detail
# ダイアログ
@st.dialog(":material/menu_book: レシピ詳細")
def show_recipe_detail_dialog(recipe, mode, idx=None, is_fav=False):

    # レシピ表示
    render_saved_recipe_detail(
        recipe,
        recipe.get("servings", 2)
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # 操作ボタン
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "再表示",
            icon=":material/restaurant:",
            key=f"reopen_{recipe['id']}",
            use_container_width=True
        ):
            from config.constants import PAGE_RECIPE

            st.session_state.page = PAGE_RECIPE
            
            # レシピ本体
            st.session_state["current_recipe_obj"] = recipe
            st.session_state["recipe_generated"] = True

            # 人数
            st.session_state["servings_input"] = recipe.get("servings", 2)

            # タイプ・テーマ復元
            st.session_state["temp_dish_type"] = recipe.get(
                "dish_type",
                "おまかせ"
            )
            st.session_state["temp_mood"] = recipe.get(
                "mood",
                "おまかせ"
            )

            st.query_params["page"] = PAGE_RECIPE
            st.rerun()

    with col2:
        if mode == "favorite":
            if st.button(
                "解除",
                icon=":material/bookmark_remove:",
                type="secondary",
                use_container_width=True
            ):
                delete_favorite(idx)
                st.rerun()

        elif mode == "history":
            btn_label = "お気に入り解除" if is_fav else "お気に入り登録"
            btn_icon = ":material/bookmark_remove:" if is_fav else ":material/bookmark_add:"
            btn_type = "primary" if is_fav else "secondary"

            if st.button(
                btn_label,
                icon=btn_icon,
                type=btn_type,
                use_container_width=True
            ):
                toggle_favorite(recipe)
                st.rerun()

# お気に入り画面
def render_favorite_page():

    st.subheader(":material/bookmark_star: Favorites")

    if not st.session_state.favorite_recipes:
        st.info("お気に入りに登録されたレシピはまだありません。")
        return

    for idx, recipe in enumerate(st.session_state.favorite_recipes):
        if st.button(
            recipe["title"],
            icon=":material/star:",
            key=f"fav_btn_{idx}",
            use_container_width=True
        ):
            show_recipe_detail_dialog(
                recipe,
                mode="favorite",
                idx=idx
            )


# 履歴画面
def render_history_page():

    st.subheader(":material/overview: Cooking Log")

    if not st.session_state.recipe_history:
        st.info("過去に提案されたレシピ履歴はありません。")
        return

    for idx, recipe in enumerate(st.session_state.recipe_history):

        recipe_id = recipe.get("id")
        is_fav = any(
            f.get("id") == recipe_id
            for f in st.session_state.favorite_recipes
        )

        icon = ":material/star:" if is_fav else ":material/push_pin:"

        if st.button(
            recipe["title"],
            icon=icon,
            key=f"hist_btn_{idx}",
            use_container_width=True
        ):
            show_recipe_detail_dialog(
                recipe,
                mode="history",
                idx=idx,
                is_fav=is_fav
            )
