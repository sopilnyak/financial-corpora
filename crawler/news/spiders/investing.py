from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
import re
import os


class InvestingSpider(CrawlSpider):
    name = 'investing'
    start_urls = ['https://investing.com/news/stock-market-news']
    rules = (
        Rule(
            LinkExtractor(
                allow='.*-[0-9]+',
                allow_domains='investing.com',
                restrict_xpaths='//*[contains(@class,"title")]'
            ),
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        self.logger.info('Crawling url %s', response.url)
        selector = Selector(response=response).xpath('//div[@class="WYSIWYG articlePage"]/p/text()')
        paragraphs = selector.extract()

        article_id_regex = re.compile('.*-([0-9]+)')
        output_directory = '../investing-com-data'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        filename = 'investing-stock-%s.txt' % article_id_regex.findall(response.url)[-1]
        with open(os.path.join(output_directory, filename), 'w') as file:
            file.writelines(paragraphs)

        self.logger.info('Saved file %s ', filename)
