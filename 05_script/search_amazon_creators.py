#!/usr/bin/env python3
"""
Amazon Creators API を使用した商品検索スクリプト
レビュー数・星評価を含む商品情報を取得します
"""

import sys
import json
import time
from amazon_creatorsapi.api import AmazonCreatorsApi, SearchItemsResource

# Creators API 認証情報
CREDENTIAL_ID = "38m4h91ecrubjs1s2oq9tf8rik"
CREDENTIAL_SECRET = "s883g8vpc7rnlge0g6k57a6ijci450e1v5nunac0ul5b05eah3f"
PARTNER_TAG = "daily-gadget-22"
COUNTRY = "JP"

def search_product(api, query):
    """
    品質チェック付き商品検索（全カテゴリ対応）
    
    検索上位3件を取得し、除外ワードがない商品を優先的に選定。
    レビューデータの代替として、Amazonの検索順位を信頼する方式。
    
    Args:
        api: AmazonCreatorsApi インスタンス
        query: 検索キーワード
    
    Returns:
        dict: 商品情報（title, url, price, features, image_url, query）
    """
    # 除外ワード（全カテゴリ共通）
    EXCLUDE_KEYWORDS = ["展示品", "中古", "訳あり", "ジャンク", "B品", "アウトレット", "整備済み", "再生品"]
    
    try:
        # 上位3件を取得（品質フィルター用）
        items = api.search_items(
            keywords=query,
            item_count=3,  # 上位3件から選定
            resources=[
                SearchItemsResource.ITEM_INFO_DOT_TITLE,
                SearchItemsResource.ITEM_INFO_DOT_FEATURES,
                SearchItemsResource.OFFERS_V2_DOT_LISTINGS_DOT_PRICE,
                SearchItemsResource.IMAGES_DOT_PRIMARY_DOT_LARGE
            ]
        )
        
        if not items or not items.items:
            print(f"  ⚠️  No results found for: {query}", file=sys.stderr)
            return None
        
        # 除外ワードチェック：上位3件から最適な商品を選定
        selected_item = None
        for item in items.items:
            title = item.item_info.title.display_value if item.item_info and item.item_info.title else ""
            
            # 除外ワードがなければ採用
            if not any(kw in title for kw in EXCLUDE_KEYWORDS):
                selected_item = item
                print(f"  ✅ Selected (no exclude words): {title[:50]}...", file=sys.stderr)
                break
        
        # 全て除外された場合は1件目を採用（最終手段）
        if not selected_item:
            selected_item = items.items[0]
            title = selected_item.item_info.title.display_value if selected_item.item_info and selected_item.item_info.title else ""
            print(f"  ⚠️  All items have exclude words, using top result: {title[:50]}...", file=sys.stderr)
        
        item = selected_item
        
        # 商品情報の抽出
        title = item.item_info.title.display_value if item.item_info and item.item_info.title else "N/A"
        url = item.detail_page_url if item.detail_page_url else "N/A"
        
        # 価格情報（offersV2 を使用）
        price = "N/A"
        if hasattr(item, 'offers_v2') and item.offers_v2 and hasattr(item.offers_v2, 'listings') and item.offers_v2.listings and len(item.offers_v2.listings) > 0:
            listing = item.offers_v2.listings[0]
            if hasattr(listing, 'price') and listing.price and hasattr(listing.price, 'display_amount'):
                price = listing.price.display_amount
        
        # Features（商品特徴）
        features = []
        if item.item_info and hasattr(item.item_info, 'features') and item.item_info.features and hasattr(item.item_info.features, 'display_values'):
            features = item.item_info.features.display_values
        
        # 画像URL
        image_url = ""
        if hasattr(item, 'images') and item.images and hasattr(item.images, 'primary') and item.images.primary and hasattr(item.images.primary, 'large'):
            image_url = item.images.primary.large.url
        
        return {
            "title": title,
            "url": url,
            "price": price,
            "image_url": image_url,
            "features": features,
            "query": query
        }
        
    except Exception as e:
        print(f"  ❌ Error searching for '{query}': {str(e)}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 search_amazon_creators.py <partner_tag> [query1] [query2] ...", file=sys.stderr)
        print("If no queries provided, uses default smart cooking appliance list", file=sys.stderr)
        sys.exit(1)
    
    # Partner Tag は引数から取得（互換性のため）
    partner_tag = sys.argv[1]
    
    # クエリリスト（引数で指定されていない場合はデフォルト）
    if len(sys.argv) > 2:
        queries = sys.argv[2:]
    else:
        # デフォルト: スマート調理家電
        queries = [
            "象印 炊飯器 スマホ",
            "パナソニック ビストロ スマホ",
            "シャープ ヘルシオ ホットクック",
            "アイリスオーヤマ 電気圧力鍋 スマホ",
            "ティファール クックフォーミー",
            "バルミューダ トースター スマホ",
            "siroca 電気圧力鍋 スマホ"
        ]
    
    # API インスタンスの作成
    print(f"🔧 Initializing Amazon Creators API (Partner Tag: {partner_tag})...", file=sys.stderr)
    api = AmazonCreatorsApi(
        credential_id=CREDENTIAL_ID,
        credential_secret=CREDENTIAL_SECRET,
        tag=partner_tag,
        country=COUNTRY,
        version="2.3"
    )
    
    all_items = []
    
    print(f"🔍 Searching for {len(queries)} products...\n", file=sys.stderr)
    
    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] Searching: {query}", file=sys.stderr)
        result = search_product(api, query)
        
        if result:
            all_items.append(result)
        
        # API レート制限対策（1秒待機）
        if i < len(queries):
            time.sleep(1)
    
    # JSON 出力（標準出力へ）
    print(json.dumps(all_items, indent=2, ensure_ascii=False))
    
    print(f"\n✅ Successfully retrieved {len(all_items)}/{len(queries)} products", file=sys.stderr)


if __name__ == "__main__":
    main()
