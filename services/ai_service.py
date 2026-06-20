# services/ai_service.py
import uuid
import streamlit as st
from utils import (
    get_openai_client, save_json, RecipeResponseSchema
)
from config.constants import HISTORY_FILE
from config.prompts import SYSTEM_PROMPT
def update_recipe_logic(
    force_new=False,
    current_mood=None
):

    client = get_openai_client()

    recipe = (
        None
        if force_new
        else st.session_state.get(
            "current_recipe_obj"
        )
    )

def update_recipe_logic(force_new=False, current_mood=None):
    recipe = None if force_new else st.session_state.get("current_recipe_obj")
    new_servings = st.session_state["servings_input"]
    
    if recipe:
        user_content = f"前回提案した『{recipe['title']}』をベースに、必ず【{new_servings}人分】に合わせて分量を再計算してください。\n【前回の材料】: {recipe['ingredients']}\nルール：材料の追加や代替は禁止。"
    else:
        ingredients_text = st.session_state.get("temp_ingredients", "おまかせ")
        seasonings_text = st.session_state.get("temp_seasonings", "基本調味料のみ")
        mood = current_mood or st.session_state.get("temp_mood", "おまかせ")
        dish_type = st.session_state.get("temp_dish_type", "おまかせ")
        user_content = f"""
    【目標】: 提供されたテーマを達成する献立を提案すること。
    【タイプ】: {dish_type}
    【テーマ】: {mood}
    【食材】: {ingredients_text}
    【調味料】: {seasonings_text}
    【人数】: {new_servings}人分
    """

    try:
        with st.spinner(":material/skillet::material/smart_toy: Testing Recipes . . ."):
            response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_content}],
                response_format=RecipeResponseSchema,
            )
            recipe_data = response.choices[0].message.parsed
    except Exception as e:
        st.error(f"⚠️ AIとの通信に失敗しました。({str(e)})")
        return

    new_recipe = {
        "id": recipe["id"] if recipe else str(uuid.uuid4()),
        "title": recipe_data.title,
        "cook_time": recipe_data.cook_time,
        "servings": new_servings,
        "ingredients": recipe_data.ingredients,
        "seasonings": recipe_data.seasonings,
        "instructions": recipe_data.instructions,
        "point": recipe_data.point,
        "nutrition": recipe_data.nutrition.model_dump(),
    }
    
    st.session_state["current_recipe_obj"] = new_recipe
    st.session_state["recipe_generated"] = True
    
    existing_idx = next((i for i, r in enumerate(st.session_state.recipe_history) if r["id"] == new_recipe["id"]), None)
    if existing_idx is not None:
        st.session_state.recipe_history[existing_idx] = new_recipe
    else:
        st.session_state.recipe_history.insert(0, new_recipe)
        
    st.session_state.recipe_history = st.session_state.recipe_history[:50]
    save_json(HISTORY_FILE, st.session_state.recipe_history)
