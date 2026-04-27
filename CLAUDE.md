# sns_marketing_catchup

中小企業のマーケティング担当者向けに、SNS運用・AIマーケ・広告運用の最新情報を毎日キャッチアップし、深読みレポートを生成するリポジトリ。

## アーキテクチャ

```
[GitHub Actions（クラウド・毎日6:00 JST）]
   ↓ rss_collect.py が国内7+海外8のRSSを取得
[Raw/ に記事mdファイルが自動コミット]
   ↓ ローカルObsidianが GitHub からpullで同期
[Obsidian + Claude Code で zept-sns-marketing-catchup スキル発動]
   ↓ 4層分類・深読みレポート生成
[Archive/YYYY年度/M月/YYYY.M.DD/index.md（日次素材）]
[Summary/YYYY年度/M月/YYYY.M.DD.md（共有用の充実レポート）]
   ↓ git push
[GitHub Pages で公開]
   ↓ chat-notify.yml が Google Chat に通知
```

## ディレクトリ構成

| パス | 役割 |
|---|---|
| `.github/workflows/rss-collect.yml` | 毎日6:00 JSTにRSS自動取得 |
| `.github/workflows/chat-notify.yml` | 平日6:00 JSTにGoogle Chat通知 |
| `scripts/rss_collect.py` | RSS取得本体（Python標準ライブラリのみ） |
| `Raw/` | RSS取得記事の自動保存先（gitignoreではない、コミット対象） |
| `Archive/YYYY年度/M月/YYYY.M.DD/` | 日次の深読みレポート素材 |
| `Summary/YYYY年度/M月/YYYY.M.DD.md` | 共有用の充実版レポート★メイン成果物 |
| `_config.yml` `index.md` | GitHub Pages公開設定 |
| `.claude/skills/zept-sns-marketing-catchup/SKILL.md` | レポート生成ワークフロー |

## RSSフィード（12本）

### 国内（5本）
- MarkeZine / AdverTimes / ITmedia マーケティング / PR TIMES / SMMLab

### 海外（7本）
- Social Media Examiner / Hootsuite Blog / Buffer Blog / Sprout Social Insights
- Search Engine Journal / Platformer / TechCrunch (Social)

> 過去に検討したがRSS廃止または取得不可で除外：Web担当者Forum / コムニコ We Love Social / Later Blog

## レポートの4層分類

1. **今日の速報ヘッドライン**：アルゴリズム変更・プラットフォーム新機能
2. **中小企業に効く最重要トピック**：低予算で真似できる事例・ツール
3. **実務・運用ノウハウ**：投稿時間・ハッシュタグ・KPI分析・AI活用法
4. **AIマーケ市場動向**：業界全体のトレンド・新ツール・規制動向

各記事に「**コンサルとしての活用法**」を付与する。

## 想定読者
- 中小企業の経営者・マーケティング担当者
- DX推進担当者
- AIマーケティングを始めたい層
- ZeptのAIコンサル提案資料の元ネタ

## セットアップ手順
1. このリポジトリを GitHub に push（リポ名: `sns-marketing-catchup`）
2. GitHub Pages を有効化（Settings → Pages → Source: main / `/`）
3. Secrets に `GOOGLE_CHAT_WEBHOOK` を登録
4. Actions の rss-collect を手動で1回実行して動作確認
