# views/history_view.py
import streamlit as st
from services.data_service import toggle_favorite, delete_favorite, prepare_recipe_for_cooking
from views.recipe_helpers import render_saved_recipe_detail
import streamlit.components.v1 as components

def reset_dialog_scroll():

    components.html("""

    <script>

    setTimeout(() => {

        // ダイアログ全体

        const dialog = document.querySelector('[data-testid="stDialog"]');
        if (dialog) {
            dialog.scrollTop = 0;
            // 内部スクロール領域を総当たりでリセット
            const scrollables = dialog.querySelectorAll('*');
            scrollables.forEach(el => {
                if (el.scrollHeight > el.clientHeight) {
                    el.scrollTop = 0;
                }
            });
        }
        // 保険
        window.scrollTo(0, 0);
    }, 80);
    </script>
    """, height=0)
# 元通りのシンプルなダイアログ構造に復活
@st.dialog(":material/kitchen: レシピ詳細")
def show_recipe_detail_dialog(recipe, mode, idx=None, is_fav=False):
    reset_dialog_scroll()

    # 詳細表示
    render_saved_recipe_detail(recipe, recipe.get("servings", 2), show_buttons=False)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 操作ボタン
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" 調理する", icon=":material/fork_spoon:", use_container_width=True):
            prepare_recipe_for_cooking(recipe)
            # 2. 【ここを追加】フッターナビのURL自動監視と連動させるため、URLのクエリを強制上書き
            from config.constants import PAGE_RECIPE
            st.session_state.page = PAGE_RECIPE

            st.query_params["page"] = PAGE_RECIPE
            # 3. セッションの現在地も合わせて同期
            st.session_state.page = PAGE_RECIPE
            
            # 4. 【ここを変更】アプリ全体（scope="app"）をリフレッシュして一気にジャンプさせる
            st.rerun()
            
    with col2:
        if mode == "favorite":
            if st.button("解除", icon=":material/bookmark_remove:", type="secondary", use_container_width=True):
                delete_favorite(idx)
                st.rerun()
        elif mode == "history":
            btn_label = "お気に入り解除" if is_fav else "お気に入り登録"
            btn_icon = ":material/bookmark_remove:" if is_fav else ":material/bookmark_add:"
            btn_type = "primary" if is_fav else "secondary"
            if st.button(btn_label, icon=btn_icon, type=btn_type, use_container_width=True):
                toggle_favorite(recipe)
                st.rerun()

def render_favorite_page():
    st.subheader(":material/menu_book_2: お気に入りレシピ")
    if not st.session_state.favorite_recipes:
        st.info("お気に入りに登録されたレシピはまだありません。")
        return

    for idx, recipe in enumerate(st.session_state.favorite_recipes):
        if st.button(f"{recipe['title']}", icon=":material/star:", key=f"fav_btn_{idx}", use_container_width=True):
            show_recipe_detail_dialog(recipe, mode="favorite", idx=idx)

def render_history_page():
    st.subheader(":material/history_edu: 過去の提案履歴")
    if not st.session_state.recipe_history:
        st.info("過去に提案されたレシピ履歴はありません。")
        return

    for idx, recipe in enumerate(st.session_state.recipe_history):
        recipe_id = recipe.get("id")
        is_fav = any(f.get("id") == recipe_id for f in st.session_state.favorite_recipes)
        
        label = f"{recipe['title']}"
        icon = ":material/star:" if is_fav else ":material/push_pin:"
        
        if st.button(label, icon=icon, key=f"hist_btn_{idx}", use_container_width=True):
            show_recipe_detail_dialog(recipe, mode="history", is_fav=is_fav)
