import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "06_research" / "2026-07"
ARTICLE_DIR = ROOT / "02_article" / "2026-07"
METADATA_PATH = ARTICLE_DIR / "_metadata.json"
SCHEDULE_PATH = ROOT / "03_schedule" / "schedule_2026.md"


CONFIG = {
    "2026-07-24": {
        "intro1": "旅行で家を空ける間、室内の様子や異変をすぐ確認できないことに不安を感じる方は少なくありません。スマートカメラなら、外出先のスマートフォンから映像を確認し、動きを検知した際に通知を受け取れます。",
        "intro2": "今回は、画質や検知機能、設置のしやすさを比較しやすいスマートカメラを7点厳選しました。ご自宅に合う一台を見つけてみてください。",
        "type": "屋内用スマートカメラ",
        "use": "旅行中の見守り・防犯",
        "tags": "おすすめガジェット スマートカメラ 防犯カメラ 見守りカメラ スマートホーム 旅行",
        "category": "スマートホーム・ライフスタイル・健康管理",
        "list_title": "家事も健康も自動化。スマートホーム＆ライフ改善ガジェット",
        "list_url": "https://www.amazon.co.jp/shop/zanetti/list/3PE57JTNNDNGZ",
        "related": ["https://note.com/daily_gadget/n/n6bb8fe0f4ed6", "https://note.com/daily_gadget/n/nb727d58b3370", "https://note.com/daily_gadget/n/ne4d3969c6fa4", "https://note.com/daily_gadget/n/nb6fc70762f8b", "https://note.com/daily_gadget/n/n08f1e8a7c62a"],
    },
    "2026-07-25": {
        "intro1": "毎日の家電操作や照明の切り替えを個別に行うと、小さな手間が積み重なります。IFTTTや音声アシスタントに対応する機器を組み合わせれば、時刻やセンサーをきっかけにルーティンを自動化できます。",
        "intro2": "今回は、既存家電を生かしながらスマート連携を始めやすい機器を6点厳選しました。自動化したい動作から選んでみてください。",
        "type": "スマートホーム連携機器",
        "use": "家電操作と日常ルーティンの自動化",
        "tags": "おすすめガジェット IFTTT スマートホーム 家電自動化 スマートリモコン 生活改善",
        "category": "スマートホーム・ライフスタイル・健康管理",
        "list_title": "家事も健康も自動化。スマートホーム＆ライフ改善ガジェット",
        "list_url": "https://www.amazon.co.jp/shop/zanetti/list/3PE57JTNNDNGZ",
        "related": ["https://note.com/daily_gadget/n/n6bb8fe0f4ed6", "https://note.com/daily_gadget/n/nb727d58b3370", "https://note.com/daily_gadget/n/ne4d3969c6fa4", "https://note.com/daily_gadget/n/nb6fc70762f8b", "https://note.com/daily_gadget/n/n70643deaa83d"],
    },
    "2026-07-26": {
        "intro1": "写真編集や動画制作では、同じショートカットを何度も入力する操作が作業時間を圧迫します。物理ダイヤルや割り当て可能なボタンを備えたデバイスなら、調整とコマンド実行を片手に集約できます。",
        "intro2": "今回は、編集ソフトやイラスト制作で使いやすいダイヤルデバイスを7点厳選しました。よく使うアプリとの対応を確認して選んでみてください。",
        "type": "クリエイター向け入力デバイス",
        "use": "写真・動画・イラスト制作の操作短縮",
        "tags": "おすすめガジェット 左手デバイス ダイヤルデバイス 動画編集 クリエイター 生産性",
        "category": "生産性向上・クリエイティブ・入力機器",
        "list_title": "仕事を速くする。生産性向上＆クリエイティブガジェット",
        "list_url": "https://amzn.to/42HITJ4",
        "related": ["https://note.com/daily_gadget/n/ne6d076bdd8f2", "https://note.com/daily_gadget/n/nc1f5c2ff7165", "https://note.com/daily_gadget/n/n7804f7a4b765", "https://note.com/daily_gadget/n/n2239d6d8e0ce", "https://note.com/daily_gadget/n/n46c91aeff52d"],
    },
    "2026-07-27": {
        "intro1": "海外旅行で会話のテンポを保ちながら翻訳アプリを操作するのは、意外と負担が大きいものです。翻訳イヤホンなら、端末を何度も手渡さずに相手との会話を続けやすくなります。",
        "intro2": "今回は、対応言語や会話方式の異なるAI翻訳イヤホンを5点厳選しました。渡航先と使い方に合うモデルを見つけてみてください。",
        "type": "AI翻訳イヤホン",
        "use": "海外旅行・出張時の対面会話",
        "tags": "おすすめガジェット AI翻訳イヤホン 翻訳機 海外旅行 語学学習 モバイル",
        "category": "コミュニケーション・会議・音声",
        "list_title": "録る・撮る・聴く。配信&リモート会議向け音響映像ガジェット",
        "list_url": "https://amzn.to/42HITJ4",
        "related": ["https://note.com/daily_gadget/n/ne6d076bdd8f2", "https://note.com/daily_gadget/n/nc1f5c2ff7165", "https://note.com/daily_gadget/n/n7804f7a4b765", "https://note.com/daily_gadget/n/n2239d6d8e0ce", "https://note.com/daily_gadget/n/n46c91aeff52d"],
    },
    "2026-07-28": {
        "intro1": "キャンプや停電時に電源を長く確保するには、ポータブル電源へ継続して給電できる仕組みが役立ちます。折りたたみ式ソーラーパネルなら、収納性を保ちながら屋外で太陽光を電力へ変換できます。",
        "intro2": "今回は、出力と携帯性のバランスを比較しやすいソーラーパネルを6点厳選しました。接続する機器の入力仕様も確認して選んでみてください。",
        "type": "折りたたみ式ソーラーパネル",
        "use": "キャンプ・防災時の太陽光充電",
        "tags": "おすすめガジェット ソーラーパネル ポータブル電源 防災 キャンプ 太陽光充電",
        "category": "モバイル・電源・周辺機器",
        "list_title": "カフェも車内も。外出先で仕事を進めるモバイルガジェット",
        "list_url": "https://amzn.to/4cPpADI",
        "related": ["https://note.com/daily_gadget/n/n4992e2b12d9f", "https://note.com/daily_gadget/n/n52d2708230bf", "https://note.com/daily_gadget/n/n50efd5c71fdf", "https://note.com/daily_gadget/n/nac6e23f3c311", "https://note.com/daily_gadget/n/nafc898aec1f1"],
    },
    "2026-07-29": {
        "intro1": "公園やキャンプ場でノートPCを使うと、安定した作業面と長く座れる場所の確保が課題になります。膝上テーブルと軽量チェアを組み合わせれば、設備のない場所でも作業姿勢を整えやすくなります。",
        "intro2": "今回は、持ち運びやすい膝上テーブル3点とアウトドアチェア3点を厳選しました。移動手段と作業時間に合わせて選んでみてください。",
        "type": "屋外ワーク用品",
        "use": "公園・キャンプ場でのモバイルワーク",
        "tags": "おすすめガジェット 膝上テーブル アウトドアチェア ワーケーション 公園 モバイル",
        "category": "ワークスペース・デスク環境の最適化",
        "list_title": "カフェも車内も。外出先で仕事を進めるモバイルガジェット",
        "list_url": "https://amzn.to/4cPpADI",
        "related": ["https://note.com/daily_gadget/n/n4992e2b12d9f", "https://note.com/daily_gadget/n/n52d2708230bf", "https://note.com/daily_gadget/n/n50efd5c71fdf", "https://note.com/daily_gadget/n/nac6e23f3c311", "https://note.com/daily_gadget/n/nafc898aec1f1"],
    },
    "2026-07-30": {
        "intro1": "夜のキャンプや部屋で過ごす時間は、明るさだけでなく光の色や置き方でも居心地が変わります。LEDランタンとスマート間接照明なら、必要な明かりを確保しながら空間の雰囲気を調整できます。",
        "intro2": "今回は、持ち運べるランタン3点とアプリ連携に対応する間接照明3点を厳選しました。使う場所に合う光を選んでみてください。",
        "type": "LEDランタン・スマート照明",
        "use": "夜間の照明と空間演出",
        "tags": "おすすめガジェット LEDランタン 間接照明 スマート照明 キャンプ スマートホーム",
        "category": "スマートホーム・ライフスタイル・健康管理",
        "list_title": "家事も健康も自動化。スマートホーム＆ライフ改善ガジェット",
        "list_url": "https://www.amazon.co.jp/shop/zanetti/list/3PE57JTNNDNGZ",
        "related": ["https://note.com/daily_gadget/n/n6bb8fe0f4ed6", "https://note.com/daily_gadget/n/nb727d58b3370", "https://note.com/daily_gadget/n/ne4d3969c6fa4", "https://note.com/daily_gadget/n/nb6fc70762f8b", "https://note.com/daily_gadget/n/n08f1e8a7c62a"],
    },
    "2026-07-31": {
        "intro1": "猛暑対策から旅行中の通信、撮影データの保存まで、7月は外出先で役立つガジェットが多く登場しました。月間ベストバイでは、用途の明確さと夏の仕事・レジャーでの使いやすさを軸に振り返ります。",
        "intro2": "今回は、7月に紹介した商品の中から改めて注目したい夏のガジェットを8点厳選しました。今の課題に合う一台を見つけてみてください。",
        "type": "夏向け実用ガジェット",
        "use": "猛暑対策・旅行・撮影・データ保護",
        "tags": "買ってよかったもの おすすめガジェット ベストバイ 夏ガジェット 旅行 生産性",
        "category": "モバイル・電源・周辺機器",
        "list_title": "カフェも車内も。外出先で仕事を進めるモバイルガジェット",
        "list_url": "https://amzn.to/4cPpADI",
        "related": ["https://note.com/daily_gadget/n/n4992e2b12d9f", "https://note.com/daily_gadget/n/n52d2708230bf", "https://note.com/daily_gadget/n/n50efd5c71fdf", "https://note.com/daily_gadget/n/nac6e23f3c311", "https://note.com/daily_gadget/n/nafc898aec1f1"],
    },
}


