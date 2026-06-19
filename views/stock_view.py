# views/stock_view.py
import streamlit as st
import re
from config.constants import INGREDIENTS_FILE, BASE_OPTIONS_FILE
from utils import save_json

# 単位リスト定義
UNIT_LIST = ["個", "g", "ml", "枚",  "本", "束", "パック", "丁", "片", "適量"]

@st.fragment
def render_stock_page_fragment():
    # CSSのカスタマイズ（タブの文字サイズ調整）
    st.markdown("""
        <style>
        button[data-baseweb="tab"] div p { 
            font-size: 18px !important; 
            font-weight: bold; 
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader(":material/briefcase_meal: 食材管理")
    st.caption("冷蔵庫にある食材をタップして登録・数量を調整できます。")
    

    # タブ設定
    #tabs = st.tabs(["🥩 肉類", "🐟 魚介類", "🥬 野菜類", "🍚 主食", "🥛 卵・乳製品・豆類", "🧂 調味料"])
    tabs = st.tabs([
    ":material/yakitori: 肉類", 
    ":material/set_meal: 魚介類", 
    ":material/spa: 野菜類", 
    ":material/washoku: 主食", 
    ":material/egg: 卵・乳製品・豆類", 
    ":material/air_freshener: 調味料"
    ])
    categories = ["meat", "fish", "vegetables", "staple", "dairy", "seasonings"]
    labels = ["肉類", "魚介類", "野菜類", "主食", "卵・乳製品・豆類", "調味料"]

    needs_save = False

    for tab, cat, label in zip(tabs, categories, labels):
        with tab:
            options = sorted(list(set(st.session_state["base_options"][cat])))
            current_stock = st.session_state["stock_data"][cat]
            default_selected = [item for item in options if item in current_stock]

            st.write("### :material/grocery: 食材一覧（タップで選択）")
            selected_items = st.pills("選択", options, default=default_selected, selection_mode="multi", key=f"pills_{cat}", label_visibility="collapsed") or []

            # 数量調整ロジック
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
                                    current_index = UNIT_LIST.index(init_unit) if init_unit in UNIT_LIST else 0
                                    unit = c_unit.selectbox("単", UNIT_LIST, index=current_index, key=f"u_{cat}_{item}", label_visibility="collapsed")

                                    if amt > 0:
                                        updated_stock[item] = f"{amt}{unit}"
                else:
                    # 調味料は選択されているだけでOK
                    updated_stock = {item: current_stock.get(item, "1.0個") for item in selected_items}
            
            # 変更の反映
            if st.session_state["stock_data"][cat] != updated_stock:
                st.session_state["stock_data"][cat] = updated_stock
                needs_save = True

            ## 新規追加フォーム
            st.write("---")
            with st.form(key=f"form_{cat}", clear_on_submit=True):
                col_input, col_btn = st.columns([4, 1])
                new_items_str = col_input.text_input(f"{label}の新規追加", placeholder="スペース区切りで複数追加可能", label_visibility="collapsed")
                if col_btn.form_submit_button("追加", icon=":material/add:"):# and new_items_str:
                    # 【ここを修正】re.splitで、空白文字(全角半角含む)とカンマで分割
                    items = re.split(r'[\s、,]+', new_items_str.strip())
                    
                    for item in items:
                        if item.strip(): # 空白でない場合のみ処理
                            item_strip = item.strip()
                            if item_strip not in st.session_state["base_options"][cat]:
                                st.session_state["base_options"][cat].append(item_strip)
                            st.session_state["stock_data"][cat][item_strip] = "1.0個"
                    
                    save_json(BASE_OPTIONS_FILE, st.session_state["base_options"])
                    needs_save = True
                    st.rerun()

            # マスター削除機能
            with st.expander(":material/settings: マスターから完全に削除する"):
                delete_targets = st.multiselect("削除する項目を選択", options=options, key=f"del_sel_{cat}")
                if st.button("選択した項目を完全削除", icon=":material/delete:", key=f"del_btn_{cat}", type="primary"):
                    if delete_targets:
                        st.session_state["base_options"][cat] = [x for x in st.session_state["base_options"][cat] if x not in delete_targets]
                        st.session_state["stock_data"][cat] = {k: v for k, v in st.session_state["stock_data"][cat].items() if k not in delete_targets}
                        save_json(BASE_OPTIONS_FILE, st.session_state["base_options"])
                        needs_save = True
                        st.success("削除しました！")
                        st.rerun()

    if needs_save:
        save_json(INGREDIENTS_FILE, st.session_state["stock_data"])
