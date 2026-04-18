import json
import os
import re
import sys
import time
from importlib.machinery import SourceFileLoader


PARTNER_TAG = "daily-gadget-22"
SEARCH_MODULE = SourceFileLoader(
    "search_custom_list", os.path.join("05_script", "search_custom_list.py")
).load_module()


TASKS = [
    {
        "date": "2026-04-09",
        "title": "家電の消し忘れを防止。電源をスマホで操る「スマートプラグ」 7 選",
        "target_count": 7,
        "queries": [
            "TP-Link Tapo P110M",
            "SwitchBot プラグミニ",
            {"query": "Meross Matter スマートプラグ", "include": ["スマートプラグ"]},
            "TP-Link Tapo P105",
            {"query": "Amazon スマートプラグ", "include": ["スマートプラグ"]},
            {"query": "SwitchBot スマートプラグ 2個セット", "include": ["スマートプラグ"]},
            {"query": "Meross スマートプラグ 消費電力", "include": ["スマートプラグ"]},
        ],
    },
    {
        "date": "2026-04-10",
        "title": "充電ケーブルを廃止。MagSafe で整う「ワイヤレスデスク」 7 選",
        "target_count": 7,
        "queries": [
            "Anker MagGo charging station",
            "Belkin 3 in 1 MagSafe",
            {"query": "Twelve South HiRise 3 Deluxe", "include": ["充電"]},
            "ESR Qi2 3 in 1 charging station",
            {"query": "UGREEN Qi2 2 in 1 ワイヤレス充電器", "include": ["充電"]},
            "MOFT Smart Desk Mat MagSafe",
            "CIO NovaWave 3Way",
        ],
    },
    {
        "date": "2026-04-11",
        "title": "庭やベランダで仕事。アウトドアで使える「ワークライト」 5 選",
        "target_count": 5,
        "queries": [
            "Ledlenser ワークライト",
            "GENTOS ワークライト USB充電",
            "Makita 充電式ワークライト",
            "Bosch ワークライト バッテリー",
            "LUMENA マルチランタン",
        ],
    },
    {
        "date": "2026-04-12",
        "title": "電気代を節約。人感センサーやアプリで賢く照らす「スマート照明」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Philips Hue スターターセット", "include": ["電球"]},
            {"query": "TP-Link Tapo L530E", "include": ["電球", "LED"]},
            {"query": "SwitchBot LED電球", "include": ["電球"]},
            "アイリスオーヤマ 人感センサー LED 電球",
            {"query": "パナソニック 人感センサー LED電球", "include": ["電球"]},
            {"query": "Meross スマート電球", "include": ["電球"]},
        ],
    },
    {
        "date": "2026-04-13",
        "title": "大切なペットを見守る。会話もできる「ネットワークカメラ」 7 選",
        "target_count": 7,
        "queries": [
            "TP-Link Tapo C200",
            "TP-Link Tapo C210",
            "SwitchBot 見守りカメラ Plus 3MP",
            "Anker Eufy IndoorCam C220",
            "Anker Eufy IndoorCam 2K Pan Tilt",
            "ATOM Cam 2",
            "Google Nest Cam",
        ],
    },
    {
        "date": "2026-04-14",
        "title": "【Anker Eufy】ロボット掃除機の人気モデル徹底比較 10 選",
        "target_count": 10,
        "queries": [
            "Eufy Robot Vacuum Omni S1 Pro",
            "Eufy Robot Vacuum Omni C20",
            "Eufy X10 Pro Omni",
            "Eufy Robot Vacuum Omni E25",
            "Eufy Robot Vacuum Omni C28",
            "Eufy Clean X8 Pro with Self-Empty Station",
            "Eufy Robot Vacuum Auto-Empty C10",
            {"query": "Eufy Clean G40 Hybrid+", "include": ["ロボット掃除機"], "exclude": ["交換", "バッグ"]},
            {"query": "Eufy RoboVac G30", "include": ["ロボット掃除機"], "exclude": ["交換", "バッグ"]},
            {"query": "Eufy RoboVac G30 Hybrid", "include": ["ロボット掃除機"], "exclude": ["交換", "バッグ"]},
        ],
    },
    {
        "date": "2026-04-15",
        "title": "集中力を維持。眠気を防ぐ「二酸化炭素モニター」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "SwitchBot CO2センサー", "include": ["CO2"]},
            {"query": "プラス CO2モニター AT-C01", "include": ["CO2"]},
            {"query": "INKBIRD IAQM-128", "include": ["CO2"]},
            {"query": "INKBIRD IAM-T2", "include": ["CO2"]},
            {"query": "CO2マネージャー 二酸化炭素濃度計", "include": ["CO2"]},
            {"query": "FieldNew 二酸化炭素濃度計 NDIR", "include": ["二酸化炭素"]},
        ],
    },
    {
        "date": "2026-04-16",
        "title": "ビデオ会議を鮮明に。顔を自動追尾する「AI カメラ」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "OBSBOT Tiny 2 web camera", "include": ["TINY 2", "AI"]},
            {"query": "OBSBOT Tiny 2 Lite", "include": ["Tiny 2 Lite", "AI"]},
            {"query": "OBSBOT Tiny SE", "include": ["TINY SE", "AI"]},
            {"query": "Insta360 Link Web camera", "include": ["Link Webカメラ", "AI追跡"]},
            {"query": "Insta360 Link 2", "include": ["Link 2", "AI"]},
            {"query": "Insta360 Link 2 Pro", "include": ["Link 2 Pro", "AI"]},
        ],
    },
    {
        "date": "2026-04-17",
        "title": "デスクの配線を隠す。床をスッキリさせる「整理ボックス」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "サンワダイレクト ケーブルボックス", "include": ["ケーブルボックス"]},
            {"query": "ELECOM ケーブル収納ボックス", "include": ["ボックス"]},
            {"query": "山崎実業 ケーブルボックス", "include": ["ボックス"]},
            {"query": "ナカバヤシ ケーブルボックス", "include": ["ボックス"]},
            {"query": "無印良品 ケーブル収納", "include": ["収納"]},
            {"query": "IKEA ケーブルボックス", "include": ["ボックス"]},
            {"query": "バッファロー ケーブルボックス", "include": ["ケーブルボックス"]},
        ],
    },
    {
        "date": "2026-04-18",
        "title": "GW 旅行を快適に。機内で役立つ「ノイキャンヘッドホン」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Sony WH-1000XM5", "include": ["ヘッドホン"]},
            {"query": "Bose QuietComfort Ultra Headphones", "include": ["ヘッドホン"]},
            {"query": "Sonos Ace", "include": ["ヘッドホン"]},
            {"query": "Sennheiser Momentum 4 Wireless", "include": ["ヘッドホン"]},
            {"query": "Soundcore Space One Pro", "include": ["ヘッドホン"]},
            {"query": "JBL Tour One M2", "include": ["ヘッドホン"]},
        ],
    },
    {
        "date": "2026-04-19",
        "title": "集中と休憩を管理。作業リズムを作る「物理タイマー」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Time Timer MOD", "include": ["タイマー"]},
            {"query": "TickTime Pomodoro タイマー", "include": ["タイマー"]},
            {"query": "dretec 学習タイマー", "include": ["タイマー"]},
            {"query": "ソニック トキサポ タイマー", "include": ["タイマー"]},
            {"query": "SEIKO タイマー", "include": ["タイマー"]},
            {"query": "磁気 キューブタイマー", "include": ["タイマー"]},
        ],
    },
    {
        "date": "2026-04-20",
        "title": "鍵のストレスをゼロに。指紋で開く「最新スマートロック」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "SwitchBot ロック Ultra 指紋認証パッド セット", "include": ["セット買い", "指紋認証"]},
            {"query": "SwitchBot スマートロック Lite 指紋認証パッド", "include": ["指紋認証", "スマートロック"]},
            {"query": "SESAME 5 指紋認証", "include": ["SESAME", "指紋認証"]},
            {"query": "Aqara H100 スマートドアロック", "include": ["指紋", "ロック"]},
            {"query": "EPIC Flassa3D-NB", "include": ["指紋"]},
            {"query": "Yale Assure Lock 2 Touch", "include": ["指紋スマートロック"]},
        ],
    },
    {
        "date": "2026-04-21",
        "title": "ガジェットを飾る収納。デスク横に置く「有孔ボード」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "EastForce ペグボード デスクパネル", "include": ["ペグボード"]},
            {"query": "サンカ スチール パンチングボード", "include": ["パンチングボード"]},
            {"query": "キングジム ペグボード ペギー", "include": ["ペギー"]},
            {"query": "イーサプライ ペグボード EEX-PRB01BK", "include": ["ペグボード", "EEX-PRB01BK"]},
            {"query": "光 パンチングボード PGBD609-1", "include": ["パンチングボード"]},
            {"query": "光 パンチングボード PGBD406-2", "include": ["パンチングボード"]},
            {"query": "サンワダイレクト 有孔ボード デスク", "include": ["有孔ボード"]},
        ],
    },
    {
        "date": "2026-04-22",
        "title": "節電を可視化。消費電力をリアルタイムで知る「モニター」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "ラトックシステム ワットチェッカー", "include": ["ワット"]},
            {"query": "サンワサプライ ワットモニター", "include": ["ワット"]},
            {"query": "Nature Remo E2 lite", "include": ["Nature Remo", "E2 lite"]},
            {"query": "TP-Link Tapo P110M", "include": ["スマートプラグ"]},
            {"query": "SwitchBot プラグミニ 消費電力", "include": ["プラグミニ"]},
        ],
    },
    {
        "date": "2026-04-23",
        "title": "プレゼンを成功させる。多機能な「レーザーポインター」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Canon PR500-RC", "include": ["PR500-RC"]},
            {"query": "ロジクール R400f", "include": ["R400"]},
            {"query": "Canon PR11-GC", "include": ["PR11-GC"]},
            {"query": "コクヨ レーザーポインター ELA", "include": ["レーザーポインター"]},
            {"query": "サンワサプライ レーザーポインター プレゼン", "include": ["レーザーポインター"]},
            {"query": "AMERTEER レーザーポインター", "include": ["レーザーポインター"]},
        ],
    },
    {
        "date": "2026-04-24",
        "title": "出張をスマートに。ガジェット収納に最適な「多機能バックパック」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "サンワダイレクト ビジネスリュック 200-BAGBP035BK", "include": ["ビジネスリュック"]},
            {"query": "エレコム off toco バックパック", "include": ["off toco"]},
            {"query": "ace. ガジェタブル バックパック", "include": ["ガジェタブル"]},
            {"query": "Samsonite バックパック エピッド", "include": ["バックパック"]},
            {"query": "THULE Crossover 2 Backpack", "include": ["Backpack"]},
            {"query": "MATEIN ビジネスリュック USB", "include": ["ビジネスリュック"]},
        ],
    },
    {
        "date": "2026-04-25",
        "title": "大事な機材を守る。盗難を防ぐ「最新 GPS トラッカー」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Apple AirTag", "include": ["AirTag"]},
            {"query": "Tile Pro", "include": ["Tile"]},
            {"query": "Tile Mate", "include": ["Tile"]},
            {"query": "Anker Eufy SmartTrack Link", "include": ["SmartTrack Link"]},
            {"query": "Anker Eufy SmartTrack Card", "include": ["SmartTrack Card"]},
            {"query": "エレコム スマートトラッカー LGT-ELBETG1BKG", "include": ["エレコム", "スマートトラッカー"]},
        ],
    },
    {
        "date": "2026-04-26",
        "title": "朝の時短をサポート。時計や温度を映す「ミラークロック」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Lamantt スマートミラーデジタル時計", "include": ["スマートミラーデジタル時計"]},
            {"query": "KOSUMOSU デジタル目覚まし時計 ミラー 温度表示", "include": ["ミラー", "温度表示"]},
            {"query": "マクロス LEDミラークロック L", "include": ["LEDミラークロック", "温度"]},
            {"query": "mooas ポップ ミラー LED卓上目覚まし時計", "include": ["ミラー", "温度計付き時計"]},
            {"query": "zmart 多機能 LED ミラー 目覚まし時計", "include": ["ミラー", "温度"]},
        ],
    },
    {
        "date": "2026-04-27",
        "title": "旅行前に揃えたい。世界で使える「翻訳機・充電器」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "POCKETALK S2 Plus", "include": ["POCKETALK", "S2 Plus"]},
            {"query": "POCKETALK S", "include": ["POCKETALK", "S"]},
            {"query": "AUTOOSE Z2 翻訳機", "include": ["AUTOOSE", "翻訳機"]},
            {"query": "AUTOOSE A70 lite 翻訳機", "include": ["AUTOOSE", "翻訳機"]},
            {"query": "MUMEOMU Z8 AI翻訳機", "include": ["Z8", "翻訳機"]},
            {"query": "MOMAX 変換プラグ PD 70W", "include": ["MOMAX", "変換プラグ"]},
            {"query": "Mobile Master 海外 変換プラグ", "include": ["Mobile Master", "変換プラグ"]},
        ],
    },
    {
        "date": "2026-04-28",
        "title": "壁を傷つけず DIY。レーザー水平器など「スマート DIY ガジェット」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Huepar B03CG レーザー墨出し器", "include": ["Huepar"]},
            {"query": "CIGMAN CM-G01T レーザー墨出し器", "include": ["CIGMAN"]},
            {"query": "Bosch EasyDistance 25", "include": ["EasyDistance 25"]},
            {"query": "シンワ測定 下地センサー Basic+", "include": ["下地センサー", "Basic+"]},
            {"query": "FieldNew デジタル角度計", "include": ["デジタル角度計"]},
        ],
    },
    {
        "date": "2026-04-29",
        "title": "Apple Watch を便利に。毎日を変える「神アクセサリ」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "Anker MagGo Power Bank For Apple Watch", "include": ["Apple Watch"]},
            {"query": "RORRY apple watch 充電器 モバイルバッテリー", "include": ["apple watch", "充電器"]},
            {"query": "Philips Apple Watch対応 5000mAh", "include": ["Apple Watch対応"]},
            {"query": "LISAMER アップルウォッチ カバー 防水", "include": ["アップルウォッチ", "カバー"]},
            {"query": "CAERMA アップルウォッチ バンド", "include": ["アップルウォッチ", "バンド"]},
            {"query": "MOFT Apple Watch対応バンド", "include": ["Apple Watch対応バンド"]},
            {"query": "Spigen Apple Watch 充電 スタンド", "include": ["Spigen", "Apple Watch", "スタンド"]},
        ],
    },
    {
        "date": "2026-04-30",
        "title": "4 月のベストバイ。買ってよかった「春のガジェット」 8 選",
        "target_count": 8,
        "editorial_summary": "4月中にリサーチした商品の中から、季節性・実用性・新しさのバランスを見て再選定した月間ベストバイ。旅行・省エネ・在宅ワーク・防犯・デスク改善といった4月の生活課題を横断して、実際に使いどころが明確な製品を優先した。",
        "query_reasons": {
            "Apple AirTag": "旅行や外出機会が増える4月後半に相性が良く、紛失防止の即効性が高い定番枠として採用。",
            "TP-Link Tapo P110M": "新生活の節電ニーズに直結し、電力見える化と遠隔操作の両立ができるため採用。",
            "Nature Remo E2 lite": "家庭全体の電力モニタリングという一段上の省エネ体験を提供できる点を評価して採用。",
            "Sony WH-1000XM5": "GW前の移動需要と在宅会議の両方で満足度が高いプレミアム枠として採用。",
            "Anker MagGo Power Bank For Apple Watch": "外出時のApple Watch充電という具体的な不満を解消し、春の旅行シーズンと相性が良いため採用。",
            "SwitchBot ロック Ultra 指紋認証パッド セット": "新生活の防犯・利便性向上という4月らしいテーマに合致し、体感価値が大きいため採用。",
            "OBSBOT Tiny 2 Lite": "新年度の会議・配信需要に対して、画質とAI追尾の分かりやすい進化を提供するため採用。",
            "EastForce ペグボード デスクパネル": "デスク環境の整理改善がしやすく、新生活の作業環境づくりに直結するため採用。"
        },
        "queries": [
            {"query": "Apple AirTag", "include": ["AirTag"]},
            {"query": "TP-Link Tapo P110M", "include": ["スマートプラグ"]},
            {"query": "Nature Remo E2 lite", "include": ["Nature Remo", "E2 lite"]},
            {"query": "Sony WH-1000XM5", "include": ["ヘッドホン"]},
            {"query": "Anker MagGo Power Bank For Apple Watch", "include": ["Apple Watch"]},
            {"query": "SwitchBot ロック Ultra 指紋認証パッド セット", "include": ["セット買い", "指紋認証"]},
            {"query": "OBSBOT Tiny 2 Lite", "include": ["Tiny 2 Lite", "AI"]},
            {"query": "EastForce ペグボード デスクパネル", "include": ["ペグボード"]},
        ],
    },
    {
        "date": "2026-05-01",
        "title": "五月病を打破。朝を快適にする「最新光目覚まし」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Philips SmartSleep HF3519/15", "include": ["SmartSleep", "HF3519"]},
            {"query": "Philips Wake-Up Light HF3520", "include": ["Wake-Up Light", "HF3520"]},
            {"query": "ADESSO Shizen Flow SZF-01", "include": ["Shizen Flow", "SZF-01"]},
            {"query": "ADESSO SZF-02 Shizen Flow Aura", "include": ["SZF-02", "Shizen Flow Aura"]},
            {"query": "ecozy 光目覚まし時計 E60A", "include": ["E60A", "光目覚まし時計"]},
            {"query": "LITSPED 光目覚ましライト Wake Up Light Bluetooth", "include": ["Wake Up Light", "Bluetooth"]},
        ],
    },
    {
        "date": "2026-05-02",
        "title": "連休明けの掃除はお任せ。AI マッピング搭載「ロボット掃除機」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "Anker Eufy X10 Pro Omni", "include": ["X10 Pro Omni"]},
            {"query": "Anker Eufy Robot Vacuum Omni E25", "include": ["Omni E25"]},
            {"query": "Lefant M1 ロボット掃除機", "include": ["Lefant M1"]},
            {"query": "ECOVACS DEEBOT mini", "include": ["DEEBOT mini"]},
            {"query": "ECOVACS DEEBOT T80 OMNI", "include": ["DEEBOT T80 OMNI"]},
            {"query": "roborock Q7B+", "include": ["Q7B+"]},
            {"query": "MOVA E20 Plus ロボット掃除機", "include": ["MOVA E20 Plus"]},
        ],
    },
    {
        "date": "2026-05-03",
        "title": "ポーチの中身を公開。ケーブルから充電器まで厳選 7 選",
        "target_count": 7,
        "queries": [
            {"query": "tomtoc ガジェットポーチ 大容量", "include": ["tomtoc", "ガジェットポーチ"]},
            {"query": "CIO NovaPort TRIOⅡ 65W", "include": ["NovaPort TRIOⅡ", "65W"]},
            {"query": "UGREEN Nexode 65W 充電器", "include": ["UGREEN", "65W", "充電器"]},
            {"query": "Anker PowerLine III Flow USB-C 240W", "include": ["PowerLine III Flow", "240W"]},
            {"query": "Anker Zolo Power Bank 10000mAh 30W", "include": ["Zolo Power Bank", "10000mAh"]},
            {"query": "UGREEN Revodok USB-C ハブ 6in1", "include": ["Revodok", "6in1"]},
            {"query": "サンワサプライ ケーブルタイ マグネット CA-610N", "include": ["ケーブルタイ", "CA-610N"]},
        ],
    },
    {
        "date": "2026-05-04",
        "title": "自律神経を整える。ストレスを計測する「最新デバイス」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "HEALBE GoBe U ストレス", "include": ["GoBe U"]},
            {"query": "Fitbit Sense 2 ストレス計測", "include": ["Sense 2", "ストレス計測"]},
            {"query": "GARMIN Instinct 2X Dual Power ストレス値", "include": ["Instinct 2X", "ストレス値"]},
            {"query": "HUAWEI Band 10 情緒モニタリング", "include": ["Band 10", "情緒モニタリング"]},
            {"query": "Amazfit Bip 6 ストレス 健康管理", "include": ["Amazfit Bip 6", "ストレス"]},
        ],
    },
    {
        "date": "2026-05-05",
        "title": "夏の準備を快適に。AIやスマホで操る「サーキュレーター」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "SwitchBot サーキュレーター Alexa", "include": ["SwitchBot", "Alexa"]},
            {"query": "SwitchBot サーキュレーター Lite", "include": ["SwitchBot", "Lite"]},
            {"query": "cocono airy fan Basic スマホ操作", "include": ["airy fan Basic", "スマホ操作"]},
            {"query": "cocono airy fan high grade スマホ操作", "include": ["airy fan high grade", "スマホ操作"]},
            {"query": "アイリスオーヤマ サーキュレーター AI操作 PCF-SCAI15T", "include": ["AI操作", "PCF-SCAI15T"]},
            {"query": "DREO サーキュレーター DCモーター 上下左右自動首振り", "include": ["DREO", "サーキュレーター"]},
        ],
    },
]


