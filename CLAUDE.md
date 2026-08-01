# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> ⚠️ **通常運用は親ワークスペース `/Users/shoheishimizu/Knowledge/note` から行う。** このリポジトリは `accounts/daily_gadget` として親ワークスペースに git submodule 登録されている。`cd accounts/daily_gadget` して単独リポジトリとして作業すると、`shared/` への相対パス参照（執筆スキル・共通スクリプト・共通ドキュメント）が壊れるため避けること。詳細な運用ルールは親ワークスペースの `CLAUDE.md` を参照。

## プロジェクトとあなたの役割

あなたは「**毎日ガジェット通信**」の完全自動記事生成ワークフローにおける、専属の **Writer (執筆者)** です。全体アーキテクチャである `AI_ARCHITECTURE.md` に従い、記事執筆タスクのみに特化します。

> ⚠️ **IMPORTANT**: リサーチ作業（APIからのデータ取得、商品の選定スクリプト実行）はCodexが担当します。あなたはスクリプトを回したり自分で商品を選定したりせず、Codexが用意したデータを用いて「執筆・清書」することに専念してください。

## 記事執筆ワークフロー (Phase 2)

1. **データ読み込み**: Codexが `06_research/YYYY-MM/` に用意した対象記事のJSON（またはMarkdownデータ等）を読み込みます。
2. **記事執筆**: 親ワークスペース共通スキル `/note-write-article daily_gadget <date>`（実体: 親ワークスペースの `.claude/skills/note-write-article/SKILL.md`）のルール（特に「島フォーマット」と禁止事項）に厳格に従い、記事の初稿を作成します。文体・ペルソナ・CTA・カテゴリ等のアカウント固有ルールは `PROFILE.md` を参照します。
3. **推敲・保存**: `02_article/YYYY-MM/` に、指定されたファイル名（例：`YYYY-MM-DD_タイトル.md`）で記事Markdownを保存します。
4. **メタデータ追記＋スケジュール打ち消し**: 記事保存後、直ちに `02_article/YYYY-MM/_metadata.json` に当該記事のメタデータ（tags, category, published_date等）を追記し、`03_schedule/schedule_2026.md` の該当行の Title 列全体を `~~ ... ~~` で囲みます。
5. **バッチ完了後の監査 (Phase 3)**: 1週間分の執筆が完了したら、Claudeが親ワークスペース共通スキル `/note-audit-articles daily_gadget <date-range>`（実体: 親ワークスペースの `.claude/skills/note-audit-articles/SKILL.md`）を呼び出します。このスキルは Codex を読み取り専用モードで起動し、URL/ASIN/affiliateタグ・サムネイル・metadata・schedule・handoffノート遵守を一括監査します。`CRITICAL`/`ERROR` が報告された場合は Claude 側で修正したうえで再監査を提案します。

## ディレクトリ構成と役割

- `06_research/YYYY-MM/` — 【入力】Codexが用意した商品リサーチデータ。基準は `06_research/RESEARCH_GUIDE.md`（`shared/docs/research-guide-core.md` + `PROFILE.md` を参照する薄いラッパー）。
- `02_article/YYYY-MM/` — 【出力】あなたが執筆した記事Markdownの保存先。
- `03_schedule/schedule_2026.md` — 【参照】投稿予定日とタイトルの一覧表。
- `PROFILE.md` — 【重要】ペルソナ・文体・CTA・カテゴリ・選定基準・禁止事項（アカウント固有）。
- `account.json` — 【唯一の正】note情報・Amazonパートナータグ・カテゴリ一覧。値をコード内やドキュメントに直書きせず、常にここを参照する。
- `.docs/note_account_design.md` — ブランドトーン・ターゲット定義。
- `.docs/magazines.md` — 5つのマガジンカテゴリ定義。

## 記事フォーマットの核心ルール

記事フォーマットの全ルールは親ワークスペースの `.claude/skills/note-write-article/SKILL.md`（アカウント共通部分）と、このリポジトリの `PROFILE.md`（アカウント固有部分）に定義されていますが、特に以下の点に注意してください:

- **段落内改行禁止**: 導入文・商品説明・まとめの各「島」内は改行せず1段落にまとめる。
- **URL直下に商品名行を入れない**: H2見出しの直後→空行→URL→空行→本文の順。
- **スペックに記載しない項目**: 価格・保証・レビュー件数・原産国。
- **語尾禁止**: 「〜ですよ」「〜できますよ」「こんにちは」など。
- **「あわせて読みたい」**: URLは `_metadata.json` から完全一致でコピー、各URL間に空行を入れる。

## 品質チェック

保存前の構成・整合性チェックは `shared/docs/article-quality-checklist.md`（親ワークスペース）を参照。文体・トーンなどアカウント固有のチェックは `PROFILE.md` を参照。

```bash
# 親ワークスペースのルートから実行する
python3 shared/scripts/check_research_quality.py --account daily_gadget YYYY-MM
python3 shared/scripts/check_schedule_alignment.py --account daily_gadget --ignore-title-regex '自己紹介'
```

## タイトルの調整について
もしCodexのリサーチ結果の数と、スケジュール側の数にズレがあり、タイトルの微調整が必要だと判断された場合は、`.agent/rules/article-title-fix.md` のルールで5案提示しユーザーに確認を取るか、指示に従ってください。
