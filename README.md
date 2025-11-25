# Note Writer

note向けガジェット紹介記事をAIで生成するためのスキル集と運用メモを管理するリポジトリです。

## ファイル構成
- `.claude/skills/SKILL.md`: Claudeに読み込ませるメインスキル。note記事作成の4フェーズワークフローを定義
- `.docs/note_account_design.md`: アカウント「毎日ガジェット便り」のブランド方針やコンテンツ運用メモ
- `.docs/product_search.md`: Amazon商品リサーチのガイドライン
- `.docs/magazines.md`: noteマガジン5カテゴリの定義
- `article/`: 公開済み・ドラフトのnote記事
- `article/_metadata.json`: 記事メタデータ管理

## 使い方
1. `.docs/note_account_design.md`でアカウントの方向性やトーンを確認
2. ご自身のテーマと商品情報を整理し、`SKILL.md`のPhase 0テンプレに沿ってClaudeへ入力
3. 出力されたnote記事ドラフトを加筆修正しつつ公開

## 補足
- 他のSNS（XやInstagramなど）に展開したい場合は、`SKILL.md`に追加ルールを追記して拡張してください。
