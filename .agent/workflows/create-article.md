---
description: 記事の自動生成フロー（検索・執筆・サムネイル）
---

# Article Creation Workflow
指定された日付とテーマに基づいて、Amazon PA-APIを使用した商品リサーチから記事執筆、サムネイル生成までを一貫して行います。
## 手順

1. **商品リサーチ**
   - 以下のコマンドを実行し、Amazonから商品情報を取得する。
   - `python3 05_script/search_amazon_products.py daily-gadget-22 "{テーマ}" > 05_script/temp_products.json`
   - 出力されたJSONファイルの中身を確認する。

2. **記事執筆**
   - **ファイルパス**: `/Users/shoheishimizu/Knowledge/note_daily_gadget/02_article/{YYYY-MM}/{YYYY-MM-DD}_{テーマ}.md`
     - `{YYYY-MM}`: 公開予定日の年月（例: 2026-02）
     - `{YYYY-MM-DD}`: 公開予定日の年月日（例: 2026-02-16）
     - `{テーマ}`: 記事タイトル（ファイル名として適切な形式に整形）
   - **フォーマット**: 参考記事のマークダウン構造を**完全に模倣**すること（タイトル → 導入3段落 → 商品セクション → 最後に → あわせて読みたい）。
   - **ルール適用**: `.agent/rules/note-writer.md` の全ルールを厳守。特にURL直下の商品名再記述は絶対禁止。
   - **重要**: URLは `05_script/temp_products.json` の `url` (アフィリエイトリンク) をそのまま使用する。
   - **metadata更新**: 
     - `02_article/{YYYY-MM}/_metadata.json` に追加するJSONブロックを、`filename`, `title`, `url`, `tags`, `category`, `published_date` の全必須項目を完全に網羅した形で出力し、ユーザーに提示する。
     - `url`は必ず空文字列 `""` にする。
     - `tags`はスペース区切りのテキストにする（例: `"tags": "ガジェット Anker オーディオ"`）。
     - `category` はファイル内の既存カテゴリを参考に必ず設定する（生成漏れ厳禁）。
   - **schedule更新**: `03_schedule/schedule_2026.md` の該当タイトルを `~~打ち消し線~~` で囲む。

3. **サムネイル生成**
   - [generete-thumbnail.md](cci:7://file:///Users/shoheishimizu/Knowledge/note-writer/.agent/rules/generete-thumbnail.md:0:0-0:0) のルールに従い、記事内容に合ったサムネイルを3枚生成する。
   - 生成した画像を `04_thumbnail` に保存する。

4. **後処理**
   - 一時ファイル `05_script/temp_products.json` を削除する。