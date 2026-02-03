import sys
import os
import json
import hashlib
import hmac
import datetime
import urllib.request
import urllib.parse
import time

# Configuration
ACCESS_KEY = "AKPAC2JB3E1767047306"
SECRET_KEY = "8+L70fp5siHCHbUvYGwVkd1DVMjqd+F58akP/K9A"
HOST = 'webservices.amazon.co.jp'
REGION = 'us-west-2'
ENDPOINT = 'https://webservices.amazon.co.jp/paapi5/searchitems'

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def search_products(keywords, partner_tag, item_count=1):
    method = 'POST'
    service = 'ProductAdvertisingAPI'
    
    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')

    canonical_uri = '/paapi5/searchitems'
    canonical_querystring = ''
    canonical_headers = 'content-encoding:amz-1.0\n' + 'host:' + HOST + '\n' + 'x-amz-date:' + amz_date + '\n' + 'x-amz-target:com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems\n'
    signed_headers = 'content-encoding;host;x-amz-date;x-amz-target'
    
    payload = {
        "Keywords": keywords,
        "Resources": [
            "ItemInfo.Title",
            "ItemInfo.Features",
            "Offers.Listings.Price",
            "Images.Primary.Large",
            "CustomerReviews.Count",
            "CustomerReviews.StarRating"
        ],
        "PartnerTag": partner_tag,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.co.jp",
        "ItemCount": item_count
    }
    
    payload_json = json.dumps(payload)
    payload_hash = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()

    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = date_stamp + '/' + REGION + '/' + service + '/aws4_request'
    string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    signing_key = getSignatureKey(SECRET_KEY, date_stamp, REGION, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = algorithm + ' ' + 'Credential=' + ACCESS_KEY + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    headers = {
        'host': HOST,
        'content-encoding': 'amz-1.0',
        'x-amz-date': amz_date,
        'x-amz-target': 'com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems',
        'Authorization': authorization_header,
        'Content-Type': 'application/json; charset=utf-8'
    }

    req = urllib.request.Request(ENDPOINT, data=payload_json.encode('utf-8'), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python search_custom_list.py <partner_tag>")
        sys.exit(1)
        
    partner_tag = sys.argv[1]
    
    # List of queries to search for
    queries = [
        "SwitchBot スマートロック Pro",
        "キャンディハウス セサミ5",
        "Qrio Lock Q-SL2",
        "SADIOT LOCK 2",
        "Lockin G30 スマートロック",
        "Philips EasyKey Alpha",
        "SwitchBot スマートロック Lite",
        "Yale Linus スマートロック",
        "美和ロック PiACK II",
        "ミネベアミツミ SADIO LOCK"
    ]
    
    all_items = []
    
    for query in queries:
        print(f"Searching for: {query}")
        result = search_products(query, partner_tag, item_count=1) # Get top 1 result for each specific query
        
        if "SearchResult" in result:
            items = result["SearchResult"].get("Items", [])
            for item in items:
                title = item["ItemInfo"]["Title"]["DisplayValue"]
                url = item["DetailPageURL"]
                price = "N/A"
                if "Offers" in item and "Listings" in item["Offers"] and len(item["Offers"]["Listings"]) > 0:
                    listing = item["Offers"]["Listings"][0]
                    if "Price" in listing and "DisplayAmount" in listing["Price"]:
                        price = listing["Price"]["DisplayAmount"]
                
                features = []
                if "ItemInfo" in item and "Features" in item["ItemInfo"] and "DisplayValues" in item["ItemInfo"]["Features"]:
                     features = item["ItemInfo"]["Features"]["DisplayValues"]

                image_url = ""
                if "Images" in item and "Primary" in item["Images"] and "Large" in item["Images"]["Primary"]:
                    image_url = item["Images"]["Primary"]["Large"]["URL"]

                review_count = 0
                star_rating = 0.0
                if "CustomerReviews" in item:
                    if "Count" in item["CustomerReviews"]:
                        review_count = item["CustomerReviews"]["Count"]
                    if "StarRating" in item["CustomerReviews"] and "Value" in item["CustomerReviews"]["StarRating"]:
                        star_rating = item["CustomerReviews"]["StarRating"]["Value"]

                all_items.append({
                    "title": title,
                    "url": url,
                    "price": price,
                    "image_url": image_url,
                    "features": features,
                    "review_count": review_count,
                    "star_rating": star_rating,
                    "query": query # Keep track of which query found this
                })
        else:
            print(f"Error searching for {query}: {result}")
        
        time.sleep(1) # Be nice to the API
    
    output_path = os.path.join(os.path.dirname(__file__), 'temp_products.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    print(f"All results saved to {output_path}")

if __name__ == '__main__':
    main()
