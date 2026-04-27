#!/usr/bin/env python3
"""RSS記事収集スクリプト - GitHub Actionsから実行（マーケキャッチアップ版）"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser

JST = timezone(timedelta(hours=9))

# RSSフィードリスト（マーケ全般・中小企業向け）
FEEDS = [
    # 国内（マーケ・SNS運用）
    "https://markezine.jp/rss/new/20/index.xml",
    "https://www.advertimes.com/feed/",
    "https://rss.itmedia.co.jp/rss/2.0/marketing.xml",
    "https://prtimes.jp/index.rdf",
    "https://smmlab.jp/feed",
    # 海外（SNSマーケ・プラットフォーム動向）
    "https://www.socialmediaexaminer.com/feed/",
    "https://blog.hootsuite.com/feed/",
    "https://buffer.com/resources/feed/",
    "https://sproutsocial.com/insights/feed/",
    "https://www.searchenginejournal.com/feed/",
    "https://www.platformer.news/feed",
    "https://techcrunch.com/category/social/feed/",
]

NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rss1': 'http://purl.org/rss/1.0/',
}


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)

    def get_text(self):
        return ''.join(self.result).strip()


def strip_html(text):
    if not text:
        return ''
    stripper = HTMLStripper()
    try:
        stripper.feed(text)
        return stripper.get_text()
    except Exception:
        return re.sub(r'<[^>]+>', '', text).strip()


def fetch_full_text(url):
    """記事URLから本文を取得（リード文のみのサイト対策）"""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; RSSBot/1.0)'})
        with urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if article_match:
            return strip_html(article_match.group(1))[:3000]
        main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
        if main_match:
            return strip_html(main_match.group(1))[:3000]
    except Exception:
        pass
    return ''


def fetch_feed(url):
    """RSSフィードをHTTPで取得"""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; RSSBot/1.0)'})
        with urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except (URLError, Exception) as e:
        print(f"  → 取得失敗: {e}", file=sys.stderr)
        return ''


def parse_feed(content):
    """RSSフィードをパースして記事リストを返す"""
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return []

    items = []

    for item in root.findall('.//item'):
        title = _text(item, 'title')
        link = _text(item, 'link')
        desc = _text(item, 'description')
        body = _text(item, 'content:encoded', NS) or desc
        pub_date = _text(item, 'pubDate') or _text(item, 'dc:date', NS)
        if title and link:
            items.append((title, link, desc, body, pub_date))

    for item in root.findall('rss1:item', NS):
        title = _text(item, 'rss1:title', NS)
        link = _text(item, 'rss1:link', NS)
        desc = _text(item, 'rss1:description', NS)
        pub_date = _text(item, 'dc:date', NS)
        if title and link:
            items.append((title, link, desc, desc, pub_date))

    for entry in root.findall('atom:entry', NS):
        title = _text(entry, 'atom:title', NS)
        link_el = entry.find('atom:link', NS)
        link = link_el.get('href', '') if link_el is not None else ''
        desc = _text(entry, 'atom:summary', NS)
        body = _text(entry, 'atom:content', NS) or desc
        pub_date = _text(entry, 'atom:published', NS) or _text(entry, 'atom:updated', NS)
        if title and link:
            items.append((title, link, desc, body, pub_date))

    return items


def _text(el, tag, ns=None):
    """要素からテキストを安全に取得"""
    child = el.find(tag, ns) if ns else el.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return ''


def get_recent_urls(days=7):
    """直近N日分のArchive/とRaw/から収集済みURLを抽出して重複除外用セットを返す"""
    urls = set()
    today = datetime.now(JST).date()

    def extract_source(md_file):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                head = f.read(2000)
            m = re.search(r'^source:\s*"?([^"\n]+)"?', head, re.MULTILINE)
            if m:
                return m.group(1).strip().strip('"')
        except Exception:
            pass
        return None

    def scan_dir(path):
        if not os.path.isdir(path):
            return
        for fname in os.listdir(path):
            if fname.endswith(".md") and fname != "index.md":
                url = extract_source(os.path.join(path, fname))
                if url:
                    urls.add(url)

    scan_dir("Raw")

    for i in range(1, days + 1):
        d = today - timedelta(days=i)
        fiscal_year = d.year if d.month >= 4 else d.year - 1
        archive_dir = f"Archive/{fiscal_year}年度/{d.month}月/{d.year}.{d.month}.{d.day:02d}"
        scan_dir(archive_dir)

    return urls


def save_article(title, link, desc, body, pub_date, seen_urls):
    """記事をMarkdownファイルとして保存"""
    if link and link in seen_urls:
        return False, 'dup_url'

    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)[:80].strip()
    if not safe_title:
        return False, 'no_title'

    filepath = f"Raw/{safe_title}.md"
    if os.path.exists(filepath):
        return False, 'exists'

    clean_desc = strip_html(desc)[:500]
    clean_body = strip_html(body)[:3000]

    if len(clean_body) < 200 and link:
        full_text = fetch_full_text(link)
        if len(full_text) > len(clean_body):
            clean_body = full_text

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(f'title: "{title}"\n')
        f.write(f'source: "{link}"\n')
        f.write(f'published: {pub_date}\n')
        f.write("tags:\n  - clippings\n")
        f.write("---\n\n")
        f.write(clean_body if clean_body else clean_desc)
        f.write("\n")

    seen_urls.add(link)
    return True, 'saved'


def main():
    os.makedirs("Raw", exist_ok=True)

    today = datetime.now(JST).strftime("%Y-%m-%d")
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")

    with open("Raw/index.md", 'w', encoding='utf-8') as f:
        f.write(f"# RSS収集 {today}\n\n")
        f.write(f"収集日時: {now}\n\n")
        f.write("---\n\n")

    seen_urls = get_recent_urls(days=7)
    print(f"直近7日の既収集URL: {len(seen_urls)}件（重複除外対象）\n")

    total = 0
    dup_total = 0

    for feed_url in FEEDS:
        print(f"取得中: {feed_url}")
        content = fetch_feed(feed_url)
        if not content:
            continue

        items = parse_feed(content)
        count = 0
        dup_count = 0

        for title, link, desc, body, pub_date in items:
            saved, reason = save_article(title, link, desc, body, pub_date, seen_urls)
            if saved:
                with open("Raw/index.md", 'a', encoding='utf-8') as f:
                    clean_desc = strip_html(desc)[:200]
                    f.write(f"### {title}\n")
                    f.write(f"- URL: {link}\n")
                    f.write(f"- 概要: {clean_desc}\n\n")
                count += 1
            elif reason == 'dup_url':
                dup_count += 1

        total += count
        dup_total += dup_count
        print(f"  → {count}件保存（重複スキップ {dup_count}件）")

    with open("Raw/index.md", 'a', encoding='utf-8') as f:
        f.write("---\n")
        f.write(f"合計: {total} 件（直近7日と重複 {dup_total}件をスキップ）\n")

    print(f"\n合計記事数: {total}（重複スキップ合計: {dup_total}件）")


if __name__ == '__main__':
    main()
