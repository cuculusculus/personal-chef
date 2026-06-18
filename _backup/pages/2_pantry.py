#2_pantry.py
import streamlit as st
import re
from utils import save_json, INGREDIENTS_FILE, BASE_OPTIONS_FILE

st.title("🛒 持っている食材の管理")
st.caption("ボタンをタップして選択（色付き）にすると、冷蔵庫に登録されます。数量もその場で設定可能です。")

st.markdown("""<style>button[data-baseweb="tab"] div p { font-size: 18px !important; font-weight: bold; }</style>""", unsafe_allow_html=True)
tabs = st.tabs(["🥩 肉類", "🐟 魚類", "🥬 野菜類", "🥛 卵・乳製品・豆類", "🧂 調味料"])
categories = ["meat", "fish", "vegetables", "dairy", "seasonings"]
labels = ["肉類", "魚類", "野菜類", "卵・乳製品・豆類", "調味料"]

for tab, cat, label in zip(tabs, categories, labels):
    with tab:
        options = sorted(list(set(st.session_state["base_options"][cat])))
        current_stock = st.session_state["stock_data"][cat]
        default_selected = [item for item in options if item in current_stock]

        st.write("### 🍱 食材一覧（タップで選択）")
        selected_items = st.pills("選択された食材", options, default=default_selected, selection_mode="multi", key=f"pills_{cat}", label_visibility="collapsed") or []

        updated_stock = {}
        if selected_items:
            if cat != "seasonings":
                st.write("▼ 選択中食材の数量調整")
                for i in range(0, len(selected_items), 2):
                    cols = st.columns(2)
                    for j, item in enumerate(selected_items[i:i+2]):
                        with cols[j]:
                            with st.container(border=True):
                                saved_val = current_stock.get(item, "1.0個")
                                match_num = re.findall(r"[-+]?\d*\.\d+|\d+", saved_val)
                                init_amt = float(match_num[0]) if match_num else 1.0
                                init_unit = saved_val.replace(str(init_amt), "").strip() or "個"
                                
                                c_name, c_amt, c_unit = st.columns([4, 3, 3])
                                c_name.markdown(f"<div style='padding-top:8px;'><b>{item}</b></div>", unsafe_allow_html=True)
                                amt = c_amt.number_input("数", min_value=0.0, value=init_amt, step=0.5, key=f"n_{cat}_{item}", label_visibility="collapsed")
                                unit = c_unit.selectbox("単", ["個", "g", "枚", "パック", "本", "適量"], index=["個", "g", "枚", "パック", "本", "適量"].index(init_unit) if init_unit in ["個", "g", "枚", "パック", "本", "適量"] else 0, key=f"u_{cat}_{item}", label_visibility="collapsed")
                                if amt > 0:
                                    updated_stock[item] = f"{amt}{unit}"
            else:
                updated_stock = {item: "1.0個" for item in selected_items}

        # 新規追加フォーム
        st.write("---")
        with st.form(key=f"form_{cat}", clear_on_submit=True):
            col_input, col_btn = st.columns([4, 1])
            new_items_str = col_input.text_input(f"{label}の新規追加", placeholder="スペース区切りで複数追加可能", label_visibility="collapsed")
            if col_btn.form_submit_button("➕追加") and new_items_str:
                for item in new_items_str.replace(" ", " ").split(" "):
                    if item.strip():
                        if item.strip() not in st.session_state["base_options"][cat]:
                            st.session_state["base_options"][cat].append(item.strip())
                        updated_stock[item.strip()] = "1.0個"
                save_json(BASE_OPTIONS_FILE, st.session_state["base_options"])
                st.session_state["stock_data"][cat] = updated_stock
                save_json(INGREDIENTS_FILE, st.session_state["stock_data"])
                st.rerun()

        st.session_state["stock_data"][cat] = updated_stock

# 最終的な在庫の保存
save_json(INGREDIENTS_FILE, st.session_state["stock_data"])