# views/recipe_view.py
import streamlit as st
from utils import (
    render_saved_recipe_detail, save_json, show_fridge_dialog, FAVORITE_FILE
)
from services.ai_service import update_recipe_logic

def render_recipe_page():
    st.title("👩‍🍳 レシピ考案")
    
    all_stock_formatted = []
    for cat in ["meat", "fish", "vegetables", "dairy"]:
        for k, v in st.session_state["stock_data"][cat].items():
            all_stock_formatted.append(f"{k}({v})")
    seasonings_stock = list(st.session_state["stock_data"]["seasonings"].keys())

    if not all_stock_formatted:
        st.info("💡 まずは下部メニューの「🛒 食材」ページから冷蔵庫の中身を登録してね！")
        return

    if st.button("🧊 登録している食材を確認", use_container_width=True):
        st.session_state.show_fridge = True
        st.rerun()

    if st.session_state.get("show_fridge", False):
        show_fridge_dialog(all_stock_formatted, seasonings_stock)
        st.session_state.show_fridge = False

    dish_types = ["おまかせ", "主菜（メイン）", "副菜（サイド）", "汁物・スープ"]
    selected_type = st.selectbox("何を作りたい？", dish_types)
    
    theme_options = ["おまかせ", "時短（15分以内）", "ガッツリ・満腹", "ヘルシー・低糖質", "おつまみ", "✏️ 自由記入"]
    selected_theme = st.selectbox("今日の料理のテーマは？", theme_options)
    mood = st.text_input("具体的なテーマを入力", placeholder="例：子供が喜ぶメニュー") if selected_theme == "✏️ 自由記入" else selected_theme
    current_ui_type = selected_type  # 今まさに選んでいるもの
    saved_type = st.session_state.get("temp_dish_type", "おまかせ")
    if st.session_state.get("recipe_generated") and current_ui_type == saved_type:
        display_type = saved_type
    else:
        display_type = current_ui_type
    current_ui_mood = mood
    saved_mood = st.session_state.get("temp_mood", "おまかせ")
    
    if st.session_state.get("recipe_generated") and current_ui_mood == saved_mood:
        display_mood = saved_mood
    else:
        display_mood = current_ui_mood
    
    is_generated = st.session_state.get("recipe_generated")
    
    # 料理タイプの表示判定
    if is_generated and current_ui_type == saved_type:
        display_type = saved_type
    else:
        display_type = current_ui_type
        
    # テーマの表示判定
    if is_generated and current_ui_mood == saved_mood:
        display_mood = saved_mood
    else:
        display_mood = current_ui_mood
    #st.info(f"料理タイプ: **{display_type}** | テーマ: **{display_mood}**")
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
    if not st.session_state.get("recipe_generated"):
        if st.button("✨ 献立をリクエスト！", type="primary", use_container_width=True):
            st.session_state["temp_ingredients"] = ", ".join(all_stock_formatted)
            st.session_state["temp_seasonings"] = ", ".join(seasonings_stock) if seasonings_stock else "基本調味料のみ"
            st.session_state["temp_mood"] = mood
            st.session_state["temp_dish_type"] = selected_type
            update_recipe_logic()
            st.rerun()
    else:
        if st.button("🔄 別のレシピを提案してもらう", use_container_width=True):
            st.session_state["temp_mood"] = mood
            st.session_state["temp_dish_type"] = selected_type
            st.session_state["recipe_generated"] = False
            st.session_state["current_recipe_obj"] = None
            update_recipe_logic(force_new=True)
            st.rerun()
    
    st.slider(
        "何人分作りますか？", min_value=1, max_value=5, key="servings_input", 
        on_change=lambda: update_recipe_logic() if st.session_state.get("recipe_generated") else None
    )

    recipe = st.session_state.get("current_recipe_obj")
    if recipe:
        st.write("---")
        st.subheader("📝 レシピ・工程")
        with st.container(border=True):
            render_saved_recipe_detail(recipe, st.session_state["servings_input"], show_buttons=False)
        
        col_fav_left, col_fav_right = st.columns([4, 2], vertical_alignment="bottom")
        recipe_title_input = col_fav_left.text_input("お気に入り登録時の保存名", value=recipe["title"], key="fav_title_input")
        if col_fav_right.button("⭐ お気に入りに登録", use_container_width=True):
            if not any(f.get("id") == recipe["id"] for f in st.session_state.favorite_recipes):
                new_fav = dict(recipe)
                new_fav["title"] = recipe_title_input
                st.session_state.favorite_recipes.insert(0, new_fav)
                save_json(FAVORITE_FILE, st.session_state.favorite_recipes)
                st.toast("登録しました！")
            else:
                st.warning("登録済みです。")