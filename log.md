# 変更履歴

## 2026-04-27

### リポジトリ初期構築
- ai_catchup を参考に、中小企業マーケ担当者向け「マーケキャッチアップ」リポジトリを構築
- ディレクトリ構成: `.github/workflows/`, `scripts/`, `Raw/`, `Archive/`, `Summary/`, `.claude/skills/zept-sns-marketing-catchup/`
- RSSフィード: 国内7本＋海外8本＝15本（マーケ全般・SNS運用・AIマーケ）
- GitHub Actions: rss-collect.yml（毎日6:00 JST）、chat-notify.yml（平日6:00 JST）
- レポート構造: 4層分類（速報/最重要/実務/市場動向）＋コンサル活用法
- 出力先: Archive/（日次素材）、Summary/（共有用の充実レポート★メイン）

### 削ぎ落とした機能（ai_catchup比）
- ブログ・note・share-text 転載生成
- XBookmark 取り込み（別リポ ai-catchup-xbookmark の責務）
- NotebookLM音声解説・漫画生成
- 自動投稿スクリプト（X/note/FB）
- 派生コンテンツ生成（eyecatch/manga/pdf-to-png/resize）

### 初回ローカルテスト結果
- 15フィード中 12稼働、3フィード（Web担当者Forum / コムニコ / Later Blog）はRSS廃止のため除外
- 12フィードで合計約205件取得確認（PR TIMESは200件と多いためスキル側で要フィルタ）

### 次回作業予定
- GitHubリポジトリ作成・push
- GitHub Pages 有効化
- Secrets `GOOGLE_CHAT_WEBHOOK` 登録
- 初回 rss-collect 手動実行で動作確認
