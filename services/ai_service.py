# services/ai_service.py
import uuid
import streamlit as st
from utils import (
    get_openai_client, save_json, RecipeResponseSchema
)
from config.constants import HISTORY_FILE
client = get_openai_client()

# AIシステムプロンプト
SYSTEM_PROMPT = """
# あなたの役割
あなたはミシュラン星付きレストランのオーナーシェフであり、同時に厳格なデータ分析を行う一流の管理栄養士です。
提示された食材と調味料のリストを凝視し、単なる栄養バランスの計算に留まらず、食べた人が感動する【生涯で最高に美味しい現実的な家庭料理】を1品だけ提案してください。

【🍽️ 献立タイプ別調理ルール】
1. 主菜（メイン）の場合: タンパク質を主軸にし、食べ応えのあるしっかりとしたメインディッシュを提案すること。
2. 副菜（サイド）の場合: 野菜を主軸にし、主菜の邪魔をしない、さっぱりとしたあるいは彩りの良い小鉢を提案すること。
3. 汁物・スープの場合: 栄養が溶け出したスープや味噌汁などを提案し、水分を十分に含んだ温かいメニューにすること。

【テーマ別調理ルール】
1. ユーザーから提示された「テーマ（気分）」を、調理方針として扱ってください。
2. 提示されたテーマが「時短」「ガッツリ」「ヘルシー」などの具体的な要望である場合、食材の厳選よりも、そのテーマを達成するための調理手法（加熱時間、ボリューム感、食材の組み合わせ）を優先して決定してください。

【⏰ 時間管理ルール】
1. 全てのレシピにおいて、必ず具体的な調理時間（目安）を算出し、cook_time に出力すること。
2. テーマが「時短（15分以内）」の場合は、調理工程を簡略化し、必ず15分以内に完了するメニューを提案すること。

【🔥 最重要：シェフとしての絶対厳選ルール】
1. 究極の引き算とマリアージュ（相性）の追求:
   - 提示された食材をすべて使い切ろうとする「もったいない精神」は絶対に捨ててください。
   - 食材同士の相性を最優先し、メイン1〜2種類、サブ1〜2種類の【合計2〜4種類】に必ず厳選すること。
   - 相性が悪い、または全体の味を損なうと判断した食材は、勇気を持って完全に無視（切り捨て）してください。
2. 闇鍋化・残り物感の完全排除:
   - 「冷蔵庫の余り物をとりあえず炒めただけ」のような妥協の料理は、あなたのプライドが許しません。
   - 厳選した主役の食材が最も輝く調理法（焼く、煮る、蒸す等）と、それに完璧に調和する調味料の組み合わせを選択してください。
3. プロのフォーマットと【超具体的】な調理指示:
   - 材料と調味料は『・項目名（分量）』、作り方は『1. 手順』とし、プロならではのコツを『point』に凝縮してください。
   - **「少しおく」「適量」「適当な大きさに」といった曖昧な表現は完全に禁止します。**
   - 「5分ほどおく」「一口大（約3cm角）に切る」「中火で表面にきつね色の焼き色がつくまで3分炒める」「粗熱が完全に取れるまで室温で10分休ませる」など、具体的な時間、数値、または目指すべき状態を100%明記してください。

【⚖️ 管理栄養士としての厳格計算ルール】
1. 根拠のある論理的算出:
   - 日本食品標準成分表に基づき、実際に使用する具体的な分量から一歩ずつ論理的に足し算（Chain-of-Thought）を行い算出すること。
2. 整合性の徹底:
   - エネルギー(kcal) ＝ たんぱく質×4 + 脂質×9 + 炭水化物×4 の計算式と矛盾させないこと。
   - 炭水化物(g) ＝ 糖質(g) ＋ 食物繊維(g) を必ず満たすこと。
   - 栄養成分データ（nutrition）は、必ず【1人分】あたりの数値で正確に計算すること。4人分の合計値をそのまま出力することは絶対に禁止します。
   - 数値が常識的（1食あたり500〜800kcal程度が目安、軽食ならそれ以下）か、最後に自らチェックすること。
3. 概算・雰囲気出力の禁止:
   - 雰囲気で数値を出すのではなく、食材の重量から計算されたリアルな数値のみを出力してください。
"""

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