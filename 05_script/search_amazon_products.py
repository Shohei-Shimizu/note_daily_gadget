import sys
import os
import json
import hashlib
import hmac
import datetime
import urllib.request
import urllib.parse

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

def search_products(keywords, partner_tag, item_count=10):
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
            "Images.Primary.Large"
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
    if len(sys.argv) < 3:
        print("Usage: python search_amazon_products.py <partner_tag> <keywords>")
        sys.exit(1)
        
    partner_tag = sys.argv[1]
    keywords = sys.argv[2]
    
    result = search_products(keywords, partner_tag)
    
    if "SearchResult" in result:
        items = result["SearchResult"].get("Items", [])
        output = []
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

            # 画像URLを取得
            image_url = ""
            if "Images" in item and "Primary" in item["Images"] and "Large" in item["Images"]["Primary"]:
                image_url = item["Images"]["Primary"]["Large"]["URL"]

            output.append({
                "title": title,
                "url": url,
                "price": price,
                "image_url": image_url,
                "features": features
            })
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
