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

*/
[data-testid="stAppHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    display: none !important;
}

/* 
   2. メインコンテンツを包むコンテナの上部パディング（padding-top）を
      0に強制上書きし、画面の一番上からコンテンツが始まるようにします。
*/
.main .block-container {
    padding-top: 0px !important;       /* 上の余白を完全にゼロにする */
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 160px !important;  /* フッター + バッジを避ける下部余白 */
    max-width: 100% !important;
}

.stApp {
    padding-top: 0px !important;       /* アプリ全体の上の余白もリセット */
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
    min-width: 0 !important; /* これがないとスマホの画面幅を突き破ります */
    overflow: hidden !important;
}

/* 
   2. アイコンの右側にある「文字が入っている領域」をピンポイントで捕獲。
      ここを最小幅0に制限（min-width: 0）することで、初めて内部の文字の自動縮小と省略（...）が発動します。
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
   3. 実際の文字（pタグ、spanタグ、テキストすべて）に対して、
      絶対に改行を許さず、画面サイズに合わせてコンパクト（スマホでは画面幅の約5.2%）に自動縮小します。
*/
.main .block-container h1 p,
.main .block-container h1 span,
.main .block-container h1,
.main .block-container h2 *,
.main .block-container h3 * {
    white-space: nowrap !important;      /* スマホでも絶対に折り返さない */
    word-break: keep-all !important;     /* 単語の途中での改行も禁止 */
    overflow: hidden !important;         /* 溢れたテキストは隠す */
    text-overflow: ellipsis !important;  /* 画面端に到達したら自動で「...」にする */
    
    /* スマホ画面の横幅（vw）に合わせてフォントサイズを動的に小さくする */
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

    st.markdown("""
<link rel="stylesheet"
href="https://googleapis.com" />
""", unsafe_allow_html=True)

    st.markdown(APP_CSS, unsafe_allow_html=True)
