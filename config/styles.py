/* ---------- 【超強化】タイトル・見出しの折り返し防止 ---------- */

/* 
   1. st.title(":material/...: タイトル") などのアイコン付き見出しコンテナ。
      スマホ画面からはみ出た部分を「...」にするため、親コンテナの幅と溢れを制限。
*/
.main .block-container [data-testid="stHeadingWithIcon"],
.main .block-container [data-testid="stHeaderBlockContainer"],
.main .block-container [data-testid="element-container"]:has(h1, h2, h3) {
    min-width: 0 !important;
    max-width: 100% !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important; /* コンテナ自体も絶対に縦に折らせない */
    align-items: center !important;
}

/* 
   2. 見出し内部の「テキスト部分」を狙い撃ち。
      アイコンの横にある文字列が絶対に2行にならないように強制します。
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
}

/* 
   3. 文字サイズが大きすぎるとスマホ画面（約360px）にそもそも収まりきらないため、
      見出しの文字サイズをスマホ向けに最適化（PCでは1.4rem以上、スマホでは画面幅の5.5%）。
*/
.main .block-container h1,
.main .block-container h1 span,
.main .block-container [data-testid="stHeadingWithIcon"] h1 p {
    font-size: max(1.3rem, 5.5vw) !important;
    line-height: 1.2 !important;
}
