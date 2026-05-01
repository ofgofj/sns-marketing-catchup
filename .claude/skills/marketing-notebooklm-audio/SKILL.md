---
name: marketing-notebooklm-audio
description: >
  マーケキャッチアップの当日Summary MDをソースとしてNotebookLMに登録し、
  「音声概要（Audio Overview / podcast）」を中小企業マーケ担当者向けプロンプトで生成、
  公開リンクを Summary/YYYY年度/M月/YYYY.M.DD-notebooklm-audio-url.txt に保存し、
  最後に Chatwork マイチャット（376976342）にURLだけを自動送信するスキル（一気通貫）。
  「マーケ音声生成」「マケ音声」「マーケキャッチアップの音声」「マーケnotebook」と言われたら使う。
  zept-sns-marketing-catchup（/marketing-catchup）が完了した後に実行する。
  ※ 参考元: ai-blockchain側の bc-notebooklm-audio。本スキルは中小企業マーケ担当者向けプロンプトに置換した版。
---

# マーケキャッチアップ NotebookLM 音声概要生成スキル

## 概要
zept-sns-marketing-catchup が出力した当日の Summary MD を元に、NotebookLM で **音声概要（Audio Overview = NotebookLMのポッドキャスト機能）** を1本生成する。中小企業のマーケ担当者・経営者・兼務マーケが移動中・家事中に耳で聞いて、明日からの施策に直結する論点をインプットするための補助教材。

