---
layout: default
title: 過去の深読みレポート（Summary）
---

# 過去の深読みレポート

中小企業のマーケティング担当者向けに、毎日のマーケ・SNS運用情報を深読みしたレポート集です。

{% assign summary_pages = site.pages | where_exp: "page", "page.path contains 'Summary/'" | where_exp: "page", "page.name != 'index.md'" | sort: "path" | reverse %}

{% if summary_pages.size == 0 %}
まだレポートがありません。
{% else %}
{% for page in summary_pages %}
{% assign parts = page.path | split: '/' %}
- [{{ page.title | default: parts.last }}]({{ page.url | relative_url }})
{% endfor %}
{% endif %}

[← トップに戻る](../)
