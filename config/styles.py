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
    padding-bottom: 160px !important;
    max-width: 100% !important;
}

.stApp {
    padding-top: 0px !important;
    padding-bottom: 100px;
}

/* ---------- 【新設】ダイアログの位置を最上部に強制固定 ---------- */
/* 
   最新のStreamlitダイアログを包む「最外層の黒い背景レイヤー（stModalContainer）」を直撃。
   画面中央に浮かすデフォルト設定を破壊し、上端（flex-start）へ強制的に引っ張り上げます。
*/
[data-testid="stModalContainer"],
div[class*="StyledModalContainer"] {
    align-items: flex-start !important; /* 中央ではなく、画面の上端から配置する */
    padding-top: 10px !important;       /* 画面の上端にピタッとくっつける（好みに応じて10px〜20px） */
}

/* ダイアログの「白い箱（stModal）」自体の位置と高さを最適化 */
[data-testid="stModal"],
div[class*="StyledModal"] {
    margin-top: 0px !important;
    top: 0px !important;
    max-height: 80vh !important;       /* スマホのフッターナビを隠さない絶妙な高さに制限 */
    overflow-y: auto !important;       /* 中身が長い場合は箱の中だけでスクロールさせる */
}

/* ---------- タイトル・見出しの画面サイズ最適化 ---------- */
.main .block-container [data-testid="stHeadingWithIcon"],
.main .block-container [data-testid="stHeaderBlockContainer"],
.main .block-container [data-testid="element-container"]:has(h1, h2, h3) {
    max-width: 100% !important;
    width: 100% !important;
    min-width: 0 !important;
    overflow: hidden !important;
}

.main .block-container h1,
.main .block-container h1 span,
.main .block-container [data-testid="stHeadingWithIcon"] h1 p {
    font-size: max(1.2rem, 5.2vw) !important;
    line-height: 1.2 !important;
}

/* ---------- フッターボタン内の調整 ---------- */
div[id="fixed_footer_root"] + div button {
    height: 52px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center;
}

div[id="fixed_footer_root"] + div button [data-testid="stIconMaterial"] {
    font-size: 28px !important;
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
