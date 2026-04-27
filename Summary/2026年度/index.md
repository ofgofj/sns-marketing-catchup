---
layout: default
title: 深読みレポート 2026年度
---

# 深読みレポート 2026年度

{% assign reports = site.pages | where_exp: "page", "page.path contains 'Summary/2026年度/'" | where_exp: "page", "page.name != 'index.md'" | sort: "path" | reverse %}

{% for page in reports %}
{% assign parts = page.path | split: '/' %}
- [{{ parts.last | replace: '.md', '' }}]({{ page.url | relative_url }})
{% endfor %}

[← Summary一覧に戻る](../)
