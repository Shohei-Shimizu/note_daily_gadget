import sys
from importlib.machinery import SourceFileLoader


BATCH = SourceFileLoader(
    "run_research_batch",
    "05_script/run_research_batch.py",
).load_module()


TASKS = [
    {
        "date": "2026-07-22",
        "title": "キャンプ最強セット。防水「スピーカーとバッテリー」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "JBL Flip 7 防水 Bluetooth スピーカー", "include": ["JBL", "Flip 7"], "exclude": ["ケース", "カバー"]},
            {"query": "Soundcore Boom 2 防水 Bluetooth スピーカー", "include": ["Boom 2"], "exclude": ["ケース", "カバー"]},
            {"query": "Sony ULT FIELD 1 防水 スピーカー", "include": ["ULT FIELD 1"], "exclude": ["ケース", "カバー"]},
            {"query": "Anker Solix C300 DC Portable Power Station", "include": ["Solix", "C300", "Portable Power Station"], "exclude": ["ケース"]},
            {"query": "EcoFlow RIVER 3 ポータブル電源", "include": ["RIVER 3"], "exclude": ["ケース", "バッグ"]},
            {"query": "Jackery ポータブル電源 240 New", "include": ["Jackery", "240 New"], "exclude": ["ソーラーパネル", "セット"]},
        ],
    },
    {
        "date": "2026-07-23",
        "title": "旅日記を声で書く。高精度な「音声入力マイク」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "SHURE MV7+ USB マイク", "include": ["MV7+"], "exclude": ["アーム", "スタンド", "ケーブル"]},
            {"query": "RODE NT-USB+ USB マイク", "include": ["NT-USB"], "exclude": ["整備済み", "ケーブル"]},
            {"query": "Audio-Technica AT2020USB-X マイク", "include": ["AT2020USB-X"], "exclude": ["アーム", "ケーブル"]},
            {"query": "Elgato Wave 3 USB マイク", "include": ["Wave:3"], "exclude": ["アーム", "ケーブル"]},
            {"query": "HyperX SoloCast USB マイク", "include": ["SoloCast"], "exclude": ["アーム", "ケーブル"]},
            {"query": "FIFINE AM8 USB マイク", "include": ["FIFINE", "AM8"], "exclude": ["ケーブルセット"]},
        ],
    },
    {
        "date": "2026-07-24",
        "title": "旅行中の家を守る。スマホで確認できる「スマートカメラ」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "TP-Link Tapo C225 見守りカメラ", "include": ["Tapo", "C225"], "exclude": ["ブラケット", "ケース"]},
            {"query": "TP-Link Tapo C210 見守りカメラ", "include": ["Tapo", "C210"], "exclude": ["ブラケット", "ケース"]},
            {"query": "SwitchBot 見守りカメラ Plus 5MP", "include": ["SwitchBot", "見守りカメラ"], "exclude": ["ブラケット", "ケース"]},
            {"query": "Anker Eufy Indoor Cam C220", "include": ["C220"], "exclude": ["ブラケット", "ケース"]},
            {"query": "ATOM Cam 2 ネットワークカメラ", "include": ["ATOM", "Cam 2"], "exclude": ["ブラケット", "ケース"]},
            {"query": "Google GA01317-JP Nest Cam", "include": ["Google", "Nest Cam"], "exclude": ["マウント", "ケース", "ケーブル", "ドアベル"]},
            {"query": "Panasonic KX-HRC100 見守りカメラ", "include": ["KX-HRC100"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-07-25",
        "title": "ルーティンを全自動化。IFTTT 対応の「スマート連携」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "SwitchBot ハブ2 スマートリモコン", "include": ["SwitchBot", "ハブ2"], "exclude": ["セット"]},
            {"query": "Nature Remo 3 スマートリモコン", "include": ["Nature Remo 3"], "exclude": ["ケーブル"]},
            {"query": "Philips Hue ブリッジ", "include": ["Hue", "ブリッジ"], "exclude": ["電球セット"]},
            {"query": "TP-Link Tapo P110M スマートプラグ", "include": ["Tapo", "P110M"], "exclude": ["セット"]},
            {"query": "Meross Matter スマートプラグ", "include": ["Meross", "スマートプラグ"], "exclude": ["電源タップ"]},
            {"query": "SwitchBot ボット スイッチ", "include": ["SwitchBot", "ボット"], "exclude": ["セット"]},
        ],
    },
    {
        "date": "2026-07-26",
        "title": "クリエイター必見。作業を加速させる「ダイヤルデバイス」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "TourBox Elite Plus 左手デバイス", "include": ["TourBox", "Elite Plus"], "exclude": ["ケース"]},
            {"query": "TourBox NEO 左手デバイス", "include": ["TourBox", "NEO"], "exclude": ["ケース"]},
            {"query": "Elgato Stream Deck Plus 本体", "include": ["Stream Deck +", "ダイヤル"], "exclude": ["専用", "Dials", "スタンド", "ケース"]},
            {"query": "Loupedeck Live S 編集コントローラー", "include": ["Loupedeck", "Live S"], "exclude": ["ケース"]},
            {"query": "XP-PEN ACK05 ワイヤレスショートカットリモート", "include": ["ACK05"], "exclude": ["ケース"]},
            {"query": "HUION Keydial Mini Bluetooth K20", "include": ["Keydial", "Mini"], "exclude": ["ケース"]},
            {"query": "8BitDo Micro Bluetooth ゲームパッド 左手デバイス", "include": ["8BitDo", "Micro"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-07-27",
        "title": "海外旅行の会話を攻略。最新の「AI 翻訳イヤホン」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Timekettle W4 Pro AI 通訳イヤホン", "include": ["W4 Pro"], "exclude": ["ケース", "イヤーピース"]},
            {"query": "Timekettle WT2 Edge W3 翻訳機", "include": ["Timekettle", "WT2"], "exclude": ["ケース", "イヤーピース"]},
            {"query": "Timekettle M3 翻訳イヤホン", "include": ["Timekettle", "M3"], "exclude": ["ケース", "イヤーピース"]},
            {"query": "Vasco Translator E1 翻訳イヤホン", "include": ["Vasco", "E1"], "exclude": ["ケース", "イヤーピース"]},
            {"query": "iFLYTEK 翻訳イヤホン", "include": ["翻訳", "イヤホン"], "exclude": ["ケース", "イヤーピース"]},
            {"query": "Wooask M6 翻訳イヤホン", "include": ["Wooask", "M6"], "exclude": ["ケース", "イヤーピース"]},
        ],
    },
    {
        "date": "2026-07-28",
        "title": "太陽光でフル充電。折りたたみ「ソーラーパネル」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Anker Solix PS100 ソーラーパネル", "include": ["Anker", "PS100"], "exclude": ["延長ケーブル"]},
            {"query": "EcoFlow 160W 軽量両面 ソーラーパネル", "include": ["EcoFlow", "160W", "ソーラーパネル"], "exclude": ["2点セット"]},
            {"query": "Jackery SolarSaga 100 ソーラーパネル", "include": ["SolarSaga", "100"], "exclude": ["延長ケーブル"]},
            {"query": "BLUETTI 100W ソーラーパネル", "include": ["BLUETTI", "100W", "ソーラーパネル"], "exclude": ["セット"]},
            {"query": "ALLPOWERS 100W 折りたたみ ソーラーパネル", "include": ["ALLPOWERS", "100W", "折りたたみ"], "exclude": ["セット"]},
            {"query": "BigBlue 28W ソーラーチャージャー", "include": ["BigBlue", "28W"], "exclude": ["延長ケーブル"]},
        ],
    },
    {
        "date": "2026-07-29",
        "title": "公園でワーク。膝上テーブルと「軽量アウトドアチェア」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "サンワダイレクト 膝上テーブル クッション", "include": ["膝上", "テーブル"], "exclude": ["交換"]},
            {"query": "Yogibo Traybo 2.0 膝上テーブル", "include": ["Traybo"], "exclude": ["カバー"]},
            {"query": "HUANUO 膝上テーブル ノートパソコン", "include": ["膝上", "テーブル"], "exclude": ["交換"]},
            {"query": "Helinox チェアワン 軽量 アウトドアチェア", "include": ["チェアワン"], "exclude": ["カバー", "脚"]},
            {"query": "MOON LENCE アウトドアチェア 軽量", "include": ["MOON LENCE", "チェア"], "exclude": ["カバー"]},
            {"query": "Coleman ヒーリングチェア NX", "include": ["ヒーリングチェア"], "exclude": ["カバー"]},
        ],
    },
    {
        "date": "2026-07-30",
        "title": "夜を彩る。LED ランタンと「スマート間接照明」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "BALMUDA The Lantern LED ランタン", "include": ["BALMUDA", "Lantern"], "exclude": ["ケース"]},
            {"query": "Coleman ハンギング Eライト LED", "include": ["ハンギング", "ライト"], "exclude": ["ケース"]},
            {"query": "GENTOS Explorer LED ランタン EX-1300D", "include": ["EX-1300D"], "exclude": ["ケース"]},
            {"query": "Philips Hue Go 2 ポータブルライト", "include": ["Hue", "Go"], "exclude": ["ケース"]},
            {"query": "SwitchBot テープライト 3", "include": ["SwitchBot", "テープライト"], "exclude": ["コネクタ"]},
            {"query": "SwitchBot RGBIC フロアライト", "include": ["SwitchBot", "フロアライト"], "exclude": ["部品"]},
        ],
    },
    {
        "date": "2026-07-31",
        "title": "7 月のベストバイ。買ってよかった「夏のガジェット」 8 選",
        "target_count": 8,
        "editorial_summary": "7月に扱った商品の中から、猛暑対策、旅行、撮影、データ保護、屋外作業の実用性を横断して再選定した月間ベストバイ。用途が明確で、夏の外出や仕事環境を具体的に改善しやすい製品を優先した。",
        "query_reasons": {
            "SONY REON POCKET PRO RNPK-P1": "猛暑対策を代表するウェアラブル冷却デバイスとして採用。",
            "IETS GT600 ノートパソコンクーラー": "高負荷作業時の熱対策という夏のPC課題に直結するため採用。",
            "DJI Osmo Mobile 7P スマホジンバル": "旅行動画を安定して残せる撮影系の代表として採用。",
            "SanDisk Extreme PRO microSDXC 512GB": "4K撮影の保存基盤として汎用性と用途の分かりやすさを評価。",
            "Samsung T7 Shield 2TB ポータブルSSD": "旅先での高速バックアップと耐久性を両立する保存機器として採用。",
            "GL.iNet GL-MT3600BE Beryl 7 トラベルルーター": "出先の通信環境を整える旅行・仕事兼用ガジェットとして採用。",
            "Yubico YubiKey 5 NFC セキュリティキー": "夏の旅行中もアカウント保護を強化できるセキュリティ枠として採用。",
            "JBL Flip 7 防水 Bluetooth スピーカー": "屋外レジャーで使いやすい防水オーディオの代表として採用。",
        },
        "queries": [
            {"query": "SONY REON POCKET PRO RNPK-P1", "include": ["REON POCKET PRO"], "exclude": ["ケース"]},
            {"query": "IETS GT600 ノートパソコンクーラー", "include": ["GT600"], "exclude": ["交換"]},
            {"query": "DJI Osmo Mobile 7P スマホジンバル", "include": ["Osmo Mobile 7P"], "exclude": ["ケース"]},
            {"query": "SanDisk Extreme PRO microSDXC 512GB", "include": ["Extreme PRO", "512GB"], "exclude": ["リーダーセット"]},
            {"query": "Samsung T7 Shield 2TB ポータブルSSD", "include": ["T7 Shield", "2TB"], "exclude": ["ケース"]},
            {"query": "GL.iNet GL-MT3600BE Beryl 7 トラベルルーター", "include": ["GL-MT3600BE", "Beryl 7"], "exclude": ["ケース"]},
            {"query": "Yubico YubiKey 5 NFC セキュリティキー", "include": ["YubiKey 5 NFC"], "exclude": ["ケース", "カバー"]},
            {"query": "JBL Flip 7 防水 Bluetooth スピーカー", "include": ["JBL", "Flip 7"], "exclude": ["ケース", "カバー"]},
        ],
    },
]


def main():
    requested_dates = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    tasks = [
        task
        for task in TASKS
        if requested_dates is None or task["date"] in requested_dates
    ]
    if not tasks:
        raise SystemExit("No matching tasks.")
    for task in tasks:
        BATCH.run_task(task)


if __name__ == "__main__":
    main()
