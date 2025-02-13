import scrapy , json
from urllib.parse import urlencode
from  errors.items import TargetItem
API_KEY = '191b57436561ccf59beb0095bd745837'
def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'render': 'true'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

class target(scrapy.Spider):
    name = "target"
    def create_url(self,offset,cat_id):
        url = f"https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&category={cat_id}&channel=WEB&default_purchasability_filter=true&include_dmc_dmr=true&include_sponsored=true&new_search=false&offset={offset}&page=%2Fc%2F5xu0x&platform=desktop&pricing_store_id=1771&scheduled_delivery_store_id=1771&spellcheck=true&store_ids=1771%2C1768%2C1113%2C3374%2C1792&useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F131.0.0.0+Safari%2F537.36&visitor_id=0193493BA2390201AC5DD11244E549C6&zip=52404"
        return url  
    def start_requests(self):
        offset = 0
        total_pages = 5
        cat_id = "899qw"

        for i in range(total_pages): 
            url = self.create_url(offset, cat_id)
            scraper_api_url = get_scraperapi_url(url) 

            yield scrapy.Request(
                url=scraper_api_url,
                callback=self.parse
            )

            offset += 28
                    
        proxyurl=get_scraperapi_url(url=url)

        yield scrapy.Request(
                    url=proxyurl,
                    callback=self.parse,
                )
        
    def parse(self, response):
        
        data = response.json()
        filteredData = data["data"].get('search').get('products')
        for product in filteredData:
            item = TargetItem()
            item['title'] = product.get("item", {}).get("product_description", {}).get("title", "N/A")
            item['product_url'] = product.get("item", {}).get("enrichment", {}).get("buy_url", "N/A")
            item['is_sponsored_sku'] =product.get("is_sponsored_sku", False)
            item['price'] = product.get("price", {}).get("formatted_current_price", "N/A")
            item['rating'] = product.get("ratings_and_reviews", {}).get("statistics", {}).get("rating", {}).get("average", "N/A")
            item['review_count'] = product.get("ratings_and_reviews", {}).get("statistics", {}).get("rating", {}).get("count", 0)
            item['primary_image_url'] = product.get("item", {}).get("enrichment", {}).get("images", {}).get("primary_image_url", "N/A")
            item['tcin'] = product.get("tcin", "N/A")
            item['alternate_image_urls'] = product.get("item", {}).get("enrichment", {}).get("images", {}).get("alternate_image_urls", [])
            item['class_id'] = product.get("item", {}).get("merchandise_classification", {}).get("class_id", "N/A")
            item['department_id'] = product.get("item", {}).get("merchandise_classification", {}).get("department_id", "N/A")
            item['dpci'] = product.get("item", {}).get("compliance", {}).get("dpci", "N/A")
            item['primary_brand'] = product.get("item", {}).get("primary_brand", "N/A")
            item['product_description'] = product.get("item", {}).get("product_description", "N/A")

            yield item
        # Save JSON data to a file (append to existing file)
        # with open("test.json", "a", encoding="utf-8") as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)
        #     f.write("\n")  # New line for each page’s data

