#styles.py
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

/* ---------- アプリ全体レイアウト ---------- */

/* .main を追加して適用範囲を確実にする */
.main .block-container {
    padding-top: 0.2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 120px !important; /* フッターと被らないよう少し広めに確保 */
    max-width: 100% !important;
}

.stApp {
    padding-bottom: 100px;
}

/* ---------- フッター固定 ---------- */

/* 
   重要: st.containerの直上の親ラッパー（stElementContainer）ごと固定します。
   これにより、コンテナ内のレイアウト（columns）がスマホで縦に潰れるのを完全に防ぎます。
*/
div[data-testid="stElementContainer"]:has(div[id="footer_nav"]) {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 80px !important; /* ボタンが収まるよう高さを微調整 */
    background-color: #ffffff !important;
    border-top: 1px solid #e0e0e0 !important;
    z-index: 999999 !important;
    padding: 12px 16px 20px 16px !important; /* 下部に少し余裕（セーフエリア対策） */
    box-shadow: 0 -4px 12px rgba(0,0,0,0.05) !important;
}

/* 内部のコンテナ自体のスタイル */
div[id="footer_nav"] {
    width: 100% !important;
}

/* ---------- フッターボタン（スマホ横並びキープ） ---------- */

/* columns全体のFlexboxをスマホでも強制維持 */
div[id="footer_nav"] div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 8px !important; /* カラム間の隙間を狭く固定 */
    width: 100% !important;
}

/* 各カラムを強制的に4等分（25%）にする */
div[id="footer_nav"] div[data-testid="column"] {
    width: 25% !important;
    flex: 1 1 25% !important;
    min-width: 0 !important; /* スマホでの縮小を許可 */
}

div[id="footer_nav"] button {
    height: 50px !important;
    padding: 4px !important; /* スマホでアイコンがはみ出さないよう余白を極小に */
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ---------- フッターアイコン ---------- */
/* 
   最新のStreamlitの組み込みアイコン（st.buttonのicon引数）は
   [data-testid="stIconMaterial"] などのクラスでレンダリングされます
*/
div[id="footer_nav"] button [data-testid="stIconMaterial"],
div[id="footer_nav"] button span {
    font-size: 28px !important; /* 36pxだとスマホで大きすぎてはみ出るため28px付近が最適 */
}

/* ボタン内のラベルサイズ（今回はテキスト空""ですが、念のため残しています） */
div[id="footer_nav"] button p {
    font-size: 11px !important;
    font-weight: 600 !important;
    margin: 0 !important;
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
href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
""", unsafe_allow_html=True)

    st.markdown(APP_CSS, unsafe_allow_html=True)
