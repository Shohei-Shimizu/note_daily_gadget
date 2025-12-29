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
   - `02_article/YYYY-MM-DD_{テーマ}.md` を作成する。
   - `05_script/temp_products.json` の情報を使用して、[note-writer.md](cci:7://file:///Users/shoheishimizu/Knowledge/note-writer/.agent/rules/note-writer.md:0:0-0:0) のルールに従い記事を執筆する。
   - **重要**: URLはJSONにある `url` (アフィリエイトリンク) をそのまま使用する。
   - [_metadata.json](cci:7://file:///Users/shoheishimizu/Knowledge/note-writer/02_article/_metadata.json:0:0-0:0) と [schedule_2026.md](cci:7://file:///Users/shoheishimizu/Knowledge/note-writer/03_schedule/schedule_2026.md:0:0-0:0) を更新する。
3. **サムネイル生成**
   - [generete-thumbnail.md](cci:7://file:///Users/shoheishimizu/Knowledge/note-writer/.agent/rules/generete-thumbnail.md:0:0-0:0) のルールに従い、記事内容に合ったサムネイルを3枚生成する。
   - 生成した画像を `04_thumbnail` に保存する。
4. **後処理**
   - 一時ファイル `05_script/temp_products.json` を削除する。