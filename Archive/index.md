---
layout: default
title: 日次アーカイブ（Archive）
---

# 日次アーカイブ

毎日の収集記事を4層分類した日次素材です。深読みレポート（Summary）の元データになります。

{% assign archive_pages = site.pages | where_exp: "page", "page.path contains 'Archive/'" | where_exp: "page", "page.name == 'index.md'" | where_exp: "page", "page.path != 'Archive/index.md'" | sort: "path" | reverse %}

{% if archive_pages.size == 0 %}
まだアーカイブがありません。
{% else %}
{% for page in archive_pages %}
{% assign parts = page.path | split: '/' %}
- [{{ parts[3] | default: parts.last }}]({{ page.url | relative_url }})
{% endfor %}
{% endif %}

[← トップに戻る](../)
