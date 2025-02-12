import scrapy , json 
from urllib.parse import urlencode
from  errors.items import TargetItem
API_KEY = ''
def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'render': 'true'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url
class target(scrapy.Spider):
    name = "target"
    start_urls = [
        "https://redsky.target.com/redsky_aggregations/v1/web/product_summary_with_fulfillment_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcins=85978622%2C85978622%2C93124207%2C89401491%2C88413607%2C83388339%2C81804770%2C82290116%2C79757338%2C92268975%2C90786725%2C90294248%2C92429369%2C92273435%2C51530146%2C85978618%2C89827259%2C92146819%2C88533013%2C83648149%2C88533065%2C91947365%2C52191759%2C91195008%2C88999834&store_id=1072&zip=43230&state=OH&latitude=40.040&longitude=-82.860&scheduled_delivery_store_id=2487&paid_membership=false&base_membership=false&card_membership=false&required_store_id=1072&skip_price_promo=true&visitor_id=0194F516FA8A0201AA9132B5AE021039&channel=WEB&page=%2Fc%2F5aazn"
    ]

    
    def start_requests(self):
        for url in self.start_urls:

            proxy_url = get_scraperapi_url(url)  # Get proxy URL
            yield scrapy.Request(
                proxy_url,
                headers=self.settings.get("DEFAULT_REQUEST_HEADERS"),
                callback=self.parse
            )


    def parse(self, response):
        #print(response.text)  # or process the JSON response
        data = response.json()
        filteredData = data["data"].get("product_summaries", [])
        for product in filteredData:
            item = TargetItem()
            item['title'] = product.get("item", {}).get("product_description", {}).get("title", "N/A")
            item['buy_url'] = product.get("item", {}).get("enrichment", {}).get("buy_url", "N/A")
            item['is_sponsored'] = product.get("item", {}).get("is_limited_time_offer", False)
            yield item
