#!/usr/bin/env python3
"""Aggregate Amazon product mentions by note magazine."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTICLE_ROOT = REPO_ROOT / "02_article"
OUTPUT_DIR = REPO_ROOT / "06_research" / "idea_lists"
OUTPUT_PATH = OUTPUT_DIR / "by_magazine.json"
FAILURE_PATH = OUTPUT_DIR / "extraction_failures.json"

MAGAZINES = [
    "🏠 デスク環境を整える",
    "🎧 音響・映像クリエイター向け",
    "🎒 モバイル・外出作業グッズ",
    "🏡 スマートホーム・生活改善",
    "🤖 AI・生産性ツール",
]

CATEGORY_TO_MAGAZINE = {
    "ワークスペース・デスク環境の最適化": "🏠 デスク環境を整える",
    "コミュニケーション・会議・音声": "🎧 音響・映像クリエイター向け",
    "モバイル・電源・周辺機器": "🎒 モバイル・外出作業グッズ",
    "スマートホーム・ライフスタイル・健康管理": "🏡 スマートホーム・生活改善",
    "生産性向上・クリエイティブ・入力機器": "🤖 AI・生産性ツール",
    "生産性向上・クリティブ・入力機器": "🤖 AI・生産性ツール",
}

SUBCATEGORY_RULES = {
    "🏠 デスク環境を整える": [
        ("ノートPCスタンド", ["ノートPC", "ノート PC", "PCスタンド", "PC スタンド", "ノートパソコンスタンド", "クラムシェル", "BookArc", "縦置き"]),
        ("デスクマット", ["デスクマット"]),
        ("昇降デスク", ["昇降デスク", "電動デスク"]),
        ("モニターアーム", ["モニターアーム", "ディスプレイアーム"]),
        ("照明", ["デスクライト", "Z-Light", "MindDuo", "ライト"]),
        ("チェア", ["チェア", "椅子"]),
        ("ハブ・ドック", ["ハブ", "Hub", "ドック", "Dock"]),
        ("その他", []),
    ],
    "🎧 音響・映像クリエイター向け": [
        ("ボイスレコーダー", ["ボイスレコーダー", "Plaud", "VOICE AI"]),
        ("ウェブカメラ", ["ウェブカメラ", "Webcam", "Logicool C", "Facecam", "Kiyo", "PowerConf C", "Insta360 Link"]),
        ("マイク", ["マイク", "Mic"]),
        ("ヘッドホン・イヤホン", ["ヘッドホン", "イヤホン", "Headphone", "Headphones", "Earphone", "Earbuds", "AirPods", "Soundcore"]),
        ("配信ライト", ["Lume", "ライト", "Lighting"]),
        ("オーディオIF", ["インターフェース", "Interface", "Audient", "Focusrite"]),
        ("その他", []),
    ],
    "🎒 モバイル・外出作業グッズ": [
        ("ケーブル", ["ケーブル", "Cable"]),
        ("モバイルバッテリー", ["モバイルバッテリー", "PowerBank", "SMARTCOBY"]),
        ("充電器・充電ステーション", ["充電器", "充電ステーション", "Charger", "MagGo"]),
        ("アクションカメラ", ["GoPro", "Osmo Action", "Insta360", "AKASO"]),
        ("ストレージ", ["SSD", "HDD"]),
        ("PC周辺", ["スタンド", "ハブ", "Hub"]),
        ("車載・作業テーブル", ["車載テーブル", "リアトレイ", "リアシートトレイ"]),
        ("その他", []),
    ],
    "🏡 スマートホーム・生活改善": [
        ("スマートハブ・リモコン", ["ハブ", "Hub", "Nature Remo", "Echo"]),
        ("スマートプラグ", ["スマートプラグ", "プラグ", "Tapo P"]),
        ("スマート照明", ["LED電球", "電球"]),
        ("センサー", ["センサー", "開閉", "Tapo H"]),
        ("カメラ", ["Tapo D", "カメラ"]),
        ("美容", ["Dyson", "Supersonic", "美容"]),
        ("睡眠", ["ブレインスリープ", "睡眠"]),
        ("フィットネス", ["Xiser", "STEADY", "トレーナー", "ステッパー"]),
        ("時短家電", ["THANKO", "ラクア", "食洗機"]),
        ("空調・除湿", ["YDC", "除湿", "サーキュレーター", "Vornado"]),
        ("アロマ", ["アロマ", "アロモア"]),
        ("その他", []),
    ],
    "🤖 AI・生産性ツール": [
        ("スマートペン", ["smartpen", "SyncPen", "NEWYES", "Neo smartpen", "Ophaya", "Livescribe", "LAMY", "iFLYTEK"]),
        ("デジタルノート", ["Kindle Scribe", "フリーノ", "Boox", "リマカブル"]),
        ("Kindle・電子書籍", ["Kindle Paperwhite", "Kindle Oasis"]),
        ("タイマー", ["Time Timer", "タイムアップ", "dretec"]),
        ("コントローラー", ["MX クリエイティブ", "Stream Deck", "コンソール"]),
        ("ペンタブ・入力", ["XPPen", "ペンタブ", "Wacom"]),
        ("照明", ["BenQ", "Z-Light", "MindDuo", "デスクライト", "SQ-LD", "PDL", "Hue Go", "テーブルランプ"]),
        ("その他", []),
    ],
}

KNOWN_BRANDS = [
    "Amazon Kindle",
    "Amazon Echo",
    "Anker MagGo",
    "Twelve South",
    "Nature Remo",
    "Time Timer",
    "Neo smartpen",
    "Kindle Scribe",
    "MX クリエイティブ",
    "TP-Link",
    "山崎実業",
    "SwitchBot",
    "BenQ",
    "GoPro",
    "Insta360",
    "AKASO",
    "Logicool",
    "ロジクール",
    "Razer",
    "Elgato",
    "SMARTCOBY",
    "CIO",
    "UGREEN",
    "サンワダイレクト",
    "サンワサプライ",
    "FlexiSpot",
    "Spigen",
    "SATECHI",
    "エレコム",
    "Buffalo",
    "バッファロー",
    "Plaud",
    "VOICE AI",
    "Bouoke",
    "Mugukue",
    "Adelagnes",
    "NEWYES",
    "Ophaya",
    "Livescribe",
    "LAMY",
    "iFLYTEK",
    "dretec",
    "XPPen",
    "キングジム",
    "ブレインスリープ",
    "Dyson",
    "THANKO",
    "STEADY",
    "Xiser",
    "山田照明",
    "Lume Cube",
    "山善",
    "LOE",
    "ミワックス",
    "DJI",
    "Bose",
    "Apple",
    "HyperX",
    "オーディオテクニカ",
    "MOFT",
    "セイワ",
    "星光産業",
    "生活の木",
    "パナソニック",
    "アイリスオーヤマ",
    "Philips",
    "ERGOTRON",
    "Anker",
]

AMAZON_URL_RE = re.compile(
    r"https://(?:www\.amazon\.co\.jp/(?:dp|gp/product)/[A-Z0-9]{10}(?:[/?#][^\s<>)\"']*)?|amzn\.to/[A-Za-z0-9_-]+(?:[/?#][^\s<>)\"']*)?)"
)
ASIN_RE = re.compile(r"https://www\.amazon\.co\.jp/(?:dp|gp/product)/([A-Z0-9]{10})(?:[/?#]|$)")
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
PRODUCT_NAME_PREFIX_RE = re.compile(
    r"^(?:[①-⑳]|[0-9０-９]+\s*[.．、)）]|[(（][0-9０-９]+[)）]|No\.?\s*[0-9０-９]+|#\s*[0-9０-９]+|[★◆●■▼▲☆◇○□▽△])\s*",
    re.IGNORECASE,
)
PRODUCT_NAME_SUFFIX_RE = re.compile(r"[\s　\t.,、。]+$")
FALLBACK_BRAND_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9+._-]*|[ァ-ヶー]+)")


@dataclass
class ArticleMention:
    article: str
    mentioned_date: str
    product_name: str
    amazon_url: str
    asin: str | None


@dataclass
class ProductAggregate:
    asin: str | None
    product_name: str
    amazon_url: str
    articles: dict[str, ArticleMention] = field(default_factory=dict)

    def add(self, mention: ArticleMention) -> None:
        existing = self.articles.get(mention.article)
        if existing and existing.mentioned_date >= mention.mentioned_date:
            return
        self.articles[mention.article] = mention
        if mention.mentioned_date >= self.last_mentioned:
            self.product_name = mention.product_name
            self.amazon_url = mention.amazon_url

    @property
    def appear_count(self) -> int:
        return len(self.articles)

    @property
    def last_mentioned(self) -> str:
        if not self.articles:
            return ""
        return max(mention.mentioned_date for mention in self.articles.values())

    @property
    def source_articles(self) -> list[str]:
        mentions = sorted(
            self.articles.values(),
            key=lambda mention: (mention.mentioned_date, mention.article),
            reverse=True,
        )
        return [mention.article for mention in mentions[:10]]


def load_metadata(month_dir: Path) -> dict[str, dict[str, Any]]:
    metadata_path = month_dir / "_metadata.json"
    if not metadata_path.exists():
        return {}
    with metadata_path.open(encoding="utf-8") as f:
        payload = json.load(f)
    articles = payload.get("articles", [])
    return {
        article.get("filename", ""): article
        for article in articles
        if isinstance(article, dict) and article.get("filename")
    }


def normalize_magazine(article_meta: dict[str, Any]) -> tuple[str | None, str | None]:
    magazine = article_meta.get("magazine")
    if magazine in MAGAZINES:
        return magazine, None
    if magazine:
        return None, f"unknown_magazine:{magazine}"

    category = article_meta.get("category")
    mapped = CATEGORY_TO_MAGAZINE.get(category)
    if mapped:
        return mapped, "mapped_from_category"
    return None, "missing_magazine"


def canonical_url(url: str, asin: str | None) -> str:
    if asin:
        return f"https://www.amazon.co.jp/dp/{asin}"
    return url.rstrip(".,、。)")


def product_key(url: str, asin: str | None) -> str:
    if asin:
        return f"asin:{asin}"
    return f"url:{canonical_url(url, None)}"


def clean_product_name(name: str) -> str:
    cleaned = name.strip()
    while True:
        next_cleaned = PRODUCT_NAME_PREFIX_RE.sub("", cleaned, count=1).lstrip()
        if next_cleaned == cleaned:
            break
        cleaned = next_cleaned
    return PRODUCT_NAME_SUFFIX_RE.sub("", cleaned).strip()


def classify_subcategory(magazine: str, product_name: str) -> str:
    rules = SUBCATEGORY_RULES.get(magazine, [])
    lowered_name = product_name.lower()
    for subcategory, keywords in rules:
        if not keywords:
            continue
        for keyword in keywords:
            if keyword.lower() in lowered_name:
                return subcategory
    return "その他"


def extract_brand(product_name: str) -> str:
    normalized_name = product_name.strip()
    lowered_name = normalized_name.lower()
    for brand in sorted(KNOWN_BRANDS, key=len, reverse=True):
        if lowered_name.startswith(brand.lower()):
            return brand
    fallback_match = FALLBACK_BRAND_RE.match(normalized_name)
    if fallback_match:
        return fallback_match.group(1)
    return "不明"


def sorted_products(products: dict[str, ProductAggregate]) -> list[ProductAggregate]:
    return sorted(
        products.values(),
        key=lambda item: (item.appear_count, item.last_mentioned),
        reverse=True,
    )


def diversify_products(
    magazine: str,
    candidates: list[ProductAggregate],
    target_count: int = 15,
) -> tuple[list[ProductAggregate], dict[str, str], dict[str, str]]:
    candidate_pool = candidates[:50]
    subcategories = {
        product_key(item.amazon_url, item.asin): classify_subcategory(magazine, item.product_name)
        for item in candidate_pool
    }
    brands = {
        product_key(item.amazon_url, item.asin): extract_brand(item.product_name)
        for item in candidate_pool
    }
    selected: list[ProductAggregate] = []
    selected_keys: set[str] = set()

    for subcategory_limit, brand_limit in [(3, 3), (4, 4), (5, 5), (999, 999)]:
        subcategory_count = Counter(
            subcategories[product_key(item.amazon_url, item.asin)] for item in selected
        )
        brand_count = Counter(brands[product_key(item.amazon_url, item.asin)] for item in selected)
        for item in candidate_pool:
            if len(selected) >= target_count:
                break
            key = product_key(item.amazon_url, item.asin)
            if key in selected_keys:
                continue
            subcategory = subcategories[key]
            brand = brands[key]
            if subcategory_count[subcategory] >= subcategory_limit:
                continue
            if brand_count[brand] >= brand_limit:
                continue
            selected.append(item)
            selected_keys.add(key)
            subcategory_count[subcategory] += 1
            brand_count[brand] += 1
        if len(selected) >= target_count:
            break

    return selected[:target_count], subcategories, brands


def extract_mentions(article_path: Path) -> tuple[list[ArticleMention], list[dict[str, Any]]]:
    article_date_match = DATE_RE.match(article_path.name)
    article_date = article_date_match.group(1) if article_date_match else ""
    mentions: list[ArticleMention] = []
    failures: list[dict[str, Any]] = []
    current_heading = ""

    lines = article_path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(lines, start=1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            current_heading = clean_product_name(heading_match.group(1))
            continue

        for url_match in AMAZON_URL_RE.finditer(line):
            raw_url = url_match.group(0).rstrip(".,、。)")
            asin_match = ASIN_RE.match(raw_url)
            asin = asin_match.group(1) if asin_match else None
            if "amazon.co.jp" in raw_url and not asin:
                failures.append(
                    {
                        "article": article_path.name,
                        "line": line_number,
                        "url": raw_url,
                        "reason": "asin_not_found",
                    }
                )
                continue
            mentions.append(
                ArticleMention(
                    article=article_path.name,
                    mentioned_date=article_date,
                    product_name=current_heading,
                    amazon_url=canonical_url(raw_url, asin),
                    asin=asin,
                )
            )
    return mentions, failures


def aggregate(generated_at: str) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, int]]:
    month_metadata = {
        month_dir: load_metadata(month_dir)
        for month_dir in sorted(ARTICLE_ROOT.iterdir())
        if month_dir.is_dir()
    }
    by_magazine: dict[str, dict[str, ProductAggregate]] = {
        magazine: {} for magazine in MAGAZINES
    }
    failures: list[dict[str, Any]] = []
    stats = defaultdict(int)

    for article_path in sorted(ARTICLE_ROOT.glob("*/*.md")):
        if article_path.name == "_metadata.json":
            continue
        stats["md_files"] += 1
        article_meta = month_metadata.get(article_path.parent, {}).get(article_path.name)
        if not article_meta:
            stats["skipped_no_metadata"] += 1
            continue
        magazine, issue = normalize_magazine(article_meta)
        if issue == "mapped_from_category":
            stats["mapped_from_category"] += 1
        elif issue:
            stats[f"skipped_{issue.split(':', 1)[0]}"] += 1
        if not magazine:
            continue

        mentions, article_failures = extract_mentions(article_path)
        failures.extend(article_failures)
        if not mentions:
            stats["articles_without_links"] += 1
            continue
        stats["source_article_count"] += 1

        seen_keys: set[str] = set()
        for mention in mentions:
            key = product_key(mention.amazon_url, mention.asin)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            products = by_magazine[magazine]
            if key not in products:
                products[key] = ProductAggregate(
                    asin=mention.asin,
                    product_name=mention.product_name,
                    amazon_url=mention.amazon_url,
                )
            products[key].add(mention)

    result_magazines: dict[str, list[dict[str, Any]]] = {}
    for magazine in MAGAZINES:
        ranked = sorted_products(by_magazine[magazine])
        selected, subcategories, brands = diversify_products(magazine, ranked)
        result_magazines[magazine] = [
            {
                "rank": rank,
                "asin": item.asin,
                "product_name": item.product_name,
                "subcategory": subcategories[product_key(item.amazon_url, item.asin)],
                "brand": brands[product_key(item.amazon_url, item.asin)],
                "amazon_url": item.amazon_url,
                "appear_count": item.appear_count,
                "last_mentioned": item.last_mentioned,
                "source_articles": item.source_articles,
            }
            for rank, item in enumerate(selected, start=1)
        ]
        if len(result_magazines[magazine]) < 5:
            stats[f"magazine_under_5:{magazine}"] = len(result_magazines[magazine])
        covered_subcategories = {
            item["subcategory"]
            for item in result_magazines[magazine]
            if item["subcategory"] != "その他"
        }
        other_count = sum(
            1 for item in result_magazines[magazine] if item["subcategory"] == "その他"
        )
        max_brand_count = max(
            Counter(item["brand"] for item in result_magazines[magazine]).values(),
            default=0,
        )
        if len(covered_subcategories) < 5:
            stats[f"magazine_under_5_subcategories:{magazine}"] = len(covered_subcategories)
        if other_count > 5:
            stats[f"magazine_other_over_5:{magazine}"] = other_count
        if max_brand_count >= 4:
            stats[f"magazine_brand_over_3:{magazine}"] = max_brand_count

    result = {
        "generated_at": generated_at,
        "source_article_count": stats["source_article_count"],
        "magazines": result_magazines,
    }
    return result, failures, dict(stats)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generated-at",
        default=os.environ.get("CURRENT_DATE", date.today().isoformat()),
        help="Date string written to generated_at.",
    )
    args = parser.parse_args()

    result, failures, stats = aggregate(args.generated_at)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    FAILURE_PATH.write_text(
        json.dumps(
            {
                "generated_at": args.generated_at,
                "failure_count": len(failures),
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"generated: {OUTPUT_PATH}")
    print(f"extraction_failures: {FAILURE_PATH} ({len(failures)} failures)")
    print(f"source_article_count: {result['source_article_count']}")
    print(f"skipped_no_metadata: {stats.get('skipped_no_metadata', 0)}")
    print(f"skipped_missing_magazine: {stats.get('skipped_missing_magazine', 0)}")
    print(f"mapped_from_category: {stats.get('mapped_from_category', 0)}")
    for magazine, items in result["magazines"].items():
        print(f"{magazine}: {len(items)} products")
        if len(items) < 5:
            print(f"WARNING: {magazine} has fewer than 5 products")
    print("=== 多様化分布 ===")
    for magazine, items in result["magazines"].items():
        subcategory_count = Counter(item["subcategory"] for item in items)
        brand_count = Counter(item["brand"] for item in items)
        covered_subcategories = len(subcategory_count)
        subcategory_summary = ", ".join(
            f"{subcategory}={count}" for subcategory, count in subcategory_count.most_common()
        )
        brand_summary = ", ".join(
            f"{brand}={count}" for brand, count in brand_count.most_common(5)
        )
        print(f"{magazine}:")
        print(f"  サブカテゴリ分布: {subcategory_summary}")
        print(f"  ブランド分布: {brand_summary}")
        print(f"  カバーサブカテゴリ数: {covered_subcategories}")
        if subcategory_count.get("その他", 0) > 5:
            print(f"  WARNING: その他が{subcategory_count['その他']}件あります")
        if covered_subcategories < 5:
            print(f"  WARNING: サブカテゴリカバー数が{covered_subcategories}件です")
        if brand_count and brand_count.most_common(1)[0][1] >= 4:
            brand, count = brand_count.most_common(1)[0]
            print(f"  WARNING: {brand} が{count}件あります")
    print("=== 商品名サンプル（修正後） ===")
    for magazine, items in result["magazines"].items():
        print(f"{magazine}:")
        for item in items[:5]:
            print(f"  {item['rank']}. {item['product_name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
