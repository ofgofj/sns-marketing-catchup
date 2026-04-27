---
layout: default
title: マーケキャッチアップ
---

# マーケキャッチアップ

中小企業のマーケティング担当者向けに、SNS運用・AIマーケ・広告運用の最新情報を深読みしてまとめています。

---

## 最新の深読みレポート（充実版）

{% assign summaries = site.pages | where_exp: "page", "page.path contains 'Summary/'" | where_exp: "page", "page.name != 'index.md'" | sort: "path" | reverse %}
{% for page in summaries limit:1 %}
{% assign parts = page.path | split: '/' %}
- [{{ parts[3] }}]({{ page.url | relative_url }})
{% endfor %}

[過去の深読みレポートを見る →](./Summary/)

---

## 日次アーカイブ

{% assign archives = site.pages | where_exp: "page", "page.path contains 'Archive/'" | where_exp: "page", "page.name == 'index.md'" | sort: "path" | reverse %}
{% for page in archives limit:1 %}
{% assign parts = page.path | split: '/' %}
- [{{ parts[3] }}]({{ page.url | relative_url }})
{% endfor %}

[過去の日次アーカイブを見る →](./Archive/)

---

## このサイトについて

毎日朝6:00（JST）に、国内5サイト＋海外7サイトのマーケティング系RSSを自動収集し、中小企業の現場で活かせる視点で深読みレポートを生成しています。

**情報源**: MarkeZine / AdverTimes / ITmedia マーケティング / PR TIMES / SMMLab / Social Media Examiner / Hootsuite / Buffer / Sprout Social / Search Engine Journal / Platformer / TechCrunch
