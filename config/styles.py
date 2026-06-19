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
    padding-bottom: 110px !important; /* フッターにコンテンツが隠れないように下部に余白を確保 */
    max-width: 100% !important;
}

.stApp {
    padding-bottom: 100px;
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
