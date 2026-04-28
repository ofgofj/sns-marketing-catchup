---
title: "Svelte × Tailwind CSSのRabee UI、サンプル4種類を追加。カラー定義もわかりやすく刷新しました"
source: "https://prtimes.jp/main/html/rd/p/000000026.000097622.html"
published: 2026-04-29T06:10:02+09:00
tags:
  - clippings
---

Svelte × Tailwind CSSのRabee UI、サンプル4種類を追加。カラー定義もわかりやすく刷新しましたカスタマイズを前提とした「UIコンポーネントの種」を提供中。Admin Layout、Authenticationなどを含む4種類のサンプルを新たに追加。カラー定義の命名も刷新しました。株式会社Rabee2026年4月28日 11時44分いいね！数を読み込み中です
株式会社Rabee（本社：東京都渋谷区、代表取締役：上松勇喜）は、Svelte × Tailwind CSSのUIコンポーネント集「Rabee UI」において、新規サンプルの追加、カラー定義の刷新などを行いました。今回のアップデートも含む全49種類のRabee UIコンポーネントは、以下から確認できます。

Rabee UI 公式ドキュメント
■ Rabee UIとは
Rabee UIとは、SvelteとTailwind CSSで構築されたUIコンポーネント集であり、カスタマイズして使うことを前提とした「コンポーネントの種」です。プロダクトごとに色やフォント、アニメーションなどを自由にカスタマイズすることで、ブランドらしさを表現するデザインシステムを小さいコストで構築できます。

■Rabee UIの特徴
・Svelte × Tailwind CSSで柔軟にカスタマイズできる
・コンポーネント単位でコピー＆ペーストして導入できる
・ダークモード・ライトモードに対応
・日本語利用を前提としたデザイン
・コードと一致したFigmaデータも公開中


■ 管理画面・SaaSの構築に役立つサンプル4種類を新たに追加
Rabee UIは2025年5月のドキュメントページ公開以後、毎月のアップデートを継続しています。今月は「Admin Layout」「Authentication」「Error Layout」「Header Snippet」の4種類のサンプルを新たに追加しました。いずれも、プロダクト開発で頻出するページの構築をサポートするためのサンプルです。

Admin Layoutは、サイドバーとヘッダーを含む一般的な管理画面のレイアウト例です。Authenticationは、サインイン・サインアップに必要な画面を揃えた例です。Error Layoutは、404（ページが存在しない）や500（サーバーエラー）といったエラー画面の例です。Header Snippetは、Webサービスで使いやすいヘッダーの例です。


Admin Layout https://rabeeui.com/docs/samples/adminlayout


Authentication https://rabeeui.com/docs/samples/authentication


Error Layout https://rabeeui.com/docs/samples/errorlayout


Header Snippet https://rabeeui.com/docs/samples/header


サンプル / Admin Layout, Header Snippet
サンプル / Authentication, Error Layout
■ 既存コンポーネントの「Badge」「Dialog」を「Chip」「Modal」にリニューアル
既存コンポーネントのうち2種をより実務で使いやすいようにアップデートしました。
Badgeを「Chip」にアップデート
これまで「Badge」として提供していたコンポーネントを「Chip」に名称を変更し、色と見た目の種類を拡充しました。ステータス表示やタグ表示などの用途にあわせて、デザインを柔軟に選べるようになりました。


Chip https://rabeeui.com/docs/components/chip


コンポーネント / Chip
Dialogを「Modal」にアップデート
これまで「Dialog」として提供していたコンポーネントを「Modal」に名称を変更し、設計を見直しました。これまでのDialogは、モーダル機能とダイアログ表示機能を1つのコンポーネントで提供していました。新しいModalは、コンポーネントの機能を「モーダルとして表示する」のみに絞り、モーダル上に表示するコンテンツは自由に変えられる設計です。これにより、用途を問わずさまざまなモーダルに使えるようになりました。


Modal https://rabeeui.com/docs/components/modal


コンポーネント / Modal
■ カラー定義を全面的に刷新
Rabee UIが提供しているカラー変数の命名を全面的に刷新しました。用途や階層が明確になるよう整理し、コード上でも目的の変数を見つけやすくなりました。あわせて、Input系のコンポーネントのボーダーの色や、キーボード操作時に表示するフォーカスのリングの色も新たに追加しました。新しいCSSの内容は、以下のドキュメントで確認できます。

Rabee UI セットアップの手順
https://rabeeui.com/docs/setup

Rabee UI カラー定義について
https://rabeeui.com/docs/colors

既にRabee UIを導入済みのプロダクトにおけるカラー定義の更新方法は、移行ガイドでご確認ください。

Rabee UI カラー定義の移行ガイド
https://rabeeui.com/docs/migration/colors
■ 全コンポーネントに data-rabee-ui 属性を付与
Rabee UIの全UIコンポーネントに data-rabee-ui 属性を付与しました。属性の値にはコンポーネント名が入っており、たとえばボタンコンポーネントは以下のようにレンダリングされます。

これにより、プロダクトに含まれるRabee UIコンポーネントをJavaScriptから検知できるようになりました。

ページ内でRabee UIが使われている箇所を一覧で把握できるため、Rabee UIを使っていない部分を見つけて置き換える作業もスムーズになります。
■ 今後の展望
私たちは今後も、Rabee UIの改善を継続して行います。実務で活用しながらアップデートを重ねることで、Rabee UIを単なるUIコンポーネント集ではなく、あらゆるプロダクト開発の基盤として強化していきます。

Rabee UI 公式ドキュメント
https://rabeeui.com/docs/components

■ Rabee UIの最新情報
Rabee UIに関する最新情報は以下で公開しています。

Rabee UI 公式ドキュメント
https://rabeeui.com/docs

Rabee UI Figma
https://www.figma.com/community/file/1479376628733075423

Rabee UI Discordコミュニティ
https://discord.com/invi
