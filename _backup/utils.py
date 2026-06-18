# utils.py
import json
import re
from openai import OpenAI
import streamlit as st
from pydantic import BaseModel, Field

# --- ファイルパス ---
HISTORY_FILE = "recipe_history.json"
FAVORITE_FILE = "favorite_recipes.json"
INGREDIENTS_FILE = "my_ingredients.json"
BASE_OPTIONS_FILE = "base_options.json"

# --- Schema ---
class NutritionSchema(BaseModel):
    energy: float
    protein: float
    fat: float
    sugar: float
    sugar_type: float
    fiber: float
    salt: float

class RecipeResponseSchema(BaseModel):
    title: str
    cook_time: str
    ingredients: str
    seasonings: str
    instructions: str
    point: str
    nutrition: NutritionSchema

# --- 🚀 高速化関数 ---
@st.cache_data
def load_json_cached(filepath, default):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    st.cache_data.clear()

@st.cache_resource
def get_openai_client():
    api_key = st.secrets["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)

# --- ダイアログ ---
@st.dialog(":material/kitchen: 現在の冷蔵庫の中身")
def show_fridge_dialog(all_stock, seasonings_stock):
    st.markdown("#### :material/grocery: 材料")
    st.info(", ".join(all_stock))
    st.markdown("#### :material/air_freshener: 調味料")
    st.info(", ".join(seasonings_stock) if seasonings_stock else "なし")
    if st.button("閉じる", use_container_width=True):
        st.rerun()

# --- レシピ描画関数 ---
def render_saved_recipe_detail(recipe, servings, show_buttons=False):
    if "body" in recipe and not any(k in recipe for k in ["ingredients", "instructions"]):
        st.warning("⚠️ 旧形式の保存データです。")
        return

    # --- 1. パース処理 ---
    title = recipe.get("title", "無題のレシピ")
    cook_time = recipe.get("cook_time", "—")
    
    ing_parts = re.split(r'[\n、,・]', recipe.get("ingredients", ""))
    ing_html = "<ul>" + "".join([f"<li>{i.strip()}</li>" for i in ing_parts if i.strip()]) + "</ul>"
    
    sea_parts = re.split(r'[\n、,・]', recipe.get("seasonings", "基本調味料"))
    sea_html = "<ul>" + "".join([f"<li>{s.strip()}</li>" for s in sea_parts if s.strip()]) + "</ul>"

    # 栄養成分パース
    nut = recipe.get("nutrition", {})
    if isinstance(nut, dict) and nut:
        e = nut.get('energy', 0)
        p = nut.get('protein', 0)
        f = nut.get('fat', 0)
        s = nut.get('sugar', 0)
        st_val = nut.get('sugar_type', 0)
        fi = nut.get('fiber', 0)
        salt = nut.get('salt', 0)
        carbo = s + fi
        
        # HTMLとして確実にレンダリングさせるため、改行を <br> に統一
        nut_content = f"""
:material/mode_heat: エネルギー {e:.1f} kcal<br>
:material/egg: たんぱく質 {p:.1f} g<br>
:material/water_drop: 脂質 {f:.1f} g<br>
:material/wheat: 炭水化物 {carbo:.1f} g <span style='font-size: 0.75rem; color: #666;'>(糖質 {s:.1f}g (糖類 {st_val:.1f}g) + 食物繊維 {fi:.1f}g)</span><br>
:material/salinity: 食塩相当量 {salt:.1f} g
"""
    else:
        nut_content = "<div style='padding:10px; border:1px solid #ddd;'>栄養成分データなし</div>"

    # 作り方パース（確実にリストとして表示させる）
    raw_instructions = recipe.get("instructions", "手順データなし")
    lines = str(raw_instructions).split('\n')
    
    steps = []
    for line in lines:
        # 数字や記号を削除
        clean_step = re.sub(r'^[0-9０-９]+[.\.．、,，\s\-─:：)）\]］>＞]*|^[①-⑨]\s*', '', line).strip()
        if clean_step:
            steps.append(clean_step)
            
    # 各行を明示的に <li> と改行で構成する
    steps_html = "<ol style='padding-left: 0px; margin: 0;'>" + \
                 "".join([f"<li style='margin-bottom: 8px; display: list-item;'>{s}</li>" for s in steps]) + \
                 "</ol>"
    # --- 2. レンダリング ---
    st.subheader(f":material/restaurant: {title}")
    st.markdown(f"##### :material/timer: 調理時間の目安: {cook_time}")
    st.markdown("---")
    
    st.markdown(f"#### :material/shopping_cart: 食材 ({servings}人分)")
    st.markdown(ing_html, unsafe_allow_html=True)
    
    st.markdown(f"#### :material/air_freshener: 調味料")
    st.markdown(sea_html, unsafe_allow_html=True)
    
    st.markdown(f"#### :material/bar_chart_4_bars: 栄養成分目安 (1人分)")
    # 【重要】ここで unsafe_allow_html=True を指定することで span タグが有効になります
    st.markdown(nut_content, unsafe_allow_html=True)
    
    st.markdown(f"#### :material/dining: 作り方")
    st.markdown(steps_html, unsafe_allow_html=True)

    point_part = recipe.get("point", "")
    if point_part:
        st.markdown(f"""
            <div style='background-color:#fffde7; border-left:5px solid #fbc02d; padding:12px; border-radius:4px; margin-top:16px; margin-bottom: 8px; font-size:0.8rem;'>
                <strong>💡 Quick Tips</strong><br>{point_part}
            </div>
        """, unsafe_allow_html=True)

    # --- 3. 最下部のボタン配置 ---
    # cook_clicked = False
    # action_clicked = False
    
    # if show_buttons:
    #     st.markdown("<hr style='margin: 16px 0 12px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
        
    #     # スマホ画面幅いっぱいに2つのボタンを横並び（50%ずつ）で配置
    #     col_btn1, col_btn2 = st.columns([1, 1])
        
    #     unique_id = recipe.get("id", recipe_idx)
    #     with col_btn1:
    #         if st.button("🍳 調理する", key=f"btn_cook_{page_id}_{unique_id}", use_container_width=True):
    #             cook_clicked = True
    #     with col_btn2:
    #         if st.button(btn2_label, key=f"btn_act_{page_id}_{unique_id}", use_container_width=True):
    #             action_clicked = True

    # return cook_clicked, action_clicked
    return

# --- 🚀 高速化3: キャッシュされた 究極CSS ---
@st.cache_data
def get_app_css():
    """アプリ全体のアプリ化・固定ナビCSSを生成する関数"""
    return """
<style>
    
    [data-testid="stSidebar"], 
    [data-testid="stSidebarCollapsedControl"], 
    header, footer, #MainMenu, .stDeployButton, [data-testid="stToolbar"], div[data-testid="stDecoration"] {
        display: none !important;
    }

    .block-container {
        padding-top: 0.2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 110px !important; 
        max-width: 100% !important;
    }

    div.st-key-footer_nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 75px !important;
        background-color: #ffffff !important;
        border-top: 1px solid #e0e0e0 !important;
        z-index: 999999 !important;
        padding: 10px !important;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.05) !important;
    }
    

    div.st-key-footer_nav [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: 25% !important;
        padding: 0 4px !important;
    }

    div.st-key-footer_nav button {
        height: 55px !important;
        white-space: pre-line !important;
        line-height: 1.3 !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* ボタン内Markdown文字対策 */
    div.st-key-footer_nav button div[data-testid="stMarkdownContainer"] {
        font-size: 14px !important;
    }

    div.st-key-footer_nav button div[data-testid="stMarkdownContainer"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    * {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    /* アイコンが大きくなった分、行全体の高さを確保 */
    .main-scroll-area p {
        line-height: 1.6 !important;
    }
    
    /* ボタン内のアイコンサイズ */
    div.st-key-footer_nav button span {
    font-size: 36px !important;
    }
    /* ボタン内の文字サイズ */
    div.st-key-footer_nav button p {
        font-size: 12px !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }
</style>
"""

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