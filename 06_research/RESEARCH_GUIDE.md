# Codex 商品リサーチ指示書（毎日ガジェット通信）

> このファイルを Codex に渡すことで、毎回基準を説明する必要がなくなります。
> 使い方: 「このファイルの基準に従って、以下の記事リストの商品をリサーチしてください」と指示する。

---

## 参照先（重要）

このアカウントのリサーチ基準は2つのファイルに分かれている。**両方を必ず参照すること。**

1. **共通コア（骨格・3段階フロー）**: `../../../shared/docs/research-guide-core.md`
   - 3段階リサーチフロー（Stage 1 候補収集 → Stage 2 実測 → Stage 3 機械選抜 → Stage 4 推しポイント仕上げ）・品質ティアの枠組み・多様性ルール・件数決定ルール・掲載順ルール・URL整合性ゲート・出力フォーマット・命名規則・QAスクリプトの実行手順など、全アカウント共通の手順を定義している
   - **注意**: このパスは親ワークスペース（`accounts/` と `shared/` が同じ階層に並ぶチェックアウト）で作業していることが前提。`accounts/daily_gadget` 単体（このsubmoduleリポジトリ単独）をcloneした環境では `shared/` が存在しないため、このファイルは開けない。作業は常に親ワークスペースルート（`/Users/shoheishimizu/Knowledge/note`）で行うこと
2. **アカウント固有の基準**: [PROFILE.md](../PROFILE.md) の「選定基準」章
   - ペルソナ・Amazonパートナータグ（`daily-gadget-22`）・カテゴリとマガジン誘導・多様性ルールの追加条件を定義している

---

## 実行コマンド例（3段階フロー）

親ワークスペースルート（`/Users/shoheishimizu/Knowledge/note`）から実行する。

```bash
# Stage 1: 候補収集（ジャンル・用途キーワードでクエリを書く。商品名の直指定は禁止）
python3 shared/scripts/search_amazon_creators.py --account daily_gadget \
  "モバイルバッテリー 軽量 大容量" "モバイルバッテリー PD対応" \
  --item-count 10 --label mobile_battery_0825

# Stage 2 + 3: 実測 + 機械選抜（まず --dry-run でレポート確認）
python3 shared/scripts/select_products.py --account daily_gadget \
  --candidates accounts/daily_gadget/06_research/_candidates/mobile_battery_0825.json \
  --date 2026-08-25 --title "毎日を軽くする。モバイルバッテリー6選" \
  --refresh-reviews --dry-run

# 問題なければ --dry-run を外して本番書き出し
python3 shared/scripts/select_products.py --account daily_gadget \
  --candidates accounts/daily_gadget/06_research/_candidates/mobile_battery_0825.json \
  --date 2026-08-25 --title "毎日を軽くする。モバイルバッテリー6選" \
  --refresh-reviews
```

Stage 4（推しポイントの仕上げ）は出力されたMarkdown内の `※Codexが記入` をペルソナに沿って手動で埋める。商品の選定・順序・件数は変更しない。

---

## このアカウント固有の補足

- **アカウント名**: 毎日ガジェット通信（詳細は [PROFILE.md](../PROFILE.md) の「ペルソナ」章）
- **Amazonパートナータグ**: `daily-gadget-22`（`accounts/daily_gadget/account.json` の `amazon.partner_tag` と一致させる）
- **カテゴリとマガジン**: [PROFILE.md](../PROFILE.md) の「カテゴリとマガジン」章を参照。`_metadata.json` の `category` は必ずここで定義された5種類から選択する
- このアカウントは Amazon「アイデアリスト」等のマガジン誘導URLを運用している（`account.json` の `categories[].magazine_url` を参照。詳細は `.docs/amazon_idea_lists.json`）
- URL整合性ゲート（保存前必須・`select_products.py` が機械実行）・品質ティアの数値基準は `../../../shared/docs/research-guide-core.md` の既定値と一致しており、[PROFILE.md](../PROFILE.md) の「選定基準」章にも同旨の記載がある。数値が食い違った場合は PROFILE.md の記載を優先する
- **新規リサーチの出力形式はMarkdownに統一**する（`select_products.py` の出力形式。旧アカウント個別スクリプト時代のJSON保存は行わない）
- **過去のJSONファイル**（`06_research/*/*_research_data.json`、2026年3〜7月分など）は履歴として残っている。レビューデータを持たないものが大半のため、変換はしない（変換してもQAを通らない）
