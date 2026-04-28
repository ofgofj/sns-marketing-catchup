---
description: 中小企業向けマーケキャッチアップ記事を生成し、push→Google Chat通知まで一括実行
---

# /marketing-catchup

`zept-sns-marketing-catchup` スキルを発動して、本日分のマーケキャッチアップ深読みレポートを生成・push します。

## 実行内容（スキルの責務）

1. `git pull --rebase` で Raw/ を最新化
2. Raw/ から本日収集分の記事を読み込み
3. 4層分類（速報／中小企業向け／実務ノウハウ／市場動向）
4. 各記事に「コンサルとしての活用法」を付与
5. `zept-veritas` でファクトチェック
6. `Archive/{年度}/{月}月/{YYYY.M.DD}/index.md` 生成
7. `Summary/{年度}/{月}月/{YYYY.M.DD}.md` 生成（メイン成果物・3000〜5000字）
8. `git add Archive/ Summary/ && git commit && git push origin main`

## push 後の自動アクション

- GitHub Pages がビルド → https://ofgofj.github.io/sns_marketing_catchup/ に反映
- `chat-notify.yml` が `Summary/**` 変更を検知して発火 → Google Chat に通知

## 完了報告

スキルの完了報告フォーマットに従って報告すること。

---

それでは `zept-sns-marketing-catchup` スキルを起動してください。
