# Codex 商品リサーチ指示書（毎日ガジェット通信）

> このファイルを Codex に渡すことで、毎回基準を説明する必要がなくなります。
> 使い方: 「このファイルの基準に従って、以下の記事リストの商品をリサーチしてください」と指示する。

---

## 参照先（重要）

このアカウントのリサーチ基準は2つのファイルに分かれている。**両方を必ず参照すること。**

1. **共通コア（骨格）**: `../../../shared/docs/research-guide-core.md`
   - 品質ティアの枠組み・多様性ルール・件数決定ルール・掲載順ルール・出力フォーマット・命名規則・QAスクリプトの実行手順など、全アカウント共通の手順を定義している
   - **注意**: このパスは親ワークスペース（`accounts/` と `shared/` が同じ階層に並ぶチェックアウト）で作業していることが前提。`accounts/daily_gadget` 単体（このsubmoduleリポジトリ単独）をcloneした環境では `shared/` が存在しないため、このファイルは開けない。作業は常に親ワークスペースルート（`/Users/shoheishimizu/Knowledge/note`）で行うこと
2. **アカウント固有の基準**: [PROFILE.md](../PROFILE.md) の「選定基準」章
   - ペルソナ・Amazonパートナータグ（`daily-gadget-22`）・カテゴリとマガジン誘導・多様性ルールの追加条件を定義している

---

## このアカウント固有の補足

- **アカウント名**: 毎日ガジェット通信（詳細は [PROFILE.md](../PROFILE.md) の「ペルソナ」章）
- **Amazonパートナータグ**: `daily-gadget-22`（`accounts/daily_gadget/account.json` の `amazon.partner_tag` と一致させる）
- **カテゴリとマガジン**: [PROFILE.md](../PROFILE.md) の「カテゴリとマガジン」章を参照。`_metadata.json` の `category` は必ずここで定義された5種類から選択する
- このアカウントは Amazon「アイデアリスト」等のマガジン誘導URLを運用している（`account.json` の `categories[].magazine_url` を参照。詳細は `.docs/amazon_idea_lists.json`）
- URL整合性チェック（保存前必須）・品質ティアの数値基準は `../../../shared/docs/research-guide-core.md` の既定値と一致しており、[PROFILE.md](../PROFILE.md) の「選定基準」章および `.agent/rules/note-researcher.md` にも同旨の記載がある。3ファイル間で数値が食い違った場合は PROFILE.md の記載を優先する
