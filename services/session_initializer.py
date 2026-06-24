#services/session_initializer.py
import streamlit as st
from utils import load_json_cached
from config.constants import (
    HISTORY_FILE,
    FAVORITE_FILE,
    INGREDIENTS_FILE,
    BASE_OPTIONS_FILE,
)

DEFAULT_BASE_OPTIONS = {
    "meat": ["豚小間肉", "牛ロース肉", "鶏もも肉", "豚ひき肉", "ベーコン", "ソーセージ"],
    "fish": ["鮭", "サバ", "マグロ", "ツナ缶", "エビ", "イカ"],
    "vegetables": ["キャベツ", "玉ねぎ", "にんじん", "じゃがいも", "大根", "トマト", "もやし", "レタス"],
    "staple": ["白米", "もち麦", "食パン", "うどん", "パスタ", "焼きそば"],
    "dairy": ["卵", "豆腐", "納豆", "チーズ", "牛乳", "ヨーグルト", "油揚げ"],
    "seasonings": ["醤油", "味噌", "砂糖", "塩", "コショウ", "マヨネーズ", "ケチャップ", "みりん", "酒", "コンソメ", "鶏ガラ"]
}

def initialize_recipe_history():

    if "recipe_history" not in st.session_state:
        st.session_state.recipe_history = (
            load_json_cached(HISTORY_FILE, [])
        )

def initialize_favorites():

    if "favorite_recipes" not in st.session_state:
        st.session_state.favorite_recipes = (
            load_json_cached(FAVORITE_FILE, [])
        )

def initialize_base_options():

    if "base_options" not in st.session_state:

        loaded_options = load_json_cached(
            BASE_OPTIONS_FILE,
            DEFAULT_BASE_OPTIONS
        )

        for cat in DEFAULT_BASE_OPTIONS:

            if cat not in loaded_options:
                loaded_options[cat] = DEFAULT_BASE_OPTIONS[cat]

        st.session_state.base_options = loaded_options

def initialize_stock_data():

    if "stock_data" in st.session_state:
        return
    default_stock_structure = {
        cat: {}
        for cat in DEFAULT_BASE_OPTIONS.keys()
    }

    raw_stock = load_json_cached(
        INGREDIENTS_FILE,
        default_stock_structure
    )

    st.session_state["stock_data"] = {}

    for cat in DEFAULT_BASE_OPTIONS.keys():

        data = raw_stock.get(cat, {})

        if isinstance(data, list):

            st.session_state["stock_data"][cat] = {
                item: "1.0個"
                for item in data
            }
        elif isinstance(data, dict):

            st.session_state["stock_data"][cat] = data
        else:

            st.session_state["stock_data"][cat] = {}

def initialize_servings():

    if "servings_input" not in st.session_state:
        st.session_state["servings_input"] = 2

def initialize_page():

    if "page" not in st.session_state:
        st.session_state.page = "👩‍🍳 レシピ考案"

def initialize_session():
    initialize_recipe_history()
    initialize_favorites()
    initialize_base_options()
    initialize_stock_data()
    initialize_servings()
    initialize_page()
