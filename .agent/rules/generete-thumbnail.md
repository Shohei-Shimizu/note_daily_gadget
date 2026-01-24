---
trigger: model_decision
description: 記事テーマからサムネイル画像を生成するスキル。具体的な画像生成プロンプトの作成と画像出力を行う。
---

# Generate Article Thumbnail

### 目的
note記事のテーマを入力すると、テーマに沿ったサムネイル用画像を複数枚生成する。先に作成したプロンプトを活用しつつ、最終的には Gemini の画像モデル `nanobanana` と `Imagen` を使って文字なしサムネイルを出力する。

### 入力フォーマット
- `theme`: 記事テーマ。例: "集中できるデスク環境"、"創造性を高める朝の習慣"。
- 任意で `style_hint` を追加可能（色味・季節感など）。

### 出力フォーマット
- 3パターン以上のサムネイル画像を番号付きで提示。
- 各パターンは以下を含める。
  - `Description`: 英語で書いた生成プロンプト（1〜2文）
  - `Japanese`: 日本語訳。
  - `Focus`: 強調した要素を一言で。
  - `Image`: 実際に生成した画像。Geminiの画像出力を添付し、同時に alt テキストを付ける。

### 共通スタイル要件
- **3Dレンダリングスタイル**: クリーンで立体的な3Dレンダリングスタイル。Blender/Cinema 4D風の滑らかな質感。
- **カラーパレット**: パステル調の明るい色使い。ソフトブルー、ベージュ、ミントグリーン、ホワイト、ゴールド/ウッドアクセントなど。
- **ライティング**: **柔らかい自然光、またはスタジオライティング**。室内の空気感を感じさせる、ソフトな影とハイライト。
- **構図とシーン（重要）**:
  - メインのオブジェクト（商品やアイテム）に焦点が合っている。
  - **背景は、部屋、カフェ、オフィスの一部などが写り込み、美しくぼかされている（浅い被写界深度、ボケ表現）**。
  - メインオブジェクトはテーブル、デスク、棚などの**上に「置かれて」いる**。
  - 奥行きとリアリティを感じさせる構図。
- **トリミング要件**:
  - 正方形で生成後、16:9（横長）にトリミングすることを前提とした配置
  - **メインのオブジェクトは画面中央の水平帯（縦方向の中央56%エリア）に配置**
  - 上下20-25%のエリアは、**ぼかされた背景要素**（棚、植物、窓など）の配置エリアとする（トリミングでカットされる可能性あり）。
- **質感**: マットな質感と光沢のある質感を組み合わせ。リアル過ぎず、クリーンなイラスト的なバランスを保つ。
- **避けるもの**: 
  - テキスト全般（キャッチコピーなど）
  - **実在する企業名、ブランドロゴ、製品ロゴ（Anker, Apple, Sonyなど）**。
  - 特定の製品を模倣しすぎたデザイン（あくまで「汎用的なデバイス」として描く）。
  - 写実的な人物（手のみや抽象的な人型はOK）。
- 画像生成は Gemini の `nanobanana` を優先し、必要に応じて `Imagen` を補助的に使用する。

### 商品画像の参照（実物に近いサムネイルの生成）

-   **画像URL の確認**: [temp_products.json](cci:7://file:///Users/shoheishimizu/Knowledge/note_daily_gadget/05_script/temp_products.json:0:0-0:0) には各商品の `image_url` が含まれている。サムネイル生成前に、代表的な商品の画像URLを確認し、実際の商品の外観（形状、色、素材感）を把握すること。
-   **プロンプトへの反映**: 確認した商品画像の特徴（例: 「黒いノブ付きコントローラー」「折りたたみ式の白いアイマスク」）を、画像生成プロンプトに具体的に盛り込む。
-   **汎用化のバランス**: ブランドロゴや特定製品の模倣は避けつつも、記事で紹介する商品カテゴリの「典型的な外観」を再現することで、読者が記事内容をイメージしやすいサムネイルを目指す。

### 生成手順
1. テーマから主題となるアイテム・シーン・雰囲気を抽出。
2. 共通スタイル要件（特に**背景のボケ**と**奥行き**）を基盤に、主題を表現する3つ以上のシーンバリエーションを設計。
3. 各シーンで焦点を変える（例: アイテムのクローズアップ、異なる室内背景、光の時間帯）ことで差別化。
4. 各シーンのために英語プロンプトを整え、分かりやすい日本語訳とフォーカスポイントを用意。
5. `nanobanana` で画像を生成し、質感や構図、ボケ感が条件から外れる場合はプロンプトを調整して再生成。
6. `Imagen` を併用して別角度・別雰囲気のバリエーションを補完し、最終的に3枚以上を出力。
7. それぞれの画像を添付し、altテキストと合わせて提示。
8. **画像の保存**: 生成した画像は **`04_thumbnail`** ディレクトリに保存する。
   - ファイル名の例: `YYYY-MM-DD_テーマ_概要.png`（記事の公開予定日と内容がわかる名前にすること）

### 例（説明形式のみ）
*（注：元の例を「グラデーション背景・浮遊」スタイルから、添付画像のような「シーン・奥行き・ボケ」スタイルに差し替えました）*
1. **Description**: A 3D render of a cozy desk setup, focusing on a steaming coffee mug and an open notebook, placed on a light wood desk. The background is a softly blurred modern living room with a shelf and green plants. Shallow depth of field, soft morning light, pastel colors. Main elements centered in the horizontal middle band for 16:9 crop.
   **Japanese**: 湯気の立つコーヒーマグと開いたノートに焦点を当てた、居心地の良いデスクセットアップの3Dレンダリング。明るい木製デスクの上に置かれている。背景は、棚や観葉植物があるモダンなリビングルームが柔らかくぼかされている。浅い被写界深度、柔らかな朝日、パステルカラー。16:9トリミングのため、主要要素は中央の水平帯に配置。
   **Focus**: 浅い被写界深度（ボケ）とデスクの空気感
   **Image**: *(ここにnanobananaで生成した画像を添付し、altテキストを付与する)*
2. **Description**: 3D illustration of high-tech noise-canceling headphones and wireless earbuds placed on a sleek white table. The background features a blurred minimalist cafe interior with large windows and soft ambient light. Main objects are in sharp focus in the center horizontal zone, optimized for 16:9 cropping.
   **Japanese**: 高性能ノイズキャンセリングヘッドホンとワイヤレスイヤホンが、洗練された白いテーブルの上に置かれている3Dイラスト。背景は、大きな窓と柔らかい環境光が特徴の、ぼかされたミニマリストなカフェの内装。主要なオブジェクトは中央の水平ゾーンでシャープに焦点が合っており、16:9トリミングに最適化されている。
   **Focus**: カフェ風の背景とガジェットの質感
   **Image**: *(ここにnanobananaで生成した画像を添付し、altテキストを付与する)*
3. **Description**: A photorealistic 3D render focused on a stack of neatly folded pastel-colored towels and a small wooden bowl on a minimalist beige shelf. The background is a simple, out-of-focus room with soft shadows, creating a sense of depth. Centered horizontal composition safe for 16:9 crop.
   **Japanese**: きれいに畳まれたパステルカラーのタオルの山と、ミニマリストなベージュの棚に置かれた小さな木製のボウルに焦点を当てた、フォトリアルな3Dレンダリング。背景はシンプルでピントの合っていない部屋と柔らかい影で、奥行き感を演出。16:9トリミングに対応した中央水平構図。
   **Focus**: モノへの焦点とシンプルな背景のボケ
   **Image**: *(ここにnanobananaで生成した画像を添付し、altテキストを付与する)*