**このスキルは毎日の一連フローの最終ステップ。生成→URL保存→Chatwork通知で終了し、git push は行わない。**
URL txt ファイルはローカル参照用。Summary配下にあるが git にはコミットしない運用（Summary/** は GitHub Pages 公開対象なので、再生用URLは外部公開せず手元参照のみで持つ）。

## 毎日の実行順序（推奨）

```
1. /marketing-catchup（zept-sns-marketing-catchup） → Summary/YYYY年度/M月/YYYY.M.DD.md 生成 + git push
2. marketing-notebooklm-audio                       → 音声概要生成 + URL保存 + Chatwork通知（本スキル・ここで一連作業は完了）
```

音声概要生成は 10〜30分かかるのが目安。バックグラウンド実行を推奨。

## 前提条件
- `notebooklm-py` CLI インストール済み（`C:\Users\yfuji\AppData\Roaming\Python\Python312\Scripts\notebooklm.exe`）
- NotebookLM 認証済み（デフォルトの `~/.notebooklm/storage_state.json`。zept.design アカウント）
- 当日の Summary MD が存在すること（`/marketing-catchup` 実行済み）
- Chatwork APIトークン: `~/.bashrc` の `CHATWORK_API_TOKEN` に設定済み

**アカウント方針:** ai-catchup・ai-blockchain と同じ **zept.design アカウント**（デフォルト認証）で運用する。

## 変数
- `NOTEBOOKLM`: `C:/Users/yfuji/AppData/Roaming/Python/Python312/Scripts/notebooklm.exe`
- `SUMMARY_ROOT`: `C:/Users/yfuji/sns_marketing_catchup/Summary`
- `CHATWORK_MY_ROOM_ID`: `376976342`（マイチャット固定）

## 入力
- Summary MD のパス（未指定時は最新を自動検出: `Summary/YYYY年度/M月/YYYY.M.DD.md` で日付が最新のもの）

## ディレクトリ構造（このリポジトリ独自）
- ai_catchup: `Summary/YYYY年度/M月/YYYY.M.DD/YYYY-MM-DD.md`（日付サブフォルダあり）
- ai-blockchain: `Summary/YYYY/MM/YYYY-MM-DD.md`（フラット）
- **sns_marketing_catchup: `Summary/YYYY年度/M月/YYYY.M.DD.md`（年月フォルダ／日付ファイル直置き）**

URL保存ファイルは MD と同じフォルダに、ファイル名プレフィックスで紐付ける:
- `Summary/YYYY年度/M月/YYYY.M.DD-notebooklm-audio-url.txt`
- `Summary/YYYY年度/M月/YYYY.M.DD-notebooklm-artifact-id.txt`

## フロー: STEP 1→2→3→4→5→6→7→8→9 を完走（一気通貫・git push なし）

```
STEP 1   Summary MD 特定
STEP 2   認証確認
STEP 3   ノートブック作成
STEP 4   ソース追加（Summary MD 1件のみ）
STEP 5   音声概要生成（中小企業マーケ担当者向けプロンプト）
STEP 6   完了待機
STEP 7   共有設定＋URL保存（ローカルのみ。git add/commit/push は行わない）
STEP 8   Chatwork 通知（ルームID 376976342 固定・URL1行のみ送信）
STEP 9   完了報告（ここで終了）
```

スキルを1回発動すれば STEP 1〜9 が一気通貫で走る。途中の認証エラー・生成失敗以外で止まらない。

### STEP 1: Summary MD の特定

未指定時、年月フォルダ配下の `YYYY.M.DD.md` ファイル（URLファイルやartifactファイルは除外）から最新を取得:
```bash
ls "$SUMMARY_ROOT"/*年度/*月/????.*.??.md 2>/dev/null \
  | grep -v 'notebooklm' \
  | sort -r | head -1
```

見つからなければ「Summary MDなし」で終了。`/marketing-catchup` の実行を促す。

`SUMMARY_MD_PATH` を決定。同時に以下を抽出:
- `SUMMARY_DIR`: MD の親ディレクトリ（= `Summary/YYYY年度/M月/`）
- `BASENAME`: ファイル名から拡張子を除いたもの（= `YYYY.M.DD`）
- `DATE_STR`: `YYYY-MM-DD` 形式（タイトル・通知用）。`BASENAME` の `.` を `-` に置換し月日をゼロ埋め
- `URL_FILE`: `${SUMMARY_DIR}/${BASENAME}-notebooklm-audio-url.txt`
- `TASK_ID_FILE`: `${SUMMARY_DIR}/${BASENAME}-notebooklm-artifact-id.txt`

### STEP 2: 認証確認
```bash
PYTHONUTF8=1 "$NOTEBOOKLM" list --json 2>&1 | head -5
```
- 正常にJSONが返ればOK
- `Not logged in` または認証エラーが出たら、ユーザーに以下を実行してもらう:
  ```powershell
  & "C:\Users\yfuji\AppData\Roaming\Python\Python312\Scripts\notebooklm.exe" login
  ```
  完了まで待つ。

### STEP 3: ノートブック作成
```bash
PYTHONUTF8=1 "$NOTEBOOKLM" create "マーケキャッチアップ ${DATE_STR}" 2>&1
```
出力から `Created notebook: <id>` を抽出 → `NOTEBOOK_ID` に保存。

コンテキスト設定:
```bash
PYTHONUTF8=1 "$NOTEBOOKLM" use "$NOTEBOOK_ID" 2>&1
```

### STEP 4: ソース追加（1件のみ）
音声概要は視覚要素がないため、画像は不要。Summary MD のみをソースにする。
```bash
PYTHONUTF8=1 "$NOTEBOOKLM" source add "$SUMMARY_MD_PATH" --title "マーケキャッチアップ ${DATE_STR}" 2>&1
```

### STEP 5: 音声概要生成（deep-dive / 日本語 / 中小企業マーケ担当者向け）

音声概要のプロンプト（定型文。大きな変更はユーザー相談）:

```
このポッドキャストの聴取者は、**中小企業の経営者・マーケティング担当者・兼務マーケ担当**
（社員数10〜100名規模・月マーケ予算10〜100万円・SNS運用は社内で兼務、もしくは代理店に半分丸投げ）です。
専門のSNSマネージャーや広告運用者ではなく、本業の傍らでマーケを回している忙しい現場の人。

このソースを元に、2人のホストによる deep-dive 形式のポッドキャストを生成してください。

## 最重要コンセプト
- 毎朝・毎晩の通勤や移動中に1本聞き終えると、「今日のSNS・AIマーケ・広告運用で何が起きたか」と
  「明日から何を変えればいいか」が頭に入る教材
- 「概念の解説」より「明日からの実装」を優先
- 1本聴き終わった後に「これを社内のSlackで共有しよう」「来週のミーティングで提案しよう」と
  具体的な次の行動が浮かぶ体験を作る

## 話し方の絶対ルール

1. **専門用語は必ず1文で噛み砕く**
   - 悪い例: 「今日はAlgo更新の話から」
   - 良い例: 「今日はFacebookのアルゴリズム更新の話から。アルゴリズムっていうのは、
     誰の投稿を誰に見せるかを自動で決めているMetaのルールのこと。
     今回はそのルールが2026年に大きく変わって……」
   - CTR、CPA、ROAS、LTV、CVR、エンゲージメント率、リーチ、インプレッション、
     LLMO、AIO、GEO、AI Overview、AI Max、ファーストパーティデータ、ヘッドレスCMS など
     **ニュース本文に出てくる用語はすべて、初出時に1文で言い直す**

2. **「中小企業の現場」を主語にして話す**
   - 「予算50万円のクライアントなら……」
   - 「社員5人のマーケチームなら……」
   - 「兼務担当が週に5時間しか取れないなら……」
   - 大企業の事例で終わらせず、必ず「これを月予算30万円の会社が真似するなら」に翻訳する

3. **数字は必ず正確に、コスト試算は具体的に**
   - 「ChatGPT Plusは月3,000円」「Canva Proは月1,500円」
   - 「外注ライターを使えば月10万円、AIで内製化すれば月3万円」
   - 「時給3,000円換算で月5時間削減なら月1.5万円」
   - 桁が大きい時は「億単位で言うと」「万円単位で言うと」など補足

4. **「明日から何をするか」を必ず添える**
   - ニュースを紹介して終わらせない
   - 「だから明日のミーティングでは○○を提案する」
   - 「だから今週中に自社のSNSレポートから○○を外して、○○を入れる」
   - 「だから3月までに広告予算を○○から○○に組み替える」

5. **2人のホストの掛け合いを活かす**
   - 一人が「うちみたいな中小だと、これってどうなるんですか？」と現場目線の質問役
   - もう一人が「中小なら、まずこの3つを今週やればいい」と実装目線の解説役
   - ただし解説役も断定口調ではなく、「〜という事例があります」「〜と言われています」

6. **代理店・SaaS提案を鵜呑みにしない目線**
   - 「代理店からTikTok提案が来たら、まずこの数字を聞き返す」
   - 「SaaSの月額が1万円なら、削減できる工数で割り返す」
   - 中小企業がベンダーロックインや過剰投資を避けるための見極め視点を入れる

7. **投資助言・ベンダー誘導にならないよう注意**
   - 「○○というSaaSを必ず買うべき」「このツールが最強」などの断定は**禁止**
   - 「こういう選択肢があります」「こういう判断軸で選べます」という情報提供にとどめる

## 扱う範囲
- ソースの「本日のハイライト」「🚨速報ヘッドライン」「🔴最重要トピック」を中心に解説
- 「🔴最重要トピック」は特に丁寧に、各トピック5〜7分かけて深掘りする
- 「🟡実務・運用ノウハウ」は「明日から使えるテンプレ・プロンプト」として軽く全件触れる
- 「🟢市場動向」は1〜2分で要点だけ
- 「💼コンサル視点まとめ」の営業アクションリストは、独立コンサル・代理店向けに転用できる形で紹介

## 避けること
- ソース自体の解説（「このレポートは〜」のメタ説明）
- キャラクター紹介や自己紹介
- ソース外の憶測・追加情報の創作
- 「○○を必ず買うべき」「このSaaSが正解」などの断定的なベンダー誘導
- 大企業のケーススタディだけで完結させる（必ず中小に翻訳する）

## 最終目標
毎日この音声を聴くことで、聴取者が
「SNS・AIマーケ・広告運用で今、何が起きているか」を構造的に理解し、
「自分の会社・自分のクライアントに、明日から何を提案すればいいか」を
言語化できるようになること。最終的にはマーケ担当者本人が
代理店との交渉・社内稟議・経営層への提案で、データに基づいた1次主張ができる
レベルまで育つこと。
```

生成開始:
```bash
PYTHONUTF8=1 "$NOTEBOOKLM" generate audio "$PROMPT" \
  --format deep-dive \
  --length default \
  --language ja \
  --json
```
出力JSONから `task_id` を抽出 → `TASK_ID`。

### STEP 6: 完了待機（最大45分）

```bash
PYTHONUTF8=1 "$NOTEBOOKLM" artifact wait "$TASK_ID" --timeout 2700 --interval 30 --json
```

- ポーリング30秒間隔、最大45分待機
- 通信タイムアウトで failed 扱いで戻った場合、`artifact get <id>` で実際の状態を確認
  - 実態が `in_progress` なら再度 `artifact wait` で継続
  - `completed` ならOK
  - `failed` なら STEP 5 からリトライ（最大2回）
- **レート制限（RATE_LIMITED）** に当たった場合: 30分以上待って再試行

### STEP 7: 共有設定＋URL保存
```bash
PYTHONUTF8=1 "$NOTEBOOKLM" share view-level full 2>&1
PYTHONUTF8=1 "$NOTEBOOKLM" share public --enable --json
```
出力JSONから `share_url` を抽出 → `SHARE_URL`。

保存（ローカルのみ。git には絶対に追加しない）:
```bash
echo "$SHARE_URL" > "$URL_FILE"
echo "$TASK_ID"   > "$TASK_ID_FILE"
```

**⚠ git add / git commit / git push は絶対に実行しない。**
URL txt ファイルは `Summary/` 配下にあるが、`Summary/**` は GitHub Pages 公開対象。NotebookLM の音声概要URLは zept.design アカウント発行のリソースであり、不特定多数に公開する想定ではない。ローカル参照のみ＋Chatworkマイチャットへの自動投函で完結させる。

`.gitignore` に以下を追加することを推奨（既になければ）:
```
Summary/**/*-notebooklm-audio-url.txt
Summary/**/*-notebooklm-artifact-id.txt
```

URL は以下から参照する:
- ローカルファイル: `Summary/YYYY年度/M月/YYYY.M.DD-notebooklm-audio-url.txt`
- またはChatworkマイチャットの過去ログ
- またはユーザーが手動でブラウザのブックマークに貼る

### STEP 8: Chatwork通知（ルームID 376976342 固定 = ユーザーのマイチャット）

生成成功後、**自動で Chatwork ルーム `376976342` に共有URLだけを送信**する。日付なし、装飾なし、URL1行のみ。Chatwork側でURLは自動リンク化される。

**⚠ 重要:** ルームID `376976342` はユーザー（藤井悠真さん）のマイチャットそのもの。Chatwork API `/v2/me` の `room_id` フィールドで確認可能。「マイチャットに送って」と言われた場合もこのIDで対応すれば二重送信不要。

実装（bash から Node.js を呼ぶ。curl は文字化けリスクあり & APIトークンは `~/.bashrc` の `CHATWORK_API_TOKEN` から読む）:

```bash
bash -c 'source ~/.bashrc && SHARE_URL="'"$SHARE_URL"'" node -e "
const https = require(\"https\");
const body = process.env.SHARE_URL;
const params = \"body=\" + encodeURIComponent(body);
const payload = Buffer.from(params, \"utf8\");
const req = https.request({
  hostname: \"api.chatwork.com\",
  path: \"/v2/rooms/376976342/messages\",
  method: \"POST\",
  headers: {
    \"X-ChatWorkToken\": process.env.CHATWORK_API_TOKEN,
    \"Content-Type\": \"application/x-www-form-urlencoded\",
    \"Content-Length\": payload.length
  }
}, res => {
  let data = \"\";
  res.on(\"data\", c => data += c);
  res.on(\"end\", () => {
    console.log(\"HTTP \" + res.statusCode);
    console.log(data);
  });
});
req.on(\"error\", e => { console.error(\"ERR\", e.message); process.exit(1); });
req.write(payload);
req.end();
"'
```

- `HTTP 200` と `{"message_id":"..."}` が返れば成功
- 失敗した場合は STEP 9 の完了報告で明記する（URLはローカルにあるので手動で送れる）
- ルームID `376976342` は固定値（= ユーザーのマイチャット）

### STEP 9: 完了報告（ここで終了）

完了報告に含める項目:
- ノートブックID
- 音声概要の共有URL（そのままクリック可能な形で提示）
- アーティファクトID
- 保存先: `Summary/YYYY年度/M月/YYYY.M.DD-notebooklm-audio-url.txt` / `-notebooklm-artifact-id.txt`
- 生成にかかった時間
- **Chatwork通知の送信ステータス**（HTTP 200 / message_id または失敗理由）

報告後、このスキルは**ここで終了**。git操作は行わない。

## エラーハンドリング

| 問題 | 対処 |
|------|------|
| Summary MDが見つからない | 「Summary MDなし」で終了。`/marketing-catchup` 実行を促す |
| 認証切れ | ユーザーに `notebooklm login` 依頼、完了後に再開 |
| 音声生成 failed × 3回 | 時間を置いて再実行。プロンプト長すぎが原因のこともあるので短縮検討 |
| RATE_LIMITED | 30分以上待って再試行 |
| source addで拒否 | Summary MDの文字数オーバーの可能性。「🚨速報ヘッドライン〜🔴最重要トピック」だけを抜粋した一時ファイルを作って渡す |
| ノートブック100個上限 | 古いノートブックを手動 or スクリプトで削除してから STEP 3 に戻る |
| 音声が英語で生成された | `--language ja` が効いていない。プロンプト先頭に「日本語で話してください」と明記して再生成 |

## 注意事項
- **プロンプトは定型文を基本とする**。NotebookLM音声概要の品質に直結する。抜本的な改変はユーザー相談必須
- **公開リンク**（閲覧のみ＝再生のみ）で共有する
- **生成に10〜30分かかる**ことを前提にバックグラウンド実行推奨
- **音声概要は耳で聞く教材**なので、ベンダー誘導と誤解される言い回し・断定的な「○○を買うべき」は絶対に避ける
- **Summary MDがまだ存在しない状態でこのスキルを呼ばれたら**「今日のレポートが未作成です。先に /marketing-catchup を実行してください」と返答
- **既に当日のURLファイルがある場合**、上書き前にユーザーに確認する（再生成=既存音声の喪失につながるため）
