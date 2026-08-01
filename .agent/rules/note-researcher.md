---
trigger: model_decision
description: 記事構成のためのAmazon商品リサーチ・選定ルール（3段階フロー）
---

# Note Article Researcher (Codex)

## **説明**:
このルールは、Codexがスケジュールに基づき記事に載せる商品をリサーチするための指針です。
**選定判断そのものはスクリプトが機械的に行います。** Codexの担当は「クエリ設計」と「推しポイントの記入」です。

## 🎯 前提条件 (Workflow)

- リサーチとデータ準備は **Codex** の責務です。
- 作業は必ず親ワークスペースのルート（`/Users/shoheishimizu/Knowledge/note`）から行ってください。
- **選定基準の実体は共通コア `shared/docs/research-guide-core.md` にあります。** Tier基準の数値・多様性・件数決定・掲載順・URL整合性ゲートはすべてそこで一元管理されており、`select_products.py` が機械実行します。このファイルに数値を再掲しません。
- アカウント固有の条件は [PROFILE.md](../../PROFILE.md) の「選定基準」章を参照してください。

---

## Phase 1: 3段階フローの実行

### Stage 1: 候補収集

```bash
python3 shared/scripts/search_amazon_creators.py --account daily_gadget --mode pool \
    --item-count 10 "クエリ1" "クエリ2" "クエリ3" --out <候補プールJSONのパス>
```

- **クエリはジャンル・用途のキーワードで書く**（例: 「モバイルバッテリー 大容量 防災」）
- **商品名の直指定は禁止**（例: 「Anker PowerCore 10000」）。候補プールが実質1件になり、選抜が成立しなくなります
- 目標候補数は最終採用数の4〜6倍を目安にする

### Stage 2 + 3: 実測と機械選抜

```bash
python3 shared/scripts/select_products.py --account daily_gadget \
    --candidates <候補プールJSONのパス> \
    --date YYYY-MM-DD --title "スケジュール上のタイトル" --refresh-reviews
```

- `--refresh-reviews` は必須。**Amazon Creators API はレビュー件数・星評価をほぼ返さない**（実測で確認済み）ため、商品ページからの実測なしにはTier判定が一切できません
- レビューデータを取得できなかった商品は自動的に除外されます（推測値の使用は禁止）
- 件数はタイトルの「◯選」から自動で読み取られます。明示指定する場合のみ `--count N`
- 選抜結果を確認したいだけのときは `--dry-run` を付けてください

### 件数が揃わなかった場合

Tier1〜3 まで緩和しても規定件数に届かない場合、スクリプトはダミーを挿入せず **エラー終了します**。そのときは以下のいずれかで対応してください。

1. クエリを追加・言い換えて候補プールを広げ、Stage 1 からやり直す（**推奨**）
2. それでも足りなければ `03_schedule/schedule_2026.md` の対象タイトルの「◯選」を実際の件数に更新し、オーナーへ報告する

---

## Phase 2: 推しポイントの記入（Codexの担当）

`select_products.py` が出力したMarkdownの「推しポイント（3点）」は `※Codexが記入` のプレースホルダになっています。ここを [PROFILE.md](../../PROFILE.md) の「ペルソナ」章に沿って埋めるのがCodexの仕事です。

> [!CAUTION]
> **商品の選定・順序・件数を手で変えないでください。** スクリプトが多様性・掲載順・URL整合性を検証した結果なので、手で編集するとQAと整合しなくなります。変更が必要な場合は候補プールを広げて Stage 1 からやり直してください。

---

## 出力と保存先

- **保存先**: `06_research/YYYY-MM/YYYY-MM-DD_{タイトル}.md`（`select_products.py` が自動で決定）
- **形式はMarkdown**。gadget_ol と共通の書式です
- 過去の `*_research_data.json` は旧フローの履歴として残してあります。**変換せず、参照もしないでください**（レビューデータを持たないため現行の品質基準を満たしません）

---

## URL整合性チェック

共通コア `shared/docs/research-guide-core.md` の「URL整合性ゲート」に一本化されており、`select_products.py` が保存前に全件検査します（形式・ASIN一致・パートナータグ一致）。1件でも不合格なら書き出しを中止します。

このアカウントのパートナータグは `daily-gadget-22`（正は `account.json` の `amazon.partner_tag`）。URLを手入力・記憶・推測で作成しないでください。
