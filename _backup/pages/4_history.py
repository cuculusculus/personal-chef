#history.py
import streamlit as st
from utils import render_saved_recipe_detail, save_json, FAVORITE_FILE

st.title("📁 過去の提案履歴")
st.caption(f"AIが提案したレシピ履歴（現在：{len(st.session_state.recipe_history)}件）")

if st.session_state.recipe_history:
    for idx, recipe in enumerate(st.session_state.recipe_history):
        recipe_id = recipe.get("id")
        is_fav = any(f.get("id") == recipe_id for f in st.session_state.favorite_recipes)
        fav_icon = "⭐" if is_fav else "📌"

        col_exp, col_fav_btn = st.columns([5, 1])
        with col_exp:
            with st.expander(f"{fav_icon} {recipe['title']}"):
                render_saved_recipe_detail(recipe, recipe.get("servings", 2))
                _, col_btn = st.columns([4, 1])
                if col_btn.button("🍳 調理する", key=f"hist_cook_{idx}"):
                    st.session_state["current_recipe_obj"] = recipe
                    st.session_state["servings_input"] = recipe.get("servings", 2)
                    st.switch_page("pages/1_recipe.py")

        with col_fav_btn:
            if is_fav:
                if st.button("⭐解除", key=f"hist_fav_{idx}", type="primary"):
                    st.session_state.favorite_recipes = [f for f in st.session_state.favorite_recipes if f.get("id") != recipe_id]
                    save_json(FAVORITE_FILE, st.session_state.favorite_recipes)
                    st.rerun()
            else:
                if st.button("⭐登録", key=f"hist_fav_{idx}", type="secondary"):
                    st.session_state.favorite_recipes.insert(0, recipe)
                    save_json(FAVORITE_FILE, st.session_state.favorite_recipes)
                    st.rerun()
else:
    st.info("過去に提案されたレシピ履歴はありません。")