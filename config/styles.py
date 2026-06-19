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

/* ---------- アプリ全体レイアウト ---------- */

.main .block-container {
    padding-top: 0.2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 160px !important; /* フッター + バッジを避ける余白 */
    max-width: 100% !important;
}

.stApp {
    padding-bottom: 100px;
}

/* ---------- タイトル・見出しの折り返し防止 ---------- */

/* 
   1. アイコン付き見出し（stHeadingWithIcon）などの親コンテナ。
      スマホ画面からはみ出た部分を「...」にするため、親コンテナ全体の折り返しを禁止。
*/
.main .block-container [data-testid="stHeadingWithIcon"],
.main .block-container [data-testid="stHeaderBlockContainer"],
.main .block-container [data-testid="element-container"]:has(h1, h2, h3) {
    min-width: 0 !important;
    max-width: 100% !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important; /* 絶対に縦に折らせない */
    align-items: center !important;
}

/* 
   2. 見出しタグおよび内部のすべての要素。
      【修正】ユニバーサルセレクタ「*」のみに絞り、解析エラーが起きない安全な形に修正。
*/
.main .block-container h1,
.main .block-container h2,
.main .block-container h3,
.main .block-container h1 *,
.main .block-container h2 *,
.main .block-container h3 * {
    white-space: nowrap !important;     /* 絶対に改行させない */
    word-break: keep-all !important;    /* 単語途中での折り返しも禁止 */
    overflow: hidden !important;        /* はみ出た部分は隠す */
    text-overflow: ellipsis !important; /* 末尾を自動で「...」にする */
    display: block !important;
}

/* 
   3. 見出しの文字サイズをスマホ向けに最適化
*/
.main .block-container h1,
.main .block-container h1 span,
.main .block-container [data-testid="stHeadingWithIcon"] h1 p {
    font-size: max(1.3rem, 5.5vw) !important;
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
/* 
   【修正】SyntaxErrorの原因だった :not() 構文を排除。
   通常の段落テキストがスマホで適切に折り返される基本設定のみにシンプル化。
*/
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

    st.markdown(APP_CSS, unsafe_allow_html=True)
