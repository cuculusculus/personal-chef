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
div[data-testid="stDecoration"] {
    display: none !important;
}

/* 
   【最重要】スマホ右下の「Manage app」バッジを強制非表示 
   アプリの外側に配置されているバッジ要素を、最高レベルの優先度で上書き・消去します。
*/
iframe[title="Manage app"],
div[class*="viewerBadge"],
div[class*="manageApp"],
.stViewerBadge,
div[data-testid="stStatusWidget"],
#tabs-bnd-tab-container + div,
div[style*="position: fixed"][style*="bottom:"] {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    pointer-events: none !important;
    z-index: -999999 !important;
}

/* ---------- アプリ全体レイアウト ---------- */

.main .block-container {
    padding-top: 0.2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 160px !important; /* フッターにコンテンツが隠れないように下部に余白を確保 */
    max-width: 100% !important;
}

.stApp {
    padding-bottom: 100px;
}
/* ---------- 【修正】タイトル・見出しの折り返し防止 ---------- */

/* 
   .main .block-container を起点にし、さらに内部のテキスト要素（spanやp、h1）まで
   すべて強制指定することで、Streamlit本来の自動改行ルールを完全に破壊して上書きします。
*/
.main .block-container h1,
.main .block-container h2,
.main .block-container h3,
.main .block-container h1 span,
.main .block-container h2 span,
.main .block-container h3 span,
.main .block-container [data-testid="stHeaderBlockContainer"] {
    white-space: nowrap !important;     /* 絶対に改行させない */
    word-break: keep-all !important;    /* 単語の途中での改行も禁止 */
    overflow: hidden !important;        /* はみ出た部分は隠す */
    text-overflow: ellipsis !important; /* 末尾を「...」にする */
    display: block !important;          /* インラインからブロック要素に変えて ellipsis を有効化 */
    
    /* スマホ画面用にサイズをコンパクトにする（h1基準） */
    font-size: max(1.4rem, 5.5vw) !important; 
}

/* ついでにタイトル下部の余計な余白も削ってスマホ画面を広くします */
.main .block-container [data-testid="element-container"]:has(h1, h2, h3) {
    margin-bottom: 0.5rem !important;
}

    
/* ---------- フッターボタン内の調整 ---------- */

/* フッター内のボタンを正方形・タップ領域最適化 */
div[id="fixed_footer_root"] + div button {
    height: 52px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ボタン内のマテリアルアイコンのサイズ調整 */
div[id="fixed_footer_root"] + div button [data-testid="stIconMaterial"] {
    font-size: 28px !important; /* スマホで綺麗に収まるサイズ */
}

/* ---------- 共通設定 ---------- */
/* 全体文字折返し */
* {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}

</style>
"""


def apply_styles():

    st.markdown("""
<link rel="stylesheet"
href="https://googleapis.com" />
""", unsafe_allow_html=True)

    st.markdown(APP_CSS, unsafe_allow_html=True)
