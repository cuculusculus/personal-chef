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

/* ---------- 【決定版】ダイアログの位置を最上部に強制固定 ---------- */
/* 
   Streamlitの独自コンテナに邪魔されないよう、HTMLの「dialog」要素そのものを直撃。
   画面中央への配置（margin: auto）を完全に上書きし、上端（margin-top: 15px）に強制固定します。
*/
dialog,
div[role="dialog"],
[data-testid="stModal"] {
    margin: 15px auto auto auto !important; /* 上の余白だけを15pxにして、左右は中央、下は自動にします */
    top: 15px !important;
    align-self: flex-start !important;      /* 親のFlexboxに対しても上寄せを強制 */
}

/* 
   ダイアログを包む最外層の黒い背景（stModalContainer）に対しても、
   中央配置を無効化して上端スタート（flex-start）に設定します。
*/
[data-testid="stModalContainer"],
div[class*="StyledModalContainer"] {
    align-items: flex-start !important;
    padding-top: 15px !important;
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
