#1_recipe.py
import streamlit as st
from views.recipe_view import render_recipe_page

# 1_recipe.py はこれだけで十分です！
st.title("👩‍🍳 AIレシピ考案")
render_recipe_page()