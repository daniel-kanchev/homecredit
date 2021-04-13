import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from homecredit.items import Article
import requests
import json
import re


class homecreditSpider(scrapy.Spider):
    name = 'homecredit'
    start_urls = ['https://homecredit.kz/press-center/news/']

    def parse(self, response):
        json_response = json.loads(requests.get("https://homecredit.kz/api/public/v2/press-center/news?locale=ru",
                                                verify=False).text)
        articles = json_response["posts"]
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article['title']
            link = self.start_urls[0] + article['slug']
            date = article["createdAt"][:10]
            p = re.compile(r'<.*?>')
            content = p.sub('', article['text'])

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('link', link)
            item.add_value('content', content)

            yield item.load_item()