SKIP_WORDS = (
    "保証", "レビュー", "販売元", "正規品", "助成金", "こんにちは",
    "無料体験", "公式サイト", "ご注意", "購入の場合", "メーカー名",
    "最新モデル発売中",
)

NAME_OVERRIDES = {
    "B0CR3Y76ZH": "SwitchBot 見守りカメラ Plus 5MP",
    "B09WQZHBTN": "Google Nest Cam",
    "B0GFWDBDR1": "Wooask M3 PLUS",
    "B0B74752CR": "Wooask M6 PLUS",
    "B01GZX4UQU": "HUION Keydial mini",
    "B0CDG5HCCH": "8BitDo Micro",
}

SUMMARY_OVERRIDES = {
    "B09WQZHBTN": (
        "最大1080pのHDR動画と130度の広い画角に対応し、室内外の様子を広く確認できます",
        "バッテリー式で設置場所を選びやすく、双方向音声とモーション検出も利用可能です",
    ),
    "B0CM3DWCZN": (
        "10個のカスタマイズキーと物理ダイヤルを備え、頻繁に使う操作を手元へ集約できます",
        "Bluetoothと有線接続に対応し、対応ソフトごとにショートカットを切り替えられます",
    ),
    "B0DY1CQ2VP": (
        "独立した2つのサーモモジュールで首元を冷却し、暑い日の移動を支えます",
        "スマートフォン連携と自動温度調整に対応し、環境に合わせて運転を制御できます",
    ),
    "B07RKL4L7Q": (
        "512GBの容量を備え、4K動画や高解像度写真をまとめて保存しやすいmicroSDカードです",
        "A2規格に対応し、対応機器でのアプリ実行や連続撮影にも使いやすい構成です",
    ),
    "B0DK71JL4Z": (
        "50言語以上の翻訳に対応し、相手と向き合ったまま会話を続けやすいイヤホン型翻訳機です",
        "手元の操作を減らせるハンズフリー設計で、旅行や出張時の対面会話に向いています",
    ),
    "B0CDC3XW44": (
        "大型ターボファンと密閉フォームを組み合わせ、ノートPC底面へ集中的に風を送ります",
        "14.1〜19.3インチに対応し、USBハブと防塵フィルターも備えています",
    ),
    "B0723GY3GV": (
        "折りたたみ式の28WパネルにUSB-AとUSB-C出力を備え、スマートフォンを直接充電できます",
        "電流計と自動再充電機能を搭載し、日照の変化がある屋外でも状態を確認しやすい設計です",
    ),
    "B07B7NXV4R": (
        "壁スイッチや家電の物理ボタンをスマートフォンから押せる小型の指ロボットです",
        "対応ハブと組み合わせることで、タイマーや音声操作、IFTTTを使った自動化に対応します",
    ),
}

