import sys
from importlib.machinery import SourceFileLoader


BATCH = SourceFileLoader(
    "run_research_batch",
    "05_script/run_research_batch.py",
).load_module()


TASKS = [
    {
        "date": "2026-07-08",
        "title": "4K 動画を撮りまくる。高耐久・大容量「microSD カード」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "SanDisk Extreme PRO microSDXC 256GB SDSQXCD", "include": ["microSD", "256GB"], "exclude": ["ケース", "リーダー"]},
            {"query": "Samsung PRO Plus microSD 512GB MB-MD512", "include": ["PRO Plus", "512GB"], "exclude": ["ケース", "リーダー"]},
            {"query": "KIOXIA microSD 256GB 高耐久 KLMHB256G", "include": ["KIOXIA", "高耐久", "256GB"], "exclude": ["ケース", "リーダー"]},
            {"query": "Lexar PLAY PRO microSDXC Express 512GB", "include": ["PLAY PRO", "microSDXC", "512GB"], "exclude": ["ケース", "リーダー"]},
            {"query": "Kingston Canvas Go Plus microSD 256GB", "include": ["Canvas Go", "256GB"], "exclude": ["ケース", "リーダー"]},
            {"query": "Transcend microSD 256GB TS256GUSD300S", "include": ["Transcend", "256GB", "TS256GUSD300S"], "exclude": ["ケース", "リーダー"]},
            {"query": "Gigastone 4K Camera Pro microSD 256GB", "include": ["microSD", "256GB"], "exclude": ["ケース", "リーダー"]},
        ],
    },
    {
        "date": "2026-07-09",
        "title": "夏フェスで耳を守る。音質を損なわない「ライブ用耳栓」 5 選",
        "target_count": 5,
        "queries": [
            {"query": "Loop Experience 2 耳栓 ライブ", "include": ["Loop", "Experience"], "exclude": ["ケース", "ミュート"]},
            {"query": "Etymotic Research ER20XS 高音質 耳栓", "include": ["ER20XS"], "exclude": ["ケース"]},
            {"query": "Alpine MusicSafe Pro ライブ 耳栓", "include": ["MusicSafe"], "exclude": ["ケース"]},
            {"query": "EarPeace Music Pro ライブ用 耳栓", "include": ["EarPeace", "Music"], "exclude": ["ケース"]},
            {"query": "Vibes High Fidelity Earplugs ライブ 耳栓", "include": ["Vibes"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-07-10",
        "title": "デスクの暑さを和らげる。卓上で使える「コンパクトファン」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "リズム Silky Wind Mini 9ZF038RH", "include": ["Silky Wind Mini"], "exclude": ["フィルター"]},
            {"query": "ドウシシャ 卓上扇風機 スリムコンパクト FSV", "include": ["卓上", "扇風機"], "exclude": ["フィルター"]},
            {"query": "エレコム USB扇風機 FAN-U177", "include": ["FAN-U177"], "exclude": ["フィルター"]},
            {"query": "サンワサプライ USB扇風機 USB-TOY101", "include": ["USB", "扇風機"], "exclude": ["フィルター"]},
            {"query": "山善 卓上扇風機 YDS-FT13", "include": ["YDS-FT13"], "exclude": ["フィルター"]},
            {"query": "KEYNICE 卓上扇風機 KN-618", "include": ["卓上", "扇風機"], "exclude": ["フィルター"]},
            {"query": "BRUNO ポータブルミニファン BDE029", "include": ["BRUNO", "ファン"], "exclude": ["フィルター"]},
        ],
    },
    {
        "date": "2026-07-11",
        "title": "旅の写真を即保存。SD リーダーと「超高速 SSD」 6 選",
        "target_count": 6,
        "queries": [
            {"query": "Anker USB-C 2-in-1 カードリーダー SD microSD", "include": ["Anker", "カードリーダー"], "exclude": ["ケース"]},
            {"query": "UGREEN USB C SDカードリーダー UHS-II", "include": ["カードリーダー", "UHS-II"], "exclude": ["ケース"]},
            {"query": "ProGrade Digital UHS-II SDカードリーダー", "include": ["ProGrade", "カードリーダー"], "exclude": ["ケース"]},
            {"query": "Samsung Portable SSD T9 2TB", "include": ["T9", "2TB"], "exclude": ["ケース", "ケーブル"]},
            {"query": "SanDisk Extreme PRO Portable SSD 2TB", "include": ["Extreme PRO", "SSD", "2TB"], "exclude": ["ケース", "ケーブル"]},
            {"query": "Crucial X10 Pro 2TB CT2000X10PROSSD9", "include": ["X10Pro", "2TB"], "exclude": ["ケース", "ケーブル"]},
        ],
    },
    {
        "date": "2026-07-12",
        "title": "長距離移動を快適に。機内で役立つ「タブレットアクセサリ」6 選",
        "target_count": 6,
        "queries": [
            {"query": "MOFT Snap フロートスタンド iPad", "include": ["MOFT", "スタンド"], "exclude": ["シール"]},
            {"query": "ロジクール KEYS TO GO 2 iK1043GRU", "include": ["KEYS TO GO 2", "iK1043"], "exclude": ["ケース", "カバー"]},
            {"query": "Anker Nano Power Bank 10000mAh 30W", "include": ["10000mAh", "30W"], "exclude": ["ケース"]},
            {"query": "UGREEN タブレットスタンド 折りたたみ", "include": ["タブレット", "スタンド"], "exclude": ["ケース"]},
            {"query": "Twelve South AirFly Pro Bluetooth トランスミッター", "include": ["AirFly Pro"], "exclude": ["ケース"]},
            {"query": "Anker 555 USB-C ハブ 8-in-1", "include": ["Anker", "USB-C", "ハブ"], "exclude": ["ケース"]},
        ],
    },
    {
        "date": "2026-07-13",
        "title": "大事なデータを暗号化。情報漏洩を防ぐ「USB メモリ・SSD ケース」 4 選",
        "target_count": 4,
        "queries": [
            {"query": "アイ・オー・データ ED-FP 指紋認証 USBメモリ", "include": ["ED-FP"], "exclude": ["ケース"]},
            {"query": "iStorage datAshur PRO2 64GB", "include": ["datAshur PRO2", "64GB"], "exclude": ["ケース"]},
            {"query": "StarTech S251BMU3FP 指紋認証 SSDケース", "include": ["StarTech", "指紋認証"], "exclude": ["フィルム"]},
            {"query": "VCOM 指紋認証 SSDケース M.2 NVMe SATA", "include": ["VCOM", "指紋認証", "SSDケース"], "exclude": ["フィルム"]},
        ],
    },
    {
        "date": "2026-07-14",
        "title": "夏休みの自由研究に。子供の学びを支える「プログラミング・知育機器」 7 選",
        "target_count": 7,
        "queries": [
            {"query": "Makeblock mBot2 プログラミング ロボット", "include": ["mBot2"], "exclude": ["部品", "タイヤ"]},
            {"query": "LEGO Education SPIKE Essential", "include": ["SPIKE", "Essential"], "exclude": ["収納"]},
            {"query": "Sphero Mini プログラミング ロボット", "include": ["Sphero Mini"], "exclude": ["ケース"]},
            {"query": "micro:bit v2 スターターキット 子供", "include": ["micro:bit", "キット"], "exclude": ["ケース"]},
            {"query": "Osmo Genius Starter Kit iPad 日本語", "include": ["Osmo", "Genius"], "exclude": ["ケース"]},
            {"query": "embot プログラミング ロボット", "include": ["embot"], "exclude": ["書籍"]},
            {"query": "ソニー KOOV プログラミング 学習キット", "include": ["KOOV"], "exclude": ["ケース"]},
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
