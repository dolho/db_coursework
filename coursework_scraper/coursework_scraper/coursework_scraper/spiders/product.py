import scrapy
import json
from scrapy import Selector

class ProductCrawlSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ['rozetka.com.ua']

    def start_requests(self):
        with open('sub-products.json', 'r') as f:
            self.links = json.loads(f.read())
        start_urls = []
        for i in self.links:
            yield scrapy.Request(url=i['link'], callback=self.parse, meta={'category': i['category'],
                                                                           'sub_category': i['sub_category_name']})

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        # links = []
        catalog = response.xpath("//section[contains(@class, 'content') and contains(@class, 'content_type_catalog')]")
        li_s = catalog.xpath(".//li[contains(@class, 'catalog-grid__cell') and contains(@class, 'catalog-grid__cell_type_slim')] ")
        for i in li_s:
            name = i.xpath(".//span[contains(@class, 'goods-tile__title')]/text()").get().strip()
            href = i.xpath(".//a[contains(@class, 'goods-tile__heading')]/@href").get()
            cost = i.xpath(".//span[contains(@class, 'goods-tile__price-value')]/text()").get()
            currency = i.xpath(".//span[contains(@class, 'goods-tile__price-currency')]/text()").get()
            cost = cost.replace(u'\xa0', u'')
            yield {'category': response.meta['category'], 'sub_category': response.meta['sub_category'],
                   'name': name.strip(), 'cost': cost.strip(), 'currency': currency.strip(), 'link': href}
        next_page = response.xpath("//a[contains(@class, 'button') and contains(@class, 'pagination__direction') and contains(@class, 'pagination__direction_type_forward')]/@href").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, meta=response.meta)

        # with open('checker.txt', 'w') as f:
        #     f.write(str(self.links[0][0]))






        # links = raw_links.css("a::text").getall()
        # links = Selector(text=response.body).xpath('//app-root/a/text()')

        # with open('links.json', 'w', encoding="utf-8") as f:
        #     f.write(json.dumps(links, indent=4, sort_keys=True, ensure_ascii=False)) #json.dumps( , indent=4, sort_keys=True)
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')