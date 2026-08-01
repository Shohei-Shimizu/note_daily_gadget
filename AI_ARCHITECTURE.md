# AI_ARCHITECTURE (毎日ガジェット通信 完全自動記事生成ワークフロー)

このドキュメントは、「毎日ガジェット通信」の完全自動記事生成ワークフローにおける、各AIエージェントの役割と連係フローを定義する**マスター構想ファイル**です。全AIエージェントはこの規定に従って動作してください。

## 概要: 3層のAIエージェント体制

本プロジェクトは以下3つのAIエージェントで運用されます。

1.  **Antigravity (アングラ) - Director / Planner**
    *   **役割**: 人間（USER）の秘書・相談役、システムとインフラの全体構築・保全
    *   **責務**: 要件定義、全体戦略の相談、軽微なファイル作成/設定変更、他のAIが生み出した内容の要約・レビュー報告
    *   **モード**: PLANNING優先（実装より設計、勝手に仕様を変えない）
2.  **Claude Code - Worker / Writer**
    *   **役割**: 専属の「記事執筆者・ライター」
    *   **責務**: 大量のテキスト生成、複雑な機能実装（執筆・リライトメイン）
    *   **参照元**: `CLAUDE.md`、親ワークスペースの `.claude/skills/note-write-article/SKILL.md`、`PROFILE.md`
    *   **制限事項**: 自身で商品選定やリサーチ（スクリプト実行）は行わず、**提供済みのデータ（`06_research` フォルダの内容）に基づき**執筆に専念する。
3.  **Codex (Cursor) - Supervisor / Researcher & Checker**
    *   **役割**: 商品リサーチ（スクリプト実行）、および記事の品質監査（最終チェック・修正）
    *   **責務**: 指定されたスケジュールに基づき候補プールを収集し、機械選抜スクリプトを実行して商品リストを確定。生成されたMarkdownの「推しポイント」を記入。執筆完了後、ルール違反がないかレビューし必要なら修正。**商品の選定判断そのものはスクリプトが機械的に行う。**
    *   **参照元**: `AGENTS.md` および `.agent/rules/note-researcher.md`

---

## 完全自動記事生成フロー (Scheduler-Driven)

各エージェントはデスクトップアプリのスケジューラーから呼び出される前提で動きます。

### Phase 1: リサーチ & データ準備 (担当: Codex)
1.  **スケジュール確認**: `03_schedule/schedule_2026.md` から本日または指定日の執筆予定タイトル・テーマを読み取る。
2.  **Stage 1 候補収集**: 親ワークスペースルートから `shared/scripts/search_amazon_creators.py --account daily_gadget --mode pool` を実行し、候補プールを集める。**クエリはジャンル・用途のキーワードで書く**（商品名の直指定は候補プールが1件になるため禁止）。目標は最終採用数の4〜6倍。
3.  **Stage 2+3 実測と機械選抜**: `shared/scripts/select_products.py --account daily_gadget --refresh-reviews` を実行。レビュー件数・星評価・在庫を商品ページから実測し、Tier判定・メーカー重複・掲載順・件数決定・URL整合性ゲートを機械適用して `06_research/YYYY-MM/YYYY-MM-DD_{タイトル}.md` を出力する。
    *   **Amazon Creators API はレビューデータをほぼ返さないため、実測ステップは必須**（省略するとTier判定が成立しない）。
    *   件数が揃わない場合スクリプトはダミーを挿入せずエラー終了する。候補プールを広げて Stage 1 からやり直すか、スケジュール側のタイトルの「◯選」を実件数に合わせる。
4.  **Stage 4 推しポイント記入**: 出力Markdownの `※Codexが記入` プレースホルダを `PROFILE.md` のペルソナに沿って埋める。**商品の選定・順序・件数は手で変えない**（QAと整合しなくなるため）。
    *   ※旧フローの `*_research_data.json` は履歴として残置。参照しない。

### Phase 2: 記事執筆 (担当: Claude Code)
1.  **データ読み込み**: Codexが準備した `06_research/YYYY-MM/` 内の該当リサーチデータを自動で読み込む。
2.  **執筆実行**: 親ワークスペースの `.claude/skills/note-write-article/SKILL.md` と `PROFILE.md` に規定された厳格なフォーマット（「島」形式、改行禁止ルール等）で原稿を作成する。
    *   ※Claude Codeは検索・選抜スクリプトを回さず、すでにある `06_research` のMarkdownを使うこと。
3.  **ドラフト保存**: 完成した原稿をMarkdown形式で `02_article/YYYY-MM/` 配下に保存する。

### Phase 3: 品質監査 & メタデータ更新 (担当: Codex)
1.  **記事レビュー**: Claude Codeが作成した `02_article/YYYY-MM/` 側のMarkdownファイルを読み込み、親ワークスペースの `.claude/skills/note-write-article/SKILL.md` と `PROFILE.md` の禁止事項やトーン規定に違反していないかチェックする。
    *   例: 「〜ですよ」という表現がないか？ 不要な商品名行が入っていないか？
2.  **自動修正**: 逸脱があれば即座に修正（Rewrite）して保存する。
3.  **完了処理**:
    *   `03_schedule/schedule_2026.md` の該当行を `~~打ち消し線~~` で処理。
    *   `02_article/_metadata.json` に記事情報を追加する。

---

## ディレクトリと役割の対応表

| パス | 種別 | 担当 (参照者) | 用途 |
| :--- | :--- | :--- | :--- |
| `02_article/` | 出力先 | Claude Code (Write) / Codex (Check) | 執筆後の最終記事Markdown。 |
| `03_schedule/` | 入力元 | Codex / Claude Code | 投稿スケジュールと仮タイトル。 |
| `05_script/` | ツール | Codex (主に実行) | 旧アカウント専用スクリプト置き場。現行の共通スクリプトは親ワークスペースの `shared/scripts/` に移行済み（`--account daily_gadget` で実行）。`legacy/` は過去の一回性バッチ。 |
| `06_research/` | 中間 | Codex (Write) / Claude (Read) | Phase1でリサーチし確定させた商品データ(JSON等)置き場。 |
| `AGENTS.md` | 設定 | Codex | Codex（リサーチャー兼監査役）のアイデンティティと責務定義。 |
| `CLAUDE.md` | 設定 | Claude Code | 執筆特化ライターとしての責務定義。 |
| `AI_ARCHITECTURE.md` | 構想 | 全員共通 (Antigravity管理) | 全体フローのルールブック（現ファイル）。 |
