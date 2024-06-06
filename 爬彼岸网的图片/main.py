# bian_pic.py
 
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
 
from bian.items import BianItem
 
 
class BianPicSpider(CrawlSpider):
    name = "bian_pic"
    # allowed_domains = ["pic.netbian.com"]
    base_url = "https://pic.netbian.com"
    start_urls = [
        "https://pic.netbian.com/4kdongman",
        "https://pic.netbian.com/4kyouxi",
        "https://pic.netbian.com/4kmeinv",
        "https://pic.netbian.com/4kfengjing",
        "https://pic.netbian.com/4kyingshi",
        "https://pic.netbian.com/4kqiche",
        "https://pic.netbian.com/4krenwu",
        "https://pic.netbian.com/4kdongwu",
        "https://pic.netbian.com/4kzongjiao",
        "https://pic.netbian.com/4kbeijing",
        "https://pic.netbian.com/pingban",
        "https://pic.netbian.com/shoujibizhi",
    ]
 
    link = LinkExtractor(restrict_xpaths='//*[@class="page"]/a')
    rules = (Rule(link, callback="parse_item", follow=True),)
 
    def parse_item(self, response):
        a_list = response.xpath('//*[@class="slist"]/ul/li/a')
        for a in a_list:
            if a.xpath('./@target').extract_first():
                href = a.xpath('./@href').extract_first()
                item = BianItem()
                item["href"] = href
                yield scrapy.Request(url=self.base_url + href, callback=self.parse_detail)
 
    def parse_detail(self, response):
        src = response.xpath('//*[@id="img"]/img/@src').extract_first()
        title = response.xpath('//*[@id="img"]/img/@title').extract_first()
        item = BianItem()
        item["src"] = self.base_url + src
        item["title"] = title
        yield item