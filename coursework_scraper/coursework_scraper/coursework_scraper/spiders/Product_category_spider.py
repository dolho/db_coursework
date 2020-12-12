import scrapy
import json
from scrapy import Selector

class EShopSpider(scrapy.Spider):
    name = "product_category"

    def start_requests(self):
        urls = [
            'https://rozetka.com.ua/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        links = []

        app_root = response.css("app-root")[0]
        raw_links = app_root.xpath("//a[contains(@class, 'menu-categories__link') and contains(@class, 'js-menu-categories__link')]")
        for i in raw_links:
            yield {"category": i.css("a::text").get().decode("utf-8"), "link": i.css("a::attr(href)").get()}

        # links = raw_links.css("a::text").getall()
        # links = Selector(text=response.body).xpath('//app-root/a/text()')

        with open('links.json', 'w', encoding="utf-8") as f:
            f.write(json.dumps(links, indent=4, sort_keys=True, ensure_ascii=False)) #json.dumps( , indent=4, sort_keys=True)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')