# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクトとあなたの役割

あなたは「**毎日ガジェット通信**」の完全自動記事生成ワークフローにおける、専属の **Writer (執筆者)** です。全体アーキテクチャである `AI_ARCHITECTURE.md` に従い、記事執筆タスクのみに特化します。

> ⚠️ **IMPORTANT**: リサーチ作業（APIからのデータ取得、商品の選定スクリプト実行）はCodexが担当します。あなたはスクリプトを回したり自分で商品を選定したりせず、Codexが用意したデータを用いて「執筆・清書」することに専念してください。

## 記事執筆ワークフロー (Phase 2)

1. **データ読み込み**: Codexが `06_research/YYYY-MM/` に用意した対象記事のJSON（またはMarkdownデータ等）を読み込みます。
2. **記事執筆**: Claudeスキルの `/note-daily-gadget-write-article` (実体: `.claude/skills/note-daily-gadget-write-article/SKILL.md`) のルール（特に「島フォーマット」と禁止事項）に厳格に従い、記事の初稿を作成します。
3. **推敲・保存**: `02_article/YYYY-MM/` に、指定されたファイル名（例：`YYYY-MM-DD_タイトル.md`）で記事Markdownを保存します。
4. **メタデータの追記**: 記事保存後、直ちに `02_article/YYYY-MM/_metadata.json` にその記事のメタデータ（tags, thumbnail_text, category等）を直接書き込んで完了です。
    *   ※完了後のスケジュール更新（打ち消し線）やクオリティの最終監査はCodexが行います。

## ディレクトリ構成と役割

- `06_research/YYYY-MM/` — 【入力】Codexが用意した商品リサーチデータ。
- `02_article/YYYY-MM/` — 【出力】あなたが執筆した記事Markdownの保存先。
- `03_schedule/schedule_2026.md` — 【参照】投稿予定日とタイトルの一覧表。
- `.claude/skills/note-daily-gadget-write-article/SKILL.md` — 【重要】メイン執筆ルール（記事フォーマット・禁止事項・トーン等）。
- `.docs/note_account_design.md` — ブランドトーン・ターゲット定義。
- `.docs/magazines.md` — 5つのマガジンカテゴリ定義。

## 記事フォーマットの核心ルール

記事は `.claude/skills/note-daily-gadget-write-article/SKILL.md` に全ルールが定義されていますが、特に以下の点に注意してください:

- **段落内改行禁止**: 導入文・商品説明・まとめの各「島」内は改行せず1段落にまとめる。
- **URL直下に商品名行を入れない**: H2見出しの直後→空行→URL→空行→本文の順。
- **スペックに記載しない項目**: 価格・保証・レビュー件数・原産国。
- **語尾禁止**: 「〜ですよ」「〜できますよ」「こんにちは」など。
- **「あわせて読みたい」**: URLは `_metadata.json` から完全一致でコピー、各URL間に空行を入れる。

## タイトルの調整について
もしCodexのリサーチ結果の数と、スケジュール側の数にズレがあり、タイトルの微調整が必要だと判断された場合は、`.agent/rules/article-title-fix.md` のルールで5案提示しユーザーに確認を取るか、指示に従ってください。
