# Note Writer

note向けガジェット紹介記事をAIで効率的に生成・管理するためのリポジトリです。
「毎日ガジェット便り」のブランド指針に基づき、リサーチから執筆、サムネイル生成までの一連のワークフローを自動・半自動化しています。

## ディレクトリ構成

- `01_analytics/`: noteのアクセス解析やAmazonアソシエイトの収益データ・分析レポート。
- `02_article/`: 執筆した記事本文（Markdown）と管理用メタデータ（`_metadata.json`）。
- `03_schedule/`: 投稿予定の記事タイトルやスケジュールの管理。
- `04_thumbnail/`: 記事用にAIで生成したサムネイル画像。
- `.agent/rules/`: 各工程でAIが参照する指示書（スキルの定義）。
    - `note-writer.md`: メインの執筆ワークフロー。
    - `article-title-fix.md`: 読まれるタイトルの生成ルール。
    - `generete-thumbnail.md`: Codex imagegenによるサムネイル画像の生成指示。
    - `setup-drafts.md`: スケジュールからの下書き一括生成。
- `.docs/`: プロジェクトの基盤ドキュメント。
    - `note_account_design.md`: ブランド方針やトーン＆マナー。
    - `product_search.md`: 商品リサーチのガイドライン。
    - `magazines.md`: noteマガジンのカテゴリ定義。

## ワークフローの概要

1. **構成・リサーチ**: `.agent/rules/note-writer.md` に基づき、ターゲットと商品の選定を行います。
2. **執筆**: リサーチ結果を元に、ブランドトーンに合わせた記事を生成します。
3. **タイトル最適化**: `article-title-fix.md` を使い、クリック率を高めるタイトルを選定します。
4. **画像生成**: `generete-thumbnail.md` により、Codex imagegenで記事にマッチしたサムネイル画像を生成し、`04_thumbnail/YYYY-MM/` に保存します。
5. **管理**: `_metadata.json` を更新し、進捗や関連記事のリンクを管理します。
