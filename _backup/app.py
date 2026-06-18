# app.py
import streamlit as st
from utils import load_json_cached, get_app_css, HISTORY_FILE, FAVORITE_FILE, INGREDIENTS_FILE, BASE_OPTIONS_FILE

# 1. 外部ビューモジュールから描画関数をインポート
from views.recipe_view import render_recipe_page
from views.stock_view import render_stock_page_fragment
from views.history_view import render_favorite_page, render_history_page

# ページ設定
st.set_page_config(
    page_title="Smart Fridge Chef", 
    page_icon="👨‍🍳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* ターゲットとなるコンテナを固定 */
    [data-testid="stVerticalBlock"]:has(div[data-key="footer_nav"]) {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        z-index: 99999;
        padding: 10px 0;
        border-top: 1px solid #ddd;
    }
    .stApp {
        padding-bottom: 100px;
    }
    </style>
""", unsafe_allow_html=True)
# st.markdown("""
#     <style>
#     /* アイコンのサイズを大きくする設定 */
#     .material-symbols-outlined {
#         font-size: 100px !important; /* ここでサイズを調整 */
#     }
    
#     /* 必要に応じてボタン内の余白も調整 */
#     button[data-testid="base"] {
#         padding: 20px !important;
#     }
#     </style>
# """, unsafe_allow_html=True)
# 高速化CSS適用
st.markdown(get_app_css(), unsafe_allow_html=True)

# データの初期化
default_base_options = {
    "meat": ["豚肉", "牛肉", "鶏肉", "ひき肉", "ベーコン", "ソーセージ"],
    "fish": ["鮭", "サバ", "マグロ", "ツナ缶", "エビ", "イカ"],
    "vegetables": ["キャベツ", "玉ねぎ", "にんじん", "じゃがいも", "大根", "トマト", "もやし", "レタス"],
    "staple": ["白米", "もち麦", "食パン", "うどん", "パスタ", "焼きそば"],
    "dairy": ["卵", "豆腐", "納豆", "チーズ", "牛乳", "ヨーグルト", "油揚げ"],
    "seasonings": ["醤油", "味噌", "砂糖", "塩", "コショウ", "マヨネーズ", "ケチャップ", "みりん", "酒", "コンソメ", "鶏ガラ"]
}

if "recipe_history" not in st.session_state:
    st.session_state.recipe_history = load_json_cached(HISTORY_FILE, [])
if "favorite_recipes" not in st.session_state:
    st.session_state.favorite_recipes = load_json_cached(FAVORITE_FILE, [])

if "stock_data" not in st.session_state:
    raw_stock = load_json_cached(INGREDIENTS_FILE, {"meat": {}, "fish": {}, "vegetables": {},"staple": {}, "dairy": {}, "seasonings": {}})
    st.session_state["stock_data"] = {}
    for cat in ["meat", "fish", "vegetables", "staple", "dairy", "seasonings"]:
        data = raw_stock.get(cat, {})
        if isinstance(data, list):
            st.session_state["stock_data"][cat] = {item: "1.0個" for item in data}
        else:
            st.session_state["stock_data"][cat] = data

if "base_options" not in st.session_state:
    loaded_options = load_json_cached(BASE_OPTIONS_FILE, default_base_options)
    
    # 既存データに足りないキーがあれば、default_base_options から補完する
    for cat in default_base_options.keys():
        if cat not in loaded_options:
            loaded_options[cat] = default_base_options[cat]
            
    st.session_state["base_options"] = loaded_options

if "stock_data" not in st.session_state:
    # 読み込む際のデフォルト辞書に全キーを含める
    default_stock_structure = {cat: {} for cat in default_base_options.keys()}
    raw_stock = load_json_cached(INGREDIENTS_FILE, default_stock_structure)
    
    st.session_state["stock_data"] = {}
    for cat in default_base_options.keys():
        data = raw_stock.get(cat, {})
        if isinstance(data, list):
            st.session_state["stock_data"][cat] = {item: "1.0個" for item in data}
        else:
            st.session_state["stock_data"][cat] = data

if "servings_input" not in st.session_state:
    st.session_state["servings_input"] = 2

# 定数とルーティング管理
PAGE_RECIPE = "👩‍🍳 レシピ考案"
PAGE_STOCK = "🛒 食材管理"
PAGE_FAVORITE = "⭐ お気に入り"
PAGE_HISTORY = "📁 履歴"

if 'page' not in st.session_state:
    st.session_state.page = PAGE_RECIPE

# --- ページ描画のルーティングスイッチ ---
if st.session_state.page == PAGE_STOCK:
    render_stock_page_fragment()
elif st.session_state.page == PAGE_RECIPE:
    render_recipe_page()
elif st.session_state.page == PAGE_FAVORITE:
    #render_favorite_page(PAGE_RECIPE)
    render_favorite_page()
elif st.session_state.page == PAGE_HISTORY:
    render_history_page()

# # --- 完全固定の下部ナビゲーション ---
# with st.container(key="footer_nav"):
#     col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
    
#     with col_nav1:
#         if st.button("👩‍🍳\nレシピ", key="nav_recipe", type="primary" if st.session_state.page == PAGE_RECIPE else "secondary", use_container_width=True):
#             if st.session_state.page != PAGE_RECIPE:
#                 st.session_state.page = PAGE_RECIPE
#                 st.rerun()
#     with col_nav2:
#         if st.button("🛒\n食材", key="nav_stock", type="primary" if st.session_state.page == PAGE_STOCK else "secondary", use_container_width=True):
#             if st.session_state.page != PAGE_STOCK:
#                 st.session_state.page = PAGE_STOCK
#                 st.rerun()
#     with col_nav3:
#         if st.button("⭐\nお気に入り", key="nav_fav", type="primary" if st.session_state.page == PAGE_FAVORITE else "secondary", use_container_width=True):
#             if st.session_state.page != PAGE_FAVORITE:
#                 st.session_state.page = PAGE_FAVORITE
#                 st.rerun()
#     with col_nav4:
#         if st.button("📁\n履歴", key="nav_hist", type="primary" if st.session_state.page == PAGE_HISTORY else "secondary", use_container_width=True):
#             if st.session_state.page != PAGE_HISTORY:
#                 st.session_state.page = PAGE_HISTORY
#                 st.rerun()
# --- Material Symbols を利用した下部ナビゲーション ---
# CSSでフッター固定設定が既にある場合は、ここをそのまま配置してください
with st.container(key="footer_nav"):
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

    # ページ定義（セッションの状態名と完全に一致させる）
    nav_config = [
        {"page": PAGE_RECIPE, "label": "", "icon": ":material/restaurant:"},
        {"page": PAGE_STOCK,  "label": "", "icon": ":material/kitchen:"},
        {"page": PAGE_FAVORITE, "label": "", "icon": ":material/bookmark_star:"},
        {"page": PAGE_HISTORY, "label": "", "icon": ":material/history:"}
    ]

    # ボタンの配置
    cols = [col_nav1, col_nav2, col_nav3, col_nav4]
    for i, config in enumerate(nav_config):
        with cols[i]:
            # 現在のページなら primary、それ以外なら secondary
            btn_type = "primary" if st.session_state.page == config["page"] else "secondary"
            
            if st.button(config["label"], icon=config["icon"], type=btn_type, use_container_width=True):
                if st.session_state.page != config["page"]:
                    st.session_state.page = config["page"]
                    st.rerun()
 