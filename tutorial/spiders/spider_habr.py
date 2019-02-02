from scrapy.loader import ItemLoader
from tutorial.items import HabrItem             #tutorial - название проекта  HabrItem - название класса в items.py
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HabrSpider(CrawlSpider):
    name = "spiderhabr"     #По этому названию spider будет запускаться
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="post__title"]/a'), callback='parse_item'),
    )
    start_urls = ["https://habr.com/ru/", "https://habr.com/ru/page2/"]

    def parse_item(self, response):
        l = ItemLoader(item=HabrItem(), response=response)
        l.add_xpath('url_post', './/meta[@property="og:url"]/@content')
        l.add_xpath('title_post', './/meta[@property="og:title"]/@content')
        l.add_xpath('tegs_post', './/li[@class="inline-list__item inline-list__item_tag"]/a/text()')
        #l.add_xpath('tegs_post', './/meta[@name="keywords"]/@content')
        l.add_xpath('url_related_articles_post', './/h3[@class="post-info__title post-info__title_large"]/a/@href')
        #l.add_xpath('url_related_articles_post', './/h3[@class="post-info__title post-info__title_large"]/a/text()', re=r'[^\s+].+')
        l.add_xpath('author_post', './/div[@class="post__wrapper"]//span[@class="user-info__nickname user-info__nickname_small"]/text()')
        return l.load_item()