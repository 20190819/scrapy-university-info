import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import copy
import re
from scrapy.utils.project import get_project_settings


class GkSpider(CrawlSpider):
    name = 'gk'
    settings = get_project_settings()
    allowed_domains = settings["ALLOWED_DOMAIN"]
    start_urls =settings["START_URLS"]

    rules = (
        Rule(LinkExtractor(allow=r'\/college\/list\/1\/1\/\d'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        tr_list = response.xpath("//div[@class='list']/table/tr")
        for tr in tr_list:
            detail_url = tr.xpath("./td[@class='college']/h3/a/@href").extract_first()
            title1=tr.xpath("./td[@class='rank']/a[1]/@title").extract_first()
            rank1 = tr.xpath("./td[@class='rank']/a[1]/text()").extract_first()
            title2 = tr.xpath("./td[@class='rank']/a[2]/@title").extract_first()
            rank2 = tr.xpath("./td[@class='rank']/a[2]/text()").extract_first()
			
            item['name'] = tr.xpath("./td[@class='college']/h3/a/text()").extract_first()
            item['area'] = tr.xpath("./td[@class='s3']/text()").extract_first()
            if(title1 and rank1):
                item['rank_in_country'] = str(title1)+str(rank1)
            else:
                item['rank_in_country'] = None
            if(title2 and rank2):
                item['rank_in_major'] = str(title2)+str(rank2)
            else:
                item['rank_in_major'] = None
            # 请求详情页
            yield scrapy.Request(
                response.urljoin(detail_url),
                callback=self.parse_detail,
                meta={"item": copy.deepcopy(item)}
            )

    def parse_detail(self, response):
        item = response.meta["item"]

        address=response.xpath("//div[@class='details']/p[1]/text()").extract_first()
        found_time=response.xpath("//div[contains(@class,'info')]/ul/li[4]/text()").extract_first()

        item['logo'] = response.xpath("//div[@class='college_logo']/img/@src").extract_first()
        item['tags'] = response.xpath("//div[@class='g-collegeTag']/span/@title").extract()
        item['type'] = response.xpath("//div[contains(@class,'info')]/ul/li[1]/text()").extract_first()
        item['level'] = response.xpath("//div[contains(@class,'info')]/ul/li[2]/text()").extract_first()
        item['subordinate'] = response.xpath("//div[contains(@class,'info')]/ul/li[3]/text()").extract_first()
        item['found_time'] =re.findall(r'([\w\d\w]+)',found_time)
        item['address'] = re.findall(r"([\w\d]+)",str(address))[0]
        yield item
