---
name: generate_thumbnail
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
- **スタイル**: **フォトリアルで高品質なライフスタイル写真**（3Dレンダリングではなく、実写に見えるクオリティ）。Vlogやガジェットレビューのサムネイルのような雰囲気。
- **シーン設定（In-Use Scenario）**:
  - 単にモノが置いてあるだけでなく、**「実際に使われている」状態を描く**。
  - 例: ケーブルが繋がっている、コンセントに挿さっている、スマホ画面が点灯している、手帳が開かれている。
  - **メインのオブジェクトはテーブル、デスク、棚などの上に「置かれて」いる**。
- **ライティング**: **「窓際の自然光」**。
  - 画面の片側（右や左）から強いが柔らかい日光が差し込むサイドライト。
  - **ハイキー（明るめ）なトーン**: 清潔感があり、白や木目が美しく映える明るさ。
- **カラーパレット**:
  - **モダン＆ミニマル**: 「ホワイト・ナチュラルウッド・ブラック（アクセント）」の配色。
  - パステルよりも、落ち着いた**無彩色のコントラストと木のぬくもり**を重視。
- **構図（重要）**:
  - **背景ボケ**: 奥行きのある室内（リビング、デスク）が背景。窓枠や観葉植物が美しくボケている。
  - **プロップ（小物）**: ノートPC（MacBook風）、スマホ、コーヒーマグ、観葉植物などを配置して「生活感」と「作業環境」を演出する。
  - **トリミング**: 正方形生成→16:9トリミングを前提とし、メイン被写体は**中央の水平帯（縦56%）**に収める。
- **避けるもの**: 
  - テキスト全般、実在するロゴ。
  - 宙に浮いている物体、非現実的なネオン発光。
  - 顔のアップ（手や後ろ姿はOKだが、モノが主役）。
- 画像生成は Gemini の `Imagen 3` (または `nanobanana`) を使用し、写実性を最優先する。

### 商品画像の参照（実物に近いサムネイルの生成）

-   **画像URL の確認**: [temp_products.json](cci:7://file:///Users/shoheishimizu/Knowledge/note_daily_gadget/05_script/temp_products.json:0:0-0:0) には各商品の `image_url` が含まれている。サムネイル生成前に、代表的な商品の画像URLを確認し、実際の商品の外観（形状、色、素材感）を把握すること。
-   **プロンプトへの反映**: 確認した商品画像の特徴（例: 「黒いノブ付きコントローラー」「折りたたみ式の白いアイマスク」）を、画像生成プロンプトに具体的に盛り込む。
-   **再現性の重視**: 記事で紹介している**実際の商品**（またはそのカテゴリの代表的な商品）の**外観的特徴（形状、色、素材、ボタン配置など）を忠実にプロンプトに反映する**。
-   **具体化**: 「汎用的なデバイス」ではなく、**「その商品そのもの」に見えるレベル**まで具体的に描写すること（例: 「角が丸い四角形」「前面に大きな丸いスピーカー穴」など）。ただし、ロゴマークは崩れる可能性があるため、形状と雰囲気を優先する。

### 生成手順
1. テーマから主題となるアイテム・シーン・雰囲気を抽出。
2. 共通スタイル要件（特に**背景のボケ**と**奥行き**）を基盤に、主題を表現する3つ以上のシーンバリエーションを設計。
3. 各シーンで焦点を変える（例: アイテムのクローズアップ、異なる室内背景、光の時間帯）ことで差別化。
4. 各シーンのために英語プロンプトを整え、分かりやすい日本語訳とフォーカスポイントを用意。
5. `nanobanana` で画像を生成し、質感や構図、ボケ感が条件から外れる場合はプロンプトを調整して再生成。
6. `Imagen` を併用して別角度・別雰囲気のバリエーションを補完し、最終的に3枚以上を出力。
7. それぞれの画像を添付し、altテキストと合わせて提示。
8. **画像の保存**:
   - 記事の公開予定日（またはファイル名の日付）から年月を特定する（例: 2026-02-08 → 2026-02）。
   - **`04_thumbnail/YYYY-MM`** ディレクトリに保存する（ディレクトリが存在しない場合は作成する）。
   - ファイル名の例: `YYYY-MM-DD_テーマ_概要.png`

### 例（説明形式のみ）
*（注：元の例を「グラデーション背景・浮遊」スタイルから、添付画像のような「シーン・奥行き・ボケ」スタイルに差し替えました）*
1. **Description**: A photorealistic lifestyle shot of a steaming ceramic coffee mug and an open notebook on a light wood desk. The scene is bathed in soft morning sunlight from a window on the right. In the background, a cozy living room with a beige sofa and green plants is beautifully blurred. High-key lighting, natural atmosphere. Main objects centered.
   **Japanese**: 湯気の立つ陶器のマグカップと開いたノートが、明るい木目のデスクに置かれているフォトリアルなライフスタイル写真。右側のウィンドウから柔らかな朝の日差しが注いでいる。背景には、ベージュのソファと観葉植物がある居心地の良いリビングルームがきれいにぼかされている。ハイキーなライティング、自然な空気感。主要なオブジェクトは中央配置。
   **Focus**: 窓際の自然光と朝の作業風景
   **Image**: *(ここにImagenで生成した画像を添付し、altテキストを付与する)*
2. **Description**: A realistic close-up of high-tech noise-canceling headphones resting on a white table in a modern cafe. A smartphone with a lit screen is placed next to them. The background shows a blurred cafe interior with large glass windows and people working in the distance. Bright, clean aesthetic with strong depth of field.
   **Japanese**: モダンなカフェの白いテーブルに置かれた、ハイテクなノイズキャンセリングヘッドホンのリアルなクローズアップ。画面が点灯しているスマートフォンが隣に置かれている。背景には、大きなガラス窓と遠くで働いている人々がいる、ぼかされたカフェの店内が写っている。明るく清潔感のある美学と、強い被写界深度。
   **Focus**: カフェでの使用シーンとデバイスの質感
   **Image**: *(ここにImagenで生成した画像を添付し、altテキストを付与する)*
3. **Description**: A lifestyle image of neatly folded monochromatic towels and a wooden bowl on a bathroom shelf. Sunlight filters through a window, creating soft shadows on the white wall. The composition is minimal and organic, emphasizing texture and cleanliness. A small green plant adds a touch of nature.
   **Japanese**: バスルームの棚に置かれた、きれいに畳まれたモノクロームのタオルと木製のボウルのライフスタイル画像。窓から日差しが差し込み、白い壁に柔らかな影を落としている。構図はミニマルでオーガニックであり、質感と清潔感を強調している。小さな観葉植物が自然なアクセントを加えている。
   **Focus**: 自然光とオーガニックな質感
   **Image**: *(ここにImagenで生成した画像を添付し、altテキストを付与する)*
