#3_favorite.py
import streamlit as st
from utils import render_saved_recipe_detail, save_json, FAVORITE_FILE

st.title("⭐ お気に入りレシピ")

if st.session_state.favorite_recipes:
    to_remove = None
    for idx, recipe in enumerate(st.session_state.favorite_recipes):
        col_exp, col_del = st.columns([5, 1])
        with col_exp:
            with st.expander(f"⭐ {recipe['title']}"):
                render_saved_recipe_detail(recipe, recipe.get("servings", 2))
                _, col_btn = st.columns([4, 1])
                if col_btn.button("🍳 調理する", key=f"fav_cook_{idx}"):
                    st.session_state["current_recipe_obj"] = recipe
                    st.session_state["servings_input"] = recipe.get("servings", 2)
                    st.switch_page("pages/1_recipe.py") # 💡 公式の機能で一瞬でレシピページへ移動

        with col_del:
            if st.button("🗑️ 解除", key=f"fav_del_{idx}", type="primary"):
                to_remove = idx

    if to_remove is not None:
        st.session_state.favorite_recipes.pop(to_remove)
        save_json(FAVORITE_FILE, st.session_state.favorite_recipes)
        st.rerun()
else:
    st.info("お気に入りに登録されたレシピはまだありません。")