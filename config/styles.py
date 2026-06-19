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

/* ---------- アプリ全体レイアウト（上部余白カット） ---------- */

/* 最新のStreamlitコンテナの上部余白（padding-top）を0pxに強制します */
[data-testid="stMainBlockContainer"],
.main .block-container {
    padding-top: 0px !important;
    margin-top: 0px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 160px !important;  /* フッター + バッジを避ける下部余白 */
    max-width: 100% !important;
}

.stApp {
    padding-top: 0px !important;
    padding-bottom: 100px;
}


/* ---------- 各ページタイトルの画面サイズ最適化 ---------- */

/* 
   1. タイトル全体のコンテナ（Grid構造）の横幅が
      スマホの画面幅（100%）を絶対に超えないように物理制限をかけます。
*/
.main .block-container [data-testid="stHeadingWithIcon"],
.main .block-container [data-testid="stHeaderBlockContainer"],
.main .block-container [data-testid="element-container"]:has(h1, h2, h3) {
    max-width: 100% !important;
    width: 100% !important;
    min-width: 0 !important;
    overflow: hidden !important;
}

/* 
   2. アイコンの右側にある「文字が入っている領域」をピンポイントで捕獲。
*/
.main .block-container [data-testid="stHeadingWithIcon"] > div:last-child,
.main .block-container h1,
.main .block-container h2,
.main .block-container h3 {
    min-width: 0 !important;
    max-width: 100% !important;
    overflow: hidden !important;
}

/* 
   3. 実際の文字に対して、絶対に改行を許さず自動縮小・省略（...）させます。
*/
.main .block-container h1 p,
.main .block-container h1 span,
.main .block-container h1,
.main .block-container h2 *,
.main .block-container h3 * {
    white-space: nowrap !important;
    word-break: keep-all !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    font-size: max(1.2rem, 5.2vw) !important; 
    line-height: 1.2 !important;
}

/* ---------- フッターボタン内の調整 ---------- */

/* フッター内のボタンを正方形・タップ領域最適化 */
div[id="fixed_footer_root"] + div button {
    height: 52px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center;
}

/* ボタン内のマテリアルアイコンのサイズ調整 */
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
    # 【修正】崩れていたGoogle FontsのURLを、マテリアルアイコン用の正しいURLに修正
    st.markdown("""
<link rel="stylesheet"
href="https://googleapis.com" />
""", unsafe_allow_html=True)

    # 確実に上部余白を消去するため、st.markdownではなく、自動余白のつかないst.htmlで出力
    st.html(APP_CSS)