META_ONLY = {
    "2026-07-22": {
        "filename": "2026-07-22_キャンプ最強セット。防水「スピーカーとバッテリー」_6選.md",
        "tags": "おすすめガジェット 防水スピーカー ポータブル電源 キャンプ 防災 アウトドア",
        "category": "モバイル・電源・周辺機器",
    },
    "2026-07-23": {
        "filename": "2026-07-23_旅日記を声で書く。高精度な「音声入力マイク」_6選.md",
        "tags": "おすすめガジェット USBマイク 音声入力 旅日記 録音 生産性",
        "category": "コミュニケーション・会議・音声",
    },
}


def clean_text(value):
    value = value.strip()
    while re.match(r"^(?:【[^】]+】|\[[^\]]+\])", value):
        value = re.sub(r"^(?:【[^】]+】|\[[^\]]+\])\s*", "", value)
    value = re.sub(r"^[^\w一-龥ぁ-んァ-ヶ]+", "", value)
    while re.match(r"^(?:【[^】]+】|\[[^\]]+\])", value):
        value = re.sub(r"^(?:【[^】]+】|\[[^\]]+\])\s*", "", value)
    value = re.sub(r"\s+", " ", value)
    return value


def first_sentence(value, limit=118):
    value = clean_text(value)
    parts = re.split(r"(?<=[。！？])", value)
    text = next((p.strip("。！？ ") for p in parts if p.strip()), value)
    if "：" in text and text.index("：") < 28:
        text = text.split("：", 1)[1].strip()
    if len(text) > limit:
        commas = [m.start() for m in re.finditer(r"[、,]", text) if 55 <= m.start() <= limit]
        cut = commas[-1] if commas else limit
        text = text[:cut].rstrip("、, ") + "点が特徴です"
    return text.strip("。")


