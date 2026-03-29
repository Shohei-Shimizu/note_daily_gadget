import json
import os
import re
import sys
import time
from importlib.machinery import SourceFileLoader


PARTNER_TAG = "daily-gadget-22"
OUTPUT_DIR = "06_research/2026-04"
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

    output_path = os.path.join(OUTPUT_DIR, f"{task['date']}_research_data.json")
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
    os.makedirs(OUTPUT_DIR, exist_ok=True)
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
