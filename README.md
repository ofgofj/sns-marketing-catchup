# sns_marketing_catchup

**中小企業のマーケ担当者向け、SNS運用・AIマーケ最新情報の自動収集＆深読みレポート生成リポジトリ。**

## 1. このリポジトリの目的

毎日朝6時にマーケ系RSS15本を自動巡回し、Claude Code＋GPT-5.5などで「中小企業の現場視点」の深読みレポートを生成する。読者は中小企業のマーケ担当者・DX推進担当・コンサル提案の素材作りをする人。

## 2. 仕組み

```
GitHub Actions (毎日6:00 JST)
  ↓ scripts/rss_collect.py が15フィード取得
Raw/ に記事を自動コミット
  ↓ ローカル Obsidian に GitHub から sync
Claude Code でスキル zept-sns-marketing-catchup 起動
  ↓ 4層分類・深読みレポート生成
Archive/YYYY年度/M月/YYYY.M.DD/  （日次素材）
Summary/YYYY年度/M月/YYYY.M.DD.md  （共有用★メイン成果物）
  ↓ git push
GitHub Pages 公開
  ↓ chat-notify.yml が Google Chat 通知
```

## 3. ディレクトリ構成

```
.
├── .github/workflows/
│   ├── rss-collect.yml    ← 毎日6:00 JSTにRSS自動取得
│   └── chat-notify.yml     ← 平日6:00 JSTにGoogle Chat通知
├── scripts/
│   └── rss_collect.py      ← RSS取得本体（Python標準ライブラリのみ）
├── Raw/                    ← RSS取得記事の自動保存先
├── Archive/                ← 日次の深読みレポート素材
├── Summary/                ← 共有用の充実版レポート★メイン成果物
├── _config.yml             ← Jekyll設定（GitHub Pages公開）
├── index.md                ← トップページ
├── CLAUDE.md               ← リポジトリ説明（詳細版）
├── .claude/skills/zept-sns-marketing-catchup/SKILL.md  ← レポート生成ワークフロー
├── .gitignore
├── log.md                  ← 変更履歴
└── README.md               ← このファイル
```

## 4. セットアップ手順（新規クローン時）

### Step 1: GitHubリポジトリ作成・push
```bash
cd C:/Users/yfuji/sns_marketing_catchup
git init
git add .
git commit -m "初期構築"
gh repo create sns_marketing_catchup --public --source=. --push
```

### Step 2: GitHub Pages を有効化
リポジトリ Settings → Pages → Source: `main` / `/ (root)` → Save

### Step 3: Secrets 登録
リポジトリ Settings → Secrets and variables → Actions → `GOOGLE_CHAT_WEBHOOK` を新規登録（既存ai-catchupと同じURLを流用可）

### Step 4: 動作確認
Actions タブ → 「RSS記事収集」 → Run workflow を手動実行 → Raw/ にmdファイルが追加されることを確認

### Step 5: ローカル運用
1. ObsidianのVaultにこのフォルダを追加
2. 毎朝GitHubからpullで同期
3. Claude Codeで「マーケキャッチアップ」と発話 → スキル起動
4. Archive/ と Summary/ が生成され、push される

## 5. RSS フィード一覧（12本）

### 国内（5本）
- [MarkeZine](https://markezine.jp/) - デジタルマーケ全般
- [AdverTimes](https://www.advertimes.com/) - 広告・マーケ（宣伝会議）
- [ITmedia マーケティング](https://www.itmedia.co.jp/marketing/)
- [PR TIMES](https://prtimes.jp/) - リリース・事例（記事数多め、スキル側でフィルタ推奨）
- [SMMLab](https://smmlab.jp/) - SNSマーケ専門

### 海外（7本）
- [Social Media Examiner](https://www.socialmediaexaminer.com/) - SNSマーケ世界最大級
- [Hootsuite Blog](https://blog.hootsuite.com/) - プラットフォーム公式
- [Buffer Blog](https://buffer.com/resources/) - データドリブンSNS論
- [Sprout Social Insights](https://sproutsocial.com/insights/) - エンタープライズ視点
- [Search Engine Journal](https://www.searchenginejournal.com/) - アルゴリズム変更速報
- [Platformer](https://www.platformer.news/) - プラットフォーム政治学
- [TechCrunch (Social)](https://techcrunch.com/category/social/) - プラットフォーム速報

### 検討したが除外（RSS廃止・取得不可）
- Web担当者Forum（webtan.impress.co.jp）：HTMLページのみで実RSSなし
- コムニコ We Love Social：RSS提供なし
- Later Blog：RSS提供なし

## 6. 注意点

- **Pythonの追加パッケージは不要**。`rss_collect.py` は標準ライブラリ（urllib + xml.etree）のみで動く。
- **GitHub Actionsはパブリックリポなら無料・無制限**。プライベートリポは月2,000分まで無料。
- **海外サイトは英語**。レポート生成時にGPT-5.5などで日本語化する。
- **PR TIMESはノイズが多い**。レポート生成時に「中小企業のマーケに関係ない」リリースは除外する。
- **Raw/ はそのままコミット**するため、リポジトリ容量に注意（数ヶ月で数千ファイルになる可能性）。
