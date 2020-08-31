import re
from urllib.parse import urlencode

import pymysql
import scrapy

from GoogleScholarCrawler import config
from GoogleScholarCrawler.items import PaperCitationItem


class CitationSpider(scrapy.Spider):
    name = 'citation'
    handle_httpstatus_list = [403, 429]
    url = 'https://scholar.google.com/scholar'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mysql, self.table = config.get_mysql()

    def start_requests(self):
        conn = pymysql.connect(**self.mysql)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        size = cursor.execute(
            'SELECT id, title FROM `{}`'
            ' WHERE id BETWEEN %s AND %s AND finished = 0'
            ' ORDER BY id LIMIT 100'.format(self.table),
            (self.lower, self.upper)
        )
        self.logger.info('lower = %s, upper = %s, size = %s', self.lower, self.upper, size)
        for r in cursor:
            yield scrapy.Request(
                self.url + '?' + urlencode({'q': r['title']}), self.parse,
                meta={'paper_id': r['id']}
            )

    def parse(self, response, **kwargs):
        paper_id = response.meta['paper_id']
        if response.status != 200 or not response.css('#gs_res_ccl'):
            self.logger.info('id = %s 又被封了。。 status = %s', paper_id, response.status)
            yield PaperCitationItem(paper_id=paper_id, status='blocked')
            return

        query_title = process_title(response.css('#gs_hdr_tsi::attr(value)').get())
        for paper_elem in response.css('#gs_res_ccl_mid > div.gs_r > div.gs_ri'):
            title = process_title(''.join(paper_elem.css('h3 > a *::text').getall()))
            if title == query_title:
                citation = 0
                for a_elem in paper_elem.css('div.gs_fl > a'):
                    if a_elem.attrib['href'].startswith('/scholar?cites='):
                        citation = int(a_elem.css('::text').re_first('\\d+'))
                        break
                self.logger.info('id = %s, citation = %s', paper_id, citation)
                yield PaperCitationItem(paper_id=paper_id, citation=citation, status='OK')
                break
        else:
            self.logger.info('id = %s 未找到', paper_id)
            yield PaperCitationItem(paper_id=paper_id, status='not found')


def process_title(title):
    title = re.sub(r'\[引用\]', '', title.lower(), 1)
    return re.sub(r'[^0-9a-z\u4e00\u9fa5]', '', title)
