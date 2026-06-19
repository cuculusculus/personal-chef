import re
import streamlit as st

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
                :material/wheat: 炭水化物 {carbo:.1f} g<span style='font-size: 0.7rem; color: #666;'>(糖質 {s:.1f}g (糖類 {st_val:.1f}g) + 食物繊維 {fi:.1f}g)</span><br>
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
    
    st.markdown(f"#### :material/skillet: 作り方")
    st.markdown(steps_html, unsafe_allow_html=True)

    point_part = recipe.get("point", "")
    if point_part:
        st.markdown(f"""
            <div style='background-color:#fffde7; border-left:5px solid #fbc02d; padding:12px; border-radius:4px; margin-top:16px; margin-bottom: 8px; font-size:0.8rem;'>
                <strong>💡 Quick Tips</strong><br>{point_part}
            </div>
        """, unsafe_allow_html=True)

    return
