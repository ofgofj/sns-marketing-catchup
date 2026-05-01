---
description: 当日のマーケキャッチアップSummary MDからNotebookLM音声概要を生成し、Chatworkマイチャットに通知
---

# /marketing-audio

`marketing-notebooklm-audio` スキルを発動し、本日分の Summary MD を NotebookLM に登録、音声概要（podcast）を生成→共有URL取得→Chatworkマイチャット（376976342）にURLだけ通知する。

## 前提
- `/marketing-catchup` が当日分の Summary を生成済みであること
- `notebooklm-py` CLI が認証済みであること
- `~/.bashrc` に `CHATWORK_API_TOKEN` が設定済みであること

## 実行内容（スキルの責務）
1. Summary MD を `Summary/YYYY年度/M月/YYYY.M.DD.md` から最新自動検出
2. NotebookLM 認証確認 → ノートブック作成 → Summary MD をソース追加
3. 中小企業マーケ担当者向けプロンプトで音声概要を deep-dive 形式・日本語で生成
4. 完了待機（10〜30分・最大45分）→ 公開共有URLを取得
5. URLとtask_idをローカル `Summary/YYYY年度/M月/YYYY.M.DD-notebooklm-audio-url.txt` 等に保存
6. Chatworkマイチャット（376976342）にURL1行だけ送信
7. 完了報告（git push は行わない）

## 重要
- URLファイルは git にコミットしない（`Summary/**` は GitHub Pages 公開対象のため）
- 生成に時間がかかるためバックグラウンド実行を推奨

それでは `marketing-notebooklm-audio` スキルを起動してください。
