# 毎日ガジェット通信

note向けガジェット紹介記事をAIで効率的に生成・管理するためのリポジトリです。
「毎日ガジェット通信」のブランド指針に基づき、リサーチから執筆、サムネイル生成までの一連のワークフローを自動・半自動化しています。

> ⚠️ **通常運用は親ワークスペース `/Users/shoheishimizu/Knowledge/note` から行います。** このリポジトリは `accounts/daily_gadget` として親ワークスペースに git submodule 登録されています。単独でこのディレクトリに `cd` して作業すると、共通スキル・共通スクリプト（`shared/`）への相対パス参照が壊れるため、常に親ワークスペースのルートで作業してください。詳細は親ワークスペースの `CLAUDE.md` を参照してください。

## ディレクトリ構成

- `00_knowledge/`: アカウント設計・戦略・ナレッジベース（サブモジュール）。
- `01_analytics/`: noteのアクセス解析やAmazonアソシエイトの収益データ・分析レポート。
- `02_article/`: 執筆した記事本文（Markdown）と管理用メタデータ（`_metadata.json`）。
- `03_schedule/`: 投稿予定の記事タイトルやスケジュールの管理。
- `04_thumbnail/`: 記事用にCodex imagegenで生成したサムネイル画像。
- `05_script/`: 旧・アカウント専用スクリプト置き場。現行の共通スクリプトは親ワークスペースの `shared/scripts/` に移行済み（詳細は `05_script/README.md`）。`legacy/` 配下は過去の一回性バッチスクリプト。
- `06_research/`: Codexが用意した商品リサーチデータ（`RESEARCH_GUIDE.md` に選定基準の参照先をまとめている）。
- `PROFILE.md`: ペルソナ・文体・CTA・カテゴリ・選定基準・禁止事項（アカウント固有）。
- `account.json`: note情報・Amazonパートナータグ・カテゴリ一覧（唯一の正）。
- `.agent/rules/`: 各工程でAIが参照する補助指示書。
    - `note-researcher.md`: リサーチ選定基準（Codex向け）。
    - `article-title-fix.md`: 読まれるタイトルの生成ルール。
- `.agent/skills/generete-thumbnail/`: Codex imagegenによるサムネイル画像の生成指示。
- `.docs/`: プロジェクトの基盤ドキュメント。
    - `note_account_design.md`: ブランド方針やトーン＆マナー。
    - `product_search.md`: 商品リサーチのガイドライン。
    - `magazines.md`: noteマガジンのカテゴリ定義。

## ワークフローの概要

1. **リサーチ（Codex担当）**: `06_research/RESEARCH_GUIDE.md`（`shared/docs/research-guide-core.md` + `PROFILE.md`）の基準に基づき、`06_research/` に商品データを保存します。
2. **執筆（Claude Code担当）**: 親ワークスペース共通スキル `/note-write-article daily_gadget <date>` を使い、ブランドトーンに合わせた記事を生成します。
3. **タイトル最適化**: `.agent/rules/article-title-fix.md` を使い、クリック率を高めるタイトルを選定します。
4. **画像生成（Codex担当）**: `.agent/skills/generete-thumbnail/SKILL.md` により、記事にマッチしたサムネイル画像を生成し、`04_thumbnail/YYYY-MM/` に保存します。
5. **管理**: `_metadata.json` と `03_schedule/schedule_2026.md` を更新し、進捗や関連記事のリンクを管理します。
6. **監査**: 1週間分の執筆完了後、親ワークスペース共通スキル `/note-audit-articles daily_gadget <date-range>` でCodexに品質監査を委譲します。
