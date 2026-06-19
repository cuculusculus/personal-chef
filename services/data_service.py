# services/data_service.py
import streamlit as st
from utils import save_json
from config.constants import FAVORITE_FILE
def toggle_favorite(recipe):
    """お気に入りの追加/削除を切り替える"""
    recipe_id = recipe.get("id")
    is_fav = any(f.get("id") == recipe_id for f in st.session_state.favorite_recipes)
    
    if is_fav:
        st.session_state.favorite_recipes = [f for f in st.session_state.favorite_recipes if f.get("id") != recipe_id]
    else:
        st.session_state.favorite_recipes.insert(0, dict(recipe))
        
    save_json(FAVORITE_FILE, st.session_state.favorite_recipes)

def delete_favorite(idx):
    """お気に入りから完全に削除する"""
    st.session_state.favorite_recipes.pop(idx)
    save_json(FAVORITE_FILE, st.session_state.favorite_recipes)

def prepare_recipe_for_cooking(recipe):
    """調理するための状態をセットアップする"""
    st.session_state["current_recipe_obj"] = recipe
    st.session_state["servings_input"] = recipe.get("servings", 2)
    st.session_state["recipe_generated"] = True
    st.session_state.page = "recipe" # app.pyの定数に合わせて設定
