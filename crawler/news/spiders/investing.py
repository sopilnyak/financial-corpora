import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
import re
from datetime import datetime, timedelta
from .. import items


def parse_timestamp(timestamp):
    if 'ago' in timestamp:
        # Remove unnecessary information, e.g. "N minutes ago"
        timestamp = timestamp[timestamp.find('(') + 1:timestamp.find(')')]

    return datetime.strptime(timestamp, '%b %d, %Y %I:%M%p ET')


class InvestingSpider(CrawlSpider):
    name = 'investing'
    base_url = 'https://investing.com/news/stock-market-news/'
    input_format = '%Y-%m-%d'
    rules = (
        Rule(
            LinkExtractor(
                allow='.*-[0-9]+',
                allow_domains='investing.com',
                restrict_xpaths='//section[@id="leftColumn"]//*[@class="title"]'
            ),
            callback='parse_item'
        ),
    )
    start_date = datetime.now() - timedelta(days=3)
    end_date = datetime.now()
    do_continue = True
    
    def __init__(self, start='', end='today', *args, **kwargs):
        super(InvestingSpider, self).__init__(*args, **kwargs)

        if start:
            self.start_date = datetime.strptime(start, self.input_format)
        if end != 'today':
            # Add 1 day to cover the full end_date day
            # supposing 'end_date = Oct 5' means Oct 5 23:59, not Oct 5 00:00
            self.end_date = datetime.strptime(end, self.input_format) + timedelta(days=1)

    def start_requests(self):
        self.logger.info('Start date: %s, end date: %s' %
                         (datetime.strftime(self.start_date, self.input_format),
                          datetime.strftime(self.end_date, self.input_format)))
        page = 1
        while self.do_continue:
            yield scrapy.Request(self.base_url + str(page))
            page += 1
            # TODO: max number of pages?

    def parse_item(self, response):
        self.logger.info('Crawling url {}'.format(response.url))
        selector = Selector(response=response)
        item = items.NewsItem()

        # Extract and process timestamp
        timestamp = selector.xpath('//div[@class="contentSectionDetails"]//span/text()').extract_first()
        try:
            timestamp = parse_timestamp(timestamp)
            if timestamp < self.start_date:
                # Too old article, stop crawling
                self.do_continue = False
                return item
            if timestamp > self.end_date:
                # Too new article, skipping
                return item
        except ValueError:
            self.logger.warning('Unrecognized timestamp "{}"'.format(timestamp))

        item['timestamp'] = timestamp.strftime('%Y-%m-%d %H:%M')
        item['date'] = timestamp.strftime('%Y-%m-%d')

        # Extract article id
        item['url'] = response.url
        article_id_regex = re.compile('.*-([0-9]+)')
        item['id'] = article_id_regex.findall(item['url'])[-1]

        # Extract meta information
        item['language'] = 'en'
        item['agency'] = selector.xpath('//meta[@property="article:author"]/@content').extract_first()
        item['title'] = selector.xpath('//h1[@class="articleHeader"]/text()').extract_first()
        item['category'] = selector.xpath('//div[@class="contentSectionDetails"]//a/text()').extract_first()

        image = selector.xpath('//img[@id="carouselImage"]')
        item['image_url'] = image.xpath('./@src').extract_first()
        item['image_alt'] = image.xpath('./@alt').extract_first()

        # Extract author from text
        possible_author = selector.xpath('//div[@class="WYSIWYG articlePage"]//p//text()').extract_first()
        item['author'] = possible_author[3:] if possible_author and possible_author[:3] == 'By ' else 'unknown'

        # Extract main text
        paragraphs = selector.xpath('//div[@class="WYSIWYG articlePage"]//p | //div[@class="WYSIWYG articlePage"]//li')
        item['paragraphs'] = [''.join(paragraph.xpath('.//text()').extract()) for paragraph in paragraphs]
        if item['author'] != 'unknown':
            item['paragraphs'] = item['paragraphs'][1:]  # Author is in the first paragraph

        return item
