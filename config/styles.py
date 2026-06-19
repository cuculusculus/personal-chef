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

/* ---------- タイトル・見出しの折り返し防止（完全版） ---------- */

/* 
   1. タイトルを包んでいるStreamlitの全階層（コンテナ、Heading、ブロック要素）に対して、
      「画面幅100%を超えたら即座に非表示（hidden）にし、横1列（flex-direction: row）を死守する」設定を強制します。
*/
.main .block-container [data-testid="stHeadingWithIcon"],
.main .block-container [data-testid="stHeaderBlockContainer"],
.main .block-container [data-testid="element-container"]:has(h1, h2, h3),
.main .block-container h1,
.main .block-container h2,
.main .block-container h3 {
    min-width: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important; /* 縦への折り返しを地球上で絶対に禁止 */
    align-items: center !important;
}

/* 
   2. 効かなかった最大の原因である「見出し内部のすべての文字・要素（p, span, div等）」を狙い撃ち。
      Streamlitが自動生成するインライン要素の挙動をすべて破壊し、改行なし（nowrap）と省略（ellipsis）を上書きします。
*/
.main .block-container h1 *,
.main .block-container h2 *,
.main .block-container h3 * {
    white-space: nowrap !important;      /* 自動改行を完全に禁止 */
    word-break: keep-all !important;     /* 文字の切れ目での改行も許さない */
    overflow: hidden !important;         /* 溢れたテキストは隠す */
    text-overflow: ellipsis !important;  /* 末尾を必ず「...」にする */
    display: inline-block !important;    /* 1行で並べるためにインラインブロック化 */
    max-width: 100% !important;
}

/* 
   3. 文字サイズ自体が大きすぎると「...」だらけで何も読めなくなるため、
      スマホ画面向けにフォントサイズをコンパクト（約20px〜22px前後）に強制縮小します。
*/
.main .block-container h1,
.main .block-container h1 *,
.main .block-container [data-testid="stHeadingWithIcon"] h1 p {
    font-size: max(1.2rem, 5.2vw) !important;
    line-height: 1.1 !important;
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

    st.markdown("""
<link rel="stylesheet"
href="https://googleapis.com" />
""", unsafe_allow_html=True)

    st.markdown(APP_CSS, unsafe_allow_html=True)
