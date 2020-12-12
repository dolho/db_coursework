import scrapy
import json
from scrapy import Selector

class SubCategorySpider(scrapy.Spider):
    name = "sub-products"
    current_category_number = -1

    def start_requests(self):
        with open('products.json', 'r') as f:
            self.links = json.loads(f.read())
        # We save links to add main category to json when sub-category parsed
        # links have stricture [[category_name, link]]
        urls = []

        for i in self.links:
            yield scrapy.Request(url=i["link"], callback=self.parse, meta={"category": i['category']})

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        links = []

        ul = response.xpath("//ul[contains(@class, 'portal-grid') and contains(@class, 'portal-grid_type_1_6')]")
        for j in ul:
            li_s = j.xpath(".//li[contains(@class, 'portal-grid__cell')]")
            self.current_category_number += 1
            for i in li_s:
                name = i.css("a::text").get().strip()
                href = i.css("a::attr(href)").get()
                yield {'category': response.meta['category'], 'sub_category_name': name, 'link': href}
