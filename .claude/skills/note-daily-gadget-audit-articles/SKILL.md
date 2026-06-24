---
name: note-daily-gadget-audit-articles
description: 毎日ガジェット通信の記事バッチ（通常1週間分）の品質をCodexに監査させるスキル。URL/ASIN/affiliateタグの整合性、サムネイル、metadata、scheduleの打ち消し線、handoffノート遵守を読み取り専用でチェックし、レポートを返す。/note-daily-gadget-audit-articles で呼び出す。
---

# Note Daily Gadget — Article Batch Audit (Codex Delegation)

## **説明**: 1週間分の記事執筆が完了したら、Codex（読み取り専用）に監査を委譲してレポートを取得するスキル。URL/サムネ/metadata/schedule の機械的整合性と handoff ノート遵守を確認する。

## 🎯 想定ユースケース

-   **`note-daily-gadget-write-article` スキルで 1 週間バッチ（通常 7 日分）の執筆が完了した直後**に、Claude が自動で呼び出す。
-   ユーザーが手動で `/note-daily-gadget-audit-articles 2026-07-15..2026-07-21` のように日付範囲指定して呼ぶことも可能。

## 🛡️ Core Principle: 役割分担

-   **Codex は読み取り専用の監査者**。コードや記事ファイルを書き換えない。問題を検出してレポートを返すのみ。
-   **修正は Claude（執筆者）が行う**。記事の文体や構造を理解しているのは執筆者なので、prose の一貫性を保ったまま反映する。

---

## 監査フロー

### Step 1: 監査対象範囲の確定

スキル呼び出し時の引数から日付範囲を取得する：

-   引数あり（例: `2026-07-15..2026-07-21` または `2026-07-15..21`）→ その範囲を使う。
-   引数なし → 直前に書いた記事の日付範囲を会話文脈から特定して使う。不明なら `02_article/YYYY-MM/_metadata.json` の末尾 N 件から推定する。

### Step 2: Codex 監査プロンプトの組み立て

下記の **「Codex 監査プロンプトテンプレート」** に対象日付・対象ファイルパスを埋め込んで完成させる。範囲が複数月をまたぐ場合は対象ファイルパスを月ごとに列挙する。

### Step 3: Codex への委譲（Agent ツール）

`Agent` ツールを `subagent_type: "codex:codex-rescue"` で 1 回だけ呼ぶ。プロンプトには Step 2 で組み立てた監査依頼テキストをそのまま渡す。

**重要な呼び出しルール**:

-   `--effort medium` を指定（バッチ監査には適度な深さが必要）。
-   `--fresh` を付ける（前のセッションを引き継がず、新規スレッドで監査）。
-   `--write` フラグは絶対に付けない（Codex 側で `--write` 既定だが、プロンプト本文で「**read-only audit. Do NOT modify any files. Report only.**」と強く指示する）。
-   モデル指定は省略（Codex デフォルトを使う）。

### Step 4: Codex レポートの受領と確認

Codex から返ってきたレポート（stdout 全体）を **そのまま** ユーザーに表示する。装飾・要約・解釈を加えない。

### Step 5: 問題があれば Claude が修正

レポートで指摘された問題のうち以下は **Claude が即時修正** する：

-   URL の affiliate タグ抜け・ASIN 不一致
-   schedule_2026.md の打ち消し線漏れ
-   `_metadata.json` の必須フィールド欠落（filename / title / category / published_date）
-   見出し直下の「商品名:〜」「💡注目ポイント」行などフォーマット違反
-   禁止語句（〜ですよ／こんにちは／比喩表現）の混入
-   handoff ノートで指示された "model-specific" 但し書きの欠落

prose の改善提案（言い回しの自然さ、説得力など）は **ユーザーに判断を仰ぐ**。

修正後に再監査が必要そうな場合のみ、Step 3 を 1 回だけ再実行する。

---

## Codex 監査プロンプトテンプレート

下記をそのまま組み立てて Codex に渡す。`{{...}}` の部分は実値で埋める。

