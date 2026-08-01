# 05_script

共通スクリプトは親ワークスペース `shared/scripts/` へ移行済みです。**親ワークスペースのルート（`/Users/shoheishimizu/Knowledge/note`）から `--account daily_gadget` を付けて実行**してください。このリポジトリ単独（`accounts/daily_gadget` 内）で実行すると `shared/` への相対パスが解決できません。

```bash
# 商品リサーチ（PA-API）
python3 shared/scripts/search_custom_list.py --account daily_gadget

# 商品リサーチ（Amazon Creators API）
python3 shared/scripts/search_amazon_creators.py --account daily_gadget "テーマ"

# レビュー件数・星評価・在庫状態の一括取得/更新
python3 shared/scripts/fetch_amazon_reviews.py --asin B0XXXXXXXX
python3 shared/scripts/refresh_research_reviews.py --account daily_gadget --month 2026-08 --fail-on-oos

# リサーチ品質QA
python3 shared/scripts/check_research_quality.py --account daily_gadget 2026-08

# リサーチと記事の整合性チェック
python3 shared/scripts/check_schedule_alignment.py --account daily_gadget --ignore-title-regex '自己紹介'

# note入稿の下ごしらえ
python3 shared/scripts/note_publish_prepare.py --account daily_gadget 2026-08-05
```

詳細は親ワークスペースの `CLAUDE.md`・`shared/docs/research-guide-core.md`・`shared/docs/article-quality-checklist.md`・`shared/docs/note-publish-playbook.md` を参照してください。

## legacy/

`legacy/` 配下のスクリプトは過去の一回性バッチ処理（特定週・特定月のリサーチ/記事生成をまとめて実行するために書かれたワンオフスクリプト）です。現行の日常運用では使用しません。参考資料として残置しています。
