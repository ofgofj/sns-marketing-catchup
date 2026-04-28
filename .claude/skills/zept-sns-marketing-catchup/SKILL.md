---
name: zept-sns-marketing-catchup
description: 中小企業のマーケ担当者向けマーケキャッチアップ記事を生成する。Raw/に集めたRSS記事を読み込み、4層分類で深読みレポート（Archive/とSummary/）を生成する。トリガー：「マーケキャッチアップ」「マーケ記事生成」「マケキャッチ」等。
---

# zept-sns-marketing-catchup

中小企業のマーケティング担当者向けに、Raw/に集まったRSS記事を読み込み、深読みレポートを生成するスキル。

## システム全体像（参考）

```
[6:00 JST 自動]
GitHub Actions (rss-collect.yml) が国内5+海外7のRSS取得 → Raw/にコミット
        ↓
[10分以内 自動]
Obsidian Git が auto-pull でローカル sns_marketing_catchup/Raw/ を更新
        ↓
【このスキルの責務】
ユーザーが「マーケキャッチアップ」と発話 → 本スキル発動
        ↓
[Summary/にpushされた瞬間・自動]
chat-notify.yml が Google Chat に通知（Summary/**変更検知トリガー）
```

リポジトリ: `C:\Users\yfuji\sns_marketing_catchup`
GitHub: ofgofj/sns_marketing_catchup
公開: https://ofgofj.github.io/sns_marketing_catchup/

## 想定読者（必ずこの目線でレポートを書く）
- 中小企業の経営者・マーケティング担当者
- DX推進担当者
- 月予算50万円以下でマーケ施策を回している現場
- AIマーケを始めたいが何から手をつけるか迷っている層

## ワークフロー

### STEP 0: 同期確認
作業開始前に必ず最新の Raw/ をローカルに引き込む：
```bash
cd C:/Users/yfuji/sns_marketing_catchup
git pull --rebase
```
※ Obsidian Git が10分間隔で auto-pull しているため通常は最新だが、念のため。

### STEP 1: Raw/ の最新記事を読み込む
1. `Raw/index.md` を読み、当日収集された記事一覧を把握（タイトル・URL・概要）
2. 重要そうな記事は個別 `.md` ファイルを読み込み本文を理解
3. 重複・薄い・無関係（中小企業マーケに関係ないPR TIMESなど）は除外

### STEP 2: 4層分類

| 層 | 内容 | 含めるもの |
|---|---|---|
| ① 今日の速報ヘッドライン | プラットフォーム公式発表・アルゴ変更・障害情報 | Meta/X/TikTok/LinkedInの公式動向、アップデート |
| ② 中小企業に効く最重要トピック | 低予算で真似できる事例・テンプレ・ツール | 月数千円〜数万円のSaaS事例、DIY可能な手法 |
| ③ 実務・運用ノウハウ | KPI分析・投稿時間・ハッシュタグ・AI活用 | 数値根拠付きのHowTo、運用Tips |
| ④ AIマーケ市場動向 | 業界全体トレンド・新ツール・規制 | 業界レポート、調査データ、規制動向 |

各層から最重要1〜3件を厳選。

### STEP 3: 各記事に「コンサルとしての活用法」を付与
ZeptのAIコンサル提案にどう転用できるかを1〜2文で添える。

例：
> 「クライアントに『月3万円のCanva＋ChatGPT Plus組み合わせで、SNS投稿制作工数を週20h→週5hに削減』を提案。1人当たり月15時間×時給3,000円＝月4.5万円コスト減を見える化」

### STEP 4: ファクトチェック（zept-veritas呼び出し）
レポート草稿を `zept-veritas` スキルに渡し、以下を検証する：
- 引用した数値（CVR・売上・コストなど）の真偽
- 企業名・サービス名・URL の正確性
- 「過半数」「業界初」など断定表現の根拠
- 自分が付加した「コンサル活用法」のコスト試算が妥当か

**veritas からの指摘事項を反映してから次STEPへ進む**。修正不要なら通過。

### STEP 5: ファイル出力

#### Archive（日次素材）
パス: `Archive/{年度}/{月}月/{YYYY.M.DD}/index.md`
- 4層分類した全記事の見出し・要約・コンサル活用法
- フロントマター必須（`layout: default` `title: 日次アーカイブ {YYYY-MM-DD}`）

#### Summary（共有用の充実レポート）★メイン成果物
パス: `Summary/{年度}/{月}月/{YYYY.M.DD}.md`
- フロントマター必須（`layout: default` `title: マーケキャッチアップ {YYYY-MM-DD}（深読みレポート）`）
- フォーマット: 「# マーケキャッチアップ YYYY-MM-DD（深読みレポート）」
- 各層から最重要1〜2件を厳選し、深く掘り下げる
- 中小企業の現場で「明日から何をすればいいか」が分かる粒度
- 約3,000〜5,000字
- 図表は使わず、文章中心
- 末尾に「今日のひとこと」（1段落、約200字）を入れる

### STEP 6: git push
```bash
git add Archive/ Summary/
git commit -m "マーケキャッチアップ {YYYY-MM-DD}"
git push origin main
```
push後の動き（自動）：
- GitHub Pages がビルド → https://ofgofj.github.io/sns_marketing_catchup/ に反映
- chat-notify.yml が `Summary/**` 変更検知で発火 → Google Chat 通知（push後すぐ）
- 通知フォーマット（ai-blockchain統一形式）：
  ```
  マーケキャッチアップ YYYY-MM-DD
  今日はN件まとめました。気になる方だけどうぞ。
  📖 https://ofgofj.github.io/sns_marketing_catchup/
  ```

**重要**: `Summary/` を必ず含めて push すること（含めないと通知が飛ばない）。

## レポート文体ルール
- 結論ファースト
- 数値はできるだけ具体（「効果あり」ではなく「CTR1.2%→2.8%」）
- 中小企業の現場感を重視（「大企業の事例」だけで終わらせない）
- カタカナ専門用語は初出時に「（＝〇〇のこと）」で補足
- 月予算・人月コストなどコスト視点を必ず入れる

## やらないこと
- ブログ転載用文章の生成（このリポジトリの責務外）
- note・X・FBへの自動投稿
- 画像生成
- 真偽不明の数値・引用の使用（必ず記事ソースを引用）
- ファクトチェック未実施でのpush

## 完了報告フォーマット
```
✅ マーケキャッチアップ {YYYY-MM-DD} 完成

- Raw/ から {N}件読み込み
- Archive/{年度}/{月}月/{YYYY.M.DD}/index.md 生成
- Summary/{年度}/{月}月/{YYYY.M.DD}.md 生成（{文字数}字）
- ファクトチェック: zept-veritas 通過済み
- git push 完了

公開URL: https://ofgofj.github.io/sns_marketing_catchup/
本日の深読み: https://ofgofj.github.io/sns_marketing_catchup/Summary/{YYYY年度}/{M月}/{YYYY.M.DD}.html
```