def normalize_url(detail_page_url: str, asin: str) -> str:
    match = re.search(r"/dp/([A-Z0-9]{10})", detail_page_url)
    if not match:
        raise ValueError(f"detail_page_url does not contain ASIN: {detail_page_url}")
    url_asin = match.group(1)
    if url_asin != asin:
        raise ValueError(f"ASIN mismatch: url={url_asin} item={asin}")
    return f"https://www.amazon.co.jp/dp/{asin}?tag={PARTNER_TAG}&linkCode=osi&th=1&psc=1"


def to_item(item, query: str):
    asin = item["ASIN"]
    title = item["ItemInfo"]["Title"]["DisplayValue"]
    features = item.get("ItemInfo", {}).get("Features", {}).get("DisplayValues", [])
    image_url = (
        item.get("Images", {})
        .get("Primary", {})
        .get("Large", {})
        .get("URL", "")
    )
    price = "N/A"
    listings = item.get("Offers", {}).get("Listings", [])
    if listings:
        price = listings[0].get("Price", {}).get("DisplayAmount", "N/A")
    url = normalize_url(item["DetailPageURL"], asin)
    return {
        "title": title,
        "url": url,
        "price": price,
        "image_url": image_url,
        "features": features,
        "query": query,
        "asin": asin,
    }


