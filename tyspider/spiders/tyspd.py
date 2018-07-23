# -*- coding: utf-8 -*-

import scrapy
from tyspider.items import TyspiderItem

PAGE_COUNT_MAX = 2
KEY_WORDS = [
    'rct'
]


class TySpider(scrapy.Spider):
    name = "tyspd"
    allowed_domain = ['t66y.com']
    start_urls = [
        'http://t66y.com/thread0806.php?fid=2&search=&page=1'
    ]
    page_count = 1

    def parse(self, response):
        movies = response.css('td.tal')
        for movie in movies:
            title = movie.css('a::text').extract_first()
            if not title:
                continue
            encoded_title = title.encode('utf-8')
            for key_word in KEY_WORDS:
                if key_word in encoded_title:
                    link = movie.css('a::attr(href)').extract_first()
                    item = TyspiderItem(
                        name=title,
                        url=self._format_link(link),
                        page_url=response.url,
                        page_count=self.page_count)
                    yield item

        self.page_count += 1
        if self.page_count <= PAGE_COUNT_MAX:
            pages = response.css('div.pages a')
            next_page = pages[len(pages) - 2].xpath('@href').extract_first()
            print next_page
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def _format_link(self, link):
        return 'http://t66y.com/{0}'.format(link)