```text
# Article batch audit — read-only

Repository: /Users/shoheishimizu/Knowledge/note_daily_gadget
Audit scope: articles from {{START_DATE}} to {{END_DATE}} ({{ARTICLE_COUNT}} articles)

**This is a read-only audit. Do NOT modify any files. Report findings only.**

## Files to audit

Articles ({{ARTICLE_COUNT}} markdown files):
{{ARTICLE_FILE_PATHS}}

Sources to cross-reference:
- Research JSONs: 06_research/{{YYYY-MM}}/2026-MM-DD_research_data.json (one per article)
- Thumbnails: 04_thumbnail/{{YYYY-MM}}/2026-MM-DD_*.png (one per article)
- Metadata: 02_article/{{YYYY-MM}}/_metadata.json
- Schedule: 03_schedule/schedule_2026.md
- Handoff note (if present): 06_research/{{YYYY-MM}}/claude_handoff_{{RANGE}}.md
- Skill rules: .claude/skills/note-daily-gadget-write-article/SKILL.md

## Audit checklist

For each article, verify:

### 1. URL / ASIN integrity (CRITICAL)
- Every Amazon URL contains `tag=daily-gadget-22` exactly.
- The ASIN segment in each Amazon URL (`/dp/XXXXXXXXXX`) matches the corresponding `selected_items[*].asin` in the research JSON.
- The order of products in the article matches the JSON `selected_items` order (or note the divergence with reason if intentional).
- No broken or placeholder URLs.

### 2. Thumbnail presence
- A thumbnail PNG exists in `04_thumbnail/YYYY-MM/` for each article date.
- Report the matched filename per article. Flag any missing thumbnails.

### 3. Metadata sanity
- Every article has a corresponding entry in `_metadata.json` with: filename, title, url (""), tags, category, published_date.
- The `filename` field exactly matches the on-disk filename.
- The `category` is one of: ワークスペース・デスク環境の最適化 / コミュニケーション・会議・音声 / モバイル・電源・周辺機器 / スマートホーム・ライフスタイル・健康管理 / 生産性向上・クリエイティブ・入力機器.
- The `published_date` matches the date in the filename.

### 4. Schedule sync
- Every article date's row in `03_schedule/schedule_2026.md` is wrapped in `~~...~~` strikethrough.
- The title inside the strikethrough matches the article title (allow trivial whitespace differences).

### 5. Format compliance (spot check)
- H1 (title) → blank → intro 2 islands → blank → `## ① {name}` → blank → URL → blank → body paragraph (single paragraph, no internal newlines) → blank → `> **スペック**` + `> ・項目：内容` lines.
- No "商品名: 〜" or "💡注目ポイント" lines below URLs.
- No forbidden endings: 〜ですよ / 〜できますよ / こんにちは.
- No banned metaphors: スパゲッティ / 相棒 / 魔法のような.
- No price / warranty / review-count / origin-country lines in `> **スペック**` blocks.
- Each product body is one paragraph (no `\n` inside). Soft warning if > 230 chars.
- No 3-consecutive 「〜ます。」 endings in any single product body.
- Intro is 2 paragraphs (2 islands). 「最後に」 section is 2 paragraphs.
- 「あわせて読みたい」 URLs are separated by blank lines (one URL per paragraph).
- 「🛒 同じテーマの厳選アイテム…」 block is present, with the correct Amazon idea-list URL per the article's category (see `.docs/amazon_idea_lists.json`).

### 6. Handoff-note compliance
- If `claude_handoff_{{RANGE}}.md` exists, check its "Notes for writing" bullets. Each model-specific caveat (e.g. "describe cooling method per product", "do not claim VPN equivalence") should be reflected somewhere in the corresponding article.

## Report format

Produce a single Markdown report with:

1. **Summary table** — one row per article with PASS / WARN / FAIL per checklist section (1–6).
2. **Findings** — grouped by article, then by checklist section. Each finding includes:
   - The exact file path and line number (when applicable).
   - What was expected vs what was found.
   - Severity: CRITICAL (URL/ASIN/affiliate-tag) / ERROR (metadata/schedule/format violation) / WARN (style/length advisory).
3. **Cross-cutting issues** — any patterns affecting multiple articles.
4. **Verdict** — `READY TO PUBLISH` if zero CRITICAL/ERROR, `NEEDS FIX` otherwise.

Do not propose rewrites. Do not modify files. Only report.
```

---

## 呼び出し方の具体例

引数なしで呼ばれた場合（直前バッチを監査）:

```
ユーザー: 監査して
↓
Claude:
1. 会話文脈から「直前に 2026-07-15〜2026-07-21 を書いた」と特定
2. Agent(subagent_type="codex:codex-rescue", prompt="--effort medium --fresh\n\n<上記テンプレートを埋めたもの>")
3. Codex stdout をそのままユーザーに提示
4. CRITICAL/ERROR があれば修正 → 再監査
```

引数ありで呼ばれた場合（任意の範囲）:

```
ユーザー: /note-daily-gadget-audit-articles 2026-07-08..2026-07-14
↓
Claude:
1. 範囲を 2026-07-08〜2026-07-14 に確定
2. 同上
```

---

## 注意事項

-   **Codex への 1 回の呼び出しで全件監査する**。日付ごとに分割しない（コンテキストとコストの無駄）。
-   Codex のレポートを **paraphrase・要約しない**。stdout 全体をそのまま提示する。
-   レポート末尾の Verdict が `READY TO PUBLISH` なら、Claude 側からは「Phase 3 監査パス」と一言添えるだけで完了とする。
-   `NEEDS FIX` の場合は、Claude が修正したうえで「修正済みの差分一覧」を表示し、必要なら再監査を提案する。
-   Codex が失敗した場合（実行エラー、認証切れ等）は Codex のエラーメッセージをそのまま見せ、ユーザーに `/codex:setup` を促す。