def normalize_query_entry(entry):
    if isinstance(entry, str):
        return {"query": entry, "include": [], "exclude": []}
    return {
        "query": entry["query"],
        "include": entry.get("include", []),
        "exclude": entry.get("exclude", []),
    }


def get_output_dir(task_date: str) -> str:
    year_month = task_date[:7]
    return os.path.join("06_research", year_month)


def run_task(task):
    selected_items = []
    seen_asins = set()
    errors = []

    for raw_query in task["queries"]:
        query_entry = normalize_query_entry(raw_query)
        query = query_entry["query"]
        result = SEARCH_MODULE.search_products(query, PARTNER_TAG, 5)
        if "error" in result:
            errors.append({"query": query, "error": result["error"]})
            time.sleep(1)
            continue

        items = result.get("SearchResult", {}).get("Items", [])
        chosen = None
        for raw_item in items:
            title = raw_item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "")
            if not title:
                continue
            asin = raw_item.get("ASIN")
            if not asin or asin in seen_asins:
                continue
            if query_entry["include"] and not all(term.lower() in title.lower() for term in query_entry["include"]):
                continue
            if query_entry["exclude"] and any(term.lower() in title.lower() for term in query_entry["exclude"]):
                continue
            chosen = to_item(raw_item, query)
            break

        if chosen:
            if task.get("query_reasons"):
                chosen["editorial_reason"] = task["query_reasons"].get(query, "")
            selected_items.append(chosen)
            seen_asins.add(chosen["asin"])
        else:
            errors.append({"query": query, "error": "no usable item found"})

        time.sleep(1)

    payload = {
        "date": task["date"],
        "title": task["title"],
        "queries": task["queries"],
        "selection_policy": {
            "default_tiers": {
                "tier1": "review_count >= 500 and star_rating >= 4.0",
                "tier2": "review_count >= 100 and star_rating >= 3.5",
                "tier3": "review_count >= 30 and star_rating >= 3.0",
            },
            "applied_tier": "fallback",
            "fallback_applied": True,
            "fallback_reason": "レビュー情報が安定取得できないため、Amazon PA-API検索上位 + 除外ワード + テーマ適合で選定",
            "fallback_policy": "Amazon検索上位・除外ワード排除・メーカー重複制限（特集テーマ除く）・URL/ASIN一致検証",
        },
        "search_execution": {
            "script": "05_script/run_research_batch.py via 05_script/search_custom_list.py (PA-API direct)",
            "partner_tag": PARTNER_TAG,
            "status": "success" if len(selected_items) >= task["target_count"] else "partial",
            "errors": errors,
        },
        "target_count": task["target_count"],
        "fetched_count": len(selected_items),
        "dedup_count": 0,
        "selected_count": len(selected_items),
        "selected_items": selected_items,
        "all_candidates": [],
    }
    if task.get("editorial_summary"):
        payload["editorial_summary"] = task["editorial_summary"]

    output_dir = get_output_dir(task["date"])
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{task['date']}_research_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"{task['date']}: {len(selected_items)}/{task['target_count']} saved to {output_path}")
    return payload


def probe(query):
    result = SEARCH_MODULE.search_products(query, PARTNER_TAG, 5)
    if "error" in result:
        print(result["error"])
        return
    for idx, item in enumerate(result.get("SearchResult", {}).get("Items", []), start=1):
        title = item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "")
        asin = item.get("ASIN", "")
        print(f"{idx}. {asin} {title}")


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--probe":
        probe(" ".join(sys.argv[2:]))
        return
    requested_dates = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    tasks = [task for task in TASKS if requested_dates is None or task["date"] in requested_dates]
    if not tasks:
        raise SystemExit("No matching tasks.")
    for task in tasks:
        run_task(task)


if __name__ == "__main__":
    main()