def product_name(item):
    if item["asin"] in NAME_OVERRIDES:
        return NAME_OVERRIDES[item["asin"]]
    query = item.get("query", "")
    for suffix in (
        " 見守りカメラ", " スマートリモコン", " スマートプラグ", " スイッチ",
        " 左手デバイス", " 編集コントローラー", " ワイヤレスショートカットリモート",
        " 翻訳イヤホン", " 翻訳機", " ソーラーパネル", " ソーラーチャージャー",
        " 膝上テーブル", " ノートパソコン", " 軽量 アウトドアチェア",
        " アウトドアチェア 軽量", " LED ランタン", " ポータブルライト",
    ):
        query = query.replace(suffix, "")
    return query.strip()


def feature_sentences(item):
    if item["asin"] in SUMMARY_OVERRIDES:
        return list(SUMMARY_OVERRIDES[item["asin"]])
    candidates = []
    for feature in item.get("features", []):
        if any(word in feature for word in SKIP_WORDS):
            continue
        sentence = first_sentence(feature)
        if len(sentence) >= 18 and sentence not in candidates:
            candidates.append(sentence)
        if len(candidates) == 2:
            break
    if not candidates:
        candidates.append(first_sentence(item["title"]))
    if len(candidates) == 1:
        candidates.append(f"{item.get('query', product_name(item))}として必要な機能を一台にまとめています")
    return candidates


