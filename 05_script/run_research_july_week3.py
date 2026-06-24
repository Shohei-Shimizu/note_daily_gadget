import sys
from importlib.machinery import SourceFileLoader


BATCH = SourceFileLoader(
    "run_research_batch",
    "05_script/run_research_batch.py",
).load_module()


TASKS = [
    {
        "date": "2026-07-15",
        "title": "パスワードを卒業。高度なセキュリティを実現する「セキュリティキー」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Yubico YubiKey 5 NFC セキュリティキー", "include": ["YubiKey 5 NFC"], "exclude": ["ケース", "カバー"]},
            {"query": "Yubico Security Key C NFC", "include": ["Security Key C NFC"], "exclude": ["ケース", "カバー"]},
            {"query": "Identiv uTrust FIDO2 NFC セキュリティキー", "include": ["Identiv", "FIDO2", "NFC"], "exclude": ["ケース", "カバー"]},
            {"query": "FEITIAN ePass K40 FIDO2 NFC", "include": ["FEITIAN", "ePass K40"], "exclude": ["ケース", "カバー"]},
            {"query": "AuthenTrend ATKey.Pro Zinc USB-C FIDO2", "include": ["ATKey.Pro", "USB-C", "FIDO2"], "exclude": ["ケース", "カバー"]},
        ],
    },
    {
        "date": "2026-07-16",
        "title": "旅先で写真共有。自分専用の「パーソナルクラウド」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Synology BeeStation 4TB パーソナルクラウド", "include": ["BeeStation", "4TB"], "exclude": ["ケース", "交換"]},
            {"query": "UGREEN NASync DXP2800 NAS", "include": ["DXP2800"], "exclude": ["ケース", "メモリ"]},
            {"query": "バッファロー LinkStation LS720D 4TB", "include": ["LS720D", "4TB"], "exclude": ["交換", "ケース"]},
            {"query": "アイオーデータ HDL2-TA4 NAS 4TB", "include": ["HDL2-TA4"], "exclude": ["交換", "ケース"]},
            {"query": "QNAP TS-233 NAS", "include": ["TS-233"], "exclude": ["ケース", "メモリ"]},
        ],
    },
    {
        "date": "2026-07-17",
        "title": "旅行の相談を AI に。音声入力に強い「AI デバイス」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "PLAUD NotePin AI ボイスレコーダー", "include": ["PLAUD", "NotePin"], "exclude": ["ケース", "ストラップ"]},
            {"query": "iFLYTEK AINOTE Air 2 AI ボイスレコーダー", "include": ["AINOTE Air 2"], "exclude": ["ケース", "フィルム"]},
            {"query": "iFLYTEK AIライティングレコーダー VOITER SR502J", "include": ["VOITER", "SR502J"], "exclude": ["ケース"]},
            {"query": "Timekettle W4 Pro AI 通訳イヤホン", "include": ["W4 Pro"], "exclude": ["ケース", "イヤーピース"]},
            {"query": "Vasco Translator V4 翻訳機", "include": ["Vasco", "V4"], "exclude": ["ケース", "フィルム"]},
        ],
    },
    {
        "date": "2026-07-18",
        "title": "ホテルや出先の Wi-Fi を中継。持ち運べる「トラベルルーター」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "GL.iNet GL-MT3600BE Beryl 7 トラベルルーター", "include": ["GL-MT3600BE", "Beryl 7"], "exclude": ["CaseSack", "ケース"]},
            {"query": "GL.iNet GL-AXT1800 Slate AX トラベルルーター", "include": ["GL-AXT1800", "Slate AX"], "exclude": ["CaseSack", "ケース"]},
            {"query": "TP-Link TL-WR802N ホテル WiFi ルーター", "include": ["TP-Link", "TL-WR802N"], "exclude": ["ブラケット", "ケース"]},
            {"query": "エレコム ホテルルーター WRH-300BK3", "include": ["エレコム", "WRH-300BK3"], "exclude": ["ケース"]},
            {"query": "バッファロー トラベルルーター WMR-433W2-BK", "include": ["BUFFALO", "WMR-433W2-BK"], "exclude": ["ケース"]},
            {"query": "プラネックス ちびファイ4 MZK-DP300N", "include": ["MZK-DP300N", "小型"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-07-19",
        "title": "家族の予定を共有。壁掛け対応の「スマートディスプレイ」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Amazon Echo Show 15 スマートディスプレイ", "include": ["Echo Show 15"], "exclude": ["スタンド", "ホルダー", "保護"]},
            {"query": "Acogedor 15.6インチ デジタルカレンダー 家族", "include": ["Acogedor", "デジタルカレンダー"], "exclude": ["プロテクター", "保護"]},
            {"query": "Hibeauty 15.6インチ スマートデジタルカレンダー", "include": ["Hibeauty", "デジタルカレンダー"], "exclude": ["プロテクター", "保護"]},
            {"query": "Hirelax スマートデジタルカレンダー 15.6インチ", "include": ["Hirelax", "デジタルカレンダー"], "exclude": ["プロテクター", "保護"]},
            {"query": "NEWYES デジタル家族カレンダー 15.6インチ", "include": ["NEWYES", "デジタル家族カレンダー"], "exclude": ["プロテクター", "保護"]},
        ],
    },
    {
        "date": "2026-07-20",
        "title": "生成 AI を使いこなす。文章・画像作成に適した「AI PC」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "Microsoft Surface Laptop 13 Snapdragon X Plus", "include": ["Surface Laptop", "Snapdragon X Plus"], "exclude": ["ケース", "フィルム", "充電器"]},
            {"query": "ASUS Vivobook S 14 Copilot+ PC Ryzen AI", "include": ["Vivobook S 14", "Ryzen AI"], "exclude": ["ケース", "フィルム"]},
            {"query": "Lenovo Yoga Slim 7i Aura Edition Core Ultra", "include": ["Yoga Slim 7i", "Core Ultra"], "exclude": ["ケース", "フィルム"]},
            {"query": "HP OmniBook Ultra Flip AI PC", "include": ["OmniBook", "Ultra Flip"], "exclude": ["ケース", "フィルム"]},
            {"query": "Dell XPS 13 Copilot+ PC Snapdragon X Elite", "include": ["XPS 13", "Snapdragon"], "exclude": ["ケース", "フィルム"]},
            {"query": "Acer Swift 14 AI Copilot+ PC", "include": ["Swift 14 AI"], "exclude": ["ケース", "フィルム"]},
            {"query": "Apple MacBook Air M4 15インチ", "include": ["MacBook Air", "M4", "15"], "exclude": ["ケース", "フィルム", "充電器"]},
        ],
    },
    {
        "date": "2026-07-21",
        "title": "ビーチでも仕事。屋外に持ち出せる「タフネスタブレット」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Kayoote SS9 Pro タフネスタブレット", "include": ["Kayoote", "SS9 Pro", "IP68"], "exclude": ["ケース", "フィルム"]},
            {"query": "Kayoote SS9 Ultra タフネスタブレット", "include": ["Kayoote", "SS9 Ultra", "IP68"], "exclude": ["ケース", "フィルム"]},
            {"query": "FOSSiBOT DT3 防水 タブレット", "include": ["FOSSiBOT", "DT3", "防水"], "exclude": ["ケース", "フィルム"]},
            {"query": "Ulefone Armor Pad Pro 防水 タブレット", "include": ["Ulefone", "Armor Pad Pro", "防水"], "exclude": ["ケース", "フィルム"]},
            {"query": "HOTWAV R7 頑丈 タブレット", "include": ["HOTWAV", "R7", "防水"], "exclude": ["ケース", "フィルム"]},
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
