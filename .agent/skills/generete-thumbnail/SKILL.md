---
name: generate_thumbnail
description: 記事テーマとリサーチデータをもとに、Codex imagegenでnote記事用サムネイル画像を生成して保存するスキル。
---

# Generate Article Thumbnail

## 目的

note記事のテーマ、タイトル、紹介商品の内容から、記事に合ったサムネイル画像をCodexの `imagegen` で生成し、投稿時に使える画像ファイルとして保存する。

## 入力

- 記事の公開日
- 記事タイトル
- `06_research/YYYY-MM/` のリサーチデータ
- 紹介商品の外観的特徴、用途、利用シーン
- 任意で `style_hint`（季節感、色味、置き場所など）

## 出力先

- 保存先: `04_thumbnail/YYYY-MM/`
- ファイル名: `YYYY-MM-DD_短いテーマ名.png`

例:

```text
04_thumbnail/2026-06/2026-06-02_rain_gadgets.png
04_thumbnail/2026-06/2026-06-03_desk_fan.png
```

ファイル名は、公開日と記事内容が対応できるようにする。テーマ名は短く、英数字または日本語で判別できる名前にする。

## 画像生成ルール

- **スタイル**: フォトリアルで高品質なライフスタイル写真。実写に見えるクオリティにする。
- **用途**: note記事のサムネイルとして使いやすい横長構図にする。
- **構図**: メイン被写体を中央の水平帯に配置し、投稿画面でトリミングされても内容が伝わるようにする。
- **シーン**: 商品が実際に置かれ、すぐ使える状態を描く。人物や手を入れず、生活シーンの文脈で用途が伝わる構図にする。
- **配置**: メインのオブジェクトはテーブル、デスク、棚、床など現実的な場所に置く。
- **ライティング**: 窓際の自然光、柔らかいサイドライト、明るく清潔感のあるトーン。
- **カラーパレット**: ホワイト、ナチュラルウッド、ブラックを基調に、記事テーマに必要な色だけを加える。
- **背景**: 奥行きのある室内、デスク、リビング、玄関、洗面所など、記事テーマに合う生活空間にする。
- **小物**: ノートPC、スマホ、コーヒーマグ、観葉植物、ケーブル、収納用品などを必要に応じて加える。

## 量産用の基本方針

サムネイルは毎回細かく調整せず、一発採用できる安定性を優先する。AIっぽさは「接地の曖昧さ」「つなぎ目のばらつき」「空間の切れ」「めり込み」「不自然な人体」「壊れたケーブルやヒンジ」から出るため、プロンプト段階で破綻要因を減らす。

- **人物・手・髪・顔は原則禁止**: 人体は不自然さの原因になりやすいため入れない。
- **主役は原則1製品**: 「〇選」記事でも、サムネイルは代表カテゴリを1点で見せる。記事タイトル側でまとめ感は伝わるため、画像では一目理解と物理整合性を優先する。
- **例外的に複数製品を使うケース**: 旅行準備セット、配信スターターセット、防災セットなど、複数アイテムがそろって初めてテーマが成立する記事のみ。複数にする場合も2〜3点までに抑える。
- **複雑な形状を避ける**: 可動アーム、細いケーブル、多関節スタンド、人物の手元、鏡の複雑な反射は破綻しやすいため、必要最小限にする。
- **同月内の類似構図を避ける**: すべてを「木目デスク、黒モニター、窓、観葉植物」に寄せない。洗面台、玄関、棚、リビング、ベッドサイド、旅行バッグ周辺など、記事テーマに合わせて場所を変える。

## 商品表現ルール

- リサーチデータの商品名、カテゴリ、画像URL、特徴から、代表商品の外観を把握する。
- 実在するロゴやブランド名は画像内に入れない。
- 商品そのものを完全再現しようとせず、形状、色、素材、使われ方が記事テーマと一致するようにする。
- 複数商品を扱う記事でも、原則として代表的な1製品を主役にする。
- 「〇選」記事では、全商品を並べない。まとめ感より、テーマが一目で伝わる単純で破綻しにくい構図を優先する。

## 禁止事項

- 画像内の文字、ロゴ、ブランド名
- 宙に浮いている物体
- 人物、手、髪、顔、体の一部（原則禁止）
- 非現実的なネオン発光
- 顔のアップ
- 商品だけが白背景に並ぶカタログ風構図
- 記事テーマと無関係な過度な装飾
- 読者が実用品として想像しづらい抽象的なイメージ
- 複数製品の過剰な陳列
- 物体同士のめり込み、壊れたヒンジ、切れた空間、交差するケーブル、不自然な反射

## 標準プロンプト骨子

以下の考え方を毎回の `imagegen` プロンプトに含める。

```text
Use case: photorealistic-natural
Asset type: note article thumbnail, wide landscape lifestyle photo
Primary request: Create a thumbnail for an article about <記事テーマ>. Focus on one clear hero product, not a roundup lineup.
Scene/backdrop: <記事テーマに合う生活空間>. The setting should feel practical and lived-in, not decorative.
Subject: one realistic <代表カテゴリ> as the only hero product. No second product, no product lineup.
Style/medium: photorealistic editorial lifestyle photography, natural camera optics, realistic consumer product design, magazine-quality but restrained.
Composition/framing: wide 16:9 horizontal composition. Camera at a slight 30-degree angle. The hero product sits in the central lower third, fully visible with a clean silhouette and enough empty space around it.
Lighting/mood: soft natural daylight, realistic contact shadows, no dramatic effects.
Constraints: No people, no hands, no hair, no face, no body parts. All objects must be physically plausible: correct scale, clear contact shadows, no floating objects, no intersections, no merged cables, no broken joints, no impossible hinges, no cut-off furniture planes, no distorted reflections, no fake text, no logos.
Avoid: multiple products, product lineup, catalog shot, malformed handles, broken cables, brand logos, readable labels, text, watermark, decorative clutter.
```

## 実行手順

1. `03_schedule/schedule_2026.md` とリサーチデータから、対象記事の日付・タイトル・テーマを確認する。
2. `06_research/YYYY-MM/` の対象JSONを読み、代表商品のカテゴリ、外観、利用シーンを整理する。
3. 記事テーマが一目で伝わるサムネイル構図を決める。原則として「人物なし・代表1製品・破綻しにくい生活空間」にする。
4. Codexの `imagegen` で画像を生成する。
5. 生成画像を `04_thumbnail/YYYY-MM/YYYY-MM-DD_短いテーマ名.png` として保存する。
6. 完了報告では、対象記事タイトルと保存先パスを明示する。

## 品質確認

- 記事テーマが画像だけで伝わるか
- 商品や利用シーンが現実的に見えるか
- 文字やロゴが含まれていないか
- サムネイルとして小さく表示されても主題が見えるか
- 保存ファイル名から対象日付と記事が判別できるか
- 人物、手、髪、顔、体の一部が入っていないか
- 商品の接地、影、ヒンジ、ケーブル、反射、奥行きに不自然な破綻がないか