def facts(item):
    text = item["title"] + " " + " ".join(item.get("features", [])[:3])
    patterns = [
        r"IP\d{2}[K]?", r"\d+(?:\.\d+)?(?:W|Wh|mAh|GB|TB|MP|lm|ルーメン)",
        r"\b[248]K\b", r"Bluetooth\s?\d(?:\.\d)?",
        r"USB(?:-C|-A| Type-C)?", r"Matter", r"IFTTT", r"FIDO2", r"NFC",
    ]
    found = []
    for pattern in patterns:
        for match in re.findall(pattern, text, flags=re.I):
            fact = match if isinstance(match, str) else "".join(match)
            if fact.lower() not in {x.lower() for x in found}:
                found.append(fact)
            if len(found) == 3:
                return found
    return found


def filename_for(data):
    compact = data["title"].replace(" ", "")
    compact = re.sub(r"(\d+)選$", r"_\1選", compact)
    return f'{data["date"]}_{compact}.md'


def render_article(data, config):
    lines = [f'# {data["title"]}', "", config["intro1"], "", config["intro2"], ""]
    for index, item in enumerate(data["selected_items"], start=1):
        name = product_name(item)
        fs = feature_sentences(item)
        body = (
            f"{name}は、{fs[0]}。{fs[1]}。"
            f"{config['use']}を重視して候補を絞る際に、機能と扱いやすさを比較しやすい一台です。"
        )
        lines.extend([
            f"## {chr(0x245f + index)} {name}", "", item["url"], "", body, "",
            "> **スペック**",
            f"> ・製品タイプ：{config['type']}",
            f"> ・主な用途：{config['use']}",
        ])
        for fact in facts(item):
            lines.append(f"> ・対応・仕様：{fact}")
        lines.append("")

    count = data["selected_count"]
    lines.extend([
        "## 最後に", "",
        f"今回は、{config['use']}に役立つ製品を{count}点紹介しました。必要な機能と持ち運びや設置の条件を整理し、ご自身の使い方に合う一台を見つけてみてください。", "",
        "毎日ガジェット通信では、仕事と生活をラクにするガジェット情報を発信しています。気に入っていただけたら、ぜひスキとフォローをお願いします！", "",
        "## 🛒 同じテーマの厳選アイテムをまとめてチェック", "",
        "このカテゴリのおすすめガジェットをAmazonの「アイデアリスト」にまとめました。気になった商品を一覧で比較したい方はこちらからどうぞ。", "",
        f"▼ {config['list_title']}", config["list_url"], "",
        "## あわせて読みたい", "",
    ])
    for url in config["related"]:
        lines.extend([url, ""])
    return "\n".join(lines).rstrip() + "\n"


def update_metadata(records):
    metadata = json.loads(METADATA_PATH.read_text())
    existing = {article["published_date"]: article for article in metadata["articles"]}
    for data, config, filename in records:
        record = {
            "filename": filename,
            "title": data["title"],
            "url": "",
            "tags": config["tags"],
            "category": config["category"],
            "published_date": data["date"],
        }
        if data["date"] in existing:
            existing[data["date"]].update(record)
        else:
            metadata["articles"].append(record)
    metadata["articles"].sort(key=lambda article: article["published_date"])
    METADATA_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")


def update_schedule(records):
    text = SCHEDULE_PATH.read_text()
    for data, _, _ in records:
        date = data["date"].replace("-", "/")
        pattern = re.compile(rf"^(\| {re.escape(date)} \| )(.+?)(\s+\|)$", re.M)
        text, count = pattern.subn(
            lambda match: f"{match.group(1)}~~{data['title']}~~{match.group(3)}",
            text,
            count=1,
        )
        if count != 1:
            raise RuntimeError(f"schedule row not found: {date}")
    SCHEDULE_PATH.write_text(text)


def main():
    ARTICLE_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    for date, config in CONFIG.items():
        data = json.loads((RESEARCH_DIR / f"{date}_research_data.json").read_text())
        filename = filename_for(data)
        (ARTICLE_DIR / filename).write_text(render_article(data, config))
        records.append((data, config, filename))
        print(f"wrote {filename}")
    for date, config in META_ONLY.items():
        data = json.loads((RESEARCH_DIR / f"{date}_research_data.json").read_text())
        records.append((data, config, config["filename"]))
    update_metadata(records)
    update_schedule(records)


if __name__ == "__main__":
    main()
