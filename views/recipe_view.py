# views/recipe_view.py
import streamlit as st
from config.constants import BASE_OPTIONS_FILE, FAVORITE_FILE
from utils import (
    save_json, load_json_cached
)
from services.ai_service import update_recipe_logic
from views.recipe_helpers import render_saved_recipe_detail

@st.dialog(":material/kitchen: 現在の冷蔵庫の中身")
def show_fridge_dialog(all_stock, seasonings_stock):
    # 日本語ラベルとアイコンの定義
    label_map = {
        "meat": ":material/yakitori: 肉類",
        "fish": ":material/set_meal: 魚介類",
        "vegetables": ":material/spa: 野菜類",
        "staple": ":material/washoku: 主食",
        "dairy": ":material/egg: 卵・乳製品・大豆製品"
    }

    # JSONからベース設定を読み込み
    data = load_json_cached(BASE_OPTIONS_FILE, {})

    # カテゴリごとに食材を表示
    for key, items_in_category in data.items():
        if key == "seasonings": continue  # 調味料は後で別途表示

        # 登録済みの食材リスト(all_stock)から、カテゴリに該当するものを抽出
        # 括弧書きがあってもマッチするように部分一致判定を使用
        found_items = [
            stock_item for stock_item in all_stock 
            if any(cat_item in stock_item for cat_item in items_in_category)
        ]
        
        if found_items:
            label = label_map.get(key, f":material/category: {key}")
            st.markdown(f"#### {label}")
            
            # チップ形式のスタイル（CSSを埋め込み）
            tags_html = (
                '<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;">' + 
                "".join([
                    f'<span style="background:#e8f4f8; padding:4px 10px; border-radius:12px; '
                    f'font-size:13px; border:1px solid #ddd; color:#444;">{item}</span>' 
                    for item in found_items
                ]) + 
                '</div>'
            )
            st.markdown(tags_html, unsafe_allow_html=True)


    st.markdown("#### :material/air_freshener: 調味料")
    if seasonings_stock:
        # スタイルを適用したコンテナを作成
        seasonings_html = (
            '<div style="background:#e8f4f8; padding:4px 10px; border-radius:8px; '
            'border: 1px solid #ddd; font-size:13px; color:#333; line-height:1.6;">' + 
            ", ".join(seasonings_stock) + 
            '</div>'
        )
        st.markdown(seasonings_html, unsafe_allow_html=True)
    else:
        st.write("なし")
    st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)
    
def render_recipe_page():
    st.subheader(":material/chef_hat: レシピ考案")
    all_stock_formatted = [
        f"{k}({v})"
        for cat in ["meat", "fish", "vegetables", "staple", "dairy"]
        for k, v in st.session_state["stock_data"][cat].items()
    ]
    seasonings_stock = list(st.session_state["stock_data"]["seasonings"].keys())

    if not all_stock_formatted:
        st.info(":material/shopping_cart: まずは下部メニューの「食材」ページから冷蔵庫の中身を登録してね！")
        return
    
    if st.button("登録している食材を確認", icon=":material/frame_inspect:", use_container_width=True):
        st.session_state.show_fridge = True
        st.rerun()

    if st.session_state.get("show_fridge", False):
        show_fridge_dialog(all_stock_formatted, seasonings_stock)
        st.session_state.show_fridge = False

    dish_types = ["おまかせ", "主菜（メイン）", "副菜（サイド）", "汁物・スープ"]
    selected_type = st.selectbox("何を作りたい？", dish_types)
    
    theme_options = ["おまかせ", "時短（15分以内）", "ガッツリ・満腹", "ヘルシー・低糖質", "おつまみ", "✏️ 自由記入"]
    selected_theme = st.selectbox("料理のテーマは？", theme_options)
    mood = st.text_input("具体的なテーマを入力", placeholder="例：子供が喜ぶメニュー") if selected_theme == "✏️ 自由記入" else selected_theme
    is_generated = st.session_state.get(
    "recipe_generated"
    )
    
    saved_type = st.session_state.get(
        "temp_dish_type",
        "おまかせ"
    )

    saved_mood = st.session_state.get(
        "temp_mood",
        "おまかせ"
    )
    # 料理タイプの表示判定
    display_type = (
        saved_type
        if is_generated and selected_type == saved_type
        else selected_type
    )
    # テーマの表示判定
    display_mood = (
        saved_mood
        if is_generated and mood == saved_mood
        else mood
     )

    st.markdown(f"""
        <div style="
            background-color: #e8f4fd; 
            padding: 10px; 
            border-radius: 5px; 
            border-left: 0px solid #2196f3;
            color: #0d47a1;
            font-size: 12px;
            margin-bottom: 15px;
        ">
            料理タイプ： <b>{display_type}</b>　|　テーマ： <b>{display_mood}</b>
        </div>
    """, unsafe_allow_html=True)
    st.slider(
        "何人分作りますか？", min_value=1, max_value=5, key="servings_input")
       # on_change=lambda: update_recipe_logic() if st.session_state.get("recipe_generated") else None
    
    if not st.session_state.get("recipe_generated"):
        if st.button("Let's cook !",  icon=":material/local_dining:",type="primary", use_container_width=True):
            st.session_state["temp_ingredients"] = ", ".join(all_stock_formatted)
            st.session_state["temp_seasonings"] = ", ".join(seasonings_stock) if seasonings_stock else "基本調味料のみ"
            st.session_state["temp_mood"] = mood
            st.session_state["temp_dish_type"] = selected_type
            update_recipe_logic()
            st.rerun()
    else:
        if st.button("別のレシピを提案", icon=":material/refresh:", use_container_width=True):
            st.session_state["temp_mood"] = mood
            st.session_state["temp_dish_type"] = selected_type
            st.session_state["recipe_generated"] = False
            st.session_state["current_recipe_obj"] = None
            
            update_recipe_logic(force_new=True)
            st.rerun()
    
    # st.slider(
    #     "何人分作りますか？", min_value=1, max_value=5, key=f"fav_title_{recipe['id']}", 
    #     on_change=lambda: update_recipe_logic() if st.session_state.get("recipe_generated") else None
    # )

    recipe = st.session_state.get("current_recipe_obj")
    st.write("現在人数:", st.session_state["servings_input"])
st.write("保存人数:", recipe.get("servings"))
    if recipe:
        st.write("---")
        st.subheader(":material/menu_book: レシピ・工程")
        with st.container(border=True):
            render_saved_recipe_detail(recipe, st.session_state["servings_input"])
        
        col_fav_left, col_fav_right = st.columns([4, 2], vertical_alignment="bottom")
        recipe_title_input = col_fav_left.text_input("お気に入り登録時の保存名", value=recipe["title"], key=f"fav_title_{recipe['id']}")
        if col_fav_right.button("お気に入り登録", icon=":material/bookmark_add:", use_container_width=True):
            if not any(f.get("id") == recipe["id"] for f in st.session_state.favorite_recipes):
                new_fav = dict(recipe)
                new_fav["title"] = recipe_title_input
                st.session_state.favorite_recipes.insert(0, new_fav)
                save_json(FAVORITE_FILE, st.session_state.favorite_recipes)
                st.toast("登録しました！")
            else:
                st.warning("登録済みです。")
