# config/styles.py
import streamlit as st

APP_CSS = """
<style>

/* ---------- Streamlit標準UI非表示 ---------- */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
header,
footer,
#MainMenu,
.stDeployButton,
[data-testid="stToolbar"],
div[data-testid="stDecoration"],
[data-testid="stAppHeader"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
}

/* ---------- アプリ全体レイアウト ---------- */
[data-testid="stMainBlockContainer"],
.main .block-container {
    padding-top: 0px !important;
    margin-top: 0px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 160px !important; /* フッターを避ける余白 */
    max-width: 100% !important;
}

.stApp {
    padding-top: 0px !important;
    padding-bottom: 100px;
}

/* ---------- 【決定版】下部メニューのスマホ横並び＆バッジ回避固定 ---------- */

/* 
   1. あなたの指定してくれた key="footer_nav" を起点にして、
      Streamlitの親ラッパーごと最下部から45px上の位置に強制固定（Sticky）します。
*/
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[id="footer_nav"]) {
    position: fixed !important;
    bottom: 45px !important; /* スマホのバッジを完璧に避けて上に浮かせる */
    left: 0 !important;
    width: 100% !important;
    height: 70px !important;
    background-color: #ffffff !important;
    border-top: 1px solid #e0e0e0 !important;
    border-bottom: 1px solid #e0e0e0 !important;
    z-index: 999999 !important;
    padding: 10px 16px !important;
    box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.08) !important;
}

/* 
   2. スマホ表示になった瞬間に st.columns が縦4つに積み上がってしまうStreamlitの初期設定を、
      CSSのFlexbox（横並び・折り返し禁止）で強力に上書きして阻止します。
*/
div[id="footer_nav"] div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    width: 100% !important;
    gap: 6px !important;
}

/* 
   3. 4つのカラムそれぞれの横幅を、スマホ画面でも「絶対に25%（4等分）」に維持します。
*/
div[id="footer_nav"] div[data-testid="column"] {
    width: 25% !important;
    flex: 1 1 25% !important;
    min-width: 0 !important;
}

/* 
   4. st.buttonの箱をタップしやすい大きなサイズに最適化します。
*/
div[id="footer_nav"] button {
    height: 50px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ボタン内のマテリアルアイコンのサイズをスマホに最適化 */
div[id="footer_nav"] button [data-testid="stIconMaterial"] {
    font-size: 26px !important;
}

/* ---------- 共通設定 ---------- */
.main .block-container p, 
.main .block-container div {
    word-wrap: break-word;
    overflow-wrap: break-word;
}

</style>
"""

def apply_styles():
    st.markdown("""
<link rel="stylesheet"
href="https://googleapis.com" />
""", unsafe_allow_html=True)
    st.html(APP_CSS)